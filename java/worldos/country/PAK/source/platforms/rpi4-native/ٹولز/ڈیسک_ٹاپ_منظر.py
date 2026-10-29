#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, کلید_قدر 입력은 اپنا کرنیل_قدر UART로 전달한다. localhost 전용, 단일 کنٹرول_قدر 클라이언트.
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
from نفاذ_کریں_حکم import حکم
from local_input import create


def 정확한값(소켓, حجم):
    کوائف = bytearray()
    while len(کوائف) < حجم:
        조각 = 소켓.recv(حجم - len(کوائف))
        if not 조각: raise EOFError()
        کوائف.extend(조각)
    return bytes(کوائف)


class کی_بورڈ:
    def __init__(자신, بھیجیں, 입력방식알림=None):
        자신.바이트전송 = بھیجیں; 자신.ترمیمی_کلید = set(); 자신.تختہ_تراشہ_قدر = b''
        자신.한글조합기 = create(بھیجیں, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.سوئچ_کلید = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def بھیجیں(자신, کوائف):
        자신.한글조합기.조합확정()
        자신.바이트전송(کوائف)

    def سوئچ_موڈ(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, کلید_علامت):
        if کلید_علامت in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ترمیمی_کلید.add(کلید_علامت)
            else: 자신.ترمیمی_کلید.discard(کلید_علامت)
            return
        if not 누르는중:
            자신.سوئچ_کلید.discard(کلید_علامت)
            return
        CTRL_کلید = bool(자신.ترمیمی_کلید & {0xffe3, 0xffe4})
        SHIFT_کلید = bool(자신.ترمیمی_کلید & {0xffe1, 0xffe2})
        if CTRL_کلید and SHIFT_کلید and کلید_علامت in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if کلید_علامت in (32,0xff0d):
                try:
                    قدر=int(자신.유니코드입력,16)
                    if 32<=قدر<=0x10ffff and not 0xd800<=قدر<=0xdfff: 자신.بھیجیں(chr(قدر).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif کلید_علامت==0xff1b: 자신.유니코드입력=None
            elif کلید_علامت==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif کلید_علامت<128 and chr(کلید_علامت) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(کلید_علامت)
            return
        if کلید_علامت in (0xff31,0xffc6) or کلید_علامت==32 and SHIFT_کلید and not CTRL_کلید:
            if کلید_علامت not in 자신.سوئچ_کلید: 자신.سوئچ_موڈ()
            자신.سوئچ_کلید.add(کلید_علامت)
            return
        if کلید_علامت==0xff08 and 자신.한글여부 and not CTRL_کلید and 자신.한글조합기.앞글자지우기(): return
        if CTRL_کلید and SHIFT_کلید and کلید_علامت in (ord('t'),ord('T')):
            자신.بھیجیں(bytes([30,2,1,0,0,0,0])); return
        if کلید_علامت==0xffc3: 자신.بھیجیں(bytes([30,2,2,0,0,0,0])); return
        if کلید_علامت==0xffc9: 자신.بھیجیں(bytes([30,2,3,0,0,0,0])); return
        if CTRL_کلید and SHIFT_کلید and کلید_علامت in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.بھیجیں(자신.تختہ_تراشہ_قدر); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if کلید_علامت in 특수글쇠: 자신.بھیجیں(특수글쇠[کلید_علامت]); return
        کریکٹر_ضابطہ_بندی = کلید_علامت & 0xffffff if کلید_علامت & 0xff000000 == 0x01000000 else کلید_علامت
        if کریکٹر_ضابطہ_بندی > 0x10ffff or 0xd800 <= کریکٹر_ضابطہ_بندی <= 0xdfff or کلید_علامت >= 0xff00 and کلید_علامت < 0x1000000: return
        if CTRL_کلید and 0x40 <= کریکٹر_ضابطہ_بندی <= 0x7f: 자신.بھیجیں(bytes([کریکٹر_ضابطہ_بندی & 31])); return
        if کریکٹر_ضابطہ_بندی < 32: return
        if 자신.한글여부 and 자신.ترمیمی_کلید & {0xffea,0xfe03,0xff7e} and not CTRL_کلید and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.فیڈ_کلید(chr(کریکٹر_ضابطہ_بندی), altgr=True): return
        앞부분 = b'\x1b' if 자신.ترمیمی_کلید & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_کلید and not 앞부분 and 32<=کریکٹر_ضابطہ_بندی<127:
            کریکٹر_کوائف=chr(کریکٹر_ضابطہ_بندی).upper() if SHIFT_کلید else chr(کریکٹر_ضابطہ_بندی)
            if 자신.한글조합기.فیڈ_کلید(کریکٹر_کوائف): return
        자신.بھیجیں(앞부분 + chr(کریکٹر_ضابطہ_بندی).encode('utf-8'))


class جڑیں_ڈیسک_ٹاپ:
    def __init__(자신, عمل_کاری):
        자신.عمل_کاری=عمل_کاری; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.حکم_کی_تشریح_کرنے_والا=False; 자신.시작화면=False; 자신.닫힘=False

    def بھیجیں(자신, کوائف):
        if not کوائف or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.عمل_کاری.stdin.write(کوائف); 자신.عمل_کاری.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                کوائف=자신.عمل_کاری.stdout.read(4096)
                if not کوائف: break
                sys.stdout.buffer.write(کوائف); sys.stdout.buffer.flush()
                끝부분=(끝부분+کوائف)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.حکم_کی_تشریح_کرنے_والا=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.بھیجیں(b'terminal\n')
        finally: 자신.닫힘=True

    def کلائنٹ(자신, کلائنٹ, راستہ_2):
        سرور_قدر=socket.socket(socket.AF_UNIX); سرور_قدر.settimeout(10); کلائنٹ.settimeout(10)
        کی_بورڈ_اندراج=کی_بورڈ(자신.بھیجیں,lambda 한글여부:자신.بھیجیں(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            سرور_قدر.connect(str(راستہ_2))
            # 초기 협상은 순서대로 끝낸다. 이후 اخراج_کا_مقام 가닥만 클라이언트에 쓴다.
            کلائنٹ.sendall(정확한값(سرور_قدر,12))
            판번호=정확한값(کلائنٹ,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            سرور_قدر.sendall(판번호)
            개수=정확한값(سرور_قدر,1);کلائنٹ.sendall(개수+정확한값(سرور_قدر,개수[0]))
            سلامتی=정확한값(کلائنٹ,1)
            if سلامتی!=b'\x01': raise ValueError('unexpected security type')
            سرور_قدر.sendall(سلامتی)
            if 판번호==b'RFB 003.008\n':کلائنٹ.sendall(정확한값(سرور_قدر,4))
            سرور_قدر.sendall(정확한값(کلائنٹ,1))
            초기값=정확한값(سرور_قدر,24)
            کلائنٹ.sendall(초기값+정확한값(سرور_قدر,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            کلائنٹ.settimeout(None);سرور_قدر.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        زمرہ_قدر=정확한값(سرور_قدر,1)[0]
                        if زمرہ_قدر==0:
                            머리=정확한값(سرور_قدر,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 بعید_قدر 포인터의 중복을 피한다.
                            خفیہ_قدر=포인터지원
                            if خفیہ_قدر:کلائنٹ.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            کلائنٹ.sendall(bytes([زمرہ_قدر])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(سرور_قدر,12);가로,عمودی_پوزیشن_ٹھیک_کریں,폭,높이,ضابطہ_بندی_قدر=struct.unpack('>HHHHi',사각형)
                                if ضابطہ_بندی_قدر!=0:raise ValueError('unexpected framebuffer encoding: '+str(ضابطہ_بندی_قدر))
                                کلائنٹ.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    کوائف=정확한값(سرور_قدر,min(남음,65536));کلائنٹ.sendall(کوائف);남음-=len(کوائف)
                        elif زمرہ_قدر==1:
                            머리=정확한값(سرور_قدر,5);개수=struct.unpack('>H',머리[3:])[0]
                            کلائنٹ.sendall(bytes([زمرہ_قدر])+머리+정확한값(سرور_قدر,개수*6))
                        elif زمرہ_قدر==2:کلائنٹ.sendall(bytes([زمرہ_قدر]))
                        elif زمرہ_قدر==3:
                            머리=정확한값(سرور_قدر,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            کلائنٹ.sendall(bytes([زمرہ_قدر])+머리+정확한값(سرور_قدر,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(زمرہ_قدر))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:کلائنٹ.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                زمرہ_قدر=정확한값(کلائنٹ,1)[0]
                if زمرہ_قدر==4:
                    بنیادی_متن=정확한값(کلائنٹ,7); کی_بورڈ_اندراج.누름값(بنیادی_متن[0]!=0,struct.unpack('>I',بنیادی_متن[3:])[0]); continue
                if زمرہ_قدر==255:
                    بنیادی_متن=정확한값(کلائنٹ,11)
                    if بنیادی_متن[0]!=0: raise ValueError('unsupported QEMU input extension')
                    کی_بورڈ_اندراج.누름값(struct.unpack('>H',بنیادی_متن[1:3])[0]!=0,struct.unpack('>I',بنیادی_متن[3:7])[0]); continue
                if زمرہ_قدر==5:
                    بنیادی_متن=정확한값(کلائنٹ,5); 단추들,ایکس_مربوط,세로좌표=struct.unpack('>BHH',بنیادی_متن)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: کی_بورڈ_اندراج.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=ایکس_مربوط<576 and 112<=세로좌표<372:
                        لُک_اپ_اشاریہ=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and لُک_اپ_اشاریہ<5: 자신.بھیجیں(bytes([ord('1')+لُک_اپ_اشاریہ]))
                    else: 자신.بھیجیں(bytes([30,1,단추들,ایکس_مربوط&255,ایکس_مربوط>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if زمرہ_قدر==6:
                    بنیادی_متن=정확한값(کلائنٹ,7); لمبا_ئی_قدر=struct.unpack('>i',بنیادی_متن[3:])[0]
                    if abs(لمبا_ئی_قدر)>65536: raise ValueError('clipboard too large')
                    متن=정확한값(کلائنٹ,abs(لمبا_ئی_قدر))
                    if لمبا_ئی_قدر>=0:
                        try: کی_بورڈ_اندراج.تختہ_تراشہ_قدر=متن.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: کی_بورڈ_اندراج.تختہ_تراشہ_قدر=متن.decode('latin-1').encode('utf-8')
                        کی_بورڈ_اندراج.تختہ_تراشہ_قدر=کی_بورڈ_اندراج.تختہ_تراشہ_قدر[:65536].decode('utf-8','ignore').encode('utf-8')
                    سرور_قدر.sendall(bytes([زمرہ_قدر])+بنیادی_متن+متن); continue
                if زمرہ_قدر==0:
                    بنیادی_متن=정확한값(کلائنٹ,19)
                    if بنیادی_متن[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=بنیادی_متن[3]//8
                elif زمرہ_قدر==2:
                    بنیادی_متن=정확한값(کلائنٹ,3); 항목수=struct.unpack('>H',بنیادی_متن[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(کلائنٹ,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 طے_شدہ_قدر Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    بنیادی_متن=struct.pack('>BHi',0,1,0)
                elif زمرہ_قدر in (3,150): بنیادی_متن=정확한값(کلائنٹ,9)
                elif زمرہ_قدر==248:
                    بنیادی_متن=정확한값(کلائنٹ,8)
                    if بنیادی_متن[7]>64: raise ValueError('fence too large')
                    بنیادی_متن+=정확한값(کلائنٹ,بنیادی_متن[7])
                elif زمرہ_قدر==250: بنیادی_متن=정확한값(کلائنٹ,3)
                elif زمرہ_قدر==251:
                    بنیادی_متن=정확한값(کلائنٹ,7)
                    if بنیادی_متن[5]>16: raise ValueError('too many screens')
                    بنیادی_متن+=정확한값(کلائنٹ,بنیادی_متن[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(زمرہ_قدر))
                سرور_قدر.sendall(bytes([زمرہ_قدر])+بنیادی_متن)
        except (OSError,EOFError,ValueError) as غلطی:
            if str(غلطی): print('VNC client:',غلطی,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (کلائنٹ,سرور_قدر):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def چلائیں_ڈیسک_ٹاپ(دہانہ_نمبر=5902, نیٹ_ورک=False, فائل_منتقلی_دہانہ_نمبر=2121, 전달규칙들=(), جزیات_کاری_قدر=(640, 480), مہمان_پتہ=None, میزبان_پتہ='127.0.0.1'):
    with ExitStack() as وسائل, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        نیٹ_ورک_برج_اندراج = None
        if نیٹ_ورک:
            from نیٹ_ورک_برج import نیٹ_ورک_برج
            نیٹ_ورک_برج_اندراج = وسائل.enter_context(نیٹ_ورک_برج(فائل_منتقلی_دہانہ_نمبر, 전달규칙들, مہمان_پتہ=مہمان_پتہ, میزبان_پتہ=میزبان_پتہ))
        راستہ_2=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',دہانہ_نمبر)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if نیٹ_ورک_برج_اندراج and (원격화면접속번호==فائل_منتقلی_دہانہ_نمبر or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and میزبان==원격화면접속번호 for 통신규약,میزبان,_ in نیٹ_ورک_برج_اندراج.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            عمل_کاری=subprocess.Popen(حکم(جزیات_کاری_قدر)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(راستہ_2)]+(نیٹ_ورک_برج_اندراج.전달인수() if نیٹ_ورک_برج_اندراج else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            برج=جڑیں_ڈیسک_ٹاپ(عمل_کاری); ریڈر=threading.Thread(target=برج.직렬입출력,daemon=True); ریڈر.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if نیٹ_ورک_برج_اندراج: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(میزبان_پتہ,فائل_منتقلی_دہانہ_نمبر),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while عمل_کاری.poll() is None:
                    try: کلائنٹ,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): کلائنٹ.close(); continue
                    if not راستہ_2.exists(): کلائنٹ.close(); continue
                    처리작업=threading.Thread(target=برج.کلائنٹ,args=(کلائنٹ,راستہ_2),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                برج.닫힘=True
                if نیٹ_ورک_برج_اندراج: نیٹ_ورک_برج_اندراج.توقف_ایونٹ.set()
                if عمل_کاری.poll() is None:
                    عمل_کاری.terminate()
                    try: عمل_کاری.wait(timeout=5)
                    except subprocess.TimeoutExpired: عمل_کاری.kill(); عمل_کاری.wait()
                ریڈر.join(timeout=2); عمل_کاری.stdin.close(); عمل_کاری.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if نیٹ_ورک_برج_اندراج and نیٹ_ورک_برج_اندراج.غلطی: raise RuntimeError('network bridge: '+نیٹ_ورک_برج_اندراج.غلطی)
            return 0 if 가로채기됨 else عمل_کاری.returncode


if __name__=='__main__':
    from نفاذ_کریں_حکم import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    دلائل_لڑی=인수해석기.parse_args()
    if دلائل_لڑی.forward and not دلائل_لڑی.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(چلائیں_ڈیسک_ٹاپ(دلائل_لڑی.port,نیٹ_ورک=دلائل_لڑی.network,فائل_منتقلی_دہانہ_نمبر=دلائل_لڑی.ftp_port,전달규칙들=دلائل_لڑی.forward,جزیات_کاری_قدر=دلائل_لڑی.resolution))
