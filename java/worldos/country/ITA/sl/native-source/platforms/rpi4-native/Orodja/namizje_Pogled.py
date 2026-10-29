#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Ključ_VALUE 입력은 lastno jedro_VALUE UART로 전달한다. localhost 전용, 단일 nadzor_VALUE 클라이언트.
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
from Izvedi_ukaz import Ukaz
from local_input import create


def EXACT_VALUE(vtičnica_VALUE, Velikost):
    podatki = bytearray()
    while len(podatki) < Velikost:
        조각 = vtičnica_VALUE.recv(Velikost - len(podatki))
        if not 조각: raise EOFError()
        podatki.extend(조각)
    return bytes(podatki)


class tipkovnica:
    def __init__(자신, poslati, 입력방식알림=None):
        자신.바이트전송 = poslati; 자신.modifikacijska_tipka = set(); 자신.odložišče_VALUE = b''
        자신.한글조합기 = create(poslati, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Ključ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def poslati(자신, podatki):
        자신.한글조합기.조합확정()
        자신.바이트전송(podatki)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Ključ_simbol):
        if Ključ_simbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.modifikacijska_tipka.add(Ključ_simbol)
            else: 자신.modifikacijska_tipka.discard(Ključ_simbol)
            return
        if not 누르는중:
            자신.SWITCH_Ključ.discard(Ključ_simbol)
            return
        nadzor_Ključ = bool(자신.modifikacijska_tipka & {0xffe3, 0xffe4})
        tipka_SHIFT = bool(자신.modifikacijska_tipka & {0xffe1, 0xffe2})
        if nadzor_Ključ and tipka_SHIFT and Ključ_simbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Ključ_simbol in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.poslati(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Ključ_simbol==0xff1b: 자신.유니코드입력=None
            elif Ključ_simbol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Ključ_simbol<128 and chr(Ključ_simbol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Ključ_simbol)
            return
        if Ključ_simbol in (0xff31,0xffc6) or Ključ_simbol==32 and tipka_SHIFT and not nadzor_Ključ:
            if Ključ_simbol not in 자신.SWITCH_Ključ: 자신.SWITCH_MODE()
            자신.SWITCH_Ključ.add(Ključ_simbol)
            return
        if Ključ_simbol==0xff08 and 자신.한글여부 and not nadzor_Ključ and 자신.한글조합기.앞글자지우기(): return
        if nadzor_Ključ and tipka_SHIFT and Ključ_simbol in (ord('t'),ord('T')):
            자신.poslati(bytes([30,2,1,0,0,0,0])); return
        if Ključ_simbol==0xffc3: 자신.poslati(bytes([30,2,2,0,0,0,0])); return
        if Ključ_simbol==0xffc9: 자신.poslati(bytes([30,2,3,0,0,0,0])); return
        if nadzor_Ključ and tipka_SHIFT and Ključ_simbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.poslati(자신.odložišče_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Ključ_simbol in 특수글쇠: 자신.poslati(특수글쇠[Ključ_simbol]); return
        kodiranje_znakov = Ključ_simbol & 0xffffff if Ključ_simbol & 0xff000000 == 0x01000000 else Ključ_simbol
        if kodiranje_znakov > 0x10ffff or 0xd800 <= kodiranje_znakov <= 0xdfff or Ključ_simbol >= 0xff00 and Ključ_simbol < 0x1000000: return
        if nadzor_Ključ and 0x40 <= kodiranje_znakov <= 0x7f: 자신.poslati(bytes([kodiranje_znakov & 31])); return
        if kodiranje_znakov < 32: return
        if 자신.한글여부 and 자신.modifikacijska_tipka & {0xffea,0xfe03,0xff7e} and not nadzor_Ključ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.vir_Ključ(chr(kodiranje_znakov), altgr=True): return
        앞부분 = b'\x1b' if 자신.modifikacijska_tipka & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not nadzor_Ključ and not 앞부분 and 32<=kodiranje_znakov<127:
            znakovni_podatki=chr(kodiranje_znakov).upper() if tipka_SHIFT else chr(kodiranje_znakov)
            if 자신.한글조합기.vir_Ključ(znakovni_podatki): return
        자신.poslati(앞부분 + chr(kodiranje_znakov).encode('utf-8'))


class POVEŽI_namizje:
    def __init__(자신, Opravilo):
        자신.Opravilo=Opravilo; 자신.zaklepanje_VALUE=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def poslati(자신, podatki):
        if not podatki or 자신.닫힘: return
        with 자신.zaklepanje_VALUE:
            try: 자신.Opravilo.stdin.write(podatki); 자신.Opravilo.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                podatki=자신.Opravilo.stdout.read(4096)
                if not podatki: break
                sys.stdout.buffer.write(podatki); sys.stdout.buffer.flush()
                끝부분=(끝부분+podatki)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.poslati(b'terminal\n')
        finally: 자신.닫힘=True

    def odjemalec(자신, odjemalec, POT):
        strežnik_VALUE=socket.socket(socket.AF_UNIX); strežnik_VALUE.settimeout(10); odjemalec.settimeout(10)
        tipkovnica_vnos=tipkovnica(자신.poslati,lambda 한글여부:자신.poslati(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            strežnik_VALUE.connect(str(POT))
            # začetno_stanje 협상은 순서대로 끝낸다. 이후 Izpis 가닥만 클라이언트에 쓴다.
            odjemalec.sendall(EXACT_VALUE(strežnik_VALUE,12))
            številka_različice=EXACT_VALUE(odjemalec,12)
            if številka_različice not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            strežnik_VALUE.sendall(številka_različice)
            element_COUNT=EXACT_VALUE(strežnik_VALUE,1);odjemalec.sendall(element_COUNT+EXACT_VALUE(strežnik_VALUE,element_COUNT[0]))
            Varnost=EXACT_VALUE(odjemalec,1)
            if Varnost!=b'\x01': raise ValueError('unexpected security type')
            strežnik_VALUE.sendall(Varnost)
            if številka_različice==b'RFB 003.008\n':odjemalec.sendall(EXACT_VALUE(strežnik_VALUE,4))
            strežnik_VALUE.sendall(EXACT_VALUE(odjemalec,1))
            초기값=EXACT_VALUE(strežnik_VALUE,24)
            odjemalec.sendall(초기값+EXACT_VALUE(strežnik_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            odjemalec.settimeout(None);strežnik_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        območje_VALUE=EXACT_VALUE(strežnik_VALUE,1)[0]
                        if območje_VALUE==0:
                            머리=EXACT_VALUE(strežnik_VALUE,3);vnos_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 oddaljen_VALUE 포인터의 중복을 피한다.
                            Skrito_VALUE=포인터지원
                            if Skrito_VALUE:odjemalec.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            odjemalec.sendall(bytes([območje_VALUE])+머리)
                            for _ in range(vnos_COUNT):
                                pravokotnik=EXACT_VALUE(strežnik_VALUE,12);가로,Navpično_položaj,폭,višina_VALUE,kodiranje_VALUE=struct.unpack('>HHHHi',pravokotnik)
                                if kodiranje_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodiranje_VALUE))
                                odjemalec.sendall(pravokotnik)
                                남음=폭*višina_VALUE*화소바이트
                                while 남음:
                                    podatki=EXACT_VALUE(strežnik_VALUE,min(남음,65536));odjemalec.sendall(podatki);남음-=len(podatki)
                        elif območje_VALUE==1:
                            머리=EXACT_VALUE(strežnik_VALUE,5);element_COUNT=struct.unpack('>H',머리[3:])[0]
                            odjemalec.sendall(bytes([območje_VALUE])+머리+EXACT_VALUE(strežnik_VALUE,element_COUNT*6))
                        elif območje_VALUE==2:odjemalec.sendall(bytes([območje_VALUE]))
                        elif območje_VALUE==3:
                            머리=EXACT_VALUE(strežnik_VALUE,7);element_COUNT=struct.unpack('>I',머리[3:])[0]
                            if element_COUNT>1048576:raise ValueError('server clipboard too large')
                            odjemalec.sendall(bytes([območje_VALUE])+머리+EXACT_VALUE(strežnik_VALUE,element_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(območje_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:odjemalec.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                območje_VALUE=EXACT_VALUE(odjemalec,1)[0]
                if območje_VALUE==4:
                    telo_besedila=EXACT_VALUE(odjemalec,7); tipkovnica_vnos.누름값(telo_besedila[0]!=0,struct.unpack('>I',telo_besedila[3:])[0]); continue
                if območje_VALUE==255:
                    telo_besedila=EXACT_VALUE(odjemalec,11)
                    if telo_besedila[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tipkovnica_vnos.누름값(struct.unpack('>H',telo_besedila[1:3])[0]!=0,struct.unpack('>I',telo_besedila[3:7])[0]); continue
                if območje_VALUE==5:
                    telo_besedila=EXACT_VALUE(odjemalec,5); 단추들,koordinata_x,세로좌표=struct.unpack('>BHH',telo_besedila)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tipkovnica_vnos.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=koordinata_x<576 and 112<=세로좌표<372:
                        LOOKUP_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and LOOKUP_INDEX<5: 자신.poslati(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.poslati(bytes([30,1,단추들,koordinata_x&255,koordinata_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if območje_VALUE==6:
                    telo_besedila=EXACT_VALUE(odjemalec,7); 길이=struct.unpack('>i',telo_besedila[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    Besedilo=EXACT_VALUE(odjemalec,abs(길이))
                    if 길이>=0:
                        try: tipkovnica_vnos.odložišče_VALUE=Besedilo.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tipkovnica_vnos.odložišče_VALUE=Besedilo.decode('latin-1').encode('utf-8')
                        tipkovnica_vnos.odložišče_VALUE=tipkovnica_vnos.odložišče_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    strežnik_VALUE.sendall(bytes([območje_VALUE])+telo_besedila+Besedilo); continue
                if območje_VALUE==0:
                    telo_besedila=EXACT_VALUE(odjemalec,19)
                    if telo_besedila[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=telo_besedila[3]//8
                elif območje_VALUE==2:
                    telo_besedila=EXACT_VALUE(odjemalec,3); vnos_COUNT=struct.unpack('>H',telo_besedila[1:])[0]
                    if vnos_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(vnos_COUNT)+'i',EXACT_VALUE(odjemalec,vnos_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 privzeta_vrednost Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    telo_besedila=struct.pack('>BHi',0,1,0)
                elif območje_VALUE in (3,150): telo_besedila=EXACT_VALUE(odjemalec,9)
                elif območje_VALUE==248:
                    telo_besedila=EXACT_VALUE(odjemalec,8)
                    if telo_besedila[7]>64: raise ValueError('fence too large')
                    telo_besedila+=EXACT_VALUE(odjemalec,telo_besedila[7])
                elif območje_VALUE==250: telo_besedila=EXACT_VALUE(odjemalec,3)
                elif območje_VALUE==251:
                    telo_besedila=EXACT_VALUE(odjemalec,7)
                    if telo_besedila[5]>16: raise ValueError('too many screens')
                    telo_besedila+=EXACT_VALUE(odjemalec,telo_besedila[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(območje_VALUE))
                strežnik_VALUE.sendall(bytes([območje_VALUE])+telo_besedila)
        except (OSError,EOFError,ValueError) as NAPAKA:
            if str(NAPAKA): print('VNC client:',NAPAKA,file=sys.stderr,flush=True)
        finally:
            for vtičnica_VALUE in (odjemalec,strežnik_VALUE):
                try: vtičnica_VALUE.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                vtičnica_VALUE.close()


def izvajati_namizje(številka_vrat=5902, mreža=False, prenos_datotek_številka_vrat=2121, 전달규칙들=(), ločljivost_VALUE=(640, 480), gost_naslov=None, gostiti_naslov='127.0.0.1'):
    with ExitStack() as Viri, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        most_vnos = None
        if mreža:
            from most_3de4fe3a import most_3de4fe3a
            most_vnos = Viri.enter_context(most_3de4fe3a(prenos_datotek_številka_vrat, 전달규칙들, gost_naslov=gost_naslov, gostiti_naslov=gostiti_naslov))
        POT=Path(작업경로)/'display.sock'
        with socket.socket() as sprejeti_sprejemati_prejeti_prejemati_vrata:
            sprejeti_sprejemati_prejeti_prejemati_vrata.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            sprejeti_sprejemati_prejeti_prejemati_vrata.bind(('127.0.0.1',številka_vrat)); sprejeti_sprejemati_prejeti_prejemati_vrata.listen(1); sprejeti_sprejemati_prejeti_prejemati_vrata.settimeout(.2)
            원격화면접속번호=sprejeti_sprejemati_prejeti_prejemati_vrata.getsockname()[1]
            if most_vnos and (원격화면접속번호==prenos_datotek_številka_vrat or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and gostiti==원격화면접속번호 for 통신규약,gostiti,_ in most_vnos.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Opravilo=subprocess.Popen(Ukaz(ločljivost_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(POT)]+(most_vnos.전달인수() if most_vnos else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            most=POVEŽI_namizje(Opravilo); bralec=threading.Thread(target=most.직렬입출력,daemon=True); bralec.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(sprejeti_sprejemati_prejeti_prejemati_vrata.getsockname()[1]),flush=True)
            if most_vnos: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(gostiti_naslov,prenos_datotek_številka_vrat),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            obdelava_opravek=None; 가로채기됨=False
            try:
                while Opravilo.poll() is None:
                    try: odjemalec,_=sprejeti_sprejemati_prejeti_prejemati_vrata.accept()
                    except socket.timeout: continue
                    if obdelava_opravek is not None and obdelava_opravek.is_alive(): odjemalec.close(); continue
                    if not POT.exists(): odjemalec.close(); continue
                    obdelava_opravek=threading.Thread(target=most.odjemalec,args=(odjemalec,POT),daemon=True); obdelava_opravek.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                most.닫힘=True
                if most_vnos: most_vnos.Premor_dogodek.set()
                if Opravilo.poll() is None:
                    Opravilo.terminate()
                    try: Opravilo.wait(timeout=5)
                    except subprocess.TimeoutExpired: Opravilo.kill(); Opravilo.wait()
                bralec.join(timeout=2); Opravilo.stdin.close(); Opravilo.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if most_vnos and most_vnos.NAPAKA: raise RuntimeError('network bridge: '+most_vnos.NAPAKA)
            return 0 if 가로채기됨 else Opravilo.returncode


if __name__=='__main__':
    from Izvedi_ukaz import 해상도읽기
    razčlenjevalnik=argparse.ArgumentParser(description=__doc__); razčlenjevalnik.add_argument('--port',type=int,default=5902)
    razčlenjevalnik.add_argument('--resolution',type=해상도읽기,default=(640,480))
    razčlenjevalnik.add_argument('--network',action='store_true'); razčlenjevalnik.add_argument('--ftp-port',type=int,default=2121)
    razčlenjevalnik.add_argument('--forward',action='append',default=[])
    argument_ARRAY=razčlenjevalnik.parse_args()
    if argument_ARRAY.forward and not argument_ARRAY.network: razčlenjevalnik.error('--forward requires --network')
    raise SystemExit(izvajati_namizje(argument_ARRAY.port,mreža=argument_ARRAY.network,prenos_datotek_številka_vrat=argument_ARRAY.ftp_port,전달규칙들=argument_ARRAY.forward,ločljivost_VALUE=argument_ARRAY.resolution))
