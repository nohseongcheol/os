#!/usr/bin/env python3
"""ھەقىقىي_مەلۇمات QEMU/VNC에서 화면 چوڭلۇقى·경계·كۆزنەك يۆتكىمەك_قىممىتى·Swing·언어별 그리기를 검사한다."""
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
from ئۈستەليۈزى_كۆرۈنمە import 정확한값
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز


def 해상도시험(너비, 높이, ئۆلچەم_يول):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ئۆزگەرتمەك_تېكست = '{}x{}'.format(너비, 높이)
    جەريان_قىممىتى = subprocess.Popen(['python3', str(كۆرسىتىش_يىلتىز/'قوراللار/ئىجرا_قىلىش_بۇيرۇق.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ئۆزگەرتمەك_تېكست], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    تاللىغۇچ_a916db4e = selectors.DefaultSelector(); تاللىغۇچ_a916db4e.register(جەريان_قىممىتى.stdout, selectors.EVENT_READ)
    خاتىرە_قۇر = bytearray(); يىراق_قىممىتى = None; يوللاش_قىممىتى_630ba093 = None

    def 기다리기(كۆرسەتمەك_قىممىتى, ئىجرا_قىل_2=0):
        마감 = time.monotonic() + 60
        while كۆرسەتمەك_قىممىتى not in خاتىرە_قۇر[ئىجرا_قىل_2:]:
            if time.monotonic() > 마감 or جەريان_قىممىتى.poll() is not None or b'HALTED' in خاتىرە_قۇر or b'PANIC:' in خاتىرە_قۇر:
                raise AssertionError(خاتىرە_قۇر[ئىجرا_قىل_2:].decode('utf-8', 'replace'))
            for ھادىسە, _ in تاللىغۇچ_a916db4e.select(.1):
                مەلۇمات = ھادىسە.fileobj.read(65536)
                if مەلۇمات: خاتىرە_قۇر.extend(مەلۇمات)
        return خاتىرە_قۇر[ئىجرا_قىل_2:].decode('utf-8', 'replace')

    def چەكمەك_كۇنۇپكا(بەلگە, 눌림=True): يىراق_قىممىتى.sendall(struct.pack('>BBHI', 4, int(눌림), 0, بەلگە))

    def تېكىست_ئەۋەتىش(تېكىست):
        ئىجرا_قىل_2 = len(خاتىرە_قۇر)
        for ھەرپ_بەلگە_قىممىتى in تېكىست:
            بەلگە = 0xff0d if ھەرپ_بەلگە_قىممىتى == '\n' else ord(ھەرپ_بەلگە_قىممىتى) if ord(ھەرپ_بەلگە_قىممىتى) < 256 else 0x1000000 | ord(ھەرپ_بەلگە_قىممىتى)
            چەكمەك_كۇنۇپكا(بەلگە); چەكمەك_كۇنۇپكا(بەلگە, False)
        return ئىجرا_قىل_2

    def قاپ(تېكىست): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', تېكىست_ئەۋەتىش(تېكىست+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, تىك_ئورۇنلاشتۇرۇش, 눌림): يىراق_قىممىتى.sendall(struct.pack('>BBHH', 5, 눌림, 가로, تىك_ئورۇنلاشتۇرۇش))

    def چەكمەك_قىممىتى(가로, تىك_ئورۇنلاشتۇرۇش): 가리키기(가로, تىك_ئورۇنلاشتۇرۇش, 1); 가리키기(가로, تىك_ئورۇنلاشتۇرۇش, 0)

    def چېكىتلىك_تەسۋىر_رەسىم():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ھەقىقىي_مەلۇمات 너비를 쓴다.
        يىراق_قىممىتى.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        سىزىش_قىممىتى = Image.new('RGB', (너비, 높이)); تۈر_قىممىتى_9285603e = 0
        while True:
            종류 = 정확한값(يىراق_قىممىتى, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ئۇزۇنلۇق_قىممىتى = struct.unpack('>I', 정확한값(يىراق_قىممىتى, 7)[3:])[0]; 정확한값(يىراق_قىممىتى, ئۇزۇنلۇق_قىممىتى); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(يىراق_قىممىتى, 3)[1:])[0]
            for _ in range(개수):
                가로, تىك_ئورۇنلاشتۇرۇش, 폭, ئۇزۇنلۇق_قىممىتى, كودىلاش_قىممىتى = struct.unpack('>HHHHi', 정확한값(يىراق_قىممىتى, 12))
                assert كودىلاش_قىممىتى == 0 and 가로+폭 <= 너비 and تىك_ئورۇنلاشتۇرۇش+ئۇزۇنلۇق_قىممىتى <= 높이
                سىزىش_قىممىتى.paste(Image.frombytes('RGB', (폭, ئۇزۇنلۇق_قىممىتى), 정확한값(يىراق_قىممىتى, 폭*ئۇزۇنلۇق_قىممىتى*4), 'raw', 'BGRX'), (가로, تىك_ئورۇنلاشتۇرۇش))
                تۈر_قىممىتى_9285603e += 폭*ئۇزۇنلۇق_قىممىتى
            if تۈر_قىممىتى_9285603e:
                assert تۈر_قىممىتى_9285603e == 너비*높이, تۈر_قىممىتى_9285603e
                return سىزىش_قىممىتى

    def تەكشۈرۈش_پىكسېل(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            سىزىش_قىممىتى = چېكىتلىك_تەسۋىر_رەسىم()
            if سىزىش_قىممىتى.getpixel(좌표) == 색: return سىزىش_قىممىتى
            if time.monotonic() > 마감: raise AssertionError((좌표, سىزىش_قىممىتى.getpixel(좌표), 색))

    def يۈكلىمەك_ھۆججەت(ئاتى, مەلۇمات): يوللاش_قىممىتى_630ba093.storbinary('STOR '+ئاتى, io.BytesIO(مەلۇمات))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ئۆزگەرتمەك_تېكست+' RGB32').encode() in خاتىرە_قۇر
        print('BOOT:', ئۆزگەرتمەك_تېكست, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', خاتىرە_قۇر).group(1))
        يىراق_قىممىتى = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(يىراق_قىممىتى, 12) == b'RFB 003.008\n'; يىراق_قىممىتى.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(يىراق_قىممىتى, 정확한값(يىراق_قىممىتى, 1)[0]); يىراق_قىممىتى.sendall(b'\x01')
        assert 정확한값(يىراق_قىممىتى, 4) == b'\0'*4; يىراق_قىممىتى.sendall(b'\x01')
        초기 = 정확한값(يىراق_قىممىتى, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(يىراق_قىممىتى, struct.unpack('>I', 초기[20:])[0])
        يىراق_قىممىتى.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        يىراق_قىممىتى.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        تەكشۈرۈش_پىكسېل((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        تەكشۈرۈش_پىكسېل((너비-568, 높이-360), (32, 80, 144))
        ئىجرا_قىل_2 = len(خاتىرە_قۇر); چەكمەك_قىممىتى(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ئىجرا_قىل_2)
        تەكشۈرۈش_پىكسېل((너비-568, 높이-360), (24, 32, 48))
        ئىجرا_قىل_2 = len(خاتىرە_قۇر); چەكمەك_قىممىتى(80, 16); 기다리기(b'TERMINAL FOCUS 1', ئىجرا_قىل_2)
        قاپ('ftpd start')
        يوللاش_قىممىتى_630ba093 = ftplib.FTP(); يوللاش_قىممىتى_630ba093.encoding = 'utf-8'; يوللاش_قىممىتى_630ba093.connect('127.0.0.1', 접속번호, timeout=20); يوللاش_قىممىتى_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·كەسمە 밖·빈 사각형을 포함한다.
        مەنبە = '''#include <화면규약.h>
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
    يازماق_ھۆججەت_مەلۇمات(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        يۈكلىمەك_ھۆججەت('화면시험.c', مەنبە.encode())
        assert 'exit 0' in قاپ('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', تېكىست_ئەۋەتىش('run /화면시험\n'))
        تەكشۈرۈش_پىكسېل((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', تېكىست_ئەۋەتىش('q'))
        مەنبە = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, چىقار, سىستېما_خاتالىق
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except سىستېما_خاتالىق as خاتالىق:
    assert خاتالىق.ئىندېكس == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
چىقار("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        يۈكلىمەك_ھۆججەت('화면시험.py', مەنبە.encode())
        기다리기(b'PYTHON RESOLUTION PASS', تېكىست_ئەۋەتىش('python /화면시험.py\n'))
        تەكشۈرۈش_پىكسېل((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', تېكىست_ئەۋەتىش('q'))
        مەنبە = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] ئۆزگەرگۈچىلەر) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("چوڭلۇقى");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("كەسمە"); }
        catch (잘못된인수예외 خاتالىق) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 باقار javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = ئۆلچەم_يول/'해상도경계시험.java'
        경계원문.write_text(مەنبە.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(كۆرسىتىش_يىلتىز/'dist/jkoros-native-korean.jar'), '-d', str(ئۆلچەم_يول), str(경계원문)])
        يۈكلىمەك_ھۆججەت('해상도경계시험.class', (ئۆلچەم_يول/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', تېكىست_ئەۋەتىش('java 해상도경계시험\n'))
        تەكشۈرۈش_پىكسېل((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', تېكىست_ئەۋەتىش('q'))
        # 게스트 javac의 قوللاش_قىممىتى 문법으로 چوڭلۇقى تەكشۈرۈش_قىممىتى·지우기·다섯 ئۆزگەرگۈچىلەر 그리기를 컴파일한다.
        مەنبە = '''public class 해상도시험 {
    public static void main(String[] ئۆزگەرگۈچىلەر) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.چىقار.يازماق_قۇر("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        يۈكلىمەك_ھۆججەت('해상도시험.java', مەنبە.encode())
        ئۆلچەم = قاپ('javac 해상도시험.java'); assert 'exit 0' in ئۆلچەم, ئۆلچەم
        기다리기(b'JAVA RESOLUTION PASS', تېكىست_ئەۋەتىش('java 해상도시험\n'))
        تەكشۈرۈش_پىكسېل((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', تېكىست_ئەۋەتىش('q'))
        يۈكلىمەك_ھۆججەت('스윙시험.class', (ئۆلچەم_يول/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', تېكىست_ئەۋەتىش('java 스윙시험\n'))
        가로, تىك_ئورۇنلاشتۇرۇش = (너비-400)//2, (높이-280)//2
        سىزىش_قىممىتى = تەكشۈرۈش_پىكسېل((가로, تىك_ئورۇنلاشتۇرۇش), (32, 80, 144))
        سىزىش_قىممىتى.save(str(ئۆلچەم_يول/(ئۆزگەرتمەك_تېكست+'.png')))
        ئىجرا_قىل_2 = len(خاتىرە_قۇر); چەكمەك_قىممىتى(가로+80, تىك_ئورۇنلاشتۇرۇش+155)
        기다리기('SWING CLICK ئاتى'.encode(), ئىجرا_قىل_2)
        ئىجرا_قىل_2 = len(خاتىرە_قۇر); چەكمەك_قىممىتى(가로+385, تىك_ئورۇنلاشتۇرۇش+15); 기다리기(b'jkoros-native> ', ئىجرا_قىل_2)
        assert 'AFTER_RESOLUTION' in قاپ('echo AFTER_RESOLUTION')
        print('PASS:', ئۆزگەرتمەك_تېكست, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if يوللاش_قىممىتى_630ba093: يوللاش_قىممىتى_630ba093.close()
        if يىراق_قىممىتى: يىراق_قىممىتى.close()
        if جەريان_قىممىتى.poll() is None:
            جەريان_قىممىتى.terminate()
            try: جەريان_قىممىتى.wait(timeout=8)
            except subprocess.TimeoutExpired: جەريان_قىممىتى.kill(); جەريان_قىممىتى.wait()
        تاللىغۇچ_a916db4e.close(); جەريان_قىممىتى.stdout.close()
        (ئۆلچەم_يول/(ئۆزگەرتمەك_تېكست+'.log')).write_bytes(خاتىرە_قۇر)


def ئىجرا_قىل_2():
    ئۆلچەم_يول = كۆرسىتىش_يىلتىز/'build/verification/resolution'; ئۆلچەم_يول.mkdir(parents=True, exist_ok=True)
    خاتىرە_قۇر = {'passed': False, 'kernel_sha256': hashlib.sha256((كۆرسىتىش_يىلتىز/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ئۈنۈمسىز_قىممىتى in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ئۆلچەم = subprocess.run(['python3', str(كۆرسىتىش_يىلتىز/'قوراللار/ئىجرا_قىلىش_بۇيرۇق.py'), '--resolution', ئۈنۈمسىز_قىممىتى], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ئۆلچەم.returncode == 2 and b'--resolution' in ئۆلچەم.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ئۆلچەم_يول), str(كۆرسىتىش_يىلتىز/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, ئۆلچەم_يول); خاتىرە_قۇر['resolutions'].append([너비, 높이])
        خاتىرە_قۇر.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (ئۆلچەم_يول/'report.json').write_text(json.dumps(خاتىرە_قۇر, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ئىجرا_قىل_2()
