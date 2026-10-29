#!/usr/bin/env python3
"""ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ QEMU/VNC에서 화면 ᎢᎩᏓ·경계·ᏦᎳᏂ ᎯᎲᎾ_ᏧᎬᏩᎶᏗᏯ·Swing·언어별 그리기를 검사한다."""
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
from ᎦᏍᎩᎶᎩ_ᎦᏚ_ᎯᎪᎵᏯ import 정확한값
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준


def ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᎠᏓᎪᎵᏰᏍᎩ(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ᎢᎩᏓ_ᎠᎪᎵᏰᏗ = '{}x{}'.format(너비, 높이)
    ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ = subprocess.Popen(['python3', str(기준/'도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ᎢᎩᏓ_ᎠᎪᎵᏰᏗ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ᎠᏑᏰᏍᎩ_a916db4e = selectors.DefaultSelector(); ᎠᏑᏰᏍᎩ_a916db4e.register(ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdout, selectors.EVENT_READ)
    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = bytearray(); 원격 = None; ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ = None

    def 기다리기(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ, ᎠᎢᏎᏍᏗ=0):
        마감 = time.monotonic() + 60
        while ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ not in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:]:
            if time.monotonic() > 마감 or ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is not None or b'HALTED' in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ or b'PANIC:' in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ:
                raise AssertionError(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:].decode('utf-8', 'replace'))
            for ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ, _ in ᎠᏑᏰᏍᎩ_a916db4e.select(.1):
                ᎦᏟᏌᏅᎯ = ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.fileobj.read(65536)
                if ᎦᏟᏌᏅᎯ: ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.extend(ᎦᏟᏌᏅᎯ)
        return ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:].decode('utf-8', 'replace')

    def ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(기호, 눌림=True): 원격.sendall(struct.pack('>BBHI', 4, int(눌림), 0, 기호))

    def ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ(ᎠᎪᎵᏰᏗ):
        ᎠᎢᏎᏍᏗ = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
        for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in ᎠᎪᎵᏰᏗ:
            기호 = 0xff0d if ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ == '\n' else ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ) if ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ) < 256 else 0x1000000 | ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ)
            ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(기호); ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(기호, False)
        return ᎠᎢᏎᏍᏗ

    def ᎤᏯᏍᎦ(ᎠᎪᎵᏰᏗ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ(ᎠᎪᎵᏰᏗ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): 원격.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def bitmap_ᎤᏓᏴᎳᏛ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 너비를 쓴다.
        원격.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ = Image.new('RGB', (너비, 높이)); ᎢᎬᎾᏕᎾ_ᏧᎬᏩᎶᏗᏯ = 0
        while True:
            종류 = 정확한값(원격, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = struct.unpack('>I', 정확한값(원격, 7)[3:])[0]; 정확한값(원격, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(원격, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ, ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ = struct.unpack('>HHHHi', 정확한값(원격, 12))
                assert ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ == 0 and 가로+폭 <= 너비 and 세로+ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ <= 높이
                ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.paste(Image.frombytes('RGB', (폭, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ), 정확한값(원격, 폭*ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ*4), 'raw', 'BGRX'), (가로, 세로))
                ᎢᎬᎾᏕᎾ_ᏧᎬᏩᎶᏗᏯ += 폭*ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ
            if ᎢᎬᎾᏕᎾ_ᏧᎬᏩᎶᏗᏯ:
                assert ᎢᎬᎾᏕᎾ_ᏧᎬᏩᎶᏗᏯ == 너비*높이, ᎢᎬᎾᏕᎾ_ᏧᎬᏩᎶᏗᏯ
                return ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ

    def ᎪᎯᏳᏔᏅ_pel(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ = bitmap_ᎤᏓᏴᎳᏛ()
            if ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.getpixel(좌표) == 색: return ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ
            if time.monotonic() > 마감: raise AssertionError((좌표, ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.getpixel(좌표), 색))

    def 올리기(ᏚᏙᎥᎢ, ᎦᏟᏌᏅᎯ): ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.storbinary('STOR '+ᏚᏙᎥᎢ, io.BytesIO(ᎦᏟᏌᏅᎯ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ᎢᎩᏓ_ᎠᎪᎵᏰᏗ+' RGB32').encode() in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ
        print('BOOT:', ᎢᎩᏓ_ᎠᎪᎵᏰᏗ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ).group(1))
        원격 = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(원격, 12) == b'RFB 003.008\n'; 원격.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(원격, 정확한값(원격, 1)[0]); 원격.sendall(b'\x01')
        assert 정확한값(원격, 4) == b'\0'*4; 원격.sendall(b'\x01')
        초기 = 정확한값(원격, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(원격, struct.unpack('>I', 초기[20:])[0])
        원격.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        원격.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ᎪᎯᏳᏔᏅ_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ᎪᎯᏳᏔᏅ_pel((너비-568, 높이-360), (32, 80, 144))
        ᎠᎢᏎᏍᏗ = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ); ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ᎠᎢᏎᏍᏗ)
        ᎪᎯᏳᏔᏅ_pel((너비-568, 높이-360), (24, 32, 48))
        ᎠᎢᏎᏍᏗ = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ); ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(80, 16); 기다리기(b'TERMINAL FOCUS 1', ᎠᎢᏎᏍᏗ)
        ᎤᏯᏍᎦ('ftpd start')
        ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ = ftplib.FTP(); ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.encoding = 'utf-8'; ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.connect('127.0.0.1', 접속번호, timeout=20); ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ᎠᎬᎭᎸᏓ_ᏗᏓᏴᎳᏛᏙᏗ 밖·빈 사각형을 포함한다.
        ᎦᏟᏌᏅᎯ_0201f362 = '''#include <화면규약.h>
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
    ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏟᏌᏅᎯ(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('화면시험.c', ᎦᏟᏌᏅᎯ_0201f362.encode())
        assert 'exit 0' in ᎤᏯᏍᎦ('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('run /화면시험\n'))
        ᎪᎯᏳᏔᏅ_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('q'))
        ᎦᏟᏌᏅᎯ_0201f362 = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, ᏄᏍᏗᏓᏅᎢ_ᎦᎵᏓᏍᏔᏅ
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ᏄᏍᏗᏓᏅᎢ_ᎦᎵᏓᏍᏔᏅ as ᎦᎵᏓᏍᏔᏅ:
    assert ᎦᎵᏓᏍᏔᏅ.ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('화면시험.py', ᎦᏟᏌᏅᎯ_0201f362.encode())
        기다리기(b'PYTHON RESOLUTION PASS', ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('python /화면시험.py\n'))
        ᎪᎯᏳᏔᏅ_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('q'))
        ᎦᏟᏌᏅᎯ_0201f362 = '''import 한국어.자체.*;
public class ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᎠᏓᎪᎵᏰᏍᎩ {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("ᎢᎩᏓ");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("ᎠᎬᎭᎸᏓ_ᏗᏓᏴᎳᏛᏙᏗ"); }
        catch (잘못된인수예외 ᎦᎵᏓᏍᏔᏅ) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 ᎠᏁᏢᏍᎩ javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(ᎦᏟᏌᏅᎯ_0201f362.replace('class ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᎠᏓᎪᎵᏰᏍᎩ', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        올리기('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('java 해상도경계시험\n'))
        ᎪᎯᏳᏔᏅ_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('q'))
        # 게스트 javac의 ᎦᎫᏍᏛᏗ_ᏧᎬᏩᎶᏗᏯ 문법으로 ᎢᎩᏓ ᎠᏛᏛᎲᏍᎩ_ᏧᎬᏩᎶᏗᏯ·지우기·다섯 인수 그리기를 컴파일한다.
        ᎦᏟᏌᏅᎯ_0201f362 = '''public class ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᎠᏓᎪᎵᏰᏍᎩ {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.ᎪᏪᎶᏗ_ᏚᏓᏅᏅᎢ("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᎠᏓᎪᎵᏰᏍᎩ.java', ᎦᏟᏌᏅᎯ_0201f362.encode())
        결과 = ᎤᏯᏍᎦ('javac ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᎠᏓᎪᎵᏰᏍᎩ.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('java ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᎠᏓᎪᎵᏰᏍᎩ\n'))
        ᎪᎯᏳᏔᏅ_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('q'))
        올리기('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ = ᎪᎯᏳᏔᏅ_pel((가로, 세로), (32, 80, 144))
        ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.save(str(결과경로/(ᎢᎩᏓ_ᎠᎪᎵᏰᏗ+'.png')))
        ᎠᎢᏎᏍᏗ = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ); ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(가로+80, 세로+155)
        기다리기('SWING CLICK ᏚᏙᎥᎢ'.encode(), ᎠᎢᏎᏍᏗ)
        ᎠᎢᏎᏍᏗ = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ); ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(가로+385, 세로+15); 기다리기(b'jkoros-native> ', ᎠᎢᏎᏍᏗ)
        assert 'AFTER_RESOLUTION' in ᎤᏯᏍᎦ('echo AFTER_RESOLUTION')
        print('PASS:', ᎢᎩᏓ_ᎠᎪᎵᏰᏗ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ: ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.close()
        if 원격: 원격.close()
        if ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is None:
            ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.terminate()
            try: ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait(timeout=8)
            except subprocess.TimeoutExpired: ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.kill(); ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait()
        ᎠᏑᏰᏍᎩ_a916db4e.close(); ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdout.close()
        (결과경로/(ᎢᎩᏓ_ᎠᎪᎵᏰᏗ+'.log')).write_bytes(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)


def ᎠᎢᏎᏍᏗ():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ᏂᏓᏓᏂᎸᎬᎾ_ᏧᎬᏩᎶᏗᏯ in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py'), '--resolution', ᏂᏓᏓᏂᎸᎬᎾ_ᏧᎬᏩᎶᏗᏯ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᎠᏓᎪᎵᏰᏍᎩ(너비, 높이, 결과경로); ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ['resolutions'].append([너비, 높이])
        ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ᎠᎢᏎᏍᏗ()
