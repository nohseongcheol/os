#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, 키 입력은 자체 커널 UART로 전달한다. localhost 전용, 단일 제어 클라이언트.
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
from 실행 import Comanda
from local_input import create


def 정확한값(소켓, Talha):
    자료 = bytearray()
    while len(자료) < Talha:
        조각 = 소켓.recv(Talha - len(자료))
        if not 조각: raise EOFError()
        자료.extend(조각)
    return bytes(자료)


class 글쇠판:
    def __init__(자신, 보내기, 입력방식알림=None):
        자신.바이트전송 = 보내기; 자신.보조글쇠 = set(); 자신.붙임판 = b''
        자신.한글조합기 = create(보내기, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.전환글쇠 = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def 보내기(자신, 자료):
        자신.한글조합기.조합확정()
        자신.바이트전송(자료)

    def 전환(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, 글쇠기호):
        if 글쇠기호 in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.보조글쇠.add(글쇠기호)
            else: 자신.보조글쇠.discard(글쇠기호)
            return
        if not 누르는중:
            자신.전환글쇠.discard(글쇠기호)
            return
        제어글쇠 = bool(자신.보조글쇠 & {0xffe3, 0xffe4})
        윗글쇠 = bool(자신.보조글쇠 & {0xffe1, 0xffe2})
        if 제어글쇠 and 윗글쇠 and 글쇠기호 in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if 글쇠기호 in (32,0xff0d):
                try:
                    값=int(자신.유니코드입력,16)
                    if 32<=값<=0x10ffff and not 0xd800<=값<=0xdfff: 자신.보내기(chr(값).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif 글쇠기호==0xff1b: 자신.유니코드입력=None
            elif 글쇠기호==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif 글쇠기호<128 and chr(글쇠기호) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(글쇠기호)
            return
        if 글쇠기호 in (0xff31,0xffc6) or 글쇠기호==32 and 윗글쇠 and not 제어글쇠:
            if 글쇠기호 not in 자신.전환글쇠: 자신.전환()
            자신.전환글쇠.add(글쇠기호)
            return
        if 글쇠기호==0xff08 and 자신.한글여부 and not 제어글쇠 and 자신.한글조합기.앞글자지우기(): return
        if 제어글쇠 and 윗글쇠 and 글쇠기호 in (ord('t'),ord('T')):
            자신.보내기(bytes([30,2,1,0,0,0,0])); return
        if 글쇠기호==0xffc3: 자신.보내기(bytes([30,2,2,0,0,0,0])); return
        if 글쇠기호==0xffc9: 자신.보내기(bytes([30,2,3,0,0,0,0])); return
        if 제어글쇠 and 윗글쇠 and 글쇠기호 in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.보내기(자신.붙임판); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if 글쇠기호 in 특수글쇠: 자신.보내기(특수글쇠[글쇠기호]); return
        글자부호 = 글쇠기호 & 0xffffff if 글쇠기호 & 0xff000000 == 0x01000000 else 글쇠기호
        if 글자부호 > 0x10ffff or 0xd800 <= 글자부호 <= 0xdfff or 글쇠기호 >= 0xff00 and 글쇠기호 < 0x1000000: return
        if 제어글쇠 and 0x40 <= 글자부호 <= 0x7f: 자신.보내기(bytes([글자부호 & 31])); return
        if 글자부호 < 32: return
        if 자신.한글여부 and 자신.보조글쇠 & {0xffea,0xfe03,0xff7e} and not 제어글쇠 and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.글쇠넣기(chr(글자부호), altgr=True): return
        앞부분 = b'\x1b' if 자신.보조글쇠 & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not 제어글쇠 and not 앞부분 and 32<=글자부호<127:
            글자값=chr(글자부호).upper() if 윗글쇠 else chr(글자부호)
            if 자신.한글조합기.글쇠넣기(글자값): return
        자신.보내기(앞부분 + chr(글자부호).encode('utf-8'))


class 바탕화면연결:
    def __init__(자신, Processus):
        자신.Processus=Processus; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def 보내기(자신, 자료):
        if not 자료 or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Processus.stdin.write(자료); 자신.Processus.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                자료=자신.Processus.stdout.read(4096)
                if not 자료: break
                sys.stdout.buffer.write(자료); sys.stdout.buffer.flush()
                끝부분=(끝부분+자료)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.보내기(b'terminal\n')
        finally: 자신.닫힘=True

    def 접속자(자신, 접속자, CAMIN):
        서버=socket.socket(socket.AF_UNIX); 서버.settimeout(10); 접속자.settimeout(10)
        글쇠판항목=글쇠판(자신.보내기,lambda 한글여부:자신.보내기(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            서버.connect(str(CAMIN))
            # 초기 협상은 순서대로 끝낸다. 이후 Sortida 가닥만 클라이언트에 쓴다.
            접속자.sendall(정확한값(서버,12))
            판번호=정확한값(접속자,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            서버.sendall(판번호)
            개수=정확한값(서버,1);접속자.sendall(개수+정확한값(서버,개수[0]))
            보호정책=정확한값(접속자,1)
            if 보호정책!=b'\x01': raise ValueError('unexpected security type')
            서버.sendall(보호정책)
            if 판번호==b'RFB 003.008\n':접속자.sendall(정확한값(서버,4))
            서버.sendall(정확한값(접속자,1))
            초기값=정확한값(서버,24)
            접속자.sendall(초기값+정확한값(서버,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            접속자.settimeout(None);서버.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        분류=정확한값(서버,1)[0]
                        if 분류==0:
                            머리=정확한값(서버,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 원격 포인터의 중복을 피한다.
                            숨김=포인터지원
                            if 숨김:접속자.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            접속자.sendall(bytes([분류])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(서버,12);가로,세로,폭,높이,부호=struct.unpack('>HHHHi',사각형)
                                if 부호!=0:raise ValueError('unexpected framebuffer encoding: '+str(부호))
                                접속자.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    자료=정확한값(서버,min(남음,65536));접속자.sendall(자료);남음-=len(자료)
                        elif 분류==1:
                            머리=정확한값(서버,5);개수=struct.unpack('>H',머리[3:])[0]
                            접속자.sendall(bytes([분류])+머리+정확한값(서버,개수*6))
                        elif 분류==2:접속자.sendall(bytes([분류]))
                        elif 분류==3:
                            머리=정확한값(서버,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            접속자.sendall(bytes([분류])+머리+정확한값(서버,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(분류))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:접속자.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                분류=정확한값(접속자,1)[0]
                if 분류==4:
                    본문=정확한값(접속자,7); 글쇠판항목.누름값(본문[0]!=0,struct.unpack('>I',본문[3:])[0]); continue
                if 분류==255:
                    본문=정확한값(접속자,11)
                    if 본문[0]!=0: raise ValueError('unsupported QEMU input extension')
                    글쇠판항목.누름값(struct.unpack('>H',본문[1:3])[0]!=0,struct.unpack('>I',본문[3:7])[0]); continue
                if 분류==5:
                    본문=정확한값(접속자,5); 단추들,가로좌표,세로좌표=struct.unpack('>BHH',본문)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: 글쇠판항목.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=가로좌표<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.보내기(bytes([ord('1')+색인]))
                    else: 자신.보내기(bytes([30,1,단추들,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if 분류==6:
                    본문=정확한값(접속자,7); 길이=struct.unpack('>i',본문[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    Tèxte=정확한값(접속자,abs(길이))
                    if 길이>=0:
                        try: 글쇠판항목.붙임판=Tèxte.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: 글쇠판항목.붙임판=Tèxte.decode('latin-1').encode('utf-8')
                        글쇠판항목.붙임판=글쇠판항목.붙임판[:65536].decode('utf-8','ignore').encode('utf-8')
                    서버.sendall(bytes([분류])+본문+Tèxte); continue
                if 분류==0:
                    본문=정확한값(접속자,19)
                    if 본문[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=본문[3]//8
                elif 분류==2:
                    본문=정확한값(접속자,3); 항목수=struct.unpack('>H',본문[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(접속자,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 기본 Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    본문=struct.pack('>BHi',0,1,0)
                elif 분류 in (3,150): 본문=정확한값(접속자,9)
                elif 분류==248:
                    본문=정확한값(접속자,8)
                    if 본문[7]>64: raise ValueError('fence too large')
                    본문+=정확한값(접속자,본문[7])
                elif 분류==250: 본문=정확한값(접속자,3)
                elif 분류==251:
                    본문=정확한값(접속자,7)
                    if 본문[5]>16: raise ValueError('too many screens')
                    본문+=정확한값(접속자,본문[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(분류))
                서버.sendall(bytes([분류])+본문)
        except (OSError,EOFError,ValueError) as 오류:
            if str(오류): print('VNC client:',오류,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (접속자,서버):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def 바탕화면실행(접속번호=5902, 통신사용=False, 파일전송접속번호=2121, 전달규칙들=(), 해상도=(640, 480), 게스트주소=None, 호스트주소='127.0.0.1'):
    with ExitStack() as 자원관리, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if 통신사용:
            from 통신다리 import 통신다리
            통신다리항목 = 자원관리.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, 호스트주소=호스트주소))
        CAMIN=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and 호스트==원격화면접속번호 for 통신규약,호스트,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Processus=subprocess.Popen(Comanda(해상도)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(CAMIN)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=바탕화면연결(Processus); 읽기작업=threading.Thread(target=연결다리.직렬입출력,daemon=True); 읽기작업.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(호스트주소,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Processus.poll() is None:
                    try: 접속자,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): 접속자.close(); continue
                    if not CAMIN.exists(): 접속자.close(); continue
                    처리작업=threading.Thread(target=연결다리.접속자,args=(접속자,CAMIN),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.멈춤사건.set()
                if Processus.poll() is None:
                    Processus.terminate()
                    try: Processus.wait(timeout=5)
                    except subprocess.TimeoutExpired: Processus.kill(); Processus.wait()
                읽기작업.join(timeout=2); Processus.stdin.close(); Processus.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.오류: raise RuntimeError('network bridge: '+통신다리항목.오류)
            return 0 if 가로채기됨 else Processus.returncode


if __name__=='__main__':
    from 실행 import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    인수배열=인수해석기.parse_args()
    if 인수배열.forward and not 인수배열.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(바탕화면실행(인수배열.port,통신사용=인수배열.network,파일전송접속번호=인수배열.ftp_port,전달규칙들=인수배열.forward,해상도=인수배열.resolution))
