#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Avain_ARVO 입력은 oma ydin_ARVO UART로 전달한다. localhost 전용, 단일 ohjain_ARVO 클라이언트.
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
from Suorita_komento import komento
from local_input import create


def VERTAA_ARVO(vastake_ARVO, Koko):
    data = bytearray()
    while len(data) < Koko:
        조각 = vastake_ARVO.recv(Koko - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class näppäimistö:
    def __init__(자신, lähettää, 입력방식알림=None):
        자신.바이트전송 = lähettää; 자신.VAIHTO_CTRL_tai_ALT_näppäin = set(); 자신.leikepöytä_ARVO = b''
        자신.한글조합기 = create(lähettää, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.MUUTA_Avain = set()
        자신.UNICODE_syöte = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def lähettää(자신, data):
        자신.한글조합기.vahvistaa_muutokset_kokoonpano()
        자신.바이트전송(data)

    def MUUTA_tila(자신):
        자신.한글조합기.vahvistaa_muutokset_kokoonpano(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Avain_symboli):
        if Avain_symboli in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.VAIHTO_CTRL_tai_ALT_näppäin.add(Avain_symboli)
            else: 자신.VAIHTO_CTRL_tai_ALT_näppäin.discard(Avain_symboli)
            return
        if not 누르는중:
            자신.MUUTA_Avain.discard(Avain_symboli)
            return
        CTRL = bool(자신.VAIHTO_CTRL_tai_ALT_näppäin & {0xffe3, 0xffe4})
        VAIHTONÄPPÄIN = bool(자신.VAIHTO_CTRL_tai_ALT_näppäin & {0xffe1, 0xffe2})
        if CTRL and VAIHTONÄPPÄIN and Avain_symboli in (ord('u'),ord('U')):
            자신.한글조합기.vahvistaa_muutokset_kokoonpano(); 자신.UNICODE_syöte = ''; return
        if 자신.UNICODE_syöte is not None:
            if Avain_symboli in (32,0xff0d):
                try:
                    ARVO=int(자신.UNICODE_syöte,16)
                    if 32<=ARVO<=0x10ffff and not 0xd800<=ARVO<=0xdfff: 자신.lähettää(chr(ARVO).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_syöte=None
            elif Avain_symboli==0xff1b: 자신.UNICODE_syöte=None
            elif Avain_symboli==0xff08: 자신.UNICODE_syöte=자신.UNICODE_syöte[:-1]
            elif Avain_symboli<128 and chr(Avain_symboli) in '0123456789abcdefABCDEF' and len(자신.UNICODE_syöte)<6: 자신.UNICODE_syöte+=chr(Avain_symboli)
            return
        if Avain_symboli in (0xff31,0xffc6) or Avain_symboli==32 and VAIHTONÄPPÄIN and not CTRL:
            if Avain_symboli not in 자신.MUUTA_Avain: 자신.MUUTA_tila()
            자신.MUUTA_Avain.add(Avain_symboli)
            return
        if Avain_symboli==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and VAIHTONÄPPÄIN and Avain_symboli in (ord('t'),ord('T')):
            자신.lähettää(bytes([30,2,1,0,0,0,0])); return
        if Avain_symboli==0xffc3: 자신.lähettää(bytes([30,2,2,0,0,0,0])); return
        if Avain_symboli==0xffc9: 자신.lähettää(bytes([30,2,3,0,0,0,0])); return
        if CTRL and VAIHTONÄPPÄIN and Avain_symboli in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.lähettää(자신.leikepöytä_ARVO); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Avain_symboli in 특수글쇠: 자신.lähettää(특수글쇠[Avain_symboli]); return
        merkkikoodaus = Avain_symboli & 0xffffff if Avain_symboli & 0xff000000 == 0x01000000 else Avain_symboli
        if merkkikoodaus > 0x10ffff or 0xd800 <= merkkikoodaus <= 0xdfff or Avain_symboli >= 0xff00 and Avain_symboli < 0x1000000: return
        if CTRL and 0x40 <= merkkikoodaus <= 0x7f: 자신.lähettää(bytes([merkkikoodaus & 31])); return
        if merkkikoodaus < 32: return
        if 자신.한글여부 and 자신.VAIHTO_CTRL_tai_ALT_näppäin & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.syöte_Avain(chr(merkkikoodaus), altgr=True): return
        앞부분 = b'\x1b' if 자신.VAIHTO_CTRL_tai_ALT_näppäin & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=merkkikoodaus<127:
            merkkitiedot=chr(merkkikoodaus).upper() if VAIHTONÄPPÄIN else chr(merkkikoodaus)
            if 자신.한글조합기.syöte_Avain(merkkitiedot): return
        자신.lähettää(앞부분 + chr(merkkikoodaus).encode('utf-8'))


class YHDISTÄ_työpöytä:
    def __init__(자신, Prosessi):
        자신.Prosessi=Prosessi; 자신.lukita_ARVO=threading.Lock(); 자신.준비완료=False; 자신.komentotulkki=False; 자신.시작화면=False; 자신.tietojärjestelmät_suljettu=False

    def lähettää(자신, data):
        if not data or 자신.tietojärjestelmät_suljettu: return
        with 자신.lukita_ARVO:
            try: 자신.Prosessi.stdin.write(data); 자신.Prosessi.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.Prosessi.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); tietojärjestelmät_suljettu=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,tietojärjestelmät_suljettu,그림화면,종료됨)>=0:
                    자신.komentotulkki=열림>max(tietojärjestelmät_suljettu,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,tietojärjestelmät_suljettu,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.lähettää(b'terminal\n')
        finally: 자신.tietojärjestelmät_suljettu=True

    def asiakas(자신, asiakas, polku_2):
        palvelin_ARVO=socket.socket(socket.AF_UNIX); palvelin_ARVO.settimeout(10); asiakas.settimeout(10)
        näppäimistö_merkintä=näppäimistö(자신.lähettää,lambda 한글여부:자신.lähettää(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            palvelin_ARVO.connect(str(polku_2))
            # alkutila 협상은 순서대로 끝낸다. 이후 tulostuspaikka 가닥만 클라이언트에 쓴다.
            asiakas.sendall(VERTAA_ARVO(palvelin_ARVO,12))
            versionumero=VERTAA_ARVO(asiakas,12)
            if versionumero not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            palvelin_ARVO.sendall(versionumero)
            kohde_LASKE=VERTAA_ARVO(palvelin_ARVO,1);asiakas.sendall(kohde_LASKE+VERTAA_ARVO(palvelin_ARVO,kohde_LASKE[0]))
            suojaus=VERTAA_ARVO(asiakas,1)
            if suojaus!=b'\x01': raise ValueError('unexpected security type')
            palvelin_ARVO.sendall(suojaus)
            if versionumero==b'RFB 003.008\n':asiakas.sendall(VERTAA_ARVO(palvelin_ARVO,4))
            palvelin_ARVO.sendall(VERTAA_ARVO(asiakas,1))
            초기값=VERTAA_ARVO(palvelin_ARVO,24)
            asiakas.sendall(초기값+VERTAA_ARVO(palvelin_ARVO,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            asiakas.settimeout(None);palvelin_ARVO.settimeout(None)
            def tulos():
                try:
                    while True:
                        alue_ARVO=VERTAA_ARVO(palvelin_ARVO,1)[0]
                        if alue_ARVO==0:
                            머리=VERTAA_ARVO(palvelin_ARVO,3);merkintä_LASKE=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 etä_ARVO 포인터의 중복을 피한다.
                            Piilotettu_ARVO=포인터지원
                            if Piilotettu_ARVO:asiakas.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            asiakas.sendall(bytes([alue_ARVO])+머리)
                            for _ in range(merkintä_LASKE):
                                suorakulmio=VERTAA_ARVO(palvelin_ARVO,12);가로,toimiala_toimi,폭,높이,koodaus_ARVO=struct.unpack('>HHHHi',suorakulmio)
                                if koodaus_ARVO!=0:raise ValueError('unexpected framebuffer encoding: '+str(koodaus_ARVO))
                                asiakas.sendall(suorakulmio)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=VERTAA_ARVO(palvelin_ARVO,min(남음,65536));asiakas.sendall(data);남음-=len(data)
                        elif alue_ARVO==1:
                            머리=VERTAA_ARVO(palvelin_ARVO,5);kohde_LASKE=struct.unpack('>H',머리[3:])[0]
                            asiakas.sendall(bytes([alue_ARVO])+머리+VERTAA_ARVO(palvelin_ARVO,kohde_LASKE*6))
                        elif alue_ARVO==2:asiakas.sendall(bytes([alue_ARVO]))
                        elif alue_ARVO==3:
                            머리=VERTAA_ARVO(palvelin_ARVO,7);kohde_LASKE=struct.unpack('>I',머리[3:])[0]
                            if kohde_LASKE>1048576:raise ValueError('server clipboard too large')
                            asiakas.sendall(bytes([alue_ARVO])+머리+VERTAA_ARVO(palvelin_ARVO,kohde_LASKE))
                        else:raise ValueError('unexpected RFB server message: '+str(alue_ARVO))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:asiakas.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            työntekijä=threading.Thread(target=tulos,daemon=True);työntekijä.start()
            while not 자신.tietojärjestelmät_suljettu:
                alue_ARVO=VERTAA_ARVO(asiakas,1)[0]
                if alue_ARVO==4:
                    leipäteksti=VERTAA_ARVO(asiakas,7); näppäimistö_merkintä.누름값(leipäteksti[0]!=0,struct.unpack('>I',leipäteksti[3:])[0]); continue
                if alue_ARVO==255:
                    leipäteksti=VERTAA_ARVO(asiakas,11)
                    if leipäteksti[0]!=0: raise ValueError('unsupported QEMU input extension')
                    näppäimistö_merkintä.누름값(struct.unpack('>H',leipäteksti[1:3])[0]!=0,struct.unpack('>I',leipäteksti[3:7])[0]); continue
                if alue_ARVO==5:
                    leipäteksti=VERTAA_ARVO(asiakas,5); 단추들,x_koordinaatti,Y_koordinaatti=struct.unpack('>BHH',leipäteksti)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: näppäimistö_merkintä.한글조합기.vahvistaa_muutokset_kokoonpano()
                    if 눌림&1 and 자신.시작화면 and 64<=x_koordinaatti<576 and 112<=Y_koordinaatti<372:
                        HAKU_INDEKSI=(Y_koordinaatti-112)//52
                        if (Y_koordinaatti-112)%52<40 and HAKU_INDEKSI<5: 자신.lähettää(bytes([ord('1')+HAKU_INDEKSI]))
                    else: 자신.lähettää(bytes([30,1,단추들,x_koordinaatti&255,x_koordinaatti>>8,Y_koordinaatti&255,Y_koordinaatti>>8]))
                    continue
                if alue_ARVO==6:
                    leipäteksti=VERTAA_ARVO(asiakas,7); kesto_ARVO=struct.unpack('>i',leipäteksti[3:])[0]
                    if abs(kesto_ARVO)>65536: raise ValueError('clipboard too large')
                    teksti=VERTAA_ARVO(asiakas,abs(kesto_ARVO))
                    if kesto_ARVO>=0:
                        try: näppäimistö_merkintä.leikepöytä_ARVO=teksti.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: näppäimistö_merkintä.leikepöytä_ARVO=teksti.decode('latin-1').encode('utf-8')
                        näppäimistö_merkintä.leikepöytä_ARVO=näppäimistö_merkintä.leikepöytä_ARVO[:65536].decode('utf-8','ignore').encode('utf-8')
                    palvelin_ARVO.sendall(bytes([alue_ARVO])+leipäteksti+teksti); continue
                if alue_ARVO==0:
                    leipäteksti=VERTAA_ARVO(asiakas,19)
                    if leipäteksti[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=leipäteksti[3]//8
                elif alue_ARVO==2:
                    leipäteksti=VERTAA_ARVO(asiakas,3); merkintä_LASKE=struct.unpack('>H',leipäteksti[1:])[0]
                    if merkintä_LASKE>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(merkintä_LASKE)+'i',VERTAA_ARVO(asiakas,merkintä_LASKE*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 oletusarvo Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    leipäteksti=struct.pack('>BHi',0,1,0)
                elif alue_ARVO in (3,150): leipäteksti=VERTAA_ARVO(asiakas,9)
                elif alue_ARVO==248:
                    leipäteksti=VERTAA_ARVO(asiakas,8)
                    if leipäteksti[7]>64: raise ValueError('fence too large')
                    leipäteksti+=VERTAA_ARVO(asiakas,leipäteksti[7])
                elif alue_ARVO==250: leipäteksti=VERTAA_ARVO(asiakas,3)
                elif alue_ARVO==251:
                    leipäteksti=VERTAA_ARVO(asiakas,7)
                    if leipäteksti[5]>16: raise ValueError('too many screens')
                    leipäteksti+=VERTAA_ARVO(asiakas,leipäteksti[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(alue_ARVO))
                palvelin_ARVO.sendall(bytes([alue_ARVO])+leipäteksti)
        except (OSError,EOFError,ValueError) as VIRHE:
            if str(VIRHE): print('VNC client:',VIRHE,file=sys.stderr,flush=True)
        finally:
            for vastake_ARVO in (asiakas,palvelin_ARVO):
                try: vastake_ARVO.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                vastake_ARVO.close()


def suorittaa_työpöytä(portin_numero=5902, verkko=False, tiedostonsiirto_portin_numero=2121, 전달규칙들=(), tarkkuus_ARVO=(640, 480), vieras_OSOITE=None, isäntä_OSOITE='127.0.0.1'):
    with ExitStack() as Resurssit, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        silta_merkintä = None
        if verkko:
            from silta_3de4fe3a import silta_3de4fe3a
            silta_merkintä = Resurssit.enter_context(silta_3de4fe3a(tiedostonsiirto_portin_numero, 전달규칙들, vieras_OSOITE=vieras_OSOITE, isäntä_OSOITE=isäntä_OSOITE))
        polku_2=Path(작업경로)/'display.sock'
        with socket.socket() as saada_portti:
            saada_portti.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            saada_portti.bind(('127.0.0.1',portin_numero)); saada_portti.listen(1); saada_portti.settimeout(.2)
            원격화면접속번호=saada_portti.getsockname()[1]
            if silta_merkintä and (원격화면접속번호==tiedostonsiirto_portin_numero or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and isäntä==원격화면접속번호 for 통신규약,isäntä,_ in silta_merkintä.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Prosessi=subprocess.Popen(komento(tarkkuus_ARVO)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(polku_2)]+(silta_merkintä.전달인수() if silta_merkintä else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            silta=YHDISTÄ_työpöytä(Prosessi); Lukija=threading.Thread(target=silta.직렬입출력,daemon=True); Lukija.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(saada_portti.getsockname()[1]),flush=True)
            if silta_merkintä: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(isäntä_OSOITE,tiedostonsiirto_portin_numero),flush=True)
            def lopeta(ilmoitus_numero,suoritus_kuva): raise KeyboardInterrupt()
            Edellinen=signal.signal(signal.SIGTERM,lopeta)
            käsittely_tehtävä=None; 가로채기됨=False
            try:
                while Prosessi.poll() is None:
                    try: asiakas,_=saada_portti.accept()
                    except socket.timeout: continue
                    if käsittely_tehtävä is not None and käsittely_tehtävä.is_alive(): asiakas.close(); continue
                    if not polku_2.exists(): asiakas.close(); continue
                    käsittely_tehtävä=threading.Thread(target=silta.asiakas,args=(asiakas,polku_2),daemon=True); käsittely_tehtävä.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                silta.tietojärjestelmät_suljettu=True
                if silta_merkintä: silta_merkintä.Keskeytä_tapahtuma.set()
                if Prosessi.poll() is None:
                    Prosessi.terminate()
                    try: Prosessi.wait(timeout=5)
                    except subprocess.TimeoutExpired: Prosessi.kill(); Prosessi.wait()
                Lukija.join(timeout=2); Prosessi.stdin.close(); Prosessi.stdout.close(); signal.signal(signal.SIGTERM,Edellinen)
            if silta_merkintä and silta_merkintä.VIRHE: raise RuntimeError('network bridge: '+silta_merkintä.VIRHE)
            return 0 if 가로채기됨 else Prosessi.returncode


if __name__=='__main__':
    from Suorita_komento import lukea_tarkkuus
    jäsennin=argparse.ArgumentParser(description=__doc__); jäsennin.add_argument('--port',type=int,default=5902)
    jäsennin.add_argument('--resolution',type=lukea_tarkkuus,default=(640,480))
    jäsennin.add_argument('--network',action='store_true'); jäsennin.add_argument('--ftp-port',type=int,default=2121)
    jäsennin.add_argument('--forward',action='append',default=[])
    argumentti_MATRIISI=jäsennin.parse_args()
    if argumentti_MATRIISI.forward and not argumentti_MATRIISI.network: jäsennin.error('--forward requires --network')
    raise SystemExit(suorittaa_työpöytä(argumentti_MATRIISI.port,verkko=argumentti_MATRIISI.network,tiedostonsiirto_portin_numero=argumentti_MATRIISI.ftp_port,전달규칙들=argumentti_MATRIISI.forward,tarkkuus_ARVO=argumentti_MATRIISI.resolution))
