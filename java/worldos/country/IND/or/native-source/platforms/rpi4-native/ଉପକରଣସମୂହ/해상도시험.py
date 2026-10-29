#!/usr/bin/env python3
"""ପ୍ରକୃତ_ଡାଟା QEMU/VNC에서 화면 ଆକାର·경계·ଓ୍ୱିଣ୍ଡୋ ଘୁଞ୍ଚାଇବା_ମୂଲ୍ୟ·Swing·언어별 그리기를 검사한다."""
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
from ଡେସ୍କଟପ୍_ଭିୟୁ import 정확한값
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍


def 해상도시험(너비, 높이, ମାପ_ପଥ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); ପୋର୍ଟ୍_ନମ୍ଵର୍ = 임시.getsockname()[1]
    ଅକାର_ପାଠ = '{}x{}'.format(너비, 높이)
    ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = subprocess.Popen(['python3', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(ପୋର୍ଟ୍_ନମ୍ଵର୍), '--resolution', ଅକାର_ପାଠ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ଚୟନକାରୀ_a916db4e = selectors.DefaultSelector(); ଚୟନକାରୀ_a916db4e.register(ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdout, selectors.EVENT_READ)
    ଲଗ୍_ଧାଡ଼ି = bytearray(); ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ = None; ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ = None

    def 기다리기(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ, ଚଳାନ୍ତୁ=0):
        마감 = time.monotonic() + 60
        while ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ not in ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:]:
            if time.monotonic() > 마감 or ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is not None or b'HALTED' in ଲଗ୍_ଧାଡ଼ି or b'PANIC:' in ଲଗ୍_ଧାଡ଼ି:
                raise AssertionError(ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:].decode('utf-8', 'replace'))
            for ଘଟଣା, _ in ଚୟନକାରୀ_a916db4e.select(.1):
                ଡାଟା = ଘଟଣା.fileobj.read(65536)
                if ଡାଟା: ଲଗ୍_ଧାଡ଼ି.extend(ଡାଟା)
        return ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:].decode('utf-8', 'replace')

    def କ୍ଲିକ୍_କରିବା_ବଟନ୍(ସଙ୍କେତ, 눌림=True): ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ସଙ୍କେତ))

    def SMS_ପ୍ରେରଣ_କରନ୍ତୁ(ପାଠ୍ଯ):
        ଚଳାନ୍ତୁ = len(ଲଗ୍_ଧାଡ଼ି)
        for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in ପାଠ୍ଯ:
            ସଙ୍କେତ = 0xff0d if ବର୍ଣ୍ଣ_ମୂଲ୍ୟ == '\n' else ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ) if ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ) < 256 else 0x1000000 | ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ)
            କ୍ଲିକ୍_କରିବା_ବଟନ୍(ସଙ୍କେତ); କ୍ଲିକ୍_କରିବା_ବଟନ୍(ସଙ୍କେତ, False)
        return ଚଳାନ୍ତୁ

    def ଖୋଳ(ପାଠ୍ଯ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_ପ୍ରେରଣ_କରନ୍ତୁ(ପାଠ୍ଯ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 눌림): ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି))

    def କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି): 가리키기(가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 1); 가리키기(가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 0)

    def ବିଟ୍_ମ୍ୟାପ୍_ଚିତ୍ର():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ପ୍ରକୃତ_ଡାଟା 너비를 쓴다.
        ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ଅଙ୍କନ_ମୂଲ୍ୟ = Image.new('RGB', (너비, 높이)); ବର୍ଗ_ମୂଲ୍ୟ_9285603e = 0
        while True:
            종류 = 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = struct.unpack('>I', 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 7)[3:])[0]; 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 3)[1:])[0]
            for _ in range(개수):
                가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 폭, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ, ଏନକୋଡିଂ_ମୂଲ୍ୟ = struct.unpack('>HHHHi', 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 12))
                assert ଏନକୋଡିଂ_ମୂଲ୍ୟ == 0 and 가로+폭 <= 너비 and ଅନୁଲମ୍ବ_ସ୍ଥିତି+ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ <= 높이
                ଅଙ୍କନ_ମୂଲ୍ୟ.paste(Image.frombytes('RGB', (폭, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ), 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 폭*ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ*4), 'raw', 'BGRX'), (가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି))
                ବର୍ଗ_ମୂଲ୍ୟ_9285603e += 폭*ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ
            if ବର୍ଗ_ମୂଲ୍ୟ_9285603e:
                assert ବର୍ଗ_ମୂଲ୍ୟ_9285603e == 너비*높이, ବର୍ଗ_ମୂଲ୍ୟ_9285603e
                return ଅଙ୍କନ_ମୂଲ୍ୟ

    def ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍(ସଂଯୋଜନ_ମୂଲ୍ୟ, 색):
        마감 = time.monotonic()+10
        while True:
            ଅଙ୍କନ_ମୂଲ୍ୟ = ବିଟ୍_ମ୍ୟାପ୍_ଚିତ୍ର()
            if ଅଙ୍କନ_ମୂଲ୍ୟ.getpixel(ସଂଯୋଜନ_ମୂଲ୍ୟ) == 색: return ଅଙ୍କନ_ମୂଲ୍ୟ
            if time.monotonic() > 마감: raise AssertionError((ସଂଯୋଜନ_ମୂଲ୍ୟ, ଅଙ୍କନ_ମୂଲ୍ୟ.getpixel(ସଂଯୋଜନ_ମୂଲ୍ୟ), 색))

    def ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ(ନାମ, ଡାଟା): ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.storbinary('STOR '+ନାମ, io.BytesIO(ଡାଟା))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ଅକାର_ପାଠ+' RGB32').encode() in ଲଗ୍_ଧାଡ଼ି
        print('BOOT:', ଅକାର_ପାଠ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ଲଗ୍_ଧାଡ଼ି).group(1))
        ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 12) == b'RFB 003.008\n'; ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 1)[0]); ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(b'\x01')
        assert 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 4) == b'\0'*4; ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(b'\x01')
        초기 = 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, struct.unpack('>I', 초기[20:])[0])
        ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍((너비-568, 높이-360), (32, 80, 144))
        ଚଳାନ୍ତୁ = len(ଲଗ୍_ଧାଡ଼ି); କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ଚଳାନ୍ତୁ)
        ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍((너비-568, 높이-360), (24, 32, 48))
        ଚଳାନ୍ତୁ = len(ଲଗ୍_ଧାଡ଼ି); କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(80, 16); 기다리기(b'TERMINAL FOCUS 1', ଚଳାନ୍ତୁ)
        ଖୋଳ('ftpd start')
        ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ = ftplib.FTP(); ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.encoding = 'utf-8'; ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.connect('127.0.0.1', ପୋର୍ଟ୍_ନମ୍ଵର୍, timeout=20); ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·କ୍ଲିପ୍ 밖·빈 사각형을 포함한다.
        ଉତ୍ସ = '''#include <화면규약.h>
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
    ଲିଖନ_ଫାଇଲ୍_ଡାଟା(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('화면시험.c', ଉତ୍ସ.encode())
        assert 'exit 0' in ଖୋଳ('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_ପ୍ରେରଣ_କରନ୍ତୁ('run /화면시험\n'))
        ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_ପ୍ରେରଣ_କରନ୍ତୁ('q'))
        ଉତ୍ସ = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, ନିର୍ଗମ, ସିଷ୍ଟମ_ତ୍ରୁଟି
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ସିଷ୍ଟମ_ତ୍ରୁଟି as ତ୍ରୁଟି:
    assert ତ୍ରୁଟି.ଅନୁକ୍ରମଣିକା == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
ନିର୍ଗମ("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('화면시험.py', ଉତ୍ସ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_ପ୍ରେରଣ_କରନ୍ତୁ('python /화면시험.py\n'))
        ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_ପ୍ରେରଣ_କରନ୍ତୁ('q'))
        ଉତ୍ସ = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new ସ୍ଥିତି_ବ୍ୟତିକ୍ରମ("ଆକାର");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new ସ୍ଥିତି_ବ୍ୟତିକ୍ରମ("କ୍ଲିପ୍"); }
        catch (ଅବୈଧ_ଯୁକ୍ତି_ବ୍ୟତିକ୍ରମ ତ୍ରୁଟି) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # ବ୍ୟତିକ୍ରମ 처리는 ଆୟୋଜକ javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = ମାପ_ପଥ/'해상도경계시험.java'
        경계원문.write_text(ଉତ୍ସ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist/jkoros-native-korean.jar'), '-d', str(ମାପ_ପଥ), str(경계원문)])
        ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('해상도경계시험.class', (ମାପ_ପଥ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_ପ୍ରେରଣ_କରନ୍ତୁ('java 해상도경계시험\n'))
        ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_ପ୍ରେରଣ_କରନ୍ତୁ('q'))
        # 게스트 javac의 ସମର୍ଥନ_ମୂଲ୍ୟ 문법으로 ଆକାର ଜିଜ୍ଞାସା_ମୂଲ୍ୟ·지우기·다섯 인수 그리기를 컴파일한다.
        ଉତ୍ସ = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.ନିର୍ଗମ.ଲିଖନ_ରେଖା("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('해상도시험.java', ଉତ୍ସ.encode())
        ମାପ = ଖୋଳ('javac 해상도시험.java'); assert 'exit 0' in ମାପ, ମାପ
        기다리기(b'JAVA RESOLUTION PASS', SMS_ପ୍ରେରଣ_କରନ୍ତୁ('java 해상도시험\n'))
        ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_ପ୍ରେରଣ_କରନ୍ତୁ('q'))
        ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('스윙시험.class', (ମାପ_ପଥ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_ପ୍ରେରଣ_କରନ୍ତୁ('java 스윙시험\n'))
        가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି = (너비-400)//2, (높이-280)//2
        ଅଙ୍କନ_ମୂଲ୍ୟ = ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍((가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି), (32, 80, 144))
        ଅଙ୍କନ_ମୂଲ୍ୟ.save(str(ମାପ_ପଥ/(ଅକାର_ପାଠ+'.png')))
        ଚଳାନ୍ତୁ = len(ଲଗ୍_ଧାଡ଼ି); କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(가로+80, ଅନୁଲମ୍ବ_ସ୍ଥିତି+155)
        기다리기('SWING CLICK ନାମ'.encode(), ଚଳାନ୍ତୁ)
        ଚଳାନ୍ତୁ = len(ଲଗ୍_ଧାଡ଼ି); କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(가로+385, ଅନୁଲମ୍ବ_ସ୍ଥିତି+15); 기다리기(b'jkoros-native> ', ଚଳାନ୍ତୁ)
        assert 'AFTER_RESOLUTION' in ଖୋଳ('echo AFTER_RESOLUTION')
        print('PASS:', ଅକାର_ପାଠ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ: ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.close()
        if ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ: ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.close()
        if ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is None:
            ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.terminate()
            try: ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait(timeout=8)
            except subprocess.TimeoutExpired: ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.kill(); ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait()
        ଚୟନକାରୀ_a916db4e.close(); ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdout.close()
        (ମାପ_ପଥ/(ଅକାର_ପାଠ+'.log')).write_bytes(ଲଗ୍_ଧାଡ଼ି)


def ଚଳାନ୍ତୁ():
    ମାପ_ପଥ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/resolution'; ମାପ_ପଥ.mkdir(parents=True, exist_ok=True)
    ଲଗ୍_ଧାଡ଼ି = {'passed': False, 'kernel_sha256': hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ଅବୈଧ_ମୂଲ୍ୟ in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ମାପ = subprocess.run(['python3', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py'), '--resolution', ଅବୈଧ_ମୂଲ୍ୟ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ମାପ.returncode == 2 and b'--resolution' in ମାପ.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ମାପ_ପଥ), str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, ମାପ_ପଥ); ଲଗ୍_ଧାଡ଼ି['resolutions'].append([너비, 높이])
        ଲଗ୍_ଧାଡ଼ି.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (ମାପ_ପଥ/'report.json').write_text(json.dumps(ଲଗ୍_ଧାଡ଼ି, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ଚଳାନ୍ତୁ()
