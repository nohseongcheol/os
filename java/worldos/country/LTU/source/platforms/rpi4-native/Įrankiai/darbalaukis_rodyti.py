#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Raktas_VALUE 입력은 savas branduolys_VALUE UART로 전달한다. localhost 전용, 단일 valdymas_VALUE 클라이언트.
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
from Vykdyti_komanda import Komanda
from local_input import create


def EXACT_VALUE(소켓, Dydis):
    duomenys = bytearray()
    while len(duomenys) < Dydis:
        조각 = 소켓.recv(Dydis - len(duomenys))
        if not 조각: raise EOFError()
        duomenys.extend(조각)
    return bytes(duomenys)


class klaviatūra:
    def __init__(자신, siųsti, 입력방식알림=None):
        자신.바이트전송 = siųsti; 자신.modifikavimo_klavišas = set(); 자신.mainų_sritis_VALUE = b''
        자신.한글조합기 = create(siųsti, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Raktas = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def siųsti(자신, duomenys):
        자신.한글조합기.vykdymas_struktūra()
        자신.바이트전송(duomenys)

    def SWITCH_MODE(자신):
        자신.한글조합기.vykdymas_struktūra(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Raktas_simbolis):
        if Raktas_simbolis in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.modifikavimo_klavišas.add(Raktas_simbolis)
            else: 자신.modifikavimo_klavišas.discard(Raktas_simbolis)
            return
        if not 누르는중:
            자신.SWITCH_Raktas.discard(Raktas_simbolis)
            return
        valdymas_Raktas = bool(자신.modifikavimo_klavišas & {0xffe3, 0xffe4})
        윗글쇠 = bool(자신.modifikavimo_klavišas & {0xffe1, 0xffe2})
        if valdymas_Raktas and 윗글쇠 and Raktas_simbolis in (ord('u'),ord('U')):
            자신.한글조합기.vykdymas_struktūra(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Raktas_simbolis in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.siųsti(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Raktas_simbolis==0xff1b: 자신.유니코드입력=None
            elif Raktas_simbolis==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Raktas_simbolis<128 and chr(Raktas_simbolis) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Raktas_simbolis)
            return
        if Raktas_simbolis in (0xff31,0xffc6) or Raktas_simbolis==32 and 윗글쇠 and not valdymas_Raktas:
            if Raktas_simbolis not in 자신.SWITCH_Raktas: 자신.SWITCH_MODE()
            자신.SWITCH_Raktas.add(Raktas_simbolis)
            return
        if Raktas_simbolis==0xff08 and 자신.한글여부 and not valdymas_Raktas and 자신.한글조합기.앞글자지우기(): return
        if valdymas_Raktas and 윗글쇠 and Raktas_simbolis in (ord('t'),ord('T')):
            자신.siųsti(bytes([30,2,1,0,0,0,0])); return
        if Raktas_simbolis==0xffc3: 자신.siųsti(bytes([30,2,2,0,0,0,0])); return
        if Raktas_simbolis==0xffc9: 자신.siųsti(bytes([30,2,3,0,0,0,0])); return
        if valdymas_Raktas and 윗글쇠 and Raktas_simbolis in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.siųsti(자신.mainų_sritis_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Raktas_simbolis in 특수글쇠: 자신.siųsti(특수글쇠[Raktas_simbolis]); return
        simbolių_koduotė = Raktas_simbolis & 0xffffff if Raktas_simbolis & 0xff000000 == 0x01000000 else Raktas_simbolis
        if simbolių_koduotė > 0x10ffff or 0xd800 <= simbolių_koduotė <= 0xdfff or Raktas_simbolis >= 0xff00 and Raktas_simbolis < 0x1000000: return
        if valdymas_Raktas and 0x40 <= simbolių_koduotė <= 0x7f: 자신.siųsti(bytes([simbolių_koduotė & 31])); return
        if simbolių_koduotė < 32: return
        if 자신.한글여부 and 자신.modifikavimo_klavišas & {0xffea,0xfe03,0xff7e} and not valdymas_Raktas and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.sklaidos_kanalai_Raktas(chr(simbolių_koduotė), altgr=True): return
        앞부분 = b'\x1b' if 자신.modifikavimo_klavišas & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not valdymas_Raktas and not 앞부분 and 32<=simbolių_koduotė<127:
            simbolių_duomenys=chr(simbolių_koduotė).upper() if 윗글쇠 else chr(simbolių_koduotė)
            if 자신.한글조합기.sklaidos_kanalai_Raktas(simbolių_duomenys): return
        자신.siųsti(앞부분 + chr(simbolių_koduotė).encode('utf-8'))


class ryšys_darbalaukis:
    def __init__(자신, Procesas):
        자신.Procesas=Procesas; 자신.užraktas_VALUE=threading.Lock(); 자신.준비완료=False; 자신.Terminalas=False; 자신.시작화면=False; 자신.informacinės_technologijos_uždaryta=False

    def siųsti(자신, duomenys):
        if not duomenys or 자신.informacinės_technologijos_uždaryta: return
        with 자신.užraktas_VALUE:
            try: 자신.Procesas.stdin.write(duomenys); 자신.Procesas.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                duomenys=자신.Procesas.stdout.read(4096)
                if not duomenys: break
                sys.stdout.buffer.write(duomenys); sys.stdout.buffer.flush()
                끝부분=(끝부분+duomenys)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); informacinės_technologijos_uždaryta=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,informacinės_technologijos_uždaryta,그림화면,종료됨)>=0:
                    자신.Terminalas=열림>max(informacinės_technologijos_uždaryta,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,informacinės_technologijos_uždaryta,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.siųsti(b'terminal\n')
        finally: 자신.informacinės_technologijos_uždaryta=True

    def klientas(자신, klientas, KELIAS):
        serveris_VALUE=socket.socket(socket.AF_UNIX); serveris_VALUE.settimeout(10); klientas.settimeout(10)
        klaviatūra_įrašas=klaviatūra(자신.siųsti,lambda 한글여부:자신.siųsti(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            serveris_VALUE.connect(str(KELIAS))
            # pradinė_būsena 협상은 순서대로 끝낸다. 이후 Išvestis 가닥만 클라이언트에 쓴다.
            klientas.sendall(EXACT_VALUE(serveris_VALUE,12))
            versijos_numeris=EXACT_VALUE(klientas,12)
            if versijos_numeris not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            serveris_VALUE.sendall(versijos_numeris)
            prekė_COUNT=EXACT_VALUE(serveris_VALUE,1);klientas.sendall(prekė_COUNT+EXACT_VALUE(serveris_VALUE,prekė_COUNT[0]))
            Sauga=EXACT_VALUE(klientas,1)
            if Sauga!=b'\x01': raise ValueError('unexpected security type')
            serveris_VALUE.sendall(Sauga)
            if versijos_numeris==b'RFB 003.008\n':klientas.sendall(EXACT_VALUE(serveris_VALUE,4))
            serveris_VALUE.sendall(EXACT_VALUE(klientas,1))
            초기값=EXACT_VALUE(serveris_VALUE,24)
            klientas.sendall(초기값+EXACT_VALUE(serveris_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klientas.settimeout(None);serveris_VALUE.settimeout(None)
            def išeiga():
                try:
                    while True:
                        sritis_VALUE=EXACT_VALUE(serveris_VALUE,1)[0]
                        if sritis_VALUE==0:
                            머리=EXACT_VALUE(serveris_VALUE,3);įrašas_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 nuotolinis_VALUE 포인터의 중복을 피한다.
                            Paslėptas_VALUE=포인터지원
                            if Paslėptas_VALUE:klientas.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klientas.sendall(bytes([sritis_VALUE])+머리)
                            for _ in range(įrašas_COUNT):
                                stačiakampis=EXACT_VALUE(serveris_VALUE,12);가로,segmentas_padėtis,폭,높이,kodavimas_VALUE=struct.unpack('>HHHHi',stačiakampis)
                                if kodavimas_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodavimas_VALUE))
                                klientas.sendall(stačiakampis)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    duomenys=EXACT_VALUE(serveris_VALUE,min(남음,65536));klientas.sendall(duomenys);남음-=len(duomenys)
                        elif sritis_VALUE==1:
                            머리=EXACT_VALUE(serveris_VALUE,5);prekė_COUNT=struct.unpack('>H',머리[3:])[0]
                            klientas.sendall(bytes([sritis_VALUE])+머리+EXACT_VALUE(serveris_VALUE,prekė_COUNT*6))
                        elif sritis_VALUE==2:klientas.sendall(bytes([sritis_VALUE]))
                        elif sritis_VALUE==3:
                            머리=EXACT_VALUE(serveris_VALUE,7);prekė_COUNT=struct.unpack('>I',머리[3:])[0]
                            if prekė_COUNT>1048576:raise ValueError('server clipboard too large')
                            klientas.sendall(bytes([sritis_VALUE])+머리+EXACT_VALUE(serveris_VALUE,prekė_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(sritis_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klientas.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            darbininkas=threading.Thread(target=išeiga,daemon=True);darbininkas.start()
            while not 자신.informacinės_technologijos_uždaryta:
                sritis_VALUE=EXACT_VALUE(klientas,1)[0]
                if sritis_VALUE==4:
                    pagrindinis_tekstas=EXACT_VALUE(klientas,7); klaviatūra_įrašas.누름값(pagrindinis_tekstas[0]!=0,struct.unpack('>I',pagrindinis_tekstas[3:])[0]); continue
                if sritis_VALUE==255:
                    pagrindinis_tekstas=EXACT_VALUE(klientas,11)
                    if pagrindinis_tekstas[0]!=0: raise ValueError('unsupported QEMU input extension')
                    klaviatūra_įrašas.누름값(struct.unpack('>H',pagrindinis_tekstas[1:3])[0]!=0,struct.unpack('>I',pagrindinis_tekstas[3:7])[0]); continue
                if sritis_VALUE==5:
                    pagrindinis_tekstas=EXACT_VALUE(klientas,5); 단추들,x_koordinatė,세로좌표=struct.unpack('>BHH',pagrindinis_tekstas)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: klaviatūra_įrašas.한글조합기.vykdymas_struktūra()
                    if 눌림&1 and 자신.시작화면 and 64<=x_koordinatė<576 and 112<=세로좌표<372:
                        LOOKUP_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and LOOKUP_INDEX<5: 자신.siųsti(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.siųsti(bytes([30,1,단추들,x_koordinatė&255,x_koordinatė>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if sritis_VALUE==6:
                    pagrindinis_tekstas=EXACT_VALUE(klientas,7); 길이=struct.unpack('>i',pagrindinis_tekstas[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    Tekstas=EXACT_VALUE(klientas,abs(길이))
                    if 길이>=0:
                        try: klaviatūra_įrašas.mainų_sritis_VALUE=Tekstas.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: klaviatūra_įrašas.mainų_sritis_VALUE=Tekstas.decode('latin-1').encode('utf-8')
                        klaviatūra_įrašas.mainų_sritis_VALUE=klaviatūra_įrašas.mainų_sritis_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    serveris_VALUE.sendall(bytes([sritis_VALUE])+pagrindinis_tekstas+Tekstas); continue
                if sritis_VALUE==0:
                    pagrindinis_tekstas=EXACT_VALUE(klientas,19)
                    if pagrindinis_tekstas[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=pagrindinis_tekstas[3]//8
                elif sritis_VALUE==2:
                    pagrindinis_tekstas=EXACT_VALUE(klientas,3); įrašas_COUNT=struct.unpack('>H',pagrindinis_tekstas[1:])[0]
                    if įrašas_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(įrašas_COUNT)+'i',EXACT_VALUE(klientas,įrašas_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 numatytoji_reikšmė Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    pagrindinis_tekstas=struct.pack('>BHi',0,1,0)
                elif sritis_VALUE in (3,150): pagrindinis_tekstas=EXACT_VALUE(klientas,9)
                elif sritis_VALUE==248:
                    pagrindinis_tekstas=EXACT_VALUE(klientas,8)
                    if pagrindinis_tekstas[7]>64: raise ValueError('fence too large')
                    pagrindinis_tekstas+=EXACT_VALUE(klientas,pagrindinis_tekstas[7])
                elif sritis_VALUE==250: pagrindinis_tekstas=EXACT_VALUE(klientas,3)
                elif sritis_VALUE==251:
                    pagrindinis_tekstas=EXACT_VALUE(klientas,7)
                    if pagrindinis_tekstas[5]>16: raise ValueError('too many screens')
                    pagrindinis_tekstas+=EXACT_VALUE(klientas,pagrindinis_tekstas[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(sritis_VALUE))
                serveris_VALUE.sendall(bytes([sritis_VALUE])+pagrindinis_tekstas)
        except (OSError,EOFError,ValueError) as KLAIDA:
            if str(KLAIDA): print('VNC client:',KLAIDA,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (klientas,serveris_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def vykdyti_darbalaukis(prievado_numeris=5902, tinklas=False, failo_perdavimas_prievado_numeris=2121, 전달규칙들=(), skiriamoji_geba_VALUE=(640, 480), svečias_ADDRESS=None, organizuoti_ADDRESS='127.0.0.1'):
    with ExitStack() as Ištekliai, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        tiltas_įrašas = None
        if tinklas:
            from tiltas_3de4fe3a import tiltas_3de4fe3a
            tiltas_įrašas = Ištekliai.enter_context(tiltas_3de4fe3a(failo_perdavimas_prievado_numeris, 전달규칙들, svečias_ADDRESS=svečias_ADDRESS, organizuoti_ADDRESS=organizuoti_ADDRESS))
        KELIAS=Path(작업경로)/'display.sock'
        with socket.socket() as gauti_jungtis:
            gauti_jungtis.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            gauti_jungtis.bind(('127.0.0.1',prievado_numeris)); gauti_jungtis.listen(1); gauti_jungtis.settimeout(.2)
            원격화면접속번호=gauti_jungtis.getsockname()[1]
            if tiltas_įrašas and (원격화면접속번호==failo_perdavimas_prievado_numeris or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and organizuoti==원격화면접속번호 for 통신규약,organizuoti,_ in tiltas_įrašas.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Procesas=subprocess.Popen(Komanda(skiriamoji_geba_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(KELIAS)]+(tiltas_įrašas.전달인수() if tiltas_įrašas else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            tiltas=ryšys_darbalaukis(Procesas); Skaitytuvė=threading.Thread(target=tiltas.직렬입출력,daemon=True); Skaitytuvė.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(gauti_jungtis.getsockname()[1]),flush=True)
            if tiltas_įrašas: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(organizuoti_ADDRESS,failo_perdavimas_prievado_numeris),flush=True)
            def 종료시키기(signalas_numeris,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            apdorojimas_užduotis=None; 가로채기됨=False
            try:
                while Procesas.poll() is None:
                    try: klientas,_=gauti_jungtis.accept()
                    except socket.timeout: continue
                    if apdorojimas_užduotis is not None and apdorojimas_užduotis.is_alive(): klientas.close(); continue
                    if not KELIAS.exists(): klientas.close(); continue
                    apdorojimas_užduotis=threading.Thread(target=tiltas.klientas,args=(klientas,KELIAS),daemon=True); apdorojimas_užduotis.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                tiltas.informacinės_technologijos_uždaryta=True
                if tiltas_įrašas: tiltas_įrašas.Pauzė_įvykis.set()
                if Procesas.poll() is None:
                    Procesas.terminate()
                    try: Procesas.wait(timeout=5)
                    except subprocess.TimeoutExpired: Procesas.kill(); Procesas.wait()
                Skaitytuvė.join(timeout=2); Procesas.stdin.close(); Procesas.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if tiltas_įrašas and tiltas_įrašas.KLAIDA: raise RuntimeError('network bridge: '+tiltas_įrašas.KLAIDA)
            return 0 if 가로채기됨 else Procesas.returncode


if __name__=='__main__':
    from Vykdyti_komanda import 해상도읽기
    analizatorius=argparse.ArgumentParser(description=__doc__); analizatorius.add_argument('--port',type=int,default=5902)
    analizatorius.add_argument('--resolution',type=해상도읽기,default=(640,480))
    analizatorius.add_argument('--network',action='store_true'); analizatorius.add_argument('--ftp-port',type=int,default=2121)
    analizatorius.add_argument('--forward',action='append',default=[])
    argumentas_ARRAY=analizatorius.parse_args()
    if argumentas_ARRAY.forward and not argumentas_ARRAY.network: analizatorius.error('--forward requires --network')
    raise SystemExit(vykdyti_darbalaukis(argumentas_ARRAY.port,tinklas=argumentas_ARRAY.network,failo_perdavimas_prievado_numeris=argumentas_ARRAY.ftp_port,전달규칙들=argumentas_ARRAY.forward,skiriamoji_geba_VALUE=argumentas_ARRAY.resolution))
