#!/usr/bin/env python3
"""اصلی_کوائف QEMU/VNC에서 화면 سائز·경계·کھڑکی بڑھاؤ_قدر·Swing·언어별 그리기를 검사한다."""
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
from نفاذ_کرو_حکم import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    سائز_متن = '{}x{}'.format(너비, 높이)
    عمل_قدر = subprocess.Popen(['python3', str(기준/'اوزار/نفاذ_کرو_حکم.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', سائز_متن], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    منتخب_کرنڑ_آلا_a916db4e = selectors.DefaultSelector(); منتخب_کرنڑ_آلا_a916db4e.register(عمل_قدر.stdout, selectors.EVENT_READ)
    لاگ_صف = bytearray(); بعيد_قدر = None; منتقلی_قدر = None

    def 기다리기(نمایش_کرو_قدر, چلاؤ=0):
        마감 = time.monotonic() + 60
        while نمایش_کرو_قدر not in لاگ_صف[چلاؤ:]:
            if time.monotonic() > 마감 or عمل_قدر.poll() is not None or b'HALTED' in لاگ_صف or b'PANIC:' in لاگ_صف:
                raise AssertionError(لاگ_صف[چلاؤ:].decode('utf-8', 'replace'))
            for واقعہ, _ in منتخب_کرنڑ_آلا_a916db4e.select(.1):
                کوائف = واقعہ.fileobj.read(65536)
                if کوائف: لاگ_صف.extend(کوائف)
        return لاگ_صف[چلاؤ:].decode('utf-8', 'replace')

    def کلک_کرو_بٹن(علامت, 눌림=True): بعيد_قدر.sendall(struct.pack('>BBHI', 4, int(눌림), 0, علامت))

    def متن_پیجو(متن):
        چلاؤ = len(لاگ_صف)
        for کریکٹر_قدر in متن:
            علامت = 0xff0d if کریکٹر_قدر == '\n' else ord(کریکٹر_قدر) if ord(کریکٹر_قدر) < 256 else 0x1000000 | ord(کریکٹر_قدر)
            کلک_کرو_بٹن(علامت); کلک_کرو_بٹن(علامت, False)
        return چلاؤ

    def شیل(متن): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', متن_پیجو(متن+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): بعيد_قدر.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def کلک_کرو_قدر(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def بِٹ_میپ_نقش():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 اصلی_کوائف 너비를 쓴다.
        بعيد_قدر.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ڈرائنگ_قدر = Image.new('RGB', (너비, 높이)); قِسم_قدر = 0
        while True:
            종류 = 정확한값(بعيد_قدر, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                لمبائی_قدر = struct.unpack('>I', 정확한값(بعيد_قدر, 7)[3:])[0]; 정확한값(بعيد_قدر, لمبائی_قدر); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(بعيد_قدر, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, لمبائی_قدر, ضابطہ_ربائی_قدر = struct.unpack('>HHHHi', 정확한값(بعيد_قدر, 12))
                assert ضابطہ_ربائی_قدر == 0 and 가로+폭 <= 너비 and 세로+لمبائی_قدر <= 높이
                ڈرائنگ_قدر.paste(Image.frombytes('RGB', (폭, لمبائی_قدر), 정확한값(بعيد_قدر, 폭*لمبائی_قدر*4), 'raw', 'BGRX'), (가로, 세로))
                قِسم_قدر += 폭*لمبائی_قدر
            if قِسم_قدر:
                assert قِسم_قدر == 너비*높이, قِسم_قدر
                return ڈرائنگ_قدر

    def پڑتال_دانہ(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            ڈرائنگ_قدر = بِٹ_میپ_نقش()
            if ڈرائنگ_قدر.getpixel(좌표) == 색: return ڈرائنگ_قدر
            if time.monotonic() > 마감: raise AssertionError((좌표, ڈرائنگ_قدر.getpixel(좌표), 색))

    def اپ_لوڈ_کرو_فائلاں(ناں, کوائف): منتقلی_قدر.storbinary('STOR '+ناں, io.BytesIO(کوائف))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+سائز_متن+' RGB32').encode() in لاگ_صف
        print('BOOT:', سائز_متن, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', لاگ_صف).group(1))
        بعيد_قدر = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(بعيد_قدر, 12) == b'RFB 003.008\n'; بعيد_قدر.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(بعيد_قدر, 정확한값(بعيد_قدر, 1)[0]); بعيد_قدر.sendall(b'\x01')
        assert 정확한값(بعيد_قدر, 4) == b'\0'*4; بعيد_قدر.sendall(b'\x01')
        초기 = 정확한값(بعيد_قدر, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(بعيد_قدر, struct.unpack('>I', 초기[20:])[0])
        بعيد_قدر.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        بعيد_قدر.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        پڑتال_دانہ((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        پڑتال_دانہ((너비-568, 높이-360), (32, 80, 144))
        چلاؤ = len(لاگ_صف); کلک_کرو_قدر(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', چلاؤ)
        پڑتال_دانہ((너비-568, 높이-360), (24, 32, 48))
        چلاؤ = len(لاگ_صف); کلک_کرو_قدر(80, 16); 기다리기(b'TERMINAL FOCUS 1', چلاؤ)
        شیل('ftpd start')
        منتقلی_قدر = ftplib.FTP(); منتقلی_قدر.encoding = 'utf-8'; منتقلی_قدر.connect('127.0.0.1', 접속번호, timeout=20); منتقلی_قدر.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·تراشہ 밖·빈 사각형을 포함한다.
        ماخذ = '''#include <화면규약.h>
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
    لکھو_فائل_کوائف(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        اپ_لوڈ_کرو_فائلاں('화면시험.c', ماخذ.encode())
        assert 'exit 0' in شیل('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', متن_پیجو('run /화면시험\n'))
        پڑتال_دانہ((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', متن_پیجو('q'))
        ماخذ = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, نظام_نقص
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except نظام_نقص as نقص:
    assert نقص.اشاریہ == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        اپ_لوڈ_کرو_فائلاں('화면시험.py', ماخذ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', متن_پیجو('python /화면시험.py\n'))
        پڑتال_دانہ((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', متن_پیجو('q'))
        ماخذ = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("سائز");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("تراشہ"); }
        catch (잘못된인수예외 نقص) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 مہمان_b78e430d javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(ماخذ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        اپ_لوڈ_کرو_فائلاں('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', متن_پیجو('java 해상도경계시험\n'))
        پڑتال_دانہ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', متن_پیجو('q'))
        # 게스트 javac의 مدد_قدر 문법으로 سائز طلب_قدر·지우기·다섯 인수 그리기를 컴파일한다.
        ماخذ = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.لکھو_لائن("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        اپ_لوڈ_کرو_فائلاں('해상도시험.java', ماخذ.encode())
        결과 = شیل('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', متن_پیجو('java 해상도시험\n'))
        پڑتال_دانہ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', متن_پیجو('q'))
        اپ_لوڈ_کرو_فائلاں('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', متن_پیجو('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        ڈرائنگ_قدر = پڑتال_دانہ((가로, 세로), (32, 80, 144))
        ڈرائنگ_قدر.save(str(결과경로/(سائز_متن+'.png')))
        چلاؤ = len(لاگ_صف); کلک_کرو_قدر(가로+80, 세로+155)
        기다리기('SWING CLICK ناں'.encode(), چلاؤ)
        چلاؤ = len(لاگ_صف); کلک_کرو_قدر(가로+385, 세로+15); 기다리기(b'jkoros-native> ', چلاؤ)
        assert 'AFTER_RESOLUTION' in شیل('echo AFTER_RESOLUTION')
        print('PASS:', سائز_متن, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if منتقلی_قدر: منتقلی_قدر.close()
        if بعيد_قدر: بعيد_قدر.close()
        if عمل_قدر.poll() is None:
            عمل_قدر.terminate()
            try: عمل_قدر.wait(timeout=8)
            except subprocess.TimeoutExpired: عمل_قدر.kill(); عمل_قدر.wait()
        منتخب_کرنڑ_آلا_a916db4e.close(); عمل_قدر.stdout.close()
        (결과경로/(سائز_متن+'.log')).write_bytes(لاگ_صف)


def چلاؤ():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    لاگ_صف = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ناجائز_قدر in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'اوزار/نفاذ_کرو_حکم.py'), '--resolution', ناجائز_قدر], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); لاگ_صف['resolutions'].append([너비, 높이])
        لاگ_صف.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(لاگ_صف, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': چلاؤ()
