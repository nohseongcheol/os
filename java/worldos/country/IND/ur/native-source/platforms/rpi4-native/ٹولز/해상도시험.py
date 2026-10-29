#!/usr/bin/env python3
"""اصل_کوائف QEMU/VNC에서 화면 حجم·경계·ونڈو منتقل_کریں_قدر·Swing·언어별 그리기를 검사한다."""
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
from ڈیسک_ٹاپ_منظر import 정확한값
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ


def 해상도시험(너비, 높이, پیمائش_راہ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); دہانہ_نمبر = 임시.getsockname()[1]
    سائز_دیں_متن = '{}x{}'.format(너비, 높이)
    عمل_قدر = subprocess.Popen(['python3', str(عکس_ڈالنا_روٹ/'ٹولز/نفاذ_کریں_حکم.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(دہانہ_نمبر), '--resolution', سائز_دیں_متن], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    منتخب_کنندہ_a916db4e = selectors.DefaultSelector(); منتخب_کنندہ_a916db4e.register(عمل_قدر.stdout, selectors.EVENT_READ)
    لاگ_صف = bytearray(); بعید_قدر = None; منتقلی_قدر = None

    def 기다리기(دکھانا_قدر, چلائیں=0):
        마감 = time.monotonic() + 60
        while دکھانا_قدر not in لاگ_صف[چلائیں:]:
            if time.monotonic() > 마감 or عمل_قدر.poll() is not None or b'HALTED' in لاگ_صف or b'PANIC:' in لاگ_صف:
                raise AssertionError(لاگ_صف[چلائیں:].decode('utf-8', 'replace'))
            for واقعہ, _ in منتخب_کنندہ_a916db4e.select(.1):
                کوائف = واقعہ.fileobj.read(65536)
                if کوائف: لاگ_صف.extend(کوائف)
        return لاگ_صف[چلائیں:].decode('utf-8', 'replace')

    def کلک_بٹن(علامت, 눌림=True): بعید_قدر.sendall(struct.pack('>BBHI', 4, int(눌림), 0, علامت))

    def SMS_بھیجیں(متن):
        چلائیں = len(لاگ_صف)
        for کریکٹر_قدر in متن:
            علامت = 0xff0d if کریکٹر_قدر == '\n' else ord(کریکٹر_قدر) if ord(کریکٹر_قدر) < 256 else 0x1000000 | ord(کریکٹر_قدر)
            کلک_بٹن(علامت); کلک_بٹن(علامت, False)
        return چلائیں

    def شیل(متن): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_بھیجیں(متن+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, عمودی_پوزیشن_ٹھیک_کریں, 눌림): بعید_قدر.sendall(struct.pack('>BBHH', 5, 눌림, 가로, عمودی_پوزیشن_ٹھیک_کریں))

    def کلک_قدر(가로, عمودی_پوزیشن_ٹھیک_کریں): 가리키기(가로, عمودی_پوزیشن_ٹھیک_کریں, 1); 가리키기(가로, عمودی_پوزیشن_ٹھیک_کریں, 0)

    def بِٹ_میپ_نقش():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 اصل_کوائف 너비를 쓴다.
        بعید_قدر.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ڈرائنگ_قدر = Image.new('RGB', (너비, 높이)); زمرہ_قدر_9285603e = 0
        while True:
            종류 = 정확한값(بعید_قدر, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                لمبا_ئی_قدر = struct.unpack('>I', 정확한값(بعید_قدر, 7)[3:])[0]; 정확한값(بعید_قدر, لمبا_ئی_قدر); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(بعید_قدر, 3)[1:])[0]
            for _ in range(개수):
                가로, عمودی_پوزیشن_ٹھیک_کریں, 폭, لمبا_ئی_قدر, ضابطہ_بندی_قدر = struct.unpack('>HHHHi', 정확한값(بعید_قدر, 12))
                assert ضابطہ_بندی_قدر == 0 and 가로+폭 <= 너비 and عمودی_پوزیشن_ٹھیک_کریں+لمبا_ئی_قدر <= 높이
                ڈرائنگ_قدر.paste(Image.frombytes('RGB', (폭, لمبا_ئی_قدر), 정확한값(بعید_قدر, 폭*لمبا_ئی_قدر*4), 'raw', 'BGRX'), (가로, عمودی_پوزیشن_ٹھیک_کریں))
                زمرہ_قدر_9285603e += 폭*لمبا_ئی_قدر
            if زمرہ_قدر_9285603e:
                assert زمرہ_قدر_9285603e == 너비*높이, زمرہ_قدر_9285603e
                return ڈرائنگ_قدر

    def پڑتال_کریں_پکسل(محدد_قدر, 색):
        마감 = time.monotonic()+10
        while True:
            ڈرائنگ_قدر = بِٹ_میپ_نقش()
            if ڈرائنگ_قدر.getpixel(محدد_قدر) == 색: return ڈرائنگ_قدر
            if time.monotonic() > 마감: raise AssertionError((محدد_قدر, ڈرائنگ_قدر.getpixel(محدد_قدر), 색))

    def اپ_لوڈ_کريں_فائلیں(نام, کوائف): منتقلی_قدر.storbinary('STOR '+نام, io.BytesIO(کوائف))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+سائز_دیں_متن+' RGB32').encode() in لاگ_صف
        print('BOOT:', سائز_دیں_متن, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', لاگ_صف).group(1))
        بعید_قدر = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(بعید_قدر, 12) == b'RFB 003.008\n'; بعید_قدر.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(بعید_قدر, 정확한값(بعید_قدر, 1)[0]); بعید_قدر.sendall(b'\x01')
        assert 정확한값(بعید_قدر, 4) == b'\0'*4; بعید_قدر.sendall(b'\x01')
        초기 = 정확한값(بعید_قدر, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(بعید_قدر, struct.unpack('>I', 초기[20:])[0])
        بعید_قدر.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        بعید_قدر.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        پڑتال_کریں_پکسل((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        پڑتال_کریں_پکسل((너비-568, 높이-360), (32, 80, 144))
        چلائیں = len(لاگ_صف); کلک_قدر(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', چلائیں)
        پڑتال_کریں_پکسل((너비-568, 높이-360), (24, 32, 48))
        چلائیں = len(لاگ_صف); کلک_قدر(80, 16); 기다리기(b'TERMINAL FOCUS 1', چلائیں)
        شیل('ftpd start')
        منتقلی_قدر = ftplib.FTP(); منتقلی_قدر.encoding = 'utf-8'; منتقلی_قدر.connect('127.0.0.1', دہانہ_نمبر, timeout=20); منتقلی_قدر.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·تراشہ 밖·빈 사각형을 포함한다.
        ماخذ_فائل = '''#include <화면규약.h>
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
    لکھیں_فائل_کوائف(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        اپ_لوڈ_کريں_فائلیں('화면시험.c', ماخذ_فائل.encode())
        assert 'exit 0' in شیل('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_بھیجیں('run /화면시험\n'))
        پڑتال_کریں_پکسل((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_بھیجیں('q'))
        ماخذ_فائل = '''from اردو import 화면크기, 네모그리기, 그림기다리기, اخراج_کا_مقام, نظام_نقص
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except نظام_نقص as غلطی:
    assert غلطی.اشاریہ == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
اخراج_کا_مقام("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        اپ_لوڈ_کريں_فائلیں('화면시험.py', ماخذ_فائل.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_بھیجیں('python /화면시험.py\n'))
        پڑتال_کریں_پکسل((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_بھیجیں('q'))
        ماخذ_فائل = '''import اردو.اپنا.*;
public class 해상도시험 {
    public static void main(String[] دلائل) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new حالت_استثنا("حجم");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new حالت_استثنا("تراشہ"); }
        catch (بے_جواز_دلائل_استثنا غلطی) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # استثنا 처리는 میزبان javac 결과를 اپنا JVM에 올려 검사한다.
        경계원문 = پیمائش_راہ/'해상도경계시험.java'
        경계원문.write_text(ماخذ_فائل.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(عکس_ڈالنا_روٹ/'dist/jkoros-native-korean.jar'), '-d', str(پیمائش_راہ), str(경계원문)])
        اپ_لوڈ_کريں_فائلیں('해상도경계시험.class', (پیمائش_راہ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_بھیجیں('java 해상도경계시험\n'))
        پڑتال_کریں_پکسل((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_بھیجیں('q'))
        # 게스트 javac의 معاونت_قدر 문법으로 حجم طلب_قدر·지우기·다섯 دلائل 그리기를 컴파일한다.
        ماخذ_فائل = '''public class 해상도시험 {
    public static void main(String[] دلائل) {
        int 너비=اردو.اپنا.화면.너비();
        int 높이=اردو.اپنا.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        اردو.اپنا.화면.지우기(3153944);
        اردو.اپنا.화면.사각형(너비-1,높이-1,1,1,10061943);
        اردو.اپنا.اخراج_کا_مقام.لکھیں_لائن("JAVA RESOLUTION PASS");
        اردو.اپنا.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        اپ_لوڈ_کريں_فائلیں('해상도시험.java', ماخذ_فائل.encode())
        پیمائش = شیل('javac 해상도시험.java'); assert 'exit 0' in پیمائش, پیمائش
        기다리기(b'JAVA RESOLUTION PASS', SMS_بھیجیں('java 해상도시험\n'))
        پڑتال_کریں_پکسل((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_بھیجیں('q'))
        اپ_لوڈ_کريں_فائلیں('스윙시험.class', (پیمائش_راہ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_بھیجیں('java 스윙시험\n'))
        가로, عمودی_پوزیشن_ٹھیک_کریں = (너비-400)//2, (높이-280)//2
        ڈرائنگ_قدر = پڑتال_کریں_پکسل((가로, عمودی_پوزیشن_ٹھیک_کریں), (32, 80, 144))
        ڈرائنگ_قدر.save(str(پیمائش_راہ/(سائز_دیں_متن+'.png')))
        چلائیں = len(لاگ_صف); کلک_قدر(가로+80, عمودی_پوزیشن_ٹھیک_کریں+155)
        기다리기('SWING CLICK نام'.encode(), چلائیں)
        چلائیں = len(لاگ_صف); کلک_قدر(가로+385, عمودی_پوزیشن_ٹھیک_کریں+15); 기다리기(b'jkoros-native> ', چلائیں)
        assert 'AFTER_RESOLUTION' in شیل('echo AFTER_RESOLUTION')
        print('PASS:', سائز_دیں_متن, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if منتقلی_قدر: منتقلی_قدر.close()
        if بعید_قدر: بعید_قدر.close()
        if عمل_قدر.poll() is None:
            عمل_قدر.terminate()
            try: عمل_قدر.wait(timeout=8)
            except subprocess.TimeoutExpired: عمل_قدر.kill(); عمل_قدر.wait()
        منتخب_کنندہ_a916db4e.close(); عمل_قدر.stdout.close()
        (پیمائش_راہ/(سائز_دیں_متن+'.log')).write_bytes(لاگ_صف)


def چلائیں():
    پیمائش_راہ = عکس_ڈالنا_روٹ/'build/verification/resolution'; پیمائش_راہ.mkdir(parents=True, exist_ok=True)
    لاگ_صف = {'passed': False, 'kernel_sha256': hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for بے_جواز_قدر in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            پیمائش = subprocess.run(['python3', str(عکس_ڈالنا_روٹ/'ٹولز/نفاذ_کریں_حکم.py'), '--resolution', بے_جواز_قدر], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert پیمائش.returncode == 2 and b'--resolution' in پیمائش.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(پیمائش_راہ), str(عکس_ڈالنا_روٹ/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, پیمائش_راہ); لاگ_صف['resolutions'].append([너비, 높이])
        لاگ_صف.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (پیمائش_راہ/'report.json').write_text(json.dumps(لاگ_صف, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': چلائیں()
