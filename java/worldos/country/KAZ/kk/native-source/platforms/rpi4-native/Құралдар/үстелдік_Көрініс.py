#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Кілт_мән 입력은 자체 ядро_мән UART로 전달한다. localhost 전용, 단일 Басқару_мән 클라이언트.
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
from орындау_пәрмен import Команда
from local_input import create


def 정확한값(소켓, Өлшемі):
    деректер = bytearray()
    while len(деректер) < Өлшемі:
        조각 = 소켓.recv(Өлшемі - len(деректер))
        if not 조각: raise EOFError()
        деректер.extend(조각)
    return bytes(деректер)


class пернетақта:
    def __init__(자신, жіберу, 입력방식알림=None):
        자신.바이트전송 = жіберу; 자신.өзгерткіш_пернеcі = set(); 자신.аралық_сақтағыш_мән = b''
        자신.한글조합기 = create(жіберу, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ауысу_Кілт = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def жіберу(자신, деректер):
        자신.한글조합기.조합확정()
        자신.바이트전송(деректер)

    def ауысу_режим(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Кілт_символ):
        if Кілт_символ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.өзгерткіш_пернеcі.add(Кілт_символ)
            else: 자신.өзгерткіш_пернеcі.discard(Кілт_символ)
            return
        if not 누르는중:
            자신.ауысу_Кілт.discard(Кілт_символ)
            return
        CTRL_пернесі = bool(자신.өзгерткіш_пернеcі & {0xffe3, 0xffe4})
        SHIFT_пернесі = bool(자신.өзгерткіш_пернеcі & {0xffe1, 0xffe2})
        if CTRL_пернесі and SHIFT_пернесі and Кілт_символ in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Кілт_символ in (32,0xff0d):
                try:
                    мән=int(자신.유니코드입력,16)
                    if 32<=мән<=0x10ffff and not 0xd800<=мән<=0xdfff: 자신.жіберу(chr(мән).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Кілт_символ==0xff1b: 자신.유니코드입력=None
            elif Кілт_символ==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Кілт_символ<128 and chr(Кілт_символ) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Кілт_символ)
            return
        if Кілт_символ in (0xff31,0xffc6) or Кілт_символ==32 and SHIFT_пернесі and not CTRL_пернесі:
            if Кілт_символ not in 자신.ауысу_Кілт: 자신.ауысу_режим()
            자신.ауысу_Кілт.add(Кілт_символ)
            return
        if Кілт_символ==0xff08 and 자신.한글여부 and not CTRL_пернесі and 자신.한글조합기.앞글자지우기(): return
        if CTRL_пернесі and SHIFT_пернесі and Кілт_символ in (ord('t'),ord('T')):
            자신.жіберу(bytes([30,2,1,0,0,0,0])); return
        if Кілт_символ==0xffc3: 자신.жіберу(bytes([30,2,2,0,0,0,0])); return
        if Кілт_символ==0xffc9: 자신.жіберу(bytes([30,2,3,0,0,0,0])); return
        if CTRL_пернесі and SHIFT_пернесі and Кілт_символ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.жіберу(자신.аралық_сақтағыш_мән); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Кілт_символ in 특수글쇠: 자신.жіберу(특수글쇠[Кілт_символ]); return
        символдарды_кодтау = Кілт_символ & 0xffffff if Кілт_символ & 0xff000000 == 0x01000000 else Кілт_символ
        if символдарды_кодтау > 0x10ffff or 0xd800 <= символдарды_кодтау <= 0xdfff or Кілт_символ >= 0xff00 and Кілт_символ < 0x1000000: return
        if CTRL_пернесі and 0x40 <= символдарды_кодтау <= 0x7f: 자신.жіберу(bytes([символдарды_кодтау & 31])); return
        if символдарды_кодтау < 32: return
        if 자신.한글여부 and 자신.өзгерткіш_пернеcі & {0xffea,0xfe03,0xff7e} and not CTRL_пернесі and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.арна_Кілт(chr(символдарды_кодтау), altgr=True): return
        앞부분 = b'\x1b' if 자신.өзгерткіш_пернеcі & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_пернесі and not 앞부분 and 32<=символдарды_кодтау<127:
            символдық_деректер=chr(символдарды_кодтау).upper() if SHIFT_пернесі else chr(символдарды_кодтау)
            if 자신.한글조합기.арна_Кілт(символдық_деректер): return
        자신.жіберу(앞부분 + chr(символдарды_кодтау).encode('utf-8'))


class қосу_үстелдік:
    def __init__(자신, Үрдіс):
        자신.Үрдіс=Үрдіс; 자신.блоктау_мән=threading.Lock(); 자신.준비완료=False; 자신.Терминал=False; 자신.시작화면=False; 자신.닫힘=False

    def жіберу(자신, деректер):
        if not деректер or 자신.닫힘: return
        with 자신.блоктау_мән:
            try: 자신.Үрдіс.stdin.write(деректер); 자신.Үрдіс.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                деректер=자신.Үрдіс.stdout.read(4096)
                if not деректер: break
                sys.stdout.buffer.write(деректер); sys.stdout.buffer.flush()
                끝부분=(끝부분+деректер)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Терминал=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.жіберу(b'terminal\n')
        finally: 자신.닫힘=True

    def клиент(자신, клиент, Жол_2):
        сервер_мән=socket.socket(socket.AF_UNIX); сервер_мән.settimeout(10); клиент.settimeout(10)
        пернетақта_енгізу=пернетақта(자신.жіберу,lambda 한글여부:자신.жіберу(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сервер_мән.connect(str(Жол_2))
            # бастапқы_күй 협상은 순서대로 끝낸다. 이후 Шығысы 가닥만 클라이언트에 쓴다.
            клиент.sendall(정확한값(сервер_мән,12))
            Нұсқа_нөмірі=정확한값(клиент,12)
            if Нұсқа_нөмірі not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сервер_мән.sendall(Нұсқа_нөмірі)
            개수=정확한값(сервер_мән,1);клиент.sendall(개수+정확한값(сервер_мән,개수[0]))
            Қауіпсіздік=정확한값(клиент,1)
            if Қауіпсіздік!=b'\x01': raise ValueError('unexpected security type')
            сервер_мән.sendall(Қауіпсіздік)
            if Нұсқа_нөмірі==b'RFB 003.008\n':клиент.sendall(정확한값(сервер_мән,4))
            сервер_мән.sendall(정확한값(клиент,1))
            초기값=정확한값(сервер_мән,24)
            клиент.sendall(초기값+정확한값(сервер_мән,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            клиент.settimeout(None);сервер_мән.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        Санат_мән=정확한값(сервер_мән,1)[0]
                        if Санат_мән==0:
                            머리=정확한값(сервер_мән,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 원격 포인터의 중복을 피한다.
                            Жасырын_мән=포인터지원
                            if Жасырын_мән:клиент.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            клиент.sendall(bytes([Санат_мән])+머리)
                            for _ in range(항목수):
                                тік_төртбұрыш=정확한값(сервер_мән,12);가로,Тік_лауазым,폭,높이,кодтау_мән=struct.unpack('>HHHHi',тік_төртбұрыш)
                                if кодтау_мән!=0:raise ValueError('unexpected framebuffer encoding: '+str(кодтау_мән))
                                клиент.sendall(тік_төртбұрыш)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    деректер=정확한값(сервер_мән,min(남음,65536));клиент.sendall(деректер);남음-=len(деректер)
                        elif Санат_мән==1:
                            머리=정확한값(сервер_мән,5);개수=struct.unpack('>H',머리[3:])[0]
                            клиент.sendall(bytes([Санат_мән])+머리+정확한값(сервер_мән,개수*6))
                        elif Санат_мән==2:клиент.sendall(bytes([Санат_мән]))
                        elif Санат_мән==3:
                            머리=정확한값(сервер_мән,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            клиент.sendall(bytes([Санат_мән])+머리+정확한값(сервер_мән,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(Санат_мән))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:клиент.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                Санат_мән=정확한값(клиент,1)[0]
                if Санат_мән==4:
                    негізгі_мәтін=정확한값(клиент,7); пернетақта_енгізу.누름값(негізгі_мәтін[0]!=0,struct.unpack('>I',негізгі_мәтін[3:])[0]); continue
                if Санат_мән==255:
                    негізгі_мәтін=정확한값(клиент,11)
                    if негізгі_мәтін[0]!=0: raise ValueError('unsupported QEMU input extension')
                    пернетақта_енгізу.누름값(struct.unpack('>H',негізгі_мәтін[1:3])[0]!=0,struct.unpack('>I',негізгі_мәтін[3:7])[0]); continue
                if Санат_мән==5:
                    негізгі_мәтін=정확한값(клиент,5); 단추들,x_координатасы,Y_түймешігі_координата=struct.unpack('>BHH',негізгі_мәтін)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: пернетақта_енгізу.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_координатасы<576 and 112<=Y_түймешігі_координата<372:
                        Іздеу_индекс=(Y_түймешігі_координата-112)//52
                        if (Y_түймешігі_координата-112)%52<40 and Іздеу_индекс<5: 자신.жіберу(bytes([ord('1')+Іздеу_индекс]))
                    else: 자신.жіберу(bytes([30,1,단추들,x_координатасы&255,x_координатасы>>8,Y_түймешігі_координата&255,Y_түймешігі_координата>>8]))
                    continue
                if Санат_мән==6:
                    негізгі_мәтін=정확한값(клиент,7); ұзындық_мән=struct.unpack('>i',негізгі_мәтін[3:])[0]
                    if abs(ұзындық_мән)>65536: raise ValueError('clipboard too large')
                    Мәтін=정확한값(клиент,abs(ұзындық_мән))
                    if ұзындық_мән>=0:
                        try: пернетақта_енгізу.аралық_сақтағыш_мән=Мәтін.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: пернетақта_енгізу.аралық_сақтағыш_мән=Мәтін.decode('latin-1').encode('utf-8')
                        пернетақта_енгізу.аралық_сақтағыш_мән=пернетақта_енгізу.аралық_сақтағыш_мән[:65536].decode('utf-8','ignore').encode('utf-8')
                    сервер_мән.sendall(bytes([Санат_мән])+негізгі_мәтін+Мәтін); continue
                if Санат_мән==0:
                    негізгі_мәтін=정확한값(клиент,19)
                    if негізгі_мәтін[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=негізгі_мәтін[3]//8
                elif Санат_мән==2:
                    негізгі_мәтін=정확한값(клиент,3); 항목수=struct.unpack('>H',негізгі_мәтін[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(клиент,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 әдепкі_мән Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    негізгі_мәтін=struct.pack('>BHi',0,1,0)
                elif Санат_мән in (3,150): негізгі_мәтін=정확한값(клиент,9)
                elif Санат_мән==248:
                    негізгі_мәтін=정확한값(клиент,8)
                    if негізгі_мәтін[7]>64: raise ValueError('fence too large')
                    негізгі_мәтін+=정확한값(клиент,негізгі_мәтін[7])
                elif Санат_мән==250: негізгі_мәтін=정확한값(клиент,3)
                elif Санат_мән==251:
                    негізгі_мәтін=정확한값(клиент,7)
                    if негізгі_мәтін[5]>16: raise ValueError('too many screens')
                    негізгі_мәтін+=정확한값(клиент,негізгі_мәтін[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(Санат_мән))
                сервер_мән.sendall(bytes([Санат_мән])+негізгі_мәтін)
        except (OSError,EOFError,ValueError) as Қате:
            if str(Қате): print('VNC client:',Қате,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (клиент,сервер_мән):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def орындалу_үстелдік(порт_нөмірі=5902, желі=False, файл_тасымалдау_порт_нөмірі=2121, 전달규칙들=(), ажыратымдылық_мән=(640, 480), қонақ_мекенжай=None, орналастыру_мекенжай='127.0.0.1'):
    with ExitStack() as Ресурстар, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        желі_көпір_енгізу = None
        if желі:
            from желі_көпір import желі_көпір
            желі_көпір_енгізу = Ресурстар.enter_context(желі_көпір(файл_тасымалдау_порт_нөмірі, 전달규칙들, қонақ_мекенжай=қонақ_мекенжай, орналастыру_мекенжай=орналастыру_мекенжай))
        Жол_2=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',порт_нөмірі)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if желі_көпір_енгізу and (원격화면접속번호==файл_тасымалдау_порт_нөмірі or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and орналастыру==원격화면접속번호 for 통신규약,орналастыру,_ in желі_көпір_енгізу.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Үрдіс=subprocess.Popen(Команда(ажыратымдылық_мән)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Жол_2)]+(желі_көпір_енгізу.전달인수() if желі_көпір_енгізу else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            көпір=қосу_үстелдік(Үрдіс); оқушы=threading.Thread(target=көпір.직렬입출력,daemon=True); оқушы.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if желі_көпір_енгізу: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(орналастыру_мекенжай,файл_тасымалдау_порт_нөмірі),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            өңдеу_тапсырма=None; 가로채기됨=False
            try:
                while Үрдіс.poll() is None:
                    try: клиент,_=수신창구.accept()
                    except socket.timeout: continue
                    if өңдеу_тапсырма is not None and өңдеу_тапсырма.is_alive(): клиент.close(); continue
                    if not Жол_2.exists(): клиент.close(); continue
                    өңдеу_тапсырма=threading.Thread(target=көпір.клиент,args=(клиент,Жол_2),daemon=True); өңдеу_тапсырма.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                көпір.닫힘=True
                if желі_көпір_енгізу: желі_көпір_енгізу.Тоқтата_тұру_оқиға.set()
                if Үрдіс.poll() is None:
                    Үрдіс.terminate()
                    try: Үрдіс.wait(timeout=5)
                    except subprocess.TimeoutExpired: Үрдіс.kill(); Үрдіс.wait()
                оқушы.join(timeout=2); Үрдіс.stdin.close(); Үрдіс.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if желі_көпір_енгізу and желі_көпір_енгізу.Қате: raise RuntimeError('network bridge: '+желі_көпір_енгізу.Қате)
            return 0 if 가로채기됨 else Үрдіс.returncode


if __name__=='__main__':
    from орындау_пәрмен import 해상도읽기
    талдау_құралы=argparse.ArgumentParser(description=__doc__); талдау_құралы.add_argument('--port',type=int,default=5902)
    талдау_құралы.add_argument('--resolution',type=해상도읽기,default=(640,480))
    талдау_құралы.add_argument('--network',action='store_true'); талдау_құралы.add_argument('--ftp-port',type=int,default=2121)
    талдау_құралы.add_argument('--forward',action='append',default=[])
    аргумент_массив=талдау_құралы.parse_args()
    if аргумент_массив.forward and not аргумент_массив.network: талдау_құралы.error('--forward requires --network')
    raise SystemExit(орындалу_үстелдік(аргумент_массив.port,желі=аргумент_массив.network,файл_тасымалдау_порт_нөмірі=аргумент_массив.ftp_port,전달규칙들=аргумент_массив.forward,ажыратымдылық_мән=аргумент_массив.resolution))
