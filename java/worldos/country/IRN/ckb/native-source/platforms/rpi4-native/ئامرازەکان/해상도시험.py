#!/usr/bin/env python3
"""ڕاستەکی_دەیتا QEMU/VNC에서 화면 گۆڕینی_ئەندازە·경계·پەنجەرە گواستنەوە_نرخ·Swing·언어별 그리기를 검사한다."""
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
from دێسکتۆپ_دیمەن import 정확한값
from جێبەجێکردن_فەرمان import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    گۆڕینی_ئەندازە_دەق = '{}x{}'.format(너비, 높이)
    پرۆسە_نرخ = subprocess.Popen(['python3', str(기준/'ئامرازەکان/جێبەجێکردن_فەرمان.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', گۆڕینی_ئەندازە_دەق], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    هەڵبژێرەر_a916db4e = selectors.DefaultSelector(); هەڵبژێرەر_a916db4e.register(پرۆسە_نرخ.stdout, selectors.EVENT_READ)
    تۆمار_ڕزن = bytearray(); دوورەدەس_نرخ = None; گواستنەوە_نرخ_630ba093 = None

    def 기다리기(نیشاندان_نرخ, ڕادان=0):
        마감 = time.monotonic() + 60
        while نیشاندان_نرخ not in تۆمار_ڕزن[ڕادان:]:
            if time.monotonic() > 마감 or پرۆسە_نرخ.poll() is not None or b'HALTED' in تۆمار_ڕزن or b'PANIC:' in تۆمار_ڕزن:
                raise AssertionError(تۆمار_ڕزن[ڕادان:].decode('utf-8', 'replace'))
            for پێشهات, _ in هەڵبژێرەر_a916db4e.select(.1):
                دەیتا = پێشهات.fileobj.read(65536)
                if دەیتا: تۆمار_ڕزن.extend(دەیتا)
        return تۆمار_ڕزن[ڕادان:].decode('utf-8', 'replace')

    def کرته_کردن_دوگمه(سیمبۆل, 눌림=True): دوورەدەس_نرخ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, سیمبۆل))

    def تێکست_بنێرە(دەق):
        ڕادان = len(تۆمار_ڕزن)
        for نووسە_نرخ in دەق:
            سیمبۆل = 0xff0d if نووسە_نرخ == '\n' else ord(نووسە_نرخ) if ord(نووسە_نرخ) < 256 else 0x1000000 | ord(نووسە_نرخ)
            کرته_کردن_دوگمه(سیمبۆل); کرته_کردن_دوگمه(سیمبۆل, False)
        return ڕادان

    def توێکڵ(دەق): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', تێکست_بنێرە(دەق+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): دوورەدەس_نرخ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def کرته_کردن_نرخ(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def بیتمەپ_وێنە():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ڕاستەکی_دەیتا 너비를 쓴다.
        دوورەدەس_نرخ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        نگار_نرخ = Image.new('RGB', (너비, 높이)); شوێن_نرخ = 0
        while True:
            종류 = 정확한값(دوورەدەس_نرخ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                درێژی_نرخ = struct.unpack('>I', 정확한값(دوورەدەس_نرخ, 7)[3:])[0]; 정확한값(دوورەدەس_نرخ, درێژی_نرخ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(دوورەدەس_نرخ, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, درێژی_نرخ, نهێنبەندی_نرخ = struct.unpack('>HHHHi', 정확한값(دوورەدەس_نرخ, 12))
                assert نهێنبەندی_نرخ == 0 and 가로+폭 <= 너비 and 세로+درێژی_نرخ <= 높이
                نگار_نرخ.paste(Image.frombytes('RGB', (폭, درێژی_نرخ), 정확한값(دوورەدەس_نرخ, 폭*درێژی_نرخ*4), 'raw', 'BGRX'), (가로, 세로))
                شوێن_نرخ += 폭*درێژی_نرخ
            if شوێن_نرخ:
                assert شوێن_نرخ == 너비*높이, شوێن_نرخ
                return نگار_نرخ

    def پشکنین_پێڵ(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            نگار_نرخ = بیتمەپ_وێنە()
            if نگار_نرخ.getpixel(좌표) == 색: return نگار_نرخ
            if time.monotonic() > 마감: raise AssertionError((좌표, نگار_نرخ.getpixel(좌표), 색))

    def بار_کردن_فایله_کان(ناو, دەیتا): گواستنەوە_نرخ_630ba093.storbinary('STOR '+ناو, io.BytesIO(دەیتا))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+گۆڕینی_ئەندازە_دەق+' RGB32').encode() in تۆمار_ڕزن
        print('BOOT:', گۆڕینی_ئەندازە_دەق, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', تۆمار_ڕزن).group(1))
        دوورەدەس_نرخ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(دوورەدەس_نرخ, 12) == b'RFB 003.008\n'; دوورەدەس_نرخ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(دوورەدەس_نرخ, 정확한값(دوورەدەس_نرخ, 1)[0]); دوورەدەس_نرخ.sendall(b'\x01')
        assert 정확한값(دوورەدەس_نرخ, 4) == b'\0'*4; دوورەدەس_نرخ.sendall(b'\x01')
        초기 = 정확한값(دوورەدەس_نرخ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(دوورەدەس_نرخ, struct.unpack('>I', 초기[20:])[0])
        دوورەدەس_نرخ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        دوورەدەس_نرخ.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        پشکنین_پێڵ((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        پشکنین_پێڵ((너비-568, 높이-360), (32, 80, 144))
        ڕادان = len(تۆمار_ڕزن); کرته_کردن_نرخ(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ڕادان)
        پشکنین_پێڵ((너비-568, 높이-360), (24, 32, 48))
        ڕادان = len(تۆمار_ڕزن); کرته_کردن_نرخ(80, 16); 기다리기(b'TERMINAL FOCUS 1', ڕادان)
        توێکڵ('ftpd start')
        گواستنەوە_نرخ_630ba093 = ftplib.FTP(); گواستنەوە_نرخ_630ba093.encoding = 'utf-8'; گواستنەوە_نرخ_630ba093.connect('127.0.0.1', 접속번호, timeout=20); گواستنەوە_نرخ_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·کلیپ 밖·빈 사각형을 포함한다.
        ژێدەر = '''#include <화면규약.h>
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
    ڕایت_کردن_فایل_دەیتا(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        بار_کردن_فایله_کان('화면시험.c', ژێدەر.encode())
        assert 'exit 0' in توێکڵ('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', تێکست_بنێرە('run /화면시험\n'))
        پشکنین_پێڵ((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', تێکست_بنێرە('q'))
        ژێدەر = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, سیستم_هەڵە
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except سیستم_هەڵە as هەڵە:
    assert هەڵە.پێرست == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        بار_کردن_فایله_کان('화면시험.py', ژێدەر.encode())
        기다리기(b'PYTHON RESOLUTION PASS', تێکست_بنێرە('python /화면시험.py\n'))
        پشکنین_پێڵ((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', تێکست_بنێرە('q'))
        ژێدەر = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("گۆڕینی_ئەندازە");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("کلیپ"); }
        catch (잘못된인수예외 هەڵە) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 جێدەر javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(ژێدەر.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        بار_کردن_فایله_کان('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', تێکست_بنێرە('java 해상도경계시험\n'))
        پشکنین_پێڵ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', تێکست_بنێرە('q'))
        # 게스트 javac의 پشتیوانی_نرخ 문법으로 گۆڕینی_ئەندازە پرس_نرخ·지우기·다섯 인수 그리기를 컴파일한다.
        ژێدەر = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.ڕایت_کردن_دێڕ("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        بار_کردن_فایله_کان('해상도시험.java', ژێدەر.encode())
        결과 = توێکڵ('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', تێکست_بنێرە('java 해상도시험\n'))
        پشکنین_پێڵ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', تێکست_بنێرە('q'))
        بار_کردن_فایله_کان('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', تێکست_بنێرە('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        نگار_نرخ = پشکنین_پێڵ((가로, 세로), (32, 80, 144))
        نگار_نرخ.save(str(결과경로/(گۆڕینی_ئەندازە_دەق+'.png')))
        ڕادان = len(تۆمار_ڕزن); کرته_کردن_نرخ(가로+80, 세로+155)
        기다리기('SWING CLICK ناو'.encode(), ڕادان)
        ڕادان = len(تۆمار_ڕزن); کرته_کردن_نرخ(가로+385, 세로+15); 기다리기(b'jkoros-native> ', ڕادان)
        assert 'AFTER_RESOLUTION' in توێکڵ('echo AFTER_RESOLUTION')
        print('PASS:', گۆڕینی_ئەندازە_دەق, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if گواستنەوە_نرخ_630ba093: گواستنەوە_نرخ_630ba093.close()
        if دوورەدەس_نرخ: دوورەدەس_نرخ.close()
        if پرۆسە_نرخ.poll() is None:
            پرۆسە_نرخ.terminate()
            try: پرۆسە_نرخ.wait(timeout=8)
            except subprocess.TimeoutExpired: پرۆسە_نرخ.kill(); پرۆسە_نرخ.wait()
        هەڵبژێرەر_a916db4e.close(); پرۆسە_نرخ.stdout.close()
        (결과경로/(گۆڕینی_ئەندازە_دەق+'.log')).write_bytes(تۆمار_ڕزن)


def ڕادان():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    تۆمار_ڕزن = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for بێبایەخ_نرخ in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'ئامرازەکان/جێبەجێکردن_فەرمان.py'), '--resolution', بێبایەخ_نرخ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); تۆمار_ڕزن['resolutions'].append([너비, 높이])
        تۆمار_ڕزن.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(تۆمار_ڕزن, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ڕادان()
