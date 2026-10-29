#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, taetsi_Boleng 입력은 자체 Khenele_Boleng UART로 전달한다. localhost 전용, 단일 taolo_Boleng 클라이언트.
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
from diragatsa_Taelo import Taelo
from local_input import create


def 정확한값(소켓, lekanya):
    tshedimosetso = bytearray()
    while len(tshedimosetso) < lekanya:
        조각 = 소켓.recv(lekanya - len(tshedimosetso))
        if not 조각: raise EOFError()
        tshedimosetso.extend(조각)
    return bytes(tshedimosetso)


class Khiiboto:
    def __init__(자신, romela, 입력방식알림=None):
        자신.바이트전송 = romela; 자신.taetsi_e_e_fetolang = set(); 자신.peelodimamaretswa_Boleng = b''
        자신.한글조합기 = create(romela, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.fetola_taetsi = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def romela(자신, tshedimosetso):
        자신.한글조합기.조합확정()
        자신.바이트전송(tshedimosetso)

    def fetola_mokgwa(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, taetsi_letshwao):
        if taetsi_letshwao in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.taetsi_e_e_fetolang.add(taetsi_letshwao)
            else: 자신.taetsi_e_e_fetolang.discard(taetsi_letshwao)
            return
        if not 누르는중:
            자신.fetola_taetsi.discard(taetsi_letshwao)
            return
        CTRL = bool(자신.taetsi_e_e_fetolang & {0xffe3, 0xffe4})
        taetsi_ya_SHIFT = bool(자신.taetsi_e_e_fetolang & {0xffe1, 0xffe2})
        if CTRL and taetsi_ya_SHIFT and taetsi_letshwao in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if taetsi_letshwao in (32,0xff0d):
                try:
                    Boleng=int(자신.유니코드입력,16)
                    if 32<=Boleng<=0x10ffff and not 0xd800<=Boleng<=0xdfff: 자신.romela(chr(Boleng).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif taetsi_letshwao==0xff1b: 자신.유니코드입력=None
            elif taetsi_letshwao==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif taetsi_letshwao<128 and chr(taetsi_letshwao) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(taetsi_letshwao)
            return
        if taetsi_letshwao in (0xff31,0xffc6) or taetsi_letshwao==32 and taetsi_ya_SHIFT and not CTRL:
            if taetsi_letshwao not in 자신.fetola_taetsi: 자신.fetola_mokgwa()
            자신.fetola_taetsi.add(taetsi_letshwao)
            return
        if taetsi_letshwao==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and taetsi_ya_SHIFT and taetsi_letshwao in (ord('t'),ord('T')):
            자신.romela(bytes([30,2,1,0,0,0,0])); return
        if taetsi_letshwao==0xffc3: 자신.romela(bytes([30,2,2,0,0,0,0])); return
        if taetsi_letshwao==0xffc9: 자신.romela(bytes([30,2,3,0,0,0,0])); return
        if CTRL and taetsi_ya_SHIFT and taetsi_letshwao in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.romela(자신.peelodimamaretswa_Boleng); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if taetsi_letshwao in 특수글쇠: 자신.romela(특수글쇠[taetsi_letshwao]); return
        Letshwao_khoutufatso = taetsi_letshwao & 0xffffff if taetsi_letshwao & 0xff000000 == 0x01000000 else taetsi_letshwao
        if Letshwao_khoutufatso > 0x10ffff or 0xd800 <= Letshwao_khoutufatso <= 0xdfff or taetsi_letshwao >= 0xff00 and taetsi_letshwao < 0x1000000: return
        if CTRL and 0x40 <= Letshwao_khoutufatso <= 0x7f: 자신.romela(bytes([Letshwao_khoutufatso & 31])); return
        if Letshwao_khoutufatso < 32: return
        if 자신.한글여부 and 자신.taetsi_e_e_fetolang & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.sefepi_taetsi(chr(Letshwao_khoutufatso), altgr=True): return
        앞부분 = b'\x1b' if 자신.taetsi_e_e_fetolang & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=Letshwao_khoutufatso<127:
            Letshwao_tshedimosetso=chr(Letshwao_khoutufatso).upper() if taetsi_ya_SHIFT else chr(Letshwao_khoutufatso)
            if 자신.한글조합기.sefepi_taetsi(Letshwao_tshedimosetso): return
        자신.romela(앞부분 + chr(Letshwao_khoutufatso).encode('utf-8'))


class Golaganya_desekethopo:
    def __init__(자신, Thulaganyo):
        자신.Thulaganyo=Thulaganyo; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def romela(자신, tshedimosetso):
        if not tshedimosetso or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Thulaganyo.stdin.write(tshedimosetso); 자신.Thulaganyo.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                tshedimosetso=자신.Thulaganyo.stdout.read(4096)
                if not tshedimosetso: break
                sys.stdout.buffer.write(tshedimosetso); sys.stdout.buffer.flush()
                끝부분=(끝부분+tshedimosetso)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.romela(b'terminal\n')
        finally: 자신.닫힘=True

    def sedirelwa(자신, sedirelwa, tsela):
        sefara_Boleng=socket.socket(socket.AF_UNIX); sefara_Boleng.settimeout(10); sedirelwa.settimeout(10)
        Khiiboto_tsenyo=Khiiboto(자신.romela,lambda 한글여부:자신.romela(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            sefara_Boleng.connect(str(tsela))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            sedirelwa.sendall(정확한값(sefara_Boleng,12))
            판번호=정확한값(sedirelwa,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            sefara_Boleng.sendall(판번호)
            개수=정확한값(sefara_Boleng,1);sedirelwa.sendall(개수+정확한값(sefara_Boleng,개수[0]))
            tshireletso=정확한값(sedirelwa,1)
            if tshireletso!=b'\x01': raise ValueError('unexpected security type')
            sefara_Boleng.sendall(tshireletso)
            if 판번호==b'RFB 003.008\n':sedirelwa.sendall(정확한값(sefara_Boleng,4))
            sefara_Boleng.sendall(정확한값(sedirelwa,1))
            초기값=정확한값(sefara_Boleng,24)
            sedirelwa.sendall(초기값+정확한값(sefara_Boleng,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            sedirelwa.settimeout(None);sefara_Boleng.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        setlhopha_Boleng_4b6d6445=정확한값(sefara_Boleng,1)[0]
                        if setlhopha_Boleng_4b6d6445==0:
                            머리=정확한값(sefara_Boleng,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 kgakala_Boleng 포인터의 중복을 피한다.
                            fitlhegileng_Boleng=포인터지원
                            if fitlhegileng_Boleng:sedirelwa.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            sedirelwa.sendall(bytes([setlhopha_Boleng_4b6d6445])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(sefara_Boleng,12);가로,세로,폭,높이,khoutufatso_Boleng=struct.unpack('>HHHHi',사각형)
                                if khoutufatso_Boleng!=0:raise ValueError('unexpected framebuffer encoding: '+str(khoutufatso_Boleng))
                                sedirelwa.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    tshedimosetso=정확한값(sefara_Boleng,min(남음,65536));sedirelwa.sendall(tshedimosetso);남음-=len(tshedimosetso)
                        elif setlhopha_Boleng_4b6d6445==1:
                            머리=정확한값(sefara_Boleng,5);개수=struct.unpack('>H',머리[3:])[0]
                            sedirelwa.sendall(bytes([setlhopha_Boleng_4b6d6445])+머리+정확한값(sefara_Boleng,개수*6))
                        elif setlhopha_Boleng_4b6d6445==2:sedirelwa.sendall(bytes([setlhopha_Boleng_4b6d6445]))
                        elif setlhopha_Boleng_4b6d6445==3:
                            머리=정확한값(sefara_Boleng,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            sedirelwa.sendall(bytes([setlhopha_Boleng_4b6d6445])+머리+정확한값(sefara_Boleng,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(setlhopha_Boleng_4b6d6445))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:sedirelwa.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                setlhopha_Boleng_4b6d6445=정확한값(sedirelwa,1)[0]
                if setlhopha_Boleng_4b6d6445==4:
                    diteng_tsa_mokwalo=정확한값(sedirelwa,7); Khiiboto_tsenyo.누름값(diteng_tsa_mokwalo[0]!=0,struct.unpack('>I',diteng_tsa_mokwalo[3:])[0]); continue
                if setlhopha_Boleng_4b6d6445==255:
                    diteng_tsa_mokwalo=정확한값(sedirelwa,11)
                    if diteng_tsa_mokwalo[0]!=0: raise ValueError('unsupported QEMU input extension')
                    Khiiboto_tsenyo.누름값(struct.unpack('>H',diteng_tsa_mokwalo[1:3])[0]!=0,struct.unpack('>I',diteng_tsa_mokwalo[3:7])[0]); continue
                if setlhopha_Boleng_4b6d6445==5:
                    diteng_tsa_mokwalo=정확한값(sedirelwa,5); 단추들,kgokagano_ya_x,세로좌표=struct.unpack('>BHH',diteng_tsa_mokwalo)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: Khiiboto_tsenyo.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=kgokagano_ya_x<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.romela(bytes([ord('1')+색인]))
                    else: 자신.romela(bytes([30,1,단추들,kgokagano_ya_x&255,kgokagano_ya_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if setlhopha_Boleng_4b6d6445==6:
                    diteng_tsa_mokwalo=정확한값(sedirelwa,7); boleele_Boleng=struct.unpack('>i',diteng_tsa_mokwalo[3:])[0]
                    if abs(boleele_Boleng)>65536: raise ValueError('clipboard too large')
                    SMS=정확한값(sedirelwa,abs(boleele_Boleng))
                    if boleele_Boleng>=0:
                        try: Khiiboto_tsenyo.peelodimamaretswa_Boleng=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: Khiiboto_tsenyo.peelodimamaretswa_Boleng=SMS.decode('latin-1').encode('utf-8')
                        Khiiboto_tsenyo.peelodimamaretswa_Boleng=Khiiboto_tsenyo.peelodimamaretswa_Boleng[:65536].decode('utf-8','ignore').encode('utf-8')
                    sefara_Boleng.sendall(bytes([setlhopha_Boleng_4b6d6445])+diteng_tsa_mokwalo+SMS); continue
                if setlhopha_Boleng_4b6d6445==0:
                    diteng_tsa_mokwalo=정확한값(sedirelwa,19)
                    if diteng_tsa_mokwalo[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=diteng_tsa_mokwalo[3]//8
                elif setlhopha_Boleng_4b6d6445==2:
                    diteng_tsa_mokwalo=정확한값(sedirelwa,3); 항목수=struct.unpack('>H',diteng_tsa_mokwalo[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(sedirelwa,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 boleng_jo_bo_rulaganyeditsweng_ruri Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    diteng_tsa_mokwalo=struct.pack('>BHi',0,1,0)
                elif setlhopha_Boleng_4b6d6445 in (3,150): diteng_tsa_mokwalo=정확한값(sedirelwa,9)
                elif setlhopha_Boleng_4b6d6445==248:
                    diteng_tsa_mokwalo=정확한값(sedirelwa,8)
                    if diteng_tsa_mokwalo[7]>64: raise ValueError('fence too large')
                    diteng_tsa_mokwalo+=정확한값(sedirelwa,diteng_tsa_mokwalo[7])
                elif setlhopha_Boleng_4b6d6445==250: diteng_tsa_mokwalo=정확한값(sedirelwa,3)
                elif setlhopha_Boleng_4b6d6445==251:
                    diteng_tsa_mokwalo=정확한값(sedirelwa,7)
                    if diteng_tsa_mokwalo[5]>16: raise ValueError('too many screens')
                    diteng_tsa_mokwalo+=정확한값(sedirelwa,diteng_tsa_mokwalo[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(setlhopha_Boleng_4b6d6445))
                sefara_Boleng.sendall(bytes([setlhopha_Boleng_4b6d6445])+diteng_tsa_mokwalo)
        except (OSError,EOFError,ValueError) as phoso:
            if str(phoso): print('VNC client:',phoso,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (sedirelwa,sefara_Boleng):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def dirisa_desekethopo(접속번호=5902, Neteweke=False, 파일전송접속번호=2121, 전달규칙들=(), resolušene_Boleng=(640, 480), moeng_aterese=None, pinagare_aterese='127.0.0.1'):
    with ExitStack() as Ditsompelo, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Neteweke_leborogo_tsenyo = None
        if Neteweke:
            from Neteweke_leborogo import Neteweke_leborogo
            Neteweke_leborogo_tsenyo = Ditsompelo.enter_context(Neteweke_leborogo(파일전송접속번호, 전달규칙들, moeng_aterese=moeng_aterese, pinagare_aterese=pinagare_aterese))
        tsela=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Neteweke_leborogo_tsenyo and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and pinagare==원격화면접속번호 for 통신규약,pinagare,_ in Neteweke_leborogo_tsenyo.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Thulaganyo=subprocess.Popen(Taelo(resolušene_Boleng)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(tsela)]+(Neteweke_leborogo_tsenyo.전달인수() if Neteweke_leborogo_tsenyo else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            leborogo=Golaganya_desekethopo(Thulaganyo); mmuisi=threading.Thread(target=leborogo.직렬입출력,daemon=True); mmuisi.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Neteweke_leborogo_tsenyo: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(pinagare_aterese,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Thulaganyo.poll() is None:
                    try: sedirelwa,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): sedirelwa.close(); continue
                    if not tsela.exists(): sedirelwa.close(); continue
                    처리작업=threading.Thread(target=leborogo.sedirelwa,args=(sedirelwa,tsela),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                leborogo.닫힘=True
                if Neteweke_leborogo_tsenyo: Neteweke_leborogo_tsenyo.Kgaotsa_tiragalo.set()
                if Thulaganyo.poll() is None:
                    Thulaganyo.terminate()
                    try: Thulaganyo.wait(timeout=5)
                    except subprocess.TimeoutExpired: Thulaganyo.kill(); Thulaganyo.wait()
                mmuisi.join(timeout=2); Thulaganyo.stdin.close(); Thulaganyo.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Neteweke_leborogo_tsenyo and Neteweke_leborogo_tsenyo.phoso: raise RuntimeError('network bridge: '+Neteweke_leborogo_tsenyo.phoso)
            return 0 if 가로채기됨 else Thulaganyo.returncode


if __name__=='__main__':
    from diragatsa_Taelo import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    Thulaganyo_setlhopha=인수해석기.parse_args()
    if Thulaganyo_setlhopha.forward and not Thulaganyo_setlhopha.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(dirisa_desekethopo(Thulaganyo_setlhopha.port,Neteweke=Thulaganyo_setlhopha.network,파일전송접속번호=Thulaganyo_setlhopha.ftp_port,전달규칙들=Thulaganyo_setlhopha.forward,resolušene_Boleng=Thulaganyo_setlhopha.resolution))
