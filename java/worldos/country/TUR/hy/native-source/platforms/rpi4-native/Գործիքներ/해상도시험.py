#!/usr/bin/env python3
"""իրական_տվյալ QEMU/VNC에서 화면 Չափս·경계·պատուհան տեղափոխել_արժեք·Swing·언어별 그리기를 검사한다."""
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
from սեղան_տեսք import 정확한값
from կատարել_հրաման import արձակել_արմատ


def 해상도시험(너비, 높이, չափ_ուղի):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    չափափոխել_Գրվածք = '{}x{}'.format(너비, 높이)
    Ընթացք_արժեք = subprocess.Popen(['python3', str(արձակել_արմատ/'Գործիքներ/կատարել_հրաման.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', չափափոխել_Գրվածք], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ընտրիչ_a916db4e = selectors.DefaultSelector(); ընտրիչ_a916db4e.register(Ընթացք_արժեք.stdout, selectors.EVENT_READ)
    մատյան_տող = bytearray(); հեռակա_արժեք = None; փոխանցել_արժեք = None

    def 기다리기(ցուցադրել_արժեք, Գործարկել=0):
        마감 = time.monotonic() + 60
        while ցուցադրել_արժեք not in մատյան_տող[Գործարկել:]:
            if time.monotonic() > 마감 or Ընթացք_արժեք.poll() is not None or b'HALTED' in մատյան_տող or b'PANIC:' in մատյան_տող:
                raise AssertionError(մատյան_տող[Գործարկել:].decode('utf-8', 'replace'))
            for միջոցառում, _ in ընտրիչ_a916db4e.select(.1):
                տվյալ = միջոցառում.fileobj.read(65536)
                if տվյալ: մատյան_տող.extend(տվյալ)
        return մատյան_տող[Գործարկել:].decode('utf-8', 'replace')

    def կտտացնել_կոճակ(նշան, 눌림=True): հեռակա_արժեք.sendall(struct.pack('>BBHI', 4, int(눌림), 0, նշան))

    def ուղարկել_SMS(Տեքստ):
        Գործարկել = len(մատյան_տող)
        for գրանշան_արժեք in Տեքստ:
            նշան = 0xff0d if գրանշան_արժեք == '\n' else ord(գրանշան_արժեք) if ord(գրանշան_արժեք) < 256 else 0x1000000 | ord(գրանշան_արժեք)
            կտտացնել_կոճակ(նշան); կտտացնել_կոճակ(նշան, False)
        return Գործարկել

    def խեցի(Տեքստ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', ուղարկել_SMS(Տեքստ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Ուղղահայաց_դիրք, 눌림): հեռակա_արժեք.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Ուղղահայաց_դիրք))

    def կտտացնել_արժեք(가로, Ուղղահայաց_դիրք): 가리키기(가로, Ուղղահայաց_դիրք, 1); 가리키기(가로, Ուղղահայաց_դիրք, 0)

    def կետապատկեր_նկար():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 իրական_տվյալ 너비를 쓴다.
        հեռակա_արժեք.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        նկար_արժեք_c143fe9e = Image.new('RGB', (너비, 높이)); տարածք_արժեք = 0
        while True:
            종류 = 정확한값(հեռակա_արժեք, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                տեւողություն_արժեք = struct.unpack('>I', 정확한값(հեռակա_արժեք, 7)[3:])[0]; 정확한값(հեռակա_արժեք, տեւողություն_արժեք); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(հեռակա_արժեք, 3)[1:])[0]
            for _ in range(개수):
                가로, Ուղղահայաց_դիրք, 폭, տեւողություն_արժեք, կոդավորում_արժեք = struct.unpack('>HHHHi', 정확한값(հեռակա_արժեք, 12))
                assert կոդավորում_արժեք == 0 and 가로+폭 <= 너비 and Ուղղահայաց_դիրք+տեւողություն_արժեք <= 높이
                նկար_արժեք_c143fe9e.paste(Image.frombytes('RGB', (폭, տեւողություն_արժեք), 정확한값(հեռակա_արժեք, 폭*տեւողություն_արժեք*4), 'raw', 'BGRX'), (가로, Ուղղահայաց_դիրք))
                տարածք_արժեք += 폭*տեւողություն_արժեք
            if տարածք_արժեք:
                assert տարածք_արժեք == 너비*높이, տարածք_արժեք
                return նկար_արժեք_c143fe9e

    def կտրոն_փիքսել(կոորդինատ_արժեք, 색):
        마감 = time.monotonic()+10
        while True:
            նկար_արժեք_c143fe9e = կետապատկեր_նկար()
            if նկար_արժեք_c143fe9e.getpixel(կոորդինատ_արժեք) == 색: return նկար_արժեք_c143fe9e
            if time.monotonic() > 마감: raise AssertionError((կոորդինատ_արժեք, նկար_արժեք_c143fe9e.getpixel(կոորդինատ_արժեք), 색))

    def վերբեռնել_Նիշքեր(Անուն, տվյալ): փոխանցել_արժեք.storbinary('STOR '+Անուն, io.BytesIO(տվյալ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+չափափոխել_Գրվածք+' RGB32').encode() in մատյան_տող
        print('BOOT:', չափափոխել_Գրվածք, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', մատյան_տող).group(1))
        հեռակա_արժեք = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(հեռակա_արժեք, 12) == b'RFB 003.008\n'; հեռակա_արժեք.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(հեռակա_արժեք, 정확한값(հեռակա_արժեք, 1)[0]); հեռակա_արժեք.sendall(b'\x01')
        assert 정확한값(հեռակա_արժեք, 4) == b'\0'*4; հեռակա_արժեք.sendall(b'\x01')
        초기 = 정확한값(հեռակա_արժեք, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(հեռակա_արժեք, struct.unpack('>I', 초기[20:])[0])
        հեռակա_արժեք.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        հեռակա_արժեք.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        կտրոն_փիքսել((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        կտրոն_փիքսել((너비-568, 높이-360), (32, 80, 144))
        Գործարկել = len(մատյան_տող); կտտացնել_արժեք(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Գործարկել)
        կտրոն_փիքսել((너비-568, 높이-360), (24, 32, 48))
        Գործարկել = len(մատյան_տող); կտտացնել_արժեք(80, 16); 기다리기(b'TERMINAL FOCUS 1', Գործարկել)
        խեցի('ftpd start')
        փոխանցել_արժեք = ftplib.FTP(); փոխանցել_արժեք.encoding = 'utf-8'; փոխանցել_արժեք.connect('127.0.0.1', 접속번호, timeout=20); փոխանցել_արժեք.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·հոլովակ 밖·빈 사각형을 포함한다.
        ԱՂԲՅՈՒՐ = '''#include <화면규약.h>
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
    գրել_նիշք_տվյալ(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        վերբեռնել_Նիշքեր('화면시험.c', ԱՂԲՅՈՒՐ.encode())
        assert 'exit 0' in խեցի('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', ուղարկել_SMS('run /화면시험\n'))
        կտրոն_փիքսել((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', ուղարկել_SMS('q'))
        ԱՂԲՅՈՒՐ = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, Ելք, համակարգ_սխալ
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except համակարգ_սխալ as Սխալ:
    assert Սխալ.դասիչ == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Ելք("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        վերբեռնել_Նիշքեր('화면시험.py', ԱՂԲՅՈՒՐ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', ուղարկել_SMS('python /화면시험.py\n'))
        կտրոն_փիքսել((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', ուղարկել_SMS('q'))
        ԱՂԲՅՈՒՐ = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("Չափս");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("հոլովակ"); }
        catch (잘못된인수예외 Սխալ) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 հոստ javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = չափ_ուղի/'해상도경계시험.java'
        경계원문.write_text(ԱՂԲՅՈՒՐ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(արձակել_արմատ/'dist/jkoros-native-korean.jar'), '-d', str(չափ_ուղի), str(경계원문)])
        վերբեռնել_Նիշքեր('해상도경계시험.class', (չափ_ուղի/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', ուղարկել_SMS('java 해상도경계시험\n'))
        կտրոն_փիքսել((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ուղարկել_SMS('q'))
        # 게스트 javac의 Աջակցում_արժեք 문법으로 Չափս հարցում_արժեք·지우기·다섯 인수 그리기를 컴파일한다.
        ԱՂԲՅՈՒՐ = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.Ելք.գրել_կապ("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        վերբեռնել_Նիշքեր('해상도시험.java', ԱՂԲՅՈՒՐ.encode())
        չափ = խեցի('javac 해상도시험.java'); assert 'exit 0' in չափ, չափ
        기다리기(b'JAVA RESOLUTION PASS', ուղարկել_SMS('java 해상도시험\n'))
        կտրոն_փիքսել((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ուղարկել_SMS('q'))
        վերբեռնել_Նիշքեր('스윙시험.class', (չափ_ուղի/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', ուղարկել_SMS('java 스윙시험\n'))
        가로, Ուղղահայաց_դիրք = (너비-400)//2, (높이-280)//2
        նկար_արժեք_c143fe9e = կտրոն_փիքսել((가로, Ուղղահայաց_դիրք), (32, 80, 144))
        նկար_արժեք_c143fe9e.save(str(չափ_ուղի/(չափափոխել_Գրվածք+'.png')))
        Գործարկել = len(մատյան_տող); կտտացնել_արժեք(가로+80, Ուղղահայաց_դիրք+155)
        기다리기('SWING CLICK Անուն'.encode(), Գործարկել)
        Գործարկել = len(մատյան_տող); կտտացնել_արժեք(가로+385, Ուղղահայաց_դիրք+15); 기다리기(b'jkoros-native> ', Գործարկել)
        assert 'AFTER_RESOLUTION' in խեցի('echo AFTER_RESOLUTION')
        print('PASS:', չափափոխել_Գրվածք, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if փոխանցել_արժեք: փոխանցել_արժեք.close()
        if հեռակա_արժեք: հեռակա_արժեք.close()
        if Ընթացք_արժեք.poll() is None:
            Ընթացք_արժեք.terminate()
            try: Ընթացք_արժեք.wait(timeout=8)
            except subprocess.TimeoutExpired: Ընթացք_արժեք.kill(); Ընթացք_արժեք.wait()
        ընտրիչ_a916db4e.close(); Ընթացք_արժեք.stdout.close()
        (չափ_ուղի/(չափափոխել_Գրվածք+'.log')).write_bytes(մատյան_տող)


def Գործարկել():
    չափ_ուղի = արձակել_արմատ/'build/verification/resolution'; չափ_ուղի.mkdir(parents=True, exist_ok=True)
    մատյան_տող = {'passed': False, 'kernel_sha256': hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for անվավեր_արժեք in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            չափ = subprocess.run(['python3', str(արձակել_արմատ/'Գործիքներ/կատարել_հրաման.py'), '--resolution', անվավեր_արժեք], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert չափ.returncode == 2 and b'--resolution' in չափ.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(չափ_ուղի), str(արձակել_արմատ/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, չափ_ուղի); մատյան_տող['resolutions'].append([너비, 높이])
        մատյան_տող.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (չափ_ուղի/'report.json').write_text(json.dumps(մատյան_տող, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Գործարկել()
