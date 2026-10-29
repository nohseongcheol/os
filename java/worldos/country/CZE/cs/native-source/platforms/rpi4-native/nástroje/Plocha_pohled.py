#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Klíč_HODNOTA 입력은 vlastní jádro_HODNOTA UART로 전달한다. localhost 전용, 단일 řízení_HODNOTA 클라이언트.
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
from Provést_příkaz import příkaz
from local_input import create


def STEJNÉ_HODNOTA(soket_HODNOTA, Velikost):
    data = bytearray()
    while len(data) < Velikost:
        조각 = soket_HODNOTA.recv(Velikost - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class klávesnice:
    def __init__(자신, poslat, 입력방식알림=None):
        자신.바이트전송 = poslat; 자신.modifikační_klávesa = set(); 자신.schránka_HODNOTA = b''
        자신.한글조합기 = create(poslat, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Klíč = set()
        자신.UNICODE_vstup = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def poslat(자신, data):
        자신.한글조합기.zápis_složení()
        자신.바이트전송(data)

    def SWITCH_MODE(자신):
        자신.한글조합기.zápis_složení(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Klíč_symbol):
        if Klíč_symbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.modifikační_klávesa.add(Klíč_symbol)
            else: 자신.modifikační_klávesa.discard(Klíč_symbol)
            return
        if not 누르는중:
            자신.SWITCH_Klíč.discard(Klíč_symbol)
            return
        CTRL = bool(자신.modifikační_klávesa & {0xffe3, 0xffe4})
        klávesa_Shift = bool(자신.modifikační_klávesa & {0xffe1, 0xffe2})
        if CTRL and klávesa_Shift and Klíč_symbol in (ord('u'),ord('U')):
            자신.한글조합기.zápis_složení(); 자신.UNICODE_vstup = ''; return
        if 자신.UNICODE_vstup is not None:
            if Klíč_symbol in (32,0xff0d):
                try:
                    HODNOTA=int(자신.UNICODE_vstup,16)
                    if 32<=HODNOTA<=0x10ffff and not 0xd800<=HODNOTA<=0xdfff: 자신.poslat(chr(HODNOTA).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_vstup=None
            elif Klíč_symbol==0xff1b: 자신.UNICODE_vstup=None
            elif Klíč_symbol==0xff08: 자신.UNICODE_vstup=자신.UNICODE_vstup[:-1]
            elif Klíč_symbol<128 and chr(Klíč_symbol) in '0123456789abcdefABCDEF' and len(자신.UNICODE_vstup)<6: 자신.UNICODE_vstup+=chr(Klíč_symbol)
            return
        if Klíč_symbol in (0xff31,0xffc6) or Klíč_symbol==32 and klávesa_Shift and not CTRL:
            if Klíč_symbol not in 자신.SWITCH_Klíč: 자신.SWITCH_MODE()
            자신.SWITCH_Klíč.add(Klíč_symbol)
            return
        if Klíč_symbol==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and klávesa_Shift and Klíč_symbol in (ord('t'),ord('T')):
            자신.poslat(bytes([30,2,1,0,0,0,0])); return
        if Klíč_symbol==0xffc3: 자신.poslat(bytes([30,2,2,0,0,0,0])); return
        if Klíč_symbol==0xffc9: 자신.poslat(bytes([30,2,3,0,0,0,0])); return
        if CTRL and klávesa_Shift and Klíč_symbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.poslat(자신.schránka_HODNOTA); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Klíč_symbol in 특수글쇠: 자신.poslat(특수글쇠[Klíč_symbol]); return
        kódování_znaků = Klíč_symbol & 0xffffff if Klíč_symbol & 0xff000000 == 0x01000000 else Klíč_symbol
        if kódování_znaků > 0x10ffff or 0xd800 <= kódování_znaků <= 0xdfff or Klíč_symbol >= 0xff00 and Klíč_symbol < 0x1000000: return
        if CTRL and 0x40 <= kódování_znaků <= 0x7f: 자신.poslat(bytes([kódování_znaků & 31])); return
        if kódování_znaků < 32: return
        if 자신.한글여부 and 자신.modifikační_klávesa & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.novinky_Klíč(chr(kódování_znaků), altgr=True): return
        řádkování_část = b'\x1b' if 자신.modifikační_klávesa & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not řádkování_část and 32<=kódování_znaků<127:
            textová_data=chr(kódování_znaků).upper() if klávesa_Shift else chr(kódování_znaků)
            if 자신.한글조합기.novinky_Klíč(textová_data): return
        자신.poslat(řádkování_část + chr(kódování_znaků).encode('utf-8'))


class spojit_Plocha:
    def __init__(자신, Proces):
        자신.Proces=Proces; 자신.zámek_HODNOTA=threading.Lock(); 자신.준비완료=False; 자신.interpret_příkazů=False; 자신.시작화면=False; 자신.informační_systémy_uzavřeno=False

    def poslat(자신, data):
        if not data or 자신.informační_systémy_uzavřeno: return
        with 자신.zámek_HODNOTA:
            try: 자신.Proces.stdin.write(data); 자신.Proces.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.Proces.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); informační_systémy_uzavřeno=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,informační_systémy_uzavřeno,그림화면,종료됨)>=0:
                    자신.interpret_příkazů=열림>max(informační_systémy_uzavřeno,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,informační_systémy_uzavřeno,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.poslat(b'terminal\n')
        finally: 자신.informační_systémy_uzavřeno=True

    def klient(자신, klient, cesta_2):
        server_HODNOTA=socket.socket(socket.AF_UNIX); server_HODNOTA.settimeout(10); klient.settimeout(10)
        klávesnice_položka=klávesnice(자신.poslat,lambda 한글여부:자신.poslat(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_HODNOTA.connect(str(cesta_2))
            # počáteční_stav 협상은 순서대로 끝낸다. 이후 výstupní_pozice 가닥만 클라이언트에 쓴다.
            klient.sendall(STEJNÉ_HODNOTA(server_HODNOTA,12))
            číslo_verze=STEJNÉ_HODNOTA(klient,12)
            if číslo_verze not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_HODNOTA.sendall(číslo_verze)
            zboží_POČET=STEJNÉ_HODNOTA(server_HODNOTA,1);klient.sendall(zboží_POČET+STEJNÉ_HODNOTA(server_HODNOTA,zboží_POČET[0]))
            Zabezpečení=STEJNÉ_HODNOTA(klient,1)
            if Zabezpečení!=b'\x01': raise ValueError('unexpected security type')
            server_HODNOTA.sendall(Zabezpečení)
            if číslo_verze==b'RFB 003.008\n':klient.sendall(STEJNÉ_HODNOTA(server_HODNOTA,4))
            server_HODNOTA.sendall(STEJNÉ_HODNOTA(klient,1))
            초기값=STEJNÉ_HODNOTA(server_HODNOTA,24)
            klient.sendall(초기값+STEJNÉ_HODNOTA(server_HODNOTA,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klient.settimeout(None);server_HODNOTA.settimeout(None)
            def výstup():
                try:
                    while True:
                        oblast_HODNOTA=STEJNÉ_HODNOTA(server_HODNOTA,1)[0]
                        if oblast_HODNOTA==0:
                            머리=STEJNÉ_HODNOTA(server_HODNOTA,3);položka_POČET=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 vzdálený_HODNOTA 포인터의 중복을 피한다.
                            Skrytý_HODNOTA=포인터지원
                            if Skrytý_HODNOTA:klient.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klient.sendall(bytes([oblast_HODNOTA])+머리)
                            for _ in range(položka_POČET):
                                obdélník=STEJNÉ_HODNOTA(server_HODNOTA,12);가로,Svislá_pozice,폭,výška_HODNOTA,Encoding_HODNOTA=struct.unpack('>HHHHi',obdélník)
                                if Encoding_HODNOTA!=0:raise ValueError('unexpected framebuffer encoding: '+str(Encoding_HODNOTA))
                                klient.sendall(obdélník)
                                남음=폭*výška_HODNOTA*화소바이트
                                while 남음:
                                    data=STEJNÉ_HODNOTA(server_HODNOTA,min(남음,65536));klient.sendall(data);남음-=len(data)
                        elif oblast_HODNOTA==1:
                            머리=STEJNÉ_HODNOTA(server_HODNOTA,5);zboží_POČET=struct.unpack('>H',머리[3:])[0]
                            klient.sendall(bytes([oblast_HODNOTA])+머리+STEJNÉ_HODNOTA(server_HODNOTA,zboží_POČET*6))
                        elif oblast_HODNOTA==2:klient.sendall(bytes([oblast_HODNOTA]))
                        elif oblast_HODNOTA==3:
                            머리=STEJNÉ_HODNOTA(server_HODNOTA,7);zboží_POČET=struct.unpack('>I',머리[3:])[0]
                            if zboží_POČET>1048576:raise ValueError('server clipboard too large')
                            klient.sendall(bytes([oblast_HODNOTA])+머리+STEJNÉ_HODNOTA(server_HODNOTA,zboží_POČET))
                        else:raise ValueError('unexpected RFB server message: '+str(oblast_HODNOTA))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klient.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            pracovník=threading.Thread(target=výstup,daemon=True);pracovník.start()
            while not 자신.informační_systémy_uzavřeno:
                oblast_HODNOTA=STEJNÉ_HODNOTA(klient,1)[0]
                if oblast_HODNOTA==4:
                    základní_text=STEJNÉ_HODNOTA(klient,7); klávesnice_položka.누름값(základní_text[0]!=0,struct.unpack('>I',základní_text[3:])[0]); continue
                if oblast_HODNOTA==255:
                    základní_text=STEJNÉ_HODNOTA(klient,11)
                    if základní_text[0]!=0: raise ValueError('unsupported QEMU input extension')
                    klávesnice_položka.누름값(struct.unpack('>H',základní_text[1:3])[0]!=0,struct.unpack('>I',základní_text[3:7])[0]); continue
                if oblast_HODNOTA==5:
                    základní_text=STEJNÉ_HODNOTA(klient,5); 단추들,souřadnice_x,Y_souřadnice=struct.unpack('>BHH',základní_text)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: klávesnice_položka.한글조합기.zápis_složení()
                    if 눌림&1 and 자신.시작화면 and 64<=souřadnice_x<576 and 112<=Y_souřadnice<372:
                        VYHLEDAT_INDEX=(Y_souřadnice-112)//52
                        if (Y_souřadnice-112)%52<40 and VYHLEDAT_INDEX<5: 자신.poslat(bytes([ord('1')+VYHLEDAT_INDEX]))
                    else: 자신.poslat(bytes([30,1,단추들,souřadnice_x&255,souřadnice_x>>8,Y_souřadnice&255,Y_souřadnice>>8]))
                    continue
                if oblast_HODNOTA==6:
                    základní_text=STEJNÉ_HODNOTA(klient,7); délka_HODNOTA=struct.unpack('>i',základní_text[3:])[0]
                    if abs(délka_HODNOTA)>65536: raise ValueError('clipboard too large')
                    text=STEJNÉ_HODNOTA(klient,abs(délka_HODNOTA))
                    if délka_HODNOTA>=0:
                        try: klávesnice_položka.schránka_HODNOTA=text.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: klávesnice_položka.schránka_HODNOTA=text.decode('latin-1').encode('utf-8')
                        klávesnice_položka.schránka_HODNOTA=klávesnice_položka.schránka_HODNOTA[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_HODNOTA.sendall(bytes([oblast_HODNOTA])+základní_text+text); continue
                if oblast_HODNOTA==0:
                    základní_text=STEJNÉ_HODNOTA(klient,19)
                    if základní_text[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=základní_text[3]//8
                elif oblast_HODNOTA==2:
                    základní_text=STEJNÉ_HODNOTA(klient,3); položka_POČET=struct.unpack('>H',základní_text[1:])[0]
                    if položka_POČET>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(položka_POČET)+'i',STEJNÉ_HODNOTA(klient,položka_POČET*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 výchozí_hodnota Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    základní_text=struct.pack('>BHi',0,1,0)
                elif oblast_HODNOTA in (3,150): základní_text=STEJNÉ_HODNOTA(klient,9)
                elif oblast_HODNOTA==248:
                    základní_text=STEJNÉ_HODNOTA(klient,8)
                    if základní_text[7]>64: raise ValueError('fence too large')
                    základní_text+=STEJNÉ_HODNOTA(klient,základní_text[7])
                elif oblast_HODNOTA==250: základní_text=STEJNÉ_HODNOTA(klient,3)
                elif oblast_HODNOTA==251:
                    základní_text=STEJNÉ_HODNOTA(klient,7)
                    if základní_text[5]>16: raise ValueError('too many screens')
                    základní_text+=STEJNÉ_HODNOTA(klient,základní_text[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(oblast_HODNOTA))
                server_HODNOTA.sendall(bytes([oblast_HODNOTA])+základní_text)
        except (OSError,EOFError,ValueError) as chyba:
            if str(chyba): print('VNC client:',chyba,file=sys.stderr,flush=True)
        finally:
            for soket_HODNOTA in (klient,server_HODNOTA):
                try: soket_HODNOTA.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                soket_HODNOTA.close()


def spustit_Plocha(číslo_portu=5902, síť=False, přenos_souborů_číslo_portu=2121, 전달규칙들=(), řešení_HODNOTA=(640, 480), host_ODKAZ=None, hostit_ODKAZ='127.0.0.1'):
    with ExitStack() as Prostředky, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        most_položka = None
        if síť:
            from most_3de4fe3a import most_3de4fe3a
            most_položka = Prostředky.enter_context(most_3de4fe3a(přenos_souborů_číslo_portu, 전달규칙들, host_ODKAZ=host_ODKAZ, hostit_ODKAZ=hostit_ODKAZ))
        cesta_2=Path(작업경로)/'display.sock'
        with socket.socket() as dostat_port:
            dostat_port.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            dostat_port.bind(('127.0.0.1',číslo_portu)); dostat_port.listen(1); dostat_port.settimeout(.2)
            원격화면접속번호=dostat_port.getsockname()[1]
            if most_položka and (원격화면접속번호==přenos_souborů_číslo_portu or 50000<=원격화면접속번호<=50007 or any(síť_ABI=='tcp' and hostit==원격화면접속번호 for síť_ABI,hostit,_ in most_položka.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proces=subprocess.Popen(příkaz(řešení_HODNOTA)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(cesta_2)]+(most_položka.전달인수() if most_položka else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            most=spojit_Plocha(Proces); Čtenář=threading.Thread(target=most.직렬입출력,daemon=True); Čtenář.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(dostat_port.getsockname()[1]),flush=True)
            if most_položka: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(hostit_ODKAZ,přenos_souborů_číslo_portu),flush=True)
            def ukončit(signál_číslo,spuštění_rámec): raise KeyboardInterrupt()
            Předchozí=signal.signal(signal.SIGTERM,ukončit)
            zpracování_úkol=None; 가로채기됨=False
            try:
                while Proces.poll() is None:
                    try: klient,_=dostat_port.accept()
                    except socket.timeout: continue
                    if zpracování_úkol is not None and zpracování_úkol.is_alive(): klient.close(); continue
                    if not cesta_2.exists(): klient.close(); continue
                    zpracování_úkol=threading.Thread(target=most.klient,args=(klient,cesta_2),daemon=True); zpracování_úkol.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                most.informační_systémy_uzavřeno=True
                if most_položka: most_položka.Pozastavit_událost.set()
                if Proces.poll() is None:
                    Proces.terminate()
                    try: Proces.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
                Čtenář.join(timeout=2); Proces.stdin.close(); Proces.stdout.close(); signal.signal(signal.SIGTERM,Předchozí)
            if most_položka and most_položka.chyba: raise RuntimeError('network bridge: '+most_položka.chyba)
            return 0 if 가로채기됨 else Proces.returncode


if __name__=='__main__':
    from Provést_příkaz import 해상도읽기
    analyzátor=argparse.ArgumentParser(description=__doc__); analyzátor.add_argument('--port',type=int,default=5902)
    analyzátor.add_argument('--resolution',type=해상도읽기,default=(640,480))
    analyzátor.add_argument('--network',action='store_true'); analyzátor.add_argument('--ftp-port',type=int,default=2121)
    analyzátor.add_argument('--forward',action='append',default=[])
    argument_pole=analyzátor.parse_args()
    if argument_pole.forward and not argument_pole.network: analyzátor.error('--forward requires --network')
    raise SystemExit(spustit_Plocha(argument_pole.port,síť=argument_pole.network,přenos_souborů_číslo_portu=argument_pole.ftp_port,전달규칙들=argument_pole.forward,řešení_HODNOTA=argument_pole.resolution))
