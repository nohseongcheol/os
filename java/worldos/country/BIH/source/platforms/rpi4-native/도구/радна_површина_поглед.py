#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, кључ_вриједност 입력은 자체 језгро_вриједност UART로 전달한다. localhost 전용, 단일 контрола_вриједност 클라이언트.
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
from 실행 import команда
from local_input import create


def 정확한값(소켓, подесити_величину):
    подаци = bytearray()
    while len(подаци) < подесити_величину:
        조각 = 소켓.recv(подесити_величину - len(подаци))
        if not 조각: raise EOFError()
        подаци.extend(조각)
    return bytes(подаци)


class тастатура:
    def __init__(자신, послати, 입력방식알림=None):
        자신.바이트전송 = послати; 자신.модификаторска_типка = set(); 자신.међуспремник_вриједност = b''
        자신.한글조합기 = create(послати, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.промијенити_кључ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def послати(자신, подаци):
        자신.한글조합기.조합확정()
        자신.바이트전송(подаци)

    def промијенити_мод(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, 글쇠기호):
        if 글쇠기호 in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.модификаторска_типка.add(글쇠기호)
            else: 자신.модификаторска_типка.discard(글쇠기호)
            return
        if not 누르는중:
            자신.промијенити_кључ.discard(글쇠기호)
            return
        CTRL = bool(자신.модификаторска_типка & {0xffe3, 0xffe4})
        типка_SHIFT = bool(자신.модификаторска_типка & {0xffe1, 0xffe2})
        if CTRL and типка_SHIFT and 글쇠기호 in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if 글쇠기호 in (32,0xff0d):
                try:
                    вриједност=int(자신.유니코드입력,16)
                    if 32<=вриједност<=0x10ffff and not 0xd800<=вриједност<=0xdfff: 자신.послати(chr(вриједност).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif 글쇠기호==0xff1b: 자신.유니코드입력=None
            elif 글쇠기호==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif 글쇠기호<128 and chr(글쇠기호) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(글쇠기호)
            return
        if 글쇠기호 in (0xff31,0xffc6) or 글쇠기호==32 and типка_SHIFT and not CTRL:
            if 글쇠기호 not in 자신.промијенити_кључ: 자신.промијенити_мод()
            자신.промијенити_кључ.add(글쇠기호)
            return
        if 글쇠기호==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and типка_SHIFT and 글쇠기호 in (ord('t'),ord('T')):
            자신.послати(bytes([30,2,1,0,0,0,0])); return
        if 글쇠기호==0xffc3: 자신.послати(bytes([30,2,2,0,0,0,0])); return
        if 글쇠기호==0xffc9: 자신.послати(bytes([30,2,3,0,0,0,0])); return
        if CTRL and типка_SHIFT and 글쇠기호 in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.послати(자신.међуспремник_вриједност); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if 글쇠기호 in 특수글쇠: 자신.послати(특수글쇠[글쇠기호]); return
        знак_кодирање = 글쇠기호 & 0xffffff if 글쇠기호 & 0xff000000 == 0x01000000 else 글쇠기호
        if знак_кодирање > 0x10ffff or 0xd800 <= знак_кодирање <= 0xdfff or 글쇠기호 >= 0xff00 and 글쇠기호 < 0x1000000: return
        if CTRL and 0x40 <= знак_кодирање <= 0x7f: 자신.послати(bytes([знак_кодирање & 31])); return
        if знак_кодирање < 32: return
        if 자신.한글여부 and 자신.модификаторска_типка & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.сажетак_садржаја_кључ(chr(знак_кодирање), altgr=True): return
        앞부분 = b'\x1b' if 자신.модификаторска_типка & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=знак_кодирање<127:
            знак_подаци=chr(знак_кодирање).upper() if типка_SHIFT else chr(знак_кодирање)
            if 자신.한글조합기.сажетак_садржаја_кључ(знак_подаци): return
        자신.послати(앞부분 + chr(знак_кодирање).encode('utf-8'))


class повезати_радна_површина:
    def __init__(자신, процес):
        자신.процес=процес; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def послати(자신, подаци):
        if not подаци or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.процес.stdin.write(подаци); 자신.процес.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                подаци=자신.процес.stdout.read(4096)
                if not подаци: break
                sys.stdout.buffer.write(подаци); sys.stdout.buffer.flush()
                끝부분=(끝부분+подаци)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.послати(b'terminal\n')
        finally: 자신.닫힘=True

    def клијент(자신, клијент, пут):
        сервер_вриједност=socket.socket(socket.AF_UNIX); сервер_вриједност.settimeout(10); клијент.settimeout(10)
        тастатура_унос=тастатура(자신.послати,lambda 한글여부:자신.послати(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сервер_вриједност.connect(str(пут))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            клијент.sendall(정확한값(сервер_вриједност,12))
            판번호=정확한값(клијент,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сервер_вриједност.sendall(판번호)
            개수=정확한값(сервер_вриједност,1);клијент.sendall(개수+정확한값(сервер_вриједност,개수[0]))
            сигурност=정확한값(клијент,1)
            if сигурност!=b'\x01': raise ValueError('unexpected security type')
            сервер_вриједност.sendall(сигурност)
            if 판번호==b'RFB 003.008\n':клијент.sendall(정확한값(сервер_вриједност,4))
            сервер_вриједност.sendall(정확한값(клијент,1))
            초기값=정확한값(сервер_вриједност,24)
            клијент.sendall(초기값+정확한값(сервер_вриједност,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            клијент.settimeout(None);сервер_вриједност.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        категорија_вриједност=정확한값(сервер_вриједност,1)[0]
                        if категорија_вриједност==0:
                            머리=정확한값(сервер_вриједност,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 удаљено_вриједност 포인터의 중복을 피한다.
                            скривено_вриједност=포인터지원
                            if скривено_вриједност:клијент.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            клијент.sendall(bytes([категорија_вриједност])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(сервер_вриједност,12);가로,세로,폭,높이,кодирање_вриједност=struct.unpack('>HHHHi',사각형)
                                if кодирање_вриједност!=0:raise ValueError('unexpected framebuffer encoding: '+str(кодирање_вриједност))
                                клијент.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    подаци=정확한값(сервер_вриједност,min(남음,65536));клијент.sendall(подаци);남음-=len(подаци)
                        elif категорија_вриједност==1:
                            머리=정확한값(сервер_вриједност,5);개수=struct.unpack('>H',머리[3:])[0]
                            клијент.sendall(bytes([категорија_вриједност])+머리+정확한값(сервер_вриједност,개수*6))
                        elif категорија_вриједност==2:клијент.sendall(bytes([категорија_вриједност]))
                        elif категорија_вриједност==3:
                            머리=정확한값(сервер_вриједност,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            клијент.sendall(bytes([категорија_вриједност])+머리+정확한값(сервер_вриједност,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(категорија_вриједност))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:клијент.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                категорија_вриједност=정확한값(клијент,1)[0]
                if категорија_вриједност==4:
                    Тијело_текста=정확한값(клијент,7); тастатура_унос.누름값(Тијело_текста[0]!=0,struct.unpack('>I',Тијело_текста[3:])[0]); continue
                if категорија_вриједност==255:
                    Тијело_текста=정확한값(клијент,11)
                    if Тијело_текста[0]!=0: raise ValueError('unsupported QEMU input extension')
                    тастатура_унос.누름값(struct.unpack('>H',Тијело_текста[1:3])[0]!=0,struct.unpack('>I',Тијело_текста[3:7])[0]); continue
                if категорија_вриједност==5:
                    Тијело_текста=정확한값(клијент,5); 단추들,가로좌표,세로좌표=struct.unpack('>BHH',Тијело_текста)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: тастатура_унос.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=가로좌표<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.послати(bytes([ord('1')+색인]))
                    else: 자신.послати(bytes([30,1,단추들,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if категорија_вриједност==6:
                    Тијело_текста=정확한값(клијент,7); дужина_вриједност=struct.unpack('>i',Тијело_текста[3:])[0]
                    if abs(дужина_вриједност)>65536: raise ValueError('clipboard too large')
                    текст=정확한값(клијент,abs(дужина_вриједност))
                    if дужина_вриједност>=0:
                        try: тастатура_унос.међуспремник_вриједност=текст.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: тастатура_унос.међуспремник_вриједност=текст.decode('latin-1').encode('utf-8')
                        тастатура_унос.међуспремник_вриједност=тастатура_унос.међуспремник_вриједност[:65536].decode('utf-8','ignore').encode('utf-8')
                    сервер_вриједност.sendall(bytes([категорија_вриједност])+Тијело_текста+текст); continue
                if категорија_вриједност==0:
                    Тијело_текста=정확한값(клијент,19)
                    if Тијело_текста[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=Тијело_текста[3]//8
                elif категорија_вриједност==2:
                    Тијело_текста=정확한값(клијент,3); 항목수=struct.unpack('>H',Тијело_текста[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(клијент,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 задана_вриједност Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    Тијело_текста=struct.pack('>BHi',0,1,0)
                elif категорија_вриједност in (3,150): Тијело_текста=정확한값(клијент,9)
                elif категорија_вриједност==248:
                    Тијело_текста=정확한값(клијент,8)
                    if Тијело_текста[7]>64: raise ValueError('fence too large')
                    Тијело_текста+=정확한값(клијент,Тијело_текста[7])
                elif категорија_вриједност==250: Тијело_текста=정확한값(клијент,3)
                elif категорија_вриједност==251:
                    Тијело_текста=정확한값(клијент,7)
                    if Тијело_текста[5]>16: raise ValueError('too many screens')
                    Тијело_текста+=정확한값(клијент,Тијело_текста[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(категорија_вриједност))
                сервер_вриједност.sendall(bytes([категорија_вриједност])+Тијело_текста)
        except (OSError,EOFError,ValueError) as грешка:
            if str(грешка): print('VNC client:',грешка,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (клијент,сервер_вриједност):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def 바탕화면실행(접속번호=5902, Мрежа=False, 파일전송접속번호=2121, 전달규칙들=(), резолуција_вриједност=(640, 480), 게스트주소=None, хост_рачунар_адреса='127.0.0.1'):
    with ExitStack() as Ресурси, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if Мрежа:
            from 통신다리 import 통신다리
            통신다리항목 = Ресурси.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, хост_рачунар_адреса=хост_рачунар_адреса))
        пут=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and хост_рачунар==원격화면접속번호 for 통신규약,хост_рачунар,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            процес=subprocess.Popen(команда(резолуција_вриједност)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(пут)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=повезати_радна_површина(процес); читач=threading.Thread(target=연결다리.직렬입출력,daemon=True); читач.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(хост_рачунар_адреса,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while процес.poll() is None:
                    try: клијент,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): клијент.close(); continue
                    if not пут.exists(): клијент.close(); continue
                    처리작업=threading.Thread(target=연결다리.клијент,args=(клијент,пут),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.пауза_догађај.set()
                if процес.poll() is None:
                    процес.terminate()
                    try: процес.wait(timeout=5)
                    except subprocess.TimeoutExpired: процес.kill(); процес.wait()
                читач.join(timeout=2); процес.stdin.close(); процес.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.грешка: raise RuntimeError('network bridge: '+통신다리항목.грешка)
            return 0 if 가로채기됨 else процес.returncode


if __name__=='__main__':
    from 실행 import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    аргумент_низ=인수해석기.parse_args()
    if аргумент_низ.forward and not аргумент_низ.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(바탕화면실행(аргумент_низ.port,Мрежа=аргумент_низ.network,파일전송접속번호=аргумент_низ.ftp_port,전달규칙들=аргумент_низ.forward,резолуција_вриједност=аргумент_низ.resolution))
