#!/usr/bin/env python3
"""තථ්_ය_දත්ත QEMU/VNC에서 화면 ප්_රමාණය·경계·කවුළුව ගෙනයන්න_අගය·Swing·언어별 그리기를 검사한다."""
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
from වැඩතලය_දසුන import 정확한값
from ක්_රියාත්මක_කරන්න_විධානය import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ප්_රමාණනය_පෙළ = '{}x{}'.format(너비, 높이)
    ක්_රියාවලිය_අගය = subprocess.Popen(['python3', str(기준/'මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ප්_රමාණනය_පෙළ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    වරකය_a916db4e = selectors.DefaultSelector(); වරකය_a916db4e.register(ක්_රියාවලිය_අගය.stdout, selectors.EVENT_READ)
    ලොගය_පේළිය = bytearray(); දුරස්ථ_අගය = None; මාරුව_අගය = None

    def 기다리기(දර්ශනය_අගය, ක්_රියාත්මක_කරන්න_2=0):
        마감 = time.monotonic() + 60
        while දර්ශනය_අගය not in ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:]:
            if time.monotonic() > 마감 or ක්_රියාවලිය_අගය.poll() is not None or b'HALTED' in ලොගය_පේළිය or b'PANIC:' in ලොගය_පේළිය:
                raise AssertionError(ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:].decode('utf-8', 'replace'))
            for සිදුවීම, _ in වරකය_a916db4e.select(.1):
                දත්ත = සිදුවීම.fileobj.read(65536)
                if දත්ත: ලොගය_පේළිය.extend(දත්ත)
        return ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:].decode('utf-8', 'replace')

    def ක්ලික්_කරන්න_බොත්තම(සංකේතය, 눌림=True): දුරස්ථ_අගය.sendall(struct.pack('>BBHI', 4, int(눌림), 0, සංකේතය))

    def SMS_යවන්න(පෙළ):
        ක්_රියාත්මක_කරන්න_2 = len(ලොගය_පේළිය)
        for අනුලකුණ_අගය in පෙළ:
            සංකේතය = 0xff0d if අනුලකුණ_අගය == '\n' else ord(අනුලකුණ_අගය) if ord(අනුලකුණ_අගය) < 256 else 0x1000000 | ord(අනුලකුණ_අගය)
            ක්ලික්_කරන්න_බොත්තම(සංකේතය); ක්ලික්_කරන්න_බොත්තම(සංකේතය, False)
        return ක්_රියාත්මක_කරන්න_2

    def කවචය(පෙළ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_යවන්න(පෙළ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): දුරස්ථ_අගය.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def ක්ලික්_කරන්න_අගය(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def බිටු_සිතියම_අනුරුව():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 තථ්_ය_දත්ත 너비를 쓴다.
        දුරස්ථ_අගය.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        චිත්_රය_අගය = Image.new('RGB', (너비, 높이)); ප්_රදේශය_අගය = 0
        while True:
            종류 = 정확한값(දුරස්ථ_අගය, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                දිග_අගය = struct.unpack('>I', 정확한값(දුරස්ථ_අගය, 7)[3:])[0]; 정확한값(දුරස්ථ_අගය, දිග_අගය); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(දුරස්ථ_අගය, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, දිග_අගය, සංකේතනය_අගය = struct.unpack('>HHHHi', 정확한값(දුරස්ථ_අගය, 12))
                assert සංකේතනය_අගය == 0 and 가로+폭 <= 너비 and 세로+දිග_අගය <= 높이
                චිත්_රය_අගය.paste(Image.frombytes('RGB', (폭, දිග_අගය), 정확한값(දුරස්ථ_අගය, 폭*දිග_අගය*4), 'raw', 'BGRX'), (가로, 세로))
                ප්_රදේශය_අගය += 폭*දිග_අගය
            if ප්_රදේශය_අගය:
                assert ප්_රදේශය_අගය == 너비*높이, ප්_රදේශය_අගය
                return චිත්_රය_අගය

    def චෙක්පත_පික්සලය(ඛණ්ඩාංක_අගය, 색):
        마감 = time.monotonic()+10
        while True:
            චිත්_රය_අගය = බිටු_සිතියම_අනුරුව()
            if චිත්_රය_අගය.getpixel(ඛණ්ඩාංක_අගය) == 색: return චිත්_රය_අගය
            if time.monotonic() > 마감: raise AssertionError((ඛණ්ඩාංක_අගය, චිත්_රය_අගය.getpixel(ඛණ්ඩාංක_අගය), 색))

    def උඩුගත_කරන්න_ගොනු(නම, දත්ත): මාරුව_අගය.storbinary('STOR '+නම, io.BytesIO(දත්ත))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ප්_රමාණනය_පෙළ+' RGB32').encode() in ලොගය_පේළිය
        print('BOOT:', ප්_රමාණනය_පෙළ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ලොගය_පේළිය).group(1))
        දුරස්ථ_අගය = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(දුරස්ථ_අගය, 12) == b'RFB 003.008\n'; දුරස්ථ_අගය.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(දුරස්ථ_අගය, 정확한값(දුරස්ථ_අගය, 1)[0]); දුරස්ථ_අගය.sendall(b'\x01')
        assert 정확한값(දුරස්ථ_අගය, 4) == b'\0'*4; දුරස්ථ_අගය.sendall(b'\x01')
        초기 = 정확한값(දුරස්ථ_අගය, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(දුරස්ථ_අගය, struct.unpack('>I', 초기[20:])[0])
        දුරස්ථ_අගය.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        දුරස්ථ_අගය.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        චෙක්පත_පික්සලය((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        චෙක්පත_පික්සලය((너비-568, 높이-360), (32, 80, 144))
        ක්_රියාත්මක_කරන්න_2 = len(ලොගය_පේළිය); ක්ලික්_කරන්න_අගය(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ක්_රියාත්මක_කරන්න_2)
        චෙක්පත_පික්සලය((너비-568, 높이-360), (24, 32, 48))
        ක්_රියාත්මක_කරන්න_2 = len(ලොගය_පේළිය); ක්ලික්_කරන්න_අගය(80, 16); 기다리기(b'TERMINAL FOCUS 1', ක්_රියාත්මක_කරන්න_2)
        කවචය('ftpd start')
        මාරුව_අගය = ftplib.FTP(); මාරුව_අගය.encoding = 'utf-8'; මාරුව_අගය.connect('127.0.0.1', 접속번호, timeout=20); මාරුව_අගය.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·පසුර 밖·빈 사각형을 포함한다.
        මූලය = '''#include <화면규약.h>
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
    ලියන්න_ගොනුව_දත්ත(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        උඩුගත_කරන්න_ගොනු('화면시험.c', මූලය.encode())
        assert 'exit 0' in කවචය('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_යවන්න('run /화면시험\n'))
        චෙක්පත_පික්සලය((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_යවන්න('q'))
        මූලය = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, පද්ධතිය_දොස
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except පද්ධතිය_දොස as දෝෂය:
    assert දෝෂය.සූචිය == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        උඩුගත_කරන්න_ගොනු('화면시험.py', මූලය.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_යවන්න('python /화면시험.py\n'))
        චෙක්පත_පික්සලය((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_යවන්න('q'))
        මූලය = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] විස්තාරක) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("ප්_රමාණය");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("පසුර"); }
        catch (잘못된인수예외 දෝෂය) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 ධාරකය javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(මූලය.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        උඩුගත_කරන්න_ගොනු('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_යවන්න('java 해상도경계시험\n'))
        චෙක්පත_පික්සලය((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_යවන්න('q'))
        # 게스트 javac의 සහාය_අගය 문법으로 ප්_රමාණය විමසුම_අගය·지우기·다섯 විස්තාරක 그리기를 컴파일한다.
        මූලය = '''public class 해상도시험 {
    public static void main(String[] විස්තාරක) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.ලියන්න_පේළිය("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        උඩුගත_කරන්න_ගොනු('해상도시험.java', මූලය.encode())
        결과 = කවචය('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', SMS_යවන්න('java 해상도시험\n'))
        චෙක්පත_පික්සලය((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_යවන්න('q'))
        උඩුගත_කරන්න_ගොනු('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_යවන්න('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        චිත්_රය_අගය = චෙක්පත_පික්සලය((가로, 세로), (32, 80, 144))
        චිත්_රය_අගය.save(str(결과경로/(ප්_රමාණනය_පෙළ+'.png')))
        ක්_රියාත්මක_කරන්න_2 = len(ලොගය_පේළිය); ක්ලික්_කරන්න_අගය(가로+80, 세로+155)
        기다리기('SWING CLICK නම'.encode(), ක්_රියාත්මක_කරන්න_2)
        ක්_රියාත්මක_කරන්න_2 = len(ලොගය_පේළිය); ක්ලික්_කරන්න_අගය(가로+385, 세로+15); 기다리기(b'jkoros-native> ', ක්_රියාත්මක_කරන්න_2)
        assert 'AFTER_RESOLUTION' in කවචය('echo AFTER_RESOLUTION')
        print('PASS:', ප්_රමාණනය_පෙළ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if මාරුව_අගය: මාරුව_අගය.close()
        if දුරස්ථ_අගය: දුරස්ථ_අගය.close()
        if ක්_රියාවලිය_අගය.poll() is None:
            ක්_රියාවලිය_අගය.terminate()
            try: ක්_රියාවලිය_අගය.wait(timeout=8)
            except subprocess.TimeoutExpired: ක්_රියාවලිය_අගය.kill(); ක්_රියාවලිය_අගය.wait()
        වරකය_a916db4e.close(); ක්_රියාවලිය_අගය.stdout.close()
        (결과경로/(ප්_රමාණනය_පෙළ+'.log')).write_bytes(ලොගය_පේළිය)


def ක්_රියාත්මක_කරන්න_2():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    ලොගය_පේළිය = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for අවලංගු_අගය in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py'), '--resolution', අවලංගු_අගය], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); ලොගය_පේළිය['resolutions'].append([너비, 높이])
        ලොගය_පේළිය.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(ලොගය_පේළිය, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ක්_රියාත්මක_කරන්න_2()
