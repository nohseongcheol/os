#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, مفتاح_قيمة 입력은 ذاتي نواة_قيمة UART로 전달한다. localhost 전용, 단일 تحكم_قيمة 클라이언트.
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
from ينفذ_أمر import أمر
from local_input import create


def 정확한값(مأخذ_التوصيل_قيمة, حجم):
    بيانات = bytearray()
    while len(بيانات) < حجم:
        조각 = مأخذ_التوصيل_قيمة.recv(حجم - len(بيانات))
        if not 조각: raise EOFError()
        بيانات.extend(조각)
    return bytes(بيانات)


class لوحة_المفاتيح:
    def __init__(자신, يرسل, 입력방식알림=None):
        자신.바이트전송 = يرسل; 자신.مفتاح_التعديل = set(); 자신.حافظة_قيمة = b''
        자신.한글조합기 = create(يرسل, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.تبديل_مفتاح = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def يرسل(자신, بيانات):
        자신.한글조합기.تثبيت_تركيب()
        자신.바이트전송(بيانات)

    def تبديل_الوضع(자신):
        자신.한글조합기.تثبيت_تركيب(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, مفتاح_رمز):
        if مفتاح_رمز in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.مفتاح_التعديل.add(مفتاح_رمز)
            else: 자신.مفتاح_التعديل.discard(مفتاح_رمز)
            return
        if not 누르는중:
            자신.تبديل_مفتاح.discard(مفتاح_رمز)
            return
        مفتاح_CTRL = bool(자신.مفتاح_التعديل & {0xffe3, 0xffe4})
        مفتاح_SHIFT = bool(자신.مفتاح_التعديل & {0xffe1, 0xffe2})
        if مفتاح_CTRL and مفتاح_SHIFT and مفتاح_رمز in (ord('u'),ord('U')):
            자신.한글조합기.تثبيت_تركيب(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if مفتاح_رمز in (32,0xff0d):
                try:
                    قيمة=int(자신.유니코드입력,16)
                    if 32<=قيمة<=0x10ffff and not 0xd800<=قيمة<=0xdfff: 자신.يرسل(chr(قيمة).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif مفتاح_رمز==0xff1b: 자신.유니코드입력=None
            elif مفتاح_رمز==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif مفتاح_رمز<128 and chr(مفتاح_رمز) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(مفتاح_رمز)
            return
        if مفتاح_رمز in (0xff31,0xffc6) or مفتاح_رمز==32 and مفتاح_SHIFT and not مفتاح_CTRL:
            if مفتاح_رمز not in 자신.تبديل_مفتاح: 자신.تبديل_الوضع()
            자신.تبديل_مفتاح.add(مفتاح_رمز)
            return
        if مفتاح_رمز==0xff08 and 자신.한글여부 and not مفتاح_CTRL and 자신.한글조합기.앞글자지우기(): return
        if مفتاح_CTRL and مفتاح_SHIFT and مفتاح_رمز in (ord('t'),ord('T')):
            자신.يرسل(bytes([30,2,1,0,0,0,0])); return
        if مفتاح_رمز==0xffc3: 자신.يرسل(bytes([30,2,2,0,0,0,0])); return
        if مفتاح_رمز==0xffc9: 자신.يرسل(bytes([30,2,3,0,0,0,0])); return
        if مفتاح_CTRL and مفتاح_SHIFT and مفتاح_رمز in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.يرسل(자신.حافظة_قيمة); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if مفتاح_رمز in 특수글쇠: 자신.يرسل(특수글쇠[مفتاح_رمز]); return
        حرف_ترميز = مفتاح_رمز & 0xffffff if مفتاح_رمز & 0xff000000 == 0x01000000 else مفتاح_رمز
        if حرف_ترميز > 0x10ffff or 0xd800 <= حرف_ترميز <= 0xdfff or مفتاح_رمز >= 0xff00 and مفتاح_رمز < 0x1000000: return
        if مفتاح_CTRL and 0x40 <= حرف_ترميز <= 0x7f: 자신.يرسل(bytes([حرف_ترميز & 31])); return
        if حرف_ترميز < 32: return
        if 자신.한글여부 and 자신.مفتاح_التعديل & {0xffea,0xfe03,0xff7e} and not مفتاح_CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.موجز_مفتاح(chr(حرف_ترميز), altgr=True): return
        앞부분 = b'\x1b' if 자신.مفتاح_التعديل & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not مفتاح_CTRL and not 앞부분 and 32<=حرف_ترميز<127:
            بيانات_الأحرف=chr(حرف_ترميز).upper() if مفتاح_SHIFT else chr(حرف_ترميز)
            if 자신.한글조합기.موجز_مفتاح(بيانات_الأحرف): return
        자신.يرسل(앞부분 + chr(حرف_ترميز).encode('utf-8'))


class يتصل_سطح_مكتب:
    def __init__(자신, عملية):
        자신.عملية=عملية; 자신.قفل_قيمة=threading.Lock(); 자신.준비완료=False; 자신.طرفية=False; 자신.시작화면=False; 자신.أنظمة_المعلومات_مغلق=False

    def يرسل(자신, بيانات):
        if not بيانات or 자신.أنظمة_المعلومات_مغلق: return
        with 자신.قفل_قيمة:
            try: 자신.عملية.stdin.write(بيانات); 자신.عملية.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                بيانات=자신.عملية.stdout.read(4096)
                if not بيانات: break
                sys.stdout.buffer.write(بيانات); sys.stdout.buffer.flush()
                끝부분=(끝부분+بيانات)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); أنظمة_المعلومات_مغلق=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,أنظمة_المعلومات_مغلق,그림화면,종료됨)>=0:
                    자신.طرفية=열림>max(أنظمة_المعلومات_مغلق,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,أنظمة_المعلومات_مغلق,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.يرسل(b'terminal\n')
        finally: 자신.أنظمة_المعلومات_مغلق=True

    def عميل(자신, عميل, مسار):
        خادم_قيمة=socket.socket(socket.AF_UNIX); خادم_قيمة.settimeout(10); عميل.settimeout(10)
        لوحة_المفاتيح_إدخال=لوحة_المفاتيح(자신.يرسل,lambda 한글여부:자신.يرسل(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            خادم_قيمة.connect(str(مسار))
            # حالة_أولية 협상은 순서대로 끝낸다. 이후 مخرجات 가닥만 클라이언트에 쓴다.
            عميل.sendall(정확한값(خادم_قيمة,12))
            رقم_الإصدار=정확한값(عميل,12)
            if رقم_الإصدار not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            خادم_قيمة.sendall(رقم_الإصدار)
            개수=정확한값(خادم_قيمة,1);عميل.sendall(개수+정확한값(خادم_قيمة,개수[0]))
            أمان=정확한값(عميل,1)
            if أمان!=b'\x01': raise ValueError('unexpected security type')
            خادم_قيمة.sendall(أمان)
            if رقم_الإصدار==b'RFB 003.008\n':عميل.sendall(정확한값(خادم_قيمة,4))
            خادم_قيمة.sendall(정확한값(عميل,1))
            초기값=정확한값(خادم_قيمة,24)
            عميل.sendall(초기값+정확한값(خادم_قيمة,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            عميل.settimeout(None);خادم_قيمة.settimeout(None)
            def الناتج():
                try:
                    while True:
                        فئة_قيمة=정확한값(خادم_قيمة,1)[0]
                        if فئة_قيمة==0:
                            رأس_قيمة=정확한값(خادم_قيمة,3);항목수=struct.unpack('>H',رأس_قيمة[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 بعيد_قيمة 포인터의 중복을 피한다.
                            مخفية_قيمة=포인터지원
                            if مخفية_قيمة:عميل.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            عميل.sendall(bytes([فئة_قيمة])+رأس_قيمة)
                            for _ in range(항목수):
                                مستطيل=정확한값(خادم_قيمة,12);가로,عمودي_منصب,폭,ارتفاع_قيمة,ترميز_قيمة=struct.unpack('>HHHHi',مستطيل)
                                if ترميز_قيمة!=0:raise ValueError('unexpected framebuffer encoding: '+str(ترميز_قيمة))
                                عميل.sendall(مستطيل)
                                남음=폭*ارتفاع_قيمة*화소바이트
                                while 남음:
                                    بيانات=정확한값(خادم_قيمة,min(남음,65536));عميل.sendall(بيانات);남음-=len(بيانات)
                        elif فئة_قيمة==1:
                            رأس_قيمة=정확한값(خادم_قيمة,5);개수=struct.unpack('>H',رأس_قيمة[3:])[0]
                            عميل.sendall(bytes([فئة_قيمة])+رأس_قيمة+정확한값(خادم_قيمة,개수*6))
                        elif فئة_قيمة==2:عميل.sendall(bytes([فئة_قيمة]))
                        elif فئة_قيمة==3:
                            رأس_قيمة=정확한값(خادم_قيمة,7);개수=struct.unpack('>I',رأس_قيمة[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            عميل.sendall(bytes([فئة_قيمة])+رأس_قيمة+정확한값(خادم_قيمة,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(فئة_قيمة))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:عميل.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            خيطالعمل=threading.Thread(target=الناتج,daemon=True);خيطالعمل.start()
            while not 자신.أنظمة_المعلومات_مغلق:
                فئة_قيمة=정확한값(عميل,1)[0]
                if فئة_قيمة==4:
                    نص_أساسي=정확한값(عميل,7); لوحة_المفاتيح_إدخال.누름값(نص_أساسي[0]!=0,struct.unpack('>I',نص_أساسي[3:])[0]); continue
                if فئة_قيمة==255:
                    نص_أساسي=정확한값(عميل,11)
                    if نص_أساسي[0]!=0: raise ValueError('unsupported QEMU input extension')
                    لوحة_المفاتيح_إدخال.누름값(struct.unpack('>H',نص_أساسي[1:3])[0]!=0,struct.unpack('>I',نص_أساسي[3:7])[0]); continue
                if فئة_قيمة==5:
                    نص_أساسي=정확한값(عميل,5); 단추들,الإحداثي_س,الزر_Y_إحداثيات=struct.unpack('>BHH',نص_أساسي)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: لوحة_المفاتيح_إدخال.한글조합기.تثبيت_تركيب()
                    if 눌림&1 and 자신.시작화면 and 64<=الإحداثي_س<576 and 112<=الزر_Y_إحداثيات<372:
                        البحث_فهرس=(الزر_Y_إحداثيات-112)//52
                        if (الزر_Y_إحداثيات-112)%52<40 and البحث_فهرس<5: 자신.يرسل(bytes([ord('1')+البحث_فهرس]))
                    else: 자신.يرسل(bytes([30,1,단추들,الإحداثي_س&255,الإحداثي_س>>8,الزر_Y_إحداثيات&255,الزر_Y_إحداثيات>>8]))
                    continue
                if فئة_قيمة==6:
                    نص_أساسي=정확한값(عميل,7); 길이=struct.unpack('>i',نص_أساسي[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    نص=정확한값(عميل,abs(길이))
                    if 길이>=0:
                        try: لوحة_المفاتيح_إدخال.حافظة_قيمة=نص.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: لوحة_المفاتيح_إدخال.حافظة_قيمة=نص.decode('latin-1').encode('utf-8')
                        لوحة_المفاتيح_إدخال.حافظة_قيمة=لوحة_المفاتيح_إدخال.حافظة_قيمة[:65536].decode('utf-8','ignore').encode('utf-8')
                    خادم_قيمة.sendall(bytes([فئة_قيمة])+نص_أساسي+نص); continue
                if فئة_قيمة==0:
                    نص_أساسي=정확한값(عميل,19)
                    if نص_أساسي[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=نص_أساسي[3]//8
                elif فئة_قيمة==2:
                    نص_أساسي=정확한값(عميل,3); 항목수=struct.unpack('>H',نص_أساسي[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(عميل,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 قيمة_افتراضية Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    نص_أساسي=struct.pack('>BHi',0,1,0)
                elif فئة_قيمة in (3,150): نص_أساسي=정확한값(عميل,9)
                elif فئة_قيمة==248:
                    نص_أساسي=정확한값(عميل,8)
                    if نص_أساسي[7]>64: raise ValueError('fence too large')
                    نص_أساسي+=정확한값(عميل,نص_أساسي[7])
                elif فئة_قيمة==250: نص_أساسي=정확한값(عميل,3)
                elif فئة_قيمة==251:
                    نص_أساسي=정확한값(عميل,7)
                    if نص_أساسي[5]>16: raise ValueError('too many screens')
                    نص_أساسي+=정확한값(عميل,نص_أساسي[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(فئة_قيمة))
                خادم_قيمة.sendall(bytes([فئة_قيمة])+نص_أساسي)
        except (OSError,EOFError,ValueError) as خطأ:
            if str(خطأ): print('VNC client:',خطأ,file=sys.stderr,flush=True)
        finally:
            for مأخذ_التوصيل_قيمة in (عميل,خادم_قيمة):
                try: مأخذ_التوصيل_قيمة.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                مأخذ_التوصيل_قيمة.close()


def يشغّل_سطح_مكتب(رقم_المنفذ=5902, شبكة=False, نقل_الملفات_رقم_المنفذ=2121, 전달규칙들=(), دقة_قيمة=(640, 480), ضيف_عنوان=None, مضيف_عنوان='127.0.0.1'):
    with ExitStack() as المصادر, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        جسر_إدخال = None
        if شبكة:
            from جسر_3de4fe3a import جسر_3de4fe3a
            جسر_إدخال = المصادر.enter_context(جسر_3de4fe3a(نقل_الملفات_رقم_المنفذ, 전달규칙들, ضيف_عنوان=ضيف_عنوان, مضيف_عنوان=مضيف_عنوان))
        مسار=Path(작업경로)/'display.sock'
        with socket.socket() as يستلم_منفذ:
            يستلم_منفذ.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            يستلم_منفذ.bind(('127.0.0.1',رقم_المنفذ)); يستلم_منفذ.listen(1); يستلم_منفذ.settimeout(.2)
            원격화면접속번호=يستلم_منفذ.getsockname()[1]
            if جسر_إدخال and (원격화면접속번호==نقل_الملفات_رقم_المنفذ or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and مضيف==원격화면접속번호 for 통신규약,مضيف,_ in جسر_إدخال.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            عملية=subprocess.Popen(أمر(دقة_قيمة)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(مسار)]+(جسر_إدخال.전달인수() if جسر_إدخال else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            جسر=يتصل_سطح_مكتب(عملية); قارئ=threading.Thread(target=جسر.직렬입출력,daemon=True); قارئ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(يستلم_منفذ.getsockname()[1]),flush=True)
            if جسر_إدخال: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(مضيف_عنوان,نقل_الملفات_رقم_المنفذ),flush=True)
            def ينهي(إشارة_رقم,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,ينهي)
            معالجة_مهمة=None; 가로채기됨=False
            try:
                while عملية.poll() is None:
                    try: عميل,_=يستلم_منفذ.accept()
                    except socket.timeout: continue
                    if معالجة_مهمة is not None and معالجة_مهمة.is_alive(): عميل.close(); continue
                    if not مسار.exists(): عميل.close(); continue
                    معالجة_مهمة=threading.Thread(target=جسر.عميل,args=(عميل,مسار),daemon=True); معالجة_مهمة.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                جسر.أنظمة_المعلومات_مغلق=True
                if جسر_إدخال: جسر_إدخال.إيقاف_مؤقت_حدث.set()
                if عملية.poll() is None:
                    عملية.terminate()
                    try: عملية.wait(timeout=5)
                    except subprocess.TimeoutExpired: عملية.kill(); عملية.wait()
                قارئ.join(timeout=2); عملية.stdin.close(); عملية.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if جسر_إدخال and جسر_إدخال.خطأ: raise RuntimeError('network bridge: '+جسر_إدخال.خطأ)
            return 0 if 가로채기됨 else عملية.returncode


if __name__=='__main__':
    from ينفذ_أمر import يقرأ_دقة
    المحلل=argparse.ArgumentParser(description=__doc__); المحلل.add_argument('--port',type=int,default=5902)
    المحلل.add_argument('--resolution',type=يقرأ_دقة,default=(640,480))
    المحلل.add_argument('--network',action='store_true'); المحلل.add_argument('--ftp-port',type=int,default=2121)
    المحلل.add_argument('--forward',action='append',default=[])
    وسيطة_صفيف=المحلل.parse_args()
    if وسيطة_صفيف.forward and not وسيطة_صفيف.network: المحلل.error('--forward requires --network')
    raise SystemExit(يشغّل_سطح_مكتب(وسيطة_صفيف.port,شبكة=وسيطة_صفيف.network,نقل_الملفات_رقم_المنفذ=وسيطة_صفيف.ftp_port,전달규칙들=وسيطة_صفيف.forward,دقة_قيمة=وسيطة_صفيف.resolution))
