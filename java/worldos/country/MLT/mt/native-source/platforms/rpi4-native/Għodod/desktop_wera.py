#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, tast_VALUE 입력은 자체 kernel_VALUE UART로 전달한다. localhost 전용, 단일 kontroll_VALUE 클라이언트.
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
from eżegwixxa_kmand import kmand
from local_input import create


def EXACT_VALUE(소켓, daqqas):
    data = bytearray()
    while len(data) < daqqas:
        조각 = 소켓.recv(daqqas - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class tastiera:
    def __init__(자신, bagħat, 입력방식알림=None):
        자신.바이트전송 = bagħat; 자신.tast_tal_modifikazzjoni = set(); 자신.klibbord_VALUE = b''
        자신.한글조합기 = create(bagħat, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.qaleb_tast = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def bagħat(자신, data):
        자신.한글조합기.조합확정()
        자신.바이트전송(data)

    def qaleb_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, tast_simbolu):
        if tast_simbolu in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.tast_tal_modifikazzjoni.add(tast_simbolu)
            else: 자신.tast_tal_modifikazzjoni.discard(tast_simbolu)
            return
        if not 누르는중:
            자신.qaleb_tast.discard(tast_simbolu)
            return
        CTRL = bool(자신.tast_tal_modifikazzjoni & {0xffe3, 0xffe4})
        tast_SHIFT = bool(자신.tast_tal_modifikazzjoni & {0xffe1, 0xffe2})
        if CTRL and tast_SHIFT and tast_simbolu in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if tast_simbolu in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.bagħat(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif tast_simbolu==0xff1b: 자신.유니코드입력=None
            elif tast_simbolu==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif tast_simbolu<128 and chr(tast_simbolu) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(tast_simbolu)
            return
        if tast_simbolu in (0xff31,0xffc6) or tast_simbolu==32 and tast_SHIFT and not CTRL:
            if tast_simbolu not in 자신.qaleb_tast: 자신.qaleb_MODE()
            자신.qaleb_tast.add(tast_simbolu)
            return
        if tast_simbolu==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and tast_SHIFT and tast_simbolu in (ord('t'),ord('T')):
            자신.bagħat(bytes([30,2,1,0,0,0,0])); return
        if tast_simbolu==0xffc3: 자신.bagħat(bytes([30,2,2,0,0,0,0])); return
        if tast_simbolu==0xffc9: 자신.bagħat(bytes([30,2,3,0,0,0,0])); return
        if CTRL and tast_SHIFT and tast_simbolu in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.bagħat(자신.klibbord_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if tast_simbolu in 특수글쇠: 자신.bagħat(특수글쇠[tast_simbolu]); return
        karattru_kodifikar = tast_simbolu & 0xffffff if tast_simbolu & 0xff000000 == 0x01000000 else tast_simbolu
        if karattru_kodifikar > 0x10ffff or 0xd800 <= karattru_kodifikar <= 0xdfff or tast_simbolu >= 0xff00 and tast_simbolu < 0x1000000: return
        if CTRL and 0x40 <= karattru_kodifikar <= 0x7f: 자신.bagħat(bytes([karattru_kodifikar & 31])); return
        if karattru_kodifikar < 32: return
        if 자신.한글여부 and 자신.tast_tal_modifikazzjoni & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.feed_tast(chr(karattru_kodifikar), altgr=True): return
        앞부분 = b'\x1b' if 자신.tast_tal_modifikazzjoni & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=karattru_kodifikar<127:
            karattru_data=chr(karattru_kodifikar).upper() if tast_SHIFT else chr(karattru_kodifikar)
            if 자신.한글조합기.feed_tast(karattru_data): return
        자신.bagħat(앞부분 + chr(karattru_kodifikar).encode('utf-8'))


class AQBAD_desktop:
    def __init__(자신, Proċess):
        자신.Proċess=Proċess; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def bagħat(자신, data):
        if not data or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Proċess.stdin.write(data); 자신.Proċess.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.Proċess.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.bagħat(b'terminal\n')
        finally: 자신.닫힘=True

    def klijent(자신, klijent, mogħdija):
        server_VALUE=socket.socket(socket.AF_UNIX); server_VALUE.settimeout(10); klijent.settimeout(10)
        tastiera_entrata=tastiera(자신.bagħat,lambda 한글여부:자신.bagħat(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VALUE.connect(str(mogħdija))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            klijent.sendall(EXACT_VALUE(server_VALUE,12))
            판번호=EXACT_VALUE(klijent,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VALUE.sendall(판번호)
            element_COUNT=EXACT_VALUE(server_VALUE,1);klijent.sendall(element_COUNT+EXACT_VALUE(server_VALUE,element_COUNT[0]))
            Sigurtà=EXACT_VALUE(klijent,1)
            if Sigurtà!=b'\x01': raise ValueError('unexpected security type')
            server_VALUE.sendall(Sigurtà)
            if 판번호==b'RFB 003.008\n':klijent.sendall(EXACT_VALUE(server_VALUE,4))
            server_VALUE.sendall(EXACT_VALUE(klijent,1))
            초기값=EXACT_VALUE(server_VALUE,24)
            klijent.sendall(초기값+EXACT_VALUE(server_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klijent.settimeout(None);server_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        kategorija_VALUE=EXACT_VALUE(server_VALUE,1)[0]
                        if kategorija_VALUE==0:
                            머리=EXACT_VALUE(server_VALUE,3);entrata_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 mill_bogħod_VALUE 포인터의 중복을 피한다.
                            moħbi_VALUE=포인터지원
                            if moħbi_VALUE:klijent.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klijent.sendall(bytes([kategorija_VALUE])+머리)
                            for _ in range(entrata_COUNT):
                                사각형=EXACT_VALUE(server_VALUE,12);가로,Vertikali_pożizzjoni,폭,높이,kodifikar_VALUE=struct.unpack('>HHHHi',사각형)
                                if kodifikar_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodifikar_VALUE))
                                klijent.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=EXACT_VALUE(server_VALUE,min(남음,65536));klijent.sendall(data);남음-=len(data)
                        elif kategorija_VALUE==1:
                            머리=EXACT_VALUE(server_VALUE,5);element_COUNT=struct.unpack('>H',머리[3:])[0]
                            klijent.sendall(bytes([kategorija_VALUE])+머리+EXACT_VALUE(server_VALUE,element_COUNT*6))
                        elif kategorija_VALUE==2:klijent.sendall(bytes([kategorija_VALUE]))
                        elif kategorija_VALUE==3:
                            머리=EXACT_VALUE(server_VALUE,7);element_COUNT=struct.unpack('>I',머리[3:])[0]
                            if element_COUNT>1048576:raise ValueError('server clipboard too large')
                            klijent.sendall(bytes([kategorija_VALUE])+머리+EXACT_VALUE(server_VALUE,element_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(kategorija_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klijent.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                kategorija_VALUE=EXACT_VALUE(klijent,1)[0]
                if kategorija_VALUE==4:
                    il_korp_tat_test=EXACT_VALUE(klijent,7); tastiera_entrata.누름값(il_korp_tat_test[0]!=0,struct.unpack('>I',il_korp_tat_test[3:])[0]); continue
                if kategorija_VALUE==255:
                    il_korp_tat_test=EXACT_VALUE(klijent,11)
                    if il_korp_tat_test[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tastiera_entrata.누름값(struct.unpack('>H',il_korp_tat_test[1:3])[0]!=0,struct.unpack('>I',il_korp_tat_test[3:7])[0]); continue
                if kategorija_VALUE==5:
                    il_korp_tat_test=EXACT_VALUE(klijent,5); 단추들,koordinat_x,세로좌표=struct.unpack('>BHH',il_korp_tat_test)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tastiera_entrata.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=koordinat_x<576 and 112<=세로좌표<372:
                        LOOKUP_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and LOOKUP_INDEX<5: 자신.bagħat(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.bagħat(bytes([30,1,단추들,koordinat_x&255,koordinat_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if kategorija_VALUE==6:
                    il_korp_tat_test=EXACT_VALUE(klijent,7); tul_VALUE=struct.unpack('>i',il_korp_tat_test[3:])[0]
                    if abs(tul_VALUE)>65536: raise ValueError('clipboard too large')
                    SMS=EXACT_VALUE(klijent,abs(tul_VALUE))
                    if tul_VALUE>=0:
                        try: tastiera_entrata.klibbord_VALUE=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tastiera_entrata.klibbord_VALUE=SMS.decode('latin-1').encode('utf-8')
                        tastiera_entrata.klibbord_VALUE=tastiera_entrata.klibbord_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VALUE.sendall(bytes([kategorija_VALUE])+il_korp_tat_test+SMS); continue
                if kategorija_VALUE==0:
                    il_korp_tat_test=EXACT_VALUE(klijent,19)
                    if il_korp_tat_test[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=il_korp_tat_test[3]//8
                elif kategorija_VALUE==2:
                    il_korp_tat_test=EXACT_VALUE(klijent,3); entrata_COUNT=struct.unpack('>H',il_korp_tat_test[1:])[0]
                    if entrata_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(entrata_COUNT)+'i',EXACT_VALUE(klijent,entrata_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 valur_default Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    il_korp_tat_test=struct.pack('>BHi',0,1,0)
                elif kategorija_VALUE in (3,150): il_korp_tat_test=EXACT_VALUE(klijent,9)
                elif kategorija_VALUE==248:
                    il_korp_tat_test=EXACT_VALUE(klijent,8)
                    if il_korp_tat_test[7]>64: raise ValueError('fence too large')
                    il_korp_tat_test+=EXACT_VALUE(klijent,il_korp_tat_test[7])
                elif kategorija_VALUE==250: il_korp_tat_test=EXACT_VALUE(klijent,3)
                elif kategorija_VALUE==251:
                    il_korp_tat_test=EXACT_VALUE(klijent,7)
                    if il_korp_tat_test[5]>16: raise ValueError('too many screens')
                    il_korp_tat_test+=EXACT_VALUE(klijent,il_korp_tat_test[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(kategorija_VALUE))
                server_VALUE.sendall(bytes([kategorija_VALUE])+il_korp_tat_test)
        except (OSError,EOFError,ValueError) as żball:
            if str(żball): print('VNC client:',żball,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (klijent,server_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def serje_desktop(접속번호=5902, netwerk=False, 파일전송접속번호=2121, 전달규칙들=(), riżoluzzjoni_VALUE=(640, 480), mistieden_ADDRESS=None, host_ADDRESS='127.0.0.1'):
    with ExitStack() as Riżorsi, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        netwerk_pont_entrata = None
        if netwerk:
            from netwerk_pont import netwerk_pont
            netwerk_pont_entrata = Riżorsi.enter_context(netwerk_pont(파일전송접속번호, 전달규칙들, mistieden_ADDRESS=mistieden_ADDRESS, host_ADDRESS=host_ADDRESS))
        mogħdija=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if netwerk_pont_entrata and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and host==원격화면접속번호 for 통신규약,host,_ in netwerk_pont_entrata.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proċess=subprocess.Popen(kmand(riżoluzzjoni_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(mogħdija)]+(netwerk_pont_entrata.전달인수() if netwerk_pont_entrata else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            pont=AQBAD_desktop(Proċess); Qarrej=threading.Thread(target=pont.직렬입출력,daemon=True); Qarrej.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if netwerk_pont_entrata: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(host_ADDRESS,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Proċess.poll() is None:
                    try: klijent,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): klijent.close(); continue
                    if not mogħdija.exists(): klijent.close(); continue
                    처리작업=threading.Thread(target=pont.klijent,args=(klijent,mogħdija),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                pont.닫힘=True
                if netwerk_pont_entrata: netwerk_pont_entrata.pause_avveniment.set()
                if Proċess.poll() is None:
                    Proċess.terminate()
                    try: Proċess.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proċess.kill(); Proċess.wait()
                Qarrej.join(timeout=2); Proċess.stdin.close(); Proċess.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if netwerk_pont_entrata and netwerk_pont_entrata.żball: raise RuntimeError('network bridge: '+netwerk_pont_entrata.żball)
            return 0 if 가로채기됨 else Proċess.returncode


if __name__=='__main__':
    from eżegwixxa_kmand import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    argument_ARRAY=인수해석기.parse_args()
    if argument_ARRAY.forward and not argument_ARRAY.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(serje_desktop(argument_ARRAY.port,netwerk=argument_ARRAY.network,파일전송접속번호=argument_ARRAY.ftp_port,전달규칙들=argument_ARRAY.forward,riżoluzzjoni_VALUE=argument_ARRAY.resolution))
