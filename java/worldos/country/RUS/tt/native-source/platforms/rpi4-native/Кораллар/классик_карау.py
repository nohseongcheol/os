#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ачкыч_VALUE 입력은 자체 төш_VALUE UART로 전달한다. localhost 전용, 단일 идарә_VALUE 클라이언트.
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
from үтәргә_команда import команда
from local_input import create


def EXACT_VALUE(소켓, үлчәмен_үзгәртү):
    мәгълүмат = bytearray()
    while len(мәгълүмат) < үлчәмен_үзгәртү:
        조각 = 소켓.recv(үлчәмен_үзгәртү - len(мәгълүмат))
        if not 조각: raise EOFError()
        мәгълүмат.extend(조각)
    return bytes(мәгълүмат)


class төймәсар:
    def __init__(자신, җибәрү, 입력방식알림=None):
        자신.바이트전송 = җибәрү; 자신.идарә_төймәләре = set(); 자신.алмашу_буферы_VALUE = b''
        자신.한글조합기 = create(җибәрү, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_ачкыч = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def җибәрү(자신, мәгълүмат):
        자신.한글조합기.조합확정()
        자신.바이트전송(мәгълүмат)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, ачкыч_символ):
        if ачкыч_символ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.идарә_төймәләре.add(ачкыч_символ)
            else: 자신.идарә_төймәләре.discard(ачкыч_символ)
            return
        if not 누르는중:
            자신.SWITCH_ачкыч.discard(ачкыч_символ)
            return
        CTRL = bool(자신.идарә_төймәләре & {0xffe3, 0xffe4})
        SHIFT_төймәсе = bool(자신.идарә_төймәләре & {0xffe1, 0xffe2})
        if CTRL and SHIFT_төймәсе and ачкыч_символ in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if ачкыч_символ in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.җибәрү(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif ачкыч_символ==0xff1b: 자신.유니코드입력=None
            elif ачкыч_символ==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif ачкыч_символ<128 and chr(ачкыч_символ) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(ачкыч_символ)
            return
        if ачкыч_символ in (0xff31,0xffc6) or ачкыч_символ==32 and SHIFT_төймәсе and not CTRL:
            if ачкыч_символ not in 자신.SWITCH_ачкыч: 자신.SWITCH_MODE()
            자신.SWITCH_ачкыч.add(ачкыч_символ)
            return
        if ачкыч_символ==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_төймәсе and ачкыч_символ in (ord('t'),ord('T')):
            자신.җибәрү(bytes([30,2,1,0,0,0,0])); return
        if ачкыч_символ==0xffc3: 자신.җибәрү(bytes([30,2,2,0,0,0,0])); return
        if ачкыч_символ==0xffc9: 자신.җибәрү(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_төймәсе and ачкыч_символ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.җибәрү(자신.алмашу_буферы_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if ачкыч_символ in 특수글쇠: 자신.җибәрү(특수글쇠[ачкыч_символ]); return
        символ_кодлау = ачкыч_символ & 0xffffff if ачкыч_символ & 0xff000000 == 0x01000000 else ачкыч_символ
        if символ_кодлау > 0x10ffff or 0xd800 <= символ_кодлау <= 0xdfff or ачкыч_символ >= 0xff00 and ачкыч_символ < 0x1000000: return
        if CTRL and 0x40 <= символ_кодлау <= 0x7f: 자신.җибәрү(bytes([символ_кодлау & 31])); return
        if символ_кодлау < 32: return
        if 자신.한글여부 and 자신.идарә_төймәләре & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.канал_ачкыч(chr(символ_кодлау), altgr=True): return
        앞부분 = b'\x1b' if 자신.идарә_төймәләре & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=символ_кодлау<127:
            символ_мәгълүмат_4d9f8719=chr(символ_кодлау).upper() if SHIFT_төймәсе else chr(символ_кодлау)
            if 자신.한글조합기.канал_ачкыч(символ_мәгълүмат_4d9f8719): return
        자신.җибәрү(앞부분 + chr(символ_кодлау).encode('utf-8'))


class ялгау_классик:
    def __init__(자신, Процесс):
        자신.Процесс=Процесс; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Терминал=False; 자신.시작화면=False; 자신.닫힘=False

    def җибәрү(자신, мәгълүмат):
        if not мәгълүмат or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Процесс.stdin.write(мәгълүмат); 자신.Процесс.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                мәгълүмат=자신.Процесс.stdout.read(4096)
                if not мәгълүмат: break
                sys.stdout.buffer.write(мәгълүмат); sys.stdout.buffer.flush()
                끝부분=(끝부분+мәгълүмат)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Терминал=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.җибәрү(b'terminal\n')
        finally: 자신.닫힘=True

    def клиент(자신, клиент, Yul):
        сервер_VALUE=socket.socket(socket.AF_UNIX); сервер_VALUE.settimeout(10); клиент.settimeout(10)
        төймәсар_кертү=төймәсар(자신.җибәрү,lambda 한글여부:자신.җибәрү(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сервер_VALUE.connect(str(Yul))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            клиент.sendall(EXACT_VALUE(сервер_VALUE,12))
            판번호=EXACT_VALUE(клиент,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сервер_VALUE.sendall(판번호)
            элемент_COUNT=EXACT_VALUE(сервер_VALUE,1);клиент.sendall(элемент_COUNT+EXACT_VALUE(сервер_VALUE,элемент_COUNT[0]))
            Иминлек=EXACT_VALUE(клиент,1)
            if Иминлек!=b'\x01': raise ValueError('unexpected security type')
            сервер_VALUE.sendall(Иминлек)
            if 판번호==b'RFB 003.008\n':клиент.sendall(EXACT_VALUE(сервер_VALUE,4))
            сервер_VALUE.sendall(EXACT_VALUE(клиент,1))
            초기값=EXACT_VALUE(сервер_VALUE,24)
            клиент.sendall(초기값+EXACT_VALUE(сервер_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            клиент.settimeout(None);сервер_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        категория_VALUE=EXACT_VALUE(сервер_VALUE,1)[0]
                        if категория_VALUE==0:
                            머리=EXACT_VALUE(сервер_VALUE,3);кертү_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 читтәге_VALUE 포인터의 중복을 피한다.
                            яшерен_VALUE=포인터지원
                            if яшерен_VALUE:клиент.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            клиент.sendall(bytes([категория_VALUE])+머리)
                            for _ in range(кертү_COUNT):
                                사각형=EXACT_VALUE(сервер_VALUE,12);가로,Вертикаль_урнаштыру,폭,높이,кодлау_VALUE=struct.unpack('>HHHHi',사각형)
                                if кодлау_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(кодлау_VALUE))
                                клиент.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    мәгълүмат=EXACT_VALUE(сервер_VALUE,min(남음,65536));клиент.sendall(мәгълүмат);남음-=len(мәгълүмат)
                        elif категория_VALUE==1:
                            머리=EXACT_VALUE(сервер_VALUE,5);элемент_COUNT=struct.unpack('>H',머리[3:])[0]
                            клиент.sendall(bytes([категория_VALUE])+머리+EXACT_VALUE(сервер_VALUE,элемент_COUNT*6))
                        elif категория_VALUE==2:клиент.sendall(bytes([категория_VALUE]))
                        elif категория_VALUE==3:
                            머리=EXACT_VALUE(сервер_VALUE,7);элемент_COUNT=struct.unpack('>I',머리[3:])[0]
                            if элемент_COUNT>1048576:raise ValueError('server clipboard too large')
                            клиент.sendall(bytes([категория_VALUE])+머리+EXACT_VALUE(сервер_VALUE,элемент_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(категория_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:клиент.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                категория_VALUE=EXACT_VALUE(клиент,1)[0]
                if категория_VALUE==4:
                    төп_текст=EXACT_VALUE(клиент,7); төймәсар_кертү.누름값(төп_текст[0]!=0,struct.unpack('>I',төп_текст[3:])[0]); continue
                if категория_VALUE==255:
                    төп_текст=EXACT_VALUE(клиент,11)
                    if төп_текст[0]!=0: raise ValueError('unsupported QEMU input extension')
                    төймәсар_кертү.누름값(struct.unpack('>H',төп_текст[1:3])[0]!=0,struct.unpack('>I',төп_текст[3:7])[0]); continue
                if категория_VALUE==5:
                    төп_текст=EXACT_VALUE(клиент,5); 단추들,X_координатасы,세로좌표=struct.unpack('>BHH',төп_текст)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: төймәсар_кертү.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=X_координатасы<576 and 112<=세로좌표<372:
                        Эзләү_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and Эзләү_INDEX<5: 자신.җибәрү(bytes([ord('1')+Эзләү_INDEX]))
                    else: 자신.җибәрү(bytes([30,1,단추들,X_координатасы&255,X_координатасы>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if категория_VALUE==6:
                    төп_текст=EXACT_VALUE(клиент,7); озынлык_VALUE=struct.unpack('>i',төп_текст[3:])[0]
                    if abs(озынлык_VALUE)>65536: raise ValueError('clipboard too large')
                    Mäten=EXACT_VALUE(клиент,abs(озынлык_VALUE))
                    if озынлык_VALUE>=0:
                        try: төймәсар_кертү.алмашу_буферы_VALUE=Mäten.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: төймәсар_кертү.алмашу_буферы_VALUE=Mäten.decode('latin-1').encode('utf-8')
                        төймәсар_кертү.алмашу_буферы_VALUE=төймәсар_кертү.алмашу_буферы_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    сервер_VALUE.sendall(bytes([категория_VALUE])+төп_текст+Mäten); continue
                if категория_VALUE==0:
                    төп_текст=EXACT_VALUE(клиент,19)
                    if төп_текст[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=төп_текст[3]//8
                elif категория_VALUE==2:
                    төп_текст=EXACT_VALUE(клиент,3); кертү_COUNT=struct.unpack('>H',төп_текст[1:])[0]
                    if кертү_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(кертү_COUNT)+'i',EXACT_VALUE(клиент,кертү_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 килешенгәнчә_кыйммәт Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    төп_текст=struct.pack('>BHi',0,1,0)
                elif категория_VALUE in (3,150): төп_текст=EXACT_VALUE(клиент,9)
                elif категория_VALUE==248:
                    төп_текст=EXACT_VALUE(клиент,8)
                    if төп_текст[7]>64: raise ValueError('fence too large')
                    төп_текст+=EXACT_VALUE(клиент,төп_текст[7])
                elif категория_VALUE==250: төп_текст=EXACT_VALUE(клиент,3)
                elif категория_VALUE==251:
                    төп_текст=EXACT_VALUE(клиент,7)
                    if төп_текст[5]>16: raise ValueError('too many screens')
                    төп_текст+=EXACT_VALUE(клиент,төп_текст[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(категория_VALUE))
                сервер_VALUE.sendall(bytes([категория_VALUE])+төп_текст)
        except (OSError,EOFError,ValueError) as Хата:
            if str(Хата): print('VNC client:',Хата,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (клиент,сервер_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def эшләтү_классик(접속번호=5902, Челтәр=False, 파일전송접속번호=2121, 전달규칙들=(), ачыклык_VALUE=(640, 480), кунак_адрес=None, хост_адрес='127.0.0.1'):
    with ExitStack() as Ресурслар, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Челтәр_күпер_кертү = None
        if Челтәр:
            from Челтәр_күпер import Челтәр_күпер
            Челтәр_күпер_кертү = Ресурслар.enter_context(Челтәр_күпер(파일전송접속번호, 전달규칙들, кунак_адрес=кунак_адрес, хост_адрес=хост_адрес))
        Yul=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Челтәр_күпер_кертү and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and хост==원격화면접속번호 for 통신규약,хост,_ in Челтәр_күпер_кертү.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Процесс=subprocess.Popen(команда(ачыклык_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Yul)]+(Челтәр_күпер_кертү.전달인수() if Челтәр_күпер_кертү else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            күпер=ялгау_классик(Процесс); укучы=threading.Thread(target=күпер.직렬입출력,daemon=True); укучы.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Челтәр_күпер_кертү: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(хост_адрес,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Процесс.poll() is None:
                    try: клиент,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): клиент.close(); continue
                    if not Yul.exists(): клиент.close(); continue
                    처리작업=threading.Thread(target=күпер.клиент,args=(клиент,Yul),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                күпер.닫힘=True
                if Челтәр_күпер_кертү: Челтәр_күпер_кертү.туктатып_тору_вакыйга.set()
                if Процесс.poll() is None:
                    Процесс.terminate()
                    try: Процесс.wait(timeout=5)
                    except subprocess.TimeoutExpired: Процесс.kill(); Процесс.wait()
                укучы.join(timeout=2); Процесс.stdin.close(); Процесс.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Челтәр_күпер_кертү and Челтәр_күпер_кертү.Хата: raise RuntimeError('network bridge: '+Челтәр_күпер_кертү.Хата)
            return 0 if 가로채기됨 else Процесс.returncode


if __name__=='__main__':
    from үтәргә_команда import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    аргумент_МАССИВ=인수해석기.parse_args()
    if аргумент_МАССИВ.forward and not аргумент_МАССИВ.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(эшләтү_классик(аргумент_МАССИВ.port,Челтәр=аргумент_МАССИВ.network,파일전송접속번호=аргумент_МАССИВ.ftp_port,전달규칙들=аргумент_МАССИВ.forward,ачыклык_VALUE=аргумент_МАССИВ.resolution))
