#!/usr/bin/env python3
"""واقعی_داده_ها QEMU/VNC에서 화면 اندازه·경계·پنجره انتقال_مقدار·Swing·언어별 그리기를 검사한다."""
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
from رایانه_نما import 정확한값
from اجرا_فرمان import نمایش_دادن_جذر


def 해상도시험(너비, 높이, سنجش_مسیر):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); شماره_درگاه = 임시.getsockname()[1]
    اندازه_کردن_متن = '{}x{}'.format(너비, 높이)
    فرآیند_مقدار = subprocess.Popen(['python3', str(نمایش_دادن_جذر/'ابزارها/اجرا_فرمان.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(شماره_درگاه), '--resolution', اندازه_کردن_متن], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    انتخاب_کننده_a916db4e = selectors.DefaultSelector(); انتخاب_کننده_a916db4e.register(فرآیند_مقدار.stdout, selectors.EVENT_READ)
    واقعه_نگار_ردیف = bytearray(); راه_دور_مقدار = None; انتقال_مقدار_630ba093 = None

    def 기다리기(نمایش_مقدار, اجرا_2=0):
        마감 = time.monotonic() + 60
        while نمایش_مقدار not in واقعه_نگار_ردیف[اجرا_2:]:
            if time.monotonic() > 마감 or فرآیند_مقدار.poll() is not None or b'HALTED' in واقعه_نگار_ردیف or b'PANIC:' in واقعه_نگار_ردیف:
                raise AssertionError(واقعه_نگار_ردیف[اجرا_2:].decode('utf-8', 'replace'))
            for رویداد, _ in انتخاب_کننده_a916db4e.select(.1):
                داده_ها = رویداد.fileobj.read(65536)
                if داده_ها: واقعه_نگار_ردیف.extend(داده_ها)
        return واقعه_نگار_ردیف[اجرا_2:].decode('utf-8', 'replace')

    def کلیک_دکمه(نماد, 눌림=True): راه_دور_مقدار.sendall(struct.pack('>BBHI', 4, int(눌림), 0, نماد))

    def ارسال_متن(متن):
        اجرا_2 = len(واقعه_نگار_ردیف)
        for نویسه_مقدار in متن:
            نماد = 0xff0d if نویسه_مقدار == '\n' else ord(نویسه_مقدار) if ord(نویسه_مقدار) < 256 else 0x1000000 | ord(نویسه_مقدار)
            کلیک_دکمه(نماد); کلیک_دکمه(نماد, False)
        return اجرا_2

    def واسط(متن): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', ارسال_متن(متن+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, عمودی_مرتب_کردن, 눌림): راه_دور_مقدار.sendall(struct.pack('>BBHH', 5, 눌림, 가로, عمودی_مرتب_کردن))

    def کلیک_مقدار(가로, عمودی_مرتب_کردن): 가리키기(가로, عمودی_مرتب_کردن, 1); 가리키기(가로, عمودی_مرتب_کردن, 0)

    def نقش_نقطه_ای_عکس():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 واقعی_داده_ها 너비를 쓴다.
        راه_دور_مقدار.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        نقاشی_مقدار = Image.new('RGB', (너비, 높이)); مقوله_مقدار = 0
        while True:
            종류 = 정확한값(راه_دور_مقدار, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                طول_مقدار = struct.unpack('>I', 정확한값(راه_دور_مقدار, 7)[3:])[0]; 정확한값(راه_دور_مقدار, طول_مقدار); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(راه_دور_مقدار, 3)[1:])[0]
            for _ in range(개수):
                가로, عمودی_مرتب_کردن, 폭, طول_مقدار, رمزگذاری_مقدار = struct.unpack('>HHHHi', 정확한값(راه_دور_مقدار, 12))
                assert رمزگذاری_مقدار == 0 and 가로+폭 <= 너비 and عمودی_مرتب_کردن+طول_مقدار <= 높이
                نقاشی_مقدار.paste(Image.frombytes('RGB', (폭, طول_مقدار), 정확한값(راه_دور_مقدار, 폭*طول_مقدار*4), 'raw', 'BGRX'), (가로, عمودی_مرتب_کردن))
                مقوله_مقدار += 폭*طول_مقدار
            if مقوله_مقدار:
                assert مقوله_مقدار == 너비*높이, مقوله_مقدار
                return نقاشی_مقدار

    def بررسی_پیکسل(مختصات_مقدار, 색):
        마감 = time.monotonic()+10
        while True:
            نقاشی_مقدار = نقش_نقطه_ای_عکس()
            if نقاشی_مقدار.getpixel(مختصات_مقدار) == 색: return نقاشی_مقدار
            if time.monotonic() > 마감: raise AssertionError((مختصات_مقدار, نقاشی_مقدار.getpixel(مختصات_مقدار), 색))

    def آپلود_فایل(نام, داده_ها): انتقال_مقدار_630ba093.storbinary('STOR '+نام, io.BytesIO(داده_ها))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+اندازه_کردن_متن+' RGB32').encode() in واقعه_نگار_ردیف
        print('BOOT:', اندازه_کردن_متن, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', واقعه_نگار_ردیف).group(1))
        راه_دور_مقدار = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(راه_دور_مقدار, 12) == b'RFB 003.008\n'; راه_دور_مقدار.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(راه_دور_مقدار, 정확한값(راه_دور_مقدار, 1)[0]); راه_دور_مقدار.sendall(b'\x01')
        assert 정확한값(راه_دور_مقدار, 4) == b'\0'*4; راه_دور_مقدار.sendall(b'\x01')
        초기 = 정확한값(راه_دور_مقدار, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(راه_دور_مقدار, struct.unpack('>I', 초기[20:])[0])
        راه_دور_مقدار.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        راه_دور_مقدار.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        بررسی_پیکسل((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        بررسی_پیکسل((너비-568, 높이-360), (32, 80, 144))
        اجرا_2 = len(واقعه_نگار_ردیف); کلیک_مقدار(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', اجرا_2)
        بررسی_پیکسل((너비-568, 높이-360), (24, 32, 48))
        اجرا_2 = len(واقعه_نگار_ردیف); کلیک_مقدار(80, 16); 기다리기(b'TERMINAL FOCUS 1', اجرا_2)
        واسط('ftpd start')
        انتقال_مقدار_630ba093 = ftplib.FTP(); انتقال_مقدار_630ba093.encoding = 'utf-8'; انتقال_مقدار_630ba093.connect('127.0.0.1', شماره_درگاه, timeout=20); انتقال_مقدار_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·کلیپ 밖·빈 사각형을 포함한다.
        مبداء = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(네모그리기(너비,높이,0,0,0)) return 2;
    if(네모그리기(너비,높이-1,1,1,0)!=-22) return 3;
    if(네모그리기(너비-1,높이,1,1,0)!=-22) return 4;
    if(네모그리기(-1,0,1,1,0)!=-22) return 5;
    if(네모그리기(0,0,-1,1,0)!=-22) return 6;
    if(네모그리기(너비-1,높이-1,1,1,0x332211)) return 7;
    نوشتن_فایل_داده_ها(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        آپلود_فایل('화면시험.c', مبداء.encode())
        assert 'exit 0' in واسط('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', ارسال_متن('run /화면시험\n'))
        بررسی_پیکسل((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', ارسال_متن('q'))
        مبداء = '''from فارسی import 화면크기, 네모그리기, 그림기다리기, خروجی, سیستم_خطا
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except سیستم_خطا as خطا:
    assert خطا.فهرست == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
خروجی("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        آپلود_فایل('화면시험.py', مبداء.encode())
        기다리기(b'PYTHON RESOLUTION PASS', ارسال_متن('python /화면시험.py\n'))
        بررسی_پیکسل((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', ارسال_متن('q'))
        مبداء = '''import فارسی.بومی.*;
public class 해상도시험 {
    public static void main(String[] نشانوندها) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new وضعیت_استثنا("اندازه");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new وضعیت_استثنا("کلیپ"); }
        catch (بی_اعتبار_آرگومان_استثنا خطا) { }
        화면.پاک_کردن_ورودی(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # استثنا 처리는 میزبان javac 결과를 بومی JVM에 올려 검사한다.
        경계원문 = سنجش_مسیر/'해상도경계시험.java'
        경계원문.write_text(مبداء.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(نمایش_دادن_جذر/'dist/jkoros-native-korean.jar'), '-d', str(سنجش_مسیر), str(경계원문)])
        آپلود_فایل('해상도경계시험.class', (سنجش_مسیر/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', ارسال_متن('java 해상도경계시험\n'))
        بررسی_پیکسل((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ارسال_متن('q'))
        # 게스트 javac의 پشتیبان_مقدار 문법으로 اندازه جستار_مقدار·پاک_کردن_ورودی·다섯 نشانوندها 그리기를 컴파일한다.
        مبداء = '''public class 해상도시험 {
    public static void main(String[] نشانوندها) {
        int 너비=فارسی.بومی.화면.너비();
        int 높이=فارسی.بومی.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        فارسی.بومی.화면.پاک_کردن_ورودی(3153944);
        فارسی.بومی.화면.사각형(너비-1,높이-1,1,1,10061943);
        فارسی.بومی.خروجی.نوشتن_خط("JAVA RESOLUTION PASS");
        فارسی.بومی.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        آپلود_فایل('해상도시험.java', مبداء.encode())
        سنجش = واسط('javac 해상도시험.java'); assert 'exit 0' in سنجش, سنجش
        기다리기(b'JAVA RESOLUTION PASS', ارسال_متن('java 해상도시험\n'))
        بررسی_پیکسل((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ارسال_متن('q'))
        آپلود_فایل('스윙시험.class', (سنجش_مسیر/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', ارسال_متن('java 스윙시험\n'))
        가로, عمودی_مرتب_کردن = (너비-400)//2, (높이-280)//2
        نقاشی_مقدار = بررسی_پیکسل((가로, عمودی_مرتب_کردن), (32, 80, 144))
        نقاشی_مقدار.save(str(سنجش_مسیر/(اندازه_کردن_متن+'.png')))
        اجرا_2 = len(واقعه_نگار_ردیف); کلیک_مقدار(가로+80, عمودی_مرتب_کردن+155)
        기다리기('SWING CLICK نام'.encode(), اجرا_2)
        اجرا_2 = len(واقعه_نگار_ردیف); کلیک_مقدار(가로+385, عمودی_مرتب_کردن+15); 기다리기(b'jkoros-native> ', اجرا_2)
        assert 'AFTER_RESOLUTION' in واسط('echo AFTER_RESOLUTION')
        print('PASS:', اندازه_کردن_متن, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if انتقال_مقدار_630ba093: انتقال_مقدار_630ba093.close()
        if راه_دور_مقدار: راه_دور_مقدار.close()
        if فرآیند_مقدار.poll() is None:
            فرآیند_مقدار.terminate()
            try: فرآیند_مقدار.wait(timeout=8)
            except subprocess.TimeoutExpired: فرآیند_مقدار.kill(); فرآیند_مقدار.wait()
        انتخاب_کننده_a916db4e.close(); فرآیند_مقدار.stdout.close()
        (سنجش_مسیر/(اندازه_کردن_متن+'.log')).write_bytes(واقعه_نگار_ردیف)


def اجرا_2():
    سنجش_مسیر = نمایش_دادن_جذر/'build/verification/resolution'; سنجش_مسیر.mkdir(parents=True, exist_ok=True)
    واقعه_نگار_ردیف = {'passed': False, 'kernel_sha256': hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for بی_اعتبار_مقدار in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            سنجش = subprocess.run(['python3', str(نمایش_دادن_جذر/'ابزارها/اجرا_فرمان.py'), '--resolution', بی_اعتبار_مقدار], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert سنجش.returncode == 2 and b'--resolution' in سنجش.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(سنجش_مسیر), str(نمایش_دادن_جذر/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, سنجش_مسیر); واقعه_نگار_ردیف['resolutions'].append([너비, 높이])
        واقعه_نگار_ردیف.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (سنجش_مسیر/'report.json').write_text(json.dumps(واقعه_نگار_ردیف, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': اجرا_2()
