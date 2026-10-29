#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Sleutel_VALUE 입력은 자체 kern_VALUE UART로 전달한다. localhost 전용, 단일 kontrole_VALUE 클라이언트.
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
from uitvoer_bevel import Opdrag
from local_input import create


def EXACT_VALUE(소켓, Grootte):
    data = bytearray()
    while len(data) < Grootte:
        조각 = 소켓.recv(Grootte - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class sleutelbord:
    def __init__(자신, e_pos, 입력방식알림=None):
        자신.바이트전송 = e_pos; 자신.modifiseersleutel = set(); 자신.knipbord_VALUE = b''
        자신.한글조합기 = create(e_pos, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Sleutel = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def e_pos(자신, data):
        자신.한글조합기.조합확정()
        자신.바이트전송(data)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Sleutel_simbool):
        if Sleutel_simbool in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.modifiseersleutel.add(Sleutel_simbool)
            else: 자신.modifiseersleutel.discard(Sleutel_simbool)
            return
        if not 누르는중:
            자신.SWITCH_Sleutel.discard(Sleutel_simbool)
            return
        CTRL = bool(자신.modifiseersleutel & {0xffe3, 0xffe4})
        SHIFT_sleutel = bool(자신.modifiseersleutel & {0xffe1, 0xffe2})
        if CTRL and SHIFT_sleutel and Sleutel_simbool in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Sleutel_simbool in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.e_pos(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Sleutel_simbool==0xff1b: 자신.유니코드입력=None
            elif Sleutel_simbool==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Sleutel_simbool<128 and chr(Sleutel_simbool) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Sleutel_simbool)
            return
        if Sleutel_simbool in (0xff31,0xffc6) or Sleutel_simbool==32 and SHIFT_sleutel and not CTRL:
            if Sleutel_simbool not in 자신.SWITCH_Sleutel: 자신.SWITCH_MODE()
            자신.SWITCH_Sleutel.add(Sleutel_simbool)
            return
        if Sleutel_simbool==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_sleutel and Sleutel_simbool in (ord('t'),ord('T')):
            자신.e_pos(bytes([30,2,1,0,0,0,0])); return
        if Sleutel_simbool==0xffc3: 자신.e_pos(bytes([30,2,2,0,0,0,0])); return
        if Sleutel_simbool==0xffc9: 자신.e_pos(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_sleutel and Sleutel_simbool in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.e_pos(자신.knipbord_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Sleutel_simbool in 특수글쇠: 자신.e_pos(특수글쇠[Sleutel_simbool]); return
        karakter_enkodering = Sleutel_simbool & 0xffffff if Sleutel_simbool & 0xff000000 == 0x01000000 else Sleutel_simbool
        if karakter_enkodering > 0x10ffff or 0xd800 <= karakter_enkodering <= 0xdfff or Sleutel_simbool >= 0xff00 and Sleutel_simbool < 0x1000000: return
        if CTRL and 0x40 <= karakter_enkodering <= 0x7f: 자신.e_pos(bytes([karakter_enkodering & 31])); return
        if karakter_enkodering < 32: return
        if 자신.한글여부 and 자신.modifiseersleutel & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.toevoer_Sleutel(chr(karakter_enkodering), altgr=True): return
        앞부분 = b'\x1b' if 자신.modifiseersleutel & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=karakter_enkodering<127:
            karakter_data=chr(karakter_enkodering).upper() if SHIFT_sleutel else chr(karakter_enkodering)
            if 자신.한글조합기.toevoer_Sleutel(karakter_data): return
        자신.e_pos(앞부분 + chr(karakter_enkodering).encode('utf-8'))


class KOPPEL_werkskerm:
    def __init__(자신, Proses):
        자신.Proses=Proses; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Terminaal=False; 자신.시작화면=False; 자신.닫힘=False

    def e_pos(자신, data):
        if not data or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Proses.stdin.write(data); 자신.Proses.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.Proses.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminaal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.e_pos(b'terminal\n')
        finally: 자신.닫힘=True

    def kliënt(자신, kliënt, Pad):
        bediener_VALUE=socket.socket(socket.AF_UNIX); bediener_VALUE.settimeout(10); kliënt.settimeout(10)
        sleutelbord_inskrywing=sleutelbord(자신.e_pos,lambda 한글여부:자신.e_pos(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            bediener_VALUE.connect(str(Pad))
            # 초기 협상은 순서대로 끝낸다. 이후 Afvoer 가닥만 클라이언트에 쓴다.
            kliënt.sendall(EXACT_VALUE(bediener_VALUE,12))
            판번호=EXACT_VALUE(kliënt,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            bediener_VALUE.sendall(판번호)
            item_COUNT=EXACT_VALUE(bediener_VALUE,1);kliënt.sendall(item_COUNT+EXACT_VALUE(bediener_VALUE,item_COUNT[0]))
            Sekuriteit=EXACT_VALUE(kliënt,1)
            if Sekuriteit!=b'\x01': raise ValueError('unexpected security type')
            bediener_VALUE.sendall(Sekuriteit)
            if 판번호==b'RFB 003.008\n':kliënt.sendall(EXACT_VALUE(bediener_VALUE,4))
            bediener_VALUE.sendall(EXACT_VALUE(kliënt,1))
            초기값=EXACT_VALUE(bediener_VALUE,24)
            kliënt.sendall(초기값+EXACT_VALUE(bediener_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            kliënt.settimeout(None);bediener_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        kategorie_VALUE=EXACT_VALUE(bediener_VALUE,1)[0]
                        if kategorie_VALUE==0:
                            머리=EXACT_VALUE(bediener_VALUE,3);inskrywing_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 afstands_VALUE 포인터의 중복을 피한다.
                            verskuilde_VALUE=포인터지원
                            if verskuilde_VALUE:kliënt.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            kliënt.sendall(bytes([kategorie_VALUE])+머리)
                            for _ in range(inskrywing_COUNT):
                                사각형=EXACT_VALUE(bediener_VALUE,12);가로,Vertikaal_plaas,폭,높이,enkodering_VALUE=struct.unpack('>HHHHi',사각형)
                                if enkodering_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(enkodering_VALUE))
                                kliënt.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=EXACT_VALUE(bediener_VALUE,min(남음,65536));kliënt.sendall(data);남음-=len(data)
                        elif kategorie_VALUE==1:
                            머리=EXACT_VALUE(bediener_VALUE,5);item_COUNT=struct.unpack('>H',머리[3:])[0]
                            kliënt.sendall(bytes([kategorie_VALUE])+머리+EXACT_VALUE(bediener_VALUE,item_COUNT*6))
                        elif kategorie_VALUE==2:kliënt.sendall(bytes([kategorie_VALUE]))
                        elif kategorie_VALUE==3:
                            머리=EXACT_VALUE(bediener_VALUE,7);item_COUNT=struct.unpack('>I',머리[3:])[0]
                            if item_COUNT>1048576:raise ValueError('server clipboard too large')
                            kliënt.sendall(bytes([kategorie_VALUE])+머리+EXACT_VALUE(bediener_VALUE,item_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(kategorie_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:kliënt.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                kategorie_VALUE=EXACT_VALUE(kliënt,1)[0]
                if kategorie_VALUE==4:
                    inhoudteks=EXACT_VALUE(kliënt,7); sleutelbord_inskrywing.누름값(inhoudteks[0]!=0,struct.unpack('>I',inhoudteks[3:])[0]); continue
                if kategorie_VALUE==255:
                    inhoudteks=EXACT_VALUE(kliënt,11)
                    if inhoudteks[0]!=0: raise ValueError('unsupported QEMU input extension')
                    sleutelbord_inskrywing.누름값(struct.unpack('>H',inhoudteks[1:3])[0]!=0,struct.unpack('>I',inhoudteks[3:7])[0]); continue
                if kategorie_VALUE==5:
                    inhoudteks=EXACT_VALUE(kliënt,5); 단추들,x_koördinaat,Y_koördinaat=struct.unpack('>BHH',inhoudteks)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: sleutelbord_inskrywing.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_koördinaat<576 and 112<=Y_koördinaat<372:
                        LOOKUP_INDEX=(Y_koördinaat-112)//52
                        if (Y_koördinaat-112)%52<40 and LOOKUP_INDEX<5: 자신.e_pos(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.e_pos(bytes([30,1,단추들,x_koördinaat&255,x_koördinaat>>8,Y_koördinaat&255,Y_koördinaat>>8]))
                    continue
                if kategorie_VALUE==6:
                    inhoudteks=EXACT_VALUE(kliënt,7); lengte_VALUE=struct.unpack('>i',inhoudteks[3:])[0]
                    if abs(lengte_VALUE)>65536: raise ValueError('clipboard too large')
                    Teks=EXACT_VALUE(kliënt,abs(lengte_VALUE))
                    if lengte_VALUE>=0:
                        try: sleutelbord_inskrywing.knipbord_VALUE=Teks.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: sleutelbord_inskrywing.knipbord_VALUE=Teks.decode('latin-1').encode('utf-8')
                        sleutelbord_inskrywing.knipbord_VALUE=sleutelbord_inskrywing.knipbord_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    bediener_VALUE.sendall(bytes([kategorie_VALUE])+inhoudteks+Teks); continue
                if kategorie_VALUE==0:
                    inhoudteks=EXACT_VALUE(kliënt,19)
                    if inhoudteks[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=inhoudteks[3]//8
                elif kategorie_VALUE==2:
                    inhoudteks=EXACT_VALUE(kliënt,3); inskrywing_COUNT=struct.unpack('>H',inhoudteks[1:])[0]
                    if inskrywing_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(inskrywing_COUNT)+'i',EXACT_VALUE(kliënt,inskrywing_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 verstekwaarde Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    inhoudteks=struct.pack('>BHi',0,1,0)
                elif kategorie_VALUE in (3,150): inhoudteks=EXACT_VALUE(kliënt,9)
                elif kategorie_VALUE==248:
                    inhoudteks=EXACT_VALUE(kliënt,8)
                    if inhoudteks[7]>64: raise ValueError('fence too large')
                    inhoudteks+=EXACT_VALUE(kliënt,inhoudteks[7])
                elif kategorie_VALUE==250: inhoudteks=EXACT_VALUE(kliënt,3)
                elif kategorie_VALUE==251:
                    inhoudteks=EXACT_VALUE(kliënt,7)
                    if inhoudteks[5]>16: raise ValueError('too many screens')
                    inhoudteks+=EXACT_VALUE(kliënt,inhoudteks[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(kategorie_VALUE))
                bediener_VALUE.sendall(bytes([kategorie_VALUE])+inhoudteks)
        except (OSError,EOFError,ValueError) as Fout:
            if str(Fout): print('VNC client:',Fout,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (kliënt,bediener_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ry_werkskerm(접속번호=5902, Netwerk=False, 파일전송접속번호=2121, 전달규칙들=(), resolusie_VALUE=(640, 480), gas_adres=None, hou_adres='127.0.0.1'):
    with ExitStack() as Hulpbronne, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Netwerk_brug_inskrywing = None
        if Netwerk:
            from Netwerk_brug import Netwerk_brug
            Netwerk_brug_inskrywing = Hulpbronne.enter_context(Netwerk_brug(파일전송접속번호, 전달규칙들, gas_adres=gas_adres, hou_adres=hou_adres))
        Pad=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Netwerk_brug_inskrywing and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and hou==원격화면접속번호 for 통신규약,hou,_ in Netwerk_brug_inskrywing.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proses=subprocess.Popen(Opdrag(resolusie_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Pad)]+(Netwerk_brug_inskrywing.전달인수() if Netwerk_brug_inskrywing else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            brug=KOPPEL_werkskerm(Proses); Leser=threading.Thread(target=brug.직렬입출력,daemon=True); Leser.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Netwerk_brug_inskrywing: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(hou_adres,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Proses.poll() is None:
                    try: kliënt,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): kliënt.close(); continue
                    if not Pad.exists(): kliënt.close(); continue
                    처리작업=threading.Thread(target=brug.kliënt,args=(kliënt,Pad),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                brug.닫힘=True
                if Netwerk_brug_inskrywing: Netwerk_brug_inskrywing.pouseer_gebeurtenis.set()
                if Proses.poll() is None:
                    Proses.terminate()
                    try: Proses.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
                Leser.join(timeout=2); Proses.stdin.close(); Proses.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Netwerk_brug_inskrywing and Netwerk_brug_inskrywing.Fout: raise RuntimeError('network bridge: '+Netwerk_brug_inskrywing.Fout)
            return 0 if 가로채기됨 else Proses.returncode


if __name__=='__main__':
    from uitvoer_bevel import 해상도읽기
    ontleder=argparse.ArgumentParser(description=__doc__); ontleder.add_argument('--port',type=int,default=5902)
    ontleder.add_argument('--resolution',type=해상도읽기,default=(640,480))
    ontleder.add_argument('--network',action='store_true'); ontleder.add_argument('--ftp-port',type=int,default=2121)
    ontleder.add_argument('--forward',action='append',default=[])
    argument_ARRAY=ontleder.parse_args()
    if argument_ARRAY.forward and not argument_ARRAY.network: ontleder.error('--forward requires --network')
    raise SystemExit(ry_werkskerm(argument_ARRAY.port,Netwerk=argument_ARRAY.network,파일전송접속번호=argument_ARRAY.ftp_port,전달규칙들=argument_ARRAY.forward,resolusie_VALUE=argument_ARRAY.resolution))
