#!/usr/bin/env python3
"""அசல்_தரவு QEMU/VNC에서 화면 அளவு·경계·சாளரம் நகர்த்து_மதிப்பு·Swing·언어별 그리기를 검사한다."""
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
from டெஸ்க்டாப்_காட்சி import 정확한값
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்


def 해상도시험(너비, 높이, அளவிடக்கூடியது_பாதை):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); முனைய_எண் = 임시.getsockname()[1]
    அளவு_உரை = '{}x{}'.format(너비, 높이)
    செயலகம்_மதிப்பு = subprocess.Popen(['python3', str(திட்டப்பணி_மூலம்/'கருவிகள்/இயக்கு_கட்டளை.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(முனைய_எண்), '--resolution', அளவு_உரை], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    தேர்வி_a916db4e = selectors.DefaultSelector(); தேர்வி_a916db4e.register(செயலகம்_மதிப்பு.stdout, selectors.EVENT_READ)
    பதிவு_பதிவு = bytearray(); தொலைநிலை_மதிப்பு = None; இடமாற்று_மதிப்பு = None

    def 기다리기(காட்சி_மதிப்பு_487749b8, செயல்படுத்துக=0):
        마감 = time.monotonic() + 60
        while காட்சி_மதிப்பு_487749b8 not in பதிவு_பதிவு[செயல்படுத்துக:]:
            if time.monotonic() > 마감 or செயலகம்_மதிப்பு.poll() is not None or b'HALTED' in பதிவு_பதிவு or b'PANIC:' in பதிவு_பதிவு:
                raise AssertionError(பதிவு_பதிவு[செயல்படுத்துக:].decode('utf-8', 'replace'))
            for நிகழ்வு, _ in தேர்வி_a916db4e.select(.1):
                தரவு = நிகழ்வு.fileobj.read(65536)
                if தரவு: பதிவு_பதிவு.extend(தரவு)
        return பதிவு_பதிவு[செயல்படுத்துக:].decode('utf-8', 'replace')

    def கிளிக்_செய்_பொத்தான்(சின்னம், 눌림=True): தொலைநிலை_மதிப்பு.sendall(struct.pack('>BBHI', 4, int(눌림), 0, சின்னம்))

    def SMS_அனுப்புக(உரை):
        செயல்படுத்துக = len(பதிவு_பதிவு)
        for எழுத்துக்குறி_மதிப்பு in உரை:
            சின்னம் = 0xff0d if எழுத்துக்குறி_மதிப்பு == '\n' else ord(எழுத்துக்குறி_மதிப்பு) if ord(எழுத்துக்குறி_மதிப்பு) < 256 else 0x1000000 | ord(எழுத்துக்குறி_மதிப்பு)
            கிளிக்_செய்_பொத்தான்(சின்னம்); கிளிக்_செய்_பொத்தான்(சின்னம், False)
        return செயல்படுத்துக

    def கூடு(உரை): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_அனுப்புக(உரை+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, வெர்டிகல்_நிலை, 눌림): தொலைநிலை_மதிப்பு.sendall(struct.pack('>BBHH', 5, 눌림, 가로, வெர்டிகல்_நிலை))

    def கிளிக்_செய்_மதிப்பு(가로, வெர்டிகல்_நிலை): 가리키기(가로, வெர்டிகல்_நிலை, 1); 가리키기(가로, வெர்டிகல்_நிலை, 0)

    def பிட்_வரைபடம்_படம்():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 அசல்_தரவு 너비를 쓴다.
        தொலைநிலை_மதிப்பு.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        வரைதல்_மதிப்பு = Image.new('RGB', (너비, 높이)); வகை_மதிப்பு_9285603e = 0
        while True:
            종류 = 정확한값(தொலைநிலை_மதிப்பு, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                நீளம்_மதிப்பு = struct.unpack('>I', 정확한값(தொலைநிலை_மதிப்பு, 7)[3:])[0]; 정확한값(தொலைநிலை_மதிப்பு, நீளம்_மதிப்பு); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(தொலைநிலை_மதிப்பு, 3)[1:])[0]
            for _ in range(개수):
                가로, வெர்டிகல்_நிலை, 폭, நீளம்_மதிப்பு, குறியீட்டு_முறை_மதிப்பு = struct.unpack('>HHHHi', 정확한값(தொலைநிலை_மதிப்பு, 12))
                assert குறியீட்டு_முறை_மதிப்பு == 0 and 가로+폭 <= 너비 and வெர்டிகல்_நிலை+நீளம்_மதிப்பு <= 높이
                வரைதல்_மதிப்பு.paste(Image.frombytes('RGB', (폭, நீளம்_மதிப்பு), 정확한값(தொலைநிலை_மதிப்பு, 폭*நீளம்_மதிப்பு*4), 'raw', 'BGRX'), (가로, வெர்டிகல்_நிலை))
                வகை_மதிப்பு_9285603e += 폭*நீளம்_மதிப்பு
            if வகை_மதிப்பு_9285603e:
                assert வகை_மதிப்பு_9285603e == 너비*높이, வகை_மதிப்பு_9285603e
                return வரைதல்_மதிப்பு

    def காசோலை_படக்_கூறு(அச்சுத்_தொகுப்பு_மதிப்பு, 색):
        마감 = time.monotonic()+10
        while True:
            வரைதல்_மதிப்பு = பிட்_வரைபடம்_படம்()
            if வரைதல்_மதிப்பு.getpixel(அச்சுத்_தொகுப்பு_மதிப்பு) == 색: return வரைதல்_மதிப்பு
            if time.monotonic() > 마감: raise AssertionError((அச்சுத்_தொகுப்பு_மதிப்பு, வரைதல்_மதிப்பு.getpixel(அச்சுத்_தொகுப்பு_மதிப்பு), 색))

    def பதிவேற்று_கோப்புகள்(பெயர், தரவு): இடமாற்று_மதிப்பு.storbinary('STOR '+பெயர், io.BytesIO(தரவு))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+அளவு_உரை+' RGB32').encode() in பதிவு_பதிவு
        print('BOOT:', அளவு_உரை, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', பதிவு_பதிவு).group(1))
        தொலைநிலை_மதிப்பு = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(தொலைநிலை_மதிப்பு, 12) == b'RFB 003.008\n'; தொலைநிலை_மதிப்பு.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(தொலைநிலை_மதிப்பு, 정확한값(தொலைநிலை_மதிப்பு, 1)[0]); தொலைநிலை_மதிப்பு.sendall(b'\x01')
        assert 정확한값(தொலைநிலை_மதிப்பு, 4) == b'\0'*4; தொலைநிலை_மதிப்பு.sendall(b'\x01')
        초기 = 정확한값(தொலைநிலை_மதிப்பு, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(தொலைநிலை_மதிப்பு, struct.unpack('>I', 초기[20:])[0])
        தொலைநிலை_மதிப்பு.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        தொலைநிலை_மதிப்பு.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        காசோலை_படக்_கூறு((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        காசோலை_படக்_கூறு((너비-568, 높이-360), (32, 80, 144))
        செயல்படுத்துக = len(பதிவு_பதிவு); கிளிக்_செய்_மதிப்பு(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', செயல்படுத்துக)
        காசோலை_படக்_கூறு((너비-568, 높이-360), (24, 32, 48))
        செயல்படுத்துக = len(பதிவு_பதிவு); கிளிக்_செய்_மதிப்பு(80, 16); 기다리기(b'TERMINAL FOCUS 1', செயல்படுத்துக)
        கூடு('ftpd start')
        இடமாற்று_மதிப்பு = ftplib.FTP(); இடமாற்று_மதிப்பு.encoding = 'utf-8'; இடமாற்று_மதிப்பு.connect('127.0.0.1', முனைய_எண், timeout=20); இடமாற்று_மதிப்பு.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·கிளிப் 밖·빈 사각형을 포함한다.
        மூலக்_கோப்பு = '''#include <화면규약.h>
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
    எழுது_கோப்பு_தரவு(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        பதிவேற்று_கோப்புகள்('화면시험.c', மூலக்_கோப்பு.encode())
        assert 'exit 0' in கூடு('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_அனுப்புக('run /화면시험\n'))
        காசோலை_படக்_கூறு((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_அனுப்புக('q'))
        மூலக்_கோப்பு = '''from தமிழ் import 화면크기, 네모그리기, 그림기다리기, வெளியீட்டு_இடம், முறைமை_பிழை
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except முறைமை_பிழை as பிழை:
    assert பிழை.அடைவு == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
வெளியீட்டு_இடம்("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        பதிவேற்று_கோப்புகள்('화면시험.py', மூலக்_கோப்பு.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_அனுப்புக('python /화면시험.py\n'))
        காசோலை_படக்_கூறு((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_அனுப்புக('q'))
        மூலக்_கோப்பு = '''import தமிழ்.자체.*;
public class 해상도시험 {
    public static void main(String[] செயலுருபுகள்) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new நிலை_விதிவிலக்கு("அளவு");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new நிலை_விதிவிலக்கு("கிளிப்"); }
        catch (செல்லுபடியாகாத_மதிப்புரு_விதிவிலக்கு பிழை) { }
        화면.அழி_உள்ளீடு(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # விதிவிலக்கு 처리는 ஓம்பு javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = அளவிடக்கூடியது_பாதை/'해상도경계시험.java'
        경계원문.write_text(மூலக்_கோப்பு.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(திட்டப்பணி_மூலம்/'dist/jkoros-native-korean.jar'), '-d', str(அளவிடக்கூடியது_பாதை), str(경계원문)])
        பதிவேற்று_கோப்புகள்('해상도경계시험.class', (அளவிடக்கூடியது_பாதை/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_அனுப்புக('java 해상도경계시험\n'))
        காசோலை_படக்_கூறு((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_அனுப்புக('q'))
        # 게스트 javac의 ஆதரவு_மதிப்பு 문법으로 அளவு வினவல்_மதிப்பு·அழி_உள்ளீடு·다섯 செயலுருபுகள் 그리기를 컴파일한다.
        மூலக்_கோப்பு = '''public class 해상도시험 {
    public static void main(String[] செயலுருபுகள்) {
        int 너비=தமிழ்.자체.화면.너비();
        int 높이=தமிழ்.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        தமிழ்.자체.화면.அழி_உள்ளீடு(3153944);
        தமிழ்.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        தமிழ்.자체.வெளியீட்டு_இடம்.எழுது_வரி("JAVA RESOLUTION PASS");
        தமிழ்.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        பதிவேற்று_கோப்புகள்('해상도시험.java', மூலக்_கோப்பு.encode())
        அளவிடக்கூடியது = கூடு('javac 해상도시험.java'); assert 'exit 0' in அளவிடக்கூடியது, அளவிடக்கூடியது
        기다리기(b'JAVA RESOLUTION PASS', SMS_அனுப்புக('java 해상도시험\n'))
        காசோலை_படக்_கூறு((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_அனுப்புக('q'))
        பதிவேற்று_கோப்புகள்('스윙시험.class', (அளவிடக்கூடியது_பாதை/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_அனுப்புக('java 스윙시험\n'))
        가로, வெர்டிகல்_நிலை = (너비-400)//2, (높이-280)//2
        வரைதல்_மதிப்பு = காசோலை_படக்_கூறு((가로, வெர்டிகல்_நிலை), (32, 80, 144))
        வரைதல்_மதிப்பு.save(str(அளவிடக்கூடியது_பாதை/(அளவு_உரை+'.png')))
        செயல்படுத்துக = len(பதிவு_பதிவு); கிளிக்_செய்_மதிப்பு(가로+80, வெர்டிகல்_நிலை+155)
        기다리기('SWING CLICK பெயர்'.encode(), செயல்படுத்துக)
        செயல்படுத்துக = len(பதிவு_பதிவு); கிளிக்_செய்_மதிப்பு(가로+385, வெர்டிகல்_நிலை+15); 기다리기(b'jkoros-native> ', செயல்படுத்துக)
        assert 'AFTER_RESOLUTION' in கூடு('echo AFTER_RESOLUTION')
        print('PASS:', அளவு_உரை, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if இடமாற்று_மதிப்பு: இடமாற்று_மதிப்பு.close()
        if தொலைநிலை_மதிப்பு: தொலைநிலை_மதிப்பு.close()
        if செயலகம்_மதிப்பு.poll() is None:
            செயலகம்_மதிப்பு.terminate()
            try: செயலகம்_மதிப்பு.wait(timeout=8)
            except subprocess.TimeoutExpired: செயலகம்_மதிப்பு.kill(); செயலகம்_மதிப்பு.wait()
        தேர்வி_a916db4e.close(); செயலகம்_மதிப்பு.stdout.close()
        (அளவிடக்கூடியது_பாதை/(அளவு_உரை+'.log')).write_bytes(பதிவு_பதிவு)


def செயல்படுத்துக():
    அளவிடக்கூடியது_பாதை = திட்டப்பணி_மூலம்/'build/verification/resolution'; அளவிடக்கூடியது_பாதை.mkdir(parents=True, exist_ok=True)
    பதிவு_பதிவு = {'passed': False, 'kernel_sha256': hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for செல்லுபடியாகாத_மதிப்பு in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            அளவிடக்கூடியது = subprocess.run(['python3', str(திட்டப்பணி_மூலம்/'கருவிகள்/இயக்கு_கட்டளை.py'), '--resolution', செல்லுபடியாகாத_மதிப்பு], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert அளவிடக்கூடியது.returncode == 2 and b'--resolution' in அளவிடக்கூடியது.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(அளவிடக்கூடியது_பாதை), str(திட்டப்பணி_மூலம்/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, அளவிடக்கூடியது_பாதை); பதிவு_பதிவு['resolutions'].append([너비, 높이])
        பதிவு_பதிவு.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (அளவிடக்கூடியது_பாதை/'report.json').write_text(json.dumps(பதிவு_பதிவு, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': செயல்படுத்துக()
