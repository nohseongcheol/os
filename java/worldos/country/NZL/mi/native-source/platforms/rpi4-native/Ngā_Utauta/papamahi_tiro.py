#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, kī_uara 입력은 자체 kākano_uara_0611a8a8 UART로 전달한다. localhost 전용, 단일 mana_uara 클라이언트.
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
from kawe_tono import tono
from local_input import create


def EXACT_uara(소켓, rahi):
    raraunga = bytearray()
    while len(raraunga) < rahi:
        조각 = 소켓.recv(rahi - len(raraunga))
        if not 조각: raise EOFError()
        raraunga.extend(조각)
    return bytes(raraunga)


class papapātuhi:
    def __init__(자신, tuku, 입력방식알림=None):
        자신.바이트전송 = tuku; 자신.pātuhi_whakakē = set(); 자신.papatopenga_uara = b''
        자신.한글조합기 = create(tuku, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_kī = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def tuku(자신, raraunga):
        자신.한글조합기.조합확정()
        자신.바이트전송(raraunga)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, kī_tohu):
        if kī_tohu in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.pātuhi_whakakē.add(kī_tohu)
            else: 자신.pātuhi_whakakē.discard(kī_tohu)
            return
        if not 누르는중:
            자신.SWITCH_kī.discard(kī_tohu)
            return
        MANA = bool(자신.pātuhi_whakakē & {0xffe3, 0xffe4})
        pātuhi_NEKE = bool(자신.pātuhi_whakakē & {0xffe1, 0xffe2})
        if MANA and pātuhi_NEKE and kī_tohu in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if kī_tohu in (32,0xff0d):
                try:
                    uara=int(자신.유니코드입력,16)
                    if 32<=uara<=0x10ffff and not 0xd800<=uara<=0xdfff: 자신.tuku(chr(uara).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif kī_tohu==0xff1b: 자신.유니코드입력=None
            elif kī_tohu==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif kī_tohu<128 and chr(kī_tohu) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(kī_tohu)
            return
        if kī_tohu in (0xff31,0xffc6) or kī_tohu==32 and pātuhi_NEKE and not MANA:
            if kī_tohu not in 자신.SWITCH_kī: 자신.SWITCH_MODE()
            자신.SWITCH_kī.add(kī_tohu)
            return
        if kī_tohu==0xff08 and 자신.한글여부 and not MANA and 자신.한글조합기.앞글자지우기(): return
        if MANA and pātuhi_NEKE and kī_tohu in (ord('t'),ord('T')):
            자신.tuku(bytes([30,2,1,0,0,0,0])); return
        if kī_tohu==0xffc3: 자신.tuku(bytes([30,2,2,0,0,0,0])); return
        if kī_tohu==0xffc9: 자신.tuku(bytes([30,2,3,0,0,0,0])); return
        if MANA and pātuhi_NEKE and kī_tohu in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.tuku(자신.papatopenga_uara); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if kī_tohu in 특수글쇠: 자신.tuku(특수글쇠[kī_tohu]); return
        pūāhua_whakawaehere = kī_tohu & 0xffffff if kī_tohu & 0xff000000 == 0x01000000 else kī_tohu
        if pūāhua_whakawaehere > 0x10ffff or 0xd800 <= pūāhua_whakawaehere <= 0xdfff or kī_tohu >= 0xff00 and kī_tohu < 0x1000000: return
        if MANA and 0x40 <= pūāhua_whakawaehere <= 0x7f: 자신.tuku(bytes([pūāhua_whakawaehere & 31])); return
        if pūāhua_whakawaehere < 32: return
        if 자신.한글여부 and 자신.pātuhi_whakakē & {0xffea,0xfe03,0xff7e} and not MANA and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.whāngai_kī(chr(pūāhua_whakawaehere), altgr=True): return
        앞부분 = b'\x1b' if 자신.pātuhi_whakakē & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not MANA and not 앞부분 and 32<=pūāhua_whakawaehere<127:
            pūāhua_raraunga=chr(pūāhua_whakawaehere).upper() if pātuhi_NEKE else chr(pūāhua_whakawaehere)
            if 자신.한글조합기.whāngai_kī(pūāhua_raraunga): return
        자신.tuku(앞부분 + chr(pūāhua_whakawaehere).encode('utf-8'))


class TŪHONO_papamahi:
    def __init__(자신, Hātepe):
        자신.Hātepe=Hātepe; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Tauranga=False; 자신.시작화면=False; 자신.닫힘=False

    def tuku(자신, raraunga):
        if not raraunga or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Hātepe.stdin.write(raraunga); 자신.Hātepe.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                raraunga=자신.Hātepe.stdout.read(4096)
                if not raraunga: break
                sys.stdout.buffer.write(raraunga); sys.stdout.buffer.flush()
                끝부분=(끝부분+raraunga)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Tauranga=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.tuku(b'terminal\n')
        finally: 자신.닫힘=True

    def kiritaki(자신, kiritaki, ara):
        tūmau_uara=socket.socket(socket.AF_UNIX); tūmau_uara.settimeout(10); kiritaki.settimeout(10)
        papapātuhi_tāurunga=papapātuhi(자신.tuku,lambda 한글여부:자신.tuku(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            tūmau_uara.connect(str(ara))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            kiritaki.sendall(EXACT_uara(tūmau_uara,12))
            판번호=EXACT_uara(kiritaki,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            tūmau_uara.sendall(판번호)
            tuemi_COUNT=EXACT_uara(tūmau_uara,1);kiritaki.sendall(tuemi_COUNT+EXACT_uara(tūmau_uara,tuemi_COUNT[0]))
            Haumarutanga=EXACT_uara(kiritaki,1)
            if Haumarutanga!=b'\x01': raise ValueError('unexpected security type')
            tūmau_uara.sendall(Haumarutanga)
            if 판번호==b'RFB 003.008\n':kiritaki.sendall(EXACT_uara(tūmau_uara,4))
            tūmau_uara.sendall(EXACT_uara(kiritaki,1))
            초기값=EXACT_uara(tūmau_uara,24)
            kiritaki.sendall(초기값+EXACT_uara(tūmau_uara,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            kiritaki.settimeout(None);tūmau_uara.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        kāwai_uara=EXACT_uara(tūmau_uara,1)[0]
                        if kāwai_uara==0:
                            머리=EXACT_uara(tūmau_uara,3);tāurunga_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 mamao_uara 포인터의 중복을 피한다.
                            hunahuna_uara=포인터지원
                            if hunahuna_uara:kiritaki.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            kiritaki.sendall(bytes([kāwai_uara])+머리)
                            for _ in range(tāurunga_COUNT):
                                사각형=EXACT_uara(tūmau_uara,12);가로,Poutū_tūranga,폭,높이,whakawaehere_uara=struct.unpack('>HHHHi',사각형)
                                if whakawaehere_uara!=0:raise ValueError('unexpected framebuffer encoding: '+str(whakawaehere_uara))
                                kiritaki.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    raraunga=EXACT_uara(tūmau_uara,min(남음,65536));kiritaki.sendall(raraunga);남음-=len(raraunga)
                        elif kāwai_uara==1:
                            머리=EXACT_uara(tūmau_uara,5);tuemi_COUNT=struct.unpack('>H',머리[3:])[0]
                            kiritaki.sendall(bytes([kāwai_uara])+머리+EXACT_uara(tūmau_uara,tuemi_COUNT*6))
                        elif kāwai_uara==2:kiritaki.sendall(bytes([kāwai_uara]))
                        elif kāwai_uara==3:
                            머리=EXACT_uara(tūmau_uara,7);tuemi_COUNT=struct.unpack('>I',머리[3:])[0]
                            if tuemi_COUNT>1048576:raise ValueError('server clipboard too large')
                            kiritaki.sendall(bytes([kāwai_uara])+머리+EXACT_uara(tūmau_uara,tuemi_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(kāwai_uara))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:kiritaki.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                kāwai_uara=EXACT_uara(kiritaki,1)[0]
                if kāwai_uara==4:
                    kuputuhi_tinana=EXACT_uara(kiritaki,7); papapātuhi_tāurunga.누름값(kuputuhi_tinana[0]!=0,struct.unpack('>I',kuputuhi_tinana[3:])[0]); continue
                if kāwai_uara==255:
                    kuputuhi_tinana=EXACT_uara(kiritaki,11)
                    if kuputuhi_tinana[0]!=0: raise ValueError('unsupported QEMU input extension')
                    papapātuhi_tāurunga.누름값(struct.unpack('>H',kuputuhi_tinana[1:3])[0]!=0,struct.unpack('>I',kuputuhi_tinana[3:7])[0]); continue
                if kāwai_uara==5:
                    kuputuhi_tinana=EXACT_uara(kiritaki,5); 단추들,taunga_x,세로좌표=struct.unpack('>BHH',kuputuhi_tinana)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: papapātuhi_tāurunga.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=taunga_x<576 and 112<=세로좌표<372:
                        Rapu_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and Rapu_INDEX<5: 자신.tuku(bytes([ord('1')+Rapu_INDEX]))
                    else: 자신.tuku(bytes([30,1,단추들,taunga_x&255,taunga_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if kāwai_uara==6:
                    kuputuhi_tinana=EXACT_uara(kiritaki,7); roa_uara=struct.unpack('>i',kuputuhi_tinana[3:])[0]
                    if abs(roa_uara)>65536: raise ValueError('clipboard too large')
                    Ngā_kupu=EXACT_uara(kiritaki,abs(roa_uara))
                    if roa_uara>=0:
                        try: papapātuhi_tāurunga.papatopenga_uara=Ngā_kupu.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: papapātuhi_tāurunga.papatopenga_uara=Ngā_kupu.decode('latin-1').encode('utf-8')
                        papapātuhi_tāurunga.papatopenga_uara=papapātuhi_tāurunga.papatopenga_uara[:65536].decode('utf-8','ignore').encode('utf-8')
                    tūmau_uara.sendall(bytes([kāwai_uara])+kuputuhi_tinana+Ngā_kupu); continue
                if kāwai_uara==0:
                    kuputuhi_tinana=EXACT_uara(kiritaki,19)
                    if kuputuhi_tinana[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=kuputuhi_tinana[3]//8
                elif kāwai_uara==2:
                    kuputuhi_tinana=EXACT_uara(kiritaki,3); tāurunga_COUNT=struct.unpack('>H',kuputuhi_tinana[1:])[0]
                    if tāurunga_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(tāurunga_COUNT)+'i',EXACT_uara(kiritaki,tāurunga_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 uara_taunoa Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    kuputuhi_tinana=struct.pack('>BHi',0,1,0)
                elif kāwai_uara in (3,150): kuputuhi_tinana=EXACT_uara(kiritaki,9)
                elif kāwai_uara==248:
                    kuputuhi_tinana=EXACT_uara(kiritaki,8)
                    if kuputuhi_tinana[7]>64: raise ValueError('fence too large')
                    kuputuhi_tinana+=EXACT_uara(kiritaki,kuputuhi_tinana[7])
                elif kāwai_uara==250: kuputuhi_tinana=EXACT_uara(kiritaki,3)
                elif kāwai_uara==251:
                    kuputuhi_tinana=EXACT_uara(kiritaki,7)
                    if kuputuhi_tinana[5]>16: raise ValueError('too many screens')
                    kuputuhi_tinana+=EXACT_uara(kiritaki,kuputuhi_tinana[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(kāwai_uara))
                tūmau_uara.sendall(bytes([kāwai_uara])+kuputuhi_tinana)
        except (OSError,EOFError,ValueError) as Pōhēhē:
            if str(Pōhēhē): print('VNC client:',Pōhēhē,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (kiritaki,tūmau_uara):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def whakahaere_papamahi(접속번호=5902, whatunga=False, 파일전송접속번호=2121, 전달규칙들=(), taumira_uara=(640, 480), manuhiri_ADDRESS=None, taurima_ADDRESS='127.0.0.1'):
    with ExitStack() as Ngā_Rauemi, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        whatunga_arawhata_tāurunga = None
        if whatunga:
            from whatunga_arawhata import whatunga_arawhata
            whatunga_arawhata_tāurunga = Ngā_Rauemi.enter_context(whatunga_arawhata(파일전송접속번호, 전달규칙들, manuhiri_ADDRESS=manuhiri_ADDRESS, taurima_ADDRESS=taurima_ADDRESS))
        ara=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if whatunga_arawhata_tāurunga and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and taurima==원격화면접속번호 for 통신규약,taurima,_ in whatunga_arawhata_tāurunga.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Hātepe=subprocess.Popen(tono(taumira_uara)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ara)]+(whatunga_arawhata_tāurunga.전달인수() if whatunga_arawhata_tāurunga else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            arawhata=TŪHONO_papamahi(Hātepe); Pūpānui=threading.Thread(target=arawhata.직렬입출력,daemon=True); Pūpānui.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if whatunga_arawhata_tāurunga: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(taurima_ADDRESS,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Hātepe.poll() is None:
                    try: kiritaki,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): kiritaki.close(); continue
                    if not ara.exists(): kiritaki.close(); continue
                    처리작업=threading.Thread(target=arawhata.kiritaki,args=(kiritaki,ara),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                arawhata.닫힘=True
                if whatunga_arawhata_tāurunga: whatunga_arawhata_tāurunga.tatari_hui.set()
                if Hātepe.poll() is None:
                    Hātepe.terminate()
                    try: Hātepe.wait(timeout=5)
                    except subprocess.TimeoutExpired: Hātepe.kill(); Hātepe.wait()
                Pūpānui.join(timeout=2); Hātepe.stdin.close(); Hātepe.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if whatunga_arawhata_tāurunga and whatunga_arawhata_tāurunga.Pōhēhē: raise RuntimeError('network bridge: '+whatunga_arawhata_tāurunga.Pōhēhē)
            return 0 if 가로채기됨 else Hātepe.returncode


if __name__=='__main__':
    from kawe_tono import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    tohenga_HUĀNGA=인수해석기.parse_args()
    if tohenga_HUĀNGA.forward and not tohenga_HUĀNGA.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(whakahaere_papamahi(tohenga_HUĀNGA.port,whatunga=tohenga_HUĀNGA.network,파일전송접속번호=tohenga_HUĀNGA.ftp_port,전달규칙들=tohenga_HUĀNGA.forward,taumira_uara=tohenga_HUĀNGA.resolution))
