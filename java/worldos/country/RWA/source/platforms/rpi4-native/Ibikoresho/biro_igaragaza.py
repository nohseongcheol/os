#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, buto_agaciro 입력은 자체 intima_agaciro UART로 전달한다. localhost 전용, 단일 icunga_agaciro 클라이언트.
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
from gukora_ibwiriza import Icyo_wifuza
from local_input import create


def 정확한값(소켓, Ingano):
    amakurushingiro = bytearray()
    while len(amakurushingiro) < Ingano:
        조각 = 소켓.recv(Ingano - len(amakurushingiro))
        if not 조각: raise EOFError()
        amakurushingiro.extend(조각)
    return bytes(amakurushingiro)


class mwandikisho:
    def __init__(자신, kohereza, 입력방식알림=None):
        자신.바이트전송 = kohereza; 자신.buto_mpinduzi = set(); 자신.ububikogateganyo_agaciro = b''
        자신.한글조합기 = create(kohereza, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.guhinduranya_buto = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def kohereza(자신, amakurushingiro):
        자신.한글조합기.조합확정()
        자신.바이트전송(amakurushingiro)

    def guhinduranya_uburyo(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, buto_ikimenyetso):
        if buto_ikimenyetso in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.buto_mpinduzi.add(buto_ikimenyetso)
            else: 자신.buto_mpinduzi.discard(buto_ikimenyetso)
            return
        if not 누르는중:
            자신.guhinduranya_buto.discard(buto_ikimenyetso)
            return
        CTRL = bool(자신.buto_mpinduzi & {0xffe3, 0xffe4})
        buto_SHIFT = bool(자신.buto_mpinduzi & {0xffe1, 0xffe2})
        if CTRL and buto_SHIFT and buto_ikimenyetso in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if buto_ikimenyetso in (32,0xff0d):
                try:
                    agaciro=int(자신.유니코드입력,16)
                    if 32<=agaciro<=0x10ffff and not 0xd800<=agaciro<=0xdfff: 자신.kohereza(chr(agaciro).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif buto_ikimenyetso==0xff1b: 자신.유니코드입력=None
            elif buto_ikimenyetso==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif buto_ikimenyetso<128 and chr(buto_ikimenyetso) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(buto_ikimenyetso)
            return
        if buto_ikimenyetso in (0xff31,0xffc6) or buto_ikimenyetso==32 and buto_SHIFT and not CTRL:
            if buto_ikimenyetso not in 자신.guhinduranya_buto: 자신.guhinduranya_uburyo()
            자신.guhinduranya_buto.add(buto_ikimenyetso)
            return
        if buto_ikimenyetso==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and buto_SHIFT and buto_ikimenyetso in (ord('t'),ord('T')):
            자신.kohereza(bytes([30,2,1,0,0,0,0])); return
        if buto_ikimenyetso==0xffc3: 자신.kohereza(bytes([30,2,2,0,0,0,0])); return
        if buto_ikimenyetso==0xffc9: 자신.kohereza(bytes([30,2,3,0,0,0,0])); return
        if CTRL and buto_SHIFT and buto_ikimenyetso in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.kohereza(자신.ububikogateganyo_agaciro); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if buto_ikimenyetso in 특수글쇠: 자신.kohereza(특수글쇠[buto_ikimenyetso]); return
        inyuguti_gusobeka = buto_ikimenyetso & 0xffffff if buto_ikimenyetso & 0xff000000 == 0x01000000 else buto_ikimenyetso
        if inyuguti_gusobeka > 0x10ffff or 0xd800 <= inyuguti_gusobeka <= 0xdfff or buto_ikimenyetso >= 0xff00 and buto_ikimenyetso < 0x1000000: return
        if CTRL and 0x40 <= inyuguti_gusobeka <= 0x7f: 자신.kohereza(bytes([inyuguti_gusobeka & 31])); return
        if inyuguti_gusobeka < 32: return
        if 자신.한글여부 and 자신.buto_mpinduzi & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.urujyano_buto(chr(inyuguti_gusobeka), altgr=True): return
        앞부분 = b'\x1b' if 자신.buto_mpinduzi & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=inyuguti_gusobeka<127:
            inyuguti_amakurushingiro=chr(inyuguti_gusobeka).upper() if buto_SHIFT else chr(inyuguti_gusobeka)
            if 자신.한글조합기.urujyano_buto(inyuguti_amakurushingiro): return
        자신.kohereza(앞부분 + chr(inyuguti_gusobeka).encode('utf-8'))


class Guhuza_biro:
    def __init__(자신, Inzira_a7054519):
        자신.Inzira_a7054519=Inzira_a7054519; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def kohereza(자신, amakurushingiro):
        if not amakurushingiro or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Inzira_a7054519.stdin.write(amakurushingiro); 자신.Inzira_a7054519.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                amakurushingiro=자신.Inzira_a7054519.stdout.read(4096)
                if not amakurushingiro: break
                sys.stdout.buffer.write(amakurushingiro); sys.stdout.buffer.flush()
                끝부분=(끝부분+amakurushingiro)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.kohereza(b'terminal\n')
        finally: 자신.닫힘=True

    def umukiriya(자신, umukiriya, Inzira):
        seriveri_agaciro=socket.socket(socket.AF_UNIX); seriveri_agaciro.settimeout(10); umukiriya.settimeout(10)
        mwandikisho_icyinjizwa=mwandikisho(자신.kohereza,lambda 한글여부:자신.kohereza(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            seriveri_agaciro.connect(str(Inzira))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            umukiriya.sendall(정확한값(seriveri_agaciro,12))
            판번호=정확한값(umukiriya,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            seriveri_agaciro.sendall(판번호)
            개수=정확한값(seriveri_agaciro,1);umukiriya.sendall(개수+정확한값(seriveri_agaciro,개수[0]))
            Umutekano=정확한값(umukiriya,1)
            if Umutekano!=b'\x01': raise ValueError('unexpected security type')
            seriveri_agaciro.sendall(Umutekano)
            if 판번호==b'RFB 003.008\n':umukiriya.sendall(정확한값(seriveri_agaciro,4))
            seriveri_agaciro.sendall(정확한값(umukiriya,1))
            초기값=정확한값(seriveri_agaciro,24)
            umukiriya.sendall(초기값+정확한값(seriveri_agaciro,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            umukiriya.settimeout(None);seriveri_agaciro.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        icyiciro_agaciro=정확한값(seriveri_agaciro,1)[0]
                        if icyiciro_agaciro==0:
                            머리=정확한값(seriveri_agaciro,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 kure_agaciro 포인터의 중복을 피한다.
                            cyahishwe_agaciro=포인터지원
                            if cyahishwe_agaciro:umukiriya.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            umukiriya.sendall(bytes([icyiciro_agaciro])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(seriveri_agaciro,12);가로,세로,폭,높이,gusobeka_agaciro=struct.unpack('>HHHHi',사각형)
                                if gusobeka_agaciro!=0:raise ValueError('unexpected framebuffer encoding: '+str(gusobeka_agaciro))
                                umukiriya.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    amakurushingiro=정확한값(seriveri_agaciro,min(남음,65536));umukiriya.sendall(amakurushingiro);남음-=len(amakurushingiro)
                        elif icyiciro_agaciro==1:
                            머리=정확한값(seriveri_agaciro,5);개수=struct.unpack('>H',머리[3:])[0]
                            umukiriya.sendall(bytes([icyiciro_agaciro])+머리+정확한값(seriveri_agaciro,개수*6))
                        elif icyiciro_agaciro==2:umukiriya.sendall(bytes([icyiciro_agaciro]))
                        elif icyiciro_agaciro==3:
                            머리=정확한값(seriveri_agaciro,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            umukiriya.sendall(bytes([icyiciro_agaciro])+머리+정확한값(seriveri_agaciro,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(icyiciro_agaciro))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:umukiriya.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                icyiciro_agaciro=정확한값(umukiriya,1)[0]
                if icyiciro_agaciro==4:
                    igihimba_cy_umwandiko=정확한값(umukiriya,7); mwandikisho_icyinjizwa.누름값(igihimba_cy_umwandiko[0]!=0,struct.unpack('>I',igihimba_cy_umwandiko[3:])[0]); continue
                if icyiciro_agaciro==255:
                    igihimba_cy_umwandiko=정확한값(umukiriya,11)
                    if igihimba_cy_umwandiko[0]!=0: raise ValueError('unsupported QEMU input extension')
                    mwandikisho_icyinjizwa.누름값(struct.unpack('>H',igihimba_cy_umwandiko[1:3])[0]!=0,struct.unpack('>I',igihimba_cy_umwandiko[3:7])[0]); continue
                if icyiciro_agaciro==5:
                    igihimba_cy_umwandiko=정확한값(umukiriya,5); 단추들,Ihuza_rya_x,세로좌표=struct.unpack('>BHH',igihimba_cy_umwandiko)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: mwandikisho_icyinjizwa.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=Ihuza_rya_x<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.kohereza(bytes([ord('1')+색인]))
                    else: 자신.kohereza(bytes([30,1,단추들,Ihuza_rya_x&255,Ihuza_rya_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if icyiciro_agaciro==6:
                    igihimba_cy_umwandiko=정확한값(umukiriya,7); uburebure_agaciro=struct.unpack('>i',igihimba_cy_umwandiko[3:])[0]
                    if abs(uburebure_agaciro)>65536: raise ValueError('clipboard too large')
                    Umwandiko=정확한값(umukiriya,abs(uburebure_agaciro))
                    if uburebure_agaciro>=0:
                        try: mwandikisho_icyinjizwa.ububikogateganyo_agaciro=Umwandiko.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: mwandikisho_icyinjizwa.ububikogateganyo_agaciro=Umwandiko.decode('latin-1').encode('utf-8')
                        mwandikisho_icyinjizwa.ububikogateganyo_agaciro=mwandikisho_icyinjizwa.ububikogateganyo_agaciro[:65536].decode('utf-8','ignore').encode('utf-8')
                    seriveri_agaciro.sendall(bytes([icyiciro_agaciro])+igihimba_cy_umwandiko+Umwandiko); continue
                if icyiciro_agaciro==0:
                    igihimba_cy_umwandiko=정확한값(umukiriya,19)
                    if igihimba_cy_umwandiko[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=igihimba_cy_umwandiko[3]//8
                elif icyiciro_agaciro==2:
                    igihimba_cy_umwandiko=정확한값(umukiriya,3); 항목수=struct.unpack('>H',igihimba_cy_umwandiko[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(umukiriya,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 agaciro_gasanzweho Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    igihimba_cy_umwandiko=struct.pack('>BHi',0,1,0)
                elif icyiciro_agaciro in (3,150): igihimba_cy_umwandiko=정확한값(umukiriya,9)
                elif icyiciro_agaciro==248:
                    igihimba_cy_umwandiko=정확한값(umukiriya,8)
                    if igihimba_cy_umwandiko[7]>64: raise ValueError('fence too large')
                    igihimba_cy_umwandiko+=정확한값(umukiriya,igihimba_cy_umwandiko[7])
                elif icyiciro_agaciro==250: igihimba_cy_umwandiko=정확한값(umukiriya,3)
                elif icyiciro_agaciro==251:
                    igihimba_cy_umwandiko=정확한값(umukiriya,7)
                    if igihimba_cy_umwandiko[5]>16: raise ValueError('too many screens')
                    igihimba_cy_umwandiko+=정확한값(umukiriya,igihimba_cy_umwandiko[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(icyiciro_agaciro))
                seriveri_agaciro.sendall(bytes([icyiciro_agaciro])+igihimba_cy_umwandiko)
        except (OSError,EOFError,ValueError) as IKOSA:
            if str(IKOSA): print('VNC client:',IKOSA,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (umukiriya,seriveri_agaciro):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ihuriro_biro(접속번호=5902, Urusobemiyoboro=False, 파일전송접속번호=2121, 전달규칙들=(), ibonerana_agaciro=(640, 480), 게스트주소=None, gucumbikira_aderesi='127.0.0.1'):
    with ExitStack() as Ibikoresho_50487cae, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if Urusobemiyoboro:
            from 통신다리 import 통신다리
            통신다리항목 = Ibikoresho_50487cae.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, gucumbikira_aderesi=gucumbikira_aderesi))
        Inzira=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and gucumbikira==원격화면접속번호 for 통신규약,gucumbikira,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Inzira_a7054519=subprocess.Popen(Icyo_wifuza(ibonerana_agaciro)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Inzira)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=Guhuza_biro(Inzira_a7054519); Musomyi=threading.Thread(target=연결다리.직렬입출력,daemon=True); Musomyi.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(gucumbikira_aderesi,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Inzira_a7054519.poll() is None:
                    try: umukiriya,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): umukiriya.close(); continue
                    if not Inzira.exists(): umukiriya.close(); continue
                    처리작업=threading.Thread(target=연결다리.umukiriya,args=(umukiriya,Inzira),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.gusubika_icyabaye.set()
                if Inzira_a7054519.poll() is None:
                    Inzira_a7054519.terminate()
                    try: Inzira_a7054519.wait(timeout=5)
                    except subprocess.TimeoutExpired: Inzira_a7054519.kill(); Inzira_a7054519.wait()
                Musomyi.join(timeout=2); Inzira_a7054519.stdin.close(); Inzira_a7054519.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.IKOSA: raise RuntimeError('network bridge: '+통신다리항목.IKOSA)
            return 0 if 가로채기됨 else Inzira_a7054519.returncode


if __name__=='__main__':
    from gukora_ibwiriza import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    ingingo_ARRAY=인수해석기.parse_args()
    if ingingo_ARRAY.forward and not ingingo_ARRAY.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(ihuriro_biro(ingingo_ARRAY.port,Urusobemiyoboro=ingingo_ARRAY.network,파일전송접속번호=ingingo_ARRAY.ftp_port,전달규칙들=ingingo_ARRAY.forward,ibonerana_agaciro=ingingo_ARRAY.resolution))
