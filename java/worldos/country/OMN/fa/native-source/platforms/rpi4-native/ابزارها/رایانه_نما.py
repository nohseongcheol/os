#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, کلید_مقدار 입력은 بومی هسته_مقدار UART로 전달한다. localhost 전용, 단일 کنترل_مقدار 클라이언트.
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
from اجرا_فرمان import فرمان
from local_input import create


def 정확한값(소켓, اندازه):
    داده_ها = bytearray()
    while len(داده_ها) < اندازه:
        조각 = 소켓.recv(اندازه - len(داده_ها))
        if not 조각: raise EOFError()
        داده_ها.extend(조각)
    return bytes(داده_ها)


class صفحه_کلید:
    def __init__(자신, ارسال, 입력방식알림=None):
        자신.바이트전송 = ارسال; 자신.کلید_اصلاح_کننده = set(); 자신.کلیپ_بورد_مقدار = b''
        자신.한글조합기 = create(ارسال, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.جابجایی_کلید = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ارسال(자신, داده_ها):
        자신.한글조합기.조합확정()
        자신.바이트전송(داده_ها)

    def جابجایی_حالت(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, کلید_نماد):
        if کلید_نماد in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.کلید_اصلاح_کننده.add(کلید_نماد)
            else: 자신.کلید_اصلاح_کننده.discard(کلید_نماد)
            return
        if not 누르는중:
            자신.جابجایی_کلید.discard(کلید_نماد)
            return
        کلید_CTRL = bool(자신.کلید_اصلاح_کننده & {0xffe3, 0xffe4})
        کلید_SHIFT = bool(자신.کلید_اصلاح_کننده & {0xffe1, 0xffe2})
        if کلید_CTRL and کلید_SHIFT and کلید_نماد in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if کلید_نماد in (32,0xff0d):
                try:
                    مقدار=int(자신.유니코드입력,16)
                    if 32<=مقدار<=0x10ffff and not 0xd800<=مقدار<=0xdfff: 자신.ارسال(chr(مقدار).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif کلید_نماد==0xff1b: 자신.유니코드입력=None
            elif کلید_نماد==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif کلید_نماد<128 and chr(کلید_نماد) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(کلید_نماد)
            return
        if کلید_نماد in (0xff31,0xffc6) or کلید_نماد==32 and کلید_SHIFT and not کلید_CTRL:
            if کلید_نماد not in 자신.جابجایی_کلید: 자신.جابجایی_حالت()
            자신.جابجایی_کلید.add(کلید_نماد)
            return
        if کلید_نماد==0xff08 and 자신.한글여부 and not کلید_CTRL and 자신.한글조합기.앞글자지우기(): return
        if کلید_CTRL and کلید_SHIFT and کلید_نماد in (ord('t'),ord('T')):
            자신.ارسال(bytes([30,2,1,0,0,0,0])); return
        if کلید_نماد==0xffc3: 자신.ارسال(bytes([30,2,2,0,0,0,0])); return
        if کلید_نماد==0xffc9: 자신.ارسال(bytes([30,2,3,0,0,0,0])); return
        if کلید_CTRL and کلید_SHIFT and کلید_نماد in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ارسال(자신.کلیپ_بورد_مقدار); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if کلید_نماد in 특수글쇠: 자신.ارسال(특수글쇠[کلید_نماد]); return
        نویسه_رمزگذاری = کلید_نماد & 0xffffff if کلید_نماد & 0xff000000 == 0x01000000 else کلید_نماد
        if نویسه_رمزگذاری > 0x10ffff or 0xd800 <= نویسه_رمزگذاری <= 0xdfff or کلید_نماد >= 0xff00 and کلید_نماد < 0x1000000: return
        if کلید_CTRL and 0x40 <= نویسه_رمزگذاری <= 0x7f: 자신.ارسال(bytes([نویسه_رمزگذاری & 31])); return
        if نویسه_رمزگذاری < 32: return
        if 자신.한글여부 and 자신.کلید_اصلاح_کننده & {0xffea,0xfe03,0xff7e} and not کلید_CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.فید_کلید(chr(نویسه_رمزگذاری), altgr=True): return
        앞부분 = b'\x1b' if 자신.کلید_اصلاح_کننده & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not کلید_CTRL and not 앞부분 and 32<=نویسه_رمزگذاری<127:
            نویسه_داده_ها=chr(نویسه_رمزگذاری).upper() if کلید_SHIFT else chr(نویسه_رمزگذاری)
            if 자신.한글조합기.فید_کلید(نویسه_داده_ها): return
        자신.ارسال(앞부분 + chr(نویسه_رمزگذاری).encode('utf-8'))


class اتصال_رایانه:
    def __init__(자신, فرآیند):
        자신.فرآیند=فرآیند; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.پایانه=False; 자신.시작화면=False; 자신.닫힘=False

    def ارسال(자신, داده_ها):
        if not داده_ها or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.فرآیند.stdin.write(داده_ها); 자신.فرآیند.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                داده_ها=자신.فرآیند.stdout.read(4096)
                if not داده_ها: break
                sys.stdout.buffer.write(داده_ها); sys.stdout.buffer.flush()
                끝부분=(끝부분+داده_ها)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.پایانه=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ارسال(b'terminal\n')
        finally: 자신.닫힘=True

    def سرویس_گیرنده(자신, سرویس_گیرنده, مسیر):
        سرور_مقدار=socket.socket(socket.AF_UNIX); سرور_مقدار.settimeout(10); سرویس_گیرنده.settimeout(10)
        صفحه_کلید_ورودی=صفحه_کلید(자신.ارسال,lambda 한글여부:자신.ارسال(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            سرور_مقدار.connect(str(مسیر))
            # 초기 협상은 순서대로 끝낸다. 이후 خروجی 가닥만 클라이언트에 쓴다.
            سرویس_گیرنده.sendall(정확한값(سرور_مقدار,12))
            판번호=정확한값(سرویس_گیرنده,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            سرور_مقدار.sendall(판번호)
            개수=정확한값(سرور_مقدار,1);سرویس_گیرنده.sendall(개수+정확한값(سرور_مقدار,개수[0]))
            امنیت=정확한값(سرویس_گیرنده,1)
            if امنیت!=b'\x01': raise ValueError('unexpected security type')
            سرور_مقدار.sendall(امنیت)
            if 판번호==b'RFB 003.008\n':سرویس_گیرنده.sendall(정확한값(سرور_مقدار,4))
            سرور_مقدار.sendall(정확한값(سرویس_گیرنده,1))
            초기값=정확한값(سرور_مقدار,24)
            سرویس_گیرنده.sendall(초기값+정확한값(سرور_مقدار,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            سرویس_گیرنده.settimeout(None);سرور_مقدار.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        دسته_مقدار=정확한값(سرور_مقدار,1)[0]
                        if دسته_مقدار==0:
                            머리=정확한값(سرور_مقدار,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 راه_دور_مقدار 포인터의 중복을 피한다.
                            پنهان_مقدار=포인터지원
                            if پنهان_مقدار:سرویس_گیرنده.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            سرویس_گیرنده.sendall(bytes([دسته_مقدار])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(سرور_مقدار,12);가로,عمودی_مرتب_کردن,폭,높이,رمزگذاری_مقدار=struct.unpack('>HHHHi',사각형)
                                if رمزگذاری_مقدار!=0:raise ValueError('unexpected framebuffer encoding: '+str(رمزگذاری_مقدار))
                                سرویس_گیرنده.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    داده_ها=정확한값(سرور_مقدار,min(남음,65536));سرویس_گیرنده.sendall(داده_ها);남음-=len(داده_ها)
                        elif دسته_مقدار==1:
                            머리=정확한값(سرور_مقدار,5);개수=struct.unpack('>H',머리[3:])[0]
                            سرویس_گیرنده.sendall(bytes([دسته_مقدار])+머리+정확한값(سرور_مقدار,개수*6))
                        elif دسته_مقدار==2:سرویس_گیرنده.sendall(bytes([دسته_مقدار]))
                        elif دسته_مقدار==3:
                            머리=정확한값(سرور_مقدار,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            سرویس_گیرنده.sendall(bytes([دسته_مقدار])+머리+정확한값(سرور_مقدار,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(دسته_مقدار))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:سرویس_گیرنده.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                دسته_مقدار=정확한값(سرویس_گیرنده,1)[0]
                if دسته_مقدار==4:
                    متن_اصلی=정확한값(سرویس_گیرنده,7); صفحه_کلید_ورودی.누름값(متن_اصلی[0]!=0,struct.unpack('>I',متن_اصلی[3:])[0]); continue
                if دسته_مقدار==255:
                    متن_اصلی=정확한값(سرویس_گیرنده,11)
                    if متن_اصلی[0]!=0: raise ValueError('unsupported QEMU input extension')
                    صفحه_کلید_ورودی.누름값(struct.unpack('>H',متن_اصلی[1:3])[0]!=0,struct.unpack('>I',متن_اصلی[3:7])[0]); continue
                if دسته_مقدار==5:
                    متن_اصلی=정확한값(سرویس_گیرنده,5); 단추들,مختصات_x,دکمه_Y_مختصات=struct.unpack('>BHH',متن_اصلی)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: صفحه_کلید_ورودی.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=مختصات_x<576 and 112<=دکمه_Y_مختصات<372:
                        جستجو_فهرست=(دکمه_Y_مختصات-112)//52
                        if (دکمه_Y_مختصات-112)%52<40 and جستجو_فهرست<5: 자신.ارسال(bytes([ord('1')+جستجو_فهرست]))
                    else: 자신.ارسال(bytes([30,1,단추들,مختصات_x&255,مختصات_x>>8,دکمه_Y_مختصات&255,دکمه_Y_مختصات>>8]))
                    continue
                if دسته_مقدار==6:
                    متن_اصلی=정확한값(سرویس_گیرنده,7); طول_مقدار=struct.unpack('>i',متن_اصلی[3:])[0]
                    if abs(طول_مقدار)>65536: raise ValueError('clipboard too large')
                    متن=정확한값(سرویس_گیرنده,abs(طول_مقدار))
                    if طول_مقدار>=0:
                        try: صفحه_کلید_ورودی.کلیپ_بورد_مقدار=متن.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: صفحه_کلید_ورودی.کلیپ_بورد_مقدار=متن.decode('latin-1').encode('utf-8')
                        صفحه_کلید_ورودی.کلیپ_بورد_مقدار=صفحه_کلید_ورودی.کلیپ_بورد_مقدار[:65536].decode('utf-8','ignore').encode('utf-8')
                    سرور_مقدار.sendall(bytes([دسته_مقدار])+متن_اصلی+متن); continue
                if دسته_مقدار==0:
                    متن_اصلی=정확한값(سرویس_گیرنده,19)
                    if متن_اصلی[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=متن_اصلی[3]//8
                elif دسته_مقدار==2:
                    متن_اصلی=정확한값(سرویس_گیرنده,3); 항목수=struct.unpack('>H',متن_اصلی[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(سرویس_گیرنده,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 مقدار_پیش_فرض Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    متن_اصلی=struct.pack('>BHi',0,1,0)
                elif دسته_مقدار in (3,150): متن_اصلی=정확한값(سرویس_گیرنده,9)
                elif دسته_مقدار==248:
                    متن_اصلی=정확한값(سرویس_گیرنده,8)
                    if متن_اصلی[7]>64: raise ValueError('fence too large')
                    متن_اصلی+=정확한값(سرویس_گیرنده,متن_اصلی[7])
                elif دسته_مقدار==250: متن_اصلی=정확한값(سرویس_گیرنده,3)
                elif دسته_مقدار==251:
                    متن_اصلی=정확한값(سرویس_گیرنده,7)
                    if متن_اصلی[5]>16: raise ValueError('too many screens')
                    متن_اصلی+=정확한값(سرویس_گیرنده,متن_اصلی[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(دسته_مقدار))
                سرور_مقدار.sendall(bytes([دسته_مقدار])+متن_اصلی)
        except (OSError,EOFError,ValueError) as خطا:
            if str(خطا): print('VNC client:',خطا,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (سرویس_گیرنده,سرور_مقدار):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def اجرا_رایانه(شماره_درگاه=5902, شبکه=False, فایل_انتقال_شماره_درگاه=2121, 전달규칙들=(), دقت_مقدار=(640, 480), مهمان_آدرس=None, میزبان_آدرس='127.0.0.1'):
    with ExitStack() as منابع, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        شبکه_پل_ورودی = None
        if شبکه:
            from شبکه_پل import شبکه_پل
            شبکه_پل_ورودی = منابع.enter_context(شبکه_پل(فایل_انتقال_شماره_درگاه, 전달규칙들, مهمان_آدرس=مهمان_آدرس, میزبان_آدرس=میزبان_آدرس))
        مسیر=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',شماره_درگاه)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if شبکه_پل_ورودی and (원격화면접속번호==فایل_انتقال_شماره_درگاه or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and میزبان==원격화면접속번호 for 통신규약,میزبان,_ in شبکه_پل_ورودی.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            فرآیند=subprocess.Popen(فرمان(دقت_مقدار)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(مسیر)]+(شبکه_پل_ورودی.전달인수() if شبکه_پل_ورودی else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            پل=اتصال_رایانه(فرآیند); خواننده=threading.Thread(target=پل.직렬입출력,daemon=True); خواننده.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if شبکه_پل_ورودی: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(میزبان_آدرس,فایل_انتقال_شماره_درگاه),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while فرآیند.poll() is None:
                    try: سرویس_گیرنده,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): سرویس_گیرنده.close(); continue
                    if not مسیر.exists(): سرویس_گیرنده.close(); continue
                    처리작업=threading.Thread(target=پل.سرویس_گیرنده,args=(سرویس_گیرنده,مسیر),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                پل.닫힘=True
                if شبکه_پل_ورودی: شبکه_پل_ورودی.مکث_کردن_رویداد.set()
                if فرآیند.poll() is None:
                    فرآیند.terminate()
                    try: فرآیند.wait(timeout=5)
                    except subprocess.TimeoutExpired: فرآیند.kill(); فرآیند.wait()
                خواننده.join(timeout=2); فرآیند.stdin.close(); فرآیند.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if شبکه_پل_ورودی and شبکه_پل_ورودی.خطا: raise RuntimeError('network bridge: '+شبکه_پل_ورودی.خطا)
            return 0 if 가로채기됨 else فرآیند.returncode


if __name__=='__main__':
    from اجرا_فرمان import 해상도읽기
    مفسر=argparse.ArgumentParser(description=__doc__); مفسر.add_argument('--port',type=int,default=5902)
    مفسر.add_argument('--resolution',type=해상도읽기,default=(640,480))
    مفسر.add_argument('--network',action='store_true'); مفسر.add_argument('--ftp-port',type=int,default=2121)
    مفسر.add_argument('--forward',action='append',default=[])
    آرگومان_آرايه=مفسر.parse_args()
    if آرگومان_آرايه.forward and not آرگومان_آرايه.network: مفسر.error('--forward requires --network')
    raise SystemExit(اجرا_رایانه(آرگومان_آرايه.port,شبکه=آرگومان_آرايه.network,فایل_انتقال_شماره_درگاه=آرگومان_آرايه.ftp_port,전달규칙들=آرگومان_آرايه.forward,دقت_مقدار=آرگومان_آرايه.resolution))
