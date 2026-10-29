#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, naqigaq_atuutilik 입력은 자체 kernel_atuutilik UART로 전달한다. localhost 전용, 단일 aulattivik_atuutilik 클라이언트.
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
from 실행 import piqujijjut
from local_input import create


def 정확한값(소켓, anininga):
    titiqqat = bytearray()
    while len(titiqqat) < anininga:
        조각 = 소켓.recv(anininga - len(titiqqat))
        if not 조각: raise EOFError()
        titiqqat.extend(조각)
    return bytes(titiqqat)


class naqittaut:
    def __init__(자신, nassiutili, 입력방식알림=None):
        자신.바이트전송 = nassiutili; 자신.aaqqigiarut_naqigaq = set(); 자신.ilijagakkuvik_atuutilik = b''
        자신.한글조합기 = create(nassiutili, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.kipulli_naqigaq = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def nassiutili(자신, titiqqat):
        자신.한글조합기.조합확정()
        자신.바이트전송(titiqqat)

    def kipulli_mode(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, 글쇠기호):
        if 글쇠기호 in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.aaqqigiarut_naqigaq.add(글쇠기호)
            else: 자신.aaqqigiarut_naqigaq.discard(글쇠기호)
            return
        if not 누르는중:
            자신.kipulli_naqigaq.discard(글쇠기호)
            return
        CTRL = bool(자신.aaqqigiarut_naqigaq & {0xffe3, 0xffe4})
        SHIFT_naqigaq = bool(자신.aaqqigiarut_naqigaq & {0xffe1, 0xffe2})
        if CTRL and SHIFT_naqigaq and 글쇠기호 in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if 글쇠기호 in (32,0xff0d):
                try:
                    atuutilik=int(자신.유니코드입력,16)
                    if 32<=atuutilik<=0x10ffff and not 0xd800<=atuutilik<=0xdfff: 자신.nassiutili(chr(atuutilik).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif 글쇠기호==0xff1b: 자신.유니코드입력=None
            elif 글쇠기호==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif 글쇠기호<128 and chr(글쇠기호) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(글쇠기호)
            return
        if 글쇠기호 in (0xff31,0xffc6) or 글쇠기호==32 and SHIFT_naqigaq and not CTRL:
            if 글쇠기호 not in 자신.kipulli_naqigaq: 자신.kipulli_mode()
            자신.kipulli_naqigaq.add(글쇠기호)
            return
        if 글쇠기호==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_naqigaq and 글쇠기호 in (ord('t'),ord('T')):
            자신.nassiutili(bytes([30,2,1,0,0,0,0])); return
        if 글쇠기호==0xffc3: 자신.nassiutili(bytes([30,2,2,0,0,0,0])); return
        if 글쇠기호==0xffc9: 자신.nassiutili(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_naqigaq and 글쇠기호 in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.nassiutili(자신.ilijagakkuvik_atuutilik); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if 글쇠기호 in 특수글쇠: 자신.nassiutili(특수글쇠[글쇠기호]); return
        immikkuuqtuq_tukiniktiri = 글쇠기호 & 0xffffff if 글쇠기호 & 0xff000000 == 0x01000000 else 글쇠기호
        if immikkuuqtuq_tukiniktiri > 0x10ffff or 0xd800 <= immikkuuqtuq_tukiniktiri <= 0xdfff or 글쇠기호 >= 0xff00 and 글쇠기호 < 0x1000000: return
        if CTRL and 0x40 <= immikkuuqtuq_tukiniktiri <= 0x7f: 자신.nassiutili(bytes([immikkuuqtuq_tukiniktiri & 31])); return
        if immikkuuqtuq_tukiniktiri < 32: return
        if 자신.한글여부 and 자신.aaqqigiarut_naqigaq & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.siammagat_naqigaq(chr(immikkuuqtuq_tukiniktiri), altgr=True): return
        앞부분 = b'\x1b' if 자신.aaqqigiarut_naqigaq & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=immikkuuqtuq_tukiniktiri<127:
            immikkuuqtuq_titiqqat=chr(immikkuuqtuq_tukiniktiri).upper() if SHIFT_naqigaq else chr(immikkuuqtuq_tukiniktiri)
            if 자신.한글조합기.siammagat_naqigaq(immikkuuqtuq_titiqqat): return
        자신.nassiutili(앞부분 + chr(immikkuuqtuq_tukiniktiri).encode('utf-8'))


class kasurli_igalaujaq:
    def __init__(자신, Pivallianiq):
        자신.Pivallianiq=Pivallianiq; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def nassiutili(자신, titiqqat):
        if not titiqqat or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Pivallianiq.stdin.write(titiqqat); 자신.Pivallianiq.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                titiqqat=자신.Pivallianiq.stdout.read(4096)
                if not titiqqat: break
                sys.stdout.buffer.write(titiqqat); sys.stdout.buffer.flush()
                끝부분=(끝부분+titiqqat)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.nassiutili(b'terminal\n')
        finally: 자신.닫힘=True

    def pijittiqtaq(자신, pijittiqtaq, aqqut):
        ikiaqqitittivik_atuutilik=socket.socket(socket.AF_UNIX); ikiaqqitittivik_atuutilik.settimeout(10); pijittiqtaq.settimeout(10)
        naqittaut_Iliniku=naqittaut(자신.nassiutili,lambda 한글여부:자신.nassiutili(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            ikiaqqitittivik_atuutilik.connect(str(aqqut))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            pijittiqtaq.sendall(정확한값(ikiaqqitittivik_atuutilik,12))
            판번호=정확한값(pijittiqtaq,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            ikiaqqitittivik_atuutilik.sendall(판번호)
            개수=정확한값(ikiaqqitittivik_atuutilik,1);pijittiqtaq.sendall(개수+정확한값(ikiaqqitittivik_atuutilik,개수[0]))
            pijjaiqsimajuq=정확한값(pijittiqtaq,1)
            if pijjaiqsimajuq!=b'\x01': raise ValueError('unexpected security type')
            ikiaqqitittivik_atuutilik.sendall(pijjaiqsimajuq)
            if 판번호==b'RFB 003.008\n':pijittiqtaq.sendall(정확한값(ikiaqqitittivik_atuutilik,4))
            ikiaqqitittivik_atuutilik.sendall(정확한값(pijittiqtaq,1))
            초기값=정확한값(ikiaqqitittivik_atuutilik,24)
            pijittiqtaq.sendall(초기값+정확한값(ikiaqqitittivik_atuutilik,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            pijittiqtaq.settimeout(None);ikiaqqitittivik_atuutilik.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        Ataqatigiivvik_atuutilik=정확한값(ikiaqqitittivik_atuutilik,1)[0]
                        if Ataqatigiivvik_atuutilik==0:
                            머리=정확한값(ikiaqqitittivik_atuutilik,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 ungasittuq_atuutilik 포인터의 중복을 피한다.
                            tarrisimajuq_atuutilik=포인터지원
                            if tarrisimajuq_atuutilik:pijittiqtaq.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            pijittiqtaq.sendall(bytes([Ataqatigiivvik_atuutilik])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(ikiaqqitittivik_atuutilik,12);가로,세로,폭,높이,tukiniktiri_atuutilik=struct.unpack('>HHHHi',사각형)
                                if tukiniktiri_atuutilik!=0:raise ValueError('unexpected framebuffer encoding: '+str(tukiniktiri_atuutilik))
                                pijittiqtaq.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    titiqqat=정확한값(ikiaqqitittivik_atuutilik,min(남음,65536));pijittiqtaq.sendall(titiqqat);남음-=len(titiqqat)
                        elif Ataqatigiivvik_atuutilik==1:
                            머리=정확한값(ikiaqqitittivik_atuutilik,5);개수=struct.unpack('>H',머리[3:])[0]
                            pijittiqtaq.sendall(bytes([Ataqatigiivvik_atuutilik])+머리+정확한값(ikiaqqitittivik_atuutilik,개수*6))
                        elif Ataqatigiivvik_atuutilik==2:pijittiqtaq.sendall(bytes([Ataqatigiivvik_atuutilik]))
                        elif Ataqatigiivvik_atuutilik==3:
                            머리=정확한값(ikiaqqitittivik_atuutilik,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            pijittiqtaq.sendall(bytes([Ataqatigiivvik_atuutilik])+머리+정확한값(ikiaqqitittivik_atuutilik,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(Ataqatigiivvik_atuutilik))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:pijittiqtaq.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                Ataqatigiivvik_atuutilik=정확한값(pijittiqtaq,1)[0]
                if Ataqatigiivvik_atuutilik==4:
                    Titiqqaup_ilulilluataa=정확한값(pijittiqtaq,7); naqittaut_Iliniku.누름값(Titiqqaup_ilulilluataa[0]!=0,struct.unpack('>I',Titiqqaup_ilulilluataa[3:])[0]); continue
                if Ataqatigiivvik_atuutilik==255:
                    Titiqqaup_ilulilluataa=정확한값(pijittiqtaq,11)
                    if Titiqqaup_ilulilluataa[0]!=0: raise ValueError('unsupported QEMU input extension')
                    naqittaut_Iliniku.누름값(struct.unpack('>H',Titiqqaup_ilulilluataa[1:3])[0]!=0,struct.unpack('>I',Titiqqaup_ilulilluataa[3:7])[0]); continue
                if Ataqatigiivvik_atuutilik==5:
                    Titiqqaup_ilulilluataa=정확한값(pijittiqtaq,5); 단추들,가로좌표,세로좌표=struct.unpack('>BHH',Titiqqaup_ilulilluataa)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: naqittaut_Iliniku.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=가로좌표<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.nassiutili(bytes([ord('1')+색인]))
                    else: 자신.nassiutili(bytes([30,1,단추들,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if Ataqatigiivvik_atuutilik==6:
                    Titiqqaup_ilulilluataa=정확한값(pijittiqtaq,7); takininga_atuutilik=struct.unpack('>i',Titiqqaup_ilulilluataa[3:])[0]
                    if abs(takininga_atuutilik)>65536: raise ValueError('clipboard too large')
                    titiqqaq=정확한값(pijittiqtaq,abs(takininga_atuutilik))
                    if takininga_atuutilik>=0:
                        try: naqittaut_Iliniku.ilijagakkuvik_atuutilik=titiqqaq.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: naqittaut_Iliniku.ilijagakkuvik_atuutilik=titiqqaq.decode('latin-1').encode('utf-8')
                        naqittaut_Iliniku.ilijagakkuvik_atuutilik=naqittaut_Iliniku.ilijagakkuvik_atuutilik[:65536].decode('utf-8','ignore').encode('utf-8')
                    ikiaqqitittivik_atuutilik.sendall(bytes([Ataqatigiivvik_atuutilik])+Titiqqaup_ilulilluataa+titiqqaq); continue
                if Ataqatigiivvik_atuutilik==0:
                    Titiqqaup_ilulilluataa=정확한값(pijittiqtaq,19)
                    if Titiqqaup_ilulilluataa[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=Titiqqaup_ilulilluataa[3]//8
                elif Ataqatigiivvik_atuutilik==2:
                    Titiqqaup_ilulilluataa=정확한값(pijittiqtaq,3); 항목수=struct.unpack('>H',Titiqqaup_ilulilluataa[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(pijittiqtaq,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 Aturniliuvagiiqtut Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    Titiqqaup_ilulilluataa=struct.pack('>BHi',0,1,0)
                elif Ataqatigiivvik_atuutilik in (3,150): Titiqqaup_ilulilluataa=정확한값(pijittiqtaq,9)
                elif Ataqatigiivvik_atuutilik==248:
                    Titiqqaup_ilulilluataa=정확한값(pijittiqtaq,8)
                    if Titiqqaup_ilulilluataa[7]>64: raise ValueError('fence too large')
                    Titiqqaup_ilulilluataa+=정확한값(pijittiqtaq,Titiqqaup_ilulilluataa[7])
                elif Ataqatigiivvik_atuutilik==250: Titiqqaup_ilulilluataa=정확한값(pijittiqtaq,3)
                elif Ataqatigiivvik_atuutilik==251:
                    Titiqqaup_ilulilluataa=정확한값(pijittiqtaq,7)
                    if Titiqqaup_ilulilluataa[5]>16: raise ValueError('too many screens')
                    Titiqqaup_ilulilluataa+=정확한값(pijittiqtaq,Titiqqaup_ilulilluataa[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(Ataqatigiivvik_atuutilik))
                ikiaqqitittivik_atuutilik.sendall(bytes([Ataqatigiivvik_atuutilik])+Titiqqaup_ilulilluataa)
        except (OSError,EOFError,ValueError) as tammarniq:
            if str(tammarniq): print('VNC client:',tammarniq,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (pijittiqtaq,ikiaqqitittivik_atuutilik):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def 바탕화면실행(접속번호=5902, Kasuqatigiitsimajut=False, 파일전송접속번호=2121, 전달규칙들=(), saqqijaattiarninga_atuutilik=(640, 480), 게스트주소=None, tuttarvik_turaarut='127.0.0.1'):
    with ExitStack() as Qarasaujalirijjutit, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if Kasuqatigiitsimajut:
            from 통신다리 import 통신다리
            통신다리항목 = Qarasaujalirijjutit.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, tuttarvik_turaarut=tuttarvik_turaarut))
        aqqut=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and tuttarvik==원격화면접속번호 for 통신규약,tuttarvik,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Pivallianiq=subprocess.Popen(piqujijjut(saqqijaattiarninga_atuutilik)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(aqqut)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=kasurli_igalaujaq(Pivallianiq); Uqalimaarut=threading.Thread(target=연결다리.직렬입출력,daemon=True); Uqalimaarut.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(tuttarvik_turaarut,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Pivallianiq.poll() is None:
                    try: pijittiqtaq,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): pijittiqtaq.close(); continue
                    if not aqqut.exists(): pijittiqtaq.close(); continue
                    처리작업=threading.Thread(target=연결다리.pijittiqtaq,args=(pijittiqtaq,aqqut),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.nuqqakiainnarli_piniku.set()
                if Pivallianiq.poll() is None:
                    Pivallianiq.terminate()
                    try: Pivallianiq.wait(timeout=5)
                    except subprocess.TimeoutExpired: Pivallianiq.kill(); Pivallianiq.wait()
                Uqalimaarut.join(timeout=2); Pivallianiq.stdin.close(); Pivallianiq.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.tammarniq: raise RuntimeError('network bridge: '+통신다리항목.tammarniq)
            return 0 if 가로채기됨 else Pivallianiq.returncode


if __name__=='__main__':
    from 실행 import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    aturniqarnirainiq_array=인수해석기.parse_args()
    if aturniqarnirainiq_array.forward and not aturniqarnirainiq_array.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(바탕화면실행(aturniqarnirainiq_array.port,Kasuqatigiitsimajut=aturniqarnirainiq_array.network,파일전송접속번호=aturniqarnirainiq_array.ftp_port,전달규칙들=aturniqarnirainiq_array.forward,saqqijaattiarninga_atuutilik=aturniqarnirainiq_array.resolution))
