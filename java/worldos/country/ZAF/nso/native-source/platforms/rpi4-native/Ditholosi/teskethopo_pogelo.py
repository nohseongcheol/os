#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, khii_boleng 입력은 자체 khenele_boleng UART로 전달한다. localhost 전용, 단일 taolo_boleng 클라이언트.
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
from phethagatša_taelo import Taelo
from local_input import create


def 정확한값(소켓, Bogolo):
    data = bytearray()
    while len(data) < Bogolo:
        조각 = 소켓.recv(Bogolo - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class khiipote:
    def __init__(자신, Romela, 입력방식알림=None):
        자신.바이트전송 = Romela; 자신.khii_ya_go_fetoša = set(); 자신.klipbote_boleng = b''
        자신.한글조합기 = create(Romela, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.fetogela_khii = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def Romela(자신, data):
        자신.한글조합기.조합확정()
        자신.바이트전송(data)

    def fetogela_mokgwa(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, khii_leswao):
        if khii_leswao in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.khii_ya_go_fetoša.add(khii_leswao)
            else: 자신.khii_ya_go_fetoša.discard(khii_leswao)
            return
        if not 누르는중:
            자신.fetogela_khii.discard(khii_leswao)
            return
        CTRL = bool(자신.khii_ya_go_fetoša & {0xffe3, 0xffe4})
        khii_ya_SHIFT = bool(자신.khii_ya_go_fetoša & {0xffe1, 0xffe2})
        if CTRL and khii_ya_SHIFT and khii_leswao in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if khii_leswao in (32,0xff0d):
                try:
                    boleng=int(자신.유니코드입력,16)
                    if 32<=boleng<=0x10ffff and not 0xd800<=boleng<=0xdfff: 자신.Romela(chr(boleng).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif khii_leswao==0xff1b: 자신.유니코드입력=None
            elif khii_leswao==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif khii_leswao<128 and chr(khii_leswao) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(khii_leswao)
            return
        if khii_leswao in (0xff31,0xffc6) or khii_leswao==32 and khii_ya_SHIFT and not CTRL:
            if khii_leswao not in 자신.fetogela_khii: 자신.fetogela_mokgwa()
            자신.fetogela_khii.add(khii_leswao)
            return
        if khii_leswao==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and khii_ya_SHIFT and khii_leswao in (ord('t'),ord('T')):
            자신.Romela(bytes([30,2,1,0,0,0,0])); return
        if khii_leswao==0xffc3: 자신.Romela(bytes([30,2,2,0,0,0,0])); return
        if khii_leswao==0xffc9: 자신.Romela(bytes([30,2,3,0,0,0,0])); return
        if CTRL and khii_ya_SHIFT and khii_leswao in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.Romela(자신.klipbote_boleng); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if khii_leswao in 특수글쇠: 자신.Romela(특수글쇠[khii_leswao]); return
        tlhaka_go_enkhouta = khii_leswao & 0xffffff if khii_leswao & 0xff000000 == 0x01000000 else khii_leswao
        if tlhaka_go_enkhouta > 0x10ffff or 0xd800 <= tlhaka_go_enkhouta <= 0xdfff or khii_leswao >= 0xff00 and khii_leswao < 0x1000000: return
        if CTRL and 0x40 <= tlhaka_go_enkhouta <= 0x7f: 자신.Romela(bytes([tlhaka_go_enkhouta & 31])); return
        if tlhaka_go_enkhouta < 32: return
        if 자신.한글여부 and 자신.khii_ya_go_fetoša & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.fiti_ya_RSS_khii(chr(tlhaka_go_enkhouta), altgr=True): return
        앞부분 = b'\x1b' if 자신.khii_ya_go_fetoša & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=tlhaka_go_enkhouta<127:
            tlhaka_data=chr(tlhaka_go_enkhouta).upper() if khii_ya_SHIFT else chr(tlhaka_go_enkhouta)
            if 자신.한글조합기.fiti_ya_RSS_khii(tlhaka_data): return
        자신.Romela(앞부분 + chr(tlhaka_go_enkhouta).encode('utf-8'))


class KGOKAGANYA_teskethopo:
    def __init__(자신, tiragalo_a7054519):
        자신.tiragalo_a7054519=tiragalo_a7054519; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def Romela(자신, data):
        if not data or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.tiragalo_a7054519.stdin.write(data); 자신.tiragalo_a7054519.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.tiragalo_a7054519.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.Romela(b'terminal\n')
        finally: 자신.닫힘=True

    def klaente(자신, klaente, Tsejana):
        seba_boleng=socket.socket(socket.AF_UNIX); seba_boleng.settimeout(10); klaente.settimeout(10)
        khiipote_go_tsenya_tshedimošo=khiipote(자신.Romela,lambda 한글여부:자신.Romela(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            seba_boleng.connect(str(Tsejana))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            klaente.sendall(정확한값(seba_boleng,12))
            판번호=정확한값(klaente,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            seba_boleng.sendall(판번호)
            개수=정확한값(seba_boleng,1);klaente.sendall(개수+정확한값(seba_boleng,개수[0]))
            Tšhireletšo=정확한값(klaente,1)
            if Tšhireletšo!=b'\x01': raise ValueError('unexpected security type')
            seba_boleng.sendall(Tšhireletšo)
            if 판번호==b'RFB 003.008\n':klaente.sendall(정확한값(seba_boleng,4))
            seba_boleng.sendall(정확한값(klaente,1))
            초기값=정확한값(seba_boleng,24)
            klaente.sendall(초기값+정확한값(seba_boleng,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klaente.settimeout(None);seba_boleng.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        legoro_boleng=정확한값(seba_boleng,1)[0]
                        if legoro_boleng==0:
                            머리=정확한값(seba_boleng,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 ya_kgole_boleng 포인터의 중복을 피한다.
                            fihlilwego_boleng=포인터지원
                            if fihlilwego_boleng:klaente.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klaente.sendall(bytes([legoro_boleng])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(seba_boleng,12);가로,세로,폭,높이,go_enkhouta_boleng=struct.unpack('>HHHHi',사각형)
                                if go_enkhouta_boleng!=0:raise ValueError('unexpected framebuffer encoding: '+str(go_enkhouta_boleng))
                                klaente.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=정확한값(seba_boleng,min(남음,65536));klaente.sendall(data);남음-=len(data)
                        elif legoro_boleng==1:
                            머리=정확한값(seba_boleng,5);개수=struct.unpack('>H',머리[3:])[0]
                            klaente.sendall(bytes([legoro_boleng])+머리+정확한값(seba_boleng,개수*6))
                        elif legoro_boleng==2:klaente.sendall(bytes([legoro_boleng]))
                        elif legoro_boleng==3:
                            머리=정확한값(seba_boleng,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            klaente.sendall(bytes([legoro_boleng])+머리+정확한값(seba_boleng,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(legoro_boleng))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klaente.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                legoro_boleng=정확한값(klaente,1)[0]
                if legoro_boleng==4:
                    mmele_wa_sengwalwa=정확한값(klaente,7); khiipote_go_tsenya_tshedimošo.누름값(mmele_wa_sengwalwa[0]!=0,struct.unpack('>I',mmele_wa_sengwalwa[3:])[0]); continue
                if legoro_boleng==255:
                    mmele_wa_sengwalwa=정확한값(klaente,11)
                    if mmele_wa_sengwalwa[0]!=0: raise ValueError('unsupported QEMU input extension')
                    khiipote_go_tsenya_tshedimošo.누름값(struct.unpack('>H',mmele_wa_sengwalwa[1:3])[0]!=0,struct.unpack('>I',mmele_wa_sengwalwa[3:7])[0]); continue
                if legoro_boleng==5:
                    mmele_wa_sengwalwa=정확한값(klaente,5); 단추들,kamano_ya_x,세로좌표=struct.unpack('>BHH',mmele_wa_sengwalwa)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: khiipote_go_tsenya_tshedimošo.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=kamano_ya_x<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.Romela(bytes([ord('1')+색인]))
                    else: 자신.Romela(bytes([30,1,단추들,kamano_ya_x&255,kamano_ya_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if legoro_boleng==6:
                    mmele_wa_sengwalwa=정확한값(klaente,7); botelele_boleng=struct.unpack('>i',mmele_wa_sengwalwa[3:])[0]
                    if abs(botelele_boleng)>65536: raise ValueError('clipboard too large')
                    Sengwalwa=정확한값(klaente,abs(botelele_boleng))
                    if botelele_boleng>=0:
                        try: khiipote_go_tsenya_tshedimošo.klipbote_boleng=Sengwalwa.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: khiipote_go_tsenya_tshedimošo.klipbote_boleng=Sengwalwa.decode('latin-1').encode('utf-8')
                        khiipote_go_tsenya_tshedimošo.klipbote_boleng=khiipote_go_tsenya_tshedimošo.klipbote_boleng[:65536].decode('utf-8','ignore').encode('utf-8')
                    seba_boleng.sendall(bytes([legoro_boleng])+mmele_wa_sengwalwa+Sengwalwa); continue
                if legoro_boleng==0:
                    mmele_wa_sengwalwa=정확한값(klaente,19)
                    if mmele_wa_sengwalwa[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=mmele_wa_sengwalwa[3]//8
                elif legoro_boleng==2:
                    mmele_wa_sengwalwa=정확한값(klaente,3); 항목수=struct.unpack('>H',mmele_wa_sengwalwa[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(klaente,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 setsenywa_sa_tirelwa Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    mmele_wa_sengwalwa=struct.pack('>BHi',0,1,0)
                elif legoro_boleng in (3,150): mmele_wa_sengwalwa=정확한값(klaente,9)
                elif legoro_boleng==248:
                    mmele_wa_sengwalwa=정확한값(klaente,8)
                    if mmele_wa_sengwalwa[7]>64: raise ValueError('fence too large')
                    mmele_wa_sengwalwa+=정확한값(klaente,mmele_wa_sengwalwa[7])
                elif legoro_boleng==250: mmele_wa_sengwalwa=정확한값(klaente,3)
                elif legoro_boleng==251:
                    mmele_wa_sengwalwa=정확한값(klaente,7)
                    if mmele_wa_sengwalwa[5]>16: raise ValueError('too many screens')
                    mmele_wa_sengwalwa+=정확한값(klaente,mmele_wa_sengwalwa[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(legoro_boleng))
                seba_boleng.sendall(bytes([legoro_boleng])+mmele_wa_sengwalwa)
        except (OSError,EOFError,ValueError) as Phošo:
            if str(Phošo): print('VNC client:',Phošo,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (klaente,seba_boleng):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def sepetša_teskethopo(접속번호=5902, Netweke=False, 파일전송접속번호=2121, 전달규칙들=(), sephetho_boleng=(640, 480), moeng_atrese=None, go_nea_ditirelo_atrese='127.0.0.1'):
    with ExitStack() as Methopo, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Netweke_kgokaganyo_go_tsenya_tshedimošo = None
        if Netweke:
            from Netweke_kgokaganyo import Netweke_kgokaganyo
            Netweke_kgokaganyo_go_tsenya_tshedimošo = Methopo.enter_context(Netweke_kgokaganyo(파일전송접속번호, 전달규칙들, moeng_atrese=moeng_atrese, go_nea_ditirelo_atrese=go_nea_ditirelo_atrese))
        Tsejana=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Netweke_kgokaganyo_go_tsenya_tshedimošo and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and go_nea_ditirelo==원격화면접속번호 for 통신규약,go_nea_ditirelo,_ in Netweke_kgokaganyo_go_tsenya_tshedimošo.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            tiragalo_a7054519=subprocess.Popen(Taelo(sephetho_boleng)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Tsejana)]+(Netweke_kgokaganyo_go_tsenya_tshedimošo.전달인수() if Netweke_kgokaganyo_go_tsenya_tshedimošo else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            kgokaganyo=KGOKAGANYA_teskethopo(tiragalo_a7054519); mmadi=threading.Thread(target=kgokaganyo.직렬입출력,daemon=True); mmadi.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Netweke_kgokaganyo_go_tsenya_tshedimošo: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(go_nea_ditirelo_atrese,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while tiragalo_a7054519.poll() is None:
                    try: klaente,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): klaente.close(); continue
                    if not Tsejana.exists(): klaente.close(); continue
                    처리작업=threading.Thread(target=kgokaganyo.klaente,args=(klaente,Tsejana),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                kgokaganyo.닫힘=True
                if Netweke_kgokaganyo_go_tsenya_tshedimošo: Netweke_kgokaganyo_go_tsenya_tshedimošo.emiša_nakwana_tiragalo.set()
                if tiragalo_a7054519.poll() is None:
                    tiragalo_a7054519.terminate()
                    try: tiragalo_a7054519.wait(timeout=5)
                    except subprocess.TimeoutExpired: tiragalo_a7054519.kill(); tiragalo_a7054519.wait()
                mmadi.join(timeout=2); tiragalo_a7054519.stdin.close(); tiragalo_a7054519.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Netweke_kgokaganyo_go_tsenya_tshedimošo and Netweke_kgokaganyo_go_tsenya_tshedimošo.Phošo: raise RuntimeError('network bridge: '+Netweke_kgokaganyo_go_tsenya_tshedimošo.Phošo)
            return 0 if 가로채기됨 else tiragalo_a7054519.returncode


if __name__=='__main__':
    from phethagatša_taelo import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    akumente_arei=인수해석기.parse_args()
    if akumente_arei.forward and not akumente_arei.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(sepetša_teskethopo(akumente_arei.port,Netweke=akumente_arei.network,파일전송접속번호=akumente_arei.ftp_port,전달규칙들=akumente_arei.forward,sephetho_boleng=akumente_arei.resolution))
