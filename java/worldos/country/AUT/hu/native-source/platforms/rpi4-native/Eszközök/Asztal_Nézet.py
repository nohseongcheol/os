#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Kulcs_ÉRTÉK 입력은 saját kernel_ÉRTÉK UART로 전달한다. localhost 전용, 단일 vezérlő_ÉRTÉK 클라이언트.
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
from végrehajt_parancs import Parancs
from local_input import create


def AZONOS_ÉRTÉK(szoftvercsatorna_ÉRTÉK, Méret):
    adat = bytearray()
    while len(adat) < Méret:
        조각 = szoftvercsatorna_ÉRTÉK.recv(Méret - len(adat))
        if not 조각: raise EOFError()
        adat.extend(조각)
    return bytes(adat)


class billentyűzet:
    def __init__(자신, küld, 입력방식알림=None):
        자신.바이트전송 = küld; 자신.váltóbillentyű = set(); 자신.vágólap_ÉRTÉK = b''
        자신.한글조합기 = create(küld, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.vált_Kulcs = set()
        자신.UNICODE_bevitel = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def küld(자신, adat):
        자신.한글조합기.véglegesít_rész_egész()
        자신.바이트전송(adat)

    def vált_mód(자신):
        자신.한글조합기.véglegesít_rész_egész(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Kulcs_szimbólum):
        if Kulcs_szimbólum in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.váltóbillentyű.add(Kulcs_szimbólum)
            else: 자신.váltóbillentyű.discard(Kulcs_szimbólum)
            return
        if not 누르는중:
            자신.vált_Kulcs.discard(Kulcs_szimbólum)
            return
        CTRL = bool(자신.váltóbillentyű & {0xffe3, 0xffe4})
        SHIFT_billentyű = bool(자신.váltóbillentyű & {0xffe1, 0xffe2})
        if CTRL and SHIFT_billentyű and Kulcs_szimbólum in (ord('u'),ord('U')):
            자신.한글조합기.véglegesít_rész_egész(); 자신.UNICODE_bevitel = ''; return
        if 자신.UNICODE_bevitel is not None:
            if Kulcs_szimbólum in (32,0xff0d):
                try:
                    ÉRTÉK=int(자신.UNICODE_bevitel,16)
                    if 32<=ÉRTÉK<=0x10ffff and not 0xd800<=ÉRTÉK<=0xdfff: 자신.küld(chr(ÉRTÉK).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_bevitel=None
            elif Kulcs_szimbólum==0xff1b: 자신.UNICODE_bevitel=None
            elif Kulcs_szimbólum==0xff08: 자신.UNICODE_bevitel=자신.UNICODE_bevitel[:-1]
            elif Kulcs_szimbólum<128 and chr(Kulcs_szimbólum) in '0123456789abcdefABCDEF' and len(자신.UNICODE_bevitel)<6: 자신.UNICODE_bevitel+=chr(Kulcs_szimbólum)
            return
        if Kulcs_szimbólum in (0xff31,0xffc6) or Kulcs_szimbólum==32 and SHIFT_billentyű and not CTRL:
            if Kulcs_szimbólum not in 자신.vált_Kulcs: 자신.vált_mód()
            자신.vált_Kulcs.add(Kulcs_szimbólum)
            return
        if Kulcs_szimbólum==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_billentyű and Kulcs_szimbólum in (ord('t'),ord('T')):
            자신.küld(bytes([30,2,1,0,0,0,0])); return
        if Kulcs_szimbólum==0xffc3: 자신.küld(bytes([30,2,2,0,0,0,0])); return
        if Kulcs_szimbólum==0xffc9: 자신.küld(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_billentyű and Kulcs_szimbólum in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.küld(자신.vágólap_ÉRTÉK); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Kulcs_szimbólum in 특수글쇠: 자신.küld(특수글쇠[Kulcs_szimbólum]); return
        karakterkódolás = Kulcs_szimbólum & 0xffffff if Kulcs_szimbólum & 0xff000000 == 0x01000000 else Kulcs_szimbólum
        if karakterkódolás > 0x10ffff or 0xd800 <= karakterkódolás <= 0xdfff or Kulcs_szimbólum >= 0xff00 and Kulcs_szimbólum < 0x1000000: return
        if CTRL and 0x40 <= karakterkódolás <= 0x7f: 자신.küld(bytes([karakterkódolás & 31])); return
        if karakterkódolás < 32: return
        if 자신.한글여부 and 자신.váltóbillentyű & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.csatorna_Kulcs(chr(karakterkódolás), altgr=True): return
        sorköz_rész = b'\x1b' if 자신.váltóbillentyű & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not sorköz_rész and 32<=karakterkódolás<127:
            karakteres_adat=chr(karakterkódolás).upper() if SHIFT_billentyű else chr(karakterkódolás)
            if 자신.한글조합기.csatorna_Kulcs(karakteres_adat): return
        자신.küld(sorköz_rész + chr(karakterkódolás).encode('utf-8'))


class KAPCSOLAT_Asztal:
    def __init__(자신, Folyamat):
        자신.Folyamat=Folyamat; 자신.lezár_ÉRTÉK=threading.Lock(); 자신.준비완료=False; 자신.Terminál=False; 자신.시작화면=False; 자신.informatikai_részleg_lezárt=False

    def küld(자신, adat):
        if not adat or 자신.informatikai_részleg_lezárt: return
        with 자신.lezár_ÉRTÉK:
            try: 자신.Folyamat.stdin.write(adat); 자신.Folyamat.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                adat=자신.Folyamat.stdout.read(4096)
                if not adat: break
                sys.stdout.buffer.write(adat); sys.stdout.buffer.flush()
                끝부분=(끝부분+adat)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); informatikai_részleg_lezárt=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,informatikai_részleg_lezárt,그림화면,종료됨)>=0:
                    자신.Terminál=열림>max(informatikai_részleg_lezárt,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,informatikai_részleg_lezárt,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.küld(b'terminal\n')
        finally: 자신.informatikai_részleg_lezárt=True

    def kliens(자신, kliens, ÚTVONAL):
        kiszolgáló_ÉRTÉK=socket.socket(socket.AF_UNIX); kiszolgáló_ÉRTÉK.settimeout(10); kliens.settimeout(10)
        billentyűzet_bejegyzés=billentyűzet(자신.küld,lambda 한글여부:자신.küld(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            kiszolgáló_ÉRTÉK.connect(str(ÚTVONAL))
            # kiinduló_állapot 협상은 순서대로 끝낸다. 이후 Kimenet 가닥만 클라이언트에 쓴다.
            kliens.sendall(AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,12))
            verziószám=AZONOS_ÉRTÉK(kliens,12)
            if verziószám not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            kiszolgáló_ÉRTÉK.sendall(verziószám)
            cikk_DARAB=AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,1);kliens.sendall(cikk_DARAB+AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,cikk_DARAB[0]))
            Biztonság=AZONOS_ÉRTÉK(kliens,1)
            if Biztonság!=b'\x01': raise ValueError('unexpected security type')
            kiszolgáló_ÉRTÉK.sendall(Biztonság)
            if verziószám==b'RFB 003.008\n':kliens.sendall(AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,4))
            kiszolgáló_ÉRTÉK.sendall(AZONOS_ÉRTÉK(kliens,1))
            초기값=AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,24)
            kliens.sendall(초기값+AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            kliens.settimeout(None);kiszolgáló_ÉRTÉK.settimeout(None)
            def kimenet():
                try:
                    while True:
                        terület_ÉRTÉK=AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,1)[0]
                        if terület_ÉRTÉK==0:
                            머리=AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,3);bejegyzés_DARAB=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 távoli_ÉRTÉK 포인터의 중복을 피한다.
                            Rejtett_ÉRTÉK=포인터지원
                            if Rejtett_ÉRTÉK:kliens.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            kliens.sendall(bytes([terület_ÉRTÉK])+머리)
                            for _ in range(bejegyzés_DARAB):
                                téglalap=AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,12);가로,szektor_pozíció,폭,높이,kódolás_ÉRTÉK=struct.unpack('>HHHHi',téglalap)
                                if kódolás_ÉRTÉK!=0:raise ValueError('unexpected framebuffer encoding: '+str(kódolás_ÉRTÉK))
                                kliens.sendall(téglalap)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    adat=AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,min(남음,65536));kliens.sendall(adat);남음-=len(adat)
                        elif terület_ÉRTÉK==1:
                            머리=AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,5);cikk_DARAB=struct.unpack('>H',머리[3:])[0]
                            kliens.sendall(bytes([terület_ÉRTÉK])+머리+AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,cikk_DARAB*6))
                        elif terület_ÉRTÉK==2:kliens.sendall(bytes([terület_ÉRTÉK]))
                        elif terület_ÉRTÉK==3:
                            머리=AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,7);cikk_DARAB=struct.unpack('>I',머리[3:])[0]
                            if cikk_DARAB>1048576:raise ValueError('server clipboard too large')
                            kliens.sendall(bytes([terület_ÉRTÉK])+머리+AZONOS_ÉRTÉK(kiszolgáló_ÉRTÉK,cikk_DARAB))
                        else:raise ValueError('unexpected RFB server message: '+str(terület_ÉRTÉK))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:kliens.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            dolgozó=threading.Thread(target=kimenet,daemon=True);dolgozó.start()
            while not 자신.informatikai_részleg_lezárt:
                terület_ÉRTÉK=AZONOS_ÉRTÉK(kliens,1)[0]
                if terület_ÉRTÉK==4:
                    törzsszöveg=AZONOS_ÉRTÉK(kliens,7); billentyűzet_bejegyzés.누름값(törzsszöveg[0]!=0,struct.unpack('>I',törzsszöveg[3:])[0]); continue
                if terület_ÉRTÉK==255:
                    törzsszöveg=AZONOS_ÉRTÉK(kliens,11)
                    if törzsszöveg[0]!=0: raise ValueError('unsupported QEMU input extension')
                    billentyűzet_bejegyzés.누름값(struct.unpack('>H',törzsszöveg[1:3])[0]!=0,struct.unpack('>I',törzsszöveg[3:7])[0]); continue
                if terület_ÉRTÉK==5:
                    törzsszöveg=AZONOS_ÉRTÉK(kliens,5); 단추들,x_koordináta,Y_koordináta=struct.unpack('>BHH',törzsszöveg)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: billentyűzet_bejegyzés.한글조합기.véglegesít_rész_egész()
                    if 눌림&1 and 자신.시작화면 and 64<=x_koordináta<576 and 112<=Y_koordináta<372:
                        KERES_INDEX=(Y_koordináta-112)//52
                        if (Y_koordináta-112)%52<40 and KERES_INDEX<5: 자신.küld(bytes([ord('1')+KERES_INDEX]))
                    else: 자신.küld(bytes([30,1,단추들,x_koordináta&255,x_koordináta>>8,Y_koordináta&255,Y_koordináta>>8]))
                    continue
                if terület_ÉRTÉK==6:
                    törzsszöveg=AZONOS_ÉRTÉK(kliens,7); hossz_ÉRTÉK=struct.unpack('>i',törzsszöveg[3:])[0]
                    if abs(hossz_ÉRTÉK)>65536: raise ValueError('clipboard too large')
                    Szöveg=AZONOS_ÉRTÉK(kliens,abs(hossz_ÉRTÉK))
                    if hossz_ÉRTÉK>=0:
                        try: billentyűzet_bejegyzés.vágólap_ÉRTÉK=Szöveg.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: billentyűzet_bejegyzés.vágólap_ÉRTÉK=Szöveg.decode('latin-1').encode('utf-8')
                        billentyűzet_bejegyzés.vágólap_ÉRTÉK=billentyűzet_bejegyzés.vágólap_ÉRTÉK[:65536].decode('utf-8','ignore').encode('utf-8')
                    kiszolgáló_ÉRTÉK.sendall(bytes([terület_ÉRTÉK])+törzsszöveg+Szöveg); continue
                if terület_ÉRTÉK==0:
                    törzsszöveg=AZONOS_ÉRTÉK(kliens,19)
                    if törzsszöveg[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=törzsszöveg[3]//8
                elif terület_ÉRTÉK==2:
                    törzsszöveg=AZONOS_ÉRTÉK(kliens,3); bejegyzés_DARAB=struct.unpack('>H',törzsszöveg[1:])[0]
                    if bejegyzés_DARAB>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(bejegyzés_DARAB)+'i',AZONOS_ÉRTÉK(kliens,bejegyzés_DARAB*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 alapértelmezett_érték Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    törzsszöveg=struct.pack('>BHi',0,1,0)
                elif terület_ÉRTÉK in (3,150): törzsszöveg=AZONOS_ÉRTÉK(kliens,9)
                elif terület_ÉRTÉK==248:
                    törzsszöveg=AZONOS_ÉRTÉK(kliens,8)
                    if törzsszöveg[7]>64: raise ValueError('fence too large')
                    törzsszöveg+=AZONOS_ÉRTÉK(kliens,törzsszöveg[7])
                elif terület_ÉRTÉK==250: törzsszöveg=AZONOS_ÉRTÉK(kliens,3)
                elif terület_ÉRTÉK==251:
                    törzsszöveg=AZONOS_ÉRTÉK(kliens,7)
                    if törzsszöveg[5]>16: raise ValueError('too many screens')
                    törzsszöveg+=AZONOS_ÉRTÉK(kliens,törzsszöveg[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(terület_ÉRTÉK))
                kiszolgáló_ÉRTÉK.sendall(bytes([terület_ÉRTÉK])+törzsszöveg)
        except (OSError,EOFError,ValueError) as HIBA:
            if str(HIBA): print('VNC client:',HIBA,file=sys.stderr,flush=True)
        finally:
            for szoftvercsatorna_ÉRTÉK in (kliens,kiszolgáló_ÉRTÉK):
                try: szoftvercsatorna_ÉRTÉK.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                szoftvercsatorna_ÉRTÉK.close()


def futtat_Asztal(portszám=5902, hálózat=False, fájlátvitel_portszám=2121, 전달규칙들=(), felbontás_ÉRTÉK=(640, 480), vendég_CÍM=None, gazda_CÍM='127.0.0.1'):
    with ExitStack() as Források, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        híd_bejegyzés = None
        if hálózat:
            from híd_3de4fe3a import híd_3de4fe3a
            híd_bejegyzés = Források.enter_context(híd_3de4fe3a(fájlátvitel_portszám, 전달규칙들, vendég_CÍM=vendég_CÍM, gazda_CÍM=gazda_CÍM))
        ÚTVONAL=Path(작업경로)/'display.sock'
        with socket.socket() as fogad_port:
            fogad_port.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            fogad_port.bind(('127.0.0.1',portszám)); fogad_port.listen(1); fogad_port.settimeout(.2)
            원격화면접속번호=fogad_port.getsockname()[1]
            if híd_bejegyzés and (원격화면접속번호==fájlátvitel_portszám or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and gazda==원격화면접속번호 for 통신규약,gazda,_ in híd_bejegyzés.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Folyamat=subprocess.Popen(Parancs(felbontás_ÉRTÉK)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ÚTVONAL)]+(híd_bejegyzés.전달인수() if híd_bejegyzés else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            híd=KAPCSOLAT_Asztal(Folyamat); Olvasó=threading.Thread(target=híd.직렬입출력,daemon=True); Olvasó.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(fogad_port.getsockname()[1]),flush=True)
            if híd_bejegyzés: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(gazda_CÍM,fájlátvitel_portszám),flush=True)
            def leállít(jelzés_szám,végrehajtás_doboz): raise KeyboardInterrupt()
            Előző=signal.signal(signal.SIGTERM,leállít)
            feldolgozás_teendő=None; 가로채기됨=False
            try:
                while Folyamat.poll() is None:
                    try: kliens,_=fogad_port.accept()
                    except socket.timeout: continue
                    if feldolgozás_teendő is not None and feldolgozás_teendő.is_alive(): kliens.close(); continue
                    if not ÚTVONAL.exists(): kliens.close(); continue
                    feldolgozás_teendő=threading.Thread(target=híd.kliens,args=(kliens,ÚTVONAL),daemon=True); feldolgozás_teendő.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                híd.informatikai_részleg_lezárt=True
                if híd_bejegyzés: híd_bejegyzés.Szünet_esemény.set()
                if Folyamat.poll() is None:
                    Folyamat.terminate()
                    try: Folyamat.wait(timeout=5)
                    except subprocess.TimeoutExpired: Folyamat.kill(); Folyamat.wait()
                Olvasó.join(timeout=2); Folyamat.stdin.close(); Folyamat.stdout.close(); signal.signal(signal.SIGTERM,Előző)
            if híd_bejegyzés and híd_bejegyzés.HIBA: raise RuntimeError('network bridge: '+híd_bejegyzés.HIBA)
            return 0 if 가로채기됨 else Folyamat.returncode


if __name__=='__main__':
    from végrehajt_parancs import 해상도읽기
    elemző=argparse.ArgumentParser(description=__doc__); elemző.add_argument('--port',type=int,default=5902)
    elemző.add_argument('--resolution',type=해상도읽기,default=(640,480))
    elemző.add_argument('--network',action='store_true'); elemző.add_argument('--ftp-port',type=int,default=2121)
    elemző.add_argument('--forward',action='append',default=[])
    argumentum_TÖMB=elemző.parse_args()
    if argumentum_TÖMB.forward and not argumentum_TÖMB.network: elemző.error('--forward requires --network')
    raise SystemExit(futtat_Asztal(argumentum_TÖMB.port,hálózat=argumentum_TÖMB.network,fájlátvitel_portszám=argumentum_TÖMB.ftp_port,전달규칙들=argumentum_TÖMB.forward,felbontás_ÉRTÉK=argumentum_TÖMB.resolution))
