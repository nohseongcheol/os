#!/usr/bin/env python3
"""वास्तविक_लगत QEMU/VNC에서 화면 आकार·경계·सन्झ्याल लैजानुहोस्_मान·Swing·언어별 그리기를 검사한다."""
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
from डेस्कटप_दृश्य import 정확한값
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट


def 해상도시험(너비, 높이, मापन_बाटो):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    साइज_पाठ = '{}x{}'.format(너비, 높이)
    प्रक्रिया_मान = subprocess.Popen(['python3', str(परियोजना_रूट/'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', साइज_पाठ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    चयनकर्ता_a916db4e = selectors.DefaultSelector(); चयनकर्ता_a916db4e.register(प्रक्रिया_मान.stdout, selectors.EVENT_READ)
    लग_रेकर्ड = bytearray(); दूर_मान = None; ट्रान्सफर_मान = None

    def 기다리기(शो_मान, चलाउनुहोस्=0):
        마감 = time.monotonic() + 60
        while शो_मान not in लग_रेकर्ड[चलाउनुहोस्:]:
            if time.monotonic() > 마감 or प्रक्रिया_मान.poll() is not None or b'HALTED' in लग_रेकर्ड or b'PANIC:' in लग_रेकर्ड:
                raise AssertionError(लग_रेकर्ड[चलाउनुहोस्:].decode('utf-8', 'replace'))
            for घटना, _ in चयनकर्ता_a916db4e.select(.1):
                लगत = घटना.fileobj.read(65536)
                if लगत: लग_रेकर्ड.extend(लगत)
        return लग_रेकर्ड[चलाउनुहोस्:].decode('utf-8', 'replace')

    def क्लिक_गर्नुहोस्_बटन(चिन्ह, 눌림=True): दूर_मान.sendall(struct.pack('>BBHI', 4, int(눌림), 0, चिन्ह))

    def SMS_पठाउनुहोस्(पाठ):
        चलाउनुहोस् = len(लग_रेकर्ड)
        for वर्ण_मान in पाठ:
            चिन्ह = 0xff0d if वर्ण_मान == '\n' else ord(वर्ण_मान) if ord(वर्ण_मान) < 256 else 0x1000000 | ord(वर्ण_मान)
            क्लिक_गर्नुहोस्_बटन(चिन्ह); क्लिक_गर्नुहोस्_बटन(चिन्ह, False)
        return चलाउनुहोस्

    def शेल(पाठ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_पठाउनुहोस्(पाठ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, ठाडो_राख्नुहोस्, 눌림): दूर_मान.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ठाडो_राख्नुहोस्))

    def क्लिक_गर्नुहोस्_मान(가로, ठाडो_राख्नुहोस्): 가리키기(가로, ठाडो_राख्नुहोस्, 1); 가리키기(가로, ठाडो_राख्नुहोस्, 0)

    def बिटम्याप_छवि():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 वास्तविक_लगत 너비를 쓴다.
        दूर_मान.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        चित्रकारी_मान = Image.new('RGB', (너비, 높이)); कोटी_मान = 0
        while True:
            종류 = 정확한값(दूर_मान, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                लम्बाइ_मान = struct.unpack('>I', 정확한값(दूर_मान, 7)[3:])[0]; 정확한값(दूर_मान, लम्बाइ_मान); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(दूर_मान, 3)[1:])[0]
            for _ in range(개수):
                가로, ठाडो_राख्नुहोस्, 폭, लम्बाइ_मान, एनकोडिङ_मान = struct.unpack('>HHHHi', 정확한값(दूर_मान, 12))
                assert एनकोडिङ_मान == 0 and 가로+폭 <= 너비 and ठाडो_राख्नुहोस्+लम्बाइ_मान <= 높이
                चित्रकारी_मान.paste(Image.frombytes('RGB', (폭, लम्बाइ_मान), 정확한값(दूर_मान, 폭*लम्बाइ_मान*4), 'raw', 'BGRX'), (가로, ठाडो_राख्नुहोस्))
                कोटी_मान += 폭*लम्बाइ_मान
            if कोटी_मान:
                assert कोटी_मान == 너비*높이, कोटी_मान
                return चित्रकारी_मान

    def चेक_पेल(समन्वित_मान, 색):
        마감 = time.monotonic()+10
        while True:
            चित्रकारी_मान = बिटम्याप_छवि()
            if चित्रकारी_मान.getpixel(समन्वित_मान) == 색: return चित्रकारी_मान
            if time.monotonic() > 마감: raise AssertionError((समन्वित_मान, चित्रकारी_मान.getpixel(समन्वित_मान), 색))

    def अपलोड_गर्नुहोस्_फाइलहरू(नाम, लगत): ट्रान्सफर_मान.storbinary('STOR '+नाम, io.BytesIO(लगत))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+साइज_पाठ+' RGB32').encode() in लग_रेकर्ड
        print('BOOT:', साइज_पाठ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', लग_रेकर्ड).group(1))
        दूर_मान = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(दूर_मान, 12) == b'RFB 003.008\n'; दूर_मान.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(दूर_मान, 정확한값(दूर_मान, 1)[0]); दूर_मान.sendall(b'\x01')
        assert 정확한값(दूर_मान, 4) == b'\0'*4; दूर_मान.sendall(b'\x01')
        초기 = 정확한값(दूर_मान, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(दूर_मान, struct.unpack('>I', 초기[20:])[0])
        दूर_मान.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        दूर_मान.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        चेक_पेल((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        चेक_पेल((너비-568, 높이-360), (32, 80, 144))
        चलाउनुहोस् = len(लग_रेकर्ड); क्लिक_गर्नुहोस्_मान(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', चलाउनुहोस्)
        चेक_पेल((너비-568, 높이-360), (24, 32, 48))
        चलाउनुहोस् = len(लग_रेकर्ड); क्लिक_गर्नुहोस्_मान(80, 16); 기다리기(b'TERMINAL FOCUS 1', चलाउनुहोस्)
        शेल('ftpd start')
        ट्रान्सफर_मान = ftplib.FTP(); ट्रान्सफर_मान.encoding = 'utf-8'; ट्रान्सफर_मान.connect('127.0.0.1', 접속번호, timeout=20); ट्रान्सफर_मान.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·क्लिप 밖·빈 사각형을 포함한다.
        स्रोत = '''#include <화면규약.h>
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
    लेख्नुहोस्_फाइल_लगत(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        अपलोड_गर्नुहोस्_फाइलहरू('화면시험.c', स्रोत.encode())
        assert 'exit 0' in शेल('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_पठाउनुहोस्('run /화면시험\n'))
        चेक_पेल((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_पठाउनुहोस्('q'))
        स्रोत = '''from नेपाली import 화면크기, 네모그리기, 그림기다리기, 출력, प्रणाली_त्रुटि
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except प्रणाली_त्रुटि as त्रुटि:
    assert त्रुटि.अनुक्रमणिका == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        अपलोड_गर्नुहोस्_फाइलहरू('화면시험.py', स्रोत.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_पठाउनुहोस्('python /화면시험.py\n'))
        चेक_पेल((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_पठाउनुहोस्('q'))
        स्रोत = '''import नेपाली.निज.*;
public class 해상도시험 {
    public static void main(String[] तर्क) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("आकार");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("क्लिप"); }
        catch (잘못된인수예외 त्रुटि) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 होस्ट javac 결과를 निज JVM에 올려 검사한다.
        경계원문 = मापन_बाटो/'해상도경계시험.java'
        경계원문.write_text(स्रोत.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(परियोजना_रूट/'dist/jkoros-native-korean.jar'), '-d', str(मापन_बाटो), str(경계원문)])
        अपलोड_गर्नुहोस्_फाइलहरू('해상도경계시험.class', (मापन_बाटो/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_पठाउनुहोस्('java 해상도경계시험\n'))
        चेक_पेल((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_पठाउनुहोस्('q'))
        # 게스트 javac의 समर्थन_मान 문법으로 आकार क्वेरी_मान·지우기·다섯 तर्क 그리기를 컴파일한다.
        स्रोत = '''public class 해상도시험 {
    public static void main(String[] तर्क) {
        int 너비=नेपाली.निज.화면.너비();
        int 높이=नेपाली.निज.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        नेपाली.निज.화면.지우기(3153944);
        नेपाली.निज.화면.사각형(너비-1,높이-1,1,1,10061943);
        नेपाली.निज.출력.लेख्नुहोस्_रेखा("JAVA RESOLUTION PASS");
        नेपाली.निज.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        अपलोड_गर्नुहोस्_फाइलहरू('해상도시험.java', स्रोत.encode())
        मापन = शेल('javac 해상도시험.java'); assert 'exit 0' in मापन, मापन
        기다리기(b'JAVA RESOLUTION PASS', SMS_पठाउनुहोस्('java 해상도시험\n'))
        चेक_पेल((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_पठाउनुहोस्('q'))
        अपलोड_गर्नुहोस्_फाइलहरू('스윙시험.class', (मापन_बाटो/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_पठाउनुहोस्('java 스윙시험\n'))
        가로, ठाडो_राख्नुहोस् = (너비-400)//2, (높이-280)//2
        चित्रकारी_मान = चेक_पेल((가로, ठाडो_राख्नुहोस्), (32, 80, 144))
        चित्रकारी_मान.save(str(मापन_बाटो/(साइज_पाठ+'.png')))
        चलाउनुहोस् = len(लग_रेकर्ड); क्लिक_गर्नुहोस्_मान(가로+80, ठाडो_राख्नुहोस्+155)
        기다리기('SWING CLICK नाम'.encode(), चलाउनुहोस्)
        चलाउनुहोस् = len(लग_रेकर्ड); क्लिक_गर्नुहोस्_मान(가로+385, ठाडो_राख्नुहोस्+15); 기다리기(b'jkoros-native> ', चलाउनुहोस्)
        assert 'AFTER_RESOLUTION' in शेल('echo AFTER_RESOLUTION')
        print('PASS:', साइज_पाठ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ट्रान्सफर_मान: ट्रान्सफर_मान.close()
        if दूर_मान: दूर_मान.close()
        if प्रक्रिया_मान.poll() is None:
            प्रक्रिया_मान.terminate()
            try: प्रक्रिया_मान.wait(timeout=8)
            except subprocess.TimeoutExpired: प्रक्रिया_मान.kill(); प्रक्रिया_मान.wait()
        चयनकर्ता_a916db4e.close(); प्रक्रिया_मान.stdout.close()
        (मापन_बाटो/(साइज_पाठ+'.log')).write_bytes(लग_रेकर्ड)


def चलाउनुहोस्():
    मापन_बाटो = परियोजना_रूट/'build/verification/resolution'; मापन_बाटो.mkdir(parents=True, exist_ok=True)
    लग_रेकर्ड = {'passed': False, 'kernel_sha256': hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for अवैधानिक_मान in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            मापन = subprocess.run(['python3', str(परियोजना_रूट/'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py'), '--resolution', अवैधानिक_मान], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert मापन.returncode == 2 and b'--resolution' in मापन.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(मापन_बाटो), str(परियोजना_रूट/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, मापन_बाटो); लग_रेकर्ड['resolutions'].append([너비, 높이])
        लग_रेकर्ड.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (मापन_बाटो/'report.json').write_text(json.dumps(लग_रेकर्ड, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': चलाउनुहोस्()
