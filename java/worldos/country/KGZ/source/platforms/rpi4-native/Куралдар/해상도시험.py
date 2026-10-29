#!/usr/bin/env python3
"""актуалдуу_берилмелер QEMU/VNC에서 화면 Өлчөмү·경계·терезе жылдыруу_маани·Swing·언어별 그리기를 검사한다."""
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
from иш_такта_көрүү import 정확한값
from аткаруу_буйрук import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    көлөм_СМС = '{}x{}'.format(너비, 높이)
    Процесс_маани = subprocess.Popen(['python3', str(기준/'Куралдар/аткаруу_буйрук.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', көлөм_СМС], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор_a916db4e = selectors.DefaultSelector(); селектор_a916db4e.register(Процесс_маани.stdout, selectors.EVENT_READ)
    жазуу_катар = bytearray(); алыскы_маани = None; ташүү_маани = None

    def 기다리기(көрсөтүү_маани, Жүргүзүү=0):
        마감 = time.monotonic() + 60
        while көрсөтүү_маани not in жазуу_катар[Жүргүзүү:]:
            if time.monotonic() > 마감 or Процесс_маани.poll() is not None or b'HALTED' in жазуу_катар or b'PANIC:' in жазуу_катар:
                raise AssertionError(жазуу_катар[Жүргүзүү:].decode('utf-8', 'replace'))
            for окуя, _ in селектор_a916db4e.select(.1):
                берилмелер = окуя.fileobj.read(65536)
                if берилмелер: жазуу_катар.extend(берилмелер)
        return жазуу_катар[Жүргүзүү:].decode('utf-8', 'replace')

    def баскылоо_баскыч(символ, 눌림=True): алыскы_маани.sendall(struct.pack('>BBHI', 4, int(눌림), 0, символ))

    def СМС_жөнөтүү(Текст):
        Жүргүзүү = len(жазуу_катар)
        for символ_маани_068c2631 in Текст:
            символ = 0xff0d if символ_маани_068c2631 == '\n' else ord(символ_маани_068c2631) if ord(символ_маани_068c2631) < 256 else 0x1000000 | ord(символ_маани_068c2631)
            баскылоо_баскыч(символ); баскылоо_баскыч(символ, False)
        return Жүргүзүү

    def сырты(Текст): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', СМС_жөнөтүү(Текст+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): алыскы_маани.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def баскылоо_маани(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def битмап_сүрөт():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 актуалдуу_берилмелер 너비를 쓴다.
        алыскы_маани.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        чийүү_маани = Image.new('RGB', (너비, 높이)); аймак_маани = 0
        while True:
            종류 = 정확한값(алыскы_маани, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                узундук_маани = struct.unpack('>I', 정확한값(алыскы_маани, 7)[3:])[0]; 정확한값(алыскы_маани, узундук_маани); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(алыскы_маани, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, узундук_маани, коддоо_маани = struct.unpack('>HHHHi', 정확한값(алыскы_маани, 12))
                assert коддоо_маани == 0 and 가로+폭 <= 너비 and 세로+узундук_маани <= 높이
                чийүү_маани.paste(Image.frombytes('RGB', (폭, узундук_маани), 정확한값(алыскы_маани, 폭*узундук_маани*4), 'raw', 'BGRX'), (가로, 세로))
                аймак_маани += 폭*узундук_маани
            if аймак_маани:
                assert аймак_маани == 너비*높이, аймак_маани
                return чийүү_маани

    def чек_пиксел(координат_маани, 색):
        마감 = time.monotonic()+10
        while True:
            чийүү_маани = битмап_сүрөт()
            if чийүү_маани.getpixel(координат_маани) == 색: return чийүү_маани
            if time.monotonic() > 마감: raise AssertionError((координат_маани, чийүү_маани.getpixel(координат_маани), 색))

    def жүктөп_жөнөтүү_Файлдар(Аты, берилмелер): ташүү_маани.storbinary('STOR '+Аты, io.BytesIO(берилмелер))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+көлөм_СМС+' RGB32').encode() in жазуу_катар
        print('BOOT:', көлөм_СМС, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', жазуу_катар).group(1))
        алыскы_маани = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(алыскы_маани, 12) == b'RFB 003.008\n'; алыскы_маани.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(алыскы_маани, 정확한값(алыскы_маани, 1)[0]); алыскы_маани.sendall(b'\x01')
        assert 정확한값(алыскы_маани, 4) == b'\0'*4; алыскы_маани.sendall(b'\x01')
        초기 = 정확한값(алыскы_маани, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(алыскы_маани, struct.unpack('>I', 초기[20:])[0])
        алыскы_маани.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        алыскы_маани.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        чек_пиксел((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        чек_пиксел((너비-568, 높이-360), (32, 80, 144))
        Жүргүзүү = len(жазуу_катар); баскылоо_маани(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Жүргүзүү)
        чек_пиксел((너비-568, 높이-360), (24, 32, 48))
        Жүргүзүү = len(жазуу_катар); баскылоо_маани(80, 16); 기다리기(b'TERMINAL FOCUS 1', Жүргүзүү)
        сырты('ftpd start')
        ташүү_маани = ftplib.FTP(); ташүү_маани.encoding = 'utf-8'; ташүү_маани.connect('127.0.0.1', 접속번호, timeout=20); ташүү_маани.login()
        # C 경계 검사는 32비트 unsigned 음수 айландыруу_маани·клип 밖·빈 사각형을 포함한다.
        Булак = '''#include <화면규약.h>
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
    жазуу_файл_берилмелер(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        жүктөп_жөнөтүү_Файлдар('화면시험.c', Булак.encode())
        assert 'exit 0' in сырты('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', СМС_жөнөтүү('run /화면시험\n'))
        чек_пиксел((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', СМС_жөнөтүү('q'))
        Булак = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, Чыгыш, тутум_ката
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except тутум_ката as Ката:
    assert Ката.индекс == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Чыгыш("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        жүктөп_жөнөтүү_Файлдар('화면시험.py', Булак.encode())
        기다리기(b'PYTHON RESOLUTION PASS', СМС_жөнөтүү('python /화면시험.py\n'))
        чек_пиксел((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', СМС_жөнөтүү('q'))
        Булак = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("Өлчөмү");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("клип"); }
        catch (잘못된인수예외 Ката) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 кабылдоо javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(Булак.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        жүктөп_жөнөтүү_Файлдар('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', СМС_жөнөтүү('java 해상도경계시험\n'))
        чек_пиксел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', СМС_жөнөтүү('q'))
        # 게스트 javac의 Колдоо_маани 문법으로 Өлчөмү сурам_маани·지우기·다섯 인수 그리기를 컴파일한다.
        Булак = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.Чыгыш.жазуу_сап("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        жүктөп_жөнөтүү_Файлдар('해상도시험.java', Булак.encode())
        결과 = сырты('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', СМС_жөнөтүү('java 해상도시험\n'))
        чек_пиксел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', СМС_жөнөтүү('q'))
        жүктөп_жөнөтүү_Файлдар('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', СМС_жөнөтүү('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        чийүү_маани = чек_пиксел((가로, 세로), (32, 80, 144))
        чийүү_маани.save(str(결과경로/(көлөм_СМС+'.png')))
        Жүргүзүү = len(жазуу_катар); баскылоо_маани(가로+80, 세로+155)
        기다리기('SWING CLICK Аты'.encode(), Жүргүзүү)
        Жүргүзүү = len(жазуу_катар); баскылоо_маани(가로+385, 세로+15); 기다리기(b'jkoros-native> ', Жүргүзүү)
        assert 'AFTER_RESOLUTION' in сырты('echo AFTER_RESOLUTION')
        print('PASS:', көлөм_СМС, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ташүү_маани: ташүү_маани.close()
        if алыскы_маани: алыскы_маани.close()
        if Процесс_маани.poll() is None:
            Процесс_маани.terminate()
            try: Процесс_маани.wait(timeout=8)
            except subprocess.TimeoutExpired: Процесс_маани.kill(); Процесс_маани.wait()
        селектор_a916db4e.close(); Процесс_маани.stdout.close()
        (결과경로/(көлөм_СМС+'.log')).write_bytes(жазуу_катар)


def Жүргүзүү():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    жазуу_катар = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for бузук_маани in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Куралдар/аткаруу_буйрук.py'), '--resolution', бузук_маани], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); жазуу_катар['resolutions'].append([너비, 높이])
        жазуу_катар.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(жазуу_катар, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Жүргүзүү()
