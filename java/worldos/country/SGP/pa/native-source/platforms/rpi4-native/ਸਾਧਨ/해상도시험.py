#!/usr/bin/env python3
"""ਅਸਲ_ਸਮੱਗਰੀ QEMU/VNC에서 화면 ਆਕਾਰ·경계·ਵਿੰਡੋ ਖਿਸਕਾਉਣਾ_ਕੀਮਤ·Swing·언어별 그리기를 검사한다."""
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
from ਡੈਸਕਟੌਪ_ਦ੍ਰਿਸ਼ import 정확한값
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ


def 해상도시험(너비, 높이, ਮਾਪ_ਰਸਤਾ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ਆਕਾਰ_ਪਾਠ = '{}x{}'.format(너비, 높이)
    ਕਾਰਵਾਈ_ਕੀਮਤ = subprocess.Popen(['python3', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ਆਕਾਰ_ਪਾਠ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ਚੋਣਕਰਤਾ_a916db4e = selectors.DefaultSelector(); ਚੋਣਕਰਤਾ_a916db4e.register(ਕਾਰਵਾਈ_ਕੀਮਤ.stdout, selectors.EVENT_READ)
    ਲੌਗ_ਕਤਾਰ = bytearray(); ਰਿਮੋਟ_ਕੀਮਤ = None; ਸਥਾਂਨਤਰ_ਕੀਮਤ = None

    def 기다리기(ਸ਼ੋਅ_ਕੀਮਤ, ਚਲਾਓ_2=0):
        마감 = time.monotonic() + 60
        while ਸ਼ੋਅ_ਕੀਮਤ not in ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:]:
            if time.monotonic() > 마감 or ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is not None or b'HALTED' in ਲੌਗ_ਕਤਾਰ or b'PANIC:' in ਲੌਗ_ਕਤਾਰ:
                raise AssertionError(ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:].decode('utf-8', 'replace'))
            for ਇਵੈਂਟ, _ in ਚੋਣਕਰਤਾ_a916db4e.select(.1):
                ਸਮੱਗਰੀ = ਇਵੈਂਟ.fileobj.read(65536)
                if ਸਮੱਗਰੀ: ਲੌਗ_ਕਤਾਰ.extend(ਸਮੱਗਰੀ)
        return ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:].decode('utf-8', 'replace')

    def ਕਲਿਕ_ਕਰੋ_ਬਟਨ(ਪ੍ਰਤੀਕ, 눌림=True): ਰਿਮੋਟ_ਕੀਮਤ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ਪ੍ਰਤੀਕ))

    def SMS_ਭੇਜੋ(ਟੈਕਸਟ):
        ਚਲਾਓ_2 = len(ਲੌਗ_ਕਤਾਰ)
        for ਵਰਣ_ਕੀਮਤ in ਟੈਕਸਟ:
            ਪ੍ਰਤੀਕ = 0xff0d if ਵਰਣ_ਕੀਮਤ == '\n' else ord(ਵਰਣ_ਕੀਮਤ) if ord(ਵਰਣ_ਕੀਮਤ) < 256 else 0x1000000 | ord(ਵਰਣ_ਕੀਮਤ)
            ਕਲਿਕ_ਕਰੋ_ਬਟਨ(ਪ੍ਰਤੀਕ); ਕਲਿਕ_ਕਰੋ_ਬਟਨ(ਪ੍ਰਤੀਕ, False)
        return ਚਲਾਓ_2

    def ਸ਼ੈਲ(ਟੈਕਸਟ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_ਭੇਜੋ(ਟੈਕਸਟ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 눌림): ਰਿਮੋਟ_ਕੀਮਤ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ))

    def ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ): 가리키기(가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 1); 가리키기(가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 0)

    def ਬਿਟਮੈਪ_ਤਸਵੀਰ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ਅਸਲ_ਸਮੱਗਰੀ 너비를 쓴다.
        ਰਿਮੋਟ_ਕੀਮਤ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ = Image.new('RGB', (너비, 높이)); ਖੇਤਰ_ਕੀਮਤ = 0
        while True:
            종류 = 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ਲੰਬਾਈ_ਕੀਮਤ = struct.unpack('>I', 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 7)[3:])[0]; 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, ਲੰਬਾਈ_ਕੀਮਤ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 3)[1:])[0]
            for _ in range(개수):
                가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 폭, ਲੰਬਾਈ_ਕੀਮਤ, ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ_ਕੀਮਤ = struct.unpack('>HHHHi', 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 12))
                assert ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ_ਕੀਮਤ == 0 and 가로+폭 <= 너비 and ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ+ਲੰਬਾਈ_ਕੀਮਤ <= 높이
                ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.paste(Image.frombytes('RGB', (폭, ਲੰਬਾਈ_ਕੀਮਤ), 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 폭*ਲੰਬਾਈ_ਕੀਮਤ*4), 'raw', 'BGRX'), (가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ))
                ਖੇਤਰ_ਕੀਮਤ += 폭*ਲੰਬਾਈ_ਕੀਮਤ
            if ਖੇਤਰ_ਕੀਮਤ:
                assert ਖੇਤਰ_ਕੀਮਤ == 너비*높이, ਖੇਤਰ_ਕੀਮਤ
                return ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ

    def ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ(ਸਮਾਨ_ਕੀਮਤ, 색):
        마감 = time.monotonic()+10
        while True:
            ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ = ਬਿਟਮੈਪ_ਤਸਵੀਰ()
            if ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.getpixel(ਸਮਾਨ_ਕੀਮਤ) == 색: return ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ
            if time.monotonic() > 마감: raise AssertionError((ਸਮਾਨ_ਕੀਮਤ, ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.getpixel(ਸਮਾਨ_ਕੀਮਤ), 색))

    def ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ(ਨਾਂ, ਸਮੱਗਰੀ): ਸਥਾਂਨਤਰ_ਕੀਮਤ.storbinary('STOR '+ਨਾਂ, io.BytesIO(ਸਮੱਗਰੀ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ਆਕਾਰ_ਪਾਠ+' RGB32').encode() in ਲੌਗ_ਕਤਾਰ
        print('BOOT:', ਆਕਾਰ_ਪਾਠ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ਲੌਗ_ਕਤਾਰ).group(1))
        ਰਿਮੋਟ_ਕੀਮਤ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 12) == b'RFB 003.008\n'; ਰਿਮੋਟ_ਕੀਮਤ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 1)[0]); ਰਿਮੋਟ_ਕੀਮਤ.sendall(b'\x01')
        assert 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 4) == b'\0'*4; ਰਿਮੋਟ_ਕੀਮਤ.sendall(b'\x01')
        초기 = 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ਰਿਮੋਟ_ਕੀਮਤ, struct.unpack('>I', 초기[20:])[0])
        ਰਿਮੋਟ_ਕੀਮਤ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ਰਿਮੋਟ_ਕੀਮਤ.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ((너비-568, 높이-360), (32, 80, 144))
        ਚਲਾਓ_2 = len(ਲੌਗ_ਕਤਾਰ); ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ਚਲਾਓ_2)
        ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ((너비-568, 높이-360), (24, 32, 48))
        ਚਲਾਓ_2 = len(ਲੌਗ_ਕਤਾਰ); ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(80, 16); 기다리기(b'TERMINAL FOCUS 1', ਚਲਾਓ_2)
        ਸ਼ੈਲ('ftpd start')
        ਸਥਾਂਨਤਰ_ਕੀਮਤ = ftplib.FTP(); ਸਥਾਂਨਤਰ_ਕੀਮਤ.encoding = 'utf-8'; ਸਥਾਂਨਤਰ_ਕੀਮਤ.connect('127.0.0.1', 접속번호, timeout=20); ਸਥਾਂਨਤਰ_ਕੀਮਤ.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ਕਲਿਪ 밖·빈 사각형을 포함한다.
        ਸਰੋਤ = '''#include <화면규약.h>
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
    ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('화면시험.c', ਸਰੋਤ.encode())
        assert 'exit 0' in ਸ਼ੈਲ('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_ਭੇਜੋ('run /화면시험\n'))
        ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_ਭੇਜੋ('q'))
        ਸਰੋਤ = '''from ਪੰਜਾਬੀ import 화면크기, 네모그리기, 그림기다리기, ਆਉਟਪੁੱਟ, ਪਰਬੰਧ_ਗਲਤ
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ਪਰਬੰਧ_ਗਲਤ as ਗਲਤੀ:
    assert ਗਲਤੀ.ਅਨੁਕ੍ਰਮਣਿਕਾ == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
