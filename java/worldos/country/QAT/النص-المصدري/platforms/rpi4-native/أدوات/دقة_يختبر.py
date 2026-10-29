#!/usr/bin/env python3
"""الفعلي_بيانات QEMU/VNC에서 화면 حجم·경계·نافذة نقل_قيمة·Swing·언어별 그리기를 검사한다."""
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


def دقة_يختبر(너비, ارتفاع_قيمة, مقياس_مسار):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); رقم_المنفذ = 임시.getsockname()[1]
    يغير_الحجم_نص = '{}x{}'.format(너비, ارتفاع_قيمة)
    عملية_قيمة = subprocess.Popen(['python3', str(يعرض_جذر/'أدوات/ينفذ_أمر.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(رقم_المنفذ), '--resolution', يغير_الحجم_نص], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    محدد_a916db4e = selectors.DefaultSelector(); محدد_a916db4e.register(عملية_قيمة.stdout, selectors.EVENT_READ)
    سجل_سجل = bytearray(); بعيد_قيمة = None; نقل_قيمة_630ba093 = None

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

    def 셸(نص): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', إرسال_نص(نص+'; echo __RESOLUTION_DONE__\n'))

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
        بعيد_قيمة.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        شيك_عنصر_صورة((너비-1, ارتفاع_قيمة-1), (24, 32, 48))
        # 화면 حق 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, ارتفاع_قيمة-360+12, 1); 가리키기(너비-568+28, ارتفاع_قيمة-360+12, 0)
        شيك_عنصر_صورة((너비-568, ارتفاع_قيمة-360), (32, 80, 144))
        تشغيل = len(سجل_سجل); نقرة_قيمة(너비-20, ارتفاع_قيمة-345); 기다리기(b'TERMINAL FOCUS 1', تشغيل)
        شيك_عنصر_صورة((너비-568, ارتفاع_قيمة-360), (24, 32, 48))
        تشغيل = len(سجل_سجل); نقرة_قيمة(80, 16); 기다리기(b'TERMINAL FOCUS 1', تشغيل)
        셸('ftpd start')
        نقل_قيمة_630ba093 = ftplib.FTP(); نقل_قيمة_630ba093.encoding = 'utf-8'; نقل_قيمة_630ba093.connect('127.0.0.1', رقم_المنفذ, timeout=20); نقل_قيمة_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 تحويل_قيمة·يقص 밖·빈 사각형을 포함한다.
        مصدر = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), ارتفاع_قيمة=화면높이();
    if(너비!=WIDTH || ارتفاع_قيمة!=HEIGHT) return 1;
    if(رسم_مستطيل(너비,ارتفاع_قيمة,0,0,0)) return 2;
    if(رسم_مستطيل(너비,ارتفاع_قيمة-1,1,1,0)!=-22) return 3;
    if(رسم_مستطيل(너비-1,ارتفاع_قيمة,1,1,0)!=-22) return 4;
    if(رسم_مستطيل(-1,0,1,1,0)!=-22) return 5;
    if(رسم_مستطيل(0,0,-1,1,0)!=-22) return 6;
    if(رسم_مستطيل(너비-1,ارتفاع_قيمة-1,1,1,0x332211)) return 7;
    كتابة_ملف_بيانات(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(ارتفاع_قيمة))
        تحميل_الملفات('화면시험.c', مصدر.encode())
        assert 'exit 0' in 셸('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', إرسال_نص('run /화면시험\n'))
        شيك_عنصر_صورة((너비-1, ارتفاع_قيمة-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', إرسال_نص('q'))
        مصدر = '''from العربية import 화면크기, رسم_مستطيل, 그림기다리기, مخرجات, فشل_النظام
너비, ارتفاع_قيمة = 화면크기()
assert (너비, ارتفاع_قيمة) == (WIDTH, HEIGHT)
try:
    رسم_مستطيل(너비, ارتفاع_قيمة-1, 1, 1, 0)
    raise AssertionError("boundary")
except فشل_النظام as خطأ:
    assert خطأ.فهرس == 22
رسم_مستطيل(너비-1, ارتفاع_قيمة-1, 1, 1, 0x665544)
مخرجات("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(ارتفاع_قيمة))
        تحميل_الملفات('화면시험.py', مصدر.encode())
        기다리기(b'PYTHON RESOLUTION PASS', إرسال_نص('python /화면시험.py\n'))
        شيك_عنصر_صورة((너비-1, ارتفاع_قيمة-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', إرسال_نص('q'))
        مصدر = '''import العربية.ذاتي.*;
public class دقة_يختبر {
    public static void main(String[] وسائط) {
        int 너비=화면.너비(), ارتفاع_قيمة=화면.ارتفاع_قيمة();
        if (너비!=WIDTH || ارتفاع_قيمة!=HEIGHT) throw new حالة_استثناء("حجم");
        try { 화면.مستطيل(너비,ارتفاع_قيمة-1,1,1,0); throw new حالة_استثناء("يقص"); }
        catch (غير_صالح_وسيطة_استثناء خطأ) { }
        화면.مسح_إدخال(0x302018);
        화면.مستطيل(너비-1,ارتفاع_قيمة-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(ارتفاع_قيمة))
        # استثناء 처리는 مضيف javac 결과를 ذاتي JVM에 올려 검사한다.
        경계원문 = مقياس_مسار/'해상도경계시험.java'
        경계원문.write_text(مصدر.replace('class دقة_يختبر', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(يعرض_جذر/'dist/jkoros-native-korean.jar'), '-d', str(مقياس_مسار), str(경계원문)])
        تحميل_الملفات('해상도경계시험.class', (مقياس_مسار/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', إرسال_نص('java 해상도경계시험\n'))
        شيك_عنصر_صورة((너비-1, ارتفاع_قيمة-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', إرسال_نص('q'))
        # 게스트 javac의 دعم_قيمة 문법으로 حجم يستعلم_قيمة·مسح_إدخال·다섯 وسائط 그리기를 컴파일한다.
        مصدر = '''public class دقة_يختبر {
    public static void main(String[] وسائط) {
        int 너비=العربية.ذاتي.화면.너비();
        int ارتفاع_قيمة=العربية.ذاتي.화면.ارتفاع_قيمة();
        if (너비!=WIDTH || ارتفاع_قيمة!=HEIGHT) return;
        العربية.ذاتي.화면.مسح_إدخال(3153944);
        العربية.ذاتي.화면.مستطيل(너비-1,ارتفاع_قيمة-1,1,1,10061943);
        العربية.ذاتي.مخرجات.كتابة_خط("JAVA RESOLUTION PASS");
        العربية.ذاتي.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(ارتفاع_قيمة))
        تحميل_الملفات('دقة_يختبر.java', مصدر.encode())
        نتيجة = 셸('javac دقة_يختبر.java'); assert 'exit 0' in نتيجة, نتيجة
        기다리기(b'JAVA RESOLUTION PASS', إرسال_نص('java دقة_يختبر\n'))
        شيك_عنصر_صورة((너비-1, ارتفاع_قيمة-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', إرسال_نص('q'))
        تحميل_الملفات('스윙시험.class', (مقياس_مسار/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', إرسال_نص('java 스윙시험\n'))
        가로, عمودي_منصب = (너비-400)//2, (ارتفاع_قيمة-280)//2
        رسم_قيمة = شيك_عنصر_صورة((가로, عمودي_منصب), (32, 80, 144))
        رسم_قيمة.save(str(مقياس_مسار/(يغير_الحجم_نص+'.png')))
        تشغيل = len(سجل_سجل); نقرة_قيمة(가로+80, عمودي_منصب+155)
        기다리기('SWING CLICK اسم'.encode(), تشغيل)
        تشغيل = len(سجل_سجل); نقرة_قيمة(가로+385, عمودي_منصب+15); 기다리기(b'jkoros-native> ', تشغيل)
        assert 'AFTER_RESOLUTION' in 셸('echo AFTER_RESOLUTION')
        print('PASS:', يغير_الحجم_نص, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if نقل_قيمة_630ba093: نقل_قيمة_630ba093.close()
        if بعيد_قيمة: بعيد_قيمة.close()
        if عملية_قيمة.poll() is None:
            عملية_قيمة.terminate()
            try: عملية_قيمة.wait(timeout=8)
            except subprocess.TimeoutExpired: عملية_قيمة.kill(); عملية_قيمة.wait()
        محدد_a916db4e.close(); عملية_قيمة.stdout.close()
        (مقياس_مسار/(يغير_الحجم_نص+'.log')).write_bytes(سجل_سجل)


def تشغيل():
    مقياس_مسار = يعرض_جذر/'build/verification/resolution'; مقياس_مسار.mkdir(parents=True, exist_ok=True)
    سجل_سجل = {'passed': False, 'kernel_sha256': hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for غير_صالح_قيمة in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            نتيجة = subprocess.run(['python3', str(يعرض_جذر/'أدوات/ينفذ_أمر.py'), '--resolution', غير_صالح_قيمة], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert نتيجة.returncode == 2 and b'--resolution' in نتيجة.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(مقياس_مسار), str(يعرض_جذر/'اختبارات/자바/스윙시험.java')])
        for 너비, ارتفاع_قيمة in ((1920,1080), (1280,720), (640,480)):
            دقة_يختبر(너비, ارتفاع_قيمة, مقياس_مسار); سجل_سجل['resolutions'].append([너비, ارتفاع_قيمة])
        سجل_سجل.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (مقياس_مسار/'report.json').write_text(json.dumps(سجل_سجل, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': تشغيل()
