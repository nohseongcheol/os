#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, toets_WAARDE 입력은 Eigen kernel_WAARDE UART로 전달한다. localhost 전용, 단일 controle_WAARDE 클라이언트.
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
from Uitvoeren_opdracht import opdracht
from local_input import create


def GELIJK_WAARDE(socket_WAARDE, Grootte):
    gegevens = bytearray()
    while len(gegevens) < Grootte:
        조각 = socket_WAARDE.recv(Grootte - len(gegevens))
        if not 조각: raise EOFError()
        gegevens.extend(조각)
    return bytes(gegevens)


class toetsenbord:
    def __init__(자신, e_mailen, 입력방식알림=None):
        자신.바이트전송 = e_mailen; 자신.wijzigingstoets = set(); 자신.klembord_WAARDE = b''
        자신.한글조합기 = create(e_mailen, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.switch_toets = set()
        자신.UNICODE_invoer = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def e_mailen(자신, gegevens):
        자신.한글조합기.doorvoeren_samenstelling()
        자신.바이트전송(gegevens)

    def switch_MODUS(자신):
        자신.한글조합기.doorvoeren_samenstelling(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, toets_symbool):
        if toets_symbool in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.wijzigingstoets.add(toets_symbool)
            else: 자신.wijzigingstoets.discard(toets_symbool)
            return
        if not 누르는중:
            자신.switch_toets.discard(toets_symbool)
            return
        Ctrl = bool(자신.wijzigingstoets & {0xffe3, 0xffe4})
        SHIFT_toets = bool(자신.wijzigingstoets & {0xffe1, 0xffe2})
        if Ctrl and SHIFT_toets and toets_symbool in (ord('u'),ord('U')):
            자신.한글조합기.doorvoeren_samenstelling(); 자신.UNICODE_invoer = ''; return
        if 자신.UNICODE_invoer is not None:
            if toets_symbool in (32,0xff0d):
                try:
                    WAARDE=int(자신.UNICODE_invoer,16)
                    if 32<=WAARDE<=0x10ffff and not 0xd800<=WAARDE<=0xdfff: 자신.e_mailen(chr(WAARDE).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_invoer=None
            elif toets_symbool==0xff1b: 자신.UNICODE_invoer=None
            elif toets_symbool==0xff08: 자신.UNICODE_invoer=자신.UNICODE_invoer[:-1]
            elif toets_symbool<128 and chr(toets_symbool) in '0123456789abcdefABCDEF' and len(자신.UNICODE_invoer)<6: 자신.UNICODE_invoer+=chr(toets_symbool)
            return
        if toets_symbool in (0xff31,0xffc6) or toets_symbool==32 and SHIFT_toets and not Ctrl:
            if toets_symbool not in 자신.switch_toets: 자신.switch_MODUS()
            자신.switch_toets.add(toets_symbool)
            return
        if toets_symbool==0xff08 and 자신.한글여부 and not Ctrl and 자신.한글조합기.앞글자지우기(): return
        if Ctrl and SHIFT_toets and toets_symbool in (ord('t'),ord('T')):
            자신.e_mailen(bytes([30,2,1,0,0,0,0])); return
        if toets_symbool==0xffc3: 자신.e_mailen(bytes([30,2,2,0,0,0,0])); return
        if toets_symbool==0xffc9: 자신.e_mailen(bytes([30,2,3,0,0,0,0])); return
        if Ctrl and SHIFT_toets and toets_symbool in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.e_mailen(자신.klembord_WAARDE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if toets_symbool in 특수글쇠: 자신.e_mailen(특수글쇠[toets_symbool]); return
        tekencodering = toets_symbool & 0xffffff if toets_symbool & 0xff000000 == 0x01000000 else toets_symbool
        if tekencodering > 0x10ffff or 0xd800 <= tekencodering <= 0xdfff or toets_symbool >= 0xff00 and toets_symbool < 0x1000000: return
        if Ctrl and 0x40 <= tekencodering <= 0x7f: 자신.e_mailen(bytes([tekencodering & 31])); return
        if tekencodering < 32: return
        if 자신.한글여부 and 자신.wijzigingstoets & {0xffea,0xfe03,0xff7e} and not Ctrl and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.feed_toets(chr(tekencodering), altgr=True): return
        interlinie_tegel = b'\x1b' if 자신.wijzigingstoets & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not Ctrl and not interlinie_tegel and 32<=tekencodering<127:
            tekengegevens=chr(tekencodering).upper() if SHIFT_toets else chr(tekencodering)
            if 자신.한글조합기.feed_toets(tekengegevens): return
        자신.e_mailen(interlinie_tegel + chr(tekencodering).encode('utf-8'))


class VERBINDEN_pc:
    def __init__(자신, Proces):
        자신.Proces=Proces; 자신.vergrendelen_WAARDE=threading.Lock(); 자신.준비완료=False; 자신.terminal=False; 자신.시작화면=False; 자신.informatie_afgesloten=False

    def e_mailen(자신, gegevens):
        if not gegevens or 자신.informatie_afgesloten: return
        with 자신.vergrendelen_WAARDE:
            try: 자신.Proces.stdin.write(gegevens); 자신.Proces.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                gegevens=자신.Proces.stdout.read(4096)
                if not gegevens: break
                sys.stdout.buffer.write(gegevens); sys.stdout.buffer.flush()
                끝부분=(끝부분+gegevens)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); informatie_afgesloten=끝부분.rfind(b'TERMINAL CLOSED'); tekening_scherm=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,informatie_afgesloten,tekening_scherm,종료됨)>=0:
                    자신.terminal=열림>max(informatie_afgesloten,tekening_scherm,종료됨)
                    자신.시작화면=tekening_scherm>max(열림,informatie_afgesloten,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.e_mailen(b'terminal\n')
        finally: 자신.informatie_afgesloten=True

    def client(자신, client, pad):
        server_WAARDE=socket.socket(socket.AF_UNIX); server_WAARDE.settimeout(10); client.settimeout(10)
        toetsenbord_invoer=toetsenbord(자신.e_mailen,lambda 한글여부:자신.e_mailen(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_WAARDE.connect(str(pad))
            # begintoestand 협상은 순서대로 끝낸다. 이후 tekstuitvoer 가닥만 클라이언트에 쓴다.
            client.sendall(GELIJK_WAARDE(server_WAARDE,12))
            versienummer=GELIJK_WAARDE(client,12)
            if versienummer not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_WAARDE.sendall(versienummer)
            item_AANTAL=GELIJK_WAARDE(server_WAARDE,1);client.sendall(item_AANTAL+GELIJK_WAARDE(server_WAARDE,item_AANTAL[0]))
            Beveiliging=GELIJK_WAARDE(client,1)
            if Beveiliging!=b'\x01': raise ValueError('unexpected security type')
            server_WAARDE.sendall(Beveiliging)
            if versienummer==b'RFB 003.008\n':client.sendall(GELIJK_WAARDE(server_WAARDE,4))
            server_WAARDE.sendall(GELIJK_WAARDE(client,1))
            초기값=GELIJK_WAARDE(server_WAARDE,24)
            client.sendall(초기값+GELIJK_WAARDE(server_WAARDE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            client.settimeout(None);server_WAARDE.settimeout(None)
            def uitvoer():
                try:
                    while True:
                        gebied_WAARDE=GELIJK_WAARDE(server_WAARDE,1)[0]
                        if gebied_WAARDE==0:
                            kop_WAARDE=GELIJK_WAARDE(server_WAARDE,3);invoer_AANTAL_8f7753a1=struct.unpack('>H',kop_WAARDE[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 extern_WAARDE_28edcfa1 포인터의 중복을 피한다.
                            Verborgen_WAARDE=포인터지원
                            if Verborgen_WAARDE:client.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            client.sendall(bytes([gebied_WAARDE])+kop_WAARDE)
                            for _ in range(invoer_AANTAL_8f7753a1):
                                rechthoek=GELIJK_WAARDE(server_WAARDE,12);가로,Verticaal_functie,폭,hoogte_WAARDE,Encoding_WAARDE=struct.unpack('>HHHHi',rechthoek)
                                if Encoding_WAARDE!=0:raise ValueError('unexpected framebuffer encoding: '+str(Encoding_WAARDE))
                                client.sendall(rechthoek)
                                남음=폭*hoogte_WAARDE*화소바이트
                                while 남음:
                                    gegevens=GELIJK_WAARDE(server_WAARDE,min(남음,65536));client.sendall(gegevens);남음-=len(gegevens)
                        elif gebied_WAARDE==1:
                            kop_WAARDE=GELIJK_WAARDE(server_WAARDE,5);item_AANTAL=struct.unpack('>H',kop_WAARDE[3:])[0]
                            client.sendall(bytes([gebied_WAARDE])+kop_WAARDE+GELIJK_WAARDE(server_WAARDE,item_AANTAL*6))
                        elif gebied_WAARDE==2:client.sendall(bytes([gebied_WAARDE]))
                        elif gebied_WAARDE==3:
                            kop_WAARDE=GELIJK_WAARDE(server_WAARDE,7);item_AANTAL=struct.unpack('>I',kop_WAARDE[3:])[0]
                            if item_AANTAL>1048576:raise ValueError('server clipboard too large')
                            client.sendall(bytes([gebied_WAARDE])+kop_WAARDE+GELIJK_WAARDE(server_WAARDE,item_AANTAL))
                        else:raise ValueError('unexpected RFB server message: '+str(gebied_WAARDE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:client.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            achtergrondwerker=threading.Thread(target=uitvoer,daemon=True);achtergrondwerker.start()
            while not 자신.informatie_afgesloten:
                gebied_WAARDE=GELIJK_WAARDE(client,1)[0]
                if gebied_WAARDE==4:
                    hoofdtekst=GELIJK_WAARDE(client,7); toetsenbord_invoer.누름값(hoofdtekst[0]!=0,struct.unpack('>I',hoofdtekst[3:])[0]); continue
                if gebied_WAARDE==255:
                    hoofdtekst=GELIJK_WAARDE(client,11)
                    if hoofdtekst[0]!=0: raise ValueError('unsupported QEMU input extension')
                    toetsenbord_invoer.누름값(struct.unpack('>H',hoofdtekst[1:3])[0]!=0,struct.unpack('>I',hoofdtekst[3:7])[0]); continue
                if gebied_WAARDE==5:
                    hoofdtekst=GELIJK_WAARDE(client,5); 단추들,x_coördinaat,Y_coördinaat=struct.unpack('>BHH',hoofdtekst)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: toetsenbord_invoer.한글조합기.doorvoeren_samenstelling()
                    if 눌림&1 and 자신.시작화면 and 64<=x_coördinaat<576 and 112<=Y_coördinaat<372:
                        ZOEKEN_INDEX=(Y_coördinaat-112)//52
                        if (Y_coördinaat-112)%52<40 and ZOEKEN_INDEX<5: 자신.e_mailen(bytes([ord('1')+ZOEKEN_INDEX]))
                    else: 자신.e_mailen(bytes([30,1,단추들,x_coördinaat&255,x_coördinaat>>8,Y_coördinaat&255,Y_coördinaat>>8]))
                    continue
                if gebied_WAARDE==6:
                    hoofdtekst=GELIJK_WAARDE(client,7); tijdsduur_WAARDE=struct.unpack('>i',hoofdtekst[3:])[0]
                    if abs(tijdsduur_WAARDE)>65536: raise ValueError('clipboard too large')
                    tekst=GELIJK_WAARDE(client,abs(tijdsduur_WAARDE))
                    if tijdsduur_WAARDE>=0:
                        try: toetsenbord_invoer.klembord_WAARDE=tekst.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: toetsenbord_invoer.klembord_WAARDE=tekst.decode('latin-1').encode('utf-8')
                        toetsenbord_invoer.klembord_WAARDE=toetsenbord_invoer.klembord_WAARDE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_WAARDE.sendall(bytes([gebied_WAARDE])+hoofdtekst+tekst); continue
                if gebied_WAARDE==0:
                    hoofdtekst=GELIJK_WAARDE(client,19)
                    if hoofdtekst[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=hoofdtekst[3]//8
                elif gebied_WAARDE==2:
                    hoofdtekst=GELIJK_WAARDE(client,3); invoer_AANTAL_8f7753a1=struct.unpack('>H',hoofdtekst[1:])[0]
                    if invoer_AANTAL_8f7753a1>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(invoer_AANTAL_8f7753a1)+'i',GELIJK_WAARDE(client,invoer_AANTAL_8f7753a1*4))
                    포인터지원=-239 in 부호들
                    # 로컬 scherm 중계는 standaardwaarde Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    hoofdtekst=struct.pack('>BHi',0,1,0)
                elif gebied_WAARDE in (3,150): hoofdtekst=GELIJK_WAARDE(client,9)
                elif gebied_WAARDE==248:
                    hoofdtekst=GELIJK_WAARDE(client,8)
                    if hoofdtekst[7]>64: raise ValueError('fence too large')
                    hoofdtekst+=GELIJK_WAARDE(client,hoofdtekst[7])
                elif gebied_WAARDE==250: hoofdtekst=GELIJK_WAARDE(client,3)
                elif gebied_WAARDE==251:
                    hoofdtekst=GELIJK_WAARDE(client,7)
                    if hoofdtekst[5]>16: raise ValueError('too many screens')
                    hoofdtekst+=GELIJK_WAARDE(client,hoofdtekst[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(gebied_WAARDE))
                server_WAARDE.sendall(bytes([gebied_WAARDE])+hoofdtekst)
        except (OSError,EOFError,ValueError) as fout:
            if str(fout): print('VNC client:',fout,file=sys.stderr,flush=True)
        finally:
            for socket_WAARDE in (client,server_WAARDE):
                try: socket_WAARDE.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                socket_WAARDE.close()


def uitvoeren_pc(poortnummer=5902, net=False, bestandsoverdracht_poortnummer=2121, 전달규칙들=(), resolutie_WAARDE=(640, 480), gast_ADRES=None, host_ADRES='127.0.0.1'):
    with ExitStack() as Bronnen, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        brug_invoer = None
        if net:
            from brug_3de4fe3a import brug_3de4fe3a
            brug_invoer = Bronnen.enter_context(brug_3de4fe3a(bestandsoverdracht_poortnummer, 전달규칙들, gast_ADRES=gast_ADRES, host_ADRES=host_ADRES))
        pad=Path(작업경로)/'display.sock'
        with socket.socket() as ontvangen_poort:
            ontvangen_poort.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            ontvangen_poort.bind(('127.0.0.1',poortnummer)); ontvangen_poort.listen(1); ontvangen_poort.settimeout(.2)
            원격화면접속번호=ontvangen_poort.getsockname()[1]
            if brug_invoer and (원격화면접속번호==bestandsoverdracht_poortnummer or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and host==원격화면접속번호 for 통신규약,host,_ in brug_invoer.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proces=subprocess.Popen(opdracht(resolutie_WAARDE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(pad)]+(brug_invoer.전달인수() if brug_invoer else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            brug=VERBINDEN_pc(Proces); Lezer=threading.Thread(target=brug.직렬입출력,daemon=True); Lezer.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(ontvangen_poort.getsockname()[1]),flush=True)
            if brug_invoer: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(host_ADRES,bestandsoverdracht_poortnummer),flush=True)
            def beëindigen(signaal_nummer,uitvoerbewerking_frame): raise KeyboardInterrupt()
            Vorige=signal.signal(signal.SIGTERM,beëindigen)
            verwerking_taak=None; 가로채기됨=False
            try:
                while Proces.poll() is None:
                    try: client,_=ontvangen_poort.accept()
                    except socket.timeout: continue
                    if verwerking_taak is not None and verwerking_taak.is_alive(): client.close(); continue
                    if not pad.exists(): client.close(); continue
                    verwerking_taak=threading.Thread(target=brug.client,args=(client,pad),daemon=True); verwerking_taak.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                brug.informatie_afgesloten=True
                if brug_invoer: brug_invoer.Onderbreken_gebeurtenis.set()
                if Proces.poll() is None:
                    Proces.terminate()
                    try: Proces.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
                Lezer.join(timeout=2); Proces.stdin.close(); Proces.stdout.close(); signal.signal(signal.SIGTERM,Vorige)
            if brug_invoer and brug_invoer.fout: raise RuntimeError('network bridge: '+brug_invoer.fout)
            return 0 if 가로채기됨 else Proces.returncode


if __name__=='__main__':
    from Uitvoeren_opdracht import 해상도읽기
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    argument_MATRIX=parser.parse_args()
    if argument_MATRIX.forward and not argument_MATRIX.network: parser.error('--forward requires --network')
    raise SystemExit(uitvoeren_pc(argument_MATRIX.port,net=argument_MATRIX.network,bestandsoverdracht_poortnummer=argument_MATRIX.ftp_port,전달규칙들=argument_MATRIX.forward,resolutie_WAARDE=argument_MATRIX.resolution))
