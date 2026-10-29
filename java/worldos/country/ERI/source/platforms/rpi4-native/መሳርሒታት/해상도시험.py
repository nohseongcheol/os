#!/usr/bin/env python3
"""ትኽክለኛ_ሓበሬታ QEMU/VNC에서 화면 መጠን·경계·መስኮት ኣንቀሳቕስ_ዋጋ·Swing·언어별 그리기를 검사한다."""
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
from ዴስክቶፕ_ትርኢት import 정확한값
from ተግብር_ትእዛዝ import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    መጠን_ጽሑፍ_cdfada26 = '{}x{}'.format(너비, 높이)
    መስርሕ_ዋጋ = subprocess.Popen(['python3', str(기준/'መሳርሒታት/ተግብር_ትእዛዝ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', መጠን_ጽሑፍ_cdfada26], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    መራፂ_a916db4e = selectors.DefaultSelector(); መራፂ_a916db4e.register(መስርሕ_ዋጋ.stdout, selectors.EVENT_READ)
    ምዝጉብ_ሪጋ = bytearray(); ርሑቕ_ዋጋ = None; ምስጋር_ዋጋ = None

    def 기다리기(ኣርእይ_ዋጋ, ኣኺድ=0):
        마감 = time.monotonic() + 60
        while ኣርእይ_ዋጋ not in ምዝጉብ_ሪጋ[ኣኺድ:]:
            if time.monotonic() > 마감 or መስርሕ_ዋጋ.poll() is not None or b'HALTED' in ምዝጉብ_ሪጋ or b'PANIC:' in ምዝጉብ_ሪጋ:
                raise AssertionError(ምዝጉብ_ሪጋ[ኣኺድ:].decode('utf-8', 'replace'))
            for ፍጻመ, _ in መራፂ_a916db4e.select(.1):
                ሓበሬታ = ፍጻመ.fileobj.read(65536)
                if ሓበሬታ: ምዝጉብ_ሪጋ.extend(ሓበሬታ)
        return ምዝጉብ_ሪጋ[ኣኺድ:].decode('utf-8', 'replace')

    def ጠዉቕ_መጠወቒ(ምልክት, 눌림=True): ርሑቕ_ዋጋ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ምልክት))

    def SMS_ስደድ(ጽሑፍ):
        ኣኺድ = len(ምዝጉብ_ሪጋ)
        for ፊደል_ዋጋ in ጽሑፍ:
            ምልክት = 0xff0d if ፊደል_ዋጋ == '\n' else ord(ፊደል_ዋጋ) if ord(ፊደል_ዋጋ) < 256 else 0x1000000 | ord(ፊደል_ዋጋ)
            ጠዉቕ_መጠወቒ(ምልክት); ጠዉቕ_መጠወቒ(ምልክት, False)
        return ኣኺድ

    def ሽፋን(ጽሑፍ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_ስደድ(ጽሑፍ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): ርሑቕ_ዋጋ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def ጠዉቕ_ዋጋ(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def ቢትማፕ_ምስሊ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ትኽክለኛ_ሓበሬታ 너비를 쓴다.
        ርሑቕ_ዋጋ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ስእሊ_ዋጋ = Image.new('RGB', (너비, 높이)); ቦታ_ዋጋ = 0
        while True:
            종류 = 정확한값(ርሑቕ_ዋጋ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ንውሓት_ዋጋ = struct.unpack('>I', 정확한값(ርሑቕ_ዋጋ, 7)[3:])[0]; 정확한값(ርሑቕ_ዋጋ, ንውሓት_ዋጋ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ርሑቕ_ዋጋ, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, ንውሓት_ዋጋ, ምምስጣር_ዋጋ = struct.unpack('>HHHHi', 정확한값(ርሑቕ_ዋጋ, 12))
                assert ምምስጣር_ዋጋ == 0 and 가로+폭 <= 너비 and 세로+ንውሓት_ዋጋ <= 높이
                ስእሊ_ዋጋ.paste(Image.frombytes('RGB', (폭, ንውሓት_ዋጋ), 정확한값(ርሑቕ_ዋጋ, 폭*ንውሓት_ዋጋ*4), 'raw', 'BGRX'), (가로, 세로))
                ቦታ_ዋጋ += 폭*ንውሓት_ዋጋ
            if ቦታ_ዋጋ:
                assert ቦታ_ዋጋ == 너비*높이, ቦታ_ዋጋ
                return ስእሊ_ዋጋ

    def ፈትሽ_ንጣብ(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            ስእሊ_ዋጋ = ቢትማፕ_ምስሊ()
            if ስእሊ_ዋጋ.getpixel(좌표) == 색: return ስእሊ_ዋጋ
            if time.monotonic() > 마감: raise AssertionError((좌표, ስእሊ_ዋጋ.getpixel(좌표), 색))

    def ስቐል_ፋይላት(ሽም, ሓበሬታ): ምስጋር_ዋጋ.storbinary('STOR '+ሽም, io.BytesIO(ሓበሬታ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+መጠን_ጽሑፍ_cdfada26+' RGB32').encode() in ምዝጉብ_ሪጋ
        print('BOOT:', መጠን_ጽሑፍ_cdfada26, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ምዝጉብ_ሪጋ).group(1))
        ርሑቕ_ዋጋ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ርሑቕ_ዋጋ, 12) == b'RFB 003.008\n'; ርሑቕ_ዋጋ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ርሑቕ_ዋጋ, 정확한값(ርሑቕ_ዋጋ, 1)[0]); ርሑቕ_ዋጋ.sendall(b'\x01')
        assert 정확한값(ርሑቕ_ዋጋ, 4) == b'\0'*4; ርሑቕ_ዋጋ.sendall(b'\x01')
        초기 = 정확한값(ርሑቕ_ዋጋ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ርሑቕ_ዋጋ, struct.unpack('>I', 초기[20:])[0])
        ርሑቕ_ዋጋ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ርሑቕ_ዋጋ.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ፈትሽ_ንጣብ((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ፈትሽ_ንጣብ((너비-568, 높이-360), (32, 80, 144))
        ኣኺድ = len(ምዝጉብ_ሪጋ); ጠዉቕ_ዋጋ(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ኣኺድ)
        ፈትሽ_ንጣብ((너비-568, 높이-360), (24, 32, 48))
        ኣኺድ = len(ምዝጉብ_ሪጋ); ጠዉቕ_ዋጋ(80, 16); 기다리기(b'TERMINAL FOCUS 1', ኣኺድ)
        ሽፋን('ftpd start')
        ምስጋር_ዋጋ = ftplib.FTP(); ምስጋር_ዋጋ.encoding = 'utf-8'; ምስጋር_ዋጋ.connect('127.0.0.1', 접속번호, timeout=20); ምስጋር_ዋጋ.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ቅንጣብ 밖·빈 사각형을 포함한다.
        ምንጪ = '''#include <화면규약.h>
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
    ጸሓፍ_ፋይል_ሓበሬታ(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ስቐል_ፋይላት('화면시험.c', ምንጪ.encode())
        assert 'exit 0' in ሽፋን('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_ስደድ('run /화면시험\n'))
        ፈትሽ_ንጣብ((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_ስደድ('q'))
        ምንጪ = '''from ትግርኛ import 화면크기, 네모그리기, 그림기다리기, 출력, ስርዓት_ጌጋ
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ስርዓት_ጌጋ as ጌጋ:
    assert ጌጋ.መሐበሪ == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ስቐል_ፋይላት('화면시험.py', ምንጪ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_ስደድ('python /화면시험.py\n'))
        ፈትሽ_ንጣብ((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_ስደድ('q'))
        ምንጪ = '''import ትግርኛ.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("መጠን");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("ቅንጣብ"); }
        catch (잘못된인수예외 ጌጋ) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 አዐንግድ javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(ምንጪ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        ስቐል_ፋይላት('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_ስደድ('java 해상도경계시험\n'))
        ፈትሽ_ንጣብ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_ስደድ('q'))
        # 게스트 javac의 ሓገዝ_ዋጋ 문법으로 መጠን ሕቶ_ዋጋ·지우기·다섯 인수 그리기를 컴파일한다.
        ምንጪ = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=ትግርኛ.자체.화면.너비();
        int 높이=ትግርኛ.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        ትግርኛ.자체.화면.지우기(3153944);
        ትግርኛ.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        ትግርኛ.자체.출력.ጸሓፍ_መስመር("JAVA RESOLUTION PASS");
        ትግርኛ.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ስቐል_ፋይላት('해상도시험.java', ምንጪ.encode())
        결과 = ሽፋን('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', SMS_ስደድ('java 해상도시험\n'))
        ፈትሽ_ንጣብ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_ስደድ('q'))
        ስቐል_ፋይላት('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_ስደድ('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        ስእሊ_ዋጋ = ፈትሽ_ንጣብ((가로, 세로), (32, 80, 144))
        ስእሊ_ዋጋ.save(str(결과경로/(መጠን_ጽሑፍ_cdfada26+'.png')))
        ኣኺድ = len(ምዝጉብ_ሪጋ); ጠዉቕ_ዋጋ(가로+80, 세로+155)
        기다리기('SWING CLICK ሽም'.encode(), ኣኺድ)
        ኣኺድ = len(ምዝጉብ_ሪጋ); ጠዉቕ_ዋጋ(가로+385, 세로+15); 기다리기(b'jkoros-native> ', ኣኺድ)
        assert 'AFTER_RESOLUTION' in ሽፋን('echo AFTER_RESOLUTION')
        print('PASS:', መጠን_ጽሑፍ_cdfada26, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ምስጋር_ዋጋ: ምስጋር_ዋጋ.close()
        if ርሑቕ_ዋጋ: ርሑቕ_ዋጋ.close()
        if መስርሕ_ዋጋ.poll() is None:
            መስርሕ_ዋጋ.terminate()
            try: መስርሕ_ዋጋ.wait(timeout=8)
            except subprocess.TimeoutExpired: መስርሕ_ዋጋ.kill(); መስርሕ_ዋጋ.wait()
        መራፂ_a916db4e.close(); መስርሕ_ዋጋ.stdout.close()
        (결과경로/(መጠን_ጽሑፍ_cdfada26+'.log')).write_bytes(ምዝጉብ_ሪጋ)


def ኣኺድ():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    ምዝጉብ_ሪጋ = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ዘይቅቡል_ዋጋ in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'መሳርሒታት/ተግብር_ትእዛዝ.py'), '--resolution', ዘይቅቡል_ዋጋ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); ምዝጉብ_ሪጋ['resolutions'].append([너비, 높이])
        ምዝጉብ_ሪጋ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(ምዝጉብ_ሪጋ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ኣኺድ()
