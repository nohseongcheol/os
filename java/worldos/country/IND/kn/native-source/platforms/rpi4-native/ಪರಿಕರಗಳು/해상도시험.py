#!/usr/bin/env python3
"""ನಿಜವಾದ_ಡೇಟಾ QEMU/VNC에서 화면 ಗಾತ್ರ·경계·ವಿಂಡೋ ಸರಿಸು_ಮೌಲ್ಯ·Swing·언어별 그리기를 검사한다."""
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
from ಡೆಸ್ಕ್_ಟಾಪ್_ವೀಕ್ಷಣೆ import 정확한값
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ


def 해상도시험(너비, 높이, ಮಾಪನ_ಹಾದಿ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); ಪೋರ್ಟ್_ಸಂಖ್ಯೆ = 임시.getsockname()[1]
    ಗಾತ್ರಿಸು_ಪಠ್ಯ = '{}x{}'.format(너비, 높이)
    ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = subprocess.Popen(['python3', str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ), '--resolution', ಗಾತ್ರಿಸು_ಪಠ್ಯ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ಸೆಲೆಕ್ಟರ್_a916db4e = selectors.DefaultSelector(); ಸೆಲೆಕ್ಟರ್_a916db4e.register(ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdout, selectors.EVENT_READ)
    ಲಾಗ್_ದಾಖಲೆ = bytearray(); ರಿಮೋಟ್_ಮೌಲ್ಯ = None; ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ = None

    def 기다리기(ಶೋ_ಮೌಲ್ಯ, ಚಲಾಯಿಸು_2=0):
        마감 = time.monotonic() + 60
        while ಶೋ_ಮೌಲ್ಯ not in ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:]:
            if time.monotonic() > 마감 or ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is not None or b'HALTED' in ಲಾಗ್_ದಾಖಲೆ or b'PANIC:' in ಲಾಗ್_ದಾಖಲೆ:
                raise AssertionError(ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:].decode('utf-8', 'replace'))
            for ಸಂಗತಿ, _ in ಸೆಲೆಕ್ಟರ್_a916db4e.select(.1):
                ಡೇಟಾ = ಸಂಗತಿ.fileobj.read(65536)
                if ಡೇಟಾ: ಲಾಗ್_ದಾಖಲೆ.extend(ಡೇಟಾ)
        return ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:].decode('utf-8', 'replace')

    def ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(ಚಿಹ್ನೆ, 눌림=True): ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ಚಿಹ್ನೆ))

    def SMS_ಕಳುಹಿಸು(ಪಠ್ಯ):
        ಚಲಾಯಿಸು_2 = len(ಲಾಗ್_ದಾಖಲೆ)
        for ಅಕ್ಷರ_ಮೌಲ್ಯ in ಪಠ್ಯ:
            ಚಿಹ್ನೆ = 0xff0d if ಅಕ್ಷರ_ಮೌಲ್ಯ == '\n' else ord(ಅಕ್ಷರ_ಮೌಲ್ಯ) if ord(ಅಕ್ಷರ_ಮೌಲ್ಯ) < 256 else 0x1000000 | ord(ಅಕ್ಷರ_ಮೌಲ್ಯ)
            ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(ಚಿಹ್ನೆ); ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(ಚಿಹ್ನೆ, False)
        return ಚಲಾಯಿಸು_2

    def ಶೆಲ್(ಪಠ್ಯ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_ಕಳುಹಿಸು(ಪಠ್ಯ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, ಲಂಬ_ಹುದ್ದೆ, 눌림): ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ಲಂಬ_ಹುದ್ದೆ))

    def ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(가로, ಲಂಬ_ಹುದ್ದೆ): 가리키기(가로, ಲಂಬ_ಹುದ್ದೆ, 1); 가리키기(가로, ಲಂಬ_ಹುದ್ದೆ, 0)

    def ಬಿಟ್_ಮ್ಯಾಪ್_ಇಮೇಜ್():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ನಿಜವಾದ_ಡೇಟಾ 너비를 쓴다.
        ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ = Image.new('RGB', (너비, 높이)); ವರ್ಗ_ಮೌಲ್ಯ_9285603e = 0
        while True:
            종류 = 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ಉದ್ದ_ಮೌಲ್ಯ = struct.unpack('>I', 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 7)[3:])[0]; 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, ಉದ್ದ_ಮೌಲ್ಯ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 3)[1:])[0]
            for _ in range(개수):
                가로, ಲಂಬ_ಹುದ್ದೆ, 폭, ಉದ್ದ_ಮೌಲ್ಯ, ಎನ್ಕೋಡಿಂಗ್_ಮೌಲ್ಯ = struct.unpack('>HHHHi', 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 12))
                assert ಎನ್ಕೋಡಿಂಗ್_ಮೌಲ್ಯ == 0 and 가로+폭 <= 너비 and ಲಂಬ_ಹುದ್ದೆ+ಉದ್ದ_ಮೌಲ್ಯ <= 높이
                ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.paste(Image.frombytes('RGB', (폭, ಉದ್ದ_ಮೌಲ್ಯ), 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 폭*ಉದ್ದ_ಮೌಲ್ಯ*4), 'raw', 'BGRX'), (가로, ಲಂಬ_ಹುದ್ದೆ))
                ವರ್ಗ_ಮೌಲ್ಯ_9285603e += 폭*ಉದ್ದ_ಮೌಲ್ಯ
            if ವರ್ಗ_ಮೌಲ್ಯ_9285603e:
                assert ವರ್ಗ_ಮೌಲ್ಯ_9285603e == 너비*높이, ವರ್ಗ_ಮೌಲ್ಯ_9285603e
                return ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ

    def ಚೆಕ್_ಪೆಲ್(ಸಮನ್ವಯ_ಮೌಲ್ಯ, 색):
        마감 = time.monotonic()+10
        while True:
            ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ = ಬಿಟ್_ಮ್ಯಾಪ್_ಇಮೇಜ್()
            if ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.getpixel(ಸಮನ್ವಯ_ಮೌಲ್ಯ) == 색: return ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ
            if time.monotonic() > 마감: raise AssertionError((ಸಮನ್ವಯ_ಮೌಲ್ಯ, ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.getpixel(ಸಮನ್ವಯ_ಮೌಲ್ಯ), 색))

    def ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು(ಹೆಸರು, ಡೇಟಾ): ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.storbinary('STOR '+ಹೆಸರು, io.BytesIO(ಡೇಟಾ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ಗಾತ್ರಿಸು_ಪಠ್ಯ+' RGB32').encode() in ಲಾಗ್_ದಾಖಲೆ
        print('BOOT:', ಗಾತ್ರಿಸು_ಪಠ್ಯ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ಲಾಗ್_ದಾಖಲೆ).group(1))
        ರಿಮೋಟ್_ಮೌಲ್ಯ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 12) == b'RFB 003.008\n'; ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 1)[0]); ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(b'\x01')
        assert 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 4) == b'\0'*4; ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(b'\x01')
        초기 = 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, struct.unpack('>I', 초기[20:])[0])
        ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ಚೆಕ್_ಪೆಲ್((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ಚೆಕ್_ಪೆಲ್((너비-568, 높이-360), (32, 80, 144))
        ಚಲಾಯಿಸು_2 = len(ಲಾಗ್_ದಾಖಲೆ); ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ಚಲಾಯಿಸು_2)
        ಚೆಕ್_ಪೆಲ್((너비-568, 높이-360), (24, 32, 48))
        ಚಲಾಯಿಸು_2 = len(ಲಾಗ್_ದಾಖಲೆ); ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(80, 16); 기다리기(b'TERMINAL FOCUS 1', ಚಲಾಯಿಸು_2)
        ಶೆಲ್('ftpd start')
        ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ = ftplib.FTP(); ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.encoding = 'utf-8'; ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.connect('127.0.0.1', ಪೋರ್ಟ್_ಸಂಖ್ಯೆ, timeout=20); ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ಕ್ಲಿಪ್ 밖·빈 사각형을 포함한다.
        ಮೂಲ = '''#include <화면규약.h>
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
    ಬರೆ_ಫೈಲ್_ಡೇಟಾ(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('화면시험.c', ಮೂಲ.encode())
        assert 'exit 0' in ಶೆಲ್('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_ಕಳುಹಿಸು('run /화면시험\n'))
        ಚೆಕ್_ಪೆಲ್((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_ಕಳುಹಿಸು('q'))
        ಮೂಲ = '''from ಕನ್ನಡ import 화면크기, 네모그리기, 그림기다리기, ಔಟ್_ಪುಟ್, ಸಿಸ್ಟಂ_ದೋಷ
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ಸಿಸ್ಟಂ_ದೋಷ as ದೋಷ:
    assert ದೋಷ.ಪದಸೂಚಿ == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
ಔಟ್_ಪುಟ್("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('화면시험.py', ಮೂಲ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_ಕಳುಹಿಸು('python /화면시험.py\n'))
        ಚೆಕ್_ಪೆಲ್((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_ಕಳುಹಿಸು('q'))
        ಮೂಲ = '''import ಕನ್ನಡ.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new ಸ್ಥಿತಿ_ವಿನಾಯಿತಿ("ಗಾತ್ರ");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new ಸ್ಥಿತಿ_ವಿನಾಯಿತಿ("ಕ್ಲಿಪ್"); }
        catch (ಅಮಾನ್ಯ_ವಾದ_ವಿನಾಯಿತಿ ದೋಷ) { }
        화면.ಅಳಿಸು_ನಮೂದು(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # ವಿನಾಯಿತಿ 처리는 ಹೋಸ್ಟ್ javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = ಮಾಪನ_ಹಾದಿ/'해상도경계시험.java'
        경계원문.write_text(ಮೂಲ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ಬಿಂಬಿಸು_ಮೂಲ/'dist/jkoros-native-korean.jar'), '-d', str(ಮಾಪನ_ಹಾದಿ), str(경계원문)])
        ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('해상도경계시험.class', (ಮಾಪನ_ಹಾದಿ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_ಕಳುಹಿಸು('java 해상도경계시험\n'))
        ಚೆಕ್_ಪೆಲ್((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_ಕಳುಹಿಸು('q'))
        # 게스트 javac의 ಬೆಂಬಲ_ಮೌಲ್ಯ 문법으로 ಗಾತ್ರ ಪ್ರಶ್ನಾವಳಿ_ಮೌಲ್ಯ·ಅಳಿಸು_ನಮೂದು·다섯 인수 그리기를 컴파일한다.
        ಮೂಲ = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=ಕನ್ನಡ.자체.화면.너비();
        int 높이=ಕನ್ನಡ.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        ಕನ್ನಡ.자체.화면.ಅಳಿಸು_ನಮೂದು(3153944);
        ಕನ್ನಡ.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        ಕನ್ನಡ.자체.ಔಟ್_ಪುಟ್.ಬರೆ_ಸಾಲು("JAVA RESOLUTION PASS");
        ಕನ್ನಡ.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('해상도시험.java', ಮೂಲ.encode())
        ಮಾಪನ = ಶೆಲ್('javac 해상도시험.java'); assert 'exit 0' in ಮಾಪನ, ಮಾಪನ
        기다리기(b'JAVA RESOLUTION PASS', SMS_ಕಳುಹಿಸು('java 해상도시험\n'))
        ಚೆಕ್_ಪೆಲ್((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_ಕಳುಹಿಸು('q'))
        ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('스윙시험.class', (ಮಾಪನ_ಹಾದಿ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_ಕಳುಹಿಸು('java 스윙시험\n'))
        가로, ಲಂಬ_ಹುದ್ದೆ = (너비-400)//2, (높이-280)//2
        ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ = ಚೆಕ್_ಪೆಲ್((가로, ಲಂಬ_ಹುದ್ದೆ), (32, 80, 144))
        ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.save(str(ಮಾಪನ_ಹಾದಿ/(ಗಾತ್ರಿಸು_ಪಠ್ಯ+'.png')))
        ಚಲಾಯಿಸು_2 = len(ಲಾಗ್_ದಾಖಲೆ); ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(가로+80, ಲಂಬ_ಹುದ್ದೆ+155)
        기다리기('SWING CLICK ಹೆಸರು'.encode(), ಚಲಾಯಿಸು_2)
        ಚಲಾಯಿಸು_2 = len(ಲಾಗ್_ದಾಖಲೆ); ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(가로+385, ಲಂಬ_ಹುದ್ದೆ+15); 기다리기(b'jkoros-native> ', ಚಲಾಯಿಸು_2)
        assert 'AFTER_RESOLUTION' in ಶೆಲ್('echo AFTER_RESOLUTION')
        print('PASS:', ಗಾತ್ರಿಸು_ಪಠ್ಯ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ: ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.close()
        if ರಿಮೋಟ್_ಮೌಲ್ಯ: ರಿಮೋಟ್_ಮೌಲ್ಯ.close()
        if ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is None:
            ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.terminate()
            try: ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait(timeout=8)
            except subprocess.TimeoutExpired: ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.kill(); ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait()
        ಸೆಲೆಕ್ಟರ್_a916db4e.close(); ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdout.close()
        (ಮಾಪನ_ಹಾದಿ/(ಗಾತ್ರಿಸು_ಪಠ್ಯ+'.log')).write_bytes(ಲಾಗ್_ದಾಖಲೆ)


def ಚಲಾಯಿಸು_2():
    ಮಾಪನ_ಹಾದಿ = ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/resolution'; ಮಾಪನ_ಹಾದಿ.mkdir(parents=True, exist_ok=True)
    ಲಾಗ್_ದಾಖಲೆ = {'passed': False, 'kernel_sha256': hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ಅಮಾನ್ಯ_ಮೌಲ್ಯ in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ಮಾಪನ = subprocess.run(['python3', str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py'), '--resolution', ಅಮಾನ್ಯ_ಮೌಲ್ಯ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ಮಾಪನ.returncode == 2 and b'--resolution' in ಮಾಪನ.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ಮಾಪನ_ಹಾದಿ), str(ಬಿಂಬಿಸು_ಮೂಲ/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, ಮಾಪನ_ಹಾದಿ); ಲಾಗ್_ದಾಖಲೆ['resolutions'].append([너비, 높이])
        ಲಾಗ್_ದಾಖಲೆ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (ಮಾಪನ_ಹಾದಿ/'report.json').write_text(json.dumps(ಲಾಗ್_ದಾಖಲೆ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ಚಲಾಯಿಸು_2()
