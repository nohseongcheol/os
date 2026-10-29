#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Võti_VALUE 입력은 oma tuum_VALUE UART로 전달한다. localhost 전용, 단일 meede_VALUE 클라이언트.
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
from Täida_käsk import Käsk
from local_input import create


def EXACT_VALUE(소켓, Suurus):
    andmed = bytearray()
    while len(andmed) < Suurus:
        조각 = 소켓.recv(Suurus - len(andmed))
        if not 조각: raise EOFError()
        andmed.extend(조각)
    return bytes(andmed)


class klaviatuur:
    def __init__(자신, saatma, 입력방식알림=None):
        자신.바이트전송 = saatma; 자신.muuteklahv = set(); 자신.lõikelaud_VALUE = b''
        자신.한글조합기 = create(saatma, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Võti = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def saatma(자신, andmed):
        자신.한글조합기.kinnitamine_koosseis()
        자신.바이트전송(andmed)

    def SWITCH_MODE(자신):
        자신.한글조합기.kinnitamine_koosseis(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Võti_sümbol):
        if Võti_sümbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.muuteklahv.add(Võti_sümbol)
            else: 자신.muuteklahv.discard(Võti_sümbol)
            return
        if not 누르는중:
            자신.SWITCH_Võti.discard(Võti_sümbol)
            return
        meede_Võti = bool(자신.muuteklahv & {0xffe3, 0xffe4})
        윗글쇠 = bool(자신.muuteklahv & {0xffe1, 0xffe2})
        if meede_Võti and 윗글쇠 and Võti_sümbol in (ord('u'),ord('U')):
            자신.한글조합기.kinnitamine_koosseis(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Võti_sümbol in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.saatma(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Võti_sümbol==0xff1b: 자신.유니코드입력=None
            elif Võti_sümbol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Võti_sümbol<128 and chr(Võti_sümbol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Võti_sümbol)
            return
        if Võti_sümbol in (0xff31,0xffc6) or Võti_sümbol==32 and 윗글쇠 and not meede_Võti:
            if Võti_sümbol not in 자신.SWITCH_Võti: 자신.SWITCH_MODE()
            자신.SWITCH_Võti.add(Võti_sümbol)
            return
        if Võti_sümbol==0xff08 and 자신.한글여부 and not meede_Võti and 자신.한글조합기.앞글자지우기(): return
        if meede_Võti and 윗글쇠 and Võti_sümbol in (ord('t'),ord('T')):
            자신.saatma(bytes([30,2,1,0,0,0,0])); return
        if Võti_sümbol==0xffc3: 자신.saatma(bytes([30,2,2,0,0,0,0])); return
        if Võti_sümbol==0xffc9: 자신.saatma(bytes([30,2,3,0,0,0,0])); return
        if meede_Võti and 윗글쇠 and Võti_sümbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.saatma(자신.lõikelaud_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Võti_sümbol in 특수글쇠: 자신.saatma(특수글쇠[Võti_sümbol]); return
        märk_kodeerimine = Võti_sümbol & 0xffffff if Võti_sümbol & 0xff000000 == 0x01000000 else Võti_sümbol
        if märk_kodeerimine > 0x10ffff or 0xd800 <= märk_kodeerimine <= 0xdfff or Võti_sümbol >= 0xff00 and Võti_sümbol < 0x1000000: return
        if meede_Võti and 0x40 <= märk_kodeerimine <= 0x7f: 자신.saatma(bytes([märk_kodeerimine & 31])); return
        if märk_kodeerimine < 32: return
        if 자신.한글여부 and 자신.muuteklahv & {0xffea,0xfe03,0xff7e} and not meede_Võti and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.vood_Võti(chr(märk_kodeerimine), altgr=True): return
        앞부분 = b'\x1b' if 자신.muuteklahv & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not meede_Võti and not 앞부분 and 32<=märk_kodeerimine<127:
            tähemärgiandmed=chr(märk_kodeerimine).upper() if 윗글쇠 else chr(märk_kodeerimine)
            if 자신.한글조합기.vood_Võti(tähemärgiandmed): return
        자신.saatma(앞부분 + chr(märk_kodeerimine).encode('utf-8'))


class Ühenda_töölaud:
    def __init__(자신, Protsess):
        자신.Protsess=Protsess; 자신.lukk_VALUE=threading.Lock(); 자신.준비완료=False; 자신.terminal=False; 자신.시작화면=False; 자신.infotehnoloogia_suletud=False

    def saatma(자신, andmed):
        if not andmed or 자신.infotehnoloogia_suletud: return
        with 자신.lukk_VALUE:
            try: 자신.Protsess.stdin.write(andmed); 자신.Protsess.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                andmed=자신.Protsess.stdout.read(4096)
                if not andmed: break
                sys.stdout.buffer.write(andmed); sys.stdout.buffer.flush()
                끝부분=(끝부분+andmed)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); infotehnoloogia_suletud=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,infotehnoloogia_suletud,그림화면,종료됨)>=0:
                    자신.terminal=열림>max(infotehnoloogia_suletud,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,infotehnoloogia_suletud,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.saatma(b'terminal\n')
        finally: 자신.infotehnoloogia_suletud=True

    def klient(자신, klient, RADA):
        server_VALUE=socket.socket(socket.AF_UNIX); server_VALUE.settimeout(10); klient.settimeout(10)
        klaviatuur_kirje=klaviatuur(자신.saatma,lambda 한글여부:자신.saatma(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VALUE.connect(str(RADA))
            # lähteolek 협상은 순서대로 끝낸다. 이후 Väljund 가닥만 클라이언트에 쓴다.
            klient.sendall(EXACT_VALUE(server_VALUE,12))
            versiooninumber=EXACT_VALUE(klient,12)
            if versiooninumber not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VALUE.sendall(versiooninumber)
            kaup_COUNT=EXACT_VALUE(server_VALUE,1);klient.sendall(kaup_COUNT+EXACT_VALUE(server_VALUE,kaup_COUNT[0]))
            Turve=EXACT_VALUE(klient,1)
            if Turve!=b'\x01': raise ValueError('unexpected security type')
            server_VALUE.sendall(Turve)
            if versiooninumber==b'RFB 003.008\n':klient.sendall(EXACT_VALUE(server_VALUE,4))
            server_VALUE.sendall(EXACT_VALUE(klient,1))
            초기값=EXACT_VALUE(server_VALUE,24)
            klient.sendall(초기값+EXACT_VALUE(server_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klient.settimeout(None);server_VALUE.settimeout(None)
            def toodang():
                try:
                    while True:
                        ala_VALUE=EXACT_VALUE(server_VALUE,1)[0]
                        if ala_VALUE==0:
                            머리=EXACT_VALUE(server_VALUE,3);kirje_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 kauge_VALUE 포인터의 중복을 피한다.
                            Peidetud_VALUE=포인터지원
                            if Peidetud_VALUE:klient.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klient.sendall(bytes([ala_VALUE])+머리)
                            for _ in range(kirje_COUNT):
                                ristkülik=EXACT_VALUE(server_VALUE,12);가로,vertikaal_ametikoht,폭,높이,kodeerimine_VALUE=struct.unpack('>HHHHi',ristkülik)
                                if kodeerimine_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodeerimine_VALUE))
                                klient.sendall(ristkülik)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    andmed=EXACT_VALUE(server_VALUE,min(남음,65536));klient.sendall(andmed);남음-=len(andmed)
                        elif ala_VALUE==1:
                            머리=EXACT_VALUE(server_VALUE,5);kaup_COUNT=struct.unpack('>H',머리[3:])[0]
                            klient.sendall(bytes([ala_VALUE])+머리+EXACT_VALUE(server_VALUE,kaup_COUNT*6))
                        elif ala_VALUE==2:klient.sendall(bytes([ala_VALUE]))
                        elif ala_VALUE==3:
                            머리=EXACT_VALUE(server_VALUE,7);kaup_COUNT=struct.unpack('>I',머리[3:])[0]
                            if kaup_COUNT>1048576:raise ValueError('server clipboard too large')
                            klient.sendall(bytes([ala_VALUE])+머리+EXACT_VALUE(server_VALUE,kaup_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(ala_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klient.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            töötaja=threading.Thread(target=toodang,daemon=True);töötaja.start()
            while not 자신.infotehnoloogia_suletud:
                ala_VALUE=EXACT_VALUE(klient,1)[0]
                if ala_VALUE==4:
                    sisu_SMS=EXACT_VALUE(klient,7); klaviatuur_kirje.누름값(sisu_SMS[0]!=0,struct.unpack('>I',sisu_SMS[3:])[0]); continue
                if ala_VALUE==255:
                    sisu_SMS=EXACT_VALUE(klient,11)
                    if sisu_SMS[0]!=0: raise ValueError('unsupported QEMU input extension')
                    klaviatuur_kirje.누름값(struct.unpack('>H',sisu_SMS[1:3])[0]!=0,struct.unpack('>I',sisu_SMS[3:7])[0]); continue
                if ala_VALUE==5:
                    sisu_SMS=EXACT_VALUE(klient,5); 단추들,가로좌표,세로좌표=struct.unpack('>BHH',sisu_SMS)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: klaviatuur_kirje.한글조합기.kinnitamine_koosseis()
                    if 눌림&1 and 자신.시작화면 and 64<=가로좌표<576 and 112<=세로좌표<372:
                        LOOKUP_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and LOOKUP_INDEX<5: 자신.saatma(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.saatma(bytes([30,1,단추들,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if ala_VALUE==6:
                    sisu_SMS=EXACT_VALUE(klient,7); 길이=struct.unpack('>i',sisu_SMS[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    Tekst=EXACT_VALUE(klient,abs(길이))
                    if 길이>=0:
                        try: klaviatuur_kirje.lõikelaud_VALUE=Tekst.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: klaviatuur_kirje.lõikelaud_VALUE=Tekst.decode('latin-1').encode('utf-8')
                        klaviatuur_kirje.lõikelaud_VALUE=klaviatuur_kirje.lõikelaud_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VALUE.sendall(bytes([ala_VALUE])+sisu_SMS+Tekst); continue
                if ala_VALUE==0:
                    sisu_SMS=EXACT_VALUE(klient,19)
                    if sisu_SMS[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=sisu_SMS[3]//8
                elif ala_VALUE==2:
                    sisu_SMS=EXACT_VALUE(klient,3); kirje_COUNT=struct.unpack('>H',sisu_SMS[1:])[0]
                    if kirje_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(kirje_COUNT)+'i',EXACT_VALUE(klient,kirje_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 vaikeväärtus Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    sisu_SMS=struct.pack('>BHi',0,1,0)
                elif ala_VALUE in (3,150): sisu_SMS=EXACT_VALUE(klient,9)
                elif ala_VALUE==248:
                    sisu_SMS=EXACT_VALUE(klient,8)
                    if sisu_SMS[7]>64: raise ValueError('fence too large')
                    sisu_SMS+=EXACT_VALUE(klient,sisu_SMS[7])
                elif ala_VALUE==250: sisu_SMS=EXACT_VALUE(klient,3)
                elif ala_VALUE==251:
                    sisu_SMS=EXACT_VALUE(klient,7)
                    if sisu_SMS[5]>16: raise ValueError('too many screens')
                    sisu_SMS+=EXACT_VALUE(klient,sisu_SMS[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ala_VALUE))
                server_VALUE.sendall(bytes([ala_VALUE])+sisu_SMS)
        except (OSError,EOFError,ValueError) as VIGA:
            if str(VIGA): print('VNC client:',VIGA,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (klient,server_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def sari_töölaud(pordinumber=5902, võrk=False, failiedastus_pordinumber=2121, 전달규칙들=(), eraldusvõime_VALUE=(640, 480), külaline_ADDRESS=None, host_ADDRESS='127.0.0.1'):
    with ExitStack() as Ressursid, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        sild_kirje = None
        if võrk:
            from sild_3de4fe3a import sild_3de4fe3a
            sild_kirje = Ressursid.enter_context(sild_3de4fe3a(failiedastus_pordinumber, 전달규칙들, külaline_ADDRESS=külaline_ADDRESS, host_ADDRESS=host_ADDRESS))
        RADA=Path(작업경로)/'display.sock'
        with socket.socket() as saama_port:
            saama_port.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            saama_port.bind(('127.0.0.1',pordinumber)); saama_port.listen(1); saama_port.settimeout(.2)
            원격화면접속번호=saama_port.getsockname()[1]
            if sild_kirje and (원격화면접속번호==failiedastus_pordinumber or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and host==원격화면접속번호 for 통신규약,host,_ in sild_kirje.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Protsess=subprocess.Popen(Käsk(eraldusvõime_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(RADA)]+(sild_kirje.전달인수() if sild_kirje else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            sild=Ühenda_töölaud(Protsess); Reader=threading.Thread(target=sild.직렬입출력,daemon=True); Reader.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(saama_port.getsockname()[1]),flush=True)
            if sild_kirje: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(host_ADDRESS,failiedastus_pordinumber),flush=True)
            def 종료시키기(signaal_number,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            töötlemine_tööüksus=None; 가로채기됨=False
            try:
                while Protsess.poll() is None:
                    try: klient,_=saama_port.accept()
                    except socket.timeout: continue
                    if töötlemine_tööüksus is not None and töötlemine_tööüksus.is_alive(): klient.close(); continue
                    if not RADA.exists(): klient.close(); continue
                    töötlemine_tööüksus=threading.Thread(target=sild.klient,args=(klient,RADA),daemon=True); töötlemine_tööüksus.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                sild.infotehnoloogia_suletud=True
                if sild_kirje: sild_kirje.Peata_sündmus.set()
                if Protsess.poll() is None:
                    Protsess.terminate()
                    try: Protsess.wait(timeout=5)
                    except subprocess.TimeoutExpired: Protsess.kill(); Protsess.wait()
                Reader.join(timeout=2); Protsess.stdin.close(); Protsess.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if sild_kirje and sild_kirje.VIGA: raise RuntimeError('network bridge: '+sild_kirje.VIGA)
            return 0 if 가로채기됨 else Protsess.returncode


if __name__=='__main__':
    from Täida_käsk import 해상도읽기
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    argument_ARRAY=parser.parse_args()
    if argument_ARRAY.forward and not argument_ARRAY.network: parser.error('--forward requires --network')
    raise SystemExit(sari_töölaud(argument_ARRAY.port,võrk=argument_ARRAY.network,failiedastus_pordinumber=argument_ARRAY.ftp_port,전달규칙들=argument_ARRAY.forward,eraldusvõime_VALUE=argument_ARRAY.resolution))
