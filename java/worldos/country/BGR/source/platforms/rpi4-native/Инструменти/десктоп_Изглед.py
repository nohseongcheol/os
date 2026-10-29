#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Ключ_стойност 입력은 자체 ядро_стойност UART로 전달한다. localhost 전용, 단일 контрол_стойност 클라이언트.
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
from изпълнявам_команда import Команда
from local_input import create


def 정확한값(소켓, Размер):
    данни = bytearray()
    while len(данни) < Размер:
        조각 = 소켓.recv(Размер - len(данни))
        if not 조각: raise EOFError()
        данни.extend(조각)
    return bytes(данни)


class клавиатура:
    def __init__(자신, изпращам, 입력방식알림=None):
        자신.바이트전송 = изпращам; 자신.модифициращ_клавиш = set(); 자신.клипборд_стойност = b''
        자신.한글조합기 = create(изпращам, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.комутатор_Ключ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def изпращам(자신, данни):
        자신.한글조합기.조합확정()
        자신.바이트전송(данни)

    def комутатор_режим(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Ключ_символ):
        if Ключ_символ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.модифициращ_клавиш.add(Ключ_символ)
            else: 자신.модифициращ_клавиш.discard(Ключ_символ)
            return
        if not 누르는중:
            자신.комутатор_Ключ.discard(Ключ_символ)
            return
        контрол_Ключ = bool(자신.модифициращ_клавиш & {0xffe3, 0xffe4})
        윗글쇠 = bool(자신.модифициращ_клавиш & {0xffe1, 0xffe2})
        if контрол_Ключ and 윗글쇠 and Ключ_символ in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Ключ_символ in (32,0xff0d):
                try:
                    стойност=int(자신.유니코드입력,16)
                    if 32<=стойност<=0x10ffff and not 0xd800<=стойност<=0xdfff: 자신.изпращам(chr(стойност).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Ключ_символ==0xff1b: 자신.유니코드입력=None
            elif Ключ_символ==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Ключ_символ<128 and chr(Ключ_символ) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Ключ_символ)
            return
        if Ключ_символ in (0xff31,0xffc6) or Ключ_символ==32 and 윗글쇠 and not контрол_Ключ:
            if Ключ_символ not in 자신.комутатор_Ключ: 자신.комутатор_режим()
            자신.комутатор_Ключ.add(Ключ_символ)
            return
        if Ключ_символ==0xff08 and 자신.한글여부 and not контрол_Ключ and 자신.한글조합기.앞글자지우기(): return
        if контрол_Ключ and 윗글쇠 and Ключ_символ in (ord('t'),ord('T')):
            자신.изпращам(bytes([30,2,1,0,0,0,0])); return
        if Ключ_символ==0xffc3: 자신.изпращам(bytes([30,2,2,0,0,0,0])); return
        if Ключ_символ==0xffc9: 자신.изпращам(bytes([30,2,3,0,0,0,0])); return
        if контрол_Ключ and 윗글쇠 and Ключ_символ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.изпращам(자신.клипборд_стойност); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Ключ_символ in 특수글쇠: 자신.изпращам(특수글쇠[Ключ_символ]); return
        знаково_кодиране = Ключ_символ & 0xffffff if Ключ_символ & 0xff000000 == 0x01000000 else Ключ_символ
        if знаково_кодиране > 0x10ffff or 0xd800 <= знаково_кодиране <= 0xdfff or Ключ_символ >= 0xff00 and Ключ_символ < 0x1000000: return
        if контрол_Ключ and 0x40 <= знаково_кодиране <= 0x7f: 자신.изпращам(bytes([знаково_кодиране & 31])); return
        if знаково_кодиране < 32: return
        if 자신.한글여부 and 자신.модифициращ_клавиш & {0xffea,0xfe03,0xff7e} and not контрол_Ключ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.поток_Ключ(chr(знаково_кодиране), altgr=True): return
        앞부분 = b'\x1b' if 자신.модифициращ_клавиш & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not контрол_Ключ and not 앞부분 and 32<=знаково_кодиране<127:
            знакови_данни=chr(знаково_кодиране).upper() if 윗글쇠 else chr(знаково_кодиране)
            if 자신.한글조합기.поток_Ключ(знакови_данни): return
        자신.изпращам(앞부분 + chr(знаково_кодиране).encode('utf-8'))


class връзка_десктоп:
    def __init__(자신, Процес):
        자신.Процес=Процес; 자신.заключване_стойност=threading.Lock(); 자신.준비완료=False; 자신.Терминал=False; 자신.시작화면=False; 자신.닫힘=False

    def изпращам(자신, данни):
        if not данни or 자신.닫힘: return
        with 자신.заключване_стойност:
            try: 자신.Процес.stdin.write(данни); 자신.Процес.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                данни=자신.Процес.stdout.read(4096)
                if not данни: break
                sys.stdout.buffer.write(данни); sys.stdout.buffer.flush()
                끝부분=(끝부분+данни)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Терминал=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.изпращам(b'terminal\n')
        finally: 자신.닫힘=True

    def клиент(자신, клиент, ПЪТ):
        сървър_стойност=socket.socket(socket.AF_UNIX); сървър_стойност.settimeout(10); клиент.settimeout(10)
        клавиатура_запис=клавиатура(자신.изпращам,lambda 한글여부:자신.изпращам(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сървър_стойност.connect(str(ПЪТ))
            # първоначално_състояние 협상은 순서대로 끝낸다. 이후 Изход 가닥만 클라이언트에 쓴다.
            клиент.sendall(정확한값(сървър_стойност,12))
            номер_на_версия=정확한값(клиент,12)
            if номер_на_версия not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сървър_стойност.sendall(номер_на_версия)
            개수=정확한값(сървър_стойност,1);клиент.sendall(개수+정확한값(сървър_стойност,개수[0]))
            Защита=정확한값(клиент,1)
            if Защита!=b'\x01': raise ValueError('unexpected security type')
            сървър_стойност.sendall(Защита)
            if номер_на_версия==b'RFB 003.008\n':клиент.sendall(정확한값(сървър_стойност,4))
            сървър_стойност.sendall(정확한값(клиент,1))
            초기값=정확한값(сървър_стойност,24)
            клиент.sendall(초기값+정확한값(сървър_стойност,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            клиент.settimeout(None);сървър_стойност.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        област_стойност=정확한값(сървър_стойност,1)[0]
                        if област_стойност==0:
                            머리=정확한값(сървър_стойност,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 отдалечен_стойност 포인터의 중복을 피한다.
                            Скрит_стойност=포인터지원
                            if Скрит_стойност:клиент.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            клиент.sendall(bytes([област_стойност])+머리)
                            for _ in range(항목수):
                                правоъгълник=정확한값(сървър_стойност,12);가로,вертикал_позиция,폭,높이,кодиране_стойност=struct.unpack('>HHHHi',правоъгълник)
                                if кодиране_стойност!=0:raise ValueError('unexpected framebuffer encoding: '+str(кодиране_стойност))
                                клиент.sendall(правоъгълник)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    данни=정확한값(сървър_стойност,min(남음,65536));клиент.sendall(данни);남음-=len(данни)
                        elif област_стойност==1:
                            머리=정확한값(сървър_стойност,5);개수=struct.unpack('>H',머리[3:])[0]
                            клиент.sendall(bytes([област_стойност])+머리+정확한값(сървър_стойност,개수*6))
                        elif област_стойност==2:клиент.sendall(bytes([област_стойност]))
                        elif област_стойност==3:
                            머리=정확한값(сървър_стойност,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            клиент.sendall(bytes([област_стойност])+머리+정확한값(сървър_стойност,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(област_стойност))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:клиент.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                област_стойност=정확한값(клиент,1)[0]
                if област_стойност==4:
                    основен_текст=정확한값(клиент,7); клавиатура_запис.누름값(основен_текст[0]!=0,struct.unpack('>I',основен_текст[3:])[0]); continue
                if област_стойност==255:
                    основен_текст=정확한값(клиент,11)
                    if основен_текст[0]!=0: raise ValueError('unsupported QEMU input extension')
                    клавиатура_запис.누름값(struct.unpack('>H',основен_текст[1:3])[0]!=0,struct.unpack('>I',основен_текст[3:7])[0]); continue
                if област_стойност==5:
                    основен_текст=정확한값(клиент,5); 단추들,x_координата,세로좌표=struct.unpack('>BHH',основен_текст)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: клавиатура_запис.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_координата<576 and 112<=세로좌표<372:
                        Търсене_индекс=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and Търсене_индекс<5: 자신.изпращам(bytes([ord('1')+Търсене_индекс]))
                    else: 자신.изпращам(bytes([30,1,단추들,x_координата&255,x_координата>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if област_стойност==6:
                    основен_текст=정확한값(клиент,7); 길이=struct.unpack('>i',основен_текст[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    Текст=정확한값(клиент,abs(길이))
                    if 길이>=0:
                        try: клавиатура_запис.клипборд_стойност=Текст.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: клавиатура_запис.клипборд_стойност=Текст.decode('latin-1').encode('utf-8')
                        клавиатура_запис.клипборд_стойност=клавиатура_запис.клипборд_стойност[:65536].decode('utf-8','ignore').encode('utf-8')
                    сървър_стойност.sendall(bytes([област_стойност])+основен_текст+Текст); continue
                if област_стойност==0:
                    основен_текст=정확한값(клиент,19)
                    if основен_текст[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=основен_текст[3]//8
                elif област_стойност==2:
                    основен_текст=정확한값(клиент,3); 항목수=struct.unpack('>H',основен_текст[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(клиент,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 стойност_по_подразбиране Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    основен_текст=struct.pack('>BHi',0,1,0)
                elif област_стойност in (3,150): основен_текст=정확한값(клиент,9)
                elif област_стойност==248:
                    основен_текст=정확한값(клиент,8)
                    if основен_текст[7]>64: raise ValueError('fence too large')
                    основен_текст+=정확한값(клиент,основен_текст[7])
                elif област_стойност==250: основен_текст=정확한값(клиент,3)
                elif област_стойност==251:
                    основен_текст=정확한값(клиент,7)
                    if основен_текст[5]>16: raise ValueError('too many screens')
                    основен_текст+=정확한값(клиент,основен_текст[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(област_стойност))
                сървър_стойност.sendall(bytes([област_стойност])+основен_текст)
        except (OSError,EOFError,ValueError) as ГРЕШКА:
            if str(ГРЕШКА): print('VNC client:',ГРЕШКА,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (клиент,сървър_стойност):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def изпълнение_десктоп(номер_на_порт=5902, мрежа=False, прехвърляне_на_файл_номер_на_порт=2121, 전달규칙들=(), разделителна_способност_стойност=(640, 480), гост_адрес=None, хост_адрес='127.0.0.1'):
    with ExitStack() as Ресурси, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        мост_запис = None
        if мрежа:
            from мост_3de4fe3a import мост_3de4fe3a
            мост_запис = Ресурси.enter_context(мост_3de4fe3a(прехвърляне_на_файл_номер_на_порт, 전달규칙들, гост_адрес=гост_адрес, хост_адрес=хост_адрес))
        ПЪТ=Path(작업경로)/'display.sock'
        with socket.socket() as получавам_порт:
            получавам_порт.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            получавам_порт.bind(('127.0.0.1',номер_на_порт)); получавам_порт.listen(1); получавам_порт.settimeout(.2)
            원격화면접속번호=получавам_порт.getsockname()[1]
            if мост_запис and (원격화면접속번호==прехвърляне_на_файл_номер_на_порт or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and хост==원격화면접속번호 for 통신규약,хост,_ in мост_запис.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Процес=subprocess.Popen(Команда(разделителна_способност_стойност)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ПЪТ)]+(мост_запис.전달인수() if мост_запис else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            мост=връзка_десктоп(Процес); читател=threading.Thread(target=мост.직렬입출력,daemon=True); читател.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(получавам_порт.getsockname()[1]),flush=True)
            if мост_запис: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(хост_адрес,прехвърляне_на_файл_номер_на_порт),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            обработка_задача=None; 가로채기됨=False
            try:
                while Процес.poll() is None:
                    try: клиент,_=получавам_порт.accept()
                    except socket.timeout: continue
                    if обработка_задача is not None and обработка_задача.is_alive(): клиент.close(); continue
                    if not ПЪТ.exists(): клиент.close(); continue
                    обработка_задача=threading.Thread(target=мост.клиент,args=(клиент,ПЪТ),daemon=True); обработка_задача.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                мост.닫힘=True
                if мост_запис: мост_запис.Пауза_събитие.set()
                if Процес.poll() is None:
                    Процес.terminate()
                    try: Процес.wait(timeout=5)
                    except subprocess.TimeoutExpired: Процес.kill(); Процес.wait()
                читател.join(timeout=2); Процес.stdin.close(); Процес.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if мост_запис and мост_запис.ГРЕШКА: raise RuntimeError('network bridge: '+мост_запис.ГРЕШКА)
            return 0 if 가로채기됨 else Процес.returncode


if __name__=='__main__':
    from изпълнявам_команда import 해상도읽기
    анализатор=argparse.ArgumentParser(description=__doc__); анализатор.add_argument('--port',type=int,default=5902)
    анализатор.add_argument('--resolution',type=해상도읽기,default=(640,480))
    анализатор.add_argument('--network',action='store_true'); анализатор.add_argument('--ftp-port',type=int,default=2121)
    анализатор.add_argument('--forward',action='append',default=[])
    аргумент_масив=анализатор.parse_args()
    if аргумент_масив.forward and not аргумент_масив.network: анализатор.error('--forward requires --network')
    raise SystemExit(изпълнение_десктоп(аргумент_масив.port,мрежа=аргумент_масив.network,прехвърляне_на_файл_номер_на_порт=аргумент_масив.ftp_port,전달규칙들=аргумент_масив.forward,разделителна_способност_стойност=аргумент_масив.resolution))
