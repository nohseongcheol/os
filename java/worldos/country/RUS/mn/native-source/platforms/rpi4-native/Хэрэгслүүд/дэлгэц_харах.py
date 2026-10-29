#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, түлхүүр_утга 입력은 자체 кернел_утга UART로 전달한다. localhost 전용, 단일 хяналт_утга 클라이언트.
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
from Гүйцэтгэх_команд import Тушаал
from local_input import create


def 정확한값(소켓, Хэмжээ):
    өгөгдөл = bytearray()
    while len(өгөгдөл) < Хэмжээ:
        조각 = 소켓.recv(Хэмжээ - len(өгөгдөл))
        if not 조각: raise EOFError()
        өгөгдөл.extend(조각)
    return bytes(өгөгдөл)


class товчлуурт_гар:
    def __init__(자신, илгээх, 입력방식알림=None):
        자신.바이트전송 = илгээх; 자신.өөрчлөгч_товчлуур = set(); 자신.санамж_утга = b''
        자신.한글조합기 = create(илгээх, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.шилжих_түлхүүр = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def илгээх(자신, өгөгдөл):
        자신.한글조합기.조합확정()
        자신.바이트전송(өгөгдөл)

    def шилжих_горим(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, түлхүүр_тэмдэг):
        if түлхүүр_тэмдэг in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.өөрчлөгч_товчлуур.add(түлхүүр_тэмдэг)
            else: 자신.өөрчлөгч_товчлуур.discard(түлхүүр_тэмдэг)
            return
        if not 누르는중:
            자신.шилжих_түлхүүр.discard(түлхүүр_тэмдэг)
            return
        CTRL_товчлуур = bool(자신.өөрчлөгч_товчлуур & {0xffe3, 0xffe4})
        SHIFT_товчлуур = bool(자신.өөрчлөгч_товчлуур & {0xffe1, 0xffe2})
        if CTRL_товчлуур and SHIFT_товчлуур and түлхүүр_тэмдэг in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if түлхүүр_тэмдэг in (32,0xff0d):
                try:
                    утга=int(자신.유니코드입력,16)
                    if 32<=утга<=0x10ffff and not 0xd800<=утга<=0xdfff: 자신.илгээх(chr(утга).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif түлхүүр_тэмдэг==0xff1b: 자신.유니코드입력=None
            elif түлхүүр_тэмдэг==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif түлхүүр_тэмдэг<128 and chr(түлхүүр_тэмдэг) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(түлхүүр_тэмдэг)
            return
        if түлхүүр_тэмдэг in (0xff31,0xffc6) or түлхүүр_тэмдэг==32 and SHIFT_товчлуур and not CTRL_товчлуур:
            if түлхүүр_тэмдэг not in 자신.шилжих_түлхүүр: 자신.шилжих_горим()
            자신.шилжих_түлхүүр.add(түлхүүр_тэмдэг)
            return
        if түлхүүр_тэмдэг==0xff08 and 자신.한글여부 and not CTRL_товчлуур and 자신.한글조합기.앞글자지우기(): return
        if CTRL_товчлуур and SHIFT_товчлуур and түлхүүр_тэмдэг in (ord('t'),ord('T')):
            자신.илгээх(bytes([30,2,1,0,0,0,0])); return
        if түлхүүр_тэмдэг==0xffc3: 자신.илгээх(bytes([30,2,2,0,0,0,0])); return
        if түлхүүр_тэмдэг==0xffc9: 자신.илгээх(bytes([30,2,3,0,0,0,0])); return
        if CTRL_товчлуур and SHIFT_товчлуур and түлхүүр_тэмдэг in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.илгээх(자신.санамж_утга); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if түлхүүр_тэмдэг in 특수글쇠: 자신.илгээх(특수글쇠[түлхүүр_тэмдэг]); return
        тэмдэгт_кодчлол = түлхүүр_тэмдэг & 0xffffff if түлхүүр_тэмдэг & 0xff000000 == 0x01000000 else түлхүүр_тэмдэг
        if тэмдэгт_кодчлол > 0x10ffff or 0xd800 <= тэмдэгт_кодчлол <= 0xdfff or түлхүүр_тэмдэг >= 0xff00 and түлхүүр_тэмдэг < 0x1000000: return
        if CTRL_товчлуур and 0x40 <= тэмдэгт_кодчлол <= 0x7f: 자신.илгээх(bytes([тэмдэгт_кодчлол & 31])); return
        if тэмдэгт_кодчлол < 32: return
        if 자신.한글여부 and 자신.өөрчлөгч_товчлуур & {0xffea,0xfe03,0xff7e} and not CTRL_товчлуур and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.мэдээллийн_суваг_түлхүүр(chr(тэмдэгт_кодчлол), altgr=True): return
        앞부분 = b'\x1b' if 자신.өөрчлөгч_товчлуур & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_товчлуур and not 앞부분 and 32<=тэмдэгт_кодчлол<127:
            тэмдэгт_өгөгдөл=chr(тэмдэгт_кодчлол).upper() if SHIFT_товчлуур else chr(тэмдэгт_кодчлол)
            if 자신.한글조합기.мэдээллийн_суваг_түлхүүр(тэмдэгт_өгөгдөл): return
        자신.илгээх(앞부분 + chr(тэмдэгт_кодчлол).encode('utf-8'))


class холбох_дэлгэц:
    def __init__(자신, үйл_явц):
        자신.үйл_явц=үйл_явц; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Терминал=False; 자신.시작화면=False; 자신.닫힘=False

    def илгээх(자신, өгөгдөл):
        if not өгөгдөл or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.үйл_явц.stdin.write(өгөгдөл); 자신.үйл_явц.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                өгөгдөл=자신.үйл_явц.stdout.read(4096)
                if not өгөгдөл: break
                sys.stdout.buffer.write(өгөгдөл); sys.stdout.buffer.flush()
                끝부분=(끝부분+өгөгдөл)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Терминал=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.илгээх(b'terminal\n')
        finally: 자신.닫힘=True

    def клиент(자신, клиент, ЗАМ):
        сервер_утга=socket.socket(socket.AF_UNIX); сервер_утга.settimeout(10); клиент.settimeout(10)
        товчлуурт_гар_оролт=товчлуурт_гар(자신.илгээх,lambda 한글여부:자신.илгээх(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сервер_утга.connect(str(ЗАМ))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            клиент.sendall(정확한값(сервер_утга,12))
            판번호=정확한값(клиент,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сервер_утга.sendall(판번호)
            개수=정확한값(сервер_утга,1);клиент.sendall(개수+정확한값(сервер_утга,개수[0]))
            хамгаалалт=정확한값(клиент,1)
            if хамгаалалт!=b'\x01': raise ValueError('unexpected security type')
            сервер_утга.sendall(хамгаалалт)
            if 판번호==b'RFB 003.008\n':клиент.sendall(정확한값(сервер_утга,4))
            сервер_утга.sendall(정확한값(клиент,1))
            초기값=정확한값(сервер_утга,24)
            клиент.sendall(초기값+정확한값(сервер_утга,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            клиент.settimeout(None);сервер_утга.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ангилал_утга=정확한값(сервер_утга,1)[0]
                        if ангилал_утга==0:
                            머리=정확한값(сервер_утга,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 алсын_утга 포인터의 중복을 피한다.
                            нуугдмал_утга=포인터지원
                            if нуугдмал_утга:клиент.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            клиент.sendall(bytes([ангилал_утга])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(сервер_утга,12);가로,세로,폭,높이,кодчлол_утга=struct.unpack('>HHHHi',사각형)
                                if кодчлол_утга!=0:raise ValueError('unexpected framebuffer encoding: '+str(кодчлол_утга))
                                клиент.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    өгөгдөл=정확한값(сервер_утга,min(남음,65536));клиент.sendall(өгөгдөл);남음-=len(өгөгдөл)
                        elif ангилал_утга==1:
                            머리=정확한값(сервер_утга,5);개수=struct.unpack('>H',머리[3:])[0]
                            клиент.sendall(bytes([ангилал_утга])+머리+정확한값(сервер_утга,개수*6))
                        elif ангилал_утга==2:клиент.sendall(bytes([ангилал_утга]))
                        elif ангилал_утга==3:
                            머리=정확한값(сервер_утга,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            клиент.sendall(bytes([ангилал_утга])+머리+정확한값(сервер_утга,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ангилал_утга))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:клиент.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ангилал_утга=정확한값(клиент,1)[0]
                if ангилал_утга==4:
                    үндсэн_бичвэр=정확한값(клиент,7); товчлуурт_гар_оролт.누름값(үндсэн_бичвэр[0]!=0,struct.unpack('>I',үндсэн_бичвэр[3:])[0]); continue
                if ангилал_утга==255:
                    үндсэн_бичвэр=정확한값(клиент,11)
                    if үндсэн_бичвэр[0]!=0: raise ValueError('unsupported QEMU input extension')
                    товчлуурт_гар_оролт.누름값(struct.unpack('>H',үндсэн_бичвэр[1:3])[0]!=0,struct.unpack('>I',үндсэн_бичвэр[3:7])[0]); continue
                if ангилал_утга==5:
                    үндсэн_бичвэр=정확한값(клиент,5); 단추들,х_координат,세로좌표=struct.unpack('>BHH',үндсэн_бичвэр)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: товчлуурт_гар_оролт.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=х_координат<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.илгээх(bytes([ord('1')+색인]))
                    else: 자신.илгээх(bytes([30,1,단추들,х_координат&255,х_координат>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if ангилал_утга==6:
                    үндсэн_бичвэр=정확한값(клиент,7); урт_утга=struct.unpack('>i',үндсэн_бичвэр[3:])[0]
                    if abs(урт_утга)>65536: raise ValueError('clipboard too large')
                    Бичвэр=정확한값(клиент,abs(урт_утга))
                    if урт_утга>=0:
                        try: товчлуурт_гар_оролт.санамж_утга=Бичвэр.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: товчлуурт_гар_оролт.санамж_утга=Бичвэр.decode('latin-1').encode('utf-8')
                        товчлуурт_гар_оролт.санамж_утга=товчлуурт_гар_оролт.санамж_утга[:65536].decode('utf-8','ignore').encode('utf-8')
                    сервер_утга.sendall(bytes([ангилал_утга])+үндсэн_бичвэр+Бичвэр); continue
                if ангилал_утга==0:
                    үндсэн_бичвэр=정확한값(клиент,19)
                    if үндсэн_бичвэр[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=үндсэн_бичвэр[3]//8
                elif ангилал_утга==2:
                    үндсэн_бичвэр=정확한값(клиент,3); 항목수=struct.unpack('>H',үндсэн_бичвэр[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(клиент,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 өгөгдмөл_утга Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    үндсэн_бичвэр=struct.pack('>BHi',0,1,0)
                elif ангилал_утга in (3,150): үндсэн_бичвэр=정확한값(клиент,9)
                elif ангилал_утга==248:
                    үндсэн_бичвэр=정확한값(клиент,8)
                    if үндсэн_бичвэр[7]>64: raise ValueError('fence too large')
                    үндсэн_бичвэр+=정확한값(клиент,үндсэн_бичвэр[7])
                elif ангилал_утга==250: үндсэн_бичвэр=정확한값(клиент,3)
                elif ангилал_утга==251:
                    үндсэн_бичвэр=정확한값(клиент,7)
                    if үндсэн_бичвэр[5]>16: raise ValueError('too many screens')
                    үндсэн_бичвэр+=정확한값(клиент,үндсэн_бичвэр[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ангилал_утга))
                сервер_утга.sendall(bytes([ангилал_утга])+үндсэн_бичвэр)
        except (OSError,EOFError,ValueError) as Алдаа:
            if str(Алдаа): print('VNC client:',Алдаа,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (клиент,сервер_утга):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ажиллах_дэлгэц(접속번호=5902, Сүлжээ=False, 파일전송접속번호=2121, 전달규칙들=(), нягтрал_утга=(640, 480), 게스트주소=None, хост_хаяг='127.0.0.1'):
    with ExitStack() as Эх_үүсвэрүүд, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if Сүлжээ:
            from 통신다리 import 통신다리
            통신다리항목 = Эх_үүсвэрүүд.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, хост_хаяг=хост_хаяг))
        ЗАМ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and хост==원격화면접속번호 for 통신규약,хост,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            үйл_явц=subprocess.Popen(Тушаал(нягтрал_утга)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ЗАМ)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=холбох_дэлгэц(үйл_явц); Уншигч=threading.Thread(target=연결다리.직렬입출력,daemon=True); Уншигч.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(хост_хаяг,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while үйл_явц.poll() is None:
                    try: клиент,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): клиент.close(); continue
                    if not ЗАМ.exists(): клиент.close(); continue
                    처리작업=threading.Thread(target=연결다리.клиент,args=(клиент,ЗАМ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.түр_зогсоох_үйлдэл.set()
                if үйл_явц.poll() is None:
                    үйл_явц.terminate()
                    try: үйл_явц.wait(timeout=5)
                    except subprocess.TimeoutExpired: үйл_явц.kill(); үйл_явц.wait()
                Уншигч.join(timeout=2); үйл_явц.stdin.close(); үйл_явц.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.Алдаа: raise RuntimeError('network bridge: '+통신다리항목.Алдаа)
            return 0 if 가로채기됨 else үйл_явц.returncode


if __name__=='__main__':
    from Гүйцэтгэх_команд import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    аргумент_олонлог=인수해석기.parse_args()
    if аргумент_олонлог.forward and not аргумент_олонлог.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(ажиллах_дэлгэц(аргумент_олонлог.port,Сүлжээ=аргумент_олонлог.network,파일전송접속번호=аргумент_олонлог.ftp_port,전달규칙들=аргумент_олонлог.forward,нягтрал_утга=аргумент_олонлог.resolution))
