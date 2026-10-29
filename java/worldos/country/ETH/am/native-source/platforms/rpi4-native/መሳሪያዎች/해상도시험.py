#!/usr/bin/env python3
"""ትክክለኛ_ውሂብ QEMU/VNC에서 화면 መጠን·경계·መስኮት አንቀሳቅስ_እሴት·Swing·언어별 그리기를 검사한다."""
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
from ዴስክቶፕ_እየው import 정확한값
from ፈጽም_ትእዛዝ import አሳይ_ስር


def 해상도시험(너비, 높이, ልኬት_ዱካ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); የወደብ_ቁጥር = 임시.getsockname()[1]
    መጠን_ቀይር_ጽሁፍ = '{}x{}'.format(너비, 높이)
    ሂደት_እሴት = subprocess.Popen(['python3', str(አሳይ_ስር/'መሳሪያዎች/ፈጽም_ትእዛዝ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(የወደብ_ቁጥር), '--resolution', መጠን_ቀይር_ጽሁፍ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    መራጭ_a916db4e = selectors.DefaultSelector(); መራጭ_a916db4e.register(ሂደት_እሴት.stdout, selectors.EVENT_READ)
    መዝግብ_ረድፍ = bytearray(); የሩቅ_እሴት = None; ትልልፍ_እሴት = None

    def 기다리기(አሳይ_እሴት, ማስኬጃ=0):
        마감 = time.monotonic() + 60
        while አሳይ_እሴት not in መዝግብ_ረድፍ[ማስኬጃ:]:
            if time.monotonic() > 마감 or ሂደት_እሴት.poll() is not None or b'HALTED' in መዝግብ_ረድፍ or b'PANIC:' in መዝግብ_ረድፍ:
                raise AssertionError(መዝግብ_ረድፍ[ማስኬጃ:].decode('utf-8', 'replace'))
            for ፍጻሜ, _ in መራጭ_a916db4e.select(.1):
                ውሂብ = ፍጻሜ.fileobj.read(65536)
                if ውሂብ: መዝግብ_ረድፍ.extend(ውሂብ)
        return መዝግብ_ረድፍ[ማስኬጃ:].decode('utf-8', 'replace')

    def ጠቅ_አድርግ_አዝራር(ምልክት_ad6f1a96, 눌림=True): የሩቅ_እሴት.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ምልክት_ad6f1a96))

    def ጽሁፍ_ላክ(ጽሁፍ):
        ማስኬጃ = len(መዝግብ_ረድፍ)
        for ቁምፊ_እሴት in ጽሁፍ:
            ምልክት_ad6f1a96 = 0xff0d if ቁምፊ_እሴት == '\n' else ord(ቁምፊ_እሴት) if ord(ቁምፊ_እሴት) < 256 else 0x1000000 | ord(ቁምፊ_እሴት)
            ጠቅ_አድርግ_አዝራር(ምልክት_ad6f1a96); ጠቅ_አድርግ_አዝራር(ምልክት_ad6f1a96, False)
        return ማስኬጃ

    def ሼል(ጽሁፍ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', ጽሁፍ_ላክ(ጽሁፍ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, ቋሚ_በቦታ_አስቀመጠ, 눌림): የሩቅ_እሴት.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ቋሚ_በቦታ_አስቀመጠ))

    def ጠቅ_አድርግ_እሴት(가로, ቋሚ_በቦታ_አስቀመጠ): 가리키기(가로, ቋሚ_በቦታ_አስቀመጠ, 1); 가리키기(가로, ቋሚ_በቦታ_አስቀመጠ, 0)

    def ቢትማፕ_ምስል():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ትክክለኛ_ውሂብ 너비를 쓴다.
        የሩቅ_እሴት.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ስዕል_እሴት = Image.new('RGB', (너비, 높이)); ምድብ_እሴት_9285603e = 0
        while True:
            종류 = 정확한값(የሩቅ_እሴት, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ርዝመት_እሴት = struct.unpack('>I', 정확한값(የሩቅ_እሴት, 7)[3:])[0]; 정확한값(የሩቅ_እሴት, ርዝመት_እሴት); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(የሩቅ_እሴት, 3)[1:])[0]
            for _ in range(개수):
                가로, ቋሚ_በቦታ_አስቀመጠ, 폭, ርዝመት_እሴት, በኮድ_መክተት_እሴት = struct.unpack('>HHHHi', 정확한값(የሩቅ_እሴት, 12))
                assert በኮድ_መክተት_እሴት == 0 and 가로+폭 <= 너비 and ቋሚ_በቦታ_አስቀመጠ+ርዝመት_እሴት <= 높이
                ስዕል_እሴት.paste(Image.frombytes('RGB', (폭, ርዝመት_እሴት), 정확한값(የሩቅ_እሴት, 폭*ርዝመት_እሴት*4), 'raw', 'BGRX'), (가로, ቋሚ_በቦታ_አስቀመጠ))
                ምድብ_እሴት_9285603e += 폭*ርዝመት_እሴት
            if ምድብ_እሴት_9285603e:
                assert ምድብ_እሴት_9285603e == 너비*높이, ምድብ_እሴት_9285603e
                return ስዕል_እሴት

    def ቼክ_ፒክስል(አቀነባብር_እሴት, 색):
        마감 = time.monotonic()+10
        while True:
            ስዕል_እሴት = ቢትማፕ_ምስል()
            if ስዕል_እሴት.getpixel(አቀነባብር_እሴት) == 색: return ስዕል_እሴት
            if time.monotonic() > 마감: raise AssertionError((አቀነባብር_እሴት, ስዕል_እሴት.getpixel(አቀነባብር_እሴት), 색))

    def መጫን_ፋይሎች(ስም, ውሂብ): ትልልፍ_እሴት.storbinary('STOR '+ስም, io.BytesIO(ውሂብ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+መጠን_ቀይር_ጽሁፍ+' RGB32').encode() in መዝግብ_ረድፍ
        print('BOOT:', መጠን_ቀይር_ጽሁፍ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', መዝግብ_ረድፍ).group(1))
        የሩቅ_እሴት = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(የሩቅ_እሴት, 12) == b'RFB 003.008\n'; የሩቅ_እሴት.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(የሩቅ_እሴት, 정확한값(የሩቅ_እሴት, 1)[0]); የሩቅ_እሴት.sendall(b'\x01')
        assert 정확한값(የሩቅ_እሴት, 4) == b'\0'*4; የሩቅ_እሴት.sendall(b'\x01')
        초기 = 정확한값(የሩቅ_እሴት, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(የሩቅ_እሴት, struct.unpack('>I', 초기[20:])[0])
        የሩቅ_እሴት.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        የሩቅ_እሴት.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ቼክ_ፒክስል((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ቼክ_ፒክስል((너비-568, 높이-360), (32, 80, 144))
        ማስኬጃ = len(መዝግብ_ረድፍ); ጠቅ_አድርግ_እሴት(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ማስኬጃ)
        ቼክ_ፒክስል((너비-568, 높이-360), (24, 32, 48))
        ማስኬጃ = len(መዝግብ_ረድፍ); ጠቅ_አድርግ_እሴት(80, 16); 기다리기(b'TERMINAL FOCUS 1', ማስኬጃ)
        ሼል('ftpd start')
        ትልልፍ_እሴት = ftplib.FTP(); ትልልፍ_እሴት.encoding = 'utf-8'; ትልልፍ_እሴት.connect('127.0.0.1', የወደብ_ቁጥር, timeout=20); ትልልፍ_እሴት.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ቅንጥብ 밖·빈 사각형을 포함한다.
        ምንጭ = '''#include <화면규약.h>
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
    ጻፍ_ፋይል_ውሂብ(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        መጫን_ፋይሎች('화면시험.c', ምንጭ.encode())
        assert 'exit 0' in ሼል('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', ጽሁፍ_ላክ('run /화면시험\n'))
        ቼክ_ፒክስል((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', ጽሁፍ_ላክ('q'))
        ምንጭ = '''from አማርኛ import 화면크기, 네모그리기, 그림기다리기, ውጤት, ስርዓት_ስህተት
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ስርዓት_ስህተት as ስህተት:
    assert ስህተት.መረጃ_ጠቆመ == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
ውጤት("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        መጫን_ፋይሎች('화면시험.py', ምንጭ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', ጽሁፍ_ላክ('python /화면시험.py\n'))
        ቼክ_ፒክስል((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', ጽሁፍ_ላክ('q'))
        ምንጭ = '''import አማርኛ.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new ዞን_ልዩነት("መጠን");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new ዞን_ልዩነት("ቅንጥብ"); }
        catch (ልክ_ያልኾነ_ነጋሪ_እሴት_ልዩነት ስህተት) { }
        화면.አስወግድ_ምዝግብ_c8dbc399(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # ልዩነት 처리는 አዘጋጅ_b78e430d javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = ልኬት_ዱካ/'해상도경계시험.java'
        경계원문.write_text(ምንጭ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(አሳይ_ስር/'dist/jkoros-native-korean.jar'), '-d', str(ልኬት_ዱካ), str(경계원문)])
        መጫን_ፋይሎች('해상도경계시험.class', (ልኬት_ዱካ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', ጽሁፍ_ላክ('java 해상도경계시험\n'))
        ቼክ_ፒክስል((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ጽሁፍ_ላክ('q'))
        # 게스트 javac의 ድገፍ_እሴት 문법으로 መጠን መጠይቅ_እሴት·አስወግድ_ምዝግብ_c8dbc399·다섯 인수 그리기를 컴파일한다.
        ምንጭ = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=አማርኛ.자체.화면.너비();
        int 높이=አማርኛ.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        አማርኛ.자체.화면.አስወግድ_ምዝግብ_c8dbc399(3153944);
        አማርኛ.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        አማርኛ.자체.ውጤት.ጻፍ_መስመር("JAVA RESOLUTION PASS");
        አማርኛ.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        መጫን_ፋይሎች('해상도시험.java', ምንጭ.encode())
        ልኬት = ሼል('javac 해상도시험.java'); assert 'exit 0' in ልኬት, ልኬት
        기다리기(b'JAVA RESOLUTION PASS', ጽሁፍ_ላክ('java 해상도시험\n'))
        ቼክ_ፒክስል((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ጽሁፍ_ላክ('q'))
        መጫን_ፋይሎች('스윙시험.class', (ልኬት_ዱካ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', ጽሁፍ_ላክ('java 스윙시험\n'))
        가로, ቋሚ_በቦታ_አስቀመጠ = (너비-400)//2, (높이-280)//2
        ስዕል_እሴት = ቼክ_ፒክስል((가로, ቋሚ_በቦታ_አስቀመጠ), (32, 80, 144))
        ስዕል_እሴት.save(str(ልኬት_ዱካ/(መጠን_ቀይር_ጽሁፍ+'.png')))
        ማስኬጃ = len(መዝግብ_ረድፍ); ጠቅ_አድርግ_እሴት(가로+80, ቋሚ_በቦታ_አስቀመጠ+155)
        기다리기('SWING CLICK ስም'.encode(), ማስኬጃ)
        ማስኬጃ = len(መዝግብ_ረድፍ); ጠቅ_አድርግ_እሴት(가로+385, ቋሚ_በቦታ_አስቀመጠ+15); 기다리기(b'jkoros-native> ', ማስኬጃ)
        assert 'AFTER_RESOLUTION' in ሼል('echo AFTER_RESOLUTION')
        print('PASS:', መጠን_ቀይር_ጽሁፍ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ትልልፍ_እሴት: ትልልፍ_እሴት.close()
        if የሩቅ_እሴት: የሩቅ_እሴት.close()
        if ሂደት_እሴት.poll() is None:
            ሂደት_እሴት.terminate()
            try: ሂደት_እሴት.wait(timeout=8)
            except subprocess.TimeoutExpired: ሂደት_እሴት.kill(); ሂደት_እሴት.wait()
        መራጭ_a916db4e.close(); ሂደት_እሴት.stdout.close()
        (ልኬት_ዱካ/(መጠን_ቀይር_ጽሁፍ+'.log')).write_bytes(መዝግብ_ረድፍ)


def ማስኬጃ():
    ልኬት_ዱካ = አሳይ_ስር/'build/verification/resolution'; ልኬት_ዱካ.mkdir(parents=True, exist_ok=True)
    መዝግብ_ረድፍ = {'passed': False, 'kernel_sha256': hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ልክ_ያልኾነ_እሴት in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ልኬት = subprocess.run(['python3', str(አሳይ_ስር/'መሳሪያዎች/ፈጽም_ትእዛዝ.py'), '--resolution', ልክ_ያልኾነ_እሴት], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ልኬት.returncode == 2 and b'--resolution' in ልኬት.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ልኬት_ዱካ), str(አሳይ_ስር/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, ልኬት_ዱካ); መዝግብ_ረድፍ['resolutions'].append([너비, 높이])
        መዝግብ_ረድፍ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (ልኬት_ዱካ/'report.json').write_text(json.dumps(መዝግብ_ረድፍ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ማስኬጃ()
