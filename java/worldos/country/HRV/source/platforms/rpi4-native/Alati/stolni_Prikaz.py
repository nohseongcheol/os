#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Ključ_VALUE 입력은 vlastiti jezgra_sustava_VALUE UART로 전달한다. localhost 전용, 단일 kontrola_VALUE 클라이언트.
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
from Izvrši_naredba import Naredba
from local_input import create


def EXACT_VALUE(소켓, Veličina):
    podaci = bytearray()
    while len(podaci) < Veličina:
        fragment_VALUE = 소켓.recv(Veličina - len(podaci))
        if not fragment_VALUE: raise EOFError()
        podaci.extend(fragment_VALUE)
    return bytes(podaci)


class tipkovnica:
    def __init__(자신, slati, 입력방식알림=None):
        자신.바이트전송 = slati; 자신.tipka_za_modificiranje = set(); 자신.međuspremnik_VALUE = b''
        자신.한글조합기 = create(slati, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Ključ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def slati(자신, podaci):
        자신.한글조합기.조합확정()
        자신.바이트전송(podaci)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Ključ_simbol):
        if Ključ_simbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.tipka_za_modificiranje.add(Ključ_simbol)
            else: 자신.tipka_za_modificiranje.discard(Ključ_simbol)
            return
        if not 누르는중:
            자신.SWITCH_Ključ.discard(Ključ_simbol)
            return
        kontrola_Ključ = bool(자신.tipka_za_modificiranje & {0xffe3, 0xffe4})
        윗글쇠 = bool(자신.tipka_za_modificiranje & {0xffe1, 0xffe2})
        if kontrola_Ključ and 윗글쇠 and Ključ_simbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Ključ_simbol in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.slati(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Ključ_simbol==0xff1b: 자신.유니코드입력=None
            elif Ključ_simbol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Ključ_simbol<128 and chr(Ključ_simbol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Ključ_simbol)
            return
        if Ključ_simbol in (0xff31,0xffc6) or Ključ_simbol==32 and 윗글쇠 and not kontrola_Ključ:
            if Ključ_simbol not in 자신.SWITCH_Ključ: 자신.SWITCH_MODE()
            자신.SWITCH_Ključ.add(Ključ_simbol)
            return
        if Ključ_simbol==0xff08 and 자신.한글여부 and not kontrola_Ključ and 자신.한글조합기.앞글자지우기(): return
        if kontrola_Ključ and 윗글쇠 and Ključ_simbol in (ord('t'),ord('T')):
            자신.slati(bytes([30,2,1,0,0,0,0])); return
        if Ključ_simbol==0xffc3: 자신.slati(bytes([30,2,2,0,0,0,0])); return
        if Ključ_simbol==0xffc9: 자신.slati(bytes([30,2,3,0,0,0,0])); return
        if kontrola_Ključ and 윗글쇠 and Ključ_simbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.slati(자신.međuspremnik_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Ključ_simbol in 특수글쇠: 자신.slati(특수글쇠[Ključ_simbol]); return
        kodiranje_znakova = Ključ_simbol & 0xffffff if Ključ_simbol & 0xff000000 == 0x01000000 else Ključ_simbol
        if kodiranje_znakova > 0x10ffff or 0xd800 <= kodiranje_znakova <= 0xdfff or Ključ_simbol >= 0xff00 and Ključ_simbol < 0x1000000: return
        if kontrola_Ključ and 0x40 <= kodiranje_znakova <= 0x7f: 자신.slati(bytes([kodiranje_znakova & 31])); return
        if kodiranje_znakova < 32: return
        if 자신.한글여부 and 자신.tipka_za_modificiranje & {0xffea,0xfe03,0xff7e} and not kontrola_Ključ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.sažeci_Ključ(chr(kodiranje_znakova), altgr=True): return
        앞부분 = b'\x1b' if 자신.tipka_za_modificiranje & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not kontrola_Ključ and not 앞부분 and 32<=kodiranje_znakova<127:
            znakovni_podaci=chr(kodiranje_znakova).upper() if 윗글쇠 else chr(kodiranje_znakova)
            if 자신.한글조합기.sažeci_Ključ(znakovni_podaci): return
        자신.slati(앞부분 + chr(kodiranje_znakova).encode('utf-8'))


class CONNECT_stolni:
    def __init__(자신, Proces):
        자신.Proces=Proces; 자신.zaključati_VALUE=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def slati(자신, podaci):
        if not podaci or 자신.닫힘: return
        with 자신.zaključati_VALUE:
            try: 자신.Proces.stdin.write(podaci); 자신.Proces.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                podaci=자신.Proces.stdout.read(4096)
                if not podaci: break
                sys.stdout.buffer.write(podaci); sys.stdout.buffer.flush()
                끝부분=(끝부분+podaci)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.slati(b'terminal\n')
        finally: 자신.닫힘=True

    def klijent(자신, klijent, PUTANJA):
        server_VALUE=socket.socket(socket.AF_UNIX); server_VALUE.settimeout(10); klijent.settimeout(10)
        tipkovnica_unos=tipkovnica(자신.slati,lambda 한글여부:자신.slati(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VALUE.connect(str(PUTANJA))
            # početno_stanje 협상은 순서대로 끝낸다. 이후 Izlaz 가닥만 클라이언트에 쓴다.
            klijent.sendall(EXACT_VALUE(server_VALUE,12))
            broj_verzije=EXACT_VALUE(klijent,12)
            if broj_verzije not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VALUE.sendall(broj_verzije)
            artikl_COUNT=EXACT_VALUE(server_VALUE,1);klijent.sendall(artikl_COUNT+EXACT_VALUE(server_VALUE,artikl_COUNT[0]))
            Sigurnost=EXACT_VALUE(klijent,1)
            if Sigurnost!=b'\x01': raise ValueError('unexpected security type')
            server_VALUE.sendall(Sigurnost)
            if broj_verzije==b'RFB 003.008\n':klijent.sendall(EXACT_VALUE(server_VALUE,4))
            server_VALUE.sendall(EXACT_VALUE(klijent,1))
            초기값=EXACT_VALUE(server_VALUE,24)
            klijent.sendall(초기값+EXACT_VALUE(server_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klijent.settimeout(None);server_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        područje_VALUE=EXACT_VALUE(server_VALUE,1)[0]
                        if područje_VALUE==0:
                            머리=EXACT_VALUE(server_VALUE,3);unos_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 udaljeno_VALUE 포인터의 중복을 피한다.
                            sakriven_VALUE=포인터지원
                            if sakriven_VALUE:klijent.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klijent.sendall(bytes([područje_VALUE])+머리)
                            for _ in range(unos_COUNT):
                                pravokutnik=EXACT_VALUE(server_VALUE,12);가로,Okomito_položaj,폭,높이,šifriranje_VALUE=struct.unpack('>HHHHi',pravokutnik)
                                if šifriranje_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(šifriranje_VALUE))
                                klijent.sendall(pravokutnik)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    podaci=EXACT_VALUE(server_VALUE,min(남음,65536));klijent.sendall(podaci);남음-=len(podaci)
                        elif područje_VALUE==1:
                            머리=EXACT_VALUE(server_VALUE,5);artikl_COUNT=struct.unpack('>H',머리[3:])[0]
                            klijent.sendall(bytes([područje_VALUE])+머리+EXACT_VALUE(server_VALUE,artikl_COUNT*6))
                        elif područje_VALUE==2:klijent.sendall(bytes([područje_VALUE]))
                        elif područje_VALUE==3:
                            머리=EXACT_VALUE(server_VALUE,7);artikl_COUNT=struct.unpack('>I',머리[3:])[0]
                            if artikl_COUNT>1048576:raise ValueError('server clipboard too large')
                            klijent.sendall(bytes([područje_VALUE])+머리+EXACT_VALUE(server_VALUE,artikl_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(područje_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klijent.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                područje_VALUE=EXACT_VALUE(klijent,1)[0]
                if područje_VALUE==4:
                    tijelo_teksta=EXACT_VALUE(klijent,7); tipkovnica_unos.누름값(tijelo_teksta[0]!=0,struct.unpack('>I',tijelo_teksta[3:])[0]); continue
                if područje_VALUE==255:
                    tijelo_teksta=EXACT_VALUE(klijent,11)
                    if tijelo_teksta[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tipkovnica_unos.누름값(struct.unpack('>H',tijelo_teksta[1:3])[0]!=0,struct.unpack('>I',tijelo_teksta[3:7])[0]); continue
                if područje_VALUE==5:
                    tijelo_teksta=EXACT_VALUE(klijent,5); 단추들,koordinata_x,세로좌표=struct.unpack('>BHH',tijelo_teksta)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tipkovnica_unos.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=koordinata_x<576 and 112<=세로좌표<372:
                        LOOKUP_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and LOOKUP_INDEX<5: 자신.slati(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.slati(bytes([30,1,단추들,koordinata_x&255,koordinata_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if područje_VALUE==6:
                    tijelo_teksta=EXACT_VALUE(klijent,7); 길이=struct.unpack('>i',tijelo_teksta[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    Tekst=EXACT_VALUE(klijent,abs(길이))
                    if 길이>=0:
                        try: tipkovnica_unos.međuspremnik_VALUE=Tekst.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tipkovnica_unos.međuspremnik_VALUE=Tekst.decode('latin-1').encode('utf-8')
                        tipkovnica_unos.međuspremnik_VALUE=tipkovnica_unos.međuspremnik_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VALUE.sendall(bytes([područje_VALUE])+tijelo_teksta+Tekst); continue
                if područje_VALUE==0:
                    tijelo_teksta=EXACT_VALUE(klijent,19)
                    if tijelo_teksta[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=tijelo_teksta[3]//8
                elif područje_VALUE==2:
                    tijelo_teksta=EXACT_VALUE(klijent,3); unos_COUNT=struct.unpack('>H',tijelo_teksta[1:])[0]
                    if unos_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(unos_COUNT)+'i',EXACT_VALUE(klijent,unos_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 zadana_vrijednost Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    tijelo_teksta=struct.pack('>BHi',0,1,0)
                elif područje_VALUE in (3,150): tijelo_teksta=EXACT_VALUE(klijent,9)
                elif područje_VALUE==248:
                    tijelo_teksta=EXACT_VALUE(klijent,8)
                    if tijelo_teksta[7]>64: raise ValueError('fence too large')
                    tijelo_teksta+=EXACT_VALUE(klijent,tijelo_teksta[7])
                elif područje_VALUE==250: tijelo_teksta=EXACT_VALUE(klijent,3)
                elif područje_VALUE==251:
                    tijelo_teksta=EXACT_VALUE(klijent,7)
                    if tijelo_teksta[5]>16: raise ValueError('too many screens')
                    tijelo_teksta+=EXACT_VALUE(klijent,tijelo_teksta[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(područje_VALUE))
                server_VALUE.sendall(bytes([područje_VALUE])+tijelo_teksta)
        except (OSError,EOFError,ValueError) as GREŠKA:
            if str(GREŠKA): print('VNC client:',GREŠKA,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (klijent,server_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def izvršiti_stolni(broj_priključka=5902, mreža=False, prijenos_datoteka_broj_priključka=2121, 전달규칙들=(), razlučivost_VALUE=(640, 480), gost_adresa=None, domaćin_adresa='127.0.0.1'):
    with ExitStack() as Resursi, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        most_unos = None
        if mreža:
            from most_3de4fe3a import most_3de4fe3a
            most_unos = Resursi.enter_context(most_3de4fe3a(prijenos_datoteka_broj_priključka, 전달규칙들, gost_adresa=gost_adresa, domaćin_adresa=domaćin_adresa))
        PUTANJA=Path(작업경로)/'display.sock'
        with socket.socket() as primiti_prebaciti:
            primiti_prebaciti.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            primiti_prebaciti.bind(('127.0.0.1',broj_priključka)); primiti_prebaciti.listen(1); primiti_prebaciti.settimeout(.2)
            원격화면접속번호=primiti_prebaciti.getsockname()[1]
            if most_unos and (원격화면접속번호==prijenos_datoteka_broj_priključka or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and domaćin==원격화면접속번호 for 통신규약,domaćin,_ in most_unos.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proces=subprocess.Popen(Naredba(razlučivost_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(PUTANJA)]+(most_unos.전달인수() if most_unos else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            most=CONNECT_stolni(Proces); Čitač=threading.Thread(target=most.직렬입출력,daemon=True); Čitač.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(primiti_prebaciti.getsockname()[1]),flush=True)
            if most_unos: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(domaćin_adresa,prijenos_datoteka_broj_priključka),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            obrada_obaveza=None; 가로채기됨=False
            try:
                while Proces.poll() is None:
                    try: klijent,_=primiti_prebaciti.accept()
                    except socket.timeout: continue
                    if obrada_obaveza is not None and obrada_obaveza.is_alive(): klijent.close(); continue
                    if not PUTANJA.exists(): klijent.close(); continue
                    obrada_obaveza=threading.Thread(target=most.klijent,args=(klijent,PUTANJA),daemon=True); obrada_obaveza.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                most.닫힘=True
                if most_unos: most_unos.Pauziraj_događaj.set()
                if Proces.poll() is None:
                    Proces.terminate()
                    try: Proces.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
                Čitač.join(timeout=2); Proces.stdin.close(); Proces.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if most_unos and most_unos.GREŠKA: raise RuntimeError('network bridge: '+most_unos.GREŠKA)
            return 0 if 가로채기됨 else Proces.returncode


if __name__=='__main__':
    from Izvrši_naredba import 해상도읽기
    analizator=argparse.ArgumentParser(description=__doc__); analizator.add_argument('--port',type=int,default=5902)
    analizator.add_argument('--resolution',type=해상도읽기,default=(640,480))
    analizator.add_argument('--network',action='store_true'); analizator.add_argument('--ftp-port',type=int,default=2121)
    analizator.add_argument('--forward',action='append',default=[])
    argument_ARRAY=analizator.parse_args()
    if argument_ARRAY.forward and not argument_ARRAY.network: analizator.error('--forward requires --network')
    raise SystemExit(izvršiti_stolni(argument_ARRAY.port,mreža=argument_ARRAY.network,prijenos_datoteka_broj_priključka=argument_ARRAY.ftp_port,전달규칙들=argument_ARRAY.forward,razlučivost_VALUE=argument_ARRAY.resolution))
