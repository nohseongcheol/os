#!/usr/bin/env python3
"""વાસ્તવિક_ડેટા QEMU/VNC에서 화면 માપ·경계·વિંડો ખસેડવું_મૂલ્ય·Swing·언어별 그리기를 검사한다."""
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
from ડેસ્કટૉપ_જુઓ import 정확한값
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ


def 해상도시험(너비, 높이, પરિમાણ_પાથ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); પોર્ટ_નંબર = 임시.getsockname()[1]
    આકાર_પાઠ = '{}x{}'.format(너비, 높이)
    પ્રક્રિયા_મૂલ્ય = subprocess.Popen(['python3', str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/અમલ_કરો_આદેશ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(પોર્ટ_નંબર), '--resolution', આકાર_પાઠ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    પસંદકર્તા_a916db4e = selectors.DefaultSelector(); પસંદકર્તા_a916db4e.register(પ્રક્રિયા_મૂલ્ય.stdout, selectors.EVENT_READ)
    લૉગ_પંક્તિ = bytearray(); રિમોટ_મૂલ્ય = None; સ્થાનાંતર_મૂલ્ય = None

    def 기다리기(શૉ_મૂલ્ય, ચલાવો_2=0):
        마감 = time.monotonic() + 60
        while શૉ_મૂલ્ય not in લૉગ_પંક્તિ[ચલાવો_2:]:
            if time.monotonic() > 마감 or પ્રક્રિયા_મૂલ્ય.poll() is not None or b'HALTED' in લૉગ_પંક્તિ or b'PANIC:' in લૉગ_પંક્તિ:
                raise AssertionError(લૉગ_પંક્તિ[ચલાવો_2:].decode('utf-8', 'replace'))
            for ઇવેંટ, _ in પસંદકર્તા_a916db4e.select(.1):
                ડેટા = ઇવેંટ.fileobj.read(65536)
                if ડેટા: લૉગ_પંક્તિ.extend(ડેટા)
        return લૉગ_પંક્તિ[ચલાવો_2:].decode('utf-8', 'replace')

    def ક્લિક_કરો_બટન(પ્રતીક, 눌림=True): રિમોટ_મૂલ્ય.sendall(struct.pack('>BBHI', 4, int(눌림), 0, પ્રતીક))

    def SMS_મોકલો(લખાણ):
        ચલાવો_2 = len(લૉગ_પંક્તિ)
        for વર્ણ_મૂલ્ય in લખાણ:
            પ્રતીક = 0xff0d if વર્ણ_મૂલ્ય == '\n' else ord(વર્ણ_મૂલ્ય) if ord(વર્ણ_મૂલ્ય) < 256 else 0x1000000 | ord(વર્ણ_મૂલ્ય)
            ક્લિક_કરો_બટન(પ્રતીક); ક્લિક_કરો_બટન(પ્રતીક, False)
        return ચલાવો_2

    def શેલ(લખાણ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_મોકલો(લખાણ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, ઊભી_સ્થિતિ, 눌림): રિમોટ_મૂલ્ય.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ઊભી_સ્થિતિ))

    def ક્લિક_કરો_મૂલ્ય(가로, ઊભી_સ્થિતિ): 가리키기(가로, ઊભી_સ્થિતિ, 1); 가리키기(가로, ઊભી_સ્થિતિ, 0)

    def બિટમૅપ_છબી():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 વાસ્તવિક_ડેટા 너비를 쓴다.
        રિમોટ_મૂલ્ય.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        રેખાંકન_મૂલ્ય = Image.new('RGB', (너비, 높이)); શ્રેણી_મૂલ્ય_9285603e = 0
        while True:
            종류 = 정확한값(રિમોટ_મૂલ્ય, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                લંબાઈ_મૂલ્ય = struct.unpack('>I', 정확한값(રિમોટ_મૂલ્ય, 7)[3:])[0]; 정확한값(રિમોટ_મૂલ્ય, લંબાઈ_મૂલ્ય); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(રિમોટ_મૂલ્ય, 3)[1:])[0]
            for _ in range(개수):
                가로, ઊભી_સ્થિતિ, 폭, લંબાઈ_મૂલ્ય, એન્કોડિંગ_મૂલ્ય = struct.unpack('>HHHHi', 정확한값(રિમોટ_મૂલ્ય, 12))
                assert એન્કોડિંગ_મૂલ્ય == 0 and 가로+폭 <= 너비 and ઊભી_સ્થિતિ+લંબાઈ_મૂલ્ય <= 높이
                રેખાંકન_મૂલ્ય.paste(Image.frombytes('RGB', (폭, લંબાઈ_મૂલ્ય), 정확한값(રિમોટ_મૂલ્ય, 폭*લંબાઈ_મૂલ્ય*4), 'raw', 'BGRX'), (가로, ઊભી_સ્થિતિ))
                શ્રેણી_મૂલ્ય_9285603e += 폭*લંબાઈ_મૂલ્ય
            if શ્રેણી_મૂલ્ય_9285603e:
                assert શ્રેણી_મૂલ્ય_9285603e == 너비*높이, શ્રેણી_મૂલ્ય_9285603e
                return રેખાંકન_મૂલ્ય

    def તપાસો_પેલ(સુસંગત_બનાવવું_મૂલ્ય, 색):
        마감 = time.monotonic()+10
        while True:
            રેખાંકન_મૂલ્ય = બિટમૅપ_છબી()
            if રેખાંકન_મૂલ્ય.getpixel(સુસંગત_બનાવવું_મૂલ્ય) == 색: return રેખાંકન_મૂલ્ય
            if time.monotonic() > 마감: raise AssertionError((સુસંગત_બનાવવું_મૂલ્ય, રેખાંકન_મૂલ્ય.getpixel(સુસંગત_બનાવવું_મૂલ્ય), 색))

    def અપલોડ_કરો_ફાઇલો(નામ, ડેટા): સ્થાનાંતર_મૂલ્ય.storbinary('STOR '+નામ, io.BytesIO(ડેટા))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+આકાર_પાઠ+' RGB32').encode() in લૉગ_પંક્તિ
        print('BOOT:', આકાર_પાઠ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', લૉગ_પંક્તિ).group(1))
        રિમોટ_મૂલ્ય = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(રિમોટ_મૂલ્ય, 12) == b'RFB 003.008\n'; રિમોટ_મૂલ્ય.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(રિમોટ_મૂલ્ય, 정확한값(રિમોટ_મૂલ્ય, 1)[0]); રિમોટ_મૂલ્ય.sendall(b'\x01')
        assert 정확한값(રિમોટ_મૂલ્ય, 4) == b'\0'*4; રિમોટ_મૂલ્ય.sendall(b'\x01')
        초기 = 정확한값(રિમોટ_મૂલ્ય, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(રિમોટ_મૂલ્ય, struct.unpack('>I', 초기[20:])[0])
        રિમોટ_મૂલ્ય.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        રિમોટ_મૂલ્ય.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        તપાસો_પેલ((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        તપાસો_પેલ((너비-568, 높이-360), (32, 80, 144))
        ચલાવો_2 = len(લૉગ_પંક્તિ); ક્લિક_કરો_મૂલ્ય(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ચલાવો_2)
        તપાસો_પેલ((너비-568, 높이-360), (24, 32, 48))
        ચલાવો_2 = len(લૉગ_પંક્તિ); ક્લિક_કરો_મૂલ્ય(80, 16); 기다리기(b'TERMINAL FOCUS 1', ચલાવો_2)
        શેલ('ftpd start')
        સ્થાનાંતર_મૂલ્ય = ftplib.FTP(); સ્થાનાંતર_મૂલ્ય.encoding = 'utf-8'; સ્થાનાંતર_મૂલ્ય.connect('127.0.0.1', પોર્ટ_નંબર, timeout=20); સ્થાનાંતર_મૂલ્ય.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ક્લિપ 밖·빈 사각형을 포함한다.
        સ્રોત = '''#include <화면규약.h>
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
    લખો_ફાઇલ_ડેટા(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        અપલોડ_કરો_ફાઇલો('화면시험.c', સ્રોત.encode())
        assert 'exit 0' in શેલ('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_મોકલો('run /화면시험\n'))
        તપાસો_પેલ((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_મોકલો('q'))
        સ્રોત = '''from ગુજરાતી import 화면크기, 네모그리기, 그림기다리기, આઉટપુટ, સિસ્ટમ_ભૂલ
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except સિસ્ટમ_ભૂલ as ભૂલ:
    assert ભૂલ.અનુક્રમણિકા == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
આઉટપુટ("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        અપલોડ_કરો_ફાઇલો('화면시험.py', સ્રોત.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_મોકલો('python /화면시험.py\n'))
        તપાસો_પેલ((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_મોકલો('q'))
        સ્રોત = '''import ગુજરાતી.자체.*;
public class 해상도시험 {
    public static void main(String[] દલીલો) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("માપ");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("ક્લિપ"); }
        catch (잘못된인수예외 ભૂલ) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 હોસ્ટ javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = પરિમાણ_પાથ/'해상도경계시험.java'
        경계원문.write_text(સ્રોત.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(પ્રોજેક્ટ_રૂટ/'dist/jkoros-native-korean.jar'), '-d', str(પરિમાણ_પાથ), str(경계원문)])
        અપલોડ_કરો_ફાઇલો('해상도경계시험.class', (પરિમાણ_પાથ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_મોકલો('java 해상도경계시험\n'))
        તપાસો_પેલ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_મોકલો('q'))
        # 게스트 javac의 સપોર્ટ_મૂલ્ય 문법으로 માપ ક્વેરી_મૂલ્ય·지우기·다섯 દલીલો 그리기를 컴파일한다.
        સ્રોત = '''public class 해상도시험 {
    public static void main(String[] દલીલો) {
        int 너비=ગુજરાતી.자체.화면.너비();
        int 높이=ગુજરાતી.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        ગુજરાતી.자체.화면.지우기(3153944);
        ગુજરાતી.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        ગુજરાતી.자체.આઉટપુટ.લખો_લાઇન("JAVA RESOLUTION PASS");
        ગુજરાતી.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        અપલોડ_કરો_ફાઇલો('해상도시험.java', સ્રોત.encode())
        પરિમાણ = શેલ('javac 해상도시험.java'); assert 'exit 0' in પરિમાણ, પરિમાણ
        기다리기(b'JAVA RESOLUTION PASS', SMS_મોકલો('java 해상도시험\n'))
        તપાસો_પેલ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_મોકલો('q'))
        અપલોડ_કરો_ફાઇલો('스윙시험.class', (પરિમાણ_પાથ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_મોકલો('java 스윙시험\n'))
        가로, ઊભી_સ્થિતિ = (너비-400)//2, (높이-280)//2
        રેખાંકન_મૂલ્ય = તપાસો_પેલ((가로, ઊભી_સ્થિતિ), (32, 80, 144))
        રેખાંકન_મૂલ્ય.save(str(પરિમાણ_પાથ/(આકાર_પાઠ+'.png')))
        ચલાવો_2 = len(લૉગ_પંક્તિ); ક્લિક_કરો_મૂલ્ય(가로+80, ઊભી_સ્થિતિ+155)
        기다리기('SWING CLICK નામ'.encode(), ચલાવો_2)
        ચલાવો_2 = len(લૉગ_પંક્તિ); ક્લિક_કરો_મૂલ્ય(가로+385, ઊભી_સ્થિતિ+15); 기다리기(b'jkoros-native> ', ચલાવો_2)
        assert 'AFTER_RESOLUTION' in શેલ('echo AFTER_RESOLUTION')
        print('PASS:', આકાર_પાઠ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if સ્થાનાંતર_મૂલ્ય: સ્થાનાંતર_મૂલ્ય.close()
        if રિમોટ_મૂલ્ય: રિમોટ_મૂલ્ય.close()
        if પ્રક્રિયા_મૂલ્ય.poll() is None:
            પ્રક્રિયા_મૂલ્ય.terminate()
            try: પ્રક્રિયા_મૂલ્ય.wait(timeout=8)
            except subprocess.TimeoutExpired: પ્રક્રિયા_મૂલ્ય.kill(); પ્રક્રિયા_મૂલ્ય.wait()
        પસંદકર્તા_a916db4e.close(); પ્રક્રિયા_મૂલ્ય.stdout.close()
        (પરિમાણ_પાથ/(આકાર_પાઠ+'.log')).write_bytes(લૉગ_પંક્તિ)


def ચલાવો_2():
    પરિમાણ_પાથ = પ્રોજેક્ટ_રૂટ/'build/verification/resolution'; પરિમાણ_પાથ.mkdir(parents=True, exist_ok=True)
    લૉગ_પંક્તિ = {'passed': False, 'kernel_sha256': hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for અમાન્ય_મૂલ્ય in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            પરિમાણ = subprocess.run(['python3', str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/અમલ_કરો_આદેશ.py'), '--resolution', અમાન્ય_મૂલ્ય], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert પરિમાણ.returncode == 2 and b'--resolution' in પરિમાણ.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(પરિમાણ_પાથ), str(પ્રોજેક્ટ_રૂટ/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, પરિમાણ_પાથ); લૉગ_પંક્તિ['resolutions'].append([너비, 높이])
        લૉગ_પંક્તિ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (પરિમાણ_પાથ/'report.json').write_text(json.dumps(લૉગ_પંક્તિ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ચલાવો_2()
