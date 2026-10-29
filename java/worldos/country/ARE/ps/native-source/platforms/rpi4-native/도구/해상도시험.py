#!/usr/bin/env python3
"""실제 QEMU/VNC에서 화면 کچ·경계·کړکۍ 이동·Swing·언어별 그리기를 검사한다."""
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
from سرپاڼه_ليد import 정확한값
from 실행 import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    크기글 = '{}x{}'.format(너비, 높이)
    과정 = subprocess.Popen(['python3', str(기준/'도구/실행.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', 크기글], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(과정.stdout, selectors.EVENT_READ)
    خبرال_کیل = bytearray(); 원격 = None; لېږدول_ارزښت = None

    def 기다리기(표시, ځغلول=0):
        마감 = time.monotonic() + 60
        while 표시 not in خبرال_کیل[ځغلول:]:
            if time.monotonic() > 마감 or 과정.poll() is not None or b'HALTED' in خبرال_کیل or b'PANIC:' in خبرال_کیل:
                raise AssertionError(خبرال_کیل[ځغلول:].decode('utf-8', 'replace'))
            for پېښه, _ in 선택기.select(.1):
                اومتوک = پېښه.fileobj.read(65536)
                if اومتوک: خبرال_کیل.extend(اومتوک)
        return خبرال_کیل[ځغلول:].decode('utf-8', 'replace')

    def ټک_تڼۍ(기호, 눌림=True): 원격.sendall(struct.pack('>BBHI', 4, int(눌림), 0, 기호))

    def 글보내기(ليکنه):
        ځغلول = len(خبرال_کیل)
        for لوښه_ارزښت in ليکنه:
            기호 = 0xff0d if لوښه_ارزښت == '\n' else ord(لوښه_ارزښت) if ord(لوښه_ارزښت) < 256 else 0x1000000 | ord(لوښه_ارزښت)
            ټک_تڼۍ(기호); ټک_تڼۍ(기호, False)
        return ځغلول

    def سیپۍ(ليکنه): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', 글보내기(ليکنه+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): 원격.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def ټک_ارزښت(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def ټکيله_انځور():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 실제 너비를 쓴다.
        원격.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        그림 = Image.new('RGB', (너비, 높이)); 면적 = 0
        while True:
            종류 = 정확한값(원격, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                اوږدوالى_ارزښت = struct.unpack('>I', 정확한값(원격, 7)[3:])[0]; 정확한값(원격, اوږدوالى_ارزښت); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(원격, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, اوږدوالى_ارزښت, کوډييزونه_ارزښت = struct.unpack('>HHHHi', 정확한값(원격, 12))
                assert کوډييزونه_ارزښت == 0 and 가로+폭 <= 너비 and 세로+اوږدوالى_ارزښت <= 높이
                그림.paste(Image.frombytes('RGB', (폭, اوږدوالى_ارزښت), 정확한값(원격, 폭*اوږدوالى_ارزښت*4), 'raw', 'BGRX'), (가로, 세로))
                면적 += 폭*اوږدوالى_ارزښت
            if 면적:
                assert 면적 == 너비*높이, 면적
                return 그림

    def کتل_پکسل(همغږون_ارزښت, 색):
        마감 = time.monotonic()+10
        while True:
            그림 = ټکيله_انځور()
            if 그림.getpixel(همغږون_ارزښت) == 색: return 그림
            if time.monotonic() > 마감: raise AssertionError((همغږون_ارزښت, 그림.getpixel(همغږون_ارزښت), 색))

    def 올리기(نوم, اومتوک): لېږدول_ارزښت.storbinary('STOR '+نوم, io.BytesIO(اومتوک))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+크기글+' RGB32').encode() in خبرال_کیل
        print('BOOT:', 크기글, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', خبرال_کیل).group(1))
        원격 = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(원격, 12) == b'RFB 003.008\n'; 원격.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(원격, 정확한값(원격, 1)[0]); 원격.sendall(b'\x01')
        assert 정확한값(원격, 4) == b'\0'*4; 원격.sendall(b'\x01')
        초기 = 정확한값(원격, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(원격, struct.unpack('>I', 초기[20:])[0])
        원격.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        원격.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        کتل_پکسل((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        کتل_پکسل((너비-568, 높이-360), (32, 80, 144))
        ځغلول = len(خبرال_کیل); ټک_ارزښت(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ځغلول)
        کتل_پکسل((너비-568, 높이-360), (24, 32, 48))
        ځغلول = len(خبرال_کیل); ټک_ارزښت(80, 16); 기다리기(b'TERMINAL FOCUS 1', ځغلول)
        سیپۍ('ftpd start')
        لېږدول_ارزښت = ftplib.FTP(); لېږدول_ارزښت.encoding = 'utf-8'; لېږدول_ارزښت.connect('127.0.0.1', 접속번호, timeout=20); لېږدول_ارزښت.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ټوټه 밖·빈 사각형을 포함한다.
        سرچينه = '''#include <화면규약.h>
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
    ليکل_دوتنه_اومتوک(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('화면시험.c', سرچينه.encode())
        assert 'exit 0' in سیپۍ('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', 글보내기('run /화면시험\n'))
        کتل_پکسل((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', 글보내기('q'))
        سرچينه = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, غونډال_تېروتنه
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except غونډال_تېروتنه as تېروتنه:
    assert تېروتنه.لړیال == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('화면시험.py', سرچينه.encode())
        기다리기(b'PYTHON RESOLUTION PASS', 글보내기('python /화면시험.py\n'))
        کتل_پکسل((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', 글보내기('q'))
        سرچينه = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("کچ");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("ټوټه"); }
        catch (잘못된인수예외 تېروتنه) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 کوربه javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(سرچينه.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        올리기('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', 글보내기('java 해상도경계시험\n'))
        کتل_پکسل((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', 글보내기('q'))
        # 게스트 javac의 ملاتړ_ارزښت 문법으로 کچ پوښتنه_ارزښت·지우기·다섯 인수 그리기를 컴파일한다.
        سرچينه = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.ليکل_ليکه("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('해상도시험.java', سرچينه.encode())
        결과 = سیپۍ('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', 글보내기('java 해상도시험\n'))
        کتل_پکسل((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', 글보내기('q'))
        올리기('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', 글보내기('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        그림 = کتل_پکسل((가로, 세로), (32, 80, 144))
        그림.save(str(결과경로/(크기글+'.png')))
        ځغلول = len(خبرال_کیل); ټک_ارزښت(가로+80, 세로+155)
        기다리기('SWING CLICK نوم'.encode(), ځغلول)
        ځغلول = len(خبرال_کیل); ټک_ارزښت(가로+385, 세로+15); 기다리기(b'jkoros-native> ', ځغلول)
        assert 'AFTER_RESOLUTION' in سیپۍ('echo AFTER_RESOLUTION')
        print('PASS:', 크기글, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if لېږدول_ارزښت: لېږدول_ارزښت.close()
        if 원격: 원격.close()
        if 과정.poll() is None:
            과정.terminate()
            try: 과정.wait(timeout=8)
            except subprocess.TimeoutExpired: 과정.kill(); 과정.wait()
        선택기.close(); 과정.stdout.close()
        (결과경로/(크기글+'.log')).write_bytes(خبرال_کیل)


def ځغلول():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    خبرال_کیل = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ناباورى_ارزښت in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'도구/실행.py'), '--resolution', ناباورى_ارزښت], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); خبرال_کیل['resolutions'].append([너비, 높이])
        خبرال_کیل.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(خبرال_کیل, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ځغلول()
