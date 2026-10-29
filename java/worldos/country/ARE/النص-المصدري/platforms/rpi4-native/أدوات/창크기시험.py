#!/usr/bin/env python3
"""الفعلي_بيانات QEMU/VNC에서 طرفية 모서리 يسحب_قيمة·مؤشر·동적 حرف_قيمة فتحة_إدخال·يحرر_قيمة محتوى_قيمة 보존를 검사한다."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from PIL import Image
from سطح_مكتب_عرض import 정확한값
from ينفذ_أمر import يعرض_جذر


def 창크기시험(너비, ارتفاع_قيمة, مقياس_مسار):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); رقم_المنفذ = 임시.getsockname()[1]
    يغير_الحجم_نص = '{}x{}'.format(너비, ارتفاع_قيمة)
    عملية_قيمة = subprocess.Popen(['python3', str(يعرض_جذر/'أدوات/ينفذ_أمر.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(رقم_المنفذ), '--resolution', يغير_الحجم_نص], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    محدد_a916db4e = selectors.DefaultSelector(); محدد_a916db4e.register(عملية_قيمة.stdout, selectors.EVENT_READ)
    سجل_سجل = bytearray(); بعيد_قيمة = None; نقل_قيمة_630ba093 = None; مؤشر_مخفية=[False]

    def 기다리기(عرض_قيمة_487749b8, تشغيل=0):
        موعد_نهائي_قيمة = time.monotonic() + 60
        while عرض_قيمة_487749b8 not in سجل_سجل[تشغيل:]:
            if time.monotonic() > موعد_نهائي_قيمة or عملية_قيمة.poll() is not None or b'HALTED' in سجل_سجل or b'PANIC:' in سجل_سجل:
                raise AssertionError(سجل_سجل[تشغيل:].decode('utf-8', 'replace'))
            for حدث, _ in محدد_a916db4e.select(.1):
                بيانات = حدث.fileobj.read(65536)
                if بيانات: سجل_سجل.extend(بيانات)
        return سجل_سجل[تشغيل:].decode('utf-8', 'replace')

    def نقرة_زر(رمز, 눌림=True): بعيد_قيمة.sendall(struct.pack('>BBHI', 4, int(눌림), 0, رمز))

    def إرسال_نص(نص):
        تشغيل = len(سجل_سجل)
        for حرف_قيمة in نص:
            رمز = 0xff0d if حرف_قيمة == '\n' else ord(حرف_قيمة) if ord(حرف_قيمة) < 256 else 0x1000000 | ord(حرف_قيمة)
            نقرة_زر(رمز); نقرة_زر(رمز, False)
        return تشغيل

    def 셸(نص): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', إرسال_نص(نص+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, عمودي_منصب, 눌림): بعيد_قيمة.sendall(struct.pack('>BBHH', 5, 눌림, 가로, عمودي_منصب))

    def نقرة_قيمة(가로, عمودي_منصب): 가리키기(가로, عمودي_منصب, 1); 가리키기(가로, عمودي_منصب, 0)

    def صورة_نقطية_صورة():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 الفعلي_بيانات 너비를 쓴다.
        بعيد_قيمة.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, ارتفاع_قيمة))
        رسم_قيمة = Image.new('RGB', (너비, ارتفاع_قيمة)); فئة_قيمة_9285603e = 0
        while True:
            종류 = 정확한값(بعيد_قيمة, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', 정확한값(بعيد_قيمة, 7)[3:])[0]; 정확한값(بعيد_قيمة, 길이); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(بعيد_قيمة, 3)[1:])[0]
            for _ in range(개수):
                가로, عمودي_منصب, 폭, 길이, ترميز_قيمة = struct.unpack('>HHHHi', 정확한값(بعيد_قيمة, 12))
                if ترميز_قيمة == -239:
                    assert 폭==0 and 길이==0, 'remote cursor must be hidden'
                    مؤشر_مخفية[0]=True
                    continue
                assert ترميز_قيمة == 0 and 가로+폭 <= 너비 and عمودي_منصب+길이 <= ارتفاع_قيمة
                رسم_قيمة.paste(Image.frombytes('RGB', (폭, 길이), 정확한값(بعيد_قيمة, 폭*길이*4), 'raw', 'BGRX'), (가로, عمودي_منصب))
                فئة_قيمة_9285603e += 폭*길이
            if فئة_قيمة_9285603e:
                assert فئة_قيمة_9285603e == 너비*ارتفاع_قيمة, فئة_قيمة_9285603e
                return رسم_قيمة

    def شيك_عنصر_صورة(إحداثيات_قيمة, 색):
        موعد_نهائي_قيمة = time.monotonic()+10
        while True:
            رسم_قيمة = صورة_نقطية_صورة()
            if رسم_قيمة.getpixel(إحداثيات_قيمة) == 색: return رسم_قيمة
            if time.monotonic() > موعد_نهائي_قيمة: raise AssertionError((إحداثيات_قيمة, رسم_قيمة.getpixel(إحداثيات_قيمة), 색))

    def تحميل_الملفات(اسم, بيانات): نقل_قيمة_630ba093.storbinary('STOR '+اسم, io.BytesIO(بيانات))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+يغير_الحجم_نص+' RGB32').encode() in سجل_سجل
        print('BOOT:', يغير_الحجم_نص, flush=True)
        بعيد_رقم = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', سجل_سجل).group(1))
        بعيد_قيمة = socket.create_connection(('127.0.0.1', بعيد_رقم), timeout=20)
        assert 정확한값(بعيد_قيمة, 12) == b'RFB 003.008\n'; بعيد_قيمة.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(بعيد_قيمة, 정확한값(بعيد_قيمة, 1)[0]); بعيد_قيمة.sendall(b'\x01')
        assert 정확한값(بعيد_قيمة, 4) == b'\0'*4; بعيد_قيمة.sendall(b'\x01')
        حالة_أولية = 정확한값(بعيد_قيمة, 24); assert struct.unpack('>HH', حالة_أولية[:4]) == (너비, ارتفاع_قيمة)
        정확한값(بعيد_قيمة, struct.unpack('>I', حالة_أولية[20:])[0])
        بعيد_قيمة.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        بعيد_قيمة.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        شيك_عنصر_صورة((너비-1, ارتفاع_قيمة-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for حدث,_ in محدد_a916db4e.select(.02):
                    بيانات=حدث.fileobj.read(65536)
                    if بيانات:سجل_سجل.extend(بيانات)
        نافذة=[12,48,568,360]
        def يتحقق_يغير_الحجم():
            عمود_قيمة,صف_قيمة=(نافذة[2]-24)//8,(نافذة[3]-56)//16
            نص=셸('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(عمود_قيمة,صف_قيمة) in نص,نص
            # الفعلي_بيانات نافذة 테두리: 단지 حجم يستعلم_قيمة 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            شيك_عنصر_صورة((نافذة[0],نافذة[1]),(32,80,144))
            رسم_قيمة=شيك_عنصر_صورة((نافذة[0]+نافذة[2]-1,نافذة[1]+نافذة[3]-1),(39,49,64))
            return رسم_قيمة
        def 모서리(방향):
            return (نافذة[0]+(3 if 방향 in (1,3) else نافذة[2]-4),نافذة[1]+(3 if 방향<=2 else نافذة[3]-4))
        def يغيّر_الحجم_يسحب(방향,차이,زر=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            شيك_عنصر_صورة(흰점,(255,255,255))
            가리키기(가,세,زر)
            끝가=max(0,min(너비-1,가+차이[0]));إنهاء_مكالمة_عمودي=max(0,min(ارتفاع_قيمة-1,세+차이[1]))
            가리키기(끝가,إنهاء_مكالمة_عمودي,زر);가리키기(끝가,إنهاء_مكالمة_عمودي,0);숨고르기()
            if زر==1:
                왼,위,폭,길이=نافذة;حق_قيمة,아래=왼+폭,위+길이
                if 방향 in (1,3):왼=max(0,min(حق_قيمة-360,왼+끝가-가))
                else:حق_قيمة=max(왼+360,min(너비,حق_قيمة+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+إنهاء_مكالمة_عمودي-세))
                else:아래=max(위+216,min(ارتفاع_قيمة,아래+إنهاء_مكالمة_عمودي-세))
                نافذة[:]=[왼,위,حق_قيمة-왼,아래-위]
        يتحقق_يغير_الحجم();assert مؤشر_مخفية[0]
        يغيّر_الحجم_يسحب(4,(-100,-60),4);يتحقق_يغير_الحجم() # حق 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            يغيّر_الحجم_يسحب(방향,차이);يتحقق_يغير_الحجم()
        # إدخال_قيمة 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        إرسال_نص("echo '"+긴글+"'");숨고르기()
        يغيّر_الحجم_يسحب(4,(-1000,-1000));assert نافذة[2:]==[360,216]
        يغيّر_الحجم_يسحب(4,(너비,ارتفاع_قيمة))
        تشغيل=إرسال_نص('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),تشغيل);يتحقق_يغير_الحجم()
        # vi가 يحرر_قيمة 중에 화면 크기를 إعادة_محاولة_قيمة 읽고, 저장하지 않은 한글도 유지한다.
        셸('ftpd start')
        نقل_قيمة_630ba093=ftplib.FTP();نقل_قيمة_630ba093.encoding='utf-8';نقل_قيمة_630ba093.connect('127.0.0.1',رقم_المنفذ,timeout=20);نقل_قيمة_630ba093.login()
        기다리기(b'NORMAL',إرسال_نص('vi /크기자료.txt\n'))
        기다리기(b'INSERT',إرسال_نص('i미저장 한글 بيانات\n'));숨고르기()
        يغيّر_الحجم_يسحب(4,(-너비,-ارتفاع_قيمة))
        # ANSI صف_قيمة 이동에 새 صف_قيمة 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((نافذة[3]-56)//16)).encode() in سجل_سجل[-4096:]
        إرسال_نص('작은 창에서도 이어 كتابة\n');숨고르기()
        يغيّر_الحجم_يسحب(4,(너비,ارتفاع_قيمة))
        إرسال_نص('큰 창에서도 이어 كتابة\n');숨고르기()
        نقرة_زر(0xff1b);نقرة_زر(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',إرسال_نص(':wq\n'))
        محتوى_قيمة=bytearray();نقل_قيمة_630ba093.retrbinary('RETR 크기자료.txt',محتوى_قيمة.extend)
        assert محتوى_قيمة=='미저장 한글 بيانات\n작은 창에서도 이어 كتابة\n큰 창에서도 이어 كتابة\n'.encode(),محتوى_قيمة
        يتحقق_يغير_الحجم().save(str(مقياس_مسار/(يغير_الحجم_نص+'-large.png')))
        # 두 번째 창은 قيمة_افتراضية حجم, إعادة_محاولة_قيمة 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        تشغيل=len(سجل_سجل);نقرة_قيمة(70,16);기다리기(b'TERMINAL FOCUS 2',تشغيل)
        assert 'TERMINAL SIZE 68x19' in 셸('terminal size')
        تشغيل=len(سجل_سجل);نقرة_قيمة(180,16);기다리기(b'TERMINAL FOCUS 1',تشغيل);يتحقق_يغير_الحجم()
        يغيّر_الحجم_يسحب(4,(-너비,-ارتفاع_قيمة));يتحقق_يغير_الحجم().save(str(مقياس_مسار/(يغير_الحجم_نص+'-small.png')))
        # حجم يغيّر_قيمة عودة_قيمة X 닫기도 새로운 حق 가장자리를 사용한다.
        تشغيل=len(سجل_سجل);نقرة_قيمة(نافذة[0]+نافذة[2]-20,نافذة[1]+15);기다리기(b'TERMINAL FOCUS 2',تشغيل)
        assert 'RESIZE CLOSED' in 셸('echo RESIZE CLOSED')
        print('PASS:',يغير_الحجم_نص,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if نقل_قيمة_630ba093:نقل_قيمة_630ba093.close()
        if بعيد_قيمة:بعيد_قيمة.close()
        if عملية_قيمة.poll() is None:
            عملية_قيمة.terminate()
            try:عملية_قيمة.wait(timeout=8)
            except subprocess.TimeoutExpired:عملية_قيمة.kill();عملية_قيمة.wait()
        محدد_a916db4e.close();عملية_قيمة.stdout.close();(مقياس_مسار/(يغير_الحجم_نص+'.log')).write_bytes(سجل_سجل)


def تشغيل():
    مقياس_مسار=يعرض_جذر/'build/verification/resize';مقياس_مسار.mkdir(parents=True,exist_ok=True)
    سجل_سجل={'passed':False,'kernel_sha256':hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,ارتفاع_قيمة in ((640,480),(1920,1080)):
            창크기시험(너비,ارتفاع_قيمة,مقياس_مسار);سجل_سجل['resolutions'].append([너비,ارتفاع_قيمة])
        سجل_سجل.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(مقياس_مسار/'report.json').write_text(json.dumps(سجل_سجل,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':تشغيل()
