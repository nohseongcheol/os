#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Клуч_VALUE 입력은 자체 јадро_VALUE UART로 전달한다. localhost 전용, 단일 контрола_VALUE 클라이언트.
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
from Изврши_наредба import Команда
from local_input import create


def EXACT_VALUE(소켓, Големина):
    податоци = bytearray()
    while len(податоци) < Големина:
        조각 = 소켓.recv(Големина - len(податоци))
        if not 조각: raise EOFError()
        податоци.extend(조각)
    return bytes(податоци)


class тастатура:
    def __init__(자신, испрати, 입력방식알림=None):
        자신.바이트전송 = испрати; 자신.копче_за_модификување = set(); 자신.склад_VALUE = b''
        자신.한글조합기 = create(испрати, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Клуч = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def испрати(자신, податоци):
        자신.한글조합기.조합확정()
        자신.바이트전송(податоци)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Клуч_симбол):
        if Клуч_симбол in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.копче_за_модификување.add(Клуч_симбол)
            else: 자신.копче_за_модификување.discard(Клуч_симбол)
            return
        if not 누르는중:
            자신.SWITCH_Клуч.discard(Клуч_симбол)
            return
        CTRL = bool(자신.копче_за_модификување & {0xffe3, 0xffe4})
        копче_SHIFT = bool(자신.копче_за_модификување & {0xffe1, 0xffe2})
        if CTRL and копче_SHIFT and Клуч_симбол in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Клуч_симбол in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.испрати(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Клуч_симбол==0xff1b: 자신.유니코드입력=None
            elif Клуч_симбол==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Клуч_симбол<128 and chr(Клуч_симбол) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Клуч_симбол)
            return
        if Клуч_симбол in (0xff31,0xffc6) or Клуч_симбол==32 and копче_SHIFT and not CTRL:
            if Клуч_симбол not in 자신.SWITCH_Клуч: 자신.SWITCH_MODE()
            자신.SWITCH_Клуч.add(Клуч_симбол)
            return
        if Клуч_симбол==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and копче_SHIFT and Клуч_симбол in (ord('t'),ord('T')):
            자신.испрати(bytes([30,2,1,0,0,0,0])); return
        if Клуч_симбол==0xffc3: 자신.испрати(bytes([30,2,2,0,0,0,0])); return
        if Клуч_симбол==0xffc9: 자신.испрати(bytes([30,2,3,0,0,0,0])); return
        if CTRL and копче_SHIFT and Клуч_симбол in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.испрати(자신.склад_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Клуч_симбол in 특수글쇠: 자신.испрати(특수글쇠[Клуч_симбол]); return
        знак_кодирање = Клуч_симбол & 0xffffff if Клуч_симбол & 0xff000000 == 0x01000000 else Клуч_симбол
        if знак_кодирање > 0x10ffff or 0xd800 <= знак_кодирање <= 0xdfff or Клуч_симбол >= 0xff00 and Клуч_симбол < 0x1000000: return
        if CTRL and 0x40 <= знак_кодирање <= 0x7f: 자신.испрати(bytes([знак_кодирање & 31])); return
        if знак_кодирање < 32: return
        if 자신.한글여부 and 자신.копче_за_модификување & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.навестување_Клуч(chr(знак_кодирање), altgr=True): return
        앞부분 = b'\x1b' if 자신.копче_за_модификување & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=знак_кодирање<127:
            знак_податоци=chr(знак_кодирање).upper() if копче_SHIFT else chr(знак_кодирање)
            if 자신.한글조합기.навестување_Клуч(знак_податоци): return
        자신.испрати(앞부분 + chr(знак_кодирање).encode('utf-8'))


class ПОВРЗИ_десктоп:
    def __init__(자신, Процес):
        자신.Процес=Процес; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Терминал=False; 자신.시작화면=False; 자신.닫힘=False

    def испрати(자신, податоци):
        if not податоци or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Процес.stdin.write(податоци); 자신.Процес.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                податоци=자신.Процес.stdout.read(4096)
                if not податоци: break
                sys.stdout.buffer.write(податоци); sys.stdout.buffer.flush()
                끝부분=(끝부분+податоци)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Терминал=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.испрати(b'terminal\n')
        finally: 자신.닫힘=True

    def клиент(자신, клиент, ПАТЕКА):
        сервер_VALUE=socket.socket(socket.AF_UNIX); сервер_VALUE.settimeout(10); клиент.settimeout(10)
        тастатура_внес=тастатура(자신.испрати,lambda 한글여부:자신.испрати(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сервер_VALUE.connect(str(ПАТЕКА))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            клиент.sendall(EXACT_VALUE(сервер_VALUE,12))
            број_на_верзија=EXACT_VALUE(клиент,12)
            if број_на_верзија not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сервер_VALUE.sendall(број_на_верзија)
            ставка_COUNT=EXACT_VALUE(сервер_VALUE,1);клиент.sendall(ставка_COUNT+EXACT_VALUE(сервер_VALUE,ставка_COUNT[0]))
            Безбедност=EXACT_VALUE(клиент,1)
            if Безбедност!=b'\x01': raise ValueError('unexpected security type')
            сервер_VALUE.sendall(Безбедност)
            if број_на_верзија==b'RFB 003.008\n':клиент.sendall(EXACT_VALUE(сервер_VALUE,4))
            сервер_VALUE.sendall(EXACT_VALUE(клиент,1))
            초기값=EXACT_VALUE(сервер_VALUE,24)
            клиент.sendall(초기값+EXACT_VALUE(сервер_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            клиент.settimeout(None);сервер_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        област_VALUE=EXACT_VALUE(сервер_VALUE,1)[0]
                        if област_VALUE==0:
                            머리=EXACT_VALUE(сервер_VALUE,3);внес_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 далечинскo_VALUE 포인터의 중복을 피한다.
                            скриен_VALUE=포인터지원
                            if скриен_VALUE:клиент.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            клиент.sendall(bytes([област_VALUE])+머리)
                            for _ in range(внес_COUNT):
                                사각형=EXACT_VALUE(сервер_VALUE,12);가로,вертикала_позиционирање,폭,높이,кодирање_VALUE=struct.unpack('>HHHHi',사각형)
                                if кодирање_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(кодирање_VALUE))
                                клиент.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    податоци=EXACT_VALUE(сервер_VALUE,min(남음,65536));клиент.sendall(податоци);남음-=len(податоци)
                        elif област_VALUE==1:
                            머리=EXACT_VALUE(сервер_VALUE,5);ставка_COUNT=struct.unpack('>H',머리[3:])[0]
                            клиент.sendall(bytes([област_VALUE])+머리+EXACT_VALUE(сервер_VALUE,ставка_COUNT*6))
                        elif област_VALUE==2:клиент.sendall(bytes([област_VALUE]))
                        elif област_VALUE==3:
                            머리=EXACT_VALUE(сервер_VALUE,7);ставка_COUNT=struct.unpack('>I',머리[3:])[0]
                            if ставка_COUNT>1048576:raise ValueError('server clipboard too large')
                            клиент.sendall(bytes([област_VALUE])+머리+EXACT_VALUE(сервер_VALUE,ставка_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(област_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:клиент.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                област_VALUE=EXACT_VALUE(клиент,1)[0]
                if област_VALUE==4:
                    основен_текст=EXACT_VALUE(клиент,7); тастатура_внес.누름값(основен_текст[0]!=0,struct.unpack('>I',основен_текст[3:])[0]); continue
                if област_VALUE==255:
                    основен_текст=EXACT_VALUE(клиент,11)
                    if основен_текст[0]!=0: raise ValueError('unsupported QEMU input extension')
                    тастатура_внес.누름값(struct.unpack('>H',основен_текст[1:3])[0]!=0,struct.unpack('>I',основен_текст[3:7])[0]); continue
                if област_VALUE==5:
                    основен_текст=EXACT_VALUE(клиент,5); 단추들,координата_х,세로좌표=struct.unpack('>BHH',основен_текст)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: тастатура_внес.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=координата_х<576 and 112<=세로좌표<372:
                        LOOKUP_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and LOOKUP_INDEX<5: 자신.испрати(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.испрати(bytes([30,1,단추들,координата_х&255,координата_х>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if област_VALUE==6:
                    основен_текст=EXACT_VALUE(клиент,7); должина_VALUE=struct.unpack('>i',основен_текст[3:])[0]
                    if abs(должина_VALUE)>65536: raise ValueError('clipboard too large')
                    Текст=EXACT_VALUE(клиент,abs(должина_VALUE))
                    if должина_VALUE>=0:
                        try: тастатура_внес.склад_VALUE=Текст.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: тастатура_внес.склад_VALUE=Текст.decode('latin-1').encode('utf-8')
                        тастатура_внес.склад_VALUE=тастатура_внес.склад_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    сервер_VALUE.sendall(bytes([област_VALUE])+основен_текст+Текст); continue
                if област_VALUE==0:
                    основен_текст=EXACT_VALUE(клиент,19)
                    if основен_текст[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=основен_текст[3]//8
                elif област_VALUE==2:
                    основен_текст=EXACT_VALUE(клиент,3); внес_COUNT=struct.unpack('>H',основен_текст[1:])[0]
                    if внес_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(внес_COUNT)+'i',EXACT_VALUE(клиент,внес_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 стандардна_вредност Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    основен_текст=struct.pack('>BHi',0,1,0)
                elif област_VALUE in (3,150): основен_текст=EXACT_VALUE(клиент,9)
                elif област_VALUE==248:
                    основен_текст=EXACT_VALUE(клиент,8)
                    if основен_текст[7]>64: raise ValueError('fence too large')
                    основен_текст+=EXACT_VALUE(клиент,основен_текст[7])
                elif област_VALUE==250: основен_текст=EXACT_VALUE(клиент,3)
                elif област_VALUE==251:
                    основен_текст=EXACT_VALUE(клиент,7)
                    if основен_текст[5]>16: raise ValueError('too many screens')
                    основен_текст+=EXACT_VALUE(клиент,основен_текст[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(област_VALUE))
                сервер_VALUE.sendall(bytes([област_VALUE])+основен_текст)
        except (OSError,EOFError,ValueError) as ГРЕШКА:
            if str(ГРЕШКА): print('VNC client:',ГРЕШКА,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (клиент,сервер_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def изврши_десктоп(број_на_порта=5902, Мрежа=False, датотека_пренос_број_на_порта=2121, 전달규칙들=(), резолуција_VALUE=(640, 480), гостин_адреса=None, вдоми_адреса='127.0.0.1'):
    with ExitStack() as Ресурси, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Мрежа_мост_внес = None
        if Мрежа:
            from Мрежа_мост import Мрежа_мост
            Мрежа_мост_внес = Ресурси.enter_context(Мрежа_мост(датотека_пренос_број_на_порта, 전달규칙들, гостин_адреса=гостин_адреса, вдоми_адреса=вдоми_адреса))
        ПАТЕКА=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',број_на_порта)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Мрежа_мост_внес and (원격화면접속번호==датотека_пренос_број_на_порта or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and вдоми==원격화면접속번호 for 통신규약,вдоми,_ in Мрежа_мост_внес.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Процес=subprocess.Popen(Команда(резолуција_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ПАТЕКА)]+(Мрежа_мост_внес.전달인수() if Мрежа_мост_внес else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            мост=ПОВРЗИ_десктоп(Процес); Читач=threading.Thread(target=мост.직렬입출력,daemon=True); Читач.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Мрежа_мост_внес: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(вдоми_адреса,датотека_пренос_број_на_порта),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Процес.poll() is None:
                    try: клиент,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): клиент.close(); continue
                    if not ПАТЕКА.exists(): клиент.close(); continue
                    처리작업=threading.Thread(target=мост.клиент,args=(клиент,ПАТЕКА),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                мост.닫힘=True
                if Мрежа_мост_внес: Мрежа_мост_внес.пауза_настан.set()
                if Процес.poll() is None:
                    Процес.terminate()
                    try: Процес.wait(timeout=5)
                    except subprocess.TimeoutExpired: Процес.kill(); Процес.wait()
                Читач.join(timeout=2); Процес.stdin.close(); Процес.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Мрежа_мост_внес and Мрежа_мост_внес.ГРЕШКА: raise RuntimeError('network bridge: '+Мрежа_мост_внес.ГРЕШКА)
            return 0 if 가로채기됨 else Процес.returncode


if __name__=='__main__':
    from Изврши_наредба import 해상도읽기
    анализатор=argparse.ArgumentParser(description=__doc__); анализатор.add_argument('--port',type=int,default=5902)
    анализатор.add_argument('--resolution',type=해상도읽기,default=(640,480))
    анализатор.add_argument('--network',action='store_true'); анализатор.add_argument('--ftp-port',type=int,default=2121)
    анализатор.add_argument('--forward',action='append',default=[])
    аргумент_низа=анализатор.parse_args()
    if аргумент_низа.forward and not аргумент_низа.network: анализатор.error('--forward requires --network')
    raise SystemExit(изврши_десктоп(аргумент_низа.port,Мрежа=аргумент_низа.network,датотека_пренос_број_на_порта=аргумент_низа.ftp_port,전달규칙들=аргумент_низа.forward,резолуција_VALUE=аргумент_низа.resolution))
