#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Kľúč_VALUE 입력은 vlastné jadro_VALUE UART로 전달한다. localhost 전용, 단일 riadenie_VALUE 클라이언트.
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
from Vykonať_príkaz import Príkaz
from local_input import create


def EXACT_VALUE(soket_VALUE, Veľkosť):
    údaje = bytearray()
    while len(údaje) < Veľkosť:
        조각 = soket_VALUE.recv(Veľkosť - len(údaje))
        if not 조각: raise EOFError()
        údaje.extend(조각)
    return bytes(údaje)


class klávesnica:
    def __init__(자신, odoslať, 입력방식알림=None):
        자신.바이트전송 = odoslať; 자신.보조글쇠 = set(); 자신.Schránka_VALUE = b''
        자신.한글조합기 = create(odoslať, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Kľúč = set()
        자신.UNICODE_vstup = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def odoslať(자신, údaje):
        자신.한글조합기.조합확정()
        자신.바이트전송(údaje)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Kľúč_symbol):
        if Kľúč_symbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.보조글쇠.add(Kľúč_symbol)
            else: 자신.보조글쇠.discard(Kľúč_symbol)
            return
        if not 누르는중:
            자신.SWITCH_Kľúč.discard(Kľúč_symbol)
            return
        kláves_CTRL = bool(자신.보조글쇠 & {0xffe3, 0xffe4})
        kláves_Shift = bool(자신.보조글쇠 & {0xffe1, 0xffe2})
        if kláves_CTRL and kláves_Shift and Kľúč_symbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.UNICODE_vstup = ''; return
        if 자신.UNICODE_vstup is not None:
            if Kľúč_symbol in (32,0xff0d):
                try:
                    VALUE=int(자신.UNICODE_vstup,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.odoslať(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_vstup=None
            elif Kľúč_symbol==0xff1b: 자신.UNICODE_vstup=None
            elif Kľúč_symbol==0xff08: 자신.UNICODE_vstup=자신.UNICODE_vstup[:-1]
            elif Kľúč_symbol<128 and chr(Kľúč_symbol) in '0123456789abcdefABCDEF' and len(자신.UNICODE_vstup)<6: 자신.UNICODE_vstup+=chr(Kľúč_symbol)
            return
        if Kľúč_symbol in (0xff31,0xffc6) or Kľúč_symbol==32 and kláves_Shift and not kláves_CTRL:
            if Kľúč_symbol not in 자신.SWITCH_Kľúč: 자신.SWITCH_MODE()
            자신.SWITCH_Kľúč.add(Kľúč_symbol)
            return
        if Kľúč_symbol==0xff08 and 자신.한글여부 and not kláves_CTRL and 자신.한글조합기.앞글자지우기(): return
        if kláves_CTRL and kláves_Shift and Kľúč_symbol in (ord('t'),ord('T')):
            자신.odoslať(bytes([30,2,1,0,0,0,0])); return
        if Kľúč_symbol==0xffc3: 자신.odoslať(bytes([30,2,2,0,0,0,0])); return
        if Kľúč_symbol==0xffc9: 자신.odoslať(bytes([30,2,3,0,0,0,0])); return
        if kláves_CTRL and kláves_Shift and Kľúč_symbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.odoslať(자신.Schránka_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Kľúč_symbol in 특수글쇠: 자신.odoslať(특수글쇠[Kľúč_symbol]); return
        kódovanie_znakov = Kľúč_symbol & 0xffffff if Kľúč_symbol & 0xff000000 == 0x01000000 else Kľúč_symbol
        if kódovanie_znakov > 0x10ffff or 0xd800 <= kódovanie_znakov <= 0xdfff or Kľúč_symbol >= 0xff00 and Kľúč_symbol < 0x1000000: return
        if kláves_CTRL and 0x40 <= kódovanie_znakov <= 0x7f: 자신.odoslať(bytes([kódovanie_znakov & 31])); return
        if kódovanie_znakov < 32: return
        if 자신.한글여부 and 자신.보조글쇠 & {0xffea,0xfe03,0xff7e} and not kláves_CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.súhrnný_obsah_Kľúč(chr(kódovanie_znakov), altgr=True): return
        앞부분 = b'\x1b' if 자신.보조글쇠 & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not kláves_CTRL and not 앞부분 and 32<=kódovanie_znakov<127:
            znakové_údaje=chr(kódovanie_znakov).upper() if kláves_Shift else chr(kódovanie_znakov)
            if 자신.한글조합기.súhrnný_obsah_Kľúč(znakové_údaje): return
        자신.odoslať(앞부분 + chr(kódovanie_znakov).encode('utf-8'))


class spojiť_počítač:
    def __init__(자신, Proces):
        자신.Proces=Proces; 자신.zámok_VALUE=threading.Lock(); 자신.준비완료=False; 자신.Terminál=False; 자신.시작화면=False; 자신.닫힘=False

    def odoslať(자신, údaje):
        if not údaje or 자신.닫힘: return
        with 자신.zámok_VALUE:
            try: 자신.Proces.stdin.write(údaje); 자신.Proces.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                údaje=자신.Proces.stdout.read(4096)
                if not údaje: break
                sys.stdout.buffer.write(údaje); sys.stdout.buffer.flush()
                끝부분=(끝부분+údaje)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminál=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.odoslať(b'terminal\n')
        finally: 자신.닫힘=True

    def klient(자신, klient, Cesta):
        server_VALUE=socket.socket(socket.AF_UNIX); server_VALUE.settimeout(10); klient.settimeout(10)
        klávesnica_položka=klávesnica(자신.odoslať,lambda 한글여부:자신.odoslať(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VALUE.connect(str(Cesta))
            # počiatočný_stav 협상은 순서대로 끝낸다. 이후 Výstup 가닥만 클라이언트에 쓴다.
            klient.sendall(EXACT_VALUE(server_VALUE,12))
            číslo_verzie=EXACT_VALUE(klient,12)
            if číslo_verzie not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VALUE.sendall(číslo_verzie)
            položka_COUNT=EXACT_VALUE(server_VALUE,1);klient.sendall(položka_COUNT+EXACT_VALUE(server_VALUE,položka_COUNT[0]))
            Zabezpečenie=EXACT_VALUE(klient,1)
            if Zabezpečenie!=b'\x01': raise ValueError('unexpected security type')
            server_VALUE.sendall(Zabezpečenie)
            if číslo_verzie==b'RFB 003.008\n':klient.sendall(EXACT_VALUE(server_VALUE,4))
            server_VALUE.sendall(EXACT_VALUE(klient,1))
            초기값=EXACT_VALUE(server_VALUE,24)
            klient.sendall(초기값+EXACT_VALUE(server_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klient.settimeout(None);server_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        oblasť_VALUE=EXACT_VALUE(server_VALUE,1)[0]
                        if oblasť_VALUE==0:
                            머리=EXACT_VALUE(server_VALUE,3);položka_COUNT_8f7753a1=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 vzdialený_VALUE 포인터의 중복을 피한다.
                            Skryté_VALUE=포인터지원
                            if Skryté_VALUE:klient.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klient.sendall(bytes([oblasť_VALUE])+머리)
                            for _ in range(položka_COUNT_8f7753a1):
                                obdĺžnik=EXACT_VALUE(server_VALUE,12);가로,vertikála_pozícia,폭,výška_VALUE,kódovanie_VALUE=struct.unpack('>HHHHi',obdĺžnik)
                                if kódovanie_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(kódovanie_VALUE))
                                klient.sendall(obdĺžnik)
                                남음=폭*výška_VALUE*화소바이트
                                while 남음:
                                    údaje=EXACT_VALUE(server_VALUE,min(남음,65536));klient.sendall(údaje);남음-=len(údaje)
                        elif oblasť_VALUE==1:
                            머리=EXACT_VALUE(server_VALUE,5);položka_COUNT=struct.unpack('>H',머리[3:])[0]
                            klient.sendall(bytes([oblasť_VALUE])+머리+EXACT_VALUE(server_VALUE,položka_COUNT*6))
                        elif oblasť_VALUE==2:klient.sendall(bytes([oblasť_VALUE]))
                        elif oblasť_VALUE==3:
                            머리=EXACT_VALUE(server_VALUE,7);položka_COUNT=struct.unpack('>I',머리[3:])[0]
                            if položka_COUNT>1048576:raise ValueError('server clipboard too large')
                            klient.sendall(bytes([oblasť_VALUE])+머리+EXACT_VALUE(server_VALUE,položka_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(oblasť_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klient.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                oblasť_VALUE=EXACT_VALUE(klient,1)[0]
                if oblasť_VALUE==4:
                    základný_text=EXACT_VALUE(klient,7); klávesnica_položka.누름값(základný_text[0]!=0,struct.unpack('>I',základný_text[3:])[0]); continue
                if oblasť_VALUE==255:
                    základný_text=EXACT_VALUE(klient,11)
                    if základný_text[0]!=0: raise ValueError('unsupported QEMU input extension')
                    klávesnica_položka.누름값(struct.unpack('>H',základný_text[1:3])[0]!=0,struct.unpack('>I',základný_text[3:7])[0]); continue
                if oblasť_VALUE==5:
                    základný_text=EXACT_VALUE(klient,5); 단추들,X_súradnica,Y_súradnica=struct.unpack('>BHH',základný_text)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: klávesnica_položka.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=X_súradnica<576 and 112<=Y_súradnica<372:
                        LOOKUP_INDEX=(Y_súradnica-112)//52
                        if (Y_súradnica-112)%52<40 and LOOKUP_INDEX<5: 자신.odoslať(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.odoslať(bytes([30,1,단추들,X_súradnica&255,X_súradnica>>8,Y_súradnica&255,Y_súradnica>>8]))
                    continue
                if oblasť_VALUE==6:
                    základný_text=EXACT_VALUE(klient,7); dĺžka_VALUE=struct.unpack('>i',základný_text[3:])[0]
                    if abs(dĺžka_VALUE)>65536: raise ValueError('clipboard too large')
                    Spracovanie_textu=EXACT_VALUE(klient,abs(dĺžka_VALUE))
                    if dĺžka_VALUE>=0:
                        try: klávesnica_položka.Schránka_VALUE=Spracovanie_textu.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: klávesnica_položka.Schránka_VALUE=Spracovanie_textu.decode('latin-1').encode('utf-8')
                        klávesnica_položka.Schránka_VALUE=klávesnica_položka.Schránka_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VALUE.sendall(bytes([oblasť_VALUE])+základný_text+Spracovanie_textu); continue
                if oblasť_VALUE==0:
                    základný_text=EXACT_VALUE(klient,19)
                    if základný_text[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=základný_text[3]//8
                elif oblasť_VALUE==2:
                    základný_text=EXACT_VALUE(klient,3); položka_COUNT_8f7753a1=struct.unpack('>H',základný_text[1:])[0]
                    if položka_COUNT_8f7753a1>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(položka_COUNT_8f7753a1)+'i',EXACT_VALUE(klient,položka_COUNT_8f7753a1*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 predvolená_hodnota Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    základný_text=struct.pack('>BHi',0,1,0)
                elif oblasť_VALUE in (3,150): základný_text=EXACT_VALUE(klient,9)
                elif oblasť_VALUE==248:
                    základný_text=EXACT_VALUE(klient,8)
                    if základný_text[7]>64: raise ValueError('fence too large')
                    základný_text+=EXACT_VALUE(klient,základný_text[7])
                elif oblasť_VALUE==250: základný_text=EXACT_VALUE(klient,3)
                elif oblasť_VALUE==251:
                    základný_text=EXACT_VALUE(klient,7)
                    if základný_text[5]>16: raise ValueError('too many screens')
                    základný_text+=EXACT_VALUE(klient,základný_text[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(oblasť_VALUE))
                server_VALUE.sendall(bytes([oblasť_VALUE])+základný_text)
        except (OSError,EOFError,ValueError) as chyba:
            if str(chyba): print('VNC client:',chyba,file=sys.stderr,flush=True)
        finally:
            for soket_VALUE in (klient,server_VALUE):
                try: soket_VALUE.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                soket_VALUE.close()


def spustiť_počítač(číslo_portu=5902, sieť=False, prenos_súborov_číslo_portu=2121, 전달규칙들=(), rozlíšenie_VALUE=(640, 480), hosť_adresa=None, hostiteľ_adresa='127.0.0.1'):
    with ExitStack() as Zdroje, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        sieťový_most_položka = None
        if sieť:
            from sieťový_most import sieťový_most
            sieťový_most_položka = Zdroje.enter_context(sieťový_most(prenos_súborov_číslo_portu, 전달규칙들, hosť_adresa=hosť_adresa, hostiteľ_adresa=hostiteľ_adresa))
        Cesta=Path(작업경로)/'display.sock'
        with socket.socket() as dostať_port:
            dostať_port.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            dostať_port.bind(('127.0.0.1',číslo_portu)); dostať_port.listen(1); dostať_port.settimeout(.2)
            원격화면접속번호=dostať_port.getsockname()[1]
            if sieťový_most_položka and (원격화면접속번호==prenos_súborov_číslo_portu or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and hostiteľ==원격화면접속번호 for 통신규약,hostiteľ,_ in sieťový_most_položka.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proces=subprocess.Popen(Príkaz(rozlíšenie_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Cesta)]+(sieťový_most_položka.전달인수() if sieťový_most_položka else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            most=spojiť_počítač(Proces); Čítačka=threading.Thread(target=most.직렬입출력,daemon=True); Čítačka.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(dostať_port.getsockname()[1]),flush=True)
            if sieťový_most_položka: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(hostiteľ_adresa,prenos_súborov_číslo_portu),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            spracovanie_úloha=None; 가로채기됨=False
            try:
                while Proces.poll() is None:
                    try: klient,_=dostať_port.accept()
                    except socket.timeout: continue
                    if spracovanie_úloha is not None and spracovanie_úloha.is_alive(): klient.close(); continue
                    if not Cesta.exists(): klient.close(); continue
                    spracovanie_úloha=threading.Thread(target=most.klient,args=(klient,Cesta),daemon=True); spracovanie_úloha.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                most.닫힘=True
                if sieťový_most_položka: sieťový_most_položka.Pozastaviť_udalosť.set()
                if Proces.poll() is None:
                    Proces.terminate()
                    try: Proces.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
                Čítačka.join(timeout=2); Proces.stdin.close(); Proces.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if sieťový_most_položka and sieťový_most_položka.chyba: raise RuntimeError('network bridge: '+sieťový_most_položka.chyba)
            return 0 if 가로채기됨 else Proces.returncode


if __name__=='__main__':
    from Vykonať_príkaz import 해상도읽기
    analyzátor=argparse.ArgumentParser(description=__doc__); analyzátor.add_argument('--port',type=int,default=5902)
    analyzátor.add_argument('--resolution',type=해상도읽기,default=(640,480))
    analyzátor.add_argument('--network',action='store_true'); analyzátor.add_argument('--ftp-port',type=int,default=2121)
    analyzátor.add_argument('--forward',action='append',default=[])
    argument_pole=analyzátor.parse_args()
    if argument_pole.forward and not argument_pole.network: analyzátor.error('--forward requires --network')
    raise SystemExit(spustiť_počítač(argument_pole.port,sieť=argument_pole.network,prenos_súborov_číslo_portu=argument_pole.ftp_port,전달규칙들=argument_pole.forward,rozlíšenie_VALUE=argument_pole.resolution))
