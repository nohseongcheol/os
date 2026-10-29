#!/usr/bin/env python3
"""фактычны_дадзеныя QEMU/VNC에서 화면 Памер·경계·акно перамясціць_значэнне·Swing·언어별 그리기를 검사한다."""
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
from працоўны_стол_выгляд import 정확한값
from выканаць_каманда import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); нумар_порта = 임시.getsockname()[1]
    памер_Тэкст = '{}x{}'.format(너비, 높이)
    Працэс_значэнне = subprocess.Popen(['python3', str(기준/'Інструменты/выканаць_каманда.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(нумар_порта), '--resolution', памер_Тэкст], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектар_a916db4e = selectors.DefaultSelector(); селектар_a916db4e.register(Працэс_значэнне.stdout, selectors.EVENT_READ)
    журнал_запіс = bytearray(); аддалены_значэнне = None; перанос_значэнне = None

    def 기다리기(паказаць_значэнне, Выканаць=0):
        마감 = time.monotonic() + 60
        while паказаць_значэнне not in журнал_запіс[Выканаць:]:
            if time.monotonic() > 마감 or Працэс_значэнне.poll() is not None or b'HALTED' in журнал_запіс or b'PANIC:' in журнал_запіс:
                raise AssertionError(журнал_запіс[Выканаць:].decode('utf-8', 'replace'))
            for Падзея, _ in селектар_a916db4e.select(.1):
                дадзеныя = Падзея.fileobj.read(65536)
                if дадзеныя: журнал_запіс.extend(дадзеныя)
        return журнал_запіс[Выканаць:].decode('utf-8', 'replace')

    def націснуць_кнопка(сімвал, 눌림=True): аддалены_значэнне.sendall(struct.pack('>BBHI', 4, int(눌림), 0, сімвал))

    def адправіць_SMS(Тэкст):
        Выканаць = len(журнал_запіс)
        for сімвал_значэнне_068c2631 in Тэкст:
            сімвал = 0xff0d if сімвал_значэнне_068c2631 == '\n' else ord(сімвал_значэнне_068c2631) if ord(сімвал_значэнне_068c2631) < 256 else 0x1000000 | ord(сімвал_значэнне_068c2631)
            націснуць_кнопка(сімвал); націснуць_кнопка(сімвал, False)
        return Выканаць

    def абалонка(Тэкст): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', адправіць_SMS(Тэкст+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): аддалены_значэнне.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def націснуць_значэнне(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def растравая_выява_выява():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 фактычны_дадзеныя 너비를 쓴다.
        аддалены_значэнне.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        рукапісная_графіка_значэнне = Image.new('RGB', (너비, 높이)); вобласць_значэнне = 0
        while True:
            종류 = 정확한값(аддалены_значэнне, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                даўжыня_значэнне = struct.unpack('>I', 정확한값(аддалены_значэнне, 7)[3:])[0]; 정확한값(аддалены_значэнне, даўжыня_значэнне); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(аддалены_значэнне, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, даўжыня_значэнне, кадаванне_значэнне = struct.unpack('>HHHHi', 정확한값(аддалены_значэнне, 12))
                assert кадаванне_значэнне == 0 and 가로+폭 <= 너비 and 세로+даўжыня_значэнне <= 높이
                рукапісная_графіка_значэнне.paste(Image.frombytes('RGB', (폭, даўжыня_значэнне), 정확한값(аддалены_значэнне, 폭*даўжыня_значэнне*4), 'raw', 'BGRX'), (가로, 세로))
                вобласць_значэнне += 폭*даўжыня_значэнне
            if вобласць_значэнне:
                assert вобласць_значэнне == 너비*높이, вобласць_значэнне
                return рукапісная_графіка_значэнне

    def чэк_пэл(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            рукапісная_графіка_значэнне = растравая_выява_выява()
            if рукапісная_графіка_значэнне.getpixel(좌표) == 색: return рукапісная_графіка_значэнне
            if time.monotonic() > 마감: raise AssertionError((좌표, рукапісная_графіка_значэнне.getpixel(좌표), 색))

    def запампоўка_Файлы(Назва, дадзеныя): перанос_значэнне.storbinary('STOR '+Назва, io.BytesIO(дадзеныя))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+памер_Тэкст+' RGB32').encode() in журнал_запіс
        print('BOOT:', памер_Тэкст, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', журнал_запіс).group(1))
        аддалены_значэнне = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(аддалены_значэнне, 12) == b'RFB 003.008\n'; аддалены_значэнне.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(аддалены_значэнне, 정확한값(аддалены_значэнне, 1)[0]); аддалены_значэнне.sendall(b'\x01')
        assert 정확한값(аддалены_значэнне, 4) == b'\0'*4; аддалены_значэнне.sendall(b'\x01')
        초기 = 정확한값(аддалены_значэнне, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(аддалены_значэнне, struct.unpack('>I', 초기[20:])[0])
        аддалены_значэнне.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        аддалены_значэнне.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        чэк_пэл((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        чэк_пэл((너비-568, 높이-360), (32, 80, 144))
        Выканаць = len(журнал_запіс); націснуць_значэнне(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Выканаць)
        чэк_пэл((너비-568, 높이-360), (24, 32, 48))
        Выканаць = len(журнал_запіс); націснуць_значэнне(80, 16); 기다리기(b'TERMINAL FOCUS 1', Выканаць)
        абалонка('ftpd start')
        перанос_значэнне = ftplib.FTP(); перанос_значэнне.encoding = 'utf-8'; перанос_значэнне.connect('127.0.0.1', нумар_порта, timeout=20); перанос_значэнне.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·кліп 밖·빈 사각형을 포함한다.
        КРЫНІЦА = '''#include <화면규약.h>
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
    напісаць_файл_дадзеныя(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        запампоўка_Файлы('화면시험.c', КРЫНІЦА.encode())
        assert 'exit 0' in абалонка('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', адправіць_SMS('run /화면시험\n'))
        чэк_пэл((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', адправіць_SMS('q'))
        КРЫНІЦА = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, Выхад, сістэма_памылка
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except сістэма_памылка as ПАМЫЛКА:
    assert ПАМЫЛКА.індэкс == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Выхад("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        запампоўка_Файлы('화면시험.py', КРЫНІЦА.encode())
        기다리기(b'PYTHON RESOLUTION PASS', адправіць_SMS('python /화면시험.py\n'))
        чэк_пэл((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', адправіць_SMS('q'))
        КРЫНІЦА = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new стан_выключэнне("Памер");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new стан_выключэнне("кліп"); }
        catch (памылковы_аргумент_выключэнне ПАМЫЛКА) { }
        화면.ачысціць_увядзенне(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # выключэнне 처리는 вузел javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(КРЫНІЦА.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        запампоўка_Файлы('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', адправіць_SMS('java 해상도경계시험\n'))
        чэк_пэл((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', адправіць_SMS('q'))
        # 게스트 javac의 апора_значэнне 문법으로 Памер запыт_значэнне·ачысціць_увядзенне·다섯 인수 그리기를 컴파일한다.
        КРЫНІЦА = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.ачысціць_увядзенне(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.Выхад.напісаць_лінія("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        запампоўка_Файлы('해상도시험.java', КРЫНІЦА.encode())
        결과 = абалонка('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', адправіць_SMS('java 해상도시험\n'))
        чэк_пэл((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', адправіць_SMS('q'))
        запампоўка_Файлы('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', адправіць_SMS('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        рукапісная_графіка_значэнне = чэк_пэл((가로, 세로), (32, 80, 144))
        рукапісная_графіка_значэнне.save(str(결과경로/(памер_Тэкст+'.png')))
        Выканаць = len(журнал_запіс); націснуць_значэнне(가로+80, 세로+155)
        기다리기('SWING CLICK Назва'.encode(), Выканаць)
        Выканаць = len(журнал_запіс); націснуць_значэнне(가로+385, 세로+15); 기다리기(b'jkoros-native> ', Выканаць)
        assert 'AFTER_RESOLUTION' in абалонка('echo AFTER_RESOLUTION')
        print('PASS:', памер_Тэкст, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if перанос_значэнне: перанос_значэнне.close()
        if аддалены_значэнне: аддалены_значэнне.close()
        if Працэс_значэнне.poll() is None:
            Працэс_значэнне.terminate()
            try: Працэс_значэнне.wait(timeout=8)
            except subprocess.TimeoutExpired: Працэс_значэнне.kill(); Працэс_значэнне.wait()
        селектар_a916db4e.close(); Працэс_значэнне.stdout.close()
        (결과경로/(памер_Тэкст+'.log')).write_bytes(журнал_запіс)


def Выканаць():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    журнал_запіс = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for памылковы_значэнне in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Інструменты/выканаць_каманда.py'), '--resolution', памылковы_значэнне], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); журнал_запіс['resolutions'].append([너비, 높이])
        журнал_запіс.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(журнал_запіс, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Выканаць()
