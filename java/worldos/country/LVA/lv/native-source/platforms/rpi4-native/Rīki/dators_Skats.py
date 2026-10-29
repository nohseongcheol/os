#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Atslēga_VALUE 입력은 savs kodols_VALUE UART로 전달한다. localhost 전용, 단일 vadība_VALUE 클라이언트.
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
from Izpildīt_komanda import Komanda
from local_input import create


def EXACT_VALUE(소켓, Izmērs):
    dati = bytearray()
    while len(dati) < Izmērs:
        조각 = 소켓.recv(Izmērs - len(dati))
        if not 조각: raise EOFError()
        dati.extend(조각)
    return bytes(dati)


class tastatūra:
    def __init__(자신, sūtīt, 입력방식알림=None):
        자신.바이트전송 = sūtīt; 자신.modifikatora_taustiņš = set(); 자신.starpliktuve_VALUE = b''
        자신.한글조합기 = create(sūtīt, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Atslēga = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def sūtīt(자신, dati):
        자신.한글조합기.izpilde_salikums()
        자신.바이트전송(dati)

    def SWITCH_MODE(자신):
        자신.한글조합기.izpilde_salikums(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Atslēga_simbols):
        if Atslēga_simbols in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.modifikatora_taustiņš.add(Atslēga_simbols)
            else: 자신.modifikatora_taustiņš.discard(Atslēga_simbols)
            return
        if not 누르는중:
            자신.SWITCH_Atslēga.discard(Atslēga_simbols)
            return
        vadība_Atslēga = bool(자신.modifikatora_taustiņš & {0xffe3, 0xffe4})
        윗글쇠 = bool(자신.modifikatora_taustiņš & {0xffe1, 0xffe2})
        if vadība_Atslēga and 윗글쇠 and Atslēga_simbols in (ord('u'),ord('U')):
            자신.한글조합기.izpilde_salikums(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Atslēga_simbols in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.sūtīt(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Atslēga_simbols==0xff1b: 자신.유니코드입력=None
            elif Atslēga_simbols==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Atslēga_simbols<128 and chr(Atslēga_simbols) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Atslēga_simbols)
            return
        if Atslēga_simbols in (0xff31,0xffc6) or Atslēga_simbols==32 and 윗글쇠 and not vadība_Atslēga:
            if Atslēga_simbols not in 자신.SWITCH_Atslēga: 자신.SWITCH_MODE()
            자신.SWITCH_Atslēga.add(Atslēga_simbols)
            return
        if Atslēga_simbols==0xff08 and 자신.한글여부 and not vadība_Atslēga and 자신.한글조합기.앞글자지우기(): return
        if vadība_Atslēga and 윗글쇠 and Atslēga_simbols in (ord('t'),ord('T')):
            자신.sūtīt(bytes([30,2,1,0,0,0,0])); return
        if Atslēga_simbols==0xffc3: 자신.sūtīt(bytes([30,2,2,0,0,0,0])); return
        if Atslēga_simbols==0xffc9: 자신.sūtīt(bytes([30,2,3,0,0,0,0])); return
        if vadība_Atslēga and 윗글쇠 and Atslēga_simbols in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.sūtīt(자신.starpliktuve_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Atslēga_simbols in 특수글쇠: 자신.sūtīt(특수글쇠[Atslēga_simbols]); return
        rakstzīmju_kodēšana = Atslēga_simbols & 0xffffff if Atslēga_simbols & 0xff000000 == 0x01000000 else Atslēga_simbols
        if rakstzīmju_kodēšana > 0x10ffff or 0xd800 <= rakstzīmju_kodēšana <= 0xdfff or Atslēga_simbols >= 0xff00 and Atslēga_simbols < 0x1000000: return
        if vadība_Atslēga and 0x40 <= rakstzīmju_kodēšana <= 0x7f: 자신.sūtīt(bytes([rakstzīmju_kodēšana & 31])); return
        if rakstzīmju_kodēšana < 32: return
        if 자신.한글여부 and 자신.modifikatora_taustiņš & {0xffea,0xfe03,0xff7e} and not vadība_Atslēga and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.plūsma_Atslēga(chr(rakstzīmju_kodēšana), altgr=True): return
        앞부분 = b'\x1b' if 자신.modifikatora_taustiņš & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not vadība_Atslēga and not 앞부분 and 32<=rakstzīmju_kodēšana<127:
            rakstzīmju_dati=chr(rakstzīmju_kodēšana).upper() if 윗글쇠 else chr(rakstzīmju_kodēšana)
            if 자신.한글조합기.plūsma_Atslēga(rakstzīmju_dati): return
        자신.sūtīt(앞부분 + chr(rakstzīmju_kodēšana).encode('utf-8'))


class saziņa_dators:
    def __init__(자신, Process):
        자신.Process=Process; 자신.bloķēt_VALUE=threading.Lock(); 자신.준비완료=False; 자신.Terminālis=False; 자신.시작화면=False; 자신.informācijas_tehnoloģija_slēgts=False

    def sūtīt(자신, dati):
        if not dati or 자신.informācijas_tehnoloģija_slēgts: return
        with 자신.bloķēt_VALUE:
            try: 자신.Process.stdin.write(dati); 자신.Process.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                dati=자신.Process.stdout.read(4096)
                if not dati: break
                sys.stdout.buffer.write(dati); sys.stdout.buffer.flush()
                끝부분=(끝부분+dati)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); informācijas_tehnoloģija_slēgts=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,informācijas_tehnoloģija_slēgts,그림화면,종료됨)>=0:
                    자신.Terminālis=열림>max(informācijas_tehnoloģija_slēgts,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,informācijas_tehnoloģija_slēgts,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.sūtīt(b'terminal\n')
        finally: 자신.informācijas_tehnoloģija_slēgts=True

    def klients(자신, klients, CEĻŠ):
        serveris_VALUE=socket.socket(socket.AF_UNIX); serveris_VALUE.settimeout(10); klients.settimeout(10)
        tastatūra_ievade=tastatūra(자신.sūtīt,lambda 한글여부:자신.sūtīt(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            serveris_VALUE.connect(str(CEĻŠ))
            # sākumstāvoklis 협상은 순서대로 끝낸다. 이후 Izvade 가닥만 클라이언트에 쓴다.
            klients.sendall(EXACT_VALUE(serveris_VALUE,12))
            versijas_numurs=EXACT_VALUE(klients,12)
            if versijas_numurs not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            serveris_VALUE.sendall(versijas_numurs)
            krājums_COUNT=EXACT_VALUE(serveris_VALUE,1);klients.sendall(krājums_COUNT+EXACT_VALUE(serveris_VALUE,krājums_COUNT[0]))
            Drošība=EXACT_VALUE(klients,1)
            if Drošība!=b'\x01': raise ValueError('unexpected security type')
            serveris_VALUE.sendall(Drošība)
            if versijas_numurs==b'RFB 003.008\n':klients.sendall(EXACT_VALUE(serveris_VALUE,4))
            serveris_VALUE.sendall(EXACT_VALUE(klients,1))
            초기값=EXACT_VALUE(serveris_VALUE,24)
            klients.sendall(초기값+EXACT_VALUE(serveris_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klients.settimeout(None);serveris_VALUE.settimeout(None)
            def ražojums():
                try:
                    while True:
                        joma_VALUE=EXACT_VALUE(serveris_VALUE,1)[0]
                        if joma_VALUE==0:
                            머리=EXACT_VALUE(serveris_VALUE,3);ievade_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 attāls_VALUE 포인터의 중복을 피한다.
                            Slēpts_VALUE=포인터지원
                            if Slēpts_VALUE:klients.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klients.sendall(bytes([joma_VALUE])+머리)
                            for _ in range(ievade_COUNT):
                                taisnstūris=EXACT_VALUE(serveris_VALUE,12);가로,vertikāle_amats,폭,높이,kodēšana_VALUE=struct.unpack('>HHHHi',taisnstūris)
                                if kodēšana_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodēšana_VALUE))
                                klients.sendall(taisnstūris)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    dati=EXACT_VALUE(serveris_VALUE,min(남음,65536));klients.sendall(dati);남음-=len(dati)
                        elif joma_VALUE==1:
                            머리=EXACT_VALUE(serveris_VALUE,5);krājums_COUNT=struct.unpack('>H',머리[3:])[0]
                            klients.sendall(bytes([joma_VALUE])+머리+EXACT_VALUE(serveris_VALUE,krājums_COUNT*6))
                        elif joma_VALUE==2:klients.sendall(bytes([joma_VALUE]))
                        elif joma_VALUE==3:
                            머리=EXACT_VALUE(serveris_VALUE,7);krājums_COUNT=struct.unpack('>I',머리[3:])[0]
                            if krājums_COUNT>1048576:raise ValueError('server clipboard too large')
                            klients.sendall(bytes([joma_VALUE])+머리+EXACT_VALUE(serveris_VALUE,krājums_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(joma_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klients.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            nodarbinātais=threading.Thread(target=ražojums,daemon=True);nodarbinātais.start()
            while not 자신.informācijas_tehnoloģija_slēgts:
                joma_VALUE=EXACT_VALUE(klients,1)[0]
                if joma_VALUE==4:
                    pamatteksts=EXACT_VALUE(klients,7); tastatūra_ievade.누름값(pamatteksts[0]!=0,struct.unpack('>I',pamatteksts[3:])[0]); continue
                if joma_VALUE==255:
                    pamatteksts=EXACT_VALUE(klients,11)
                    if pamatteksts[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tastatūra_ievade.누름값(struct.unpack('>H',pamatteksts[1:3])[0]!=0,struct.unpack('>I',pamatteksts[3:7])[0]); continue
                if joma_VALUE==5:
                    pamatteksts=EXACT_VALUE(klients,5); 단추들,x_koordināta,세로좌표=struct.unpack('>BHH',pamatteksts)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tastatūra_ievade.한글조합기.izpilde_salikums()
                    if 눌림&1 and 자신.시작화면 and 64<=x_koordināta<576 and 112<=세로좌표<372:
                        LOOKUP_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and LOOKUP_INDEX<5: 자신.sūtīt(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.sūtīt(bytes([30,1,단추들,x_koordināta&255,x_koordināta>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if joma_VALUE==6:
                    pamatteksts=EXACT_VALUE(klients,7); 길이=struct.unpack('>i',pamatteksts[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    Teksts=EXACT_VALUE(klients,abs(길이))
                    if 길이>=0:
                        try: tastatūra_ievade.starpliktuve_VALUE=Teksts.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tastatūra_ievade.starpliktuve_VALUE=Teksts.decode('latin-1').encode('utf-8')
                        tastatūra_ievade.starpliktuve_VALUE=tastatūra_ievade.starpliktuve_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    serveris_VALUE.sendall(bytes([joma_VALUE])+pamatteksts+Teksts); continue
                if joma_VALUE==0:
                    pamatteksts=EXACT_VALUE(klients,19)
                    if pamatteksts[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=pamatteksts[3]//8
                elif joma_VALUE==2:
                    pamatteksts=EXACT_VALUE(klients,3); ievade_COUNT=struct.unpack('>H',pamatteksts[1:])[0]
                    if ievade_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(ievade_COUNT)+'i',EXACT_VALUE(klients,ievade_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 noklusējuma_vērtība Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    pamatteksts=struct.pack('>BHi',0,1,0)
                elif joma_VALUE in (3,150): pamatteksts=EXACT_VALUE(klients,9)
                elif joma_VALUE==248:
                    pamatteksts=EXACT_VALUE(klients,8)
                    if pamatteksts[7]>64: raise ValueError('fence too large')
                    pamatteksts+=EXACT_VALUE(klients,pamatteksts[7])
                elif joma_VALUE==250: pamatteksts=EXACT_VALUE(klients,3)
                elif joma_VALUE==251:
                    pamatteksts=EXACT_VALUE(klients,7)
                    if pamatteksts[5]>16: raise ValueError('too many screens')
                    pamatteksts+=EXACT_VALUE(klients,pamatteksts[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(joma_VALUE))
                serveris_VALUE.sendall(bytes([joma_VALUE])+pamatteksts)
        except (OSError,EOFError,ValueError) as Kļūda:
            if str(Kļūda): print('VNC client:',Kļūda,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (klients,serveris_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def virkne_dators(porta_numurs=5902, tīkls=False, faila_pārsūtīšana_porta_numurs=2121, 전달규칙들=(), izšķirtspēja_VALUE=(640, 480), viesis_adrese=None, viesot_adrese='127.0.0.1'):
    with ExitStack() as Resursi, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        tilts_ievade = None
        if tīkls:
            from tilts_3de4fe3a import tilts_3de4fe3a
            tilts_ievade = Resursi.enter_context(tilts_3de4fe3a(faila_pārsūtīšana_porta_numurs, 전달규칙들, viesis_adrese=viesis_adrese, viesot_adrese=viesot_adrese))
        CEĻŠ=Path(작업경로)/'display.sock'
        with socket.socket() as saņemt_ports:
            saņemt_ports.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            saņemt_ports.bind(('127.0.0.1',porta_numurs)); saņemt_ports.listen(1); saņemt_ports.settimeout(.2)
            원격화면접속번호=saņemt_ports.getsockname()[1]
            if tilts_ievade and (원격화면접속번호==faila_pārsūtīšana_porta_numurs or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and viesot==원격화면접속번호 for 통신규약,viesot,_ in tilts_ievade.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Process=subprocess.Popen(Komanda(izšķirtspēja_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(CEĻŠ)]+(tilts_ievade.전달인수() if tilts_ievade else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            tilts=saziņa_dators(Process); Lasītājs=threading.Thread(target=tilts.직렬입출력,daemon=True); Lasītājs.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(saņemt_ports.getsockname()[1]),flush=True)
            if tilts_ievade: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(viesot_adrese,faila_pārsūtīšana_porta_numurs),flush=True)
            def 종료시키기(signāls_numurs,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            apstrāde_uzdevums=None; 가로채기됨=False
            try:
                while Process.poll() is None:
                    try: klients,_=saņemt_ports.accept()
                    except socket.timeout: continue
                    if apstrāde_uzdevums is not None and apstrāde_uzdevums.is_alive(): klients.close(); continue
                    if not CEĻŠ.exists(): klients.close(); continue
                    apstrāde_uzdevums=threading.Thread(target=tilts.klients,args=(klients,CEĻŠ),daemon=True); apstrāde_uzdevums.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                tilts.informācijas_tehnoloģija_slēgts=True
                if tilts_ievade: tilts_ievade.Pauze_notikums.set()
                if Process.poll() is None:
                    Process.terminate()
                    try: Process.wait(timeout=5)
                    except subprocess.TimeoutExpired: Process.kill(); Process.wait()
                Lasītājs.join(timeout=2); Process.stdin.close(); Process.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if tilts_ievade and tilts_ievade.Kļūda: raise RuntimeError('network bridge: '+tilts_ievade.Kļūda)
            return 0 if 가로채기됨 else Process.returncode


if __name__=='__main__':
    from Izpildīt_komanda import 해상도읽기
    parsētājs=argparse.ArgumentParser(description=__doc__); parsētājs.add_argument('--port',type=int,default=5902)
    parsētājs.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parsētājs.add_argument('--network',action='store_true'); parsētājs.add_argument('--ftp-port',type=int,default=2121)
    parsētājs.add_argument('--forward',action='append',default=[])
    arg_ARRAY=parsētājs.parse_args()
    if arg_ARRAY.forward and not arg_ARRAY.network: parsētājs.error('--forward requires --network')
    raise SystemExit(virkne_dators(arg_ARRAY.port,tīkls=arg_ARRAY.network,faila_pārsūtīšana_porta_numurs=arg_ARRAY.ftp_port,전달규칙들=arg_ARRAY.forward,izšķirtspēja_VALUE=arg_ARRAY.resolution))
