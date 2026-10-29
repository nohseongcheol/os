#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, की_मोल 입력은 자체 कर्नेल_मोल UART로 전달한다. localhost 전용, 단일 नियंत्रण_मोल 클라이언트.
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
from पाळो_दिवचो_आदेश import आदेश
from local_input import create


def EXACT_मोल(소켓, आवाठ):
    डेटा = bytearray()
    while len(डेटा) < आवाठ:
        조각 = 소켓.recv(आवाठ - len(डेटा))
        if not 조각: raise EOFError()
        डेटा.extend(조각)
    return bytes(डेटा)


class किबोर्ड:
    def __init__(자신, धाडचें, 입력방식알림=None):
        자신.바이트전송 = धाडचें; 자신.मॉडिफायर_की = set(); 자신.क्लिप_बोर्ड_मोल = b''
        자신.한글조합기 = create(धाडचें, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.स्विच_की = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def धाडचें(자신, डेटा):
        자신.한글조합기.조합확정()
        자신.바이트전송(डेटा)

    def स्विच_मोड(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, की_चिन्न):
        if की_चिन्न in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.मॉडिफायर_की.add(की_चिन्न)
            else: 자신.मॉडिफायर_की.discard(की_चिन्न)
            return
        if not 누르는중:
            자신.स्विच_की.discard(की_चिन्न)
            return
        CTRL = bool(자신.मॉडिफायर_की & {0xffe3, 0xffe4})
        SHIFT_की = bool(자신.मॉडिफायर_की & {0xffe1, 0xffe2})
        if CTRL and SHIFT_की and की_चिन्न in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if की_चिन्न in (32,0xff0d):
                try:
                    मोल=int(자신.유니코드입력,16)
                    if 32<=मोल<=0x10ffff and not 0xd800<=मोल<=0xdfff: 자신.धाडचें(chr(मोल).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif की_चिन्न==0xff1b: 자신.유니코드입력=None
            elif की_चिन्न==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif की_चिन्न<128 and chr(की_चिन्न) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(की_चिन्न)
            return
        if की_चिन्न in (0xff31,0xffc6) or की_चिन्न==32 and SHIFT_की and not CTRL:
            if की_चिन्न not in 자신.स्विच_की: 자신.स्विच_मोड()
            자신.स्विच_की.add(की_चिन्न)
            return
        if की_चिन्न==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_की and की_चिन्न in (ord('t'),ord('T')):
            자신.धाडचें(bytes([30,2,1,0,0,0,0])); return
        if की_चिन्न==0xffc3: 자신.धाडचें(bytes([30,2,2,0,0,0,0])); return
        if की_चिन्न==0xffc9: 자신.धाडचें(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_की and की_चिन्न in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.धाडचें(자신.क्लिप_बोर्ड_मोल); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if की_चिन्न in 특수글쇠: 자신.धाडचें(특수글쇠[की_चिन्न]); return
        वर्ण_एनकोडिंग = की_चिन्न & 0xffffff if की_चिन्न & 0xff000000 == 0x01000000 else की_चिन्न
        if वर्ण_एनकोडिंग > 0x10ffff or 0xd800 <= वर्ण_एनकोडिंग <= 0xdfff or की_चिन्न >= 0xff00 and की_चिन्न < 0x1000000: return
        if CTRL and 0x40 <= वर्ण_एनकोडिंग <= 0x7f: 자신.धाडचें(bytes([वर्ण_एनकोडिंग & 31])); return
        if वर्ण_एनकोडिंग < 32: return
        if 자신.한글여부 and 자신.मॉडिफायर_की & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.फीड_की(chr(वर्ण_एनकोडिंग), altgr=True): return
        앞부분 = b'\x1b' if 자신.मॉडिफायर_की & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=वर्ण_एनकोडिंग<127:
            वर्ण_डेटा=chr(वर्ण_एनकोडिंग).upper() if SHIFT_की else chr(वर्ण_एनकोडिंग)
            if 자신.한글조합기.फीड_की(वर्ण_डेटा): return
        자신.धाडचें(앞부분 + chr(वर्ण_एनकोडिंग).encode('utf-8'))


class कनॅक्ट_डॅस्कटॉप:
    def __init__(자신, प्रक्रिया):
        자신.प्रक्रिया=प्रक्रिया; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.टर्मिनल=False; 자신.시작화면=False; 자신.닫힘=False

    def धाडचें(자신, डेटा):
        if not डेटा or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.प्रक्रिया.stdin.write(डेटा); 자신.प्रक्रिया.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                डेटा=자신.प्रक्रिया.stdout.read(4096)
                if not डेटा: break
                sys.stdout.buffer.write(डेटा); sys.stdout.buffer.flush()
                끝부분=(끝부분+डेटा)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.टर्मिनल=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.धाडचें(b'terminal\n')
        finally: 자신.닫힘=True

    def क्लायंट(자신, क्लायंट, पाथ):
        सर्वर_मोल=socket.socket(socket.AF_UNIX); सर्वर_मोल.settimeout(10); क्लायंट.settimeout(10)
        किबोर्ड_प्रवेश=किबोर्ड(자신.धाडचें,lambda 한글여부:자신.धाडचें(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            सर्वर_मोल.connect(str(पाथ))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            क्लायंट.sendall(EXACT_मोल(सर्वर_मोल,12))
            판번호=EXACT_मोल(क्लायंट,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            सर्वर_मोल.sendall(판번호)
            आयटम_COUNT=EXACT_मोल(सर्वर_मोल,1);क्लायंट.sendall(आयटम_COUNT+EXACT_मोल(सर्वर_मोल,आयटम_COUNT[0]))
            सुरक्षा=EXACT_मोल(क्लायंट,1)
            if सुरक्षा!=b'\x01': raise ValueError('unexpected security type')
            सर्वर_मोल.sendall(सुरक्षा)
            if 판번호==b'RFB 003.008\n':क्लायंट.sendall(EXACT_मोल(सर्वर_मोल,4))
            सर्वर_मोल.sendall(EXACT_मोल(क्लायंट,1))
            초기값=EXACT_मोल(सर्वर_मोल,24)
            क्लायंट.sendall(초기값+EXACT_मोल(सर्वर_मोल,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            क्लायंट.settimeout(None);सर्वर_मोल.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        वर्ग_मोल=EXACT_मोल(सर्वर_मोल,1)[0]
                        if वर्ग_मोल==0:
                            머리=EXACT_मोल(सर्वर_मोल,3);प्रवेश_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 दुर्मीळ_मोल 포인터의 중복을 피한다.
                            लिपिल्लें_मोल=포인터지원
                            if लिपिल्लें_मोल:क्लायंट.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            क्लायंट.sendall(bytes([वर्ग_मोल])+머리)
                            for _ in range(प्रवेश_COUNT):
                                사각형=EXACT_मोल(सर्वर_मोल,12);가로,उबें_स्थिती,폭,높이,एनकोडिंग_मोल=struct.unpack('>HHHHi',사각형)
                                if एनकोडिंग_मोल!=0:raise ValueError('unexpected framebuffer encoding: '+str(एनकोडिंग_मोल))
                                क्लायंट.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    डेटा=EXACT_मोल(सर्वर_मोल,min(남음,65536));क्लायंट.sendall(डेटा);남음-=len(डेटा)
                        elif वर्ग_मोल==1:
                            머리=EXACT_मोल(सर्वर_मोल,5);आयटम_COUNT=struct.unpack('>H',머리[3:])[0]
                            क्लायंट.sendall(bytes([वर्ग_मोल])+머리+EXACT_मोल(सर्वर_मोल,आयटम_COUNT*6))
                        elif वर्ग_मोल==2:क्लायंट.sendall(bytes([वर्ग_मोल]))
                        elif वर्ग_मोल==3:
                            머리=EXACT_मोल(सर्वर_मोल,7);आयटम_COUNT=struct.unpack('>I',머리[3:])[0]
                            if आयटम_COUNT>1048576:raise ValueError('server clipboard too large')
                            क्लायंट.sendall(bytes([वर्ग_मोल])+머리+EXACT_मोल(सर्वर_मोल,आयटम_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(वर्ग_मोल))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:क्लायंट.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                वर्ग_मोल=EXACT_मोल(क्लायंट,1)[0]
                if वर्ग_मोल==4:
                    देखीचो_उतारो=EXACT_मोल(क्लायंट,7); किबोर्ड_प्रवेश.누름값(देखीचो_उतारो[0]!=0,struct.unpack('>I',देखीचो_उतारो[3:])[0]); continue
                if वर्ग_मोल==255:
                    देखीचो_उतारो=EXACT_मोल(क्लायंट,11)
                    if देखीचो_उतारो[0]!=0: raise ValueError('unsupported QEMU input extension')
                    किबोर्ड_प्रवेश.누름값(struct.unpack('>H',देखीचो_उतारो[1:3])[0]!=0,struct.unpack('>I',देखीचो_उतारो[3:7])[0]); continue
                if वर्ग_मोल==5:
                    देखीचो_उतारो=EXACT_मोल(क्लायंट,5); 단추들,x_coordinate,세로좌표=struct.unpack('>BHH',देखीचो_उतारो)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: किबोर्ड_प्रवेश.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_coordinate<576 and 112<=세로좌표<372:
                        लूकअप_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and लूकअप_INDEX<5: 자신.धाडचें(bytes([ord('1')+लूकअप_INDEX]))
                    else: 자신.धाडचें(bytes([30,1,단추들,x_coordinate&255,x_coordinate>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if वर्ग_मोल==6:
                    देखीचो_उतारो=EXACT_मोल(क्लायंट,7); लांबाय_मोल=struct.unpack('>i',देखीचो_उतारो[3:])[0]
                    if abs(लांबाय_मोल)>65536: raise ValueError('clipboard too large')
                    SMS=EXACT_मोल(क्लायंट,abs(लांबाय_मोल))
                    if लांबाय_मोल>=0:
                        try: किबोर्ड_प्रवेश.क्लिप_बोर्ड_मोल=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: किबोर्ड_प्रवेश.क्लिप_बोर्ड_मोल=SMS.decode('latin-1').encode('utf-8')
                        किबोर्ड_प्रवेश.क्लिप_बोर्ड_मोल=किबोर्ड_प्रवेश.क्लिप_बोर्ड_मोल[:65536].decode('utf-8','ignore').encode('utf-8')
                    सर्वर_मोल.sendall(bytes([वर्ग_मोल])+देखीचो_उतारो+SMS); continue
                if वर्ग_मोल==0:
                    देखीचो_उतारो=EXACT_मोल(क्लायंट,19)
                    if देखीचो_उतारो[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=देखीचो_उतारो[3]//8
                elif वर्ग_मोल==2:
                    देखीचो_उतारो=EXACT_मोल(क्लायंट,3); प्रवेश_COUNT=struct.unpack('>H',देखीचो_उतारो[1:])[0]
                    if प्रवेश_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(प्रवेश_COUNT)+'i',EXACT_मोल(क्लायंट,प्रवेश_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 डिफॉल्ट_मोल Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    देखीचो_उतारो=struct.pack('>BHi',0,1,0)
                elif वर्ग_मोल in (3,150): देखीचो_उतारो=EXACT_मोल(क्लायंट,9)
                elif वर्ग_मोल==248:
                    देखीचो_उतारो=EXACT_मोल(क्लायंट,8)
                    if देखीचो_उतारो[7]>64: raise ValueError('fence too large')
                    देखीचो_उतारो+=EXACT_मोल(क्लायंट,देखीचो_उतारो[7])
                elif वर्ग_मोल==250: देखीचो_उतारो=EXACT_मोल(क्लायंट,3)
                elif वर्ग_मोल==251:
                    देखीचो_उतारो=EXACT_मोल(क्लायंट,7)
                    if देखीचो_उतारो[5]>16: raise ValueError('too many screens')
                    देखीचो_उतारो+=EXACT_मोल(क्लायंट,देखीचो_उतारो[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(वर्ग_मोल))
                सर्वर_मोल.sendall(bytes([वर्ग_मोल])+देखीचो_उतारो)
        except (OSError,EOFError,ValueError) as चूक:
            if str(चूक): print('VNC client:',चूक,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (क्लायंट,सर्वर_मोल):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def चलोवप_डॅस्कटॉप(접속번호=5902, नॅटवर्क=False, 파일전송접속번호=2121, 전달규칙들=(), रिजोल्युशन_मोल=(640, 480), सोयरो_नामो=None, येजमान_नामो='127.0.0.1'):
    with ExitStack() as रिसोर्सीस, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        नॅटवर्क_ब्रिज_प्रवेश = None
        if नॅटवर्क:
            from नॅटवर्क_ब्रिज import नॅटवर्क_ब्रिज
            नॅटवर्क_ब्रिज_प्रवेश = रिसोर्सीस.enter_context(नॅटवर्क_ब्रिज(파일전송접속번호, 전달규칙들, सोयरो_नामो=सोयरो_नामो, येजमान_नामो=येजमान_नामो))
        पाथ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if नॅटवर्क_ब्रिज_प्रवेश and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and येजमान==원격화면접속번호 for 통신규약,येजमान,_ in नॅटवर्क_ब्रिज_प्रवेश.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            प्रक्रिया=subprocess.Popen(आदेश(रिजोल्युशन_मोल)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(पाथ)]+(नॅटवर्क_ब्रिज_प्रवेश.전달인수() if नॅटवर्क_ब्रिज_प्रवेश else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ब्रिज=कनॅक्ट_डॅस्कटॉप(प्रक्रिया); वाचक=threading.Thread(target=ब्रिज.직렬입출력,daemon=True); वाचक.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if नॅटवर्क_ब्रिज_प्रवेश: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(येजमान_नामो,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while प्रक्रिया.poll() is None:
                    try: क्लायंट,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): क्लायंट.close(); continue
                    if not पाथ.exists(): क्लायंट.close(); continue
                    처리작업=threading.Thread(target=ब्रिज.क्लायंट,args=(क्लायंट,पाथ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ब्रिज.닫힘=True
                if नॅटवर्क_ब्रिज_प्रवेश: नॅटवर्क_ब्रिज_प्रवेश.थांबणी_प्रसंग.set()
                if प्रक्रिया.poll() is None:
                    प्रक्रिया.terminate()
                    try: प्रक्रिया.wait(timeout=5)
                    except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
                वाचक.join(timeout=2); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if नॅटवर्क_ब्रिज_प्रवेश and नॅटवर्क_ब्रिज_प्रवेश.चूक: raise RuntimeError('network bridge: '+नॅटवर्क_ब्रिज_प्रवेश.चूक)
            return 0 if 가로채기됨 else प्रक्रिया.returncode


if __name__=='__main__':
    from पाळो_दिवचो_आदेश import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    युक्तीवाद_क्रम=인수해석기.parse_args()
    if युक्तीवाद_क्रम.forward and not युक्तीवाद_क्रम.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(चलोवप_डॅस्कटॉप(युक्तीवाद_क्रम.port,नॅटवर्क=युक्तीवाद_क्रम.network,파일전송접속번호=युक्तीवाद_क्रम.ftp_port,전달규칙들=युक्तीवाद_क्रम.forward,रिजोल्युशन_मोल=युक्तीवाद_क्रम.resolution))
