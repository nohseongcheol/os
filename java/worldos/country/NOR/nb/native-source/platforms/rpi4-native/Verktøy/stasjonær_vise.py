#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, tast_VERDI 입력은 eget kjerne_VERDI UART로 전달한다. localhost 전용, 단일 kontroll_VERDI 클라이언트.
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
from Utfør_kommando import Kommando
from local_input import create


def EKSAKT_VERDI(socket_VERDI, Størrelse):
    data = bytearray()
    while len(data) < Størrelse:
        조각 = socket_VERDI.recv(Størrelse - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class tastatur:
    def __init__(자신, sende, 입력방식알림=None):
        자신.바이트전송 = sende; 자신.endringstast = set(); 자신.utklippstavle_VERDI = b''
        자신.한글조합기 = create(sende, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.bytt_tast = set()
        자신.UNICODE_inndata = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def sende(자신, data):
        자신.한글조합기.조합확정()
        자신.바이트전송(data)

    def bytt_MODUS(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, tast_symbol):
        if tast_symbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.endringstast.add(tast_symbol)
            else: 자신.endringstast.discard(tast_symbol)
            return
        if not 누르는중:
            자신.bytt_tast.discard(tast_symbol)
            return
        Ctrl_tasten = bool(자신.endringstast & {0xffe3, 0xffe4})
        Skift = bool(자신.endringstast & {0xffe1, 0xffe2})
        if Ctrl_tasten and Skift and tast_symbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.UNICODE_inndata = ''; return
        if 자신.UNICODE_inndata is not None:
            if tast_symbol in (32,0xff0d):
                try:
                    VERDI=int(자신.UNICODE_inndata,16)
                    if 32<=VERDI<=0x10ffff and not 0xd800<=VERDI<=0xdfff: 자신.sende(chr(VERDI).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_inndata=None
            elif tast_symbol==0xff1b: 자신.UNICODE_inndata=None
            elif tast_symbol==0xff08: 자신.UNICODE_inndata=자신.UNICODE_inndata[:-1]
            elif tast_symbol<128 and chr(tast_symbol) in '0123456789abcdefABCDEF' and len(자신.UNICODE_inndata)<6: 자신.UNICODE_inndata+=chr(tast_symbol)
            return
        if tast_symbol in (0xff31,0xffc6) or tast_symbol==32 and Skift and not Ctrl_tasten:
            if tast_symbol not in 자신.bytt_tast: 자신.bytt_MODUS()
            자신.bytt_tast.add(tast_symbol)
            return
        if tast_symbol==0xff08 and 자신.한글여부 and not Ctrl_tasten and 자신.한글조합기.앞글자지우기(): return
        if Ctrl_tasten and Skift and tast_symbol in (ord('t'),ord('T')):
            자신.sende(bytes([30,2,1,0,0,0,0])); return
        if tast_symbol==0xffc3: 자신.sende(bytes([30,2,2,0,0,0,0])); return
        if tast_symbol==0xffc9: 자신.sende(bytes([30,2,3,0,0,0,0])); return
        if Ctrl_tasten and Skift and tast_symbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.sende(자신.utklippstavle_VERDI); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if tast_symbol in 특수글쇠: 자신.sende(특수글쇠[tast_symbol]); return
        tegn_koding = tast_symbol & 0xffffff if tast_symbol & 0xff000000 == 0x01000000 else tast_symbol
        if tegn_koding > 0x10ffff or 0xd800 <= tegn_koding <= 0xdfff or tast_symbol >= 0xff00 and tast_symbol < 0x1000000: return
        if Ctrl_tasten and 0x40 <= tegn_koding <= 0x7f: 자신.sende(bytes([tegn_koding & 31])); return
        if tegn_koding < 32: return
        if 자신.한글여부 and 자신.endringstast & {0xffea,0xfe03,0xff7e} and not Ctrl_tasten and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.feed_tast(chr(tegn_koding), altgr=True): return
        앞부분 = b'\x1b' if 자신.endringstast & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not Ctrl_tasten and not 앞부분 and 32<=tegn_koding<127:
            tegndata=chr(tegn_koding).upper() if Skift else chr(tegn_koding)
            if 자신.한글조합기.feed_tast(tegndata): return
        자신.sende(앞부분 + chr(tegn_koding).encode('utf-8'))


class KOBLE_TIL_stasjonær:
    def __init__(자신, Prosess):
        자신.Prosess=Prosess; 자신.blokkere_VERDI=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.informasjonssystemer_lukket=False

    def sende(자신, data):
        if not data or 자신.informasjonssystemer_lukket: return
        with 자신.blokkere_VERDI:
            try: 자신.Prosess.stdin.write(data); 자신.Prosess.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.Prosess.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); informasjonssystemer_lukket=끝부분.rfind(b'TERMINAL CLOSED'); tegning_skjermbilde=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,informasjonssystemer_lukket,tegning_skjermbilde,종료됨)>=0:
                    자신.Terminal=열림>max(informasjonssystemer_lukket,tegning_skjermbilde,종료됨)
                    자신.시작화면=tegning_skjermbilde>max(열림,informasjonssystemer_lukket,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.sende(b'terminal\n')
        finally: 자신.informasjonssystemer_lukket=True

    def klient(자신, klient, Sti):
        server_VERDI=socket.socket(socket.AF_UNIX); server_VERDI.settimeout(10); klient.settimeout(10)
        tastatur_oppføring=tastatur(자신.sende,lambda 한글여부:자신.sende(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VERDI.connect(str(Sti))
            # opprinnelig_tilstand 협상은 순서대로 끝낸다. 이후 Utgang 가닥만 클라이언트에 쓴다.
            klient.sendall(EKSAKT_VERDI(server_VERDI,12))
            versjonsnummer=EKSAKT_VERDI(klient,12)
            if versjonsnummer not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VERDI.sendall(versjonsnummer)
            vare_ANTALL=EKSAKT_VERDI(server_VERDI,1);klient.sendall(vare_ANTALL+EKSAKT_VERDI(server_VERDI,vare_ANTALL[0]))
            Sikkerhet=EKSAKT_VERDI(klient,1)
            if Sikkerhet!=b'\x01': raise ValueError('unexpected security type')
            server_VERDI.sendall(Sikkerhet)
            if versjonsnummer==b'RFB 003.008\n':klient.sendall(EKSAKT_VERDI(server_VERDI,4))
            server_VERDI.sendall(EKSAKT_VERDI(klient,1))
            초기값=EKSAKT_VERDI(server_VERDI,24)
            klient.sendall(초기값+EKSAKT_VERDI(server_VERDI,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klient.settimeout(None);server_VERDI.settimeout(None)
            def produksjon():
                try:
                    while True:
                        område_VERDI=EKSAKT_VERDI(server_VERDI,1)[0]
                        if område_VERDI==0:
                            머리=EKSAKT_VERDI(server_VERDI,3);oppføring_ANTALL=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 ekstern_VERDI_28edcfa1 포인터의 중복을 피한다.
                            Skjult_VERDI=포인터지원
                            if Skjult_VERDI:klient.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klient.sendall(bytes([område_VERDI])+머리)
                            for _ in range(oppføring_ANTALL):
                                rektangel=EKSAKT_VERDI(server_VERDI,12);가로,vertikal_plassere,폭,높이,koding_VERDI=struct.unpack('>HHHHi',rektangel)
                                if koding_VERDI!=0:raise ValueError('unexpected framebuffer encoding: '+str(koding_VERDI))
                                klient.sendall(rektangel)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=EKSAKT_VERDI(server_VERDI,min(남음,65536));klient.sendall(data);남음-=len(data)
                        elif område_VERDI==1:
                            머리=EKSAKT_VERDI(server_VERDI,5);vare_ANTALL=struct.unpack('>H',머리[3:])[0]
                            klient.sendall(bytes([område_VERDI])+머리+EKSAKT_VERDI(server_VERDI,vare_ANTALL*6))
                        elif område_VERDI==2:klient.sendall(bytes([område_VERDI]))
                        elif område_VERDI==3:
                            머리=EKSAKT_VERDI(server_VERDI,7);vare_ANTALL=struct.unpack('>I',머리[3:])[0]
                            if vare_ANTALL>1048576:raise ValueError('server clipboard too large')
                            klient.sendall(bytes([område_VERDI])+머리+EKSAKT_VERDI(server_VERDI,vare_ANTALL))
                        else:raise ValueError('unexpected RFB server message: '+str(område_VERDI))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klient.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            arbeider=threading.Thread(target=produksjon,daemon=True);arbeider.start()
            while not 자신.informasjonssystemer_lukket:
                område_VERDI=EKSAKT_VERDI(klient,1)[0]
                if område_VERDI==4:
                    brødtekst=EKSAKT_VERDI(klient,7); tastatur_oppføring.누름값(brødtekst[0]!=0,struct.unpack('>I',brødtekst[3:])[0]); continue
                if område_VERDI==255:
                    brødtekst=EKSAKT_VERDI(klient,11)
                    if brødtekst[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tastatur_oppføring.누름값(struct.unpack('>H',brødtekst[1:3])[0]!=0,struct.unpack('>I',brødtekst[3:7])[0]); continue
                if område_VERDI==5:
                    brødtekst=EKSAKT_VERDI(klient,5); 단추들,x_koordinat,Y_koordinat=struct.unpack('>BHH',brødtekst)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tastatur_oppføring.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_koordinat<576 and 112<=Y_koordinat<372:
                        Oppslag_INDEKS=(Y_koordinat-112)//52
                        if (Y_koordinat-112)%52<40 and Oppslag_INDEKS<5: 자신.sende(bytes([ord('1')+Oppslag_INDEKS]))
                    else: 자신.sende(bytes([30,1,단추들,x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8]))
                    continue
                if område_VERDI==6:
                    brødtekst=EKSAKT_VERDI(klient,7); lengde_VERDI=struct.unpack('>i',brødtekst[3:])[0]
                    if abs(lengde_VERDI)>65536: raise ValueError('clipboard too large')
                    Tekst=EKSAKT_VERDI(klient,abs(lengde_VERDI))
                    if lengde_VERDI>=0:
                        try: tastatur_oppføring.utklippstavle_VERDI=Tekst.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tastatur_oppføring.utklippstavle_VERDI=Tekst.decode('latin-1').encode('utf-8')
                        tastatur_oppføring.utklippstavle_VERDI=tastatur_oppføring.utklippstavle_VERDI[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VERDI.sendall(bytes([område_VERDI])+brødtekst+Tekst); continue
                if område_VERDI==0:
                    brødtekst=EKSAKT_VERDI(klient,19)
                    if brødtekst[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=brødtekst[3]//8
                elif område_VERDI==2:
                    brødtekst=EKSAKT_VERDI(klient,3); oppføring_ANTALL=struct.unpack('>H',brødtekst[1:])[0]
                    if oppføring_ANTALL>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(oppføring_ANTALL)+'i',EKSAKT_VERDI(klient,oppføring_ANTALL*4))
                    포인터지원=-239 in 부호들
                    # 로컬 skjermbilde 중계는 standardverdi Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    brødtekst=struct.pack('>BHi',0,1,0)
                elif område_VERDI in (3,150): brødtekst=EKSAKT_VERDI(klient,9)
                elif område_VERDI==248:
                    brødtekst=EKSAKT_VERDI(klient,8)
                    if brødtekst[7]>64: raise ValueError('fence too large')
                    brødtekst+=EKSAKT_VERDI(klient,brødtekst[7])
                elif område_VERDI==250: brødtekst=EKSAKT_VERDI(klient,3)
                elif område_VERDI==251:
                    brødtekst=EKSAKT_VERDI(klient,7)
                    if brødtekst[5]>16: raise ValueError('too many screens')
                    brødtekst+=EKSAKT_VERDI(klient,brødtekst[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(område_VERDI))
                server_VERDI.sendall(bytes([område_VERDI])+brødtekst)
        except (OSError,EOFError,ValueError) as feil:
            if str(feil): print('VNC client:',feil,file=sys.stderr,flush=True)
        finally:
            for socket_VERDI in (klient,server_VERDI):
                try: socket_VERDI.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                socket_VERDI.close()


def kjøre_stasjonær(portnummer=5902, nettverk=False, filoverføring_portnummer=2121, 전달규칙들=(), oppløsning_VERDI=(640, 480), gjest_e_post=None, vert_e_post='127.0.0.1'):
    with ExitStack() as Ressurser, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        bro_oppføring = None
        if nettverk:
            from bro_3de4fe3a import bro_3de4fe3a
            bro_oppføring = Ressurser.enter_context(bro_3de4fe3a(filoverføring_portnummer, 전달규칙들, gjest_e_post=gjest_e_post, vert_e_post=vert_e_post))
        Sti=Path(작업경로)/'display.sock'
        with socket.socket() as motta_port:
            motta_port.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            motta_port.bind(('127.0.0.1',portnummer)); motta_port.listen(1); motta_port.settimeout(.2)
            원격화면접속번호=motta_port.getsockname()[1]
            if bro_oppføring and (원격화면접속번호==filoverføring_portnummer or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and vert==원격화면접속번호 for 통신규약,vert,_ in bro_oppføring.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Prosess=subprocess.Popen(Kommando(oppløsning_VERDI)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Sti)]+(bro_oppføring.전달인수() if bro_oppføring else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            bro=KOBLE_TIL_stasjonær(Prosess); Leser=threading.Thread(target=bro.직렬입출력,daemon=True); Leser.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(motta_port.getsockname()[1]),flush=True)
            if bro_oppføring: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(vert_e_post,filoverføring_portnummer),flush=True)
            def avslutte(signal_nummer,kjøring_bilde): raise KeyboardInterrupt()
            Forrige=signal.signal(signal.SIGTERM,avslutte)
            behandling_oppgave=None; 가로채기됨=False
            try:
                while Prosess.poll() is None:
                    try: klient,_=motta_port.accept()
                    except socket.timeout: continue
                    if behandling_oppgave is not None and behandling_oppgave.is_alive(): klient.close(); continue
                    if not Sti.exists(): klient.close(); continue
                    behandling_oppgave=threading.Thread(target=bro.klient,args=(klient,Sti),daemon=True); behandling_oppgave.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                bro.informasjonssystemer_lukket=True
                if bro_oppføring: bro_oppføring.Pause_hendelse.set()
                if Prosess.poll() is None:
                    Prosess.terminate()
                    try: Prosess.wait(timeout=5)
                    except subprocess.TimeoutExpired: Prosess.kill(); Prosess.wait()
                Leser.join(timeout=2); Prosess.stdin.close(); Prosess.stdout.close(); signal.signal(signal.SIGTERM,Forrige)
            if bro_oppføring and bro_oppføring.feil: raise RuntimeError('network bridge: '+bro_oppføring.feil)
            return 0 if 가로채기됨 else Prosess.returncode


if __name__=='__main__':
    from Utfør_kommando import 해상도읽기
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    argument_MATRISE=parser.parse_args()
    if argument_MATRISE.forward and not argument_MATRISE.network: parser.error('--forward requires --network')
    raise SystemExit(kjøre_stasjonær(argument_MATRISE.port,nettverk=argument_MATRISE.network,filoverføring_portnummer=argument_MATRISE.ftp_port,전달규칙들=argument_MATRISE.forward,oppløsning_VERDI=argument_MATRISE.resolution))
