#!/usr/bin/env python3
"""фактик_мәгълүмат QEMU/VNC에서 화면 үлчәмен_үзгәртү·경계·тәрәз күчерү_VALUE·Swing·언어별 그리기를 검사한다."""
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
from классик_карау import EXACT_VALUE
from үтәргә_команда import экранга_җибәрү_тамыр


def 해상도시험(너비, 높이, үлчәм_юл):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    үлчәмен_үзгәртү_СМС = '{}x{}'.format(너비, 높이)
    Процесс_VALUE = subprocess.Popen(['python3', str(экранга_җибәрү_тамыр/'Кораллар/үтәргә_команда.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', үлчәмен_үзгәртү_СМС], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    сайлагыч_a916db4e = selectors.DefaultSelector(); сайлагыч_a916db4e.register(Процесс_VALUE.stdout, selectors.EVENT_READ)
    LOG_юл = bytearray(); читтәге_VALUE = None; күчерү_VALUE_630ba093 = None

    def 기다리기(күрсәтү_VALUE, эшләтү=0):
        마감 = time.monotonic() + 60
        while күрсәтү_VALUE not in LOG_юл[эшләтү:]:
            if time.monotonic() > 마감 or Процесс_VALUE.poll() is not None or b'HALTED' in LOG_юл or b'PANIC:' in LOG_юл:
                raise AssertionError(LOG_юл[эшләтү:].decode('utf-8', 'replace'))
            for вакыйга, _ in сайлагыч_a916db4e.select(.1):
                мәгълүмат = вакыйга.fileobj.read(65536)
                if мәгълүмат: LOG_юл.extend(мәгълүмат)
        return LOG_юл[эшләтү:].decode('utf-8', 'replace')

    def чирттерү_төймә(символ, 눌림=True): читтәге_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, символ))

    def СМС_җибәрү(Mäten):
        эшләтү = len(LOG_юл)
        for символ_VALUE_068c2631 in Mäten:
            символ = 0xff0d if символ_VALUE_068c2631 == '\n' else ord(символ_VALUE_068c2631) if ord(символ_VALUE_068c2631) < 256 else 0x1000000 | ord(символ_VALUE_068c2631)
            чирттерү_төймә(символ); чирттерү_төймә(символ, False)
        return эшләтү

    def тышча(Mäten): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', СМС_җибәрү(Mäten+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Вертикаль_урнаштыру, 눌림): читтәге_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Вертикаль_урнаштыру))

    def чирттерү_VALUE(가로, Вертикаль_урнаштыру): 가리키기(가로, Вертикаль_урнаштыру, 1); 가리키기(가로, Вертикаль_урнаштыру, 0)

    def нокталы_рәсем_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 фактик_мәгълүмат 너비를 쓴다.
        читтәге_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        сызым_VALUE = Image.new('RGB', (너비, 높이)); өлкә_VALUE = 0
        while True:
            종류 = EXACT_VALUE(читтәге_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                озынлык_VALUE = struct.unpack('>I', EXACT_VALUE(читтәге_VALUE, 7)[3:])[0]; EXACT_VALUE(читтәге_VALUE, озынлык_VALUE); continue
            assert 종류 == 0, 종류
            элемент_COUNT = struct.unpack('>H', EXACT_VALUE(читтәге_VALUE, 3)[1:])[0]
            for _ in range(элемент_COUNT):
                가로, Вертикаль_урнаштыру, 폭, озынлык_VALUE, кодлау_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(читтәге_VALUE, 12))
                assert кодлау_VALUE == 0 and 가로+폭 <= 너비 and Вертикаль_урнаштыру+озынлык_VALUE <= 높이
                сызым_VALUE.paste(Image.frombytes('RGB', (폭, озынлык_VALUE), EXACT_VALUE(читтәге_VALUE, 폭*озынлык_VALUE*4), 'raw', 'BGRX'), (가로, Вертикаль_урнаштыру))
                өлкә_VALUE += 폭*озынлык_VALUE
            if өлкә_VALUE:
                assert өлкә_VALUE == 너비*높이, өлкә_VALUE
                return сызым_VALUE

    def чек_нокта(координат_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            сызым_VALUE = нокталы_рәсем_IMAGE()
            if сызым_VALUE.getpixel(координат_VALUE) == 색: return сызым_VALUE
            if time.monotonic() > 마감: raise AssertionError((координат_VALUE, сызым_VALUE.getpixel(координат_VALUE), 색))

    def йөкләп_җибәрү_Файллар(исем, мәгълүмат): күчерү_VALUE_630ba093.storbinary('STOR '+исем, io.BytesIO(мәгълүмат))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+үлчәмен_үзгәртү_СМС+' RGB32').encode() in LOG_юл
        print('BOOT:', үлчәмен_үзгәртү_СМС, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_юл).group(1))
        читтәге_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(читтәге_VALUE, 12) == b'RFB 003.008\n'; читтәге_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(читтәге_VALUE, EXACT_VALUE(читтәге_VALUE, 1)[0]); читтәге_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(читтәге_VALUE, 4) == b'\0'*4; читтәге_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(читтәге_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(читтәге_VALUE, struct.unpack('>I', 초기[20:])[0])
        читтәге_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        читтәге_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        чек_нокта((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        чек_нокта((너비-568, 높이-360), (32, 80, 144))
        эшләтү = len(LOG_юл); чирттерү_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', эшләтү)
        чек_нокта((너비-568, 높이-360), (24, 32, 48))
        эшләтү = len(LOG_юл); чирттерү_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', эшләтү)
        тышча('ftpd start')
        күчерү_VALUE_630ba093 = ftplib.FTP(); күчерү_VALUE_630ba093.encoding = 'utf-8'; күчерү_VALUE_630ba093.connect('127.0.0.1', 접속번호, timeout=20); күчерү_VALUE_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·клип 밖·빈 사각형을 포함한다.
        чыганак = '''#include <화면규약.h>
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
    язу_файл_мәгълүмат(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        йөкләп_җибәрү_Файллар('화면시험.c', чыганак.encode())
        assert 'exit 0' in тышча('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', СМС_җибәрү('run /화면시험\n'))
        чек_нокта((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', СМС_җибәрү('q'))
        чыганак = '''from Татарча import 화면크기, 네모그리기, 그림기다리기, 출력, система_хата
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except система_хата as Хата:
    assert Хата.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        йөкләп_җибәрү_Файллар('화면시험.py', чыганак.encode())
        기다리기(b'PYTHON RESOLUTION PASS', СМС_җибәрү('python /화면시험.py\n'))
        чек_нокта((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', СМС_җибәрү('q'))
        чыганак = '''import Татарча.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("үлчәмен_үзгәртү");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("клип"); }
        catch (잘못된인수예외 Хата) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 хост javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = үлчәм_юл/'해상도경계시험.java'
        경계원문.write_text(чыганак.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(экранга_җибәрү_тамыр/'dist/jkoros-native-korean.jar'), '-d', str(үлчәм_юл), str(경계원문)])
        йөкләп_җибәрү_Файллар('해상도경계시험.class', (үлчәм_юл/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', СМС_җибәрү('java 해상도경계시험\n'))
        чек_нокта((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', СМС_җибәрү('q'))
        # 게스트 javac의 ярдәм_VALUE 문법으로 үлчәмен_үзгәртү таләп_VALUE·지우기·다섯 인수 그리기를 컴파일한다.
        чыганак = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=Татарча.자체.화면.너비();
        int 높이=Татарча.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Татарча.자체.화면.지우기(3153944);
        Татарча.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        Татарча.자체.출력.язу_юл("JAVA RESOLUTION PASS");
        Татарча.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        йөкләп_җибәрү_Файллар('해상도시험.java', чыганак.encode())
        үлчәм = тышча('javac 해상도시험.java'); assert 'exit 0' in үлчәм, үлчәм
        기다리기(b'JAVA RESOLUTION PASS', СМС_җибәрү('java 해상도시험\n'))
        чек_нокта((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', СМС_җибәрү('q'))
        йөкләп_җибәрү_Файллар('스윙시험.class', (үлчәм_юл/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', СМС_җибәрү('java 스윙시험\n'))
        가로, Вертикаль_урнаштыру = (너비-400)//2, (높이-280)//2
        сызым_VALUE = чек_нокта((가로, Вертикаль_урнаштыру), (32, 80, 144))
        сызым_VALUE.save(str(үлчәм_юл/(үлчәмен_үзгәртү_СМС+'.png')))
        эшләтү = len(LOG_юл); чирттерү_VALUE(가로+80, Вертикаль_урнаштыру+155)
        기다리기('SWING CLICK исем'.encode(), эшләтү)
        эшләтү = len(LOG_юл); чирттерү_VALUE(가로+385, Вертикаль_урнаштыру+15); 기다리기(b'jkoros-native> ', эшләтү)
        assert 'AFTER_RESOLUTION' in тышча('echo AFTER_RESOLUTION')
        print('PASS:', үлчәмен_үзгәртү_СМС, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if күчерү_VALUE_630ba093: күчерү_VALUE_630ba093.close()
        if читтәге_VALUE: читтәге_VALUE.close()
        if Процесс_VALUE.poll() is None:
            Процесс_VALUE.terminate()
            try: Процесс_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Процесс_VALUE.kill(); Процесс_VALUE.wait()
        сайлагыч_a916db4e.close(); Процесс_VALUE.stdout.close()
        (үлчәм_юл/(үлчәмен_үзгәртү_СМС+'.log')).write_bytes(LOG_юл)


def эшләтү():
    үлчәм_юл = экранга_җибәрү_тамыр/'build/verification/resolution'; үлчәм_юл.mkdir(parents=True, exist_ok=True)
    LOG_юл = {'passed': False, 'kernel_sha256': hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for дөрес_булмаган_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            үлчәм = subprocess.run(['python3', str(экранга_җибәрү_тамыр/'Кораллар/үтәргә_команда.py'), '--resolution', дөрес_булмаган_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert үлчәм.returncode == 2 and b'--resolution' in үлчәм.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(үлчәм_юл), str(экранга_җибәрү_тамыр/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, үлчәм_юл); LOG_юл['resolutions'].append([너비, 높이])
        LOG_юл.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (үлчәм_юл/'report.json').write_text(json.dumps(LOG_юл, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': эшләтү()
