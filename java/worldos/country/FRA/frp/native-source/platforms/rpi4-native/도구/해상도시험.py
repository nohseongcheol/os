#!/usr/bin/env python3
"""실제 QEMU/VNC에서 화면 Talyi·경계·창 이동·Swing·언어별 그리기를 검사한다."""
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
from 바탕화면 import 정확한값
from 실행 import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    크기글 = '{}x{}'.format(너비, 높이)
    과정 = subprocess.Popen(['python3', str(기준/'도구/실행.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', 크기글], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(과정.stdout, selectors.EVENT_READ)
    기록 = bytearray(); 원격 = None; 전송 = None

    def 기다리기(표시, Emprendre=0):
        마감 = time.monotonic() + 60
        while 표시 not in 기록[Emprendre:]:
            if time.monotonic() > 마감 or 과정.poll() is not None or b'HALTED' in 기록 or b'PANIC:' in 기록:
                raise AssertionError(기록[Emprendre:].decode('utf-8', 'replace'))
            for 사건, _ in 선택기.select(.1):
                자료 = 사건.fileobj.read(65536)
                if 자료: 기록.extend(자료)
        return 기록[Emprendre:].decode('utf-8', 'replace')

    def 누르기(기호, 눌림=True): 원격.sendall(struct.pack('>BBHI', 4, int(눌림), 0, 기호))

    def 글보내기(글):
        Emprendre = len(기록)
        for 글자 in 글:
            기호 = 0xff0d if 글자 == '\n' else ord(글자) if ord(글자) < 256 else 0x1000000 | ord(글자)
            누르기(기호); 누르기(기호, False)
        return Emprendre

    def 셸(글): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', 글보내기(글+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): 원격.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def 클릭(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def 화상():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 실제 너비를 쓴다.
        원격.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        그림 = Image.new('RGB', (너비, 높이)); 면적 = 0
        while True:
            종류 = 정확한값(원격, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', 정확한값(원격, 7)[3:])[0]; 정확한값(원격, 길이); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(원격, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, 길이, 부호 = struct.unpack('>HHHHi', 정확한값(원격, 12))
                assert 부호 == 0 and 가로+폭 <= 너비 and 세로+길이 <= 높이
                그림.paste(Image.frombytes('RGB', (폭, 길이), 정확한값(원격, 폭*길이*4), 'raw', 'BGRX'), (가로, 세로))
                면적 += 폭*길이
            if 면적:
                assert 면적 == 너비*높이, 면적
                return 그림

    def 화소확인(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            그림 = 화상()
            if 그림.getpixel(좌표) == 색: return 그림
            if time.monotonic() > 마감: raise AssertionError((좌표, 그림.getpixel(좌표), 색))

    def 올리기(Nom, 자료): 전송.storbinary('STOR '+Nom, io.BytesIO(자료))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+크기글+' RGB32').encode() in 기록
        print('BOOT:', 크기글, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', 기록).group(1))
        원격 = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(원격, 12) == b'RFB 003.008\n'; 원격.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(원격, 정확한값(원격, 1)[0]); 원격.sendall(b'\x01')
        assert 정확한값(원격, 4) == b'\0'*4; 원격.sendall(b'\x01')
        초기 = 정확한값(원격, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(원격, struct.unpack('>I', 초기[20:])[0])
        원격.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        원격.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        화소확인((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        화소확인((너비-568, 높이-360), (32, 80, 144))
        Emprendre = len(기록); 클릭(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Emprendre)
        화소확인((너비-568, 높이-360), (24, 32, 48))
        Emprendre = len(기록); 클릭(80, 16); 기다리기(b'TERMINAL FOCUS 1', Emprendre)
        셸('ftpd start')
        전송 = ftplib.FTP(); 전송.encoding = 'utf-8'; 전송.connect('127.0.0.1', 접속번호, timeout=20); 전송.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·범위 밖·빈 사각형을 포함한다.
        원문 = '''#include <화면규약.h>
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
    파일자료쓰기(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('화면시험.c', 원문.encode())
        assert 'exit 0' in 셸('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', 글보내기('run /화면시험\n'))
        화소확인((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', 글보내기('q'))
        원문 = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, 운영체제오류
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except 운영체제오류 as Erròr:
    assert Erròr.번호 == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('화면시험.py', 원문.encode())
        기다리기(b'PYTHON RESOLUTION PASS', 글보내기('python /화면시험.py\n'))
        화소확인((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', 글보내기('q'))
        원문 = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("Talyi");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("범위"); }
        catch (잘못된인수예외 Erròr) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 호스트 javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(원문.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        올리기('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', 글보내기('java 해상도경계시험\n'))
        화소확인((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', 글보내기('q'))
        # 게스트 javac의 지원 문법으로 Talyi 조회·지우기·다섯 인수 그리기를 컴파일한다.
        원문 = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.줄쓰기("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('해상도시험.java', 원문.encode())
        결과 = 셸('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', 글보내기('java 해상도시험\n'))
        화소확인((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', 글보내기('q'))
        올리기('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', 글보내기('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        그림 = 화소확인((가로, 세로), (32, 80, 144))
        그림.save(str(결과경로/(크기글+'.png')))
        Emprendre = len(기록); 클릭(가로+80, 세로+155)
        기다리기('SWING CLICK Nom'.encode(), Emprendre)
        Emprendre = len(기록); 클릭(가로+385, 세로+15); 기다리기(b'jkoros-native> ', Emprendre)
        assert 'AFTER_RESOLUTION' in 셸('echo AFTER_RESOLUTION')
        print('PASS:', 크기글, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if 전송: 전송.close()
        if 원격: 원격.close()
        if 과정.poll() is None:
            과정.terminate()
            try: 과정.wait(timeout=8)
            except subprocess.TimeoutExpired: 과정.kill(); 과정.wait()
        선택기.close(); 과정.stdout.close()
        (결과경로/(크기글+'.log')).write_bytes(기록)


def Emprendre():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    기록 = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for 잘못된값 in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'도구/실행.py'), '--resolution', 잘못된값], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); 기록['resolutions'].append([너비, 높이])
        기록.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(기록, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Emprendre()
