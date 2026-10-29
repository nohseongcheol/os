#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Klucz_WARTOŚĆ 입력은 własny jądro_WARTOŚĆ UART로 전달한다. localhost 전용, 단일 kontrola_WARTOŚĆ 클라이언트.
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
from Wykonaj_polecenie import polecenie
from local_input import create


def PORÓWNAJ_WARTOŚĆ(gniazdo_WARTOŚĆ, Rozmiar):
    dane = bytearray()
    while len(dane) < Rozmiar:
        fragment_WARTOŚĆ_652d4b53 = gniazdo_WARTOŚĆ.recv(Rozmiar - len(dane))
        if not fragment_WARTOŚĆ_652d4b53: raise EOFError()
        dane.extend(fragment_WARTOŚĆ_652d4b53)
    return bytes(dane)


class klawiatura:
    def __init__(자신, wysłać, 입력방식알림=None):
        자신.바이트전송 = wysłać; 자신.klawisz_modyfikujący = set(); 자신.schowek_WARTOŚĆ = b''
        자신.한글조합기 = create(wysłać, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.zmiana_Klucz = set()
        자신.UNICODE_wejście = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def wysłać(자신, dane):
        자신.한글조합기.przekazywać_kompozycja()
        자신.바이트전송(dane)

    def zmiana_tryb(자신):
        자신.한글조합기.przekazywać_kompozycja(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Klucz_symbol):
        if Klucz_symbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.klawisz_modyfikujący.add(Klucz_symbol)
            else: 자신.klawisz_modyfikujący.discard(Klucz_symbol)
            return
        if not 누르는중:
            자신.zmiana_Klucz.discard(Klucz_symbol)
            return
        CTRL = bool(자신.klawisz_modyfikujący & {0xffe3, 0xffe4})
        klawisz_SHIFT = bool(자신.klawisz_modyfikujący & {0xffe1, 0xffe2})
        if CTRL and klawisz_SHIFT and Klucz_symbol in (ord('u'),ord('U')):
            자신.한글조합기.przekazywać_kompozycja(); 자신.UNICODE_wejście = ''; return
        if 자신.UNICODE_wejście is not None:
            if Klucz_symbol in (32,0xff0d):
                try:
                    WARTOŚĆ=int(자신.UNICODE_wejście,16)
                    if 32<=WARTOŚĆ<=0x10ffff and not 0xd800<=WARTOŚĆ<=0xdfff: 자신.wysłać(chr(WARTOŚĆ).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_wejście=None
            elif Klucz_symbol==0xff1b: 자신.UNICODE_wejście=None
            elif Klucz_symbol==0xff08: 자신.UNICODE_wejście=자신.UNICODE_wejście[:-1]
            elif Klucz_symbol<128 and chr(Klucz_symbol) in '0123456789abcdefABCDEF' and len(자신.UNICODE_wejście)<6: 자신.UNICODE_wejście+=chr(Klucz_symbol)
            return
        if Klucz_symbol in (0xff31,0xffc6) or Klucz_symbol==32 and klawisz_SHIFT and not CTRL:
            if Klucz_symbol not in 자신.zmiana_Klucz: 자신.zmiana_tryb()
            자신.zmiana_Klucz.add(Klucz_symbol)
            return
        if Klucz_symbol==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and klawisz_SHIFT and Klucz_symbol in (ord('t'),ord('T')):
            자신.wysłać(bytes([30,2,1,0,0,0,0])); return
        if Klucz_symbol==0xffc3: 자신.wysłać(bytes([30,2,2,0,0,0,0])); return
        if Klucz_symbol==0xffc9: 자신.wysłać(bytes([30,2,3,0,0,0,0])); return
        if CTRL and klawisz_SHIFT and Klucz_symbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.wysłać(자신.schowek_WARTOŚĆ); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Klucz_symbol in 특수글쇠: 자신.wysłać(특수글쇠[Klucz_symbol]); return
        kodowanie_znaku = Klucz_symbol & 0xffffff if Klucz_symbol & 0xff000000 == 0x01000000 else Klucz_symbol
        if kodowanie_znaku > 0x10ffff or 0xd800 <= kodowanie_znaku <= 0xdfff or Klucz_symbol >= 0xff00 and Klucz_symbol < 0x1000000: return
        if CTRL and 0x40 <= kodowanie_znaku <= 0x7f: 자신.wysłać(bytes([kodowanie_znaku & 31])); return
        if kodowanie_znaku < 32: return
        if 자신.한글여부 and 자신.klawisz_modyfikujący & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.kanał_Klucz(chr(kodowanie_znaku), altgr=True): return
        interlinia_część = b'\x1b' if 자신.klawisz_modyfikujący & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not interlinia_część and 32<=kodowanie_znaku<127:
            dane_znakowe=chr(kodowanie_znaku).upper() if klawisz_SHIFT else chr(kodowanie_znaku)
            if 자신.한글조합기.kanał_Klucz(dane_znakowe): return
        자신.wysłać(interlinia_część + chr(kodowanie_znaku).encode('utf-8'))


class POŁĄCZ_Pulpit:
    def __init__(자신, Proces):
        자신.Proces=Proces; 자신.blokada_WARTOŚĆ=threading.Lock(); 자신.준비완료=False; 자신.interpretator_poleceń=False; 자신.시작화면=False; 자신.systemy_informacyjne_zamknięta=False

    def wysłać(자신, dane):
        if not dane or 자신.systemy_informacyjne_zamknięta: return
        with 자신.blokada_WARTOŚĆ:
            try: 자신.Proces.stdin.write(dane); 자신.Proces.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                dane=자신.Proces.stdout.read(4096)
                if not dane: break
                sys.stdout.buffer.write(dane); sys.stdout.buffer.flush()
                끝부분=(끝부분+dane)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); systemy_informacyjne_zamknięta=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,systemy_informacyjne_zamknięta,그림화면,종료됨)>=0:
                    자신.interpretator_poleceń=열림>max(systemy_informacyjne_zamknięta,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,systemy_informacyjne_zamknięta,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.wysłać(b'terminal\n')
        finally: 자신.systemy_informacyjne_zamknięta=True

    def klient(자신, klient, ścieżka_2):
        serwer_WARTOŚĆ=socket.socket(socket.AF_UNIX); serwer_WARTOŚĆ.settimeout(10); klient.settimeout(10)
        klawiatura_wpis=klawiatura(자신.wysłać,lambda 한글여부:자신.wysłać(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            serwer_WARTOŚĆ.connect(str(ścieżka_2))
            # stan_początkowy 협상은 순서대로 끝낸다. 이후 pozycja_wyjścia 가닥만 클라이언트에 쓴다.
            klient.sendall(PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,12))
            numer_wersji=PORÓWNAJ_WARTOŚĆ(klient,12)
            if numer_wersji not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            serwer_WARTOŚĆ.sendall(numer_wersji)
            towar_ILE_LICZB=PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,1);klient.sendall(towar_ILE_LICZB+PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,towar_ILE_LICZB[0]))
            Zabezpieczenia=PORÓWNAJ_WARTOŚĆ(klient,1)
            if Zabezpieczenia!=b'\x01': raise ValueError('unexpected security type')
            serwer_WARTOŚĆ.sendall(Zabezpieczenia)
            if numer_wersji==b'RFB 003.008\n':klient.sendall(PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,4))
            serwer_WARTOŚĆ.sendall(PORÓWNAJ_WARTOŚĆ(klient,1))
            초기값=PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,24)
            klient.sendall(초기값+PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klient.settimeout(None);serwer_WARTOŚĆ.settimeout(None)
            def produkt_wyjściowy():
                try:
                    while True:
                        obszar_WARTOŚĆ=PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,1)[0]
                        if obszar_WARTOŚĆ==0:
                            머리=PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,3);wpis_ILE_LICZB=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 zdalny_WARTOŚĆ 포인터의 중복을 피한다.
                            Ukryty_WARTOŚĆ=포인터지원
                            if Ukryty_WARTOŚĆ:klient.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klient.sendall(bytes([obszar_WARTOŚĆ])+머리)
                            for _ in range(wpis_ILE_LICZB):
                                prostokąt=PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,12);가로,gałąź_stanowisko,폭,wysokość_WARTOŚĆ,Encoding_WARTOŚĆ=struct.unpack('>HHHHi',prostokąt)
                                if Encoding_WARTOŚĆ!=0:raise ValueError('unexpected framebuffer encoding: '+str(Encoding_WARTOŚĆ))
                                klient.sendall(prostokąt)
                                남음=폭*wysokość_WARTOŚĆ*화소바이트
                                while 남음:
                                    dane=PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,min(남음,65536));klient.sendall(dane);남음-=len(dane)
                        elif obszar_WARTOŚĆ==1:
                            머리=PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,5);towar_ILE_LICZB=struct.unpack('>H',머리[3:])[0]
                            klient.sendall(bytes([obszar_WARTOŚĆ])+머리+PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,towar_ILE_LICZB*6))
                        elif obszar_WARTOŚĆ==2:klient.sendall(bytes([obszar_WARTOŚĆ]))
                        elif obszar_WARTOŚĆ==3:
                            머리=PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,7);towar_ILE_LICZB=struct.unpack('>I',머리[3:])[0]
                            if towar_ILE_LICZB>1048576:raise ValueError('server clipboard too large')
                            klient.sendall(bytes([obszar_WARTOŚĆ])+머리+PORÓWNAJ_WARTOŚĆ(serwer_WARTOŚĆ,towar_ILE_LICZB))
                        else:raise ValueError('unexpected RFB server message: '+str(obszar_WARTOŚĆ))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klient.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            pracownik=threading.Thread(target=produkt_wyjściowy,daemon=True);pracownik.start()
            while not 자신.systemy_informacyjne_zamknięta:
                obszar_WARTOŚĆ=PORÓWNAJ_WARTOŚĆ(klient,1)[0]
                if obszar_WARTOŚĆ==4:
                    tekst_podstawowy=PORÓWNAJ_WARTOŚĆ(klient,7); klawiatura_wpis.누름값(tekst_podstawowy[0]!=0,struct.unpack('>I',tekst_podstawowy[3:])[0]); continue
                if obszar_WARTOŚĆ==255:
                    tekst_podstawowy=PORÓWNAJ_WARTOŚĆ(klient,11)
                    if tekst_podstawowy[0]!=0: raise ValueError('unsupported QEMU input extension')
                    klawiatura_wpis.누름값(struct.unpack('>H',tekst_podstawowy[1:3])[0]!=0,struct.unpack('>I',tekst_podstawowy[3:7])[0]); continue
                if obszar_WARTOŚĆ==5:
                    tekst_podstawowy=PORÓWNAJ_WARTOŚĆ(klient,5); 단추들,współrzędna_X,Y_współrzędna=struct.unpack('>BHH',tekst_podstawowy)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: klawiatura_wpis.한글조합기.przekazywać_kompozycja()
                    if 눌림&1 and 자신.시작화면 and 64<=współrzędna_X<576 and 112<=Y_współrzędna<372:
                        WYSZUKAJ_INDEKS=(Y_współrzędna-112)//52
                        if (Y_współrzędna-112)%52<40 and WYSZUKAJ_INDEKS<5: 자신.wysłać(bytes([ord('1')+WYSZUKAJ_INDEKS]))
                    else: 자신.wysłać(bytes([30,1,단추들,współrzędna_X&255,współrzędna_X>>8,Y_współrzędna&255,Y_współrzędna>>8]))
                    continue
                if obszar_WARTOŚĆ==6:
                    tekst_podstawowy=PORÓWNAJ_WARTOŚĆ(klient,7); długość_WARTOŚĆ=struct.unpack('>i',tekst_podstawowy[3:])[0]
                    if abs(długość_WARTOŚĆ)>65536: raise ValueError('clipboard too large')
                    tekst=PORÓWNAJ_WARTOŚĆ(klient,abs(długość_WARTOŚĆ))
                    if długość_WARTOŚĆ>=0:
                        try: klawiatura_wpis.schowek_WARTOŚĆ=tekst.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: klawiatura_wpis.schowek_WARTOŚĆ=tekst.decode('latin-1').encode('utf-8')
                        klawiatura_wpis.schowek_WARTOŚĆ=klawiatura_wpis.schowek_WARTOŚĆ[:65536].decode('utf-8','ignore').encode('utf-8')
                    serwer_WARTOŚĆ.sendall(bytes([obszar_WARTOŚĆ])+tekst_podstawowy+tekst); continue
                if obszar_WARTOŚĆ==0:
                    tekst_podstawowy=PORÓWNAJ_WARTOŚĆ(klient,19)
                    if tekst_podstawowy[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=tekst_podstawowy[3]//8
                elif obszar_WARTOŚĆ==2:
                    tekst_podstawowy=PORÓWNAJ_WARTOŚĆ(klient,3); wpis_ILE_LICZB=struct.unpack('>H',tekst_podstawowy[1:])[0]
                    if wpis_ILE_LICZB>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(wpis_ILE_LICZB)+'i',PORÓWNAJ_WARTOŚĆ(klient,wpis_ILE_LICZB*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 wartość_domyślna Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    tekst_podstawowy=struct.pack('>BHi',0,1,0)
                elif obszar_WARTOŚĆ in (3,150): tekst_podstawowy=PORÓWNAJ_WARTOŚĆ(klient,9)
                elif obszar_WARTOŚĆ==248:
                    tekst_podstawowy=PORÓWNAJ_WARTOŚĆ(klient,8)
                    if tekst_podstawowy[7]>64: raise ValueError('fence too large')
                    tekst_podstawowy+=PORÓWNAJ_WARTOŚĆ(klient,tekst_podstawowy[7])
                elif obszar_WARTOŚĆ==250: tekst_podstawowy=PORÓWNAJ_WARTOŚĆ(klient,3)
                elif obszar_WARTOŚĆ==251:
                    tekst_podstawowy=PORÓWNAJ_WARTOŚĆ(klient,7)
                    if tekst_podstawowy[5]>16: raise ValueError('too many screens')
                    tekst_podstawowy+=PORÓWNAJ_WARTOŚĆ(klient,tekst_podstawowy[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(obszar_WARTOŚĆ))
                serwer_WARTOŚĆ.sendall(bytes([obszar_WARTOŚĆ])+tekst_podstawowy)
        except (OSError,EOFError,ValueError) as błąd:
            if str(błąd): print('VNC client:',błąd,file=sys.stderr,flush=True)
        finally:
            for gniazdo_WARTOŚĆ in (klient,serwer_WARTOŚĆ):
                try: gniazdo_WARTOŚĆ.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                gniazdo_WARTOŚĆ.close()


def przebieg_Pulpit(numer_portu=5902, sieć=False, transfer_plików_numer_portu=2121, 전달규칙들=(), rozdzielczość_WARTOŚĆ=(640, 480), gość_ADRES=None, host_ADRES='127.0.0.1'):
    with ExitStack() as Zasoby, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        mostek_wpis = None
        if sieć:
            from mostek_3de4fe3a import mostek_3de4fe3a
            mostek_wpis = Zasoby.enter_context(mostek_3de4fe3a(transfer_plików_numer_portu, 전달규칙들, gość_ADRES=gość_ADRES, host_ADRES=host_ADRES))
        ścieżka_2=Path(작업경로)/'display.sock'
        with socket.socket() as odbierać_port:
            odbierać_port.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            odbierać_port.bind(('127.0.0.1',numer_portu)); odbierać_port.listen(1); odbierać_port.settimeout(.2)
            원격화면접속번호=odbierać_port.getsockname()[1]
            if mostek_wpis and (원격화면접속번호==transfer_plików_numer_portu or 50000<=원격화면접속번호<=50007 or any(sieć_ABI=='tcp' and host==원격화면접속번호 for sieć_ABI,host,_ in mostek_wpis.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proces=subprocess.Popen(polecenie(rozdzielczość_WARTOŚĆ)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ścieżka_2)]+(mostek_wpis.전달인수() if mostek_wpis else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            mostek=POŁĄCZ_Pulpit(Proces); Czytnik=threading.Thread(target=mostek.직렬입출력,daemon=True); Czytnik.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(odbierać_port.getsockname()[1]),flush=True)
            if mostek_wpis: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(host_ADRES,transfer_plików_numer_portu),flush=True)
            def przerwać(sygnał_identyfikator,wykonanie_kadr): raise KeyboardInterrupt()
            Wstecz=signal.signal(signal.SIGTERM,przerwać)
            przetwarzanie_zadanie=None; 가로채기됨=False
            try:
                while Proces.poll() is None:
                    try: klient,_=odbierać_port.accept()
                    except socket.timeout: continue
                    if przetwarzanie_zadanie is not None and przetwarzanie_zadanie.is_alive(): klient.close(); continue
                    if not ścieżka_2.exists(): klient.close(); continue
                    przetwarzanie_zadanie=threading.Thread(target=mostek.klient,args=(klient,ścieżka_2),daemon=True); przetwarzanie_zadanie.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                mostek.systemy_informacyjne_zamknięta=True
                if mostek_wpis: mostek_wpis.Wstrzymaj_konkurs.set()
                if Proces.poll() is None:
                    Proces.terminate()
                    try: Proces.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
                Czytnik.join(timeout=2); Proces.stdin.close(); Proces.stdout.close(); signal.signal(signal.SIGTERM,Wstecz)
            if mostek_wpis and mostek_wpis.błąd: raise RuntimeError('network bridge: '+mostek_wpis.błąd)
            return 0 if 가로채기됨 else Proces.returncode


if __name__=='__main__':
    from Wykonaj_polecenie import 해상도읽기
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    argument_TABLICA=parser.parse_args()
    if argument_TABLICA.forward and not argument_TABLICA.network: parser.error('--forward requires --network')
    raise SystemExit(przebieg_Pulpit(argument_TABLICA.port,sieć=argument_TABLICA.network,transfer_plików_numer_portu=argument_TABLICA.ftp_port,전달규칙들=argument_TABLICA.forward,rozdzielczość_WARTOŚĆ=argument_TABLICA.resolution))
