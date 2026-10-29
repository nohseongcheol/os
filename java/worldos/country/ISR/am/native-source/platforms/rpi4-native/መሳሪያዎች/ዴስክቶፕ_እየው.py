#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ቁልፍ_እሴት 입력은 자체 ዓንኳር_እሴት UART로 전달한다. localhost 전용, 단일 ቁጥጥር_እሴት 클라이언트.
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
from ፈጽም_ትእዛዝ import ትእዛዝ
from local_input import create


def 정확한값(소켓, መጠን):
    ውሂብ = bytearray()
    while len(ውሂብ) < መጠን:
        조각 = 소켓.recv(መጠን - len(ውሂብ))
        if not 조각: raise EOFError()
        ውሂብ.extend(조각)
    return bytes(ውሂብ)


class የቁልፍ_ሰሌዳ:
    def __init__(자신, ላክ, 입력방식알림=None):
        자신.바이트전송 = ላክ; 자신.ለዋጭ_ቁልፍ = set(); 자신.ትግበራ_እሴት = b''
        자신.한글조합기 = create(ላክ, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ቀይር_ቁልፍ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ላክ(자신, ውሂብ):
        자신.한글조합기.조합확정()
        자신.바이트전송(ውሂብ)

    def ቀይር_ሁነታ(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, ቁልፍ_ምልክት):
        if ቁልፍ_ምልክት in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ለዋጭ_ቁልፍ.add(ቁልፍ_ምልክት)
            else: 자신.ለዋጭ_ቁልፍ.discard(ቁልፍ_ምልክት)
            return
        if not 누르는중:
            자신.ቀይር_ቁልፍ.discard(ቁልፍ_ምልክት)
            return
        CTRL_ቁልፍ = bool(자신.ለዋጭ_ቁልፍ & {0xffe3, 0xffe4})
        SHIFT_ቁልፍ = bool(자신.ለዋጭ_ቁልፍ & {0xffe1, 0xffe2})
        if CTRL_ቁልፍ and SHIFT_ቁልፍ and ቁልፍ_ምልክት in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if ቁልፍ_ምልክት in (32,0xff0d):
                try:
                    እሴት=int(자신.유니코드입력,16)
                    if 32<=እሴት<=0x10ffff and not 0xd800<=እሴት<=0xdfff: 자신.ላክ(chr(እሴት).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif ቁልፍ_ምልክት==0xff1b: 자신.유니코드입력=None
            elif ቁልፍ_ምልክት==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif ቁልፍ_ምልክት<128 and chr(ቁልፍ_ምልክት) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(ቁልፍ_ምልክት)
            return
        if ቁልፍ_ምልክት in (0xff31,0xffc6) or ቁልፍ_ምልክት==32 and SHIFT_ቁልፍ and not CTRL_ቁልፍ:
            if ቁልፍ_ምልክት not in 자신.ቀይር_ቁልፍ: 자신.ቀይር_ሁነታ()
            자신.ቀይር_ቁልፍ.add(ቁልፍ_ምልክት)
            return
        if ቁልፍ_ምልክት==0xff08 and 자신.한글여부 and not CTRL_ቁልፍ and 자신.한글조합기.앞글자지우기(): return
        if CTRL_ቁልፍ and SHIFT_ቁልፍ and ቁልፍ_ምልክት in (ord('t'),ord('T')):
            자신.ላክ(bytes([30,2,1,0,0,0,0])); return
        if ቁልፍ_ምልክት==0xffc3: 자신.ላክ(bytes([30,2,2,0,0,0,0])); return
        if ቁልፍ_ምልክት==0xffc9: 자신.ላክ(bytes([30,2,3,0,0,0,0])); return
        if CTRL_ቁልፍ and SHIFT_ቁልፍ and ቁልፍ_ምልክት in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ላክ(자신.ትግበራ_እሴት); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if ቁልፍ_ምልክት in 특수글쇠: 자신.ላክ(특수글쇠[ቁልፍ_ምልክት]); return
        ቁምፊ_በኮድ_መክተት = ቁልፍ_ምልክት & 0xffffff if ቁልፍ_ምልክት & 0xff000000 == 0x01000000 else ቁልፍ_ምልክት
        if ቁምፊ_በኮድ_መክተት > 0x10ffff or 0xd800 <= ቁምፊ_በኮድ_መክተት <= 0xdfff or ቁልፍ_ምልክት >= 0xff00 and ቁልፍ_ምልክት < 0x1000000: return
        if CTRL_ቁልፍ and 0x40 <= ቁምፊ_በኮድ_መክተት <= 0x7f: 자신.ላክ(bytes([ቁምፊ_በኮድ_መክተት & 31])); return
        if ቁምፊ_በኮድ_መክተት < 32: return
        if 자신.한글여부 and 자신.ለዋጭ_ቁልፍ & {0xffea,0xfe03,0xff7e} and not CTRL_ቁልፍ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ምግብ_ቁልፍ(chr(ቁምፊ_በኮድ_መክተት), altgr=True): return
        앞부분 = b'\x1b' if 자신.ለዋጭ_ቁልፍ & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_ቁልፍ and not 앞부분 and 32<=ቁምፊ_በኮድ_መክተት<127:
            ቁምፊ_ውሂብ=chr(ቁምፊ_በኮድ_መክተት).upper() if SHIFT_ቁልፍ else chr(ቁምፊ_በኮድ_መክተት)
            if 자신.한글조합기.ምግብ_ቁልፍ(ቁምፊ_ውሂብ): return
        자신.ላክ(앞부분 + chr(ቁምፊ_በኮድ_መክተት).encode('utf-8'))


class አገናኝ_ዴስክቶፕ:
    def __init__(자신, ሂደቶች):
        자신.ሂደቶች=ሂደቶች; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.ተርሚናል=False; 자신.시작화면=False; 자신.닫힘=False

    def ላክ(자신, ውሂብ):
        if not ውሂብ or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.ሂደቶች.stdin.write(ውሂብ); 자신.ሂደቶች.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ውሂብ=자신.ሂደቶች.stdout.read(4096)
                if not ውሂብ: break
                sys.stdout.buffer.write(ውሂብ); sys.stdout.buffer.flush()
                끝부분=(끝부분+ውሂብ)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.ተርሚናል=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ላክ(b'terminal\n')
        finally: 자신.닫힘=True

    def ተገልጋይ(자신, ተገልጋይ, መተላለፊያ):
        አገልጋይ_እሴት=socket.socket(socket.AF_UNIX); አገልጋይ_እሴት.settimeout(10); ተገልጋይ.settimeout(10)
        የቁልፍ_ሰሌዳ_ምዝግብ=የቁልፍ_ሰሌዳ(자신.ላክ,lambda 한글여부:자신.ላክ(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            አገልጋይ_እሴት.connect(str(መተላለፊያ))
            # 초기 협상은 순서대로 끝낸다. 이후 ውጤት 가닥만 클라이언트에 쓴다.
            ተገልጋይ.sendall(정확한값(አገልጋይ_እሴት,12))
            판번호=정확한값(ተገልጋይ,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            አገልጋይ_እሴት.sendall(판번호)
            개수=정확한값(አገልጋይ_እሴት,1);ተገልጋይ.sendall(개수+정확한값(አገልጋይ_እሴት,개수[0]))
            መድህን=정확한값(ተገልጋይ,1)
            if መድህን!=b'\x01': raise ValueError('unexpected security type')
            አገልጋይ_እሴት.sendall(መድህን)
            if 판번호==b'RFB 003.008\n':ተገልጋይ.sendall(정확한값(አገልጋይ_እሴት,4))
            አገልጋይ_እሴት.sendall(정확한값(ተገልጋይ,1))
            초기값=정확한값(አገልጋይ_እሴት,24)
            ተገልጋይ.sendall(초기값+정확한값(አገልጋይ_እሴት,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ተገልጋይ.settimeout(None);አገልጋይ_እሴት.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ምድብ_እሴት=정확한값(አገልጋይ_እሴት,1)[0]
                        if ምድብ_እሴት==0:
                            머리=정확한값(አገልጋይ_እሴት,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 የሩቅ_እሴት 포인터의 중복을 피한다.
                            ድብቅ_እሴት=포인터지원
                            if ድብቅ_እሴት:ተገልጋይ.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ተገልጋይ.sendall(bytes([ምድብ_እሴት])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(አገልጋይ_እሴት,12);가로,ቋሚ_በቦታ_አስቀመጠ,폭,높이,በኮድ_መክተት_እሴት=struct.unpack('>HHHHi',사각형)
                                if በኮድ_መክተት_እሴት!=0:raise ValueError('unexpected framebuffer encoding: '+str(በኮድ_መክተት_እሴት))
                                ተገልጋይ.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ውሂብ=정확한값(አገልጋይ_እሴት,min(남음,65536));ተገልጋይ.sendall(ውሂብ);남음-=len(ውሂብ)
                        elif ምድብ_እሴት==1:
                            머리=정확한값(አገልጋይ_እሴት,5);개수=struct.unpack('>H',머리[3:])[0]
                            ተገልጋይ.sendall(bytes([ምድብ_እሴት])+머리+정확한값(አገልጋይ_እሴት,개수*6))
                        elif ምድብ_እሴት==2:ተገልጋይ.sendall(bytes([ምድብ_እሴት]))
                        elif ምድብ_እሴት==3:
                            머리=정확한값(አገልጋይ_እሴት,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ተገልጋይ.sendall(bytes([ምድብ_እሴት])+머리+정확한값(አገልጋይ_እሴት,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ምድብ_እሴት))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ተገልጋይ.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ምድብ_እሴት=정확한값(ተገልጋይ,1)[0]
                if ምድብ_እሴት==4:
                    የጽሁፍ_አካል=정확한값(ተገልጋይ,7); የቁልፍ_ሰሌዳ_ምዝግብ.누름값(የጽሁፍ_አካል[0]!=0,struct.unpack('>I',የጽሁፍ_አካል[3:])[0]); continue
                if ምድብ_እሴት==255:
                    የጽሁፍ_አካል=정확한값(ተገልጋይ,11)
                    if የጽሁፍ_አካል[0]!=0: raise ValueError('unsupported QEMU input extension')
                    የቁልፍ_ሰሌዳ_ምዝግብ.누름값(struct.unpack('>H',የጽሁፍ_አካል[1:3])[0]!=0,struct.unpack('>I',የጽሁፍ_አካል[3:7])[0]); continue
                if ምድብ_እሴት==5:
                    የጽሁፍ_አካል=정확한값(ተገልጋይ,5); 단추들,ኤክስ_አስተባባሪ,세로좌표=struct.unpack('>BHH',የጽሁፍ_አካል)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: የቁልፍ_ሰሌዳ_ምዝግብ.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=ኤክስ_አስተባባሪ<576 and 112<=세로좌표<372:
                        ፍለጋ_መረጃ_ጠቆመ=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and ፍለጋ_መረጃ_ጠቆመ<5: 자신.ላክ(bytes([ord('1')+ፍለጋ_መረጃ_ጠቆመ]))
                    else: 자신.ላክ(bytes([30,1,단추들,ኤክስ_አስተባባሪ&255,ኤክስ_አስተባባሪ>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if ምድብ_እሴት==6:
                    የጽሁፍ_አካል=정확한값(ተገልጋይ,7); ርዝመት_እሴት=struct.unpack('>i',የጽሁፍ_አካል[3:])[0]
                    if abs(ርዝመት_እሴት)>65536: raise ValueError('clipboard too large')
                    ጽሁፍ=정확한값(ተገልጋይ,abs(ርዝመት_እሴት))
                    if ርዝመት_እሴት>=0:
                        try: የቁልፍ_ሰሌዳ_ምዝግብ.ትግበራ_እሴት=ጽሁፍ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: የቁልፍ_ሰሌዳ_ምዝግብ.ትግበራ_እሴት=ጽሁፍ.decode('latin-1').encode('utf-8')
                        የቁልፍ_ሰሌዳ_ምዝግብ.ትግበራ_እሴት=የቁልፍ_ሰሌዳ_ምዝግብ.ትግበራ_እሴት[:65536].decode('utf-8','ignore').encode('utf-8')
                    አገልጋይ_እሴት.sendall(bytes([ምድብ_እሴት])+የጽሁፍ_አካል+ጽሁፍ); continue
                if ምድብ_እሴት==0:
                    የጽሁፍ_አካል=정확한값(ተገልጋይ,19)
                    if የጽሁፍ_አካል[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=የጽሁፍ_አካል[3]//8
                elif ምድብ_እሴት==2:
                    የጽሁፍ_አካል=정확한값(ተገልጋይ,3); 항목수=struct.unpack('>H',የጽሁፍ_አካል[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ተገልጋይ,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ነባሪ_እሴት Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    የጽሁፍ_አካል=struct.pack('>BHi',0,1,0)
                elif ምድብ_እሴት in (3,150): የጽሁፍ_አካል=정확한값(ተገልጋይ,9)
                elif ምድብ_እሴት==248:
                    የጽሁፍ_አካል=정확한값(ተገልጋይ,8)
                    if የጽሁፍ_አካል[7]>64: raise ValueError('fence too large')
                    የጽሁፍ_አካል+=정확한값(ተገልጋይ,የጽሁፍ_አካል[7])
                elif ምድብ_እሴት==250: የጽሁፍ_አካል=정확한값(ተገልጋይ,3)
                elif ምድብ_እሴት==251:
                    የጽሁፍ_አካል=정확한값(ተገልጋይ,7)
                    if የጽሁፍ_አካል[5]>16: raise ValueError('too many screens')
                    የጽሁፍ_አካል+=정확한값(ተገልጋይ,የጽሁፍ_አካል[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ምድብ_እሴት))
                አገልጋይ_እሴት.sendall(bytes([ምድብ_እሴት])+የጽሁፍ_አካል)
        except (OSError,EOFError,ValueError) as ስህተት:
            if str(ስህተት): print('VNC client:',ስህተት,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ተገልጋይ,አገልጋይ_እሴት):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def አሂድ_ዴስክቶፕ(የወደብ_ቁጥር=5902, መረብ=False, ፋይል_ትልልፍ_የወደብ_ቁጥር=2121, 전달규칙들=(), ጥራት_እሴት=(640, 480), እንግዳ_አድራሻ=None, አዘጋጅ_አድራሻ='127.0.0.1'):
    with ExitStack() as ሃብቶች, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        መረብ_ድልድይ_ምዝግብ = None
        if መረብ:
            from መረብ_ድልድይ import መረብ_ድልድይ
            መረብ_ድልድይ_ምዝግብ = ሃብቶች.enter_context(መረብ_ድልድይ(ፋይል_ትልልፍ_የወደብ_ቁጥር, 전달규칙들, እንግዳ_አድራሻ=እንግዳ_አድራሻ, አዘጋጅ_አድራሻ=አዘጋጅ_አድራሻ))
        መተላለፊያ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',የወደብ_ቁጥር)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if መረብ_ድልድይ_ምዝግብ and (원격화면접속번호==ፋይል_ትልልፍ_የወደብ_ቁጥር or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and አዘጋጅ_b78e430d==원격화면접속번호 for 통신규약,አዘጋጅ_b78e430d,_ in መረብ_ድልድይ_ምዝግብ.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            ሂደቶች=subprocess.Popen(ትእዛዝ(ጥራት_እሴት)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(መተላለፊያ)]+(መረብ_ድልድይ_ምዝግብ.전달인수() if መረብ_ድልድይ_ምዝግብ else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ድልድይ=አገናኝ_ዴስክቶፕ(ሂደቶች); አንባቢ=threading.Thread(target=ድልድይ.직렬입출력,daemon=True); አንባቢ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if መረብ_ድልድይ_ምዝግብ: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(አዘጋጅ_አድራሻ,ፋይል_ትልልፍ_የወደብ_ቁጥር),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while ሂደቶች.poll() is None:
                    try: ተገልጋይ,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): ተገልጋይ.close(); continue
                    if not መተላለፊያ.exists(): ተገልጋይ.close(); continue
                    처리작업=threading.Thread(target=ድልድይ.ተገልጋይ,args=(ተገልጋይ,መተላለፊያ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ድልድይ.닫힘=True
                if መረብ_ድልድይ_ምዝግብ: መረብ_ድልድይ_ምዝግብ.ላፍታ_አቁም_ፍጻሜ.set()
                if ሂደቶች.poll() is None:
                    ሂደቶች.terminate()
                    try: ሂደቶች.wait(timeout=5)
                    except subprocess.TimeoutExpired: ሂደቶች.kill(); ሂደቶች.wait()
                አንባቢ.join(timeout=2); ሂደቶች.stdin.close(); ሂደቶች.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if መረብ_ድልድይ_ምዝግብ and መረብ_ድልድይ_ምዝግብ.ስህተት: raise RuntimeError('network bridge: '+መረብ_ድልድይ_ምዝግብ.ስህተት)
            return 0 if 가로채기됨 else ሂደቶች.returncode


if __name__=='__main__':
    from ፈጽም_ትእዛዝ import 해상도읽기
    አግልሎ_ማስቀመጥ=argparse.ArgumentParser(description=__doc__); አግልሎ_ማስቀመጥ.add_argument('--port',type=int,default=5902)
    አግልሎ_ማስቀመጥ.add_argument('--resolution',type=해상도읽기,default=(640,480))
    አግልሎ_ማስቀመጥ.add_argument('--network',action='store_true'); አግልሎ_ማስቀመጥ.add_argument('--ftp-port',type=int,default=2121)
    አግልሎ_ማስቀመጥ.add_argument('--forward',action='append',default=[])
    ነጋሪ_እሴት_ድርድር=አግልሎ_ማስቀመጥ.parse_args()
    if ነጋሪ_እሴት_ድርድር.forward and not ነጋሪ_እሴት_ድርድር.network: አግልሎ_ማስቀመጥ.error('--forward requires --network')
    raise SystemExit(አሂድ_ዴስክቶፕ(ነጋሪ_እሴት_ድርድር.port,መረብ=ነጋሪ_እሴት_ድርድር.network,ፋይል_ትልልፍ_የወደብ_ቁጥር=ነጋሪ_እሴት_ድርድር.ftp_port,전달규칙들=ነጋሪ_እሴት_ድርድር.forward,ጥራት_እሴት=ነጋሪ_እሴት_ድርድር.resolution))
