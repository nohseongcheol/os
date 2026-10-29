#!/usr/bin/env python3
"""প্রকৃত_ডাটা QEMU/VNC에서 화면 আকার·경계·উইন্ডো অপসারণ_করা_মান·Swing·언어별 그리기를 검사한다."""
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
from ডেস্কটপ_ভিউ import 정확한값
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল


def 해상도시험(너비, 높이, পরিমাপ_পথ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); পোর্ট_নম্বর = 임시.getsockname()[1]
    আয়তন_পাঠ = '{}x{}'.format(너비, 높이)
    প্রসেসর_মান = subprocess.Popen(['python3', str(প্রকল্প_মূল/'সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(পোর্ট_নম্বর), '--resolution', আয়তন_পাঠ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    নির্বাচক_a916db4e = selectors.DefaultSelector(); নির্বাচক_a916db4e.register(প্রসেসর_মান.stdout, selectors.EVENT_READ)
    লগ_সারি = bytearray(); দূরবর্তী_মান = None; স্থানান্তর_মান = None

    def 기다리기(শো_মান, চালনা=0):
        마감 = time.monotonic() + 60
        while শো_মান not in লগ_সারি[চালনা:]:
            if time.monotonic() > 마감 or প্রসেসর_মান.poll() is not None or b'HALTED' in লগ_সারি or b'PANIC:' in লগ_সারি:
                raise AssertionError(লগ_সারি[চালনা:].decode('utf-8', 'replace'))
            for ঘটনা, _ in নির্বাচক_a916db4e.select(.1):
                ডাটা = ঘটনা.fileobj.read(65536)
                if ডাটা: লগ_সারি.extend(ডাটা)
        return লগ_সারি[চালনা:].decode('utf-8', 'replace')

    def ক্লিক_করা_বোতাম(প্রতীক, 눌림=True): দূরবর্তী_মান.sendall(struct.pack('>BBHI', 4, int(눌림), 0, প্রতীক))

    def SMS_পাঠান(পাঠ):
        চালনা = len(লগ_সারি)
        for অক্ষর_মান in পাঠ:
            প্রতীক = 0xff0d if অক্ষর_মান == '\n' else ord(অক্ষর_মান) if ord(অক্ষর_মান) < 256 else 0x1000000 | ord(অক্ষর_মান)
            ক্লিক_করা_বোতাম(প্রতীক); ক্লিক_করা_বোতাম(প্রতীক, False)
        return চালনা

    def শেল(পাঠ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_পাঠান(পাঠ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, উল্লম্ব_পদ, 눌림): দূরবর্তী_মান.sendall(struct.pack('>BBHH', 5, 눌림, 가로, উল্লম্ব_পদ))

    def ক্লিক_করা_মান(가로, উল্লম্ব_পদ): 가리키기(가로, উল্লম্ব_পদ, 1); 가리키기(가로, উল্লম্ব_পদ, 0)

    def বিটম্যাপ_ছবি():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 প্রকৃত_ডাটা 너비를 쓴다.
        দূরবর্তী_মান.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        অঙ্কন_মান = Image.new('RGB', (너비, 높이)); এলাকা_মান = 0
        while True:
            종류 = 정확한값(দূরবর্তী_মান, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                দৈর্ঘ্য_মান = struct.unpack('>I', 정확한값(দূরবর্তী_মান, 7)[3:])[0]; 정확한값(দূরবর্তী_মান, দৈর্ঘ্য_মান); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(দূরবর্তী_মান, 3)[1:])[0]
            for _ in range(개수):
                가로, উল্লম্ব_পদ, 폭, দৈর্ঘ্য_মান, এনকোড_করা_মান = struct.unpack('>HHHHi', 정확한값(দূরবর্তী_মান, 12))
                assert এনকোড_করা_মান == 0 and 가로+폭 <= 너비 and উল্লম্ব_পদ+দৈর্ঘ্য_মান <= 높이
                অঙ্কন_মান.paste(Image.frombytes('RGB', (폭, দৈর্ঘ্য_মান), 정확한값(দূরবর্তী_মান, 폭*দৈর্ঘ্য_মান*4), 'raw', 'BGRX'), (가로, উল্লম্ব_পদ))
                এলাকা_মান += 폭*দৈর্ঘ্য_মান
            if এলাকা_মান:
                assert এলাকা_মান == 너비*높이, এলাকা_মান
                return অঙ্কন_মান

    def চেক_পেল্(অক্ষবিন্দু_মান, 색):
        마감 = time.monotonic()+10
        while True:
            অঙ্কন_মান = বিটম্যাপ_ছবি()
            if অঙ্কন_মান.getpixel(অক্ষবিন্দু_মান) == 색: return অঙ্কন_মান
            if time.monotonic() > 마감: raise AssertionError((অক্ষবিন্দু_মান, অঙ্কন_মান.getpixel(অক্ষবিন্দু_মান), 색))

    def আপলোড_ফাইলগুলি(নাম, ডাটা): স্থানান্তর_মান.storbinary('STOR '+নাম, io.BytesIO(ডাটা))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+আয়তন_পাঠ+' RGB32').encode() in লগ_সারি
        print('BOOT:', আয়তন_পাঠ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', লগ_সারি).group(1))
        দূরবর্তী_মান = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(দূরবর্তী_মান, 12) == b'RFB 003.008\n'; দূরবর্তী_মান.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(দূরবর্তী_মান, 정확한값(দূরবর্তী_মান, 1)[0]); দূরবর্তী_মান.sendall(b'\x01')
        assert 정확한값(দূরবর্তী_মান, 4) == b'\0'*4; দূরবর্তী_মান.sendall(b'\x01')
        초기 = 정확한값(দূরবর্তী_মান, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(দূরবর্তী_মান, struct.unpack('>I', 초기[20:])[0])
        দূরবর্তী_মান.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        দূরবর্তী_মান.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        চেক_পেল্((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        চেক_পেল্((너비-568, 높이-360), (32, 80, 144))
        চালনা = len(লগ_সারি); ক্লিক_করা_মান(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', চালনা)
        চেক_পেল্((너비-568, 높이-360), (24, 32, 48))
        চালনা = len(লগ_সারি); ক্লিক_করা_মান(80, 16); 기다리기(b'TERMINAL FOCUS 1', চালনা)
        শেল('ftpd start')
        স্থানান্তর_মান = ftplib.FTP(); স্থানান্তর_মান.encoding = 'utf-8'; স্থানান্তর_মান.connect('127.0.0.1', পোর্ট_নম্বর, timeout=20); স্থানান্তর_মান.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ক্লিপ 밖·빈 사각형을 포함한다.
        উৎস_নথি = '''#include <화면규약.h>
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
    লেখা_ফাইল_ডাটা(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        আপলোড_ফাইলগুলি('화면시험.c', উৎস_নথি.encode())
        assert 'exit 0' in শেল('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_পাঠান('run /화면시험\n'))
        চেক_পেল্((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_পাঠান('q'))
        উৎস_নথি = '''from বাংলা import 화면크기, 네모그리기, 그림기다리기, নির্গম, সিস্টেম_ত্রুটি
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except সিস্টেম_ত্রুটি as ত্রুটি:
    assert ত্রুটি.সূচি == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
নির্গম("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        আপলোড_ফাইলগুলি('화면시험.py', উৎস_নথি.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_পাঠান('python /화면시험.py\n'))
        চেক_পেল্((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_পাঠান('q'))
        উৎস_নথি = '''import বাংলা.নিজ.*;
public class 해상도시험 {
    public static void main(String[] আর্গুমেন্ট_তালিকা) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new অবস্হা_ব্যতিক্রম("আকার");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new অবস্হা_ব্যতিক্রম("ক্লিপ"); }
        catch (অবৈধ_যুক্তি_ব্যতিক্রম ত্রুটি) { }
        화면.মুছুন_ভুক্তি(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # ব্যতিক্রম 처리는 হোস্ট javac 결과를 নিজ JVM에 올려 검사한다.
        경계원문 = পরিমাপ_পথ/'해상도경계시험.java'
        경계원문.write_text(উৎস_নথি.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(প্রকল্প_মূল/'dist/jkoros-native-korean.jar'), '-d', str(পরিমাপ_পথ), str(경계원문)])
        আপলোড_ফাইলগুলি('해상도경계시험.class', (পরিমাপ_পথ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_পাঠান('java 해상도경계시험\n'))
        চেক_পেল্((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_পাঠান('q'))
        # 게스트 javac의 সমর্থন_মান 문법으로 আকার জিজ্ঞাসা_মান·মুছুন_ভুক্তি·다섯 আর্গুমেন্ট_তালিকা 그리기를 컴파일한다.
        উৎস_নথি = '''public class 해상도시험 {
    public static void main(String[] আর্গুমেন্ট_তালিকা) {
        int 너비=বাংলা.নিজ.화면.너비();
        int 높이=বাংলা.নিজ.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        বাংলা.নিজ.화면.মুছুন_ভুক্তি(3153944);
        বাংলা.নিজ.화면.사각형(너비-1,높이-1,1,1,10061943);
        বাংলা.নিজ.নির্গম.লেখা_লাইন("JAVA RESOLUTION PASS");
        বাংলা.নিজ.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        আপলোড_ফাইলগুলি('해상도시험.java', উৎস_নথি.encode())
        পরিমাপ = শেল('javac 해상도시험.java'); assert 'exit 0' in পরিমাপ, পরিমাপ
        기다리기(b'JAVA RESOLUTION PASS', SMS_পাঠান('java 해상도시험\n'))
        চেক_পেল্((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_পাঠান('q'))
        আপলোড_ফাইলগুলি('스윙시험.class', (পরিমাপ_পথ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_পাঠান('java 스윙시험\n'))
        가로, উল্লম্ব_পদ = (너비-400)//2, (높이-280)//2
        অঙ্কন_মান = চেক_পেল্((가로, উল্লম্ব_পদ), (32, 80, 144))
        অঙ্কন_মান.save(str(পরিমাপ_পথ/(আয়তন_পাঠ+'.png')))
        চালনা = len(লগ_সারি); ক্লিক_করা_মান(가로+80, উল্লম্ব_পদ+155)
        기다리기('SWING CLICK নাম'.encode(), চালনা)
        চালনা = len(লগ_সারি); ক্লিক_করা_মান(가로+385, উল্লম্ব_পদ+15); 기다리기(b'jkoros-native> ', চালনা)
        assert 'AFTER_RESOLUTION' in শেল('echo AFTER_RESOLUTION')
        print('PASS:', আয়তন_পাঠ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if স্থানান্তর_মান: স্থানান্তর_মান.close()
        if দূরবর্তী_মান: দূরবর্তী_মান.close()
        if প্রসেসর_মান.poll() is None:
            প্রসেসর_মান.terminate()
            try: প্রসেসর_মান.wait(timeout=8)
            except subprocess.TimeoutExpired: প্রসেসর_মান.kill(); প্রসেসর_মান.wait()
        নির্বাচক_a916db4e.close(); প্রসেসর_মান.stdout.close()
        (পরিমাপ_পথ/(আয়তন_পাঠ+'.log')).write_bytes(লগ_সারি)


def চালনা():
    পরিমাপ_পথ = প্রকল্প_মূল/'build/verification/resolution'; পরিমাপ_পথ.mkdir(parents=True, exist_ok=True)
    লগ_সারি = {'passed': False, 'kernel_sha256': hashlib.sha256((প্রকল্প_মূল/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for অবৈধ_মান in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            পরিমাপ = subprocess.run(['python3', str(প্রকল্প_মূল/'সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py'), '--resolution', অবৈধ_মান], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert পরিমাপ.returncode == 2 and b'--resolution' in পরিমাপ.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(পরিমাপ_পথ), str(প্রকল্প_মূল/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, পরিমাপ_পথ); লগ_সারি['resolutions'].append([너비, 높이])
        লগ_সারি.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (পরিমাপ_পথ/'report.json').write_text(json.dumps(লগ_সারি, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': চালনা()