ਆਉਟਪੁੱਟ("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('화면시험.py', ਸਰੋਤ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_ਭੇਜੋ('python /화면시험.py\n'))
        ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_ਭੇਜੋ('q'))
        ਸਰੋਤ = '''import ਪੰਜਾਬੀ.자체.*;
public class 해상도시험 {
    public static void main(String[] ਆਰਗੂਮੈਂਟ) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("ਆਕਾਰ");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("ਕਲਿਪ"); }
        catch (잘못된인수예외 ਗਲਤੀ) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 ਹੋਸਟ javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = ਮਾਪ_ਰਸਤਾ/'해상도경계시험.java'
        경계원문.write_text(ਸਰੋਤ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist/jkoros-native-korean.jar'), '-d', str(ਮਾਪ_ਰਸਤਾ), str(경계원문)])
        ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('해상도경계시험.class', (ਮਾਪ_ਰਸਤਾ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_ਭੇਜੋ('java 해상도경계시험\n'))
        ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_ਭੇਜੋ('q'))
        # 게스트 javac의 ਸਮਰਥਨ_ਕੀਮਤ 문법으로 ਆਕਾਰ ਪੜਤਾਲ_ਕੀਮਤ·지우기·다섯 ਆਰਗੂਮੈਂਟ 그리기를 컴파일한다.
        ਸਰੋਤ = '''public class 해상도시험 {
    public static void main(String[] ਆਰਗੂਮੈਂਟ) {
        int 너비=ਪੰਜਾਬੀ.자체.화면.너비();
        int 높이=ਪੰਜਾਬੀ.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        ਪੰਜਾਬੀ.자체.화면.지우기(3153944);
        ਪੰਜਾਬੀ.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        ਪੰਜਾਬੀ.자체.ਆਉਟਪੁੱਟ.ਲਿੱਖੋ_ਕਤਾਰ("JAVA RESOLUTION PASS");
        ਪੰਜਾਬੀ.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('해상도시험.java', ਸਰੋਤ.encode())
        ਮਾਪ = ਸ਼ੈਲ('javac 해상도시험.java'); assert 'exit 0' in ਮਾਪ, ਮਾਪ
        기다리기(b'JAVA RESOLUTION PASS', SMS_ਭੇਜੋ('java 해상도시험\n'))
        ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_ਭੇਜੋ('q'))
        ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('스윙시험.class', (ਮਾਪ_ਰਸਤਾ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_ਭੇਜੋ('java 스윙시험\n'))
        가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ = (너비-400)//2, (높이-280)//2
        ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ = ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ((가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ), (32, 80, 144))
        ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.save(str(ਮਾਪ_ਰਸਤਾ/(ਆਕਾਰ_ਪਾਠ+'.png')))
        ਚਲਾਓ_2 = len(ਲੌਗ_ਕਤਾਰ); ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(가로+80, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ+155)
        기다리기('SWING CLICK ਨਾਂ'.encode(), ਚਲਾਓ_2)
        ਚਲਾਓ_2 = len(ਲੌਗ_ਕਤਾਰ); ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(가로+385, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ+15); 기다리기(b'jkoros-native> ', ਚਲਾਓ_2)
        assert 'AFTER_RESOLUTION' in ਸ਼ੈਲ('echo AFTER_RESOLUTION')
        print('PASS:', ਆਕਾਰ_ਪਾਠ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ਸਥਾਂਨਤਰ_ਕੀਮਤ: ਸਥਾਂਨਤਰ_ਕੀਮਤ.close()
        if ਰਿਮੋਟ_ਕੀਮਤ: ਰਿਮੋਟ_ਕੀਮਤ.close()
        if ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is None:
            ਕਾਰਵਾਈ_ਕੀਮਤ.terminate()
            try: ਕਾਰਵਾਈ_ਕੀਮਤ.wait(timeout=8)
            except subprocess.TimeoutExpired: ਕਾਰਵਾਈ_ਕੀਮਤ.kill(); ਕਾਰਵਾਈ_ਕੀਮਤ.wait()
        ਚੋਣਕਰਤਾ_a916db4e.close(); ਕਾਰਵਾਈ_ਕੀਮਤ.stdout.close()
        (ਮਾਪ_ਰਸਤਾ/(ਆਕਾਰ_ਪਾਠ+'.log')).write_bytes(ਲੌਗ_ਕਤਾਰ)


def ਚਲਾਓ_2():
    ਮਾਪ_ਰਸਤਾ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/resolution'; ਮਾਪ_ਰਸਤਾ.mkdir(parents=True, exist_ok=True)
    ਲੌਗ_ਕਤਾਰ = {'passed': False, 'kernel_sha256': hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ਅਯੋਗ_ਕੀਮਤ in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ਮਾਪ = subprocess.run(['python3', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py'), '--resolution', ਅਯੋਗ_ਕੀਮਤ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ਮਾਪ.returncode == 2 and b'--resolution' in ਮਾਪ.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ਮਾਪ_ਰਸਤਾ), str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, ਮਾਪ_ਰਸਤਾ); ਲੌਗ_ਕਤਾਰ['resolutions'].append([너비, 높이])
        ਲੌਗ_ਕਤਾਰ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (ਮਾਪ_ਰਸਤਾ/'report.json').write_text(json.dumps(ਲੌਗ_ਕਤਾਰ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ਚਲਾਓ_2()
