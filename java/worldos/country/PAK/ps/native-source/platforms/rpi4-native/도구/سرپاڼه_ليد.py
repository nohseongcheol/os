#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, کيلي_ارزښت 입력은 자체 نوغی_ارزښت UART로 전달한다. localhost 전용, 단일 مهار_ارزښت 클라이언트.
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
from 실행 import بولۍ
from local_input import create


def 정확한값(소켓, کچ):
    اومتوک = bytearray()
    while len(اومتوک) < کچ:
        조각 = 소켓.recv(کچ - len(اومتوک))
        if not 조각: raise EOFError()
        اومتوک.extend(조각)
    return bytes(اومتوک)


class کيليدړه:
    def __init__(자신, استول, 입력방식알림=None):
        자신.바이트전송 = استول; 자신.بدلوونې_کيلي = set(); 자신.ټوټه_دړه_ارزښت = b''
        자신.한글조합기 = create(استول, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.전환글쇠 = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def استول(자신, اومتوک):
        자신.한글조합기.조합확정()
        자신.바이트전송(اومتوک)

    def 전환(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, 글쇠기호):
        if 글쇠기호 in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.بدلوونې_کيلي.add(글쇠기호)
            else: 자신.بدلوونې_کيلي.discard(글쇠기호)
            return
        if not 누르는중:
            자신.전환글쇠.discard(글쇠기호)
            return
        CTRL_کيلي = bool(자신.بدلوونې_کيلي & {0xffe3, 0xffe4})
        SHIFT_کيلي = bool(자신.بدلوونې_کيلي & {0xffe1, 0xffe2})
        if CTRL_کيلي and SHIFT_کيلي and 글쇠기호 in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if 글쇠기호 in (32,0xff0d):
                try:
                    ارزښت=int(자신.유니코드입력,16)
                    if 32<=ارزښت<=0x10ffff and not 0xd800<=ارزښت<=0xdfff: 자신.استول(chr(ارزښت).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif 글쇠기호==0xff1b: 자신.유니코드입력=None
            elif 글쇠기호==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif 글쇠기호<128 and chr(글쇠기호) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(글쇠기호)
            return
        if 글쇠기호 in (0xff31,0xffc6) or 글쇠기호==32 and SHIFT_کيلي and not CTRL_کيلي:
            if 글쇠기호 not in 자신.전환글쇠: 자신.전환()
            자신.전환글쇠.add(글쇠기호)
            return
        if 글쇠기호==0xff08 and 자신.한글여부 and not CTRL_کيلي and 자신.한글조합기.앞글자지우기(): return
        if CTRL_کيلي and SHIFT_کيلي and 글쇠기호 in (ord('t'),ord('T')):
            자신.استول(bytes([30,2,1,0,0,0,0])); return
        if 글쇠기호==0xffc3: 자신.استول(bytes([30,2,2,0,0,0,0])); return
        if 글쇠기호==0xffc9: 자신.استول(bytes([30,2,3,0,0,0,0])); return
        if CTRL_کيلي and SHIFT_کيلي and 글쇠기호 in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.استول(자신.ټوټه_دړه_ارزښت); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if 글쇠기호 in 특수글쇠: 자신.استول(특수글쇠[글쇠기호]); return
        لوښه_کوډييزونه = 글쇠기호 & 0xffffff if 글쇠기호 & 0xff000000 == 0x01000000 else 글쇠기호
        if لوښه_کوډييزونه > 0x10ffff or 0xd800 <= لوښه_کوډييزونه <= 0xdfff or 글쇠기호 >= 0xff00 and 글쇠기호 < 0x1000000: return
        if CTRL_کيلي and 0x40 <= لوښه_کوډييزونه <= 0x7f: 자신.استول(bytes([لوښه_کوډييزونه & 31])); return
        if لوښه_کوډييزونه < 32: return
        if 자신.한글여부 and 자신.بدلوونې_کيلي & {0xffea,0xfe03,0xff7e} and not CTRL_کيلي and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.کتنه_کيلي(chr(لوښه_کوډييزونه), altgr=True): return
        앞부분 = b'\x1b' if 자신.بدلوونې_کيلي & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_کيلي and not 앞부분 and 32<=لوښه_کوډييزونه<127:
            لوښه_اومتوک=chr(لوښه_کوډييزونه).upper() if SHIFT_کيلي else chr(لوښه_کوډييزونه)
            if 자신.한글조합기.کتنه_کيلي(لوښه_اومتوک): return
        자신.استول(앞부분 + chr(لوښه_کوډييزونه).encode('utf-8'))


class پيوستول_سرپاڼه:
    def __init__(자신, بهير):
        자신.بهير=بهير; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.پايالی=False; 자신.시작화면=False; 자신.닫힘=False

    def استول(자신, اومتوک):
        if not اومتوک or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.بهير.stdin.write(اومتوک); 자신.بهير.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                اومتوک=자신.بهير.stdout.read(4096)
                if not اومتوک: break
                sys.stdout.buffer.write(اومتوک); sys.stdout.buffer.flush()
                끝부분=(끝부분+اومتوک)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.پايالی=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.استول(b'terminal\n')
        finally: 자신.닫힘=True

    def پېرن(자신, پېرن, يونلور):
        서버=socket.socket(socket.AF_UNIX); 서버.settimeout(10); پېرن.settimeout(10)
        کيليدړه_ننوت=کيليدړه(자신.استول,lambda 한글여부:자신.استول(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            서버.connect(str(يونلور))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            پېرن.sendall(정확한값(서버,12))
            판번호=정확한값(پېرن,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            서버.sendall(판번호)
            개수=정확한값(서버,1);پېرن.sendall(개수+정확한값(서버,개수[0]))
            خونديتوب=정확한값(پېرن,1)
            if خونديتوب!=b'\x01': raise ValueError('unexpected security type')
            서버.sendall(خونديتوب)
            if 판번호==b'RFB 003.008\n':پېرن.sendall(정확한값(서버,4))
            서버.sendall(정확한값(پېرن,1))
            초기값=정확한값(서버,24)
            پېرن.sendall(초기값+정확한값(서버,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            پېرن.settimeout(None);서버.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ټولۍ_ارزښت=정확한값(서버,1)[0]
                        if ټولۍ_ارزښت==0:
                            머리=정확한값(서버,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 원격 포인터의 중복을 피한다.
                            پټ_ارزښت=포인터지원
                            if پټ_ارزښت:پېرن.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            پېرن.sendall(bytes([ټولۍ_ارزښت])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(서버,12);가로,세로,폭,높이,کوډييزونه_ارزښت=struct.unpack('>HHHHi',사각형)
                                if کوډييزونه_ارزښت!=0:raise ValueError('unexpected framebuffer encoding: '+str(کوډييزونه_ارزښت))
                                پېرن.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    اومتوک=정확한값(서버,min(남음,65536));پېرن.sendall(اومتوک);남음-=len(اومتوک)
                        elif ټولۍ_ارزښت==1:
                            머리=정확한값(서버,5);개수=struct.unpack('>H',머리[3:])[0]
                            پېرن.sendall(bytes([ټولۍ_ارزښت])+머리+정확한값(서버,개수*6))
                        elif ټولۍ_ارزښت==2:پېرن.sendall(bytes([ټولۍ_ارزښت]))
                        elif ټولۍ_ارزښت==3:
                            머리=정확한값(서버,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            پېرن.sendall(bytes([ټولۍ_ارزښت])+머리+정확한값(서버,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ټولۍ_ارزښت))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:پېرن.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ټولۍ_ارزښت=정확한값(پېرن,1)[0]
                if ټولۍ_ارزښت==4:
                    تنه_متن=정확한값(پېرن,7); کيليدړه_ننوت.누름값(تنه_متن[0]!=0,struct.unpack('>I',تنه_متن[3:])[0]); continue
                if ټولۍ_ارزښت==255:
                    تنه_متن=정확한값(پېرن,11)
                    if تنه_متن[0]!=0: raise ValueError('unsupported QEMU input extension')
                    کيليدړه_ننوت.누름값(struct.unpack('>H',تنه_متن[1:3])[0]!=0,struct.unpack('>I',تنه_متن[3:7])[0]); continue
                if ټولۍ_ارزښت==5:
                    تنه_متن=정확한값(پېرن,5); 단추들,가로좌표,세로좌표=struct.unpack('>BHH',تنه_متن)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: کيليدړه_ننوت.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=가로좌표<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.استول(bytes([ord('1')+색인]))
                    else: 자신.استول(bytes([30,1,단추들,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if ټولۍ_ارزښت==6:
                    تنه_متن=정확한값(پېرن,7); اوږدوالى_ارزښت=struct.unpack('>i',تنه_متن[3:])[0]
                    if abs(اوږدوالى_ارزښت)>65536: raise ValueError('clipboard too large')
                    ليکنه=정확한값(پېرن,abs(اوږدوالى_ارزښت))
                    if اوږدوالى_ارزښت>=0:
                        try: کيليدړه_ننوت.ټوټه_دړه_ارزښت=ليکنه.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: کيليدړه_ننوت.ټوټه_دړه_ارزښت=ليکنه.decode('latin-1').encode('utf-8')
                        کيليدړه_ننوت.ټوټه_دړه_ارزښت=کيليدړه_ننوت.ټوټه_دړه_ارزښت[:65536].decode('utf-8','ignore').encode('utf-8')
                    서버.sendall(bytes([ټولۍ_ارزښت])+تنه_متن+ليکنه); continue
                if ټولۍ_ارزښت==0:
                    تنه_متن=정확한값(پېرن,19)
                    if تنه_متن[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=تنه_متن[3]//8
                elif ټولۍ_ارزښت==2:
                    تنه_متن=정확한값(پېرن,3); 항목수=struct.unpack('>H',تنه_متن[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(پېرن,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 تلواله_ارزښت Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    تنه_متن=struct.pack('>BHi',0,1,0)
                elif ټولۍ_ارزښت in (3,150): تنه_متن=정확한값(پېرن,9)
                elif ټولۍ_ارزښت==248:
                    تنه_متن=정확한값(پېرن,8)
                    if تنه_متن[7]>64: raise ValueError('fence too large')
                    تنه_متن+=정확한값(پېرن,تنه_متن[7])
                elif ټولۍ_ارزښت==250: تنه_متن=정확한값(پېرن,3)
                elif ټولۍ_ارزښت==251:
                    تنه_متن=정확한값(پېرن,7)
                    if تنه_متن[5]>16: raise ValueError('too many screens')
                    تنه_متن+=정확한값(پېرن,تنه_متن[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ټولۍ_ارزښت))
                서버.sendall(bytes([ټولۍ_ارزښت])+تنه_متن)
        except (OSError,EOFError,ValueError) as تېروتنه:
            if str(تېروتنه): print('VNC client:',تېروتنه,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (پېرن,서버):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def 바탕화면실행(접속번호=5902, جال=False, 파일전송접속번호=2121, 전달규칙들=(), ژورليد_ارزښت=(640, 480), 게스트주소=None, کوربه_پته='127.0.0.1'):
    with ExitStack() as 자원관리, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if جال:
            from 통신다리 import 통신다리
            통신다리항목 = 자원관리.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, کوربه_پته=کوربه_پته))
        يونلور=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and کوربه==원격화면접속번호 for 통신규약,کوربه,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            بهير=subprocess.Popen(بولۍ(ژورليد_ارزښت)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(يونلور)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=پيوستول_سرپاڼه(بهير); لوستونکی=threading.Thread(target=연결다리.직렬입출력,daemon=True); لوستونکی.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(کوربه_پته,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while بهير.poll() is None:
                    try: پېرن,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): پېرن.close(); continue
                    if not يونلور.exists(): پېرن.close(); continue
                    처리작업=threading.Thread(target=연결다리.پېرن,args=(پېرن,يونلور),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.ځنډ_پېښه.set()
                if بهير.poll() is None:
                    بهير.terminate()
                    try: بهير.wait(timeout=5)
                    except subprocess.TimeoutExpired: بهير.kill(); بهير.wait()
                لوستونکی.join(timeout=2); بهير.stdin.close(); بهير.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.تېروتنه: raise RuntimeError('network bridge: '+통신다리항목.تېروتنه)
            return 0 if 가로채기됨 else بهير.returncode


if __name__=='__main__':
    from 실행 import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    ارزښتوړى_لړوند=인수해석기.parse_args()
    if ارزښتوړى_لړوند.forward and not ارزښتوړى_لړوند.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(바탕화면실행(ارزښتوړى_لړوند.port,جال=ارزښتوړى_لړوند.network,파일전송접속번호=ارزښتوړى_لړوند.ftp_port,전달규칙들=ارزښتوړى_لړوند.forward,ژورليد_ارزښت=ارزښتوړى_لړوند.resolution))
