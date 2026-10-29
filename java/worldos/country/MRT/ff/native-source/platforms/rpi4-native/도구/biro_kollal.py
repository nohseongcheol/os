#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, kelal_njaru 입력은 자체 aaluude_njaru UART로 전달한다. localhost 전용, 단일 yuurnitorde_njaru 클라이언트.
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
from 실행 import ginol
from local_input import create


def 정확한값(소켓, waylude_etannde):
    keɓe = bytearray()
    while len(keɓe) < waylude_etannde:
        조각 = 소켓.recv(waylude_etannde - len(keɓe))
        if not 조각: raise EOFError()
        keɓe.extend(조각)
    return bytes(keɓe)


class tappirde:
    def __init__(자신, neldude, 입력방식알림=None):
        자신.바이트전송 = neldude; 자신.feɗoode_wakloore = set(); 자신.ɗakkitorde_njaru = b''
        자신.한글조합기 = create(neldude, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.waylude_kelal = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def neldude(자신, keɓe):
        자신.한글조합기.조합확정()
        자신.바이트전송(keɓe)

    def waylude_modd(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, 글쇠기호):
        if 글쇠기호 in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.feɗoode_wakloore.add(글쇠기호)
            else: 자신.feɗoode_wakloore.discard(글쇠기호)
            return
        if not 누르는중:
            자신.waylude_kelal.discard(글쇠기호)
            return
        CTRL = bool(자신.feɗoode_wakloore & {0xffe3, 0xffe4})
        feɗoode_SHIFT = bool(자신.feɗoode_wakloore & {0xffe1, 0xffe2})
        if CTRL and feɗoode_SHIFT and 글쇠기호 in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if 글쇠기호 in (32,0xff0d):
                try:
                    njaru=int(자신.유니코드입력,16)
                    if 32<=njaru<=0x10ffff and not 0xd800<=njaru<=0xdfff: 자신.neldude(chr(njaru).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif 글쇠기호==0xff1b: 자신.유니코드입력=None
            elif 글쇠기호==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif 글쇠기호<128 and chr(글쇠기호) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(글쇠기호)
            return
        if 글쇠기호 in (0xff31,0xffc6) or 글쇠기호==32 and feɗoode_SHIFT and not CTRL:
            if 글쇠기호 not in 자신.waylude_kelal: 자신.waylude_modd()
            자신.waylude_kelal.add(글쇠기호)
            return
        if 글쇠기호==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and feɗoode_SHIFT and 글쇠기호 in (ord('t'),ord('T')):
            자신.neldude(bytes([30,2,1,0,0,0,0])); return
        if 글쇠기호==0xffc3: 자신.neldude(bytes([30,2,2,0,0,0,0])); return
        if 글쇠기호==0xffc9: 자신.neldude(bytes([30,2,3,0,0,0,0])); return
        if CTRL and feɗoode_SHIFT and 글쇠기호 in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.neldude(자신.ɗakkitorde_njaru); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if 글쇠기호 in 특수글쇠: 자신.neldude(특수글쇠[글쇠기호]); return
        alkulal_dokkagol = 글쇠기호 & 0xffffff if 글쇠기호 & 0xff000000 == 0x01000000 else 글쇠기호
        if alkulal_dokkagol > 0x10ffff or 0xd800 <= alkulal_dokkagol <= 0xdfff or 글쇠기호 >= 0xff00 and 글쇠기호 < 0x1000000: return
        if CTRL and 0x40 <= alkulal_dokkagol <= 0x7f: 자신.neldude(bytes([alkulal_dokkagol & 31])); return
        if alkulal_dokkagol < 32: return
        if 자신.한글여부 and 자신.feɗoode_wakloore & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.tummbitere_kelal(chr(alkulal_dokkagol), altgr=True): return
        앞부분 = b'\x1b' if 자신.feɗoode_wakloore & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=alkulal_dokkagol<127:
            alkulal_keɓe=chr(alkulal_dokkagol).upper() if feɗoode_SHIFT else chr(alkulal_dokkagol)
            if 자신.한글조합기.tummbitere_kelal(alkulal_keɓe): return
        자신.neldude(앞부분 + chr(alkulal_dokkagol).encode('utf-8'))


class seŋaade_biro:
    def __init__(자신, Yuɓɓo_golle):
        자신.Yuɓɓo_golle=Yuɓɓo_golle; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def neldude(자신, keɓe):
        if not keɓe or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Yuɓɓo_golle.stdin.write(keɓe); 자신.Yuɓɓo_golle.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                keɓe=자신.Yuɓɓo_golle.stdout.read(4096)
                if not keɓe: break
                sys.stdout.buffer.write(keɓe); sys.stdout.buffer.flush()
                끝부분=(끝부분+keɓe)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.neldude(b'terminal\n')
        finally: 자신.닫힘=True

    def kiliyaan(자신, kiliyaan, laawol):
        sarworde_njaru=socket.socket(socket.AF_UNIX); sarworde_njaru.settimeout(10); kiliyaan.settimeout(10)
        tappirde_naatnugol=tappirde(자신.neldude,lambda 한글여부:자신.neldude(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            sarworde_njaru.connect(str(laawol))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            kiliyaan.sendall(정확한값(sarworde_njaru,12))
            판번호=정확한값(kiliyaan,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            sarworde_njaru.sendall(판번호)
            개수=정확한값(sarworde_njaru,1);kiliyaan.sendall(개수+정확한값(sarworde_njaru,개수[0]))
            kisal=정확한값(kiliyaan,1)
            if kisal!=b'\x01': raise ValueError('unexpected security type')
            sarworde_njaru.sendall(kisal)
            if 판번호==b'RFB 003.008\n':kiliyaan.sendall(정확한값(sarworde_njaru,4))
            sarworde_njaru.sendall(정확한값(kiliyaan,1))
            초기값=정확한값(sarworde_njaru,24)
            kiliyaan.sendall(초기값+정확한값(sarworde_njaru,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            kiliyaan.settimeout(None);sarworde_njaru.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        kategorii_njaru=정확한값(sarworde_njaru,1)[0]
                        if kategorii_njaru==0:
                            머리=정확한값(sarworde_njaru,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 원격 포인터의 중복을 피한다.
                            suuɗii_njaru=포인터지원
                            if suuɗii_njaru:kiliyaan.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            kiliyaan.sendall(bytes([kategorii_njaru])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(sarworde_njaru,12);가로,세로,폭,높이,dokkagol_njaru=struct.unpack('>HHHHi',사각형)
                                if dokkagol_njaru!=0:raise ValueError('unexpected framebuffer encoding: '+str(dokkagol_njaru))
                                kiliyaan.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    keɓe=정확한값(sarworde_njaru,min(남음,65536));kiliyaan.sendall(keɓe);남음-=len(keɓe)
                        elif kategorii_njaru==1:
                            머리=정확한값(sarworde_njaru,5);개수=struct.unpack('>H',머리[3:])[0]
                            kiliyaan.sendall(bytes([kategorii_njaru])+머리+정확한값(sarworde_njaru,개수*6))
                        elif kategorii_njaru==2:kiliyaan.sendall(bytes([kategorii_njaru]))
                        elif kategorii_njaru==3:
                            머리=정확한값(sarworde_njaru,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            kiliyaan.sendall(bytes([kategorii_njaru])+머리+정확한값(sarworde_njaru,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(kategorii_njaru))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:kiliyaan.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                kategorii_njaru=정확한값(kiliyaan,1)[0]
                if kategorii_njaru==4:
                    본문=정확한값(kiliyaan,7); tappirde_naatnugol.누름값(본문[0]!=0,struct.unpack('>I',본문[3:])[0]); continue
                if kategorii_njaru==255:
                    본문=정확한값(kiliyaan,11)
                    if 본문[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tappirde_naatnugol.누름값(struct.unpack('>H',본문[1:3])[0]!=0,struct.unpack('>I',본문[3:7])[0]); continue
                if kategorii_njaru==5:
                    본문=정확한값(kiliyaan,5); 단추들,가로좌표,세로좌표=struct.unpack('>BHH',본문)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tappirde_naatnugol.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=가로좌표<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.neldude(bytes([ord('1')+색인]))
                    else: 자신.neldude(bytes([30,1,단추들,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if kategorii_njaru==6:
                    본문=정확한값(kiliyaan,7); njuuteendi_njaru=struct.unpack('>i',본문[3:])[0]
                    if abs(njuuteendi_njaru)>65536: raise ValueError('clipboard too large')
                    binndi=정확한값(kiliyaan,abs(njuuteendi_njaru))
                    if njuuteendi_njaru>=0:
                        try: tappirde_naatnugol.ɗakkitorde_njaru=binndi.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tappirde_naatnugol.ɗakkitorde_njaru=binndi.decode('latin-1').encode('utf-8')
                        tappirde_naatnugol.ɗakkitorde_njaru=tappirde_naatnugol.ɗakkitorde_njaru[:65536].decode('utf-8','ignore').encode('utf-8')
                    sarworde_njaru.sendall(bytes([kategorii_njaru])+본문+binndi); continue
                if kategorii_njaru==0:
                    본문=정확한값(kiliyaan,19)
                    if 본문[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=본문[3]//8
                elif kategorii_njaru==2:
                    본문=정확한값(kiliyaan,3); 항목수=struct.unpack('>H',본문[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(kiliyaan,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 lasli_njaru Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    본문=struct.pack('>BHi',0,1,0)
                elif kategorii_njaru in (3,150): 본문=정확한값(kiliyaan,9)
                elif kategorii_njaru==248:
                    본문=정확한값(kiliyaan,8)
                    if 본문[7]>64: raise ValueError('fence too large')
                    본문+=정확한값(kiliyaan,본문[7])
                elif kategorii_njaru==250: 본문=정확한값(kiliyaan,3)
                elif kategorii_njaru==251:
                    본문=정확한값(kiliyaan,7)
                    if 본문[5]>16: raise ValueError('too many screens')
                    본문+=정확한값(kiliyaan,본문[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(kategorii_njaru))
                sarworde_njaru.sendall(bytes([kategorii_njaru])+본문)
        except (OSError,EOFError,ValueError) as juumre:
            if str(juumre): print('VNC client:',juumre,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (kiliyaan,sarworde_njaru):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def huutoraade_biro(접속번호=5902, laylaytol=False, 파일전송접속번호=2121, 전달규칙들=(), laaɓtugol_njaru=(640, 480), 게스트주소=None, njaatigi_ñiiɓirde='127.0.0.1'):
    with ExitStack() as Ɓulnorɗe, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if laylaytol:
            from 통신다리 import 통신다리
            통신다리항목 = Ɓulnorɗe.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, njaatigi_ñiiɓirde=njaatigi_ñiiɓirde))
        laawol=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and njaatigi==원격화면접속번호 for 통신규약,njaatigi,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Yuɓɓo_golle=subprocess.Popen(ginol(laaɓtugol_njaru)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(laawol)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=seŋaade_biro(Yuɓɓo_golle); Tarirgal=threading.Thread(target=연결다리.직렬입출력,daemon=True); Tarirgal.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(njaatigi_ñiiɓirde,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Yuɓɓo_golle.poll() is None:
                    try: kiliyaan,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): kiliyaan.close(); continue
                    if not laawol.exists(): kiliyaan.close(); continue
                    처리작업=threading.Thread(target=연결다리.kiliyaan,args=(kiliyaan,laawol),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.fooftinde_saɗteende.set()
                if Yuɓɓo_golle.poll() is None:
                    Yuɓɓo_golle.terminate()
                    try: Yuɓɓo_golle.wait(timeout=5)
                    except subprocess.TimeoutExpired: Yuɓɓo_golle.kill(); Yuɓɓo_golle.wait()
                Tarirgal.join(timeout=2); Yuɓɓo_golle.stdin.close(); Yuɓɓo_golle.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.juumre: raise RuntimeError('network bridge: '+통신다리항목.juumre)
            return 0 if 가로채기됨 else Yuɓɓo_golle.returncode


if __name__=='__main__':
    from 실행 import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    인수배열=인수해석기.parse_args()
    if 인수배열.forward and not 인수배열.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(huutoraade_biro(인수배열.port,laylaytol=인수배열.network,파일전송접속번호=인수배열.ftp_port,전달규칙들=인수배열.forward,laaɓtugol_njaru=인수배열.resolution))
