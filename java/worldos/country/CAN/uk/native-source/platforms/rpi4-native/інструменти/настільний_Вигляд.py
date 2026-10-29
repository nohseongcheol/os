#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Ключ_значення 입력은 своє ядро_значення UART로 전달한다. localhost 전용, 단일 керування_значення 클라이언트.
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
from Виконати_команда import команда
from local_input import create


def 정확한값(сокет_значення, Розмір):
    дані = bytearray()
    while len(дані) < Розмір:
        조각 = сокет_значення.recv(Розмір - len(дані))
        if not 조각: raise EOFError()
        дані.extend(조각)
    return bytes(дані)


class клавіатура:
    def __init__(자신, надсилати, 입력방식알림=None):
        자신.바이트전송 = надсилати; 자신.службова_клавіша = set(); 자신.буфер_обміну_значення = b''
        자신.한글조합기 = create(надсилати, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.перехід_Ключ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def надсилати(자신, дані):
        자신.한글조합기.조합확정()
        자신.바이트전송(дані)

    def перехід_режим(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Ключ_символ):
        if Ключ_символ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.службова_клавіша.add(Ключ_символ)
            else: 자신.службова_клавіша.discard(Ключ_символ)
            return
        if not 누르는중:
            자신.перехід_Ключ.discard(Ключ_символ)
            return
        керування_Ключ = bool(자신.службова_клавіша & {0xffe3, 0xffe4})
        윗글쇠 = bool(자신.службова_клавіша & {0xffe1, 0xffe2})
        if керування_Ключ and 윗글쇠 and Ключ_символ in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Ключ_символ in (32,0xff0d):
                try:
                    значення=int(자신.유니코드입력,16)
                    if 32<=значення<=0x10ffff and not 0xd800<=значення<=0xdfff: 자신.надсилати(chr(значення).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Ключ_символ==0xff1b: 자신.유니코드입력=None
            elif Ключ_символ==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Ключ_символ<128 and chr(Ключ_символ) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Ключ_символ)
            return
        if Ключ_символ in (0xff31,0xffc6) or Ключ_символ==32 and 윗글쇠 and not керування_Ключ:
            if Ключ_символ not in 자신.перехід_Ключ: 자신.перехід_режим()
            자신.перехід_Ключ.add(Ключ_символ)
            return
        if Ключ_символ==0xff08 and 자신.한글여부 and not керування_Ключ and 자신.한글조합기.앞글자지우기(): return
        if керування_Ключ and 윗글쇠 and Ключ_символ in (ord('t'),ord('T')):
            자신.надсилати(bytes([30,2,1,0,0,0,0])); return
        if Ключ_символ==0xffc3: 자신.надсилати(bytes([30,2,2,0,0,0,0])); return
        if Ключ_символ==0xffc9: 자신.надсилати(bytes([30,2,3,0,0,0,0])); return
        if керування_Ключ and 윗글쇠 and Ключ_символ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.надсилати(자신.буфер_обміну_значення); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Ключ_символ in 특수글쇠: 자신.надсилати(특수글쇠[Ключ_символ]); return
        кодування_символів = Ключ_символ & 0xffffff if Ключ_символ & 0xff000000 == 0x01000000 else Ключ_символ
        if кодування_символів > 0x10ffff or 0xd800 <= кодування_символів <= 0xdfff or Ключ_символ >= 0xff00 and Ключ_символ < 0x1000000: return
        if керування_Ключ and 0x40 <= кодування_символів <= 0x7f: 자신.надсилати(bytes([кодування_символів & 31])); return
        if кодування_символів < 32: return
        if 자신.한글여부 and 자신.службова_клавіша & {0xffea,0xfe03,0xff7e} and not керування_Ключ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.канал_Ключ(chr(кодування_символів), altgr=True): return
        앞부분 = b'\x1b' if 자신.службова_клавіша & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not керування_Ключ and not 앞부분 and 32<=кодування_символів<127:
            символьні_дані=chr(кодування_символів).upper() if 윗글쇠 else chr(кодування_символів)
            if 자신.한글조합기.канал_Ключ(символьні_дані): return
        자신.надсилати(앞부분 + chr(кодування_символів).encode('utf-8'))


class зв_язок_настільний:
    def __init__(자신, Процеси):
        자신.Процеси=Процеси; 자신.блокувати_значення=threading.Lock(); 자신.준비완료=False; 자신.термінал=False; 자신.시작화면=False; 자신.닫힘=False

    def надсилати(자신, дані):
        if not дані or 자신.닫힘: return
        with 자신.блокувати_значення:
            try: 자신.Процеси.stdin.write(дані); 자신.Процеси.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                дані=자신.Процеси.stdout.read(4096)
                if not дані: break
                sys.stdout.buffer.write(дані); sys.stdout.buffer.flush()
                끝부분=(끝부분+дані)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.термінал=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.надсилати(b'terminal\n')
        finally: 자신.닫힘=True

    def клієнт(자신, клієнт, шлях):
        сервер_значення=socket.socket(socket.AF_UNIX); сервер_значення.settimeout(10); клієнт.settimeout(10)
        клавіатура_запис=клавіатура(자신.надсилати,lambda 한글여부:자신.надсилати(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сервер_значення.connect(str(шлях))
            # початковий_стан 협상은 순서대로 끝낸다. 이후 Вивід 가닥만 클라이언트에 쓴다.
            клієнт.sendall(정확한값(сервер_значення,12))
            номер_версії=정확한값(клієнт,12)
            if номер_версії not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сервер_значення.sendall(номер_версії)
            개수=정확한값(сервер_значення,1);клієнт.sendall(개수+정확한값(сервер_значення,개수[0]))
            захист=정확한값(клієнт,1)
            if захист!=b'\x01': raise ValueError('unexpected security type')
            сервер_значення.sendall(захист)
            if номер_версії==b'RFB 003.008\n':клієнт.sendall(정확한값(сервер_значення,4))
            сервер_значення.sendall(정확한값(клієнт,1))
            초기값=정확한값(сервер_значення,24)
            клієнт.sendall(초기값+정확한값(сервер_значення,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            клієнт.settimeout(None);сервер_значення.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        область_значення=정확한값(сервер_значення,1)[0]
                        if область_значення==0:
                            머리=정확한값(сервер_значення,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 віддалений_значення 포인터의 중복을 피한다.
                            Прихований_значення=포인터지원
                            if Прихований_значення:клієнт.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            клієнт.sendall(bytes([область_значення])+머리)
                            for _ in range(항목수):
                                прямокутник=정확한값(сервер_значення,12);가로,Вертикаль_посада,폭,높이,кодування_значення=struct.unpack('>HHHHi',прямокутник)
                                if кодування_значення!=0:raise ValueError('unexpected framebuffer encoding: '+str(кодування_значення))
                                клієнт.sendall(прямокутник)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    дані=정확한값(сервер_значення,min(남음,65536));клієнт.sendall(дані);남음-=len(дані)
                        elif область_значення==1:
                            머리=정확한값(сервер_значення,5);개수=struct.unpack('>H',머리[3:])[0]
                            клієнт.sendall(bytes([область_значення])+머리+정확한값(сервер_значення,개수*6))
                        elif область_значення==2:клієнт.sendall(bytes([область_значення]))
                        elif область_значення==3:
                            머리=정확한값(сервер_значення,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            клієнт.sendall(bytes([область_значення])+머리+정확한값(сервер_значення,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(область_значення))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:клієнт.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            фоноваЗадача=threading.Thread(target=출력결과,daemon=True);фоноваЗадача.start()
            while not 자신.닫힘:
                область_значення=정확한값(клієнт,1)[0]
                if область_значення==4:
                    основний_текст=정확한값(клієнт,7); клавіатура_запис.누름값(основний_текст[0]!=0,struct.unpack('>I',основний_текст[3:])[0]); continue
                if область_значення==255:
                    основний_текст=정확한값(клієнт,11)
                    if основний_текст[0]!=0: raise ValueError('unsupported QEMU input extension')
                    клавіатура_запис.누름값(struct.unpack('>H',основний_текст[1:3])[0]!=0,struct.unpack('>I',основний_текст[3:7])[0]); continue
                if область_значення==5:
                    основний_текст=정확한값(клієнт,5); 단추들,координата_X,세로좌표=struct.unpack('>BHH',основний_текст)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: клавіатура_запис.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=координата_X<576 and 112<=세로좌표<372:
                        Інформування_індекс=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and Інформування_індекс<5: 자신.надсилати(bytes([ord('1')+Інформування_індекс]))
                    else: 자신.надсилати(bytes([30,1,단추들,координата_X&255,координата_X>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if область_значення==6:
                    основний_текст=정확한값(клієнт,7); 길이=struct.unpack('>i',основний_текст[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    текст=정확한값(клієнт,abs(길이))
                    if 길이>=0:
                        try: клавіатура_запис.буфер_обміну_значення=текст.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: клавіатура_запис.буфер_обміну_значення=текст.decode('latin-1').encode('utf-8')
                        клавіатура_запис.буфер_обміну_значення=клавіатура_запис.буфер_обміну_значення[:65536].decode('utf-8','ignore').encode('utf-8')
                    сервер_значення.sendall(bytes([область_значення])+основний_текст+текст); continue
                if область_значення==0:
                    основний_текст=정확한값(клієнт,19)
                    if основний_текст[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=основний_текст[3]//8
                elif область_значення==2:
                    основний_текст=정확한값(клієнт,3); 항목수=struct.unpack('>H',основний_текст[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(клієнт,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 стандартне_значення Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    основний_текст=struct.pack('>BHi',0,1,0)
                elif область_значення in (3,150): основний_текст=정확한값(клієнт,9)
                elif область_значення==248:
                    основний_текст=정확한값(клієнт,8)
                    if основний_текст[7]>64: raise ValueError('fence too large')
                    основний_текст+=정확한값(клієнт,основний_текст[7])
                elif область_значення==250: основний_текст=정확한값(клієнт,3)
                elif область_значення==251:
                    основний_текст=정확한값(клієнт,7)
                    if основний_текст[5]>16: raise ValueError('too many screens')
                    основний_текст+=정확한값(клієнт,основний_текст[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(область_значення))
                сервер_значення.sendall(bytes([область_значення])+основний_текст)
        except (OSError,EOFError,ValueError) as ПОМИЛКА:
            if str(ПОМИЛКА): print('VNC client:',ПОМИЛКА,file=sys.stderr,flush=True)
        finally:
            for сокет_значення in (клієнт,сервер_значення):
                try: сокет_значення.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                сокет_значення.close()


def запускати_настільний(номер_порту=5902, мережа=False, передавання_файлу_номер_порту=2121, 전달규칙들=(), роздільна_здатність_значення=(640, 480), гість_адреса=None, хост_адреса='127.0.0.1'):
    with ExitStack() as Ресурси, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        міст_запис = None
        if мережа:
            from міст_3de4fe3a import міст_3de4fe3a
            міст_запис = Ресурси.enter_context(міст_3de4fe3a(передавання_файлу_номер_порту, 전달규칙들, гість_адреса=гість_адреса, хост_адреса=хост_адреса))
        шлях=Path(작업경로)/'display.sock'
        with socket.socket() as отримувати_порт:
            отримувати_порт.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            отримувати_порт.bind(('127.0.0.1',номер_порту)); отримувати_порт.listen(1); отримувати_порт.settimeout(.2)
            원격화면접속번호=отримувати_порт.getsockname()[1]
            if міст_запис and (원격화면접속번호==передавання_файлу_номер_порту or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and хост==원격화면접속번호 for 통신규약,хост,_ in міст_запис.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Процеси=subprocess.Popen(команда(роздільна_здатність_значення)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(шлях)]+(міст_запис.전달인수() if міст_запис else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            міст=зв_язок_настільний(Процеси); читач=threading.Thread(target=міст.직렬입출력,daemon=True); читач.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(отримувати_порт.getsockname()[1]),flush=True)
            if міст_запис: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(хост_адреса,передавання_файлу_номер_порту),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            обробка_справа=None; 가로채기됨=False
            try:
                while Процеси.poll() is None:
                    try: клієнт,_=отримувати_порт.accept()
                    except socket.timeout: continue
                    if обробка_справа is not None and обробка_справа.is_alive(): клієнт.close(); continue
                    if not шлях.exists(): клієнт.close(); continue
                    обробка_справа=threading.Thread(target=міст.клієнт,args=(клієнт,шлях),daemon=True); обробка_справа.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                міст.닫힘=True
                if міст_запис: міст_запис.Пауза_подія.set()
                if Процеси.poll() is None:
                    Процеси.terminate()
                    try: Процеси.wait(timeout=5)
                    except subprocess.TimeoutExpired: Процеси.kill(); Процеси.wait()
                читач.join(timeout=2); Процеси.stdin.close(); Процеси.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if міст_запис and міст_запис.ПОМИЛКА: raise RuntimeError('network bridge: '+міст_запис.ПОМИЛКА)
            return 0 if 가로채기됨 else Процеси.returncode


if __name__=='__main__':
    from Виконати_команда import 해상도읽기
    аналізатор=argparse.ArgumentParser(description=__doc__); аналізатор.add_argument('--port',type=int,default=5902)
    аналізатор.add_argument('--resolution',type=해상도읽기,default=(640,480))
    аналізатор.add_argument('--network',action='store_true'); аналізатор.add_argument('--ftp-port',type=int,default=2121)
    аналізатор.add_argument('--forward',action='append',default=[])
    аргумент_масив=аналізатор.parse_args()
    if аргумент_масив.forward and not аргумент_масив.network: аналізатор.error('--forward requires --network')
    raise SystemExit(запускати_настільний(аргумент_масив.port,мережа=аргумент_масив.network,передавання_файлу_номер_порту=аргумент_масив.ftp_port,전달규칙들=аргумент_масив.forward,роздільна_здатність_значення=аргумент_масив.resolution))
