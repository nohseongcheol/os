#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Кључ_вриједност 입력은 자체 језгро_вриједност UART로 전달한다. localhost 전용, 단일 контрола_вриједност 클라이언트.
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
from Изврши_команда import Наредба
from local_input import create


def 정확한값(소켓, Величина):
    подаци = bytearray()
    while len(подаци) < Величина:
        조각 = 소켓.recv(Величина - len(подаци))
        if not 조각: raise EOFError()
        подаци.extend(조각)
    return bytes(подаци)


class тастатура:
    def __init__(자신, послати, 입력방식알림=None):
        자신.바이트전송 = послати; 자신.модификаторски_тастер = set(); 자신.међуспремник_вриједност = b''
        자신.한글조합기 = create(послати, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.пребацити_Кључ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def послати(자신, подаци):
        자신.한글조합기.조합확정()
        자신.바이트전송(подаци)

    def пребацити_мод(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Кључ_симбол):
        if Кључ_симбол in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.модификаторски_тастер.add(Кључ_симбол)
            else: 자신.модификаторски_тастер.discard(Кључ_симбол)
            return
        if not 누르는중:
            자신.пребацити_Кључ.discard(Кључ_симбол)
            return
        тастер_CTRL = bool(자신.модификаторски_тастер & {0xffe3, 0xffe4})
        тастер_SHIFT = bool(자신.модификаторски_тастер & {0xffe1, 0xffe2})
        if тастер_CTRL and тастер_SHIFT and Кључ_симбол in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Кључ_симбол in (32,0xff0d):
                try:
                    вриједност=int(자신.유니코드입력,16)
                    if 32<=вриједност<=0x10ffff and not 0xd800<=вриједност<=0xdfff: 자신.послати(chr(вриједност).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Кључ_симбол==0xff1b: 자신.유니코드입력=None
            elif Кључ_симбол==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Кључ_симбол<128 and chr(Кључ_симбол) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Кључ_симбол)
            return
        if Кључ_симбол in (0xff31,0xffc6) or Кључ_симбол==32 and тастер_SHIFT and not тастер_CTRL:
            if Кључ_симбол not in 자신.пребацити_Кључ: 자신.пребацити_мод()
            자신.пребацити_Кључ.add(Кључ_симбол)
            return
        if Кључ_симбол==0xff08 and 자신.한글여부 and not тастер_CTRL and 자신.한글조합기.앞글자지우기(): return
        if тастер_CTRL and тастер_SHIFT and Кључ_симбол in (ord('t'),ord('T')):
            자신.послати(bytes([30,2,1,0,0,0,0])); return
        if Кључ_симбол==0xffc3: 자신.послати(bytes([30,2,2,0,0,0,0])); return
        if Кључ_симбол==0xffc9: 자신.послати(bytes([30,2,3,0,0,0,0])); return
        if тастер_CTRL and тастер_SHIFT and Кључ_симбол in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.послати(자신.међуспремник_вриједност); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Кључ_симбол in 특수글쇠: 자신.послати(특수글쇠[Кључ_симбол]); return
        знак_кодирање = Кључ_симбол & 0xffffff if Кључ_симбол & 0xff000000 == 0x01000000 else Кључ_симбол
        if знак_кодирање > 0x10ffff or 0xd800 <= знак_кодирање <= 0xdfff or Кључ_симбол >= 0xff00 and Кључ_симбол < 0x1000000: return
        if тастер_CTRL and 0x40 <= знак_кодирање <= 0x7f: 자신.послати(bytes([знак_кодирање & 31])); return
        if знак_кодирање < 32: return
        if 자신.한글여부 and 자신.модификаторски_тастер & {0xffea,0xfe03,0xff7e} and not тастер_CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.фид_Кључ(chr(знак_кодирање), altgr=True): return
        앞부분 = b'\x1b' if 자신.модификаторски_тастер & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not тастер_CTRL and not 앞부분 and 32<=знак_кодирање<127:
            знак_подаци=chr(знак_кодирање).upper() if тастер_SHIFT else chr(знак_кодирање)
            if 자신.한글조합기.фид_Кључ(знак_подаци): return
        자신.послати(앞부분 + chr(знак_кодирање).encode('utf-8'))


class ПОВЕЖИ_десктоп:
    def __init__(자신, Процес):
        자신.Процес=Процес; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Терминал=False; 자신.시작화면=False; 자신.닫힘=False

    def послати(자신, подаци):
        if not подаци or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Процес.stdin.write(подаци); 자신.Процес.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                подаци=자신.Процес.stdout.read(4096)
                if not подаци: break
                sys.stdout.buffer.write(подаци); sys.stdout.buffer.flush()
                끝부분=(끝부분+подаци)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Терминал=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.послати(b'terminal\n')
        finally: 자신.닫힘=True

    def клијент(자신, клијент, ПУТАЊА):
        сервер_вриједност=socket.socket(socket.AF_UNIX); сервер_вриједност.settimeout(10); клијент.settimeout(10)
        тастатура_унос=тастатура(자신.послати,lambda 한글여부:자신.послати(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сервер_вриједност.connect(str(ПУТАЊА))
            # 초기 협상은 순서대로 끝낸다. 이후 Излаз 가닥만 클라이언트에 쓴다.
            клијент.sendall(정확한값(сервер_вриједност,12))
            판번호=정확한값(клијент,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сервер_вриједност.sendall(판번호)
            개수=정확한값(сервер_вриједност,1);клијент.sendall(개수+정확한값(сервер_вриједност,개수[0]))
            Безбедност=정확한값(клијент,1)
            if Безбедност!=b'\x01': raise ValueError('unexpected security type')
            сервер_вриједност.sendall(Безбедност)
            if 판번호==b'RFB 003.008\n':клијент.sendall(정확한값(сервер_вриједност,4))
            сервер_вриједност.sendall(정확한값(клијент,1))
            초기값=정확한값(сервер_вриједност,24)
            клијент.sendall(초기값+정확한값(сервер_вриједност,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            клијент.settimeout(None);сервер_вриједност.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        област_вриједност=정확한값(сервер_вриједност,1)[0]
                        if област_вриједност==0:
                            머리=정확한값(сервер_вриједност,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 удаљен_вриједност 포인터의 중복을 피한다.
                            Скривено_вриједност=포인터지원
                            if Скривено_вриједност:клијент.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            клијент.sendall(bytes([област_вриједност])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(сервер_вриједност,12);가로,вертикала_позиција,폭,높이,кодирање_вриједност=struct.unpack('>HHHHi',사각형)
                                if кодирање_вриједност!=0:raise ValueError('unexpected framebuffer encoding: '+str(кодирање_вриједност))
                                клијент.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    подаци=정확한값(сервер_вриједност,min(남음,65536));клијент.sendall(подаци);남음-=len(подаци)
                        elif област_вриједност==1:
                            머리=정확한값(сервер_вриједност,5);개수=struct.unpack('>H',머리[3:])[0]
                            клијент.sendall(bytes([област_вриједност])+머리+정확한값(сервер_вриједност,개수*6))
                        elif област_вриједност==2:клијент.sendall(bytes([област_вриједност]))
                        elif област_вриједност==3:
                            머리=정확한값(сервер_вриједност,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            клијент.sendall(bytes([област_вриједност])+머리+정확한값(сервер_вриједност,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(област_вриједност))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:клијент.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                област_вриједност=정확한값(клијент,1)[0]
                if област_вриједност==4:
                    тело_текста=정확한값(клијент,7); тастатура_унос.누름값(тело_текста[0]!=0,struct.unpack('>I',тело_текста[3:])[0]); continue
                if област_вриједност==255:
                    тело_текста=정확한값(клијент,11)
                    if тело_текста[0]!=0: raise ValueError('unsupported QEMU input extension')
                    тастатура_унос.누름값(struct.unpack('>H',тело_текста[1:3])[0]!=0,struct.unpack('>I',тело_текста[3:7])[0]); continue
                if област_вриједност==5:
                    тело_текста=정확한값(клијент,5); 단추들,x_координата,дугме_Y_координата=struct.unpack('>BHH',тело_текста)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: тастатура_унос.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_координата<576 and 112<=дугме_Y_координата<372:
                        Претрага_индекс=(дугме_Y_координата-112)//52
                        if (дугме_Y_координата-112)%52<40 and Претрага_индекс<5: 자신.послати(bytes([ord('1')+Претрага_индекс]))
                    else: 자신.послати(bytes([30,1,단추들,x_координата&255,x_координата>>8,дугме_Y_координата&255,дугме_Y_координата>>8]))
                    continue
                if област_вриједност==6:
                    тело_текста=정확한값(клијент,7); дужина_вриједност=struct.unpack('>i',тело_текста[3:])[0]
                    if abs(дужина_вриједност)>65536: raise ValueError('clipboard too large')
                    Текст=정확한값(клијент,abs(дужина_вриједност))
                    if дужина_вриједност>=0:
                        try: тастатура_унос.међуспремник_вриједност=Текст.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: тастатура_унос.међуспремник_вриједност=Текст.decode('latin-1').encode('utf-8')
                        тастатура_унос.међуспремник_вриједност=тастатура_унос.међуспремник_вриједност[:65536].decode('utf-8','ignore').encode('utf-8')
                    сервер_вриједност.sendall(bytes([област_вриједност])+тело_текста+Текст); continue
                if област_вриједност==0:
                    тело_текста=정확한값(клијент,19)
                    if тело_текста[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=тело_текста[3]//8
                elif област_вриједност==2:
                    тело_текста=정확한값(клијент,3); 항목수=struct.unpack('>H',тело_текста[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(клијент,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 задана_вриједност Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    тело_текста=struct.pack('>BHi',0,1,0)
                elif област_вриједност in (3,150): тело_текста=정확한값(клијент,9)
                elif област_вриједност==248:
                    тело_текста=정확한값(клијент,8)
                    if тело_текста[7]>64: raise ValueError('fence too large')
                    тело_текста+=정확한값(клијент,тело_текста[7])
                elif област_вриједност==250: тело_текста=정확한값(клијент,3)
                elif област_вриједност==251:
                    тело_текста=정확한값(клијент,7)
                    if тело_текста[5]>16: raise ValueError('too many screens')
                    тело_текста+=정확한값(клијент,тело_текста[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(област_вриједност))
                сервер_вриједност.sendall(bytes([област_вриједност])+тело_текста)
        except (OSError,EOFError,ValueError) as ГРЕШКА:
            if str(ГРЕШКА): print('VNC client:',ГРЕШКА,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (клијент,сервер_вриједност):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def низ_десктоп(број_порта=5902, Мрежа=False, фајл_пренос_број_порта=2121, 전달규칙들=(), резолуција_вриједност=(640, 480), гост_адреса=None, хост_адреса='127.0.0.1'):
    with ExitStack() as Извори, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Мрежа_мост_унос = None
        if Мрежа:
            from Мрежа_мост import Мрежа_мост
            Мрежа_мост_унос = Извори.enter_context(Мрежа_мост(фајл_пренос_број_порта, 전달규칙들, гост_адреса=гост_адреса, хост_адреса=хост_адреса))
        ПУТАЊА=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',број_порта)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Мрежа_мост_унос and (원격화면접속번호==фајл_пренос_број_порта or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and хост==원격화면접속번호 for 통신규약,хост,_ in Мрежа_мост_унос.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Процес=subprocess.Popen(Наредба(резолуција_вриједност)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ПУТАЊА)]+(Мрежа_мост_унос.전달인수() if Мрежа_мост_унос else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            мост=ПОВЕЖИ_десктоп(Процес); Читач=threading.Thread(target=мост.직렬입출력,daemon=True); Читач.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Мрежа_мост_унос: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(хост_адреса,фајл_пренос_број_порта),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            обрада_задатак=None; 가로채기됨=False
            try:
                while Процес.poll() is None:
                    try: клијент,_=수신창구.accept()
                    except socket.timeout: continue
                    if обрада_задатак is not None and обрада_задатак.is_alive(): клијент.close(); continue
                    if not ПУТАЊА.exists(): клијент.close(); continue
                    обрада_задатак=threading.Thread(target=мост.клијент,args=(клијент,ПУТАЊА),daemon=True); обрада_задатак.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                мост.닫힘=True
                if Мрежа_мост_унос: Мрежа_мост_унос.пауза_догађај.set()
                if Процес.poll() is None:
                    Процес.terminate()
                    try: Процес.wait(timeout=5)
                    except subprocess.TimeoutExpired: Процес.kill(); Процес.wait()
                Читач.join(timeout=2); Процес.stdin.close(); Процес.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Мрежа_мост_унос and Мрежа_мост_унос.ГРЕШКА: raise RuntimeError('network bridge: '+Мрежа_мост_унос.ГРЕШКА)
            return 0 if 가로채기됨 else Процес.returncode


if __name__=='__main__':
    from Изврши_команда import 해상도읽기
    анализатор=argparse.ArgumentParser(description=__doc__); анализатор.add_argument('--port',type=int,default=5902)
    анализатор.add_argument('--resolution',type=해상도읽기,default=(640,480))
    анализатор.add_argument('--network',action='store_true'); анализатор.add_argument('--ftp-port',type=int,default=2121)
    анализатор.add_argument('--forward',action='append',default=[])
    аргумент_низ=анализатор.parse_args()
    if аргумент_низ.forward and not аргумент_низ.network: анализатор.error('--forward requires --network')
    raise SystemExit(низ_десктоп(аргумент_низ.port,Мрежа=аргумент_низ.network,фајл_пренос_број_порта=аргумент_низ.ftp_port,전달규칙들=аргумент_низ.forward,резолуција_вриједност=аргумент_низ.resolution))
