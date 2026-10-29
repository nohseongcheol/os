#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Tast_VALUE 입력은 자체 Kernel_VALUE UART로 전달한다. localhost 전용, 단일 Kontroll_VALUE 클라이언트.
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
from ausféieren_Befeel import Befeel
from local_input import create


def EXACT_VALUE(소켓, d_Gréisst_veränneren):
    Daten = bytearray()
    while len(Daten) < d_Gréisst_veränneren:
        조각 = 소켓.recv(d_Gréisst_veränneren - len(Daten))
        if not 조각: raise EOFError()
        Daten.extend(조각)
    return bytes(Daten)


class Tastatur:
    def __init__(자신, mailen, 입력방식알림=None):
        자신.바이트전송 = mailen; 자신.Modifikatiounstast = set(); 자신.Tëschenoflag_VALUE = b''
        자신.한글조합기 = create(mailen, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Tast = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def mailen(자신, Daten):
        자신.한글조합기.조합확정()
        자신.바이트전송(Daten)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Tast_Symbol):
        if Tast_Symbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.Modifikatiounstast.add(Tast_Symbol)
            else: 자신.Modifikatiounstast.discard(Tast_Symbol)
            return
        if not 누르는중:
            자신.SWITCH_Tast.discard(Tast_Symbol)
            return
        CTRL = bool(자신.Modifikatiounstast & {0xffe3, 0xffe4})
        SHIFT_Tast = bool(자신.Modifikatiounstast & {0xffe1, 0xffe2})
        if CTRL and SHIFT_Tast and Tast_Symbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Tast_Symbol in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.mailen(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Tast_Symbol==0xff1b: 자신.유니코드입력=None
            elif Tast_Symbol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Tast_Symbol<128 and chr(Tast_Symbol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Tast_Symbol)
            return
        if Tast_Symbol in (0xff31,0xffc6) or Tast_Symbol==32 and SHIFT_Tast and not CTRL:
            if Tast_Symbol not in 자신.SWITCH_Tast: 자신.SWITCH_MODE()
            자신.SWITCH_Tast.add(Tast_Symbol)
            return
        if Tast_Symbol==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_Tast and Tast_Symbol in (ord('t'),ord('T')):
            자신.mailen(bytes([30,2,1,0,0,0,0])); return
        if Tast_Symbol==0xffc3: 자신.mailen(bytes([30,2,2,0,0,0,0])); return
        if Tast_Symbol==0xffc9: 자신.mailen(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_Tast and Tast_Symbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.mailen(자신.Tëschenoflag_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Tast_Symbol in 특수글쇠: 자신.mailen(특수글쇠[Tast_Symbol]); return
        Zeechen_Codéierung = Tast_Symbol & 0xffffff if Tast_Symbol & 0xff000000 == 0x01000000 else Tast_Symbol
        if Zeechen_Codéierung > 0x10ffff or 0xd800 <= Zeechen_Codéierung <= 0xdfff or Tast_Symbol >= 0xff00 and Tast_Symbol < 0x1000000: return
        if CTRL and 0x40 <= Zeechen_Codéierung <= 0x7f: 자신.mailen(bytes([Zeechen_Codéierung & 31])); return
        if Zeechen_Codéierung < 32: return
        if 자신.한글여부 and 자신.Modifikatiounstast & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.Feed_Tast(chr(Zeechen_Codéierung), altgr=True): return
        앞부분 = b'\x1b' if 자신.Modifikatiounstast & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=Zeechen_Codéierung<127:
            Zeechen_Daten=chr(Zeechen_Codéierung).upper() if SHIFT_Tast else chr(Zeechen_Codéierung)
            if 자신.한글조합기.Feed_Tast(Zeechen_Daten): return
        자신.mailen(앞부분 + chr(Zeechen_Codéierung).encode('utf-8'))


class Verbannen_Desktop:
    def __init__(자신, Prozess):
        자신.Prozess=Prozess; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def mailen(자신, Daten):
        if not Daten or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Prozess.stdin.write(Daten); 자신.Prozess.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                Daten=자신.Prozess.stdout.read(4096)
                if not Daten: break
                sys.stdout.buffer.write(Daten); sys.stdout.buffer.flush()
                끝부분=(끝부분+Daten)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.mailen(b'terminal\n')
        finally: 자신.닫힘=True

    def Client(자신, Client, Wee):
        Server_VALUE=socket.socket(socket.AF_UNIX); Server_VALUE.settimeout(10); Client.settimeout(10)
        Tastatur_Agab=Tastatur(자신.mailen,lambda 한글여부:자신.mailen(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            Server_VALUE.connect(str(Wee))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            Client.sendall(EXACT_VALUE(Server_VALUE,12))
            판번호=EXACT_VALUE(Client,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            Server_VALUE.sendall(판번호)
            Element_COUNT=EXACT_VALUE(Server_VALUE,1);Client.sendall(Element_COUNT+EXACT_VALUE(Server_VALUE,Element_COUNT[0]))
            Sécherheet=EXACT_VALUE(Client,1)
            if Sécherheet!=b'\x01': raise ValueError('unexpected security type')
            Server_VALUE.sendall(Sécherheet)
            if 판번호==b'RFB 003.008\n':Client.sendall(EXACT_VALUE(Server_VALUE,4))
            Server_VALUE.sendall(EXACT_VALUE(Client,1))
            초기값=EXACT_VALUE(Server_VALUE,24)
            Client.sendall(초기값+EXACT_VALUE(Server_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            Client.settimeout(None);Server_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        Kategorie_VALUE=EXACT_VALUE(Server_VALUE,1)[0]
                        if Kategorie_VALUE==0:
                            머리=EXACT_VALUE(Server_VALUE,3);Agab_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 extern_VALUE 포인터의 중복을 피한다.
                            verstoppt_VALUE=포인터지원
                            if verstoppt_VALUE:Client.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            Client.sendall(bytes([Kategorie_VALUE])+머리)
                            for _ in range(Agab_COUNT):
                                사각형=EXACT_VALUE(Server_VALUE,12);가로,Vertikal_positionéieren,폭,높이,Codéierung_VALUE=struct.unpack('>HHHHi',사각형)
                                if Codéierung_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(Codéierung_VALUE))
                                Client.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    Daten=EXACT_VALUE(Server_VALUE,min(남음,65536));Client.sendall(Daten);남음-=len(Daten)
                        elif Kategorie_VALUE==1:
                            머리=EXACT_VALUE(Server_VALUE,5);Element_COUNT=struct.unpack('>H',머리[3:])[0]
                            Client.sendall(bytes([Kategorie_VALUE])+머리+EXACT_VALUE(Server_VALUE,Element_COUNT*6))
                        elif Kategorie_VALUE==2:Client.sendall(bytes([Kategorie_VALUE]))
                        elif Kategorie_VALUE==3:
                            머리=EXACT_VALUE(Server_VALUE,7);Element_COUNT=struct.unpack('>I',머리[3:])[0]
                            if Element_COUNT>1048576:raise ValueError('server clipboard too large')
                            Client.sendall(bytes([Kategorie_VALUE])+머리+EXACT_VALUE(Server_VALUE,Element_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(Kategorie_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:Client.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                Kategorie_VALUE=EXACT_VALUE(Client,1)[0]
                if Kategorie_VALUE==4:
                    Textkierper=EXACT_VALUE(Client,7); Tastatur_Agab.누름값(Textkierper[0]!=0,struct.unpack('>I',Textkierper[3:])[0]); continue
                if Kategorie_VALUE==255:
                    Textkierper=EXACT_VALUE(Client,11)
                    if Textkierper[0]!=0: raise ValueError('unsupported QEMU input extension')
                    Tastatur_Agab.누름값(struct.unpack('>H',Textkierper[1:3])[0]!=0,struct.unpack('>I',Textkierper[3:7])[0]); continue
                if Kategorie_VALUE==5:
                    Textkierper=EXACT_VALUE(Client,5); 단추들,X_Koordinat,세로좌표=struct.unpack('>BHH',Textkierper)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: Tastatur_Agab.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=X_Koordinat<576 and 112<=세로좌표<372:
                        LOOKUP_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and LOOKUP_INDEX<5: 자신.mailen(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.mailen(bytes([30,1,단추들,X_Koordinat&255,X_Koordinat>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if Kategorie_VALUE==6:
                    Textkierper=EXACT_VALUE(Client,7); Längt_VALUE=struct.unpack('>i',Textkierper[3:])[0]
                    if abs(Längt_VALUE)>65536: raise ValueError('clipboard too large')
                    SMS=EXACT_VALUE(Client,abs(Längt_VALUE))
                    if Längt_VALUE>=0:
                        try: Tastatur_Agab.Tëschenoflag_VALUE=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: Tastatur_Agab.Tëschenoflag_VALUE=SMS.decode('latin-1').encode('utf-8')
                        Tastatur_Agab.Tëschenoflag_VALUE=Tastatur_Agab.Tëschenoflag_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    Server_VALUE.sendall(bytes([Kategorie_VALUE])+Textkierper+SMS); continue
                if Kategorie_VALUE==0:
                    Textkierper=EXACT_VALUE(Client,19)
                    if Textkierper[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=Textkierper[3]//8
                elif Kategorie_VALUE==2:
                    Textkierper=EXACT_VALUE(Client,3); Agab_COUNT=struct.unpack('>H',Textkierper[1:])[0]
                    if Agab_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(Agab_COUNT)+'i',EXACT_VALUE(Client,Agab_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 Standardwäert Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    Textkierper=struct.pack('>BHi',0,1,0)
                elif Kategorie_VALUE in (3,150): Textkierper=EXACT_VALUE(Client,9)
                elif Kategorie_VALUE==248:
                    Textkierper=EXACT_VALUE(Client,8)
                    if Textkierper[7]>64: raise ValueError('fence too large')
                    Textkierper+=EXACT_VALUE(Client,Textkierper[7])
                elif Kategorie_VALUE==250: Textkierper=EXACT_VALUE(Client,3)
                elif Kategorie_VALUE==251:
                    Textkierper=EXACT_VALUE(Client,7)
                    if Textkierper[5]>16: raise ValueError('too many screens')
                    Textkierper+=EXACT_VALUE(Client,Textkierper[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(Kategorie_VALUE))
                Server_VALUE.sendall(bytes([Kategorie_VALUE])+Textkierper)
        except (OSError,EOFError,ValueError) as Feeler:
            if str(Feeler): print('VNC client:',Feeler,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (Client,Server_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def Laf_Desktop(접속번호=5902, Reseau=False, 파일전송접속번호=2121, 전달규칙들=(), Opléisung_VALUE=(640, 480), Gaascht_Adress=None, Host_Adress='127.0.0.1'):
    with ExitStack() as Ressourcen, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Reseau_Bréck_Agab = None
        if Reseau:
            from Reseau_Bréck import Reseau_Bréck
            Reseau_Bréck_Agab = Ressourcen.enter_context(Reseau_Bréck(파일전송접속번호, 전달규칙들, Gaascht_Adress=Gaascht_Adress, Host_Adress=Host_Adress))
        Wee=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Reseau_Bréck_Agab and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and Host==원격화면접속번호 for 통신규약,Host,_ in Reseau_Bréck_Agab.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Prozess=subprocess.Popen(Befeel(Opléisung_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Wee)]+(Reseau_Bréck_Agab.전달인수() if Reseau_Bréck_Agab else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            Bréck=Verbannen_Desktop(Prozess); Lieser=threading.Thread(target=Bréck.직렬입출력,daemon=True); Lieser.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Reseau_Bréck_Agab: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(Host_Adress,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Prozess.poll() is None:
                    try: Client,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): Client.close(); continue
                    if not Wee.exists(): Client.close(); continue
                    처리작업=threading.Thread(target=Bréck.Client,args=(Client,Wee),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                Bréck.닫힘=True
                if Reseau_Bréck_Agab: Reseau_Bréck_Agab.pausen_Evenement.set()
                if Prozess.poll() is None:
                    Prozess.terminate()
                    try: Prozess.wait(timeout=5)
                    except subprocess.TimeoutExpired: Prozess.kill(); Prozess.wait()
                Lieser.join(timeout=2); Prozess.stdin.close(); Prozess.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Reseau_Bréck_Agab and Reseau_Bréck_Agab.Feeler: raise RuntimeError('network bridge: '+Reseau_Bréck_Agab.Feeler)
            return 0 if 가로채기됨 else Prozess.returncode


if __name__=='__main__':
    from ausféieren_Befeel import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    Argument_ARRAY=인수해석기.parse_args()
    if Argument_ARRAY.forward and not Argument_ARRAY.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(Laf_Desktop(Argument_ARRAY.port,Reseau=Argument_ARRAY.network,파일전송접속번호=Argument_ARRAY.ftp_port,전달규칙들=Argument_ARRAY.forward,Opléisung_VALUE=Argument_ARRAY.resolution))
