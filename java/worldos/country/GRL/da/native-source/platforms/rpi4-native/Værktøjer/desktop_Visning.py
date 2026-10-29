#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, tast_VÆRDI 입력은 eget kerne_VÆRDI UART로 전달한다. localhost 전용, 단일 kontrol_VÆRDI 클라이언트.
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
from Udfør_kommando import Kommando
from local_input import create


def EKSAKT_VÆRDI(socket_VÆRDI, Størrelse):
    data = bytearray()
    while len(data) < Størrelse:
        조각 = socket_VÆRDI.recv(Størrelse - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class tastatur:
    def __init__(자신, maile, 입력방식알림=None):
        자신.바이트전송 = maile; 자신.ændringstast = set(); 자신.udklipsholder_VÆRDI = b''
        자신.한글조합기 = create(maile, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SKIFT_tast = set()
        자신.UNICODE_input = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def maile(자신, data):
        자신.한글조합기.udføre_komposition()
        자신.바이트전송(data)

    def SKIFT_HYPPIGST(자신):
        자신.한글조합기.udføre_komposition(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, tast_symbol):
        if tast_symbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ændringstast.add(tast_symbol)
            else: 자신.ændringstast.discard(tast_symbol)
            return
        if not 누르는중:
            자신.SKIFT_tast.discard(tast_symbol)
            return
        Ctrl = bool(자신.ændringstast & {0xffe3, 0xffe4})
        Skift_tast = bool(자신.ændringstast & {0xffe1, 0xffe2})
        if Ctrl and Skift_tast and tast_symbol in (ord('u'),ord('U')):
            자신.한글조합기.udføre_komposition(); 자신.UNICODE_input = ''; return
        if 자신.UNICODE_input is not None:
            if tast_symbol in (32,0xff0d):
                try:
                    VÆRDI=int(자신.UNICODE_input,16)
                    if 32<=VÆRDI<=0x10ffff and not 0xd800<=VÆRDI<=0xdfff: 자신.maile(chr(VÆRDI).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_input=None
            elif tast_symbol==0xff1b: 자신.UNICODE_input=None
            elif tast_symbol==0xff08: 자신.UNICODE_input=자신.UNICODE_input[:-1]
            elif tast_symbol<128 and chr(tast_symbol) in '0123456789abcdefABCDEF' and len(자신.UNICODE_input)<6: 자신.UNICODE_input+=chr(tast_symbol)
            return
        if tast_symbol in (0xff31,0xffc6) or tast_symbol==32 and Skift_tast and not Ctrl:
            if tast_symbol not in 자신.SKIFT_tast: 자신.SKIFT_HYPPIGST()
            자신.SKIFT_tast.add(tast_symbol)
            return
        if tast_symbol==0xff08 and 자신.한글여부 and not Ctrl and 자신.한글조합기.앞글자지우기(): return
        if Ctrl and Skift_tast and tast_symbol in (ord('t'),ord('T')):
            자신.maile(bytes([30,2,1,0,0,0,0])); return
        if tast_symbol==0xffc3: 자신.maile(bytes([30,2,2,0,0,0,0])); return
        if tast_symbol==0xffc9: 자신.maile(bytes([30,2,3,0,0,0,0])); return
        if Ctrl and Skift_tast and tast_symbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.maile(자신.udklipsholder_VÆRDI); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if tast_symbol in 특수글쇠: 자신.maile(특수글쇠[tast_symbol]); return
        tegnkodning = tast_symbol & 0xffffff if tast_symbol & 0xff000000 == 0x01000000 else tast_symbol
        if tegnkodning > 0x10ffff or 0xd800 <= tegnkodning <= 0xdfff or tast_symbol >= 0xff00 and tast_symbol < 0x1000000: return
        if Ctrl and 0x40 <= tegnkodning <= 0x7f: 자신.maile(bytes([tegnkodning & 31])); return
        if tegnkodning < 32: return
        if 자신.한글여부 and 자신.ændringstast & {0xffea,0xfe03,0xff7e} and not Ctrl and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.feed_tast(chr(tegnkodning), altgr=True): return
        앞부분 = b'\x1b' if 자신.ændringstast & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not Ctrl and not 앞부분 and 32<=tegnkodning<127:
            tegndata=chr(tegnkodning).upper() if Skift_tast else chr(tegnkodning)
            if 자신.한글조합기.feed_tast(tegndata): return
        자신.maile(앞부분 + chr(tegnkodning).encode('utf-8'))


class Forbind_desktop:
    def __init__(자신, Proces):
        자신.Proces=Proces; 자신.lås_VÆRDI=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.it_lukket=False

    def maile(자신, data):
        if not data or 자신.it_lukket: return
        with 자신.lås_VÆRDI:
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
                열림=끝부분.rfind(b'TERMINAL READY'); it_lukket=끝부분.rfind(b'TERMINAL CLOSED'); tegning_skærmbillede=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,it_lukket,tegning_skærmbillede,종료됨)>=0:
                    자신.Terminal=열림>max(it_lukket,tegning_skærmbillede,종료됨)
                    자신.시작화면=tegning_skærmbillede>max(열림,it_lukket,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.maile(b'terminal\n')
        finally: 자신.it_lukket=True

    def klient(자신, klient, Sti):
        server_VÆRDI=socket.socket(socket.AF_UNIX); server_VÆRDI.settimeout(10); klient.settimeout(10)
        tastatur_post=tastatur(자신.maile,lambda 한글여부:자신.maile(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VÆRDI.connect(str(Sti))
            # starttilstand 협상은 순서대로 끝낸다. 이후 Udgang 가닥만 클라이언트에 쓴다.
            klient.sendall(EKSAKT_VÆRDI(server_VÆRDI,12))
            versionsnummer=EKSAKT_VÆRDI(klient,12)
            if versionsnummer not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VÆRDI.sendall(versionsnummer)
            vare_TÆL=EKSAKT_VÆRDI(server_VÆRDI,1);klient.sendall(vare_TÆL+EKSAKT_VÆRDI(server_VÆRDI,vare_TÆL[0]))
            Sikkerhed=EKSAKT_VÆRDI(klient,1)
            if Sikkerhed!=b'\x01': raise ValueError('unexpected security type')
            server_VÆRDI.sendall(Sikkerhed)
            if versionsnummer==b'RFB 003.008\n':klient.sendall(EKSAKT_VÆRDI(server_VÆRDI,4))
            server_VÆRDI.sendall(EKSAKT_VÆRDI(klient,1))
            초기값=EKSAKT_VÆRDI(server_VÆRDI,24)
            klient.sendall(초기값+EKSAKT_VÆRDI(server_VÆRDI,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klient.settimeout(None);server_VÆRDI.settimeout(None)
            def produktoutput():
                try:
                    while True:
                        område_VÆRDI=EKSAKT_VÆRDI(server_VÆRDI,1)[0]
                        if område_VÆRDI==0:
                            머리=EKSAKT_VÆRDI(server_VÆRDI,3);post_TÆL_8f7753a1=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 fjern_VÆRDI 포인터의 중복을 피한다.
                            Skjult_VÆRDI=포인터지원
                            if Skjult_VÆRDI:klient.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klient.sendall(bytes([område_VÆRDI])+머리)
                            for _ in range(post_TÆL_8f7753a1):
                                rektangel=EKSAKT_VÆRDI(server_VÆRDI,12);가로,Lodret_placere,폭,높이,kodning_VÆRDI=struct.unpack('>HHHHi',rektangel)
                                if kodning_VÆRDI!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodning_VÆRDI))
                                klient.sendall(rektangel)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=EKSAKT_VÆRDI(server_VÆRDI,min(남음,65536));klient.sendall(data);남음-=len(data)
                        elif område_VÆRDI==1:
                            머리=EKSAKT_VÆRDI(server_VÆRDI,5);vare_TÆL=struct.unpack('>H',머리[3:])[0]
                            klient.sendall(bytes([område_VÆRDI])+머리+EKSAKT_VÆRDI(server_VÆRDI,vare_TÆL*6))
                        elif område_VÆRDI==2:klient.sendall(bytes([område_VÆRDI]))
                        elif område_VÆRDI==3:
                            머리=EKSAKT_VÆRDI(server_VÆRDI,7);vare_TÆL=struct.unpack('>I',머리[3:])[0]
                            if vare_TÆL>1048576:raise ValueError('server clipboard too large')
                            klient.sendall(bytes([område_VÆRDI])+머리+EKSAKT_VÆRDI(server_VÆRDI,vare_TÆL))
                        else:raise ValueError('unexpected RFB server message: '+str(område_VÆRDI))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klient.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            arbejder=threading.Thread(target=produktoutput,daemon=True);arbejder.start()
            while not 자신.it_lukket:
                område_VÆRDI=EKSAKT_VÆRDI(klient,1)[0]
                if område_VÆRDI==4:
                    brødtekst=EKSAKT_VÆRDI(klient,7); tastatur_post.누름값(brødtekst[0]!=0,struct.unpack('>I',brødtekst[3:])[0]); continue
                if område_VÆRDI==255:
                    brødtekst=EKSAKT_VÆRDI(klient,11)
                    if brødtekst[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tastatur_post.누름값(struct.unpack('>H',brødtekst[1:3])[0]!=0,struct.unpack('>I',brødtekst[3:7])[0]); continue
                if område_VÆRDI==5:
                    brødtekst=EKSAKT_VÆRDI(klient,5); 단추들,X_koordinat,Y_koordinat=struct.unpack('>BHH',brødtekst)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tastatur_post.한글조합기.udføre_komposition()
                    if 눌림&1 and 자신.시작화면 and 64<=X_koordinat<576 and 112<=Y_koordinat<372:
                        Opslag_INDEKS=(Y_koordinat-112)//52
                        if (Y_koordinat-112)%52<40 and Opslag_INDEKS<5: 자신.maile(bytes([ord('1')+Opslag_INDEKS]))
                    else: 자신.maile(bytes([30,1,단추들,X_koordinat&255,X_koordinat>>8,Y_koordinat&255,Y_koordinat>>8]))
                    continue
                if område_VÆRDI==6:
                    brødtekst=EKSAKT_VÆRDI(klient,7); varighed_VÆRDI=struct.unpack('>i',brødtekst[3:])[0]
                    if abs(varighed_VÆRDI)>65536: raise ValueError('clipboard too large')
                    Tekst=EKSAKT_VÆRDI(klient,abs(varighed_VÆRDI))
                    if varighed_VÆRDI>=0:
                        try: tastatur_post.udklipsholder_VÆRDI=Tekst.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tastatur_post.udklipsholder_VÆRDI=Tekst.decode('latin-1').encode('utf-8')
                        tastatur_post.udklipsholder_VÆRDI=tastatur_post.udklipsholder_VÆRDI[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VÆRDI.sendall(bytes([område_VÆRDI])+brødtekst+Tekst); continue
                if område_VÆRDI==0:
                    brødtekst=EKSAKT_VÆRDI(klient,19)
                    if brødtekst[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=brødtekst[3]//8
                elif område_VÆRDI==2:
                    brødtekst=EKSAKT_VÆRDI(klient,3); post_TÆL_8f7753a1=struct.unpack('>H',brødtekst[1:])[0]
                    if post_TÆL_8f7753a1>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(post_TÆL_8f7753a1)+'i',EKSAKT_VÆRDI(klient,post_TÆL_8f7753a1*4))
                    포인터지원=-239 in 부호들
                    # 로컬 skærmbillede 중계는 standardværdi Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    brødtekst=struct.pack('>BHi',0,1,0)
                elif område_VÆRDI in (3,150): brødtekst=EKSAKT_VÆRDI(klient,9)
                elif område_VÆRDI==248:
                    brødtekst=EKSAKT_VÆRDI(klient,8)
                    if brødtekst[7]>64: raise ValueError('fence too large')
                    brødtekst+=EKSAKT_VÆRDI(klient,brødtekst[7])
                elif område_VÆRDI==250: brødtekst=EKSAKT_VÆRDI(klient,3)
                elif område_VÆRDI==251:
                    brødtekst=EKSAKT_VÆRDI(klient,7)
                    if brødtekst[5]>16: raise ValueError('too many screens')
                    brødtekst+=EKSAKT_VÆRDI(klient,brødtekst[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(område_VÆRDI))
                server_VÆRDI.sendall(bytes([område_VÆRDI])+brødtekst)
        except (OSError,EOFError,ValueError) as fejl:
            if str(fejl): print('VNC client:',fejl,file=sys.stderr,flush=True)
        finally:
            for socket_VÆRDI in (klient,server_VÆRDI):
                try: socket_VÆRDI.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                socket_VÆRDI.close()


def køre_desktop(portnummer=5902, netværk=False, filoverførsel_portnummer=2121, 전달규칙들=(), opløsning_VÆRDI=(640, 480), gæst_mail=None, vært_mail='127.0.0.1'):
    with ExitStack() as Ressourcer, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        bro_post = None
        if netværk:
            from bro_3de4fe3a import bro_3de4fe3a
            bro_post = Ressourcer.enter_context(bro_3de4fe3a(filoverførsel_portnummer, 전달규칙들, gæst_mail=gæst_mail, vært_mail=vært_mail))
        Sti=Path(작업경로)/'display.sock'
        with socket.socket() as modtage_port:
            modtage_port.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            modtage_port.bind(('127.0.0.1',portnummer)); modtage_port.listen(1); modtage_port.settimeout(.2)
            원격화면접속번호=modtage_port.getsockname()[1]
            if bro_post and (원격화면접속번호==filoverførsel_portnummer or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and vært==원격화면접속번호 for 통신규약,vært,_ in bro_post.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proces=subprocess.Popen(Kommando(opløsning_VÆRDI)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Sti)]+(bro_post.전달인수() if bro_post else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            bro=Forbind_desktop(Proces); Læser=threading.Thread(target=bro.직렬입출력,daemon=True); Læser.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(modtage_port.getsockname()[1]),flush=True)
            if bro_post: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(vært_mail,filoverførsel_portnummer),flush=True)
            def afslutte(signal_tal,udførelse_ramme): raise KeyboardInterrupt()
            Forrige=signal.signal(signal.SIGTERM,afslutte)
            behandling_job=None; 가로채기됨=False
            try:
                while Proces.poll() is None:
                    try: klient,_=modtage_port.accept()
                    except socket.timeout: continue
                    if behandling_job is not None and behandling_job.is_alive(): klient.close(); continue
                    if not Sti.exists(): klient.close(); continue
                    behandling_job=threading.Thread(target=bro.klient,args=(klient,Sti),daemon=True); behandling_job.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                bro.it_lukket=True
                if bro_post: bro_post.Afbryd_midlertidigt_hændelse.set()
                if Proces.poll() is None:
                    Proces.terminate()
                    try: Proces.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
                Læser.join(timeout=2); Proces.stdin.close(); Proces.stdout.close(); signal.signal(signal.SIGTERM,Forrige)
            if bro_post and bro_post.fejl: raise RuntimeError('network bridge: '+bro_post.fejl)
            return 0 if 가로채기됨 else Proces.returncode


if __name__=='__main__':
    from Udfør_kommando import 해상도읽기
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    argument_MATRIX=parser.parse_args()
    if argument_MATRIX.forward and not argument_MATRIX.network: parser.error('--forward requires --network')
    raise SystemExit(køre_desktop(argument_MATRIX.port,netværk=argument_MATRIX.network,filoverførsel_portnummer=argument_MATRIX.ftp_port,전달규칙들=argument_MATRIX.forward,opløsning_VÆRDI=argument_MATRIX.resolution))
