#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, eochair_VALUE 입력은 자체 eithne_VALUE UART로 전달한다. localhost 전용, 단일 rialú_VALUE 클라이언트.
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
from Rith_ordú import Ordú
from local_input import create


def EXACT_VALUE(소켓, Méid):
    sonraí = bytearray()
    while len(sonraí) < Méid:
        조각 = 소켓.recv(Méid - len(sonraí))
        if not 조각: raise EOFError()
        sonraí.extend(조각)
    return bytes(sonraí)


class méarchlár:
    def __init__(자신, seol, 입력방식알림=None):
        자신.바이트전송 = seol; 자신.eochair_mhionathraithe = set(); 자신.gearrthaisce_VALUE = b''
        자신.한글조합기 = create(seol, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_eochair = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def seol(자신, sonraí):
        자신.한글조합기.조합확정()
        자신.바이트전송(sonraí)

    def SWITCH_mód(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, eochair_siombail):
        if eochair_siombail in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.eochair_mhionathraithe.add(eochair_siombail)
            else: 자신.eochair_mhionathraithe.discard(eochair_siombail)
            return
        if not 누르는중:
            자신.SWITCH_eochair.discard(eochair_siombail)
            return
        CTRL = bool(자신.eochair_mhionathraithe & {0xffe3, 0xffe4})
        eochair_SHIFT = bool(자신.eochair_mhionathraithe & {0xffe1, 0xffe2})
        if CTRL and eochair_SHIFT and eochair_siombail in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if eochair_siombail in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.seol(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif eochair_siombail==0xff1b: 자신.유니코드입력=None
            elif eochair_siombail==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif eochair_siombail<128 and chr(eochair_siombail) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(eochair_siombail)
            return
        if eochair_siombail in (0xff31,0xffc6) or eochair_siombail==32 and eochair_SHIFT and not CTRL:
            if eochair_siombail not in 자신.SWITCH_eochair: 자신.SWITCH_mód()
            자신.SWITCH_eochair.add(eochair_siombail)
            return
        if eochair_siombail==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and eochair_SHIFT and eochair_siombail in (ord('t'),ord('T')):
            자신.seol(bytes([30,2,1,0,0,0,0])); return
        if eochair_siombail==0xffc3: 자신.seol(bytes([30,2,2,0,0,0,0])); return
        if eochair_siombail==0xffc9: 자신.seol(bytes([30,2,3,0,0,0,0])); return
        if CTRL and eochair_SHIFT and eochair_siombail in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.seol(자신.gearrthaisce_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if eochair_siombail in 특수글쇠: 자신.seol(특수글쇠[eochair_siombail]); return
        carachtar_ionchódú = eochair_siombail & 0xffffff if eochair_siombail & 0xff000000 == 0x01000000 else eochair_siombail
        if carachtar_ionchódú > 0x10ffff or 0xd800 <= carachtar_ionchódú <= 0xdfff or eochair_siombail >= 0xff00 and eochair_siombail < 0x1000000: return
        if CTRL and 0x40 <= carachtar_ionchódú <= 0x7f: 자신.seol(bytes([carachtar_ionchódú & 31])); return
        if carachtar_ionchódú < 32: return
        if 자신.한글여부 and 자신.eochair_mhionathraithe & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.fotha_eochair(chr(carachtar_ionchódú), altgr=True): return
        앞부분 = b'\x1b' if 자신.eochair_mhionathraithe & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=carachtar_ionchódú<127:
            carachtar_sonraí=chr(carachtar_ionchódú).upper() if eochair_SHIFT else chr(carachtar_ionchódú)
            if 자신.한글조합기.fotha_eochair(carachtar_sonraí): return
        자신.seol(앞부분 + chr(carachtar_ionchódú).encode('utf-8'))


class nasc_deasc:
    def __init__(자신, Próiseas):
        자신.Próiseas=Próiseas; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Teirminéal=False; 자신.시작화면=False; 자신.닫힘=False

    def seol(자신, sonraí):
        if not sonraí or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Próiseas.stdin.write(sonraí); 자신.Próiseas.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                sonraí=자신.Próiseas.stdout.read(4096)
                if not sonraí: break
                sys.stdout.buffer.write(sonraí); sys.stdout.buffer.flush()
                끝부분=(끝부분+sonraí)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Teirminéal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.seol(b'terminal\n')
        finally: 자신.닫힘=True

    def cliant(자신, cliant, CONAIR):
        freastalaí_VALUE=socket.socket(socket.AF_UNIX); freastalaí_VALUE.settimeout(10); cliant.settimeout(10)
        méarchlár_iontráil=méarchlár(자신.seol,lambda 한글여부:자신.seol(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            freastalaí_VALUE.connect(str(CONAIR))
            # 초기 협상은 순서대로 끝낸다. 이후 Aschur 가닥만 클라이언트에 쓴다.
            cliant.sendall(EXACT_VALUE(freastalaí_VALUE,12))
            uimhir_an_leagain=EXACT_VALUE(cliant,12)
            if uimhir_an_leagain not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            freastalaí_VALUE.sendall(uimhir_an_leagain)
            mír_COUNT=EXACT_VALUE(freastalaí_VALUE,1);cliant.sendall(mír_COUNT+EXACT_VALUE(freastalaí_VALUE,mír_COUNT[0]))
            Slándáil=EXACT_VALUE(cliant,1)
            if Slándáil!=b'\x01': raise ValueError('unexpected security type')
            freastalaí_VALUE.sendall(Slándáil)
            if uimhir_an_leagain==b'RFB 003.008\n':cliant.sendall(EXACT_VALUE(freastalaí_VALUE,4))
            freastalaí_VALUE.sendall(EXACT_VALUE(cliant,1))
            초기값=EXACT_VALUE(freastalaí_VALUE,24)
            cliant.sendall(초기값+EXACT_VALUE(freastalaí_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            cliant.settimeout(None);freastalaí_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        catagóir_VALUE=EXACT_VALUE(freastalaí_VALUE,1)[0]
                        if catagóir_VALUE==0:
                            머리=EXACT_VALUE(freastalaí_VALUE,3);iontráil_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 cianda_VALUE 포인터의 중복을 피한다.
                            folaithe_VALUE=포인터지원
                            if folaithe_VALUE:cliant.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            cliant.sendall(bytes([catagóir_VALUE])+머리)
                            for _ in range(iontráil_COUNT):
                                사각형=EXACT_VALUE(freastalaí_VALUE,12);가로,Ingearach_suíomh,폭,높이,ionchódú_VALUE=struct.unpack('>HHHHi',사각형)
                                if ionchódú_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(ionchódú_VALUE))
                                cliant.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    sonraí=EXACT_VALUE(freastalaí_VALUE,min(남음,65536));cliant.sendall(sonraí);남음-=len(sonraí)
                        elif catagóir_VALUE==1:
                            머리=EXACT_VALUE(freastalaí_VALUE,5);mír_COUNT=struct.unpack('>H',머리[3:])[0]
                            cliant.sendall(bytes([catagóir_VALUE])+머리+EXACT_VALUE(freastalaí_VALUE,mír_COUNT*6))
                        elif catagóir_VALUE==2:cliant.sendall(bytes([catagóir_VALUE]))
                        elif catagóir_VALUE==3:
                            머리=EXACT_VALUE(freastalaí_VALUE,7);mír_COUNT=struct.unpack('>I',머리[3:])[0]
                            if mír_COUNT>1048576:raise ValueError('server clipboard too large')
                            cliant.sendall(bytes([catagóir_VALUE])+머리+EXACT_VALUE(freastalaí_VALUE,mír_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(catagóir_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:cliant.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                catagóir_VALUE=EXACT_VALUE(cliant,1)[0]
                if catagóir_VALUE==4:
                    corpthéacs=EXACT_VALUE(cliant,7); méarchlár_iontráil.누름값(corpthéacs[0]!=0,struct.unpack('>I',corpthéacs[3:])[0]); continue
                if catagóir_VALUE==255:
                    corpthéacs=EXACT_VALUE(cliant,11)
                    if corpthéacs[0]!=0: raise ValueError('unsupported QEMU input extension')
                    méarchlár_iontráil.누름값(struct.unpack('>H',corpthéacs[1:3])[0]!=0,struct.unpack('>I',corpthéacs[3:7])[0]); continue
                if catagóir_VALUE==5:
                    corpthéacs=EXACT_VALUE(cliant,5); 단추들,x_chomhordanáid,세로좌표=struct.unpack('>BHH',corpthéacs)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: méarchlár_iontráil.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_chomhordanáid<576 and 112<=세로좌표<372:
                        LOOKUP_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and LOOKUP_INDEX<5: 자신.seol(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.seol(bytes([30,1,단추들,x_chomhordanáid&255,x_chomhordanáid>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if catagóir_VALUE==6:
                    corpthéacs=EXACT_VALUE(cliant,7); fad_VALUE=struct.unpack('>i',corpthéacs[3:])[0]
                    if abs(fad_VALUE)>65536: raise ValueError('clipboard too large')
                    Téacs=EXACT_VALUE(cliant,abs(fad_VALUE))
                    if fad_VALUE>=0:
                        try: méarchlár_iontráil.gearrthaisce_VALUE=Téacs.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: méarchlár_iontráil.gearrthaisce_VALUE=Téacs.decode('latin-1').encode('utf-8')
                        méarchlár_iontráil.gearrthaisce_VALUE=méarchlár_iontráil.gearrthaisce_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    freastalaí_VALUE.sendall(bytes([catagóir_VALUE])+corpthéacs+Téacs); continue
                if catagóir_VALUE==0:
                    corpthéacs=EXACT_VALUE(cliant,19)
                    if corpthéacs[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=corpthéacs[3]//8
                elif catagóir_VALUE==2:
                    corpthéacs=EXACT_VALUE(cliant,3); iontráil_COUNT=struct.unpack('>H',corpthéacs[1:])[0]
                    if iontráil_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(iontráil_COUNT)+'i',EXACT_VALUE(cliant,iontráil_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 luach_réamhshocraithe Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    corpthéacs=struct.pack('>BHi',0,1,0)
                elif catagóir_VALUE in (3,150): corpthéacs=EXACT_VALUE(cliant,9)
                elif catagóir_VALUE==248:
                    corpthéacs=EXACT_VALUE(cliant,8)
                    if corpthéacs[7]>64: raise ValueError('fence too large')
                    corpthéacs+=EXACT_VALUE(cliant,corpthéacs[7])
                elif catagóir_VALUE==250: corpthéacs=EXACT_VALUE(cliant,3)
                elif catagóir_VALUE==251:
                    corpthéacs=EXACT_VALUE(cliant,7)
                    if corpthéacs[5]>16: raise ValueError('too many screens')
                    corpthéacs+=EXACT_VALUE(cliant,corpthéacs[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(catagóir_VALUE))
                freastalaí_VALUE.sendall(bytes([catagóir_VALUE])+corpthéacs)
        except (OSError,EOFError,ValueError) as ERREÁID:
            if str(ERREÁID): print('VNC client:',ERREÁID,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (cliant,freastalaí_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def rith_deasc(uimhir_phoirt=5902, Líonra=False, comhad_traschur_uimhir_phoirt=2121, 전달규칙들=(), taifeach_VALUE=(640, 480), aoi_ADDRESS=None, óstach_ADDRESS='127.0.0.1'):
    with ExitStack() as Acmhainní, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Líonra_traschóiritheoir_iontráil = None
        if Líonra:
            from Líonra_traschóiritheoir import Líonra_traschóiritheoir
            Líonra_traschóiritheoir_iontráil = Acmhainní.enter_context(Líonra_traschóiritheoir(comhad_traschur_uimhir_phoirt, 전달규칙들, aoi_ADDRESS=aoi_ADDRESS, óstach_ADDRESS=óstach_ADDRESS))
        CONAIR=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',uimhir_phoirt)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Líonra_traschóiritheoir_iontráil and (원격화면접속번호==comhad_traschur_uimhir_phoirt or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and óstach==원격화면접속번호 for 통신규약,óstach,_ in Líonra_traschóiritheoir_iontráil.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Próiseas=subprocess.Popen(Ordú(taifeach_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(CONAIR)]+(Líonra_traschóiritheoir_iontráil.전달인수() if Líonra_traschóiritheoir_iontráil else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            traschóiritheoir=nasc_deasc(Próiseas); Léitheoir=threading.Thread(target=traschóiritheoir.직렬입출력,daemon=True); Léitheoir.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Líonra_traschóiritheoir_iontráil: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(óstach_ADDRESS,comhad_traschur_uimhir_phoirt),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Próiseas.poll() is None:
                    try: cliant,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): cliant.close(); continue
                    if not CONAIR.exists(): cliant.close(); continue
                    처리작업=threading.Thread(target=traschóiritheoir.cliant,args=(cliant,CONAIR),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                traschóiritheoir.닫힘=True
                if Líonra_traschóiritheoir_iontráil: Líonra_traschóiritheoir_iontráil.cuir_ar_shos_ócáid.set()
                if Próiseas.poll() is None:
                    Próiseas.terminate()
                    try: Próiseas.wait(timeout=5)
                    except subprocess.TimeoutExpired: Próiseas.kill(); Próiseas.wait()
                Léitheoir.join(timeout=2); Próiseas.stdin.close(); Próiseas.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Líonra_traschóiritheoir_iontráil and Líonra_traschóiritheoir_iontráil.ERREÁID: raise RuntimeError('network bridge: '+Líonra_traschóiritheoir_iontráil.ERREÁID)
            return 0 if 가로채기됨 else Próiseas.returncode


if __name__=='__main__':
    from Rith_ordú import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    argóint_ARRAY=인수해석기.parse_args()
    if argóint_ARRAY.forward and not argóint_ARRAY.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(rith_deasc(argóint_ARRAY.port,Líonra=argóint_ARRAY.network,comhad_traschur_uimhir_phoirt=argóint_ARRAY.ftp_port,전달규칙들=argóint_ARRAY.forward,taifeach_VALUE=argóint_ARRAY.resolution))
