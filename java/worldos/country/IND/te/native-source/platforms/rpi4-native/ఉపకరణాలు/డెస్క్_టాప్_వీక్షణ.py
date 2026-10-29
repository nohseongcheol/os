#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, కీ_మూల్యం 입력은 자체 కెర్నల్_మూల్యం UART로 전달한다. localhost 전용, 단일 నియంత్రణ_మూల్యం 클라이언트.
RFB 3.8: https://www.rfc-editor.org/rfc/rfc6143.html
"""
import argparse
from contextlib import ExitStack
from pathlib import Path
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
from అమలు_చేయి_ఆదేశం import ఆదేశము
from local_input import create


def 정확한값(소켓, పరిమాణం):
    డేటా = bytearray()
    while len(డేటా) < పరిమాణం:
        조각 = 소켓.recv(పరిమాణం - len(డేటా))
        if not 조각: raise EOFError()
        డేటా.extend(조각)
    return bytes(డేటా)


class కీబోర్డు:
    def __init__(자신, పంపు, 입력방식알림=None):
        자신.바이트전송 = పంపు; 자신.సవరణ_మీట = set(); 자신.క్లిప్_బోర్డ్_మూల్యం = b''
        자신.한글조합기 = create(పంపు, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.మారు_కీ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def పంపు(자신, డేటా):
        자신.한글조합기.조합확정()
        자신.바이트전송(డేటా)

    def మారు_మోడ్(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, కీ_చిహ్నం):
        if కీ_చిహ్నం in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.సవరణ_మీట.add(కీ_చిహ్నం)
            else: 자신.సవరణ_మీట.discard(కీ_చిహ్నం)
            return
        if not 누르는중:
            자신.మారు_కీ.discard(కీ_చిహ్నం)
            return
        CTRL_మీట = bool(자신.సవరణ_మీట & {0xffe3, 0xffe4})
        SHIFT_మీట = bool(자신.సవరణ_మీట & {0xffe1, 0xffe2})
        if CTRL_మీట and SHIFT_మీట and కీ_చిహ్నం in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if కీ_చిహ్నం in (32,0xff0d):
                try:
                    మూల్యం=int(자신.유니코드입력,16)
                    if 32<=మూల్యం<=0x10ffff and not 0xd800<=మూల్యం<=0xdfff: 자신.పంపు(chr(మూల్యం).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif కీ_చిహ్నం==0xff1b: 자신.유니코드입력=None
            elif కీ_చిహ్నం==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif కీ_చిహ్నం<128 and chr(కీ_చిహ్నం) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(కీ_చిహ్నం)
            return
        if కీ_చిహ్నం in (0xff31,0xffc6) or కీ_చిహ్నం==32 and SHIFT_మీట and not CTRL_మీట:
            if కీ_చిహ్నం not in 자신.మారు_కీ: 자신.మారు_మోడ్()
            자신.మారు_కీ.add(కీ_చిహ్నం)
            return
        if కీ_చిహ్నం==0xff08 and 자신.한글여부 and not CTRL_మీట and 자신.한글조합기.앞글자지우기(): return
        if CTRL_మీట and SHIFT_మీట and కీ_చిహ్నం in (ord('t'),ord('T')):
            자신.పంపు(bytes([30,2,1,0,0,0,0])); return
        if కీ_చిహ్నం==0xffc3: 자신.పంపు(bytes([30,2,2,0,0,0,0])); return
        if కీ_చిహ్నం==0xffc9: 자신.పంపు(bytes([30,2,3,0,0,0,0])); return
        if CTRL_మీట and SHIFT_మీట and కీ_చిహ్నం in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.పంపు(자신.క్లిప్_బోర్డ్_మూల్యం); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if కీ_చిహ్నం in 특수글쇠: 자신.పంపు(특수글쇠[కీ_చిహ్నం]); return
        అక్షరం_సంకేతీకరణం = కీ_చిహ్నం & 0xffffff if కీ_చిహ్నం & 0xff000000 == 0x01000000 else కీ_చిహ్నం
        if అక్షరం_సంకేతీకరణం > 0x10ffff or 0xd800 <= అక్షరం_సంకేతీకరణం <= 0xdfff or కీ_చిహ్నం >= 0xff00 and కీ_చిహ్నం < 0x1000000: return
        if CTRL_మీట and 0x40 <= అక్షరం_సంకేతీకరణం <= 0x7f: 자신.పంపు(bytes([అక్షరం_సంకేతీకరణం & 31])); return
        if అక్షరం_సంకేతీకరణం < 32: return
        if 자신.한글여부 and 자신.సవరణ_మీట & {0xffea,0xfe03,0xff7e} and not CTRL_మీట and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ఫీడ్_కీ(chr(అక్షరం_సంకేతీకరణం), altgr=True): return
        앞부분 = b'\x1b' if 자신.సవరణ_మీట & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_మీట and not 앞부분 and 32<=అక్షరం_సంకేతీకరణం<127:
            అక్షరం_డేటా=chr(అక్షరం_సంకేతీకరణం).upper() if SHIFT_మీట else chr(అక్షరం_సంకేతీకరణం)
            if 자신.한글조합기.ఫీడ్_కీ(అక్షరం_డేటా): return
        자신.పంపు(앞부분 + chr(అక్షరం_సంకేతీకరణం).encode('utf-8'))


class అనుసంధానించు_డెస్క్_టాప్:
    def __init__(자신, క్రమణం):
        자신.క్రమణం=క్రమణం; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.టెర్మినల్=False; 자신.시작화면=False; 자신.닫힘=False

    def పంపు(자신, డేటా):
        if not డేటా or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.క్రమణం.stdin.write(డేటా); 자신.క్రమణం.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                డేటా=자신.క్రమణం.stdout.read(4096)
                if not డేటా: break
                sys.stdout.buffer.write(డేటా); sys.stdout.buffer.flush()
                끝부분=(끝부분+డేటా)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.టెర్మినల్=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.పంపు(b'terminal\n')
        finally: 자신.닫힘=True

    def క్లయింట్(자신, క్లయింట్, పాత్):
        సర్వర్_మూల్యం=socket.socket(socket.AF_UNIX); సర్వర్_మూల్యం.settimeout(10); క్లయింట్.settimeout(10)
        కీబోర్డు_ప్రవేశం=కీబోర్డు(자신.పంపు,lambda 한글여부:자신.పంపు(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            సర్వర్_మూల్యం.connect(str(పాత్))
            # 초기 협상은 순서대로 끝낸다. 이후 అవుట్పుట్ 가닥만 클라이언트에 쓴다.
            క్లయింట్.sendall(정확한값(సర్వర్_మూల్యం,12))
            판번호=정확한값(క్లయింట్,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            సర్వర్_మూల్యం.sendall(판번호)
            개수=정확한값(సర్వర్_మూల్యం,1);క్లయింట్.sendall(개수+정확한값(సర్వర్_మూల్యం,개수[0]))
            భద్రత=정확한값(క్లయింట్,1)
            if భద్రత!=b'\x01': raise ValueError('unexpected security type')
            సర్వర్_మూల్యం.sendall(భద్రత)
            if 판번호==b'RFB 003.008\n':క్లయింట్.sendall(정확한값(సర్వర్_మూల్యం,4))
            సర్వర్_మూల్యం.sendall(정확한값(క్లయింట్,1))
            초기값=정확한값(సర్వర్_మూల్యం,24)
            క్లయింట్.sendall(초기값+정확한값(సర్వర్_మూల్యం,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            క్లయింట్.settimeout(None);సర్వర్_మూల్యం.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        వర్గం_మూల్యం=정확한값(సర్వర్_మూల్యం,1)[0]
                        if వర్గం_మూల్యం==0:
                            머리=정확한값(సర్వర్_మూల్యం,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 రిమోట్_మూల్యం 포인터의 중복을 피한다.
                            అదృశ్య_మూల్యం=포인터지원
                            if అదృశ్య_మూల్యం:క్లయింట్.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            క్లయింట్.sendall(bytes([వర్గం_మూల్యం])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(సర్వర్_మూల్యం,12);가로,నిలువు_స్థాయి,폭,높이,సంకేతీకరణం_మూల్యం=struct.unpack('>HHHHi',사각형)
                                if సంకేతీకరణం_మూల్యం!=0:raise ValueError('unexpected framebuffer encoding: '+str(సంకేతీకరణం_మూల్యం))
                                క్లయింట్.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    డేటా=정확한값(సర్వర్_మూల్యం,min(남음,65536));క్లయింట్.sendall(డేటా);남음-=len(డేటా)
                        elif వర్గం_మూల్యం==1:
                            머리=정확한값(సర్వర్_మూల్యం,5);개수=struct.unpack('>H',머리[3:])[0]
                            క్లయింట్.sendall(bytes([వర్గం_మూల్యం])+머리+정확한값(సర్వర్_మూల్యం,개수*6))
                        elif వర్గం_మూల్యం==2:క్లయింట్.sendall(bytes([వర్గం_మూల్యం]))
                        elif వర్గం_మూల్యం==3:
                            머리=정확한값(సర్వర్_మూల్యం,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            క్లయింట్.sendall(bytes([వర్గం_మూల్యం])+머리+정확한값(సర్వర్_మూల్యం,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(వర్గం_మూల్యం))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:క్లయింట్.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                వర్గం_మూల్యం=정확한값(క్లయింట్,1)[0]
                if వర్గం_మూల్యం==4:
                    ప్రధాన_పాఠం=정확한값(క్లయింట్,7); కీబోర్డు_ప్రవేశం.누름값(ప్రధాన_పాఠం[0]!=0,struct.unpack('>I',ప్రధాన_పాఠం[3:])[0]); continue
                if వర్గం_మూల్యం==255:
                    ప్రధాన_పాఠం=정확한값(క్లయింట్,11)
                    if ప్రధాన_పాఠం[0]!=0: raise ValueError('unsupported QEMU input extension')
                    కీబోర్డు_ప్రవేశం.누름값(struct.unpack('>H',ప్రధాన_పాఠం[1:3])[0]!=0,struct.unpack('>I',ప్రధాన_పాఠం[3:7])[0]); continue
                if వర్గం_మూల్యం==5:
                    ప్రధాన_పాఠం=정확한값(క్లయింట్,5); 단추들,x_నిర్దేశాంకం,Y_బటన్_సమన్వయపరుచు=struct.unpack('>BHH',ప్రధాన_పాఠం)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: కీబోర్డు_ప్రవేశం.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_నిర్దేశాంకం<576 and 112<=Y_బటన్_సమన్వయపరుచు<372:
                        అంశం_శోధన_సూచీ=(Y_బటన్_సమన్వయపరుచు-112)//52
                        if (Y_బటన్_సమన్వయపరుచు-112)%52<40 and అంశం_శోధన_సూచీ<5: 자신.పంపు(bytes([ord('1')+అంశం_శోధన_సూచీ]))
                    else: 자신.పంపు(bytes([30,1,단추들,x_నిర్దేశాంకం&255,x_నిర్దేశాంకం>>8,Y_బటన్_సమన్వయపరుచు&255,Y_బటన్_సమన్వయపరుచు>>8]))
                    continue
                if వర్గం_మూల్యం==6:
                    ప్రధాన_పాఠం=정확한값(క్లయింట్,7); పొడవు_మూల్యం=struct.unpack('>i',ప్రధాన_పాఠం[3:])[0]
                    if abs(పొడవు_మూల్యం)>65536: raise ValueError('clipboard too large')
                    పాఠ్యము=정확한값(క్లయింట్,abs(పొడవు_మూల్యం))
                    if పొడవు_మూల్యం>=0:
                        try: కీబోర్డు_ప్రవేశం.క్లిప్_బోర్డ్_మూల్యం=పాఠ్యము.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: కీబోర్డు_ప్రవేశం.క్లిప్_బోర్డ్_మూల్యం=పాఠ్యము.decode('latin-1').encode('utf-8')
                        కీబోర్డు_ప్రవేశం.క్లిప్_బోర్డ్_మూల్యం=కీబోర్డు_ప్రవేశం.క్లిప్_బోర్డ్_మూల్యం[:65536].decode('utf-8','ignore').encode('utf-8')
                    సర్వర్_మూల్యం.sendall(bytes([వర్గం_మూల్యం])+ప్రధాన_పాఠం+పాఠ్యము); continue
                if వర్గం_మూల్యం==0:
                    ప్రధాన_పాఠం=정확한값(క్లయింట్,19)
                    if ప్రధాన_పాఠం[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=ప్రధాన_పాఠం[3]//8
                elif వర్గం_మూల్యం==2:
                    ప్రధాన_పాఠం=정확한값(క్లయింట్,3); 항목수=struct.unpack('>H',ప్రధాన_పాఠం[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(క్లయింట్,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 స్వయంసిద్ధ_విలువ Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    ప్రధాన_పాఠం=struct.pack('>BHi',0,1,0)
                elif వర్గం_మూల్యం in (3,150): ప్రధాన_పాఠం=정확한값(క్లయింట్,9)
                elif వర్గం_మూల్యం==248:
                    ప్రధాన_పాఠం=정확한값(క్లయింట్,8)
                    if ప్రధాన_పాఠం[7]>64: raise ValueError('fence too large')
                    ప్రధాన_పాఠం+=정확한값(క్లయింట్,ప్రధాన_పాఠం[7])
                elif వర్గం_మూల్యం==250: ప్రధాన_పాఠం=정확한값(క్లయింట్,3)
                elif వర్గం_మూల్యం==251:
                    ప్రధాన_పాఠం=정확한값(క్లయింట్,7)
                    if ప్రధాన_పాఠం[5]>16: raise ValueError('too many screens')
                    ప్రధాన_పాఠం+=정확한값(క్లయింట్,ప్రధాన_పాఠం[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(వర్గం_మూల్యం))
                సర్వర్_మూల్యం.sendall(bytes([వర్గం_మూల్యం])+ప్రధాన_పాఠం)
        except (OSError,EOFError,ValueError) as దోషం:
            if str(దోషం): print('VNC client:',దోషం,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (క్లయింట్,సర్వర్_మూల్యం):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def అమలు_చెయ్_డెస్క్_టాప్(పోర్ట్_సంఖ్య=5902, నెట్_వర్క్=False, ఫైలు_బదిలీ_పోర్ట్_సంఖ్య=2121, 전달규칙들=(), స్పష్టత_మూల్యం=(640, 480), అతిథి_ఇమెయిల్=None, హోస్ట్_ఇమెయిల్='127.0.0.1'):
    with ExitStack() as వనరులు, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం = None
        if నెట్_వర్క్:
            from నెట్_వర్క్_బ్రిడ్జ్ import నెట్_వర్క్_బ్రిడ్జ్
            నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం = వనరులు.enter_context(నెట్_వర్క్_బ్రిడ్జ్(ఫైలు_బదిలీ_పోర్ట్_సంఖ్య, 전달규칙들, అతిథి_ఇమెయిల్=అతిథి_ఇమెయిల్, హోస్ట్_ఇమెయిల్=హోస్ట్_ఇమెయిల్))
        పాత్=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',పోర్ట్_సంఖ్య)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం and (원격화면접속번호==ఫైలు_బదిలీ_పోర్ట్_సంఖ్య or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and హోస్ట్==원격화면접속번호 for 통신규약,హోస్ట్,_ in నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            క్రమణం=subprocess.Popen(ఆదేశము(స్పష్టత_మూల్యం)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(పాత్)]+(నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం.전달인수() if నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            బ్రిడ్జ్=అనుసంధానించు_డెస్క్_టాప్(క్రమణం); రీడర్=threading.Thread(target=బ్రిడ్జ్.직렬입출력,daemon=True); రీడర్.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(హోస్ట్_ఇమెయిల్,ఫైలు_బదిలీ_పోర్ట్_సంఖ్య),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while క్రమణం.poll() is None:
                    try: క్లయింట్,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): క్లయింట్.close(); continue
                    if not పాత్.exists(): క్లయింట్.close(); continue
                    처리작업=threading.Thread(target=బ్రిడ్జ్.క్లయింట్,args=(క్లయింట్,పాత్),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                బ్రిడ్జ్.닫힘=True
                if నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం: నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం.నిలుపు_ఈవెంట్.set()
                if క్రమణం.poll() is None:
                    క్రమణం.terminate()
                    try: క్రమణం.wait(timeout=5)
                    except subprocess.TimeoutExpired: క్రమణం.kill(); క్రమణం.wait()
                రీడర్.join(timeout=2); క్రమణం.stdin.close(); క్రమణం.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం and నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం.దోషం: raise RuntimeError('network bridge: '+నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం.దోషం)
            return 0 if 가로채기됨 else క్రమణం.returncode


if __name__=='__main__':
    from అమలు_చేయి_ఆదేశం import 해상도읽기
    పార్సర్=argparse.ArgumentParser(description=__doc__); పార్సర్.add_argument('--port',type=int,default=5902)
    పార్సర్.add_argument('--resolution',type=해상도읽기,default=(640,480))
    పార్సర్.add_argument('--network',action='store_true'); పార్సర్.add_argument('--ftp-port',type=int,default=2121)
    పార్సర్.add_argument('--forward',action='append',default=[])
    కారకం_శ్రేణి=పార్సర్.parse_args()
    if కారకం_శ్రేణి.forward and not కారకం_శ్రేణి.network: పార్సర్.error('--forward requires --network')
    raise SystemExit(అమలు_చెయ్_డెస్క్_టాప్(కారకం_శ్రేణి.port,నెట్_వర్క్=కారకం_శ్రేణి.network,ఫైలు_బదిలీ_పోర్ట్_సంఖ్య=కారకం_శ్రేణి.ftp_port,전달규칙들=కారకం_శ్రేణి.forward,స్పష్టత_మూల్యం=కారకం_శ్రేణి.resolution))
