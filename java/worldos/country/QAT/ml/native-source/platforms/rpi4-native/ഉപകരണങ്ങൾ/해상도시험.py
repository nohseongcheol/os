#!/usr/bin/env python3
"""വാസ്തവമായ_ഡാറ്റാ QEMU/VNC에서 화면 വലിപ്പം·경계·ജാലകം നീക്കുക_മൂല്യം·Swing·언어별 그리기를 검사한다."""
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
from ഡെസ്ക്ടോപ്പ്_കാഴ്ച import 정확한값
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം


def 해상도시험(너비, 높이, അളവ്_പാത):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); പോര്_ട്ട്_നമ്പര് = 임시.getsockname()[1]
    വലുപ്പം_ക്രമീകരിക്കുക_ലിഖിതം = '{}x{}'.format(너비, 높이)
    പ്രോസസ്_മൂല്യം = subprocess.Popen(['python3', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(പോര്_ട്ട്_നമ്പര്), '--resolution', വലുപ്പം_ക്രമീകരിക്കുക_ലിഖിതം], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    సెలక్టర్_a916db4e = selectors.DefaultSelector(); సెలక్టర్_a916db4e.register(പ്രോസസ്_മൂല്യം.stdout, selectors.EVENT_READ)
    ലോഗ്_രേഖ = bytearray(); വിദൂര_മൂല്യം = None; കൈമാറുക_മൂല്യം_630ba093 = None

    def 기다리기(പ്രദർശനം_മൂല്യം, നടപ്പിലാക്കുക=0):
        마감 = time.monotonic() + 60
        while പ്രദർശനം_മൂല്യം not in ലോഗ്_രേഖ[നടപ്പിലാക്കുക:]:
            if time.monotonic() > 마감 or പ്രോസസ്_മൂല്യം.poll() is not None or b'HALTED' in ലോഗ്_രേഖ or b'PANIC:' in ലോഗ്_രേഖ:
                raise AssertionError(ലോഗ്_രേഖ[നടപ്പിലാക്കുക:].decode('utf-8', 'replace'))
            for ഇവന്റ്, _ in సెలక్టర్_a916db4e.select(.1):
                ഡാറ്റാ = ഇവന്റ്.fileobj.read(65536)
                if ഡാറ്റാ: ലോഗ്_രേഖ.extend(ഡാറ്റാ)
        return ലോഗ്_രേഖ[നടപ്പിലാക്കുക:].decode('utf-8', 'replace')

    def ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(nbsp_ചിഹ്നം, 눌림=True): വിദൂര_മൂല്യം.sendall(struct.pack('>BBHI', 4, int(눌림), 0, nbsp_ചിഹ്നം))

    def SMS_അയയ്_ക്കുക(പദാവലി):
        നടപ്പിലാക്കുക = len(ലോഗ്_രേഖ)
        for പ്രതീകം_മൂല്യം in പദാവലി:
            nbsp_ചിഹ്നം = 0xff0d if പ്രതീകം_മൂല്യം == '\n' else ord(പ്രതീകം_മൂല്യം) if ord(പ്രതീകം_മൂല്യം) < 256 else 0x1000000 | ord(പ്രതീകം_മൂല്യം)
            ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(nbsp_ചിഹ്നം); ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(nbsp_ചിഹ്നം, False)
        return നടപ്പിലാക്കുക

    def ഷെല്(പദാവലി): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_അയയ്_ക്കുക(പദാവലി+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, ലംബം_പദവി, 눌림): വിദൂര_മൂല്യം.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ലംബം_പദവി))

    def ക്ലിക്ക്_ചെയ്യുക_മൂല്യം(가로, ലംബം_പദവി): 가리키기(가로, ലംബം_പദവി, 1); 가리키기(가로, ലംബം_പദവി, 0)

    def ബിറ്റ്മാപ്പ്_ഇമേജ്():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 വാസ്തവമായ_ഡാറ്റാ 너비를 쓴다.
        വിദൂര_മൂല്യം.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ഡ്രോയിംഗ്_മൂല്യം = Image.new('RGB', (너비, 높이)); ഏരിയ_മൂല്യം = 0
        while True:
            종류 = 정확한값(വിദൂര_മൂല്യം, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ദൈര്_ഘ്യം_മൂല്യം = struct.unpack('>I', 정확한값(വിദൂര_മൂല്യം, 7)[3:])[0]; 정확한값(വിദൂര_മൂല്യം, ദൈര്_ഘ്യം_മൂല്യം); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(വിദൂര_മൂല്യം, 3)[1:])[0]
            for _ in range(개수):
                가로, ലംബം_പദവി, 폭, ദൈര്_ഘ്യം_മൂല്യം, എന്_കോഡുചെയ്യല്_മൂല്യം = struct.unpack('>HHHHi', 정확한값(വിദൂര_മൂല്യം, 12))
                assert എന്_കോഡുചെയ്യല്_മൂല്യം == 0 and 가로+폭 <= 너비 and ലംബം_പദവി+ദൈര്_ഘ്യം_മൂല്യം <= 높이
                ഡ്രോയിംഗ്_മൂല്യം.paste(Image.frombytes('RGB', (폭, ദൈര്_ഘ്യം_മൂല്യം), 정확한값(വിദൂര_മൂല്യം, 폭*ദൈര്_ഘ്യം_മൂല്യം*4), 'raw', 'BGRX'), (가로, ലംബം_പദവി))
                ഏരിയ_മൂല്യം += 폭*ദൈര്_ഘ്യം_മൂല്യം
            if ഏരിയ_മൂല്യം:
                assert ഏരിയ_മൂല്യം == 너비*높이, ഏരിയ_മൂല്യം
                return ഡ്രോയിംഗ്_മൂല്യം

    def ചെക്ക്_പെല്(ഏകോപനം_മൂല്യം, 색):
        마감 = time.monotonic()+10
        while True:
            ഡ്രോയിംഗ്_മൂല്യം = ബിറ്റ്മാപ്പ്_ഇമേജ്()
            if ഡ്രോയിംഗ്_മൂല്യം.getpixel(ഏകോപനം_മൂല്യം) == 색: return ഡ്രോയിംഗ്_മൂല്യം
            if time.monotonic() > 마감: raise AssertionError((ഏകോപനം_മൂല്യം, ഡ്രോയിംഗ്_മൂല്യം.getpixel(ഏകോപനം_മൂല്യം), 색))

    def അപ്_ലോഡ്_ഫയലുകൾ(പേരു്, ഡാറ്റാ): കൈമാറുക_മൂല്യം_630ba093.storbinary('STOR '+പേരു്, io.BytesIO(ഡാറ്റാ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+വലുപ്പം_ക്രമീകരിക്കുക_ലിഖിതം+' RGB32').encode() in ലോഗ്_രേഖ
        print('BOOT:', വലുപ്പം_ക്രമീകരിക്കുക_ലിഖിതം, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ലോഗ്_രേഖ).group(1))
        വിദൂര_മൂല്യം = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(വിദൂര_മൂല്യം, 12) == b'RFB 003.008\n'; വിദൂര_മൂല്യം.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(വിദൂര_മൂല്യം, 정확한값(വിദൂര_മൂല്യം, 1)[0]); വിദൂര_മൂല്യം.sendall(b'\x01')
        assert 정확한값(വിദൂര_മൂല്യം, 4) == b'\0'*4; വിദൂര_മൂല്യം.sendall(b'\x01')
        초기 = 정확한값(വിദൂര_മൂല്യം, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(വിദൂര_മൂല്യം, struct.unpack('>I', 초기[20:])[0])
        വിദൂര_മൂല്യം.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        വിദൂര_മൂല്യം.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ചെക്ക്_പെല്((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ചെക്ക്_പെല്((너비-568, 높이-360), (32, 80, 144))
        നടപ്പിലാക്കുക = len(ലോഗ്_രേഖ); ക്ലിക്ക്_ചെയ്യുക_മൂല്യം(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', നടപ്പിലാക്കുക)
        ചെക്ക്_പെല്((너비-568, 높이-360), (24, 32, 48))
        നടപ്പിലാക്കുക = len(ലോഗ്_രേഖ); ക്ലിക്ക്_ചെയ്യുക_മൂല്യം(80, 16); 기다리기(b'TERMINAL FOCUS 1', നടപ്പിലാക്കുക)
        ഷെല്('ftpd start')
        കൈമാറുക_മൂല്യം_630ba093 = ftplib.FTP(); കൈമാറുക_മൂല്യം_630ba093.encoding = 'utf-8'; കൈമാറുക_മൂല്യം_630ba093.connect('127.0.0.1', പോര്_ട്ട്_നമ്പര്, timeout=20); കൈമാറുക_മൂല്യം_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ക്ലിപ്പ് 밖·빈 사각형을 포함한다.
        ഉറവിടം = '''#include <화면규약.h>
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
    റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        അപ്_ലോഡ്_ഫയലുകൾ('화면시험.c', ഉറവിടം.encode())
        assert 'exit 0' in ഷെല്('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_അയയ്_ക്കുക('run /화면시험\n'))
        ചെക്ക്_പെല്((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_അയയ്_ക്കുക('q'))
        ഉറവിടം = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, ഫലം, సిస్టమ్_തെറ്റ്
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except సిస్టమ్_തെറ്റ് as പിശക്:
    assert പിശക്.സൂചിക == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
ഫലം("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        അപ്_ലോഡ്_ഫയലുകൾ('화면시험.py', ഉറവിടം.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_അയയ്_ക്കുക('python /화면시험.py\n'))
        ചെക്ക്_പെല്((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_അയയ്_ക്കുക('q'))
        ഉറവിടം = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new അവസ്ഥ_ഒഴിവാക്കൽ("വലിപ്പം");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new അവസ്ഥ_ഒഴിവാക്കൽ("ക്ലിപ്പ്"); }
        catch (അസാധുവായ_ആര്_ഗ്യുമെന്_റ്_ഒഴിവാക്കൽ പിശക്) { }
        화면.മായ്ക്കുക_എന്_ട്രി(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # ഒഴിവാക്കൽ 처리는 ഹോസ്റ്റ് javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = അളവ്_പാത/'해상도경계시험.java'
        경계원문.write_text(ഉറവിടം.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist/jkoros-native-korean.jar'), '-d', str(അളവ്_പാത), str(경계원문)])
        അപ്_ലോഡ്_ഫയലുകൾ('해상도경계시험.class', (അളവ്_പാത/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_അയയ്_ക്കുക('java 해상도경계시험\n'))
        ചെക്ക്_പെല്((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_അയയ്_ക്കുക('q'))
        # 게스트 javac의 പിന്തുണ_മൂല്യം 문법으로 വലിപ്പം ചോദ്യം_മൂല്യം·മായ്ക്കുക_എന്_ട്രി·다섯 인수 그리기를 컴파일한다.
        ഉറവിടം = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.മായ്ക്കുക_എന്_ട്രി(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.ഫലം.റൈറ്റ്_ചെയ്യുക_ലൈൻ("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        അപ്_ലോഡ്_ഫയലുകൾ('해상도시험.java', ഉറവിടം.encode())
        അളവ് = ഷെല്('javac 해상도시험.java'); assert 'exit 0' in അളവ്, അളവ്
        기다리기(b'JAVA RESOLUTION PASS', SMS_അയയ്_ക്കുക('java 해상도시험\n'))
        ചെക്ക്_പെല്((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_അയയ്_ക്കുക('q'))
        അപ്_ലോഡ്_ഫയലുകൾ('스윙시험.class', (അളവ്_പാത/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_അയയ്_ക്കുക('java 스윙시험\n'))
        가로, ലംബം_പദവി = (너비-400)//2, (높이-280)//2
        ഡ്രോയിംഗ്_മൂല്യം = ചെക്ക്_പെല്((가로, ലംബം_പദവി), (32, 80, 144))
        ഡ്രോയിംഗ്_മൂല്യം.save(str(അളവ്_പാത/(വലുപ്പം_ക്രമീകരിക്കുക_ലിഖിതം+'.png')))
        നടപ്പിലാക്കുക = len(ലോഗ്_രേഖ); ക്ലിക്ക്_ചെയ്യുക_മൂല്യം(가로+80, ലംബം_പദവി+155)
        기다리기('SWING CLICK പേരു്'.encode(), നടപ്പിലാക്കുക)
        നടപ്പിലാക്കുക = len(ലോഗ്_രേഖ); ക്ലിക്ക്_ചെയ്യുക_മൂല്യം(가로+385, ലംബം_പദവി+15); 기다리기(b'jkoros-native> ', നടപ്പിലാക്കുക)
        assert 'AFTER_RESOLUTION' in ഷെല്('echo AFTER_RESOLUTION')
        print('PASS:', വലുപ്പം_ക്രമീകരിക്കുക_ലിഖിതം, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if കൈമാറുക_മൂല്യം_630ba093: കൈമാറുക_മൂല്യം_630ba093.close()
        if വിദൂര_മൂല്യം: വിദൂര_മൂല്യം.close()
        if പ്രോസസ്_മൂല്യം.poll() is None:
            പ്രോസസ്_മൂല്യം.terminate()
            try: പ്രോസസ്_മൂല്യം.wait(timeout=8)
            except subprocess.TimeoutExpired: പ്രോസസ്_മൂല്യം.kill(); പ്രോസസ്_മൂല്യം.wait()
        సెలక్టర్_a916db4e.close(); പ്രോസസ്_മൂല്യം.stdout.close()
        (അളവ്_പാത/(വലുപ്പം_ക്രമീകരിക്കുക_ലിഖിതം+'.log')).write_bytes(ലോഗ്_രേഖ)


def നടപ്പിലാക്കുക():
    അളവ്_പാത = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/resolution'; അളവ്_പാത.mkdir(parents=True, exist_ok=True)
    ലോഗ്_രേഖ = {'passed': False, 'kernel_sha256': hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for അസാധുവായ_മൂല്യം in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            അളവ് = subprocess.run(['python3', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py'), '--resolution', അസാധുവായ_മൂല്യം], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert അളവ്.returncode == 2 and b'--resolution' in അളവ്.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(അളവ്_പാത), str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, അളവ്_പാത); ലോഗ്_രേഖ['resolutions'].append([너비, 높이])
        ലോഗ്_രേഖ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (അളവ്_പാത/'report.json').write_text(json.dumps(ലോഗ്_രേഖ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': നടപ്പിലാക്കുക()
