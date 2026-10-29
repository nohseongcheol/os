#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Nyckel_värde 입력은 eget kärna_värde UART로 전달한다. localhost 전용, 단일 kontroll_värde 클라이언트.
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
from köra_kommando import kommando
from local_input import create


def EXAKT_värde(socket_värde, Storlek):
    data = bytearray()
    while len(data) < Storlek:
        조각 = socket_värde.recv(Storlek - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class tangentbord:
    def __init__(자신, skicka, 입력방식알림=None):
        자신.바이트전송 = skicka; 자신.låstangent = set(); 자신.Urklipp_värde = b''
        자신.한글조합기 = create(skicka, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.byta_Nyckel = set()
        자신.UNICODE_indata = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def skicka(자신, data):
        자신.한글조합기.incheckning_komposition()
        자신.바이트전송(data)

    def byta_läge(자신):
        자신.한글조합기.incheckning_komposition(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Nyckel_symbol):
        if Nyckel_symbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.låstangent.add(Nyckel_symbol)
            else: 자신.låstangent.discard(Nyckel_symbol)
            return
        if not 누르는중:
            자신.byta_Nyckel.discard(Nyckel_symbol)
            return
        CTRL = bool(자신.låstangent & {0xffe3, 0xffe4})
        SKIFT_tangenten = bool(자신.låstangent & {0xffe1, 0xffe2})
        if CTRL and SKIFT_tangenten and Nyckel_symbol in (ord('u'),ord('U')):
            자신.한글조합기.incheckning_komposition(); 자신.UNICODE_indata = ''; return
        if 자신.UNICODE_indata is not None:
            if Nyckel_symbol in (32,0xff0d):
                try:
                    värde=int(자신.UNICODE_indata,16)
                    if 32<=värde<=0x10ffff and not 0xd800<=värde<=0xdfff: 자신.skicka(chr(värde).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_indata=None
            elif Nyckel_symbol==0xff1b: 자신.UNICODE_indata=None
            elif Nyckel_symbol==0xff08: 자신.UNICODE_indata=자신.UNICODE_indata[:-1]
            elif Nyckel_symbol<128 and chr(Nyckel_symbol) in '0123456789abcdefABCDEF' and len(자신.UNICODE_indata)<6: 자신.UNICODE_indata+=chr(Nyckel_symbol)
            return
        if Nyckel_symbol in (0xff31,0xffc6) or Nyckel_symbol==32 and SKIFT_tangenten and not CTRL:
            if Nyckel_symbol not in 자신.byta_Nyckel: 자신.byta_läge()
            자신.byta_Nyckel.add(Nyckel_symbol)
            return
        if Nyckel_symbol==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SKIFT_tangenten and Nyckel_symbol in (ord('t'),ord('T')):
            자신.skicka(bytes([30,2,1,0,0,0,0])); return
        if Nyckel_symbol==0xffc3: 자신.skicka(bytes([30,2,2,0,0,0,0])); return
        if Nyckel_symbol==0xffc9: 자신.skicka(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SKIFT_tangenten and Nyckel_symbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.skicka(자신.Urklipp_värde); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Nyckel_symbol in 특수글쇠: 자신.skicka(특수글쇠[Nyckel_symbol]); return
        teckenkodning = Nyckel_symbol & 0xffffff if Nyckel_symbol & 0xff000000 == 0x01000000 else Nyckel_symbol
        if teckenkodning > 0x10ffff or 0xd800 <= teckenkodning <= 0xdfff or Nyckel_symbol >= 0xff00 and Nyckel_symbol < 0x1000000: return
        if CTRL and 0x40 <= teckenkodning <= 0x7f: 자신.skicka(bytes([teckenkodning & 31])); return
        if teckenkodning < 32: return
        if 자신.한글여부 and 자신.låstangent & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.feed_Nyckel(chr(teckenkodning), altgr=True): return
        avstånd_del = b'\x1b' if 자신.låstangent & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not avstånd_del and 32<=teckenkodning<127:
            teckendata=chr(teckenkodning).upper() if SKIFT_tangenten else chr(teckenkodning)
            if 자신.한글조합기.feed_Nyckel(teckendata): return
        자신.skicka(avstånd_del + chr(teckenkodning).encode('utf-8'))


class ANSLUT_Dator:
    def __init__(자신, Process):
        자신.Process=Process; 자신.lås_värde=threading.Lock(); 자신.준비완료=False; 자신.kommandotolk=False; 자신.시작화면=False; 자신.informationsteknik_stängd=False

    def skicka(자신, data):
        if not data or 자신.informationsteknik_stängd: return
        with 자신.lås_värde:
            try: 자신.Process.stdin.write(data); 자신.Process.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.Process.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); informationsteknik_stängd=끝부분.rfind(b'TERMINAL CLOSED'); ritning_skärmbild=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,informationsteknik_stängd,ritning_skärmbild,종료됨)>=0:
                    자신.kommandotolk=열림>max(informationsteknik_stängd,ritning_skärmbild,종료됨)
                    자신.시작화면=ritning_skärmbild>max(열림,informationsteknik_stängd,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.skicka(b'terminal\n')
        finally: 자신.informationsteknik_stängd=True

    def klient(자신, klient, sökväg_2):
        server_värde=socket.socket(socket.AF_UNIX); server_värde.settimeout(10); klient.settimeout(10)
        tangentbord_post=tangentbord(자신.skicka,lambda 한글여부:자신.skicka(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_värde.connect(str(sökväg_2))
            # starttillstånd 협상은 순서대로 끝낸다. 이후 utmatningsposition 가닥만 클라이언트에 쓴다.
            klient.sendall(EXAKT_värde(server_värde,12))
            versionsnummer=EXAKT_värde(klient,12)
            if versionsnummer not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_värde.sendall(versionsnummer)
            objekt_ANTAL=EXAKT_värde(server_värde,1);klient.sendall(objekt_ANTAL+EXAKT_värde(server_värde,objekt_ANTAL[0]))
            Säkerhet=EXAKT_värde(klient,1)
            if Säkerhet!=b'\x01': raise ValueError('unexpected security type')
            server_värde.sendall(Säkerhet)
            if versionsnummer==b'RFB 003.008\n':klient.sendall(EXAKT_värde(server_värde,4))
            server_värde.sendall(EXAKT_värde(klient,1))
            초기값=EXAKT_värde(server_värde,24)
            klient.sendall(초기값+EXAKT_värde(server_värde,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klient.settimeout(None);server_värde.settimeout(None)
            def utleverans():
                try:
                    while True:
                        område_värde=EXAKT_värde(server_värde,1)[0]
                        if område_värde==0:
                            머리=EXAKT_värde(server_värde,3);post_ANTAL=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 fjärr_värde 포인터의 중복을 피한다.
                            Dold_värde=포인터지원
                            if Dold_värde:klient.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klient.sendall(bytes([område_värde])+머리)
                            for _ in range(post_ANTAL):
                                rektangel=EXAKT_värde(server_värde,12);가로,bransch_placera,폭,높이,kodning_värde=struct.unpack('>HHHHi',rektangel)
                                if kodning_värde!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodning_värde))
                                klient.sendall(rektangel)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=EXAKT_värde(server_värde,min(남음,65536));klient.sendall(data);남음-=len(data)
                        elif område_värde==1:
                            머리=EXAKT_värde(server_värde,5);objekt_ANTAL=struct.unpack('>H',머리[3:])[0]
                            klient.sendall(bytes([område_värde])+머리+EXAKT_värde(server_värde,objekt_ANTAL*6))
                        elif område_värde==2:klient.sendall(bytes([område_värde]))
                        elif område_värde==3:
                            머리=EXAKT_värde(server_värde,7);objekt_ANTAL=struct.unpack('>I',머리[3:])[0]
                            if objekt_ANTAL>1048576:raise ValueError('server clipboard too large')
                            klient.sendall(bytes([område_värde])+머리+EXAKT_värde(server_värde,objekt_ANTAL))
                        else:raise ValueError('unexpected RFB server message: '+str(område_värde))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klient.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            arbete=threading.Thread(target=utleverans,daemon=True);arbete.start()
            while not 자신.informationsteknik_stängd:
                område_värde=EXAKT_värde(klient,1)[0]
                if område_värde==4:
                    brödtext=EXAKT_värde(klient,7); tangentbord_post.누름값(brödtext[0]!=0,struct.unpack('>I',brödtext[3:])[0]); continue
                if område_värde==255:
                    brödtext=EXAKT_värde(klient,11)
                    if brödtext[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tangentbord_post.누름값(struct.unpack('>H',brödtext[1:3])[0]!=0,struct.unpack('>I',brödtext[3:7])[0]); continue
                if område_värde==5:
                    brödtext=EXAKT_värde(klient,5); 단추들,x_koordinat,Y_koordinat=struct.unpack('>BHH',brödtext)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tangentbord_post.한글조합기.incheckning_komposition()
                    if 눌림&1 and 자신.시작화면 and 64<=x_koordinat<576 and 112<=Y_koordinat<372:
                        LETAUPP_INDEX=(Y_koordinat-112)//52
                        if (Y_koordinat-112)%52<40 and LETAUPP_INDEX<5: 자신.skicka(bytes([ord('1')+LETAUPP_INDEX]))
                    else: 자신.skicka(bytes([30,1,단추들,x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8]))
                    continue
                if område_värde==6:
                    brödtext=EXAKT_värde(klient,7); längd_värde=struct.unpack('>i',brödtext[3:])[0]
                    if abs(längd_värde)>65536: raise ValueError('clipboard too large')
                    text=EXAKT_värde(klient,abs(längd_värde))
                    if längd_värde>=0:
                        try: tangentbord_post.Urklipp_värde=text.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tangentbord_post.Urklipp_värde=text.decode('latin-1').encode('utf-8')
                        tangentbord_post.Urklipp_värde=tangentbord_post.Urklipp_värde[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_värde.sendall(bytes([område_värde])+brödtext+text); continue
                if område_värde==0:
                    brödtext=EXAKT_värde(klient,19)
                    if brödtext[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=brödtext[3]//8
                elif område_värde==2:
                    brödtext=EXAKT_värde(klient,3); post_ANTAL=struct.unpack('>H',brödtext[1:])[0]
                    if post_ANTAL>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(post_ANTAL)+'i',EXAKT_värde(klient,post_ANTAL*4))
                    포인터지원=-239 in 부호들
                    # 로컬 skärmbild 중계는 standardvärde Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    brödtext=struct.pack('>BHi',0,1,0)
                elif område_värde in (3,150): brödtext=EXAKT_värde(klient,9)
                elif område_värde==248:
                    brödtext=EXAKT_värde(klient,8)
                    if brödtext[7]>64: raise ValueError('fence too large')
                    brödtext+=EXAKT_värde(klient,brödtext[7])
                elif område_värde==250: brödtext=EXAKT_värde(klient,3)
                elif område_värde==251:
                    brödtext=EXAKT_värde(klient,7)
                    if brödtext[5]>16: raise ValueError('too many screens')
                    brödtext+=EXAKT_värde(klient,brödtext[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(område_värde))
                server_värde.sendall(bytes([område_värde])+brödtext)
        except (OSError,EOFError,ValueError) as fel:
            if str(fel): print('VNC client:',fel,file=sys.stderr,flush=True)
        finally:
            for socket_värde in (klient,server_värde):
                try: socket_värde.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                socket_värde.close()


def köra_Dator(portnummer=5902, nätverk=False, filöverföring_portnummer=2121, 전달규칙들=(), upplösning_värde=(640, 480), gäst_ADRESS=None, värd_ADRESS='127.0.0.1'):
    with ExitStack() as Resurser, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        brygga_post = None
        if nätverk:
            from brygga_3de4fe3a import brygga_3de4fe3a
            brygga_post = Resurser.enter_context(brygga_3de4fe3a(filöverföring_portnummer, 전달규칙들, gäst_ADRESS=gäst_ADRESS, värd_ADRESS=värd_ADRESS))
        sökväg_2=Path(작업경로)/'display.sock'
        with socket.socket() as få_port:
            få_port.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            få_port.bind(('127.0.0.1',portnummer)); få_port.listen(1); få_port.settimeout(.2)
            원격화면접속번호=få_port.getsockname()[1]
            if brygga_post and (원격화면접속번호==filöverföring_portnummer or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and värd==원격화면접속번호 for 통신규약,värd,_ in brygga_post.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Process=subprocess.Popen(kommando(upplösning_värde)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(sökväg_2)]+(brygga_post.전달인수() if brygga_post else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            brygga=ANSLUT_Dator(Process); Läsare=threading.Thread(target=brygga.직렬입출력,daemon=True); Läsare.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(få_port.getsockname()[1]),flush=True)
            if brygga_post: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(värd_ADRESS,filöverföring_portnummer),flush=True)
            def avsluta(signal_nummer,körning_ram): raise KeyboardInterrupt()
            Föregående=signal.signal(signal.SIGTERM,avsluta)
            bearbetning_uppgift=None; 가로채기됨=False
            try:
                while Process.poll() is None:
                    try: klient,_=få_port.accept()
                    except socket.timeout: continue
                    if bearbetning_uppgift is not None and bearbetning_uppgift.is_alive(): klient.close(); continue
                    if not sökväg_2.exists(): klient.close(); continue
                    bearbetning_uppgift=threading.Thread(target=brygga.klient,args=(klient,sökväg_2),daemon=True); bearbetning_uppgift.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                brygga.informationsteknik_stängd=True
                if brygga_post: brygga_post.Pausa_händelse.set()
                if Process.poll() is None:
                    Process.terminate()
                    try: Process.wait(timeout=5)
                    except subprocess.TimeoutExpired: Process.kill(); Process.wait()
                Läsare.join(timeout=2); Process.stdin.close(); Process.stdout.close(); signal.signal(signal.SIGTERM,Föregående)
            if brygga_post and brygga_post.fel: raise RuntimeError('network bridge: '+brygga_post.fel)
            return 0 if 가로채기됨 else Process.returncode


if __name__=='__main__':
    from köra_kommando import läsa_upplösning
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=läsa_upplösning,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    argument_MATRIS=parser.parse_args()
    if argument_MATRIS.forward and not argument_MATRIS.network: parser.error('--forward requires --network')
    raise SystemExit(köra_Dator(argument_MATRIS.port,nätverk=argument_MATRIS.network,filöverföring_portnummer=argument_MATRIS.ftp_port,전달규칙들=argument_MATRIS.forward,upplösning_värde=argument_MATRIS.resolution))
