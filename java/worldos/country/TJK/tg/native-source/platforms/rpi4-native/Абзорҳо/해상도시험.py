#!/usr/bin/env python3
"""воқеӣ_иттилоот QEMU/VNC에서 화면 андоза_кардан·경계·равзана интиқол_додан_қимат·Swing·언어별 그리기를 검사한다."""
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
from мизи_корӣ_намуд import 정확한값
from иҷро_кардан_фармон import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    андоза_кардан_Матн = '{}x{}'.format(너비, 높이)
    Раванд_қимат = subprocess.Popen(['python3', str(기준/'Абзорҳо/иҷро_кардан_фармон.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', андоза_кардан_Матн], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    интихобкунанда_a916db4e = selectors.DefaultSelector(); интихобкунанда_a916db4e.register(Раванд_қимат.stdout, selectors.EVENT_READ)
    сабт_кардан_сабт = bytearray(); дурдаст_қимат = None; интиқол_қимат = None

    def 기다리기(намоиш_додан_қимат, порча=0):
        마감 = time.monotonic() + 60
        while намоиш_додан_қимат not in сабт_кардан_сабт[порча:]:
            if time.monotonic() > 마감 or Раванд_қимат.poll() is not None or b'HALTED' in сабт_кардан_сабт or b'PANIC:' in сабт_кардан_сабт:
                raise AssertionError(сабт_кардан_сабт[порча:].decode('utf-8', 'replace'))
            for рӯйдод, _ in интихобкунанда_a916db4e.select(.1):
                иттилоот = рӯйдод.fileobj.read(65536)
                if иттилоот: сабт_кардан_сабт.extend(иттилоот)
        return сабт_кардан_сабт[порча:].decode('utf-8', 'replace')

    def зер_кардан_тугма(аломат, 눌림=True): дурдаст_қимат.sendall(struct.pack('>BBHI', 4, int(눌림), 0, аломат))

    def фиристодани_SMS(Матн):
        порча = len(сабт_кардан_сабт)
        for аломат_қимат_068c2631 in Матн:
            аломат = 0xff0d if аломат_қимат_068c2631 == '\n' else ord(аломат_қимат_068c2631) if ord(аломат_қимат_068c2631) < 256 else 0x1000000 | ord(аломат_қимат_068c2631)
            зер_кардан_тугма(аломат); зер_кардан_тугма(аломат, False)
        return порча

    def восит(Матн): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', фиристодани_SMS(Матн+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): дурдаст_қимат.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def зер_кардан_қимат(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def нақши_нуқтаӣ_расм():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 воқеӣ_иттилоот 너비를 쓴다.
        дурдаст_қимат.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        нақша_қимат = Image.new('RGB', (너비, 높이)); ноҳия_қимат = 0
        while True:
            종류 = 정확한값(дурдаст_қимат, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                дарозӣ_қимат = struct.unpack('>I', 정확한값(дурдаст_қимат, 7)[3:])[0]; 정확한값(дурдаст_қимат, дарозӣ_қимат); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(дурдаст_қимат, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, дарозӣ_қимат, рамзгузорӣ_қимат = struct.unpack('>HHHHi', 정확한값(дурдаст_қимат, 12))
                assert рамзгузорӣ_қимат == 0 and 가로+폭 <= 너비 and 세로+дарозӣ_қимат <= 높이
                нақша_қимат.paste(Image.frombytes('RGB', (폭, дарозӣ_қимат), 정확한값(дурдаст_қимат, 폭*дарозӣ_қимат*4), 'raw', 'BGRX'), (가로, 세로))
                ноҳия_қимат += 폭*дарозӣ_қимат
            if ноҳия_қимат:
                assert ноҳия_қимат == 너비*높이, ноҳия_қимат
                return нақша_қимат

    def санҷиш_пиксел(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            нақша_қимат = нақши_нуқтаӣ_расм()
            if нақша_қимат.getpixel(좌표) == 색: return нақша_қимат
            if time.monotonic() > 마감: raise AssertionError((좌표, нақша_қимат.getpixel(좌표), 색))

    def бор_кардан_Файлҳо(Ном, иттилоот): интиқол_қимат.storbinary('STOR '+Ном, io.BytesIO(иттилоот))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+андоза_кардан_Матн+' RGB32').encode() in сабт_кардан_сабт
        print('BOOT:', андоза_кардан_Матн, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', сабт_кардан_сабт).group(1))
        дурдаст_қимат = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(дурдаст_қимат, 12) == b'RFB 003.008\n'; дурдаст_қимат.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(дурдаст_қимат, 정확한값(дурдаст_қимат, 1)[0]); дурдаст_қимат.sendall(b'\x01')
        assert 정확한값(дурдаст_қимат, 4) == b'\0'*4; дурдаст_қимат.sendall(b'\x01')
        초기 = 정확한값(дурдаст_қимат, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(дурдаст_қимат, struct.unpack('>I', 초기[20:])[0])
        дурдаст_қимат.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        дурдаст_қимат.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        санҷиш_пиксел((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        санҷиш_пиксел((너비-568, 높이-360), (32, 80, 144))
        порча = len(сабт_кардан_сабт); зер_кардан_қимат(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', порча)
        санҷиш_пиксел((너비-568, 높이-360), (24, 32, 48))
        порча = len(сабт_кардан_сабт); зер_кардан_қимат(80, 16); 기다리기(b'TERMINAL FOCUS 1', порча)
        восит('ftpd start')
        интиқол_қимат = ftplib.FTP(); интиқол_қимат.encoding = 'utf-8'; интиқол_қимат.connect('127.0.0.1', 접속번호, timeout=20); интиқол_қимат.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·клип 밖·빈 사각형을 포함한다.
        манбаъ = '''#include <화면규약.h>
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
    навиштан_файл_иттилоот(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        бор_кардан_Файлҳо('화면시험.c', манбаъ.encode())
        assert 'exit 0' in восит('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', фиристодани_SMS('run /화면시험\n'))
        санҷиш_пиксел((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', фиристодани_SMS('q'))
        манбаъ = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, система_хато
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except система_хато as Хато:
    assert Хато.индекс == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        бор_кардан_Файлҳо('화면시험.py', манбаъ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', фиристодани_SMS('python /화면시험.py\n'))
        санҷиш_пиксел((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', фиристодани_SMS('q'))
        манбаъ = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("андоза_кардан");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("клип"); }
        catch (잘못된인수예외 Хато) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 мизбон javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(манбаъ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        бор_кардан_Файлҳо('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', фиристодани_SMS('java 해상도경계시험\n'))
        санҷиш_пиксел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', фиристодани_SMS('q'))
        # 게스트 javac의 Дастгирӣ_қимат 문법으로 андоза_кардан ковиш_қимат·지우기·다섯 인수 그리기를 컴파일한다.
        манбаъ = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.навиштан_хат("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        бор_кардан_Файлҳо('해상도시험.java', манбаъ.encode())
        결과 = восит('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', фиристодани_SMS('java 해상도시험\n'))
        санҷиш_пиксел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', фиристодани_SMS('q'))
        бор_кардан_Файлҳо('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', фиристодани_SMS('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        нақша_қимат = санҷиш_пиксел((가로, 세로), (32, 80, 144))
        нақша_қимат.save(str(결과경로/(андоза_кардан_Матн+'.png')))
        порча = len(сабт_кардан_сабт); зер_кардан_қимат(가로+80, 세로+155)
        기다리기('SWING CLICK Ном'.encode(), порча)
        порча = len(сабт_кардан_сабт); зер_кардан_қимат(가로+385, 세로+15); 기다리기(b'jkoros-native> ', порча)
        assert 'AFTER_RESOLUTION' in восит('echo AFTER_RESOLUTION')
        print('PASS:', андоза_кардан_Матн, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if интиқол_қимат: интиқол_қимат.close()
        if дурдаст_қимат: дурдаст_қимат.close()
        if Раванд_қимат.poll() is None:
            Раванд_қимат.terminate()
            try: Раванд_қимат.wait(timeout=8)
            except subprocess.TimeoutExpired: Раванд_қимат.kill(); Раванд_қимат.wait()
        интихобкунанда_a916db4e.close(); Раванд_қимат.stdout.close()
        (결과경로/(андоза_кардан_Матн+'.log')).write_bytes(сабт_кардан_сабт)


def порча():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    сабт_кардан_сабт = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for беэътибор_қимат in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Абзорҳо/иҷро_кардан_фармон.py'), '--resolution', беэътибор_қимат], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); сабт_кардан_сабт['resolutions'].append([너비, 높이])
        сабт_кардан_сабт.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(сабт_кардан_сабт, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': порча()
