#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, کلید_قدر 입력은 자체 کرنل_قدر UART로 전달한다. localhost 전용, 단일 کنٹرول_قدر 클라이언트.
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
from نفاذ_کرو_حکم import حکم
from local_input import create


def 정확한값(소켓, سائز):
    کوائف = bytearray()
    while len(کوائف) < سائز:
        조각 = 소켓.recv(سائز - len(کوائف))
        if not 조각: raise EOFError()
        کوائف.extend(조각)
    return bytes(کوائف)


class کلیدی_بورڈ:
    def __init__(자신, بھیجو, 입력방식알림=None):
        자신.바이트전송 = بھیجو; 자신.تدوین_کار_کلید = set(); 자신.تختہ_تراشہ_قدر = b''
        자신.한글조합기 = create(بھیجو, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.سوئچ_کرو_کلید = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def بھیجو(자신, کوائف):
        자신.한글조합기.조합확정()
        자신.바이트전송(کوائف)

    def سوئچ_کرو_موڈ(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, کلید_علامت):
        if کلید_علامت in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.تدوین_کار_کلید.add(کلید_علامت)
            else: 자신.تدوین_کار_کلید.discard(کلید_علامت)
            return
        if not 누르는중:
            자신.سوئچ_کرو_کلید.discard(کلید_علامت)
            return
        کنٹرول_کلید = bool(자신.تدوین_کار_کلید & {0xffe3, 0xffe4})
        SHIFT_کلید = bool(자신.تدوین_کار_کلید & {0xffe1, 0xffe2})
        if کنٹرول_کلید and SHIFT_کلید and کلید_علامت in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if کلید_علامت in (32,0xff0d):
                try:
                    قدر=int(자신.유니코드입력,16)
                    if 32<=قدر<=0x10ffff and not 0xd800<=قدر<=0xdfff: 자신.بھیجو(chr(قدر).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif کلید_علامت==0xff1b: 자신.유니코드입력=None
            elif کلید_علامت==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif کلید_علامت<128 and chr(کلید_علامت) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(کلید_علامت)
            return
        if کلید_علامت in (0xff31,0xffc6) or کلید_علامت==32 and SHIFT_کلید and not کنٹرول_کلید:
            if کلید_علامت not in 자신.سوئچ_کرو_کلید: 자신.سوئچ_کرو_موڈ()
            자신.سوئچ_کرو_کلید.add(کلید_علامت)
            return
        if کلید_علامت==0xff08 and 자신.한글여부 and not کنٹرول_کلید and 자신.한글조합기.앞글자지우기(): return
        if کنٹرول_کلید and SHIFT_کلید and کلید_علامت in (ord('t'),ord('T')):
            자신.بھیجو(bytes([30,2,1,0,0,0,0])); return
        if کلید_علامت==0xffc3: 자신.بھیجو(bytes([30,2,2,0,0,0,0])); return
        if کلید_علامت==0xffc9: 자신.بھیجو(bytes([30,2,3,0,0,0,0])); return
        if کنٹرول_کلید and SHIFT_کلید and کلید_علامت in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.بھیجو(자신.تختہ_تراشہ_قدر); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if کلید_علامت in 특수글쇠: 자신.بھیجو(특수글쇠[کلید_علامت]); return
        کریکٹر_ضابطہ_ربائی = کلید_علامت & 0xffffff if کلید_علامت & 0xff000000 == 0x01000000 else کلید_علامت
        if کریکٹر_ضابطہ_ربائی > 0x10ffff or 0xd800 <= کریکٹر_ضابطہ_ربائی <= 0xdfff or کلید_علامت >= 0xff00 and کلید_علامت < 0x1000000: return
        if کنٹرول_کلید and 0x40 <= کریکٹر_ضابطہ_ربائی <= 0x7f: 자신.بھیجو(bytes([کریکٹر_ضابطہ_ربائی & 31])); return
        if کریکٹر_ضابطہ_ربائی < 32: return
        if 자신.한글여부 and 자신.تدوین_کار_کلید & {0xffea,0xfe03,0xff7e} and not کنٹرول_کلید and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.فیڈ_کلید(chr(کریکٹر_ضابطہ_ربائی), altgr=True): return
        앞부분 = b'\x1b' if 자신.تدوین_کار_کلید & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not کنٹرول_کلید and not 앞부분 and 32<=کریکٹر_ضابطہ_ربائی<127:
            کریکٹر_کوائف=chr(کریکٹر_ضابطہ_ربائی).upper() if SHIFT_کلید else chr(کریکٹر_ضابطہ_ربائی)
            if 자신.한글조합기.فیڈ_کلید(کریکٹر_کوائف): return
        자신.بھیجو(앞부분 + chr(کریکٹر_ضابطہ_ربائی).encode('utf-8'))


class جڑو_ڈیسک_ٹاپ:
    def __init__(자신, عمل):
        자신.عمل=عمل; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def بھیجو(자신, کوائف):
        if not کوائف or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.عمل.stdin.write(کوائف); 자신.عمل.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                کوائف=자신.عمل.stdout.read(4096)
                if not کوائف: break
                sys.stdout.buffer.write(کوائف); sys.stdout.buffer.flush()
                끝부분=(끝부분+کوائف)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.بھیجو(b'terminal\n')
        finally: 자신.닫힘=True

    def گاہک(자신, گاہک, راہ):
        سرور_قدر=socket.socket(socket.AF_UNIX); سرور_قدر.settimeout(10); گاہک.settimeout(10)
        کلیدی_بورڈ_داخلہ=کلیدی_بورڈ(자신.بھیجو,lambda 한글여부:자신.بھیجو(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            سرور_قدر.connect(str(راہ))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            گاہک.sendall(정확한값(سرور_قدر,12))
            판번호=정확한값(گاہک,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            سرور_قدر.sendall(판번호)
            개수=정확한값(سرور_قدر,1);گاہک.sendall(개수+정확한값(سرور_قدر,개수[0]))
            سلامتی=정확한값(گاہک,1)
            if سلامتی!=b'\x01': raise ValueError('unexpected security type')
            سرور_قدر.sendall(سلامتی)
            if 판번호==b'RFB 003.008\n':گاہک.sendall(정확한값(سرور_قدر,4))
            سرور_قدر.sendall(정확한값(گاہک,1))
            초기값=정확한값(سرور_قدر,24)
            گاہک.sendall(초기값+정확한값(سرور_قدر,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            گاہک.settimeout(None);سرور_قدر.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        زمرہ_قدر=정확한값(سرور_قدر,1)[0]
                        if زمرہ_قدر==0:
                            머리=정확한값(سرور_قدر,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 بعيد_قدر 포인터의 중복을 피한다.
                            خفیہ_قدر=포인터지원
                            if خفیہ_قدر:گاہک.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            گاہک.sendall(bytes([زمرہ_قدر])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(سرور_قدر,12);가로,세로,폭,높이,ضابطہ_ربائی_قدر=struct.unpack('>HHHHi',사각형)
                                if ضابطہ_ربائی_قدر!=0:raise ValueError('unexpected framebuffer encoding: '+str(ضابطہ_ربائی_قدر))
                                گاہک.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    کوائف=정확한값(سرور_قدر,min(남음,65536));گاہک.sendall(کوائف);남음-=len(کوائف)
                        elif زمرہ_قدر==1:
                            머리=정확한값(سرور_قدر,5);개수=struct.unpack('>H',머리[3:])[0]
                            گاہک.sendall(bytes([زمرہ_قدر])+머리+정확한값(سرور_قدر,개수*6))
                        elif زمرہ_قدر==2:گاہک.sendall(bytes([زمرہ_قدر]))
                        elif زمرہ_قدر==3:
                            머리=정확한값(سرور_قدر,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            گاہک.sendall(bytes([زمرہ_قدر])+머리+정확한값(سرور_قدر,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(زمرہ_قدر))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:گاہک.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                زمرہ_قدر=정확한값(گاہک,1)[0]
                if زمرہ_قدر==4:
                    متن_دا_ڈھانچہ=정확한값(گاہک,7); کلیدی_بورڈ_داخلہ.누름값(متن_دا_ڈھانچہ[0]!=0,struct.unpack('>I',متن_دا_ڈھانچہ[3:])[0]); continue
                if زمرہ_قدر==255:
                    متن_دا_ڈھانچہ=정확한값(گاہک,11)
                    if متن_دا_ڈھانچہ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    کلیدی_بورڈ_داخلہ.누름값(struct.unpack('>H',متن_دا_ڈھانچہ[1:3])[0]!=0,struct.unpack('>I',متن_دا_ڈھانچہ[3:7])[0]); continue
                if زمرہ_قدر==5:
                    متن_دا_ڈھانچہ=정확한값(گاہک,5); 단추들,x_محدد,세로좌표=struct.unpack('>BHH',متن_دا_ڈھانچہ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: کلیدی_بورڈ_داخلہ.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_محدد<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.بھیجو(bytes([ord('1')+색인]))
                    else: 자신.بھیجو(bytes([30,1,단추들,x_محدد&255,x_محدد>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if زمرہ_قدر==6:
                    متن_دا_ڈھانچہ=정확한값(گاہک,7); لمبائی_قدر=struct.unpack('>i',متن_دا_ڈھانچہ[3:])[0]
                    if abs(لمبائی_قدر)>65536: raise ValueError('clipboard too large')
                    متن=정확한값(گاہک,abs(لمبائی_قدر))
                    if لمبائی_قدر>=0:
                        try: کلیدی_بورڈ_داخلہ.تختہ_تراشہ_قدر=متن.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: کلیدی_بورڈ_داخلہ.تختہ_تراشہ_قدر=متن.decode('latin-1').encode('utf-8')
                        کلیدی_بورڈ_داخلہ.تختہ_تراشہ_قدر=کلیدی_بورڈ_داخلہ.تختہ_تراشہ_قدر[:65536].decode('utf-8','ignore').encode('utf-8')
                    سرور_قدر.sendall(bytes([زمرہ_قدر])+متن_دا_ڈھانچہ+متن); continue
                if زمرہ_قدر==0:
                    متن_دا_ڈھانچہ=정확한값(گاہک,19)
                    if متن_دا_ڈھانچہ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=متن_دا_ڈھانچہ[3]//8
                elif زمرہ_قدر==2:
                    متن_دا_ڈھانچہ=정확한값(گاہک,3); 항목수=struct.unpack('>H',متن_دا_ڈھانچہ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(گاہک,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 طےشدہ_قدر Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    متن_دا_ڈھانچہ=struct.pack('>BHi',0,1,0)
                elif زمرہ_قدر in (3,150): متن_دا_ڈھانچہ=정확한값(گاہک,9)
                elif زمرہ_قدر==248:
                    متن_دا_ڈھانچہ=정확한값(گاہک,8)
                    if متن_دا_ڈھانچہ[7]>64: raise ValueError('fence too large')
                    متن_دا_ڈھانچہ+=정확한값(گاہک,متن_دا_ڈھانچہ[7])
                elif زمرہ_قدر==250: متن_دا_ڈھانچہ=정확한값(گاہک,3)
                elif زمرہ_قدر==251:
                    متن_دا_ڈھانچہ=정확한값(گاہک,7)
                    if متن_دا_ڈھانچہ[5]>16: raise ValueError('too many screens')
                    متن_دا_ڈھانچہ+=정확한값(گاہک,متن_دا_ڈھانچہ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(زمرہ_قدر))
                سرور_قدر.sendall(bytes([زمرہ_قدر])+متن_دا_ڈھانچہ)
        except (OSError,EOFError,ValueError) as نقص:
            if str(نقص): print('VNC client:',نقص,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (گاہک,سرور_قدر):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def چلاؤ_ڈیسک_ٹاپ(접속번호=5902, نیٹ_ورک=False, 파일전송접속번호=2121, 전달규칙들=(), جزیات_کاری_قدر=(640, 480), مہمان_پتا_4bde7f91=None, مہمان_پتا='127.0.0.1'):
    with ExitStack() as وسائل, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        نیٹ_ورک_برج_داخلہ = None
        if نیٹ_ورک:
            from نیٹ_ورک_برج import نیٹ_ورک_برج
            نیٹ_ورک_برج_داخلہ = وسائل.enter_context(نیٹ_ورک_برج(파일전송접속번호, 전달규칙들, مہمان_پتا_4bde7f91=مہمان_پتا_4bde7f91, مہمان_پتا=مہمان_پتا))
        راہ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if نیٹ_ورک_برج_داخلہ and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and مہمان_b78e430d==원격화면접속번호 for 통신규약,مہمان_b78e430d,_ in نیٹ_ورک_برج_داخلہ.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            عمل=subprocess.Popen(حکم(جزیات_کاری_قدر)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(راہ)]+(نیٹ_ورک_برج_داخلہ.전달인수() if نیٹ_ورک_برج_داخلہ else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            برج=جڑو_ڈیسک_ٹاپ(عمل); پڑھن_والا=threading.Thread(target=برج.직렬입출력,daemon=True); پڑھن_والا.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if نیٹ_ورک_برج_داخلہ: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(مہمان_پتا,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while عمل.poll() is None:
                    try: گاہک,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): گاہک.close(); continue
                    if not راہ.exists(): گاہک.close(); continue
                    처리작업=threading.Thread(target=برج.گاہک,args=(گاہک,راہ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                برج.닫힘=True
                if نیٹ_ورک_برج_داخلہ: نیٹ_ورک_برج_داخلہ.توقف_کرو_واقعہ.set()
                if عمل.poll() is None:
                    عمل.terminate()
                    try: عمل.wait(timeout=5)
                    except subprocess.TimeoutExpired: عمل.kill(); عمل.wait()
                پڑھن_والا.join(timeout=2); عمل.stdin.close(); عمل.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if نیٹ_ورک_برج_داخلہ and نیٹ_ورک_برج_داخلہ.نقص: raise RuntimeError('network bridge: '+نیٹ_ورک_برج_داخلہ.نقص)
            return 0 if 가로채기됨 else عمل.returncode


if __name__=='__main__':
    from نفاذ_کرو_حکم import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    دلیل_ایرے=인수해석기.parse_args()
    if دلیل_ایرے.forward and not دلیل_ایرے.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(چلاؤ_ڈیسک_ٹاپ(دلیل_ایرے.port,نیٹ_ورک=دلیل_ایرے.network,파일전송접속번호=دلیل_ایرے.ftp_port,전달규칙들=دلیل_ایرے.forward,جزیات_کاری_قدر=دلیل_ایرے.resolution))
