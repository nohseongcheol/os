#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Cheie_VALUE 입력은 propriu nucleu_VALUE UART로 전달한다. localhost 전용, 단일 control_VALUE 클라이언트.
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
from executa_comandă import Comandă
from local_input import create


def EXACT_VALUE(소켓, Mărime):
    date = bytearray()
    while len(date) < Mărime:
        조각 = 소켓.recv(Mărime - len(date))
        if not 조각: raise EOFError()
        date.extend(조각)
    return bytes(date)


class tastatură:
    def __init__(자신, trimite, 입력방식알림=None):
        자신.바이트전송 = trimite; 자신.tastă_modificatoare = set(); 자신.clipboard_VALUE = b''
        자신.한글조합기 = create(trimite, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Cheie = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def trimite(자신, date):
        자신.한글조합기.조합확정()
        자신.바이트전송(date)

    def SWITCH_mod(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Cheie_simbol):
        if Cheie_simbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.tastă_modificatoare.add(Cheie_simbol)
            else: 자신.tastă_modificatoare.discard(Cheie_simbol)
            return
        if not 누르는중:
            자신.SWITCH_Cheie.discard(Cheie_simbol)
            return
        control_Cheie = bool(자신.tastă_modificatoare & {0xffe3, 0xffe4})
        윗글쇠 = bool(자신.tastă_modificatoare & {0xffe1, 0xffe2})
        if control_Cheie and 윗글쇠 and Cheie_simbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Cheie_simbol in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.trimite(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Cheie_simbol==0xff1b: 자신.유니코드입력=None
            elif Cheie_simbol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Cheie_simbol<128 and chr(Cheie_simbol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Cheie_simbol)
            return
        if Cheie_simbol in (0xff31,0xffc6) or Cheie_simbol==32 and 윗글쇠 and not control_Cheie:
            if Cheie_simbol not in 자신.SWITCH_Cheie: 자신.SWITCH_mod()
            자신.SWITCH_Cheie.add(Cheie_simbol)
            return
        if Cheie_simbol==0xff08 and 자신.한글여부 and not control_Cheie and 자신.한글조합기.앞글자지우기(): return
        if control_Cheie and 윗글쇠 and Cheie_simbol in (ord('t'),ord('T')):
            자신.trimite(bytes([30,2,1,0,0,0,0])); return
        if Cheie_simbol==0xffc3: 자신.trimite(bytes([30,2,2,0,0,0,0])); return
        if Cheie_simbol==0xffc9: 자신.trimite(bytes([30,2,3,0,0,0,0])); return
        if control_Cheie and 윗글쇠 and Cheie_simbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.trimite(자신.clipboard_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Cheie_simbol in 특수글쇠: 자신.trimite(특수글쇠[Cheie_simbol]); return
        codificare_caractere = Cheie_simbol & 0xffffff if Cheie_simbol & 0xff000000 == 0x01000000 else Cheie_simbol
        if codificare_caractere > 0x10ffff or 0xd800 <= codificare_caractere <= 0xdfff or Cheie_simbol >= 0xff00 and Cheie_simbol < 0x1000000: return
        if control_Cheie and 0x40 <= codificare_caractere <= 0x7f: 자신.trimite(bytes([codificare_caractere & 31])); return
        if codificare_caractere < 32: return
        if 자신.한글여부 and 자신.tastă_modificatoare & {0xffea,0xfe03,0xff7e} and not control_Cheie and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.flux_Cheie(chr(codificare_caractere), altgr=True): return
        앞부분 = b'\x1b' if 자신.tastă_modificatoare & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not control_Cheie and not 앞부분 and 32<=codificare_caractere<127:
            date_de_tip_caracter=chr(codificare_caractere).upper() if 윗글쇠 else chr(codificare_caractere)
            if 자신.한글조합기.flux_Cheie(date_de_tip_caracter): return
        자신.trimite(앞부분 + chr(codificare_caractere).encode('utf-8'))


class conecta_desktop:
    def __init__(자신, Proces):
        자신.Proces=Proces; 자신.blocare_VALUE=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def trimite(자신, date):
        if not date or 자신.닫힘: return
        with 자신.blocare_VALUE:
            try: 자신.Proces.stdin.write(date); 자신.Proces.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                date=자신.Proces.stdout.read(4096)
                if not date: break
                sys.stdout.buffer.write(date); sys.stdout.buffer.flush()
                끝부분=(끝부분+date)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.trimite(b'terminal\n')
        finally: 자신.닫힘=True

    def client(자신, client, Cale):
        server_VALUE=socket.socket(socket.AF_UNIX); server_VALUE.settimeout(10); client.settimeout(10)
        tastatură_intrare=tastatură(자신.trimite,lambda 한글여부:자신.trimite(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VALUE.connect(str(Cale))
            # stare_inițială 협상은 순서대로 끝낸다. 이후 Rezultat 가닥만 클라이언트에 쓴다.
            client.sendall(EXACT_VALUE(server_VALUE,12))
            număr_de_versiune=EXACT_VALUE(client,12)
            if număr_de_versiune not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VALUE.sendall(număr_de_versiune)
            element_COUNT=EXACT_VALUE(server_VALUE,1);client.sendall(element_COUNT+EXACT_VALUE(server_VALUE,element_COUNT[0]))
            Securitate=EXACT_VALUE(client,1)
            if Securitate!=b'\x01': raise ValueError('unexpected security type')
            server_VALUE.sendall(Securitate)
            if număr_de_versiune==b'RFB 003.008\n':client.sendall(EXACT_VALUE(server_VALUE,4))
            server_VALUE.sendall(EXACT_VALUE(client,1))
            초기값=EXACT_VALUE(server_VALUE,24)
            client.sendall(초기값+EXACT_VALUE(server_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            client.settimeout(None);server_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        zonă_VALUE=EXACT_VALUE(server_VALUE,1)[0]
                        if zonă_VALUE==0:
                            머리=EXACT_VALUE(server_VALUE,3);intrare_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 la_distanță_VALUE 포인터의 중복을 피한다.
                            Ascunsă_VALUE=포인터지원
                            if Ascunsă_VALUE:client.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            client.sendall(bytes([zonă_VALUE])+머리)
                            for _ in range(intrare_COUNT):
                                dreptunghi=EXACT_VALUE(server_VALUE,12);가로,Verticală_poziție,폭,높이,codificare_VALUE=struct.unpack('>HHHHi',dreptunghi)
                                if codificare_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(codificare_VALUE))
                                client.sendall(dreptunghi)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    date=EXACT_VALUE(server_VALUE,min(남음,65536));client.sendall(date);남음-=len(date)
                        elif zonă_VALUE==1:
                            머리=EXACT_VALUE(server_VALUE,5);element_COUNT=struct.unpack('>H',머리[3:])[0]
                            client.sendall(bytes([zonă_VALUE])+머리+EXACT_VALUE(server_VALUE,element_COUNT*6))
                        elif zonă_VALUE==2:client.sendall(bytes([zonă_VALUE]))
                        elif zonă_VALUE==3:
                            머리=EXACT_VALUE(server_VALUE,7);element_COUNT=struct.unpack('>I',머리[3:])[0]
                            if element_COUNT>1048576:raise ValueError('server clipboard too large')
                            client.sendall(bytes([zonă_VALUE])+머리+EXACT_VALUE(server_VALUE,element_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(zonă_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:client.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                zonă_VALUE=EXACT_VALUE(client,1)[0]
                if zonă_VALUE==4:
                    text_corp=EXACT_VALUE(client,7); tastatură_intrare.누름값(text_corp[0]!=0,struct.unpack('>I',text_corp[3:])[0]); continue
                if zonă_VALUE==255:
                    text_corp=EXACT_VALUE(client,11)
                    if text_corp[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tastatură_intrare.누름값(struct.unpack('>H',text_corp[1:3])[0]!=0,struct.unpack('>I',text_corp[3:7])[0]); continue
                if zonă_VALUE==5:
                    text_corp=EXACT_VALUE(client,5); 단추들,coordonata_X,세로좌표=struct.unpack('>BHH',text_corp)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tastatură_intrare.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=coordonata_X<576 and 112<=세로좌표<372:
                        LOOKUP_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and LOOKUP_INDEX<5: 자신.trimite(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.trimite(bytes([30,1,단추들,coordonata_X&255,coordonata_X>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if zonă_VALUE==6:
                    text_corp=EXACT_VALUE(client,7); lungime_VALUE=struct.unpack('>i',text_corp[3:])[0]
                    if abs(lungime_VALUE)>65536: raise ValueError('clipboard too large')
                    SMS=EXACT_VALUE(client,abs(lungime_VALUE))
                    if lungime_VALUE>=0:
                        try: tastatură_intrare.clipboard_VALUE=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tastatură_intrare.clipboard_VALUE=SMS.decode('latin-1').encode('utf-8')
                        tastatură_intrare.clipboard_VALUE=tastatură_intrare.clipboard_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VALUE.sendall(bytes([zonă_VALUE])+text_corp+SMS); continue
                if zonă_VALUE==0:
                    text_corp=EXACT_VALUE(client,19)
                    if text_corp[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=text_corp[3]//8
                elif zonă_VALUE==2:
                    text_corp=EXACT_VALUE(client,3); intrare_COUNT=struct.unpack('>H',text_corp[1:])[0]
                    if intrare_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(intrare_COUNT)+'i',EXACT_VALUE(client,intrare_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 valoare_implicită Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    text_corp=struct.pack('>BHi',0,1,0)
                elif zonă_VALUE in (3,150): text_corp=EXACT_VALUE(client,9)
                elif zonă_VALUE==248:
                    text_corp=EXACT_VALUE(client,8)
                    if text_corp[7]>64: raise ValueError('fence too large')
                    text_corp+=EXACT_VALUE(client,text_corp[7])
                elif zonă_VALUE==250: text_corp=EXACT_VALUE(client,3)
                elif zonă_VALUE==251:
                    text_corp=EXACT_VALUE(client,7)
                    if text_corp[5]>16: raise ValueError('too many screens')
                    text_corp+=EXACT_VALUE(client,text_corp[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(zonă_VALUE))
                server_VALUE.sendall(bytes([zonă_VALUE])+text_corp)
        except (OSError,EOFError,ValueError) as eroare:
            if str(eroare): print('VNC client:',eroare,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (client,server_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def rula_desktop(număr_port=5902, rețea=False, transfer_de_fișiere_număr_port=2121, 전달규칙들=(), rezoluție_VALUE=(640, 480), invitat_adresa=None, gazdă_adresa='127.0.0.1'):
    with ExitStack() as Resurse, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        punte_intrare = None
        if rețea:
            from punte_3de4fe3a import punte_3de4fe3a
            punte_intrare = Resurse.enter_context(punte_3de4fe3a(transfer_de_fișiere_număr_port, 전달규칙들, invitat_adresa=invitat_adresa, gazdă_adresa=gazdă_adresa))
        Cale=Path(작업경로)/'display.sock'
        with socket.socket() as primi_muta:
            primi_muta.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            primi_muta.bind(('127.0.0.1',număr_port)); primi_muta.listen(1); primi_muta.settimeout(.2)
            원격화면접속번호=primi_muta.getsockname()[1]
            if punte_intrare and (원격화면접속번호==transfer_de_fișiere_număr_port or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and gazdă==원격화면접속번호 for 통신규약,gazdă,_ in punte_intrare.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proces=subprocess.Popen(Comandă(rezoluție_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Cale)]+(punte_intrare.전달인수() if punte_intrare else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            punte=conecta_desktop(Proces); Reader=threading.Thread(target=punte.직렬입출력,daemon=True); Reader.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(primi_muta.getsockname()[1]),flush=True)
            if punte_intrare: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(gazdă_adresa,transfer_de_fișiere_număr_port),flush=True)
            def 종료시키기(신호번호,executare_cadru): raise KeyboardInterrupt()
            Anteriorul=signal.signal(signal.SIGTERM,종료시키기)
            procesare_sarcină=None; 가로채기됨=False
            try:
                while Proces.poll() is None:
                    try: client,_=primi_muta.accept()
                    except socket.timeout: continue
                    if procesare_sarcină is not None and procesare_sarcină.is_alive(): client.close(); continue
                    if not Cale.exists(): client.close(); continue
                    procesare_sarcină=threading.Thread(target=punte.client,args=(client,Cale),daemon=True); procesare_sarcină.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                punte.닫힘=True
                if punte_intrare: punte_intrare.Pauză_eveniment.set()
                if Proces.poll() is None:
                    Proces.terminate()
                    try: Proces.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
                Reader.join(timeout=2); Proces.stdin.close(); Proces.stdout.close(); signal.signal(signal.SIGTERM,Anteriorul)
            if punte_intrare and punte_intrare.eroare: raise RuntimeError('network bridge: '+punte_intrare.eroare)
            return 0 if 가로채기됨 else Proces.returncode


if __name__=='__main__':
    from executa_comandă import 해상도읽기
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    argument_ARRAY=parser.parse_args()
    if argument_ARRAY.forward and not argument_ARRAY.network: parser.error('--forward requires --network')
    raise SystemExit(rula_desktop(argument_ARRAY.port,rețea=argument_ARRAY.network,transfer_de_fișiere_număr_port=argument_ARRAY.ftp_port,전달규칙들=argument_ARRAY.forward,rezoluție_VALUE=argument_ARRAY.resolution))
