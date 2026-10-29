#!/usr/bin/env python3
"""प्रत्यक्ष_डेटा QEMU/VNC에서 화면 आवाठ·경계·विंडो हालोवचें_मोल·Swing·언어별 그리기를 검사한다."""
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
from डॅस्कटॉप_दृश्य import EXACT_मोल
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट


def 해상도시험(너비, 높이, मेजप_पाथ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    आवाठ_SMS = '{}x{}'.format(너비, 높이)
    प्रक्रिया_मोल = subprocess.Popen(['python3', str(प्रॉजॅक्ट_रूट/'साधनां/पाळो_दिवचो_आदेश.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', आवाठ_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    वेंचक_a916db4e = selectors.DefaultSelector(); वेंचक_a916db4e.register(प्रक्रिया_मोल.stdout, selectors.EVENT_READ)
    LOG_नोंद = bytearray(); दुर्मीळ_मोल = None; ट्रान्सफर_मोल = None

    def 기다리기(शो_मोल, चलोवप=0):
        마감 = time.monotonic() + 60
        while शो_मोल not in LOG_नोंद[चलोवप:]:
            if time.monotonic() > 마감 or प्रक्रिया_मोल.poll() is not None or b'HALTED' in LOG_नोंद or b'PANIC:' in LOG_नोंद:
                raise AssertionError(LOG_नोंद[चलोवप:].decode('utf-8', 'replace'))
            for प्रसंग, _ in वेंचक_a916db4e.select(.1):
                डेटा = प्रसंग.fileobj.read(65536)
                if डेटा: LOG_नोंद.extend(डेटा)
        return LOG_नोंद[चलोवप:].decode('utf-8', 'replace')

    def क्लिक_करचें_बटन(चिन्न, 눌림=True): दुर्मीळ_मोल.sendall(struct.pack('>BBHI', 4, int(눌림), 0, चिन्न))

    def SMS_धाडचो(SMS):
        चलोवप = len(LOG_नोंद)
        for वर्ण_मोल in SMS:
            चिन्न = 0xff0d if वर्ण_मोल == '\n' else ord(वर्ण_मोल) if ord(वर्ण_मोल) < 256 else 0x1000000 | ord(वर्ण_मोल)
            क्लिक_करचें_बटन(चिन्न); क्लिक_करचें_बटन(चिन्न, False)
        return चलोवप

    def शॅल(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_धाडचो(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, उबें_स्थिती, 눌림): दुर्मीळ_मोल.sendall(struct.pack('>BBHH', 5, 눌림, 가로, उबें_स्थिती))

    def क्लिक_करचें_मोल(가로, उबें_स्थिती): 가리키기(가로, उबें_स्थिती, 1); 가리키기(가로, उबें_स्थिती, 0)

    def बिटमॅप_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 प्रत्यक्ष_डेटा 너비를 쓴다.
        दुर्मीळ_मोल.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        रेखाटन_मोल = Image.new('RGB', (너비, 높이)); वर्ग_मोल_9285603e = 0
        while True:
            종류 = EXACT_मोल(दुर्मीळ_मोल, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                लांबाय_मोल = struct.unpack('>I', EXACT_मोल(दुर्मीळ_मोल, 7)[3:])[0]; EXACT_मोल(दुर्मीळ_मोल, लांबाय_मोल); continue
            assert 종류 == 0, 종류
            आयटम_COUNT = struct.unpack('>H', EXACT_मोल(दुर्मीळ_मोल, 3)[1:])[0]
            for _ in range(आयटम_COUNT):
                가로, उबें_स्थिती, 폭, लांबाय_मोल, एनकोडिंग_मोल = struct.unpack('>HHHHi', EXACT_मोल(दुर्मीळ_मोल, 12))
                assert एनकोडिंग_मोल == 0 and 가로+폭 <= 너비 and उबें_स्थिती+लांबाय_मोल <= 높이
                रेखाटन_मोल.paste(Image.frombytes('RGB', (폭, लांबाय_मोल), EXACT_मोल(दुर्मीळ_मोल, 폭*लांबाय_मोल*4), 'raw', 'BGRX'), (가로, उबें_स्थिती))
                वर्ग_मोल_9285603e += 폭*लांबाय_मोल
            if वर्ग_मोल_9285603e:
                assert वर्ग_मोल_9285603e == 너비*높이, वर्ग_मोल_9285603e
                return रेखाटन_मोल

    def तपासचें_पिक्सॅल(कोऑर्डिनेट_मोल, 색):
        마감 = time.monotonic()+10
        while True:
            रेखाटन_मोल = बिटमॅप_IMAGE()
            if रेखाटन_मोल.getpixel(कोऑर्डिनेट_मोल) == 색: return रेखाटन_मोल
            if time.monotonic() > 마감: raise AssertionError((कोऑर्डिनेट_मोल, रेखाटन_मोल.getpixel(कोऑर्डिनेट_मोल), 색))

    def अपलोड_करचें_फायली(नांव, डेटा): ट्रान्सफर_मोल.storbinary('STOR '+नांव, io.BytesIO(डेटा))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+आवाठ_SMS+' RGB32').encode() in LOG_नोंद
        print('BOOT:', आवाठ_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_नोंद).group(1))
        दुर्मीळ_मोल = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_मोल(दुर्मीळ_मोल, 12) == b'RFB 003.008\n'; दुर्मीळ_मोल.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_मोल(दुर्मीळ_मोल, EXACT_मोल(दुर्मीळ_मोल, 1)[0]); दुर्मीळ_मोल.sendall(b'\x01')
        assert EXACT_मोल(दुर्मीळ_मोल, 4) == b'\0'*4; दुर्मीळ_मोल.sendall(b'\x01')
        초기 = EXACT_मोल(दुर्मीळ_मोल, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_मोल(दुर्मीळ_मोल, struct.unpack('>I', 초기[20:])[0])
        दुर्मीळ_मोल.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        दुर्मीळ_मोल.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        तपासचें_पिक्सॅल((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        तपासचें_पिक्सॅल((너비-568, 높이-360), (32, 80, 144))
        चलोवप = len(LOG_नोंद); क्लिक_करचें_मोल(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', चलोवप)
        तपासचें_पिक्सॅल((너비-568, 높이-360), (24, 32, 48))
        चलोवप = len(LOG_नोंद); क्लिक_करचें_मोल(80, 16); 기다리기(b'TERMINAL FOCUS 1', चलोवप)
        शॅल('ftpd start')
        ट्रान्सफर_मोल = ftplib.FTP(); ट्रान्सफर_मोल.encoding = 'utf-8'; ट्रान्सफर_मोल.connect('127.0.0.1', 접속번호, timeout=20); ट्रान्सफर_मोल.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_मोल·क्लिप 밖·빈 사각형을 포함한다.
        स्त्रोत = '''#include <화면규약.h>
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
    बरोवचें_फायल_डेटा(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        अपलोड_करचें_फायली('화면시험.c', स्त्रोत.encode())
        assert 'exit 0' in शॅल('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_धाडचो('run /화면시험\n'))
        तपासचें_पिक्सॅल((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_धाडचो('q'))
        स्त्रोत = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, प्रणाली_चूक
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except प्रणाली_चूक as चूक:
    assert चूक.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        अपलोड_करचें_फायली('화면시험.py', स्त्रोत.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_धाडचो('python /화면시험.py\n'))
        तपासचें_पिक्सॅल((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_धाडचो('q'))
        स्त्रोत = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("आवाठ");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("क्लिप"); }
        catch (잘못된인수예외 चूक) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 येजमान javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = मेजप_पाथ/'해상도경계시험.java'
        경계원문.write_text(स्त्रोत.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(प्रॉजॅक्ट_रूट/'dist/jkoros-native-korean.jar'), '-d', str(मेजप_पाथ), str(경계원문)])
        अपलोड_करचें_फायली('해상도경계시험.class', (मेजप_पाथ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_धाडचो('java 해상도경계시험\n'))
        तपासचें_पिक्सॅल((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_धाडचो('q'))
        # 게스트 javac의 तेंको_मोल 문법으로 आवाठ क्वॅरी_मोल·지우기·다섯 인수 그리기를 컴파일한다.
        स्त्रोत = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.बरोवचें_रेग("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        अपलोड_करचें_फायली('해상도시험.java', स्त्रोत.encode())
        मेजप = शॅल('javac 해상도시험.java'); assert 'exit 0' in मेजप, मेजप
        기다리기(b'JAVA RESOLUTION PASS', SMS_धाडचो('java 해상도시험\n'))
        तपासचें_पिक्सॅल((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_धाडचो('q'))
        अपलोड_करचें_फायली('스윙시험.class', (मेजप_पाथ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_धाडचो('java 스윙시험\n'))
        가로, उबें_स्थिती = (너비-400)//2, (높이-280)//2
        रेखाटन_मोल = तपासचें_पिक्सॅल((가로, उबें_स्थिती), (32, 80, 144))
        रेखाटन_मोल.save(str(मेजप_पाथ/(आवाठ_SMS+'.png')))
        चलोवप = len(LOG_नोंद); क्लिक_करचें_मोल(가로+80, उबें_स्थिती+155)
        기다리기('SWING CLICK नांव'.encode(), चलोवप)
        चलोवप = len(LOG_नोंद); क्लिक_करचें_मोल(가로+385, उबें_स्थिती+15); 기다리기(b'jkoros-native> ', चलोवप)
        assert 'AFTER_RESOLUTION' in शॅल('echo AFTER_RESOLUTION')
        print('PASS:', आवाठ_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ट्रान्सफर_मोल: ट्रान्सफर_मोल.close()
        if दुर्मीळ_मोल: दुर्मीळ_मोल.close()
        if प्रक्रिया_मोल.poll() is None:
            प्रक्रिया_मोल.terminate()
            try: प्रक्रिया_मोल.wait(timeout=8)
            except subprocess.TimeoutExpired: प्रक्रिया_मोल.kill(); प्रक्रिया_मोल.wait()
        वेंचक_a916db4e.close(); प्रक्रिया_मोल.stdout.close()
        (मेजप_पाथ/(आवाठ_SMS+'.log')).write_bytes(LOG_नोंद)


def चलोवप():
    मेजप_पाथ = प्रॉजॅक्ट_रूट/'build/verification/resolution'; मेजप_पाथ.mkdir(parents=True, exist_ok=True)
    LOG_नोंद = {'passed': False, 'kernel_sha256': hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for अवैध_मोल in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            मेजप = subprocess.run(['python3', str(प्रॉजॅक्ट_रूट/'साधनां/पाळो_दिवचो_आदेश.py'), '--resolution', अवैध_मोल], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert मेजप.returncode == 2 and b'--resolution' in मेजप.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(मेजप_पाथ), str(प्रॉजॅक्ट_रूट/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, मेजप_पाथ); LOG_नोंद['resolutions'].append([너비, 높이])
        LOG_नोंद.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (मेजप_पाथ/'report.json').write_text(json.dumps(LOG_नोंद, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': चलोवप()
