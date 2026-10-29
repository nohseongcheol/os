#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, клавіша_значэнне 입력은 자체 ядро_значэнне UART로 전달한다. localhost 전용, 단일 кіраванне_значэнне 클라이언트.
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
from выканаць_каманда import Загад
from local_input import create


def 정확한값(소켓, Памер):
    дадзеныя = bytearray()
    while len(дадзеныя) < Памер:
        조각 = 소켓.recv(Памер - len(дадзеныя))
        if not 조각: raise EOFError()
        дадзеныя.extend(조각)
    return bytes(дадзеныя)


class клавіятура:
    def __init__(자신, адправіць, 입력방식알림=None):
        자신.바이트전송 = адправіць; 자신.службовая_клавіша = set(); 자신.буфер_абмену_значэнне = b''
        자신.한글조합기 = create(адправіць, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.пераход_клавіша = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def адправіць(자신, дадзеныя):
        자신.한글조합기.조합확정()
        자신.바이트전송(дадзеныя)

    def пераход_рэжым(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, клавіша_сімвал):
        if клавіша_сімвал in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.службовая_клавіша.add(клавіша_сімвал)
            else: 자신.службовая_клавіша.discard(клавіша_сімвал)
            return
        if not 누르는중:
            자신.пераход_клавіша.discard(клавіша_сімвал)
            return
        кіраванне_клавіша = bool(자신.службовая_клавіша & {0xffe3, 0xffe4})
        клавіша_SHIFT = bool(자신.службовая_клавіша & {0xffe1, 0xffe2})
        if кіраванне_клавіша and клавіша_SHIFT and клавіша_сімвал in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if клавіша_сімвал in (32,0xff0d):
                try:
                    значэнне=int(자신.유니코드입력,16)
                    if 32<=значэнне<=0x10ffff and not 0xd800<=значэнне<=0xdfff: 자신.адправіць(chr(значэнне).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif клавіша_сімвал==0xff1b: 자신.유니코드입력=None
            elif клавіша_сімвал==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif клавіша_сімвал<128 and chr(клавіша_сімвал) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(клавіша_сімвал)
            return
        if клавіша_сімвал in (0xff31,0xffc6) or клавіша_сімвал==32 and клавіша_SHIFT and not кіраванне_клавіша:
            if клавіша_сімвал not in 자신.пераход_клавіша: 자신.пераход_рэжым()
            자신.пераход_клавіша.add(клавіша_сімвал)
            return
        if клавіша_сімвал==0xff08 and 자신.한글여부 and not кіраванне_клавіша and 자신.한글조합기.앞글자지우기(): return
        if кіраванне_клавіша and клавіша_SHIFT and клавіша_сімвал in (ord('t'),ord('T')):
            자신.адправіць(bytes([30,2,1,0,0,0,0])); return
        if клавіша_сімвал==0xffc3: 자신.адправіць(bytes([30,2,2,0,0,0,0])); return
        if клавіша_сімвал==0xffc9: 자신.адправіць(bytes([30,2,3,0,0,0,0])); return
        if кіраванне_клавіша and клавіша_SHIFT and клавіша_сімвал in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.адправіць(자신.буфер_абмену_значэнне); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if клавіша_сімвал in 특수글쇠: 자신.адправіць(특수글쇠[клавіша_сімвал]); return
        сімвал_кадаванне = клавіша_сімвал & 0xffffff if клавіша_сімвал & 0xff000000 == 0x01000000 else клавіша_сімвал
        if сімвал_кадаванне > 0x10ffff or 0xd800 <= сімвал_кадаванне <= 0xdfff or клавіша_сімвал >= 0xff00 and клавіша_сімвал < 0x1000000: return
        if кіраванне_клавіша and 0x40 <= сімвал_кадаванне <= 0x7f: 자신.адправіць(bytes([сімвал_кадаванне & 31])); return
        if сімвал_кадаванне < 32: return
        if 자신.한글여부 and 자신.службовая_клавіша & {0xffea,0xfe03,0xff7e} and not кіраванне_клавіша and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.канал_клавіша(chr(сімвал_кадаванне), altgr=True): return
        앞부분 = b'\x1b' if 자신.службовая_клавіша & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not кіраванне_клавіша and not 앞부분 and 32<=сімвал_кадаванне<127:
            сімвал_дадзеныя_4d9f8719=chr(сімвал_кадаванне).upper() if клавіша_SHIFT else chr(сімвал_кадаванне)
            if 자신.한글조합기.канал_клавіша(сімвал_дадзеныя_4d9f8719): return
        자신.адправіць(앞부분 + chr(сімвал_кадаванне).encode('utf-8'))


class злучаць_працоўны_стол:
    def __init__(자신, Працэс):
        자신.Працэс=Працэс; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Тэрмінал=False; 자신.시작화면=False; 자신.닫힘=False

    def адправіць(자신, дадзеныя):
        if not дадзеныя or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Працэс.stdin.write(дадзеныя); 자신.Працэс.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                дадзеныя=자신.Працэс.stdout.read(4096)
                if not дадзеныя: break
                sys.stdout.buffer.write(дадзеныя); sys.stdout.buffer.flush()
                끝부분=(끝부분+дадзеныя)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Тэрмінал=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.адправіць(b'terminal\n')
        finally: 자신.닫힘=True

    def кліент(자신, кліент, ШЛЯХ):
        сервер_значэнне=socket.socket(socket.AF_UNIX); сервер_значэнне.settimeout(10); кліент.settimeout(10)
        клавіятура_увядзенне=клавіятура(자신.адправіць,lambda 한글여부:자신.адправіць(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сервер_значэнне.connect(str(ШЛЯХ))
            # 초기 협상은 순서대로 끝낸다. 이후 Выхад 가닥만 클라이언트에 쓴다.
            кліент.sendall(정확한값(сервер_значэнне,12))
            판번호=정확한값(кліент,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сервер_значэнне.sendall(판번호)
            개수=정확한값(сервер_значэнне,1);кліент.sendall(개수+정확한값(сервер_значэнне,개수[0]))
            Бяспека=정확한값(кліент,1)
            if Бяспека!=b'\x01': raise ValueError('unexpected security type')
            сервер_значэнне.sendall(Бяспека)
            if 판번호==b'RFB 003.008\n':кліент.sendall(정확한값(сервер_значэнне,4))
            сервер_значэнне.sendall(정확한값(кліент,1))
            초기값=정확한값(сервер_значэнне,24)
            кліент.sendall(초기값+정확한값(сервер_значэнне,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            кліент.settimeout(None);сервер_значэнне.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        катэгорыя_значэнне=정확한값(сервер_значэнне,1)[0]
                        if катэгорыя_значэнне==0:
                            머리=정확한값(сервер_значэнне,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 аддалены_значэнне 포인터의 중복을 피한다.
                            схаваны_значэнне=포인터지원
                            if схаваны_значэнне:кліент.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            кліент.sendall(bytes([катэгорыя_значэнне])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(сервер_значэнне,12);가로,세로,폭,높이,кадаванне_значэнне=struct.unpack('>HHHHi',사각형)
                                if кадаванне_значэнне!=0:raise ValueError('unexpected framebuffer encoding: '+str(кадаванне_значэнне))
                                кліент.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    дадзеныя=정확한값(сервер_значэнне,min(남음,65536));кліент.sendall(дадзеныя);남음-=len(дадзеныя)
                        elif катэгорыя_значэнне==1:
                            머리=정확한값(сервер_значэнне,5);개수=struct.unpack('>H',머리[3:])[0]
                            кліент.sendall(bytes([катэгорыя_значэнне])+머리+정확한값(сервер_значэнне,개수*6))
                        elif катэгорыя_значэнне==2:кліент.sendall(bytes([катэгорыя_значэнне]))
                        elif катэгорыя_значэнне==3:
                            머리=정확한값(сервер_значэнне,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            кліент.sendall(bytes([катэгорыя_значэнне])+머리+정확한값(сервер_значэнне,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(катэгорыя_значэнне))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:кліент.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                катэгорыя_значэнне=정확한값(кліент,1)[0]
                if катэгорыя_значэнне==4:
                    асноўны_тэкст=정확한값(кліент,7); клавіятура_увядзенне.누름값(асноўны_тэкст[0]!=0,struct.unpack('>I',асноўны_тэкст[3:])[0]); continue
                if катэгорыя_значэнне==255:
                    асноўны_тэкст=정확한값(кліент,11)
                    if асноўны_тэкст[0]!=0: raise ValueError('unsupported QEMU input extension')
                    клавіятура_увядзенне.누름값(struct.unpack('>H',асноўны_тэкст[1:3])[0]!=0,struct.unpack('>I',асноўны_тэкст[3:7])[0]); continue
                if катэгорыя_значэнне==5:
                    асноўны_тэкст=정확한값(кліент,5); 단추들,каардыната_x,세로좌표=struct.unpack('>BHH',асноўны_тэкст)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: клавіятура_увядзенне.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=каардыната_x<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.адправіць(bytes([ord('1')+색인]))
                    else: 자신.адправіць(bytes([30,1,단추들,каардыната_x&255,каардыната_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if катэгорыя_значэнне==6:
                    асноўны_тэкст=정확한값(кліент,7); даўжыня_значэнне=struct.unpack('>i',асноўны_тэкст[3:])[0]
                    if abs(даўжыня_значэнне)>65536: raise ValueError('clipboard too large')
                    Тэкст=정확한값(кліент,abs(даўжыня_значэнне))
                    if даўжыня_значэнне>=0:
                        try: клавіятура_увядзенне.буфер_абмену_значэнне=Тэкст.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: клавіятура_увядзенне.буфер_абмену_значэнне=Тэкст.decode('latin-1').encode('utf-8')
                        клавіятура_увядзенне.буфер_абмену_значэнне=клавіятура_увядзенне.буфер_абмену_значэнне[:65536].decode('utf-8','ignore').encode('utf-8')
                    сервер_значэнне.sendall(bytes([катэгорыя_значэнне])+асноўны_тэкст+Тэкст); continue
                if катэгорыя_значэнне==0:
                    асноўны_тэкст=정확한값(кліент,19)
                    if асноўны_тэкст[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=асноўны_тэкст[3]//8
                elif катэгорыя_значэнне==2:
                    асноўны_тэкст=정확한값(кліент,3); 항목수=struct.unpack('>H',асноўны_тэкст[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(кліент,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 значэнне_па_змаўчанні Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    асноўны_тэкст=struct.pack('>BHi',0,1,0)
                elif катэгорыя_значэнне in (3,150): асноўны_тэкст=정확한값(кліент,9)
                elif катэгорыя_значэнне==248:
                    асноўны_тэкст=정확한값(кліент,8)
                    if асноўны_тэкст[7]>64: raise ValueError('fence too large')
                    асноўны_тэкст+=정확한값(кліент,асноўны_тэкст[7])
                elif катэгорыя_значэнне==250: асноўны_тэкст=정확한값(кліент,3)
                elif катэгорыя_значэнне==251:
                    асноўны_тэкст=정확한값(кліент,7)
                    if асноўны_тэкст[5]>16: raise ValueError('too many screens')
                    асноўны_тэкст+=정확한값(кліент,асноўны_тэкст[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(катэгорыя_значэнне))
                сервер_значэнне.sendall(bytes([катэгорыя_значэнне])+асноўны_тэкст)
        except (OSError,EOFError,ValueError) as ПАМЫЛКА:
            if str(ПАМЫЛКА): print('VNC client:',ПАМЫЛКА,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (кліент,сервер_значэнне):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def паток_працоўны_стол(нумар_порта=5902, Сетка=False, файл_перанос_нумар_порта=2121, 전달규칙들=(), разрознасць_значэнне=(640, 480), госць_адрас=None, вузел_адрас='127.0.0.1'):
    with ExitStack() as Рэсурсы, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Сетка_мост_увядзенне = None
        if Сетка:
            from Сетка_мост import Сетка_мост
            Сетка_мост_увядзенне = Рэсурсы.enter_context(Сетка_мост(файл_перанос_нумар_порта, 전달규칙들, госць_адрас=госць_адрас, вузел_адрас=вузел_адрас))
        ШЛЯХ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',нумар_порта)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Сетка_мост_увядзенне and (원격화면접속번호==файл_перанос_нумар_порта or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and вузел==원격화면접속번호 for 통신규약,вузел,_ in Сетка_мост_увядзенне.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Працэс=subprocess.Popen(Загад(разрознасць_значэнне)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ШЛЯХ)]+(Сетка_мост_увядзенне.전달인수() if Сетка_мост_увядзенне else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            мост=злучаць_працоўны_стол(Працэс); чытач=threading.Thread(target=мост.직렬입출력,daemon=True); чытач.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Сетка_мост_увядзенне: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(вузел_адрас,файл_перанос_нумар_порта),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Працэс.poll() is None:
                    try: кліент,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): кліент.close(); continue
                    if not ШЛЯХ.exists(): кліент.close(); continue
                    처리작업=threading.Thread(target=мост.кліент,args=(кліент,ШЛЯХ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                мост.닫힘=True
                if Сетка_мост_увядзенне: Сетка_мост_увядзенне.прыпыніць_падзея.set()
                if Працэс.poll() is None:
                    Працэс.terminate()
                    try: Працэс.wait(timeout=5)
                    except subprocess.TimeoutExpired: Працэс.kill(); Працэс.wait()
                чытач.join(timeout=2); Працэс.stdin.close(); Працэс.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Сетка_мост_увядзенне and Сетка_мост_увядзенне.ПАМЫЛКА: raise RuntimeError('network bridge: '+Сетка_мост_увядзенне.ПАМЫЛКА)
            return 0 if 가로채기됨 else Працэс.returncode


if __name__=='__main__':
    from выканаць_каманда import 해상도읽기
    аналізатар=argparse.ArgumentParser(description=__doc__); аналізатар.add_argument('--port',type=int,default=5902)
    аналізатар.add_argument('--resolution',type=해상도읽기,default=(640,480))
    аналізатар.add_argument('--network',action='store_true'); аналізатар.add_argument('--ftp-port',type=int,default=2121)
    аналізатар.add_argument('--forward',action='append',default=[])
    аргумент_масіў=аналізатар.parse_args()
    if аргумент_масіў.forward and not аргумент_масіў.network: аналізатар.error('--forward requires --network')
    raise SystemExit(паток_працоўны_стол(аргумент_масіў.port,Сетка=аргумент_масіў.network,файл_перанос_нумар_порта=аргумент_масіў.ftp_port,전달규칙들=аргумент_масіў.forward,разрознасць_значэнне=аргумент_масіў.resolution))
