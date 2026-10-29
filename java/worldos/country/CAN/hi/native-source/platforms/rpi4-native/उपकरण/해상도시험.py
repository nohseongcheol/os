#!/usr/bin/env python3
"""वास्तविक_डेटा QEMU/VNC에서 화면 आकार·경계·खिड़की ले_जाएँ_मान·Swing·언어별 그리기를 검사한다."""
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
from डेस्कटॉप_दृश्य import 정확한값
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल


def 해상도시험(너비, 높이, परिणाम_पथ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); पोर्ट_संख्या = 임시.getsockname()[1]
    आकार_पाठ = '{}x{}'.format(너비, 높이)
    प्रक्रिया_मान = subprocess.Popen(['python3', str(प्रोजेक्ट_करें_मूल/'उपकरण/निष्पादित_करें_आदेश.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(पोर्ट_संख्या), '--resolution', आकार_पाठ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    सिलेक्टर_a916db4e = selectors.DefaultSelector(); सिलेक्टर_a916db4e.register(प्रक्रिया_मान.stdout, selectors.EVENT_READ)
    लॉग_रिकॉर्ड = bytearray(); दूरस्थ_मान = None; हस्तांतरण_मान = None

    def 기다리기(शो_मान, चलाएँ=0):
        अंति_म_समय_सीमा_मान = time.monotonic() + 60
        while शो_मान not in लॉग_रिकॉर्ड[चलाएँ:]:
            if time.monotonic() > अंति_म_समय_सीमा_मान or प्रक्रिया_मान.poll() is not None or b'HALTED' in लॉग_रिकॉर्ड or b'PANIC:' in लॉग_रिकॉर्ड:
                raise AssertionError(लॉग_रिकॉर्ड[चलाएँ:].decode('utf-8', 'replace'))
            for घटना, _ in सिलेक्टर_a916db4e.select(.1):
                आँकड़े = घटना.fileobj.read(65536)
                if आँकड़े: लॉग_रिकॉर्ड.extend(आँकड़े)
        return लॉग_रिकॉर्ड[चलाएँ:].decode('utf-8', 'replace')

    def क्लिक_करना_बटन(प्रतीक, 눌림=True): दूरस्थ_मान.sendall(struct.pack('>BBHI', 4, int(눌림), 0, प्रतीक))

    def SMS_भेजें(पाठ):
        चलाएँ = len(लॉग_रिकॉर्ड)
        for कैरेक्टर_मान in पाठ:
            प्रतीक = 0xff0d if कैरेक्टर_मान == '\n' else ord(कैरेक्टर_मान) if ord(कैरेक्टर_मान) < 256 else 0x1000000 | ord(कैरेक्टर_मान)
            क्लिक_करना_बटन(प्रतीक); क्लिक_करना_बटन(प्रतीक, False)
        return चलाएँ

    def शेल(पाठ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_भेजें(पाठ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, अनुलंब_पद, 눌림): दूरस्थ_मान.sendall(struct.pack('>BBHH', 5, 눌림, 가로, अनुलंब_पद))

    def क्लिक_करना_मान(가로, अनुलंब_पद): 가리키기(가로, अनुलंब_पद, 1); 가리키기(가로, अनुलंब_पद, 0)

    def बिटमैप_छवि():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 वास्तविक_डेटा 너비를 쓴다.
        दूरस्थ_मान.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ड्रॉइंग_मान = Image.new('RGB', (너비, 높이)); क्षेत्र_मान_9285603e = 0
        while True:
            종류 = 정확한값(दूरस्थ_मान, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', 정확한값(दूरस्थ_मान, 7)[3:])[0]; 정확한값(दूरस्थ_मान, 길이); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(दूरस्थ_मान, 3)[1:])[0]
            for _ in range(개수):
                가로, अनुलंब_पद, 폭, 길이, एन्कोडिंग_मान = struct.unpack('>HHHHi', 정확한값(दूरस्थ_मान, 12))
                assert एन्कोडिंग_मान == 0 and 가로+폭 <= 너비 and अनुलंब_पद+길이 <= 높이
                ड्रॉइंग_मान.paste(Image.frombytes('RGB', (폭, 길이), 정확한값(दूरस्थ_मान, 폭*길이*4), 'raw', 'BGRX'), (가로, अनुलंब_पद))
                क्षेत्र_मान_9285603e += 폭*길이
            if क्षेत्र_मान_9285603e:
                assert क्षेत्र_मान_9285603e == 너비*높이, क्षेत्र_मान_9285603e
                return ड्रॉइंग_मान

    def जाँचें_पिक्सेल(좌표, 색):
        अंति_म_समय_सीमा_मान = time.monotonic()+10
        while True:
            ड्रॉइंग_मान = बिटमैप_छवि()
            if ड्रॉइंग_मान.getpixel(좌표) == 색: return ड्रॉइंग_मान
            if time.monotonic() > अंति_म_समय_सीमा_मान: raise AssertionError((좌표, ड्रॉइंग_मान.getpixel(좌표), 색))

    def अपलोड_फ़ाइलें(नाम, आँकड़े): हस्तांतरण_मान.storbinary('STOR '+नाम, io.BytesIO(आँकड़े))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+आकार_पाठ+' RGB32').encode() in लॉग_रिकॉर्ड
        print('BOOT:', आकार_पाठ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', लॉग_रिकॉर्ड).group(1))
        दूरस्थ_मान = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(दूरस्थ_मान, 12) == b'RFB 003.008\n'; दूरस्थ_मान.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(दूरस्थ_मान, 정확한값(दूरस्थ_मान, 1)[0]); दूरस्थ_मान.sendall(b'\x01')
        assert 정확한값(दूरस्थ_मान, 4) == b'\0'*4; दूरस्थ_मान.sendall(b'\x01')
        प्रारंभिक_स्थिति = 정확한값(दूरस्थ_मान, 24); assert struct.unpack('>HH', प्रारंभिक_स्थिति[:4]) == (너비, 높이)
        정확한값(दूरस्थ_मान, struct.unpack('>I', प्रारंभिक_स्थिति[20:])[0])
        दूरस्थ_मान.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        दूरस्थ_मान.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        जाँचें_पिक्सेल((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        जाँचें_पिक्सेल((너비-568, 높이-360), (32, 80, 144))
        चलाएँ = len(लॉग_रिकॉर्ड); क्लिक_करना_मान(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', चलाएँ)
        जाँचें_पिक्सेल((너비-568, 높이-360), (24, 32, 48))
        चलाएँ = len(लॉग_रिकॉर्ड); क्लिक_करना_मान(80, 16); 기다리기(b'TERMINAL FOCUS 1', चलाएँ)
        शेल('ftpd start')
        हस्तांतरण_मान = ftplib.FTP(); हस्तांतरण_मान.encoding = 'utf-8'; हस्तांतरण_मान.connect('127.0.0.1', पोर्ट_संख्या, timeout=20); हस्तांतरण_मान.login()
        # C 경계 검사는 32비트 unsigned 음수 रूपांतरित_करें_मान·क्लिप 밖·빈 사각형을 포함한다.
        स्रोत = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(आरेखित_करना_रेक्_टेंगल(너비,높이,0,0,0)) return 2;
    if(आरेखित_करना_रेक्_टेंगल(너비,높이-1,1,1,0)!=-22) return 3;
    if(आरेखित_करना_रेक्_टेंगल(너비-1,높이,1,1,0)!=-22) return 4;
    if(आरेखित_करना_रेक्_टेंगल(-1,0,1,1,0)!=-22) return 5;
    if(आरेखित_करना_रेक्_टेंगल(0,0,-1,1,0)!=-22) return 6;
    if(आरेखित_करना_रेक्_टेंगल(너비-1,높이-1,1,1,0x332211)) return 7;
    लिखना_फ़ाइल_डेटा(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        अपलोड_फ़ाइलें('화면시험.c', स्रोत.encode())
        assert 'exit 0' in शेल('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_भेजें('run /화면시험\n'))
        जाँचें_पिक्सेल((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_भेजें('q'))
        स्रोत = '''from हिंदी import 화면크기, आरेखित_करना_रेक्_टेंगल, 그림기다리기, निर्गम, सिस्टम_त्रुटि
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    आरेखित_करना_रेक्_टेंगल(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except सिस्टम_त्रुटि as त्रुटि:
    assert त्रुटि.इंडेक्स == 22
आरेखित_करना_रेक्_टेंगल(너비-1, 높이-1, 1, 1, 0x665544)
निर्गम("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        अपलोड_फ़ाइलें('화면시험.py', स्रोत.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_भेजें('python /화면시험.py\n'))
        जाँचें_पिक्सेल((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_भेजें('q'))
        स्रोत = '''import हिंदी.निज.*;
public class 해상도시험 {
    public static void main(String[] तर्क) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new अवस्था_अपवाद("आकार");
        try { 화면.रेक्_टेंगल(너비,높이-1,1,1,0); throw new अवस्था_अपवाद("क्लिप"); }
        catch (अमान्य_तर्क_अपवाद त्रुटि) { }
        화면.मिटाएँ_एन्ट्री(0x302018);
        화면.रेक्_टेंगल(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # अपवाद 처리는 आयोजक javac 결과를 निज JVM에 올려 검사한다.
        경계원문 = परिणाम_पथ/'해상도경계시험.java'
        경계원문.write_text(स्रोत.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(प्रोजेक्ट_करें_मूल/'dist/jkoros-native-korean.jar'), '-d', str(परिणाम_पथ), str(경계원문)])
        अपलोड_फ़ाइलें('해상도경계시험.class', (परिणाम_पथ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_भेजें('java 해상도경계시험\n'))
        जाँचें_पिक्सेल((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_भेजें('q'))
        # 게스트 javac의 समर्थन_मान 문법으로 आकार क्वेरी_मान·मिटाएँ_एन्ट्री·다섯 तर्क 그리기를 컴파일한다.
        स्रोत = '''public class 해상도시험 {
    public static void main(String[] तर्क) {
        int 너비=हिंदी.निज.화면.너비();
        int 높이=हिंदी.निज.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        हिंदी.निज.화면.मिटाएँ_एन्ट्री(3153944);
        हिंदी.निज.화면.रेक्_टेंगल(너비-1,높이-1,1,1,10061943);
        हिंदी.निज.निर्गम.लिखना_लाइन("JAVA RESOLUTION PASS");
        हिंदी.निज.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        अपलोड_फ़ाइलें('해상도시험.java', स्रोत.encode())
        परिणाम = शेल('javac 해상도시험.java'); assert 'exit 0' in परिणाम, परिणाम
        기다리기(b'JAVA RESOLUTION PASS', SMS_भेजें('java 해상도시험\n'))
        जाँचें_पिक्सेल((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_भेजें('q'))
        अपलोड_फ़ाइलें('스윙시험.class', (परिणाम_पथ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_भेजें('java 스윙시험\n'))
        가로, अनुलंब_पद = (너비-400)//2, (높이-280)//2
        ड्रॉइंग_मान = जाँचें_पिक्सेल((가로, अनुलंब_पद), (32, 80, 144))
        ड्रॉइंग_मान.save(str(परिणाम_पथ/(आकार_पाठ+'.png')))
        चलाएँ = len(लॉग_रिकॉर्ड); क्लिक_करना_मान(가로+80, अनुलंब_पद+155)
        기다리기('SWING CLICK नाम'.encode(), चलाएँ)
        चलाएँ = len(लॉग_रिकॉर्ड); क्लिक_करना_मान(가로+385, अनुलंब_पद+15); 기다리기(b'jkoros-native> ', चलाएँ)
        assert 'AFTER_RESOLUTION' in शेल('echo AFTER_RESOLUTION')
        print('PASS:', आकार_पाठ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if हस्तांतरण_मान: हस्तांतरण_मान.close()
        if दूरस्थ_मान: दूरस्थ_मान.close()
        if प्रक्रिया_मान.poll() is None:
            प्रक्रिया_मान.terminate()
            try: प्रक्रिया_मान.wait(timeout=8)
            except subprocess.TimeoutExpired: प्रक्रिया_मान.kill(); प्रक्रिया_मान.wait()
        सिलेक्टर_a916db4e.close(); प्रक्रिया_मान.stdout.close()
        (परिणाम_पथ/(आकार_पाठ+'.log')).write_bytes(लॉग_रिकॉर्ड)


def चलाएँ():
    परिणाम_पथ = प्रोजेक्ट_करें_मूल/'build/verification/resolution'; परिणाम_पथ.mkdir(parents=True, exist_ok=True)
    लॉग_रिकॉर्ड = {'passed': False, 'kernel_sha256': hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for अमान्य_मान in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            परिणाम = subprocess.run(['python3', str(प्रोजेक्ट_करें_मूल/'उपकरण/निष्पादित_करें_आदेश.py'), '--resolution', अमान्य_मान], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert परिणाम.returncode == 2 and b'--resolution' in परिणाम.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(परिणाम_पथ), str(प्रोजेक्ट_करें_मूल/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, परिणाम_पथ); लॉग_रिकॉर्ड['resolutions'].append([너비, 높이])
        लॉग_रिकॉर्ड.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (परिणाम_पथ/'report.json').write_text(json.dumps(लॉग_रिकॉर्ड, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': चलाएँ()
