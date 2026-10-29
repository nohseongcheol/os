#!/usr/bin/env python3
"""প্ৰকৃত_ডাটা QEMU/VNC에서 화면 মাপ·경계·উইণ্ড লৈ_যাওক_মান·Swing·언어별 그리기를 검사한다."""
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
from ডেস্কটপ_দর্শন import 정확한값
from নিষ্পাদন_আদেশ import 기준


def 해상도시험(너비, 높이, পৰিমাপ_পথ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    আকাৰ_কৰক_পাঠ = '{}x{}'.format(너비, 높이)
    প্ৰক্ৰিয়া_মান = subprocess.Popen(['python3', str(기준/'সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', আকাৰ_কৰক_পাঠ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    চয়নকাৰী_a916db4e = selectors.DefaultSelector(); চয়নকাৰী_a916db4e.register(প্ৰক্ৰিয়া_মান.stdout, selectors.EVENT_READ)
    লগ_শাৰী = bytearray(); দূৰবৰ্তী_মান = None; স্থানান্তৰণ_মান = None

    def 기다리기(শ্ব_মান, সঞ্চালন=0):
        마감 = time.monotonic() + 60
        while শ্ব_মান not in লগ_শাৰী[সঞ্চালন:]:
            if time.monotonic() > 마감 or প্ৰক্ৰিয়া_মান.poll() is not None or b'HALTED' in লগ_শাৰী or b'PANIC:' in লগ_শাৰী:
                raise AssertionError(লগ_শাৰী[সঞ্চালন:].decode('utf-8', 'replace'))
            for ইভেণ্ট, _ in চয়নকাৰী_a916db4e.select(.1):
                ডাটা = ইভেণ্ট.fileobj.read(65536)
                if ডাটা: লগ_শাৰী.extend(ডাটা)
        return লগ_শাৰী[সঞ্চালন:].decode('utf-8', 'replace')

    def ক্লিক_কৰক_বুটাম(প্ৰতীক, 눌림=True): দূৰবৰ্তী_মান.sendall(struct.pack('>BBHI', 4, int(눌림), 0, প্ৰতীক))

    def SMS_প্ৰেৰণ_কৰক(টেক্সট):
        সঞ্চালন = len(লগ_শাৰী)
        for বৰ্ণ_মান in টেক্সট:
            প্ৰতীক = 0xff0d if বৰ্ণ_মান == '\n' else ord(বৰ্ণ_মান) if ord(বৰ্ণ_মান) < 256 else 0x1000000 | ord(বৰ্ণ_মান)
            ক্লিক_কৰক_বুটাম(প্ৰতীক); ক্লিক_কৰক_বুটাম(প্ৰতীক, False)
        return সঞ্চালন

    def শ্বেল(টেক্সট): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_প্ৰেৰণ_কৰক(টেক্সট+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, উলম্ব_স্থান_সলনি_কৰক, 눌림): দূৰবৰ্তী_মান.sendall(struct.pack('>BBHH', 5, 눌림, 가로, উলম্ব_স্থান_সলনি_কৰক))

    def ক্লিক_কৰক_মান(가로, উলম্ব_স্থান_সলনি_কৰক): 가리키기(가로, উলম্ব_স্থান_সলনি_কৰক, 1); 가리키기(가로, উলম্ব_স্থান_সলনি_কৰক, 0)

    def বিটমেপ_ছবি():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 প্ৰকৃত_ডাটা 너비를 쓴다.
        দূৰবৰ্তী_মান.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        অংকন_মান = Image.new('RGB', (너비, 높이)); বৰ্গ_মান = 0
        while True:
            종류 = 정확한값(দূৰবৰ্তী_মান, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                দৈর্ঘ্য_মান = struct.unpack('>I', 정확한값(দূৰবৰ্তী_মান, 7)[3:])[0]; 정확한값(দূৰবৰ্তী_মান, দৈর্ঘ্য_মান); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(দূৰবৰ্তী_মান, 3)[1:])[0]
            for _ in range(개수):
                가로, উলম্ব_স্থান_সলনি_কৰক, 폭, দৈর্ঘ্য_মান, এনকোডিং_মান = struct.unpack('>HHHHi', 정확한값(দূৰবৰ্তী_মান, 12))
                assert এনকোডিং_মান == 0 and 가로+폭 <= 너비 and উলম্ব_স্থান_সলনি_কৰক+দৈর্ঘ্য_মান <= 높이
                অংকন_মান.paste(Image.frombytes('RGB', (폭, দৈর্ঘ্য_মান), 정확한값(দূৰবৰ্তী_মান, 폭*দৈর্ঘ্য_মান*4), 'raw', 'BGRX'), (가로, উলম্ব_স্থান_সলনি_কৰক))
                বৰ্গ_মান += 폭*দৈর্ঘ্য_মান
            if বৰ্গ_মান:
                assert বৰ্গ_মান == 너비*높이, বৰ্গ_মান
                return অংকন_মান

    def পৰীক্ষণ_পিক্সেল(সমন্বয়_মান, 색):
        마감 = time.monotonic()+10
        while True:
            অংকন_মান = বিটমেপ_ছবি()
            if অংকন_মান.getpixel(সমন্বয়_মান) == 색: return অংকন_মান
            if time.monotonic() > 마감: raise AssertionError((সমন্বয়_মান, অংকন_মান.getpixel(সমন্বয়_মান), 색))

    def আপল_ড_কৰক_ফাইলসমূহ(নাম, ডাটা): স্থানান্তৰণ_মান.storbinary('STOR '+নাম, io.BytesIO(ডাটা))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+আকাৰ_কৰক_পাঠ+' RGB32').encode() in লগ_শাৰী
        print('BOOT:', আকাৰ_কৰক_পাঠ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', লগ_শাৰী).group(1))
        দূৰবৰ্তী_মান = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(দূৰবৰ্তী_মান, 12) == b'RFB 003.008\n'; দূৰবৰ্তী_মান.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(দূৰবৰ্তী_মান, 정확한값(দূৰবৰ্তী_মান, 1)[0]); দূৰবৰ্তী_মান.sendall(b'\x01')
        assert 정확한값(দূৰবৰ্তী_মান, 4) == b'\0'*4; দূৰবৰ্তী_মান.sendall(b'\x01')
        초기 = 정확한값(দূৰবৰ্তী_মান, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(দূৰবৰ্তী_মান, struct.unpack('>I', 초기[20:])[0])
        দূৰবৰ্তী_মান.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        দূৰবৰ্তী_মান.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        পৰীক্ষণ_পিক্সেল((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        পৰীক্ষণ_পিক্সেল((너비-568, 높이-360), (32, 80, 144))
        সঞ্চালন = len(লগ_শাৰী); ক্লিক_কৰক_মান(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', সঞ্চালন)
        পৰীক্ষণ_পিক্সেল((너비-568, 높이-360), (24, 32, 48))
        সঞ্চালন = len(লগ_শাৰী); ক্লিক_কৰক_মান(80, 16); 기다리기(b'TERMINAL FOCUS 1', সঞ্চালন)
        শ্বেল('ftpd start')
        স্থানান্তৰণ_মান = ftplib.FTP(); স্থানান্তৰণ_মান.encoding = 'utf-8'; স্থানান্তৰণ_মান.connect('127.0.0.1', 접속번호, timeout=20); স্থানান্তৰণ_মান.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ক্লিপ 밖·빈 사각형을 포함한다.
        উৎস = '''#include <화면규약.h>
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
    লিখক_ফাইল_ডাটা(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        আপল_ড_কৰক_ফাইলসমূহ('화면시험.c', উৎস.encode())
        assert 'exit 0' in শ্বেল('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_প্ৰেৰণ_কৰক('run /화면시험\n'))
        পৰীক্ষণ_পিক্সেল((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_প্ৰেৰণ_কৰক('q'))
        উৎস = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, নিৰ্গম, ছিষ্টেম_ত্ৰুটি
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ছিষ্টেম_ত্ৰুটি as ত্ৰুটি:
    assert ত্ৰুটি.ইনডেক্স == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
নিৰ্গম("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        আপল_ড_কৰক_ফাইলসমূহ('화면시험.py', উৎস.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_প্ৰেৰণ_কৰক('python /화면시험.py\n'))
        পৰীক্ষণ_পিক্সেল((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_প্ৰেৰণ_কৰক('q'))
        উৎস = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("মাপ");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("ক্লিপ"); }
        catch (잘못된인수예외 ত্ৰুটি) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 হ_ষ্ট javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = পৰিমাপ_পথ/'해상도경계시험.java'
        경계원문.write_text(উৎস.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(পৰিমাপ_পথ), str(경계원문)])
        আপল_ড_কৰক_ফাইলসমূহ('해상도경계시험.class', (পৰিমাপ_পথ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_প্ৰেৰণ_কৰক('java 해상도경계시험\n'))
        পৰীক্ষণ_পিক্সেল((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_প্ৰেৰণ_কৰক('q'))
        # 게스트 javac의 সমর্থন_মান 문법으로 মাপ কুৱেৰী_মান·지우기·다섯 인수 그리기를 컴파일한다.
        উৎস = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.নিৰ্গম.লিখক_লাইন("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        আপল_ড_কৰক_ফাইলসমূহ('해상도시험.java', উৎস.encode())
        পৰিমাপ = শ্বেল('javac 해상도시험.java'); assert 'exit 0' in পৰিমাপ, পৰিমাপ
        기다리기(b'JAVA RESOLUTION PASS', SMS_প্ৰেৰণ_কৰক('java 해상도시험\n'))
        পৰীক্ষণ_পিক্সেল((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_প্ৰেৰণ_কৰক('q'))
        আপল_ড_কৰক_ফাইলসমূহ('스윙시험.class', (পৰিমাপ_পথ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_প্ৰেৰণ_কৰক('java 스윙시험\n'))
        가로, উলম্ব_স্থান_সলনি_কৰক = (너비-400)//2, (높이-280)//2
        অংকন_মান = পৰীক্ষণ_পিক্সেল((가로, উলম্ব_স্থান_সলনি_কৰক), (32, 80, 144))
        অংকন_মান.save(str(পৰিমাপ_পথ/(আকাৰ_কৰক_পাঠ+'.png')))
        সঞ্চালন = len(লগ_শাৰী); ক্লিক_কৰক_মান(가로+80, উলম্ব_স্থান_সলনি_কৰক+155)
        기다리기('SWING CLICK নাম'.encode(), সঞ্চালন)
        সঞ্চালন = len(লগ_শাৰী); ক্লিক_কৰক_মান(가로+385, উলম্ব_স্থান_সলনি_কৰক+15); 기다리기(b'jkoros-native> ', সঞ্চালন)
        assert 'AFTER_RESOLUTION' in শ্বেল('echo AFTER_RESOLUTION')
        print('PASS:', আকাৰ_কৰক_পাঠ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if স্থানান্তৰণ_মান: স্থানান্তৰণ_মান.close()
        if দূৰবৰ্তী_মান: দূৰবৰ্তী_মান.close()
        if প্ৰক্ৰিয়া_মান.poll() is None:
            প্ৰক্ৰিয়া_মান.terminate()
            try: প্ৰক্ৰিয়া_মান.wait(timeout=8)
            except subprocess.TimeoutExpired: প্ৰক্ৰিয়া_মান.kill(); প্ৰক্ৰিয়া_মান.wait()
        চয়নকাৰী_a916db4e.close(); প্ৰক্ৰিয়া_মান.stdout.close()
        (পৰিমাপ_পথ/(আকাৰ_কৰক_পাঠ+'.log')).write_bytes(লগ_শাৰী)


def সঞ্চালন():
    পৰিমাপ_পথ = 기준/'build/verification/resolution'; পৰিমাপ_পথ.mkdir(parents=True, exist_ok=True)
    লগ_শাৰী = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for অবৈধ_মান in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            পৰিমাপ = subprocess.run(['python3', str(기준/'সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py'), '--resolution', অবৈধ_মান], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert পৰিমাপ.returncode == 2 and b'--resolution' in পৰিমাপ.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(পৰিমাপ_পথ), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, পৰিমাপ_পথ); লগ_শাৰী['resolutions'].append([너비, 높이])
        লগ_শাৰী.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (পৰিমাপ_পথ/'report.json').write_text(json.dumps(লগ_শাৰী, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': সঞ্চালন()
