#!/usr/bin/env python3
"""нақты_деректер QEMU/VNC에서 화면 Өлшемі·경계·Терезе жылжыту_мән·Swing·언어별 그리기를 검사한다."""
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
from үстелдік_Көрініс import 정확한값
from орындау_пәрмен import жоба_түбір


def 해상도시험(너비, 높이, өлшем_жол):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); порт_нөмірі = 임시.getsockname()[1]
    өлшемді_өзгерту_Мәтін = '{}x{}'.format(너비, 높이)
    Процесс_мән = subprocess.Popen(['python3', str(жоба_түбір/'Құралдар/орындау_пәрмен.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(порт_нөмірі), '--resolution', өлшемді_өзгерту_Мәтін], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор_a916db4e = selectors.DefaultSelector(); селектор_a916db4e.register(Процесс_мән.stdout, selectors.EVENT_READ)
    журнал_жол = bytearray(); 원격 = None; аудару_мән = None

    def 기다리기(көрсету_мән, Орындау_2=0):
        ең_соңғы_мерзім_мән = time.monotonic() + 60
        while көрсету_мән not in журнал_жол[Орындау_2:]:
            if time.monotonic() > ең_соңғы_мерзім_мән or Процесс_мән.poll() is not None or b'HALTED' in журнал_жол or b'PANIC:' in журнал_жол:
                raise AssertionError(журнал_жол[Орындау_2:].decode('utf-8', 'replace'))
            for Оқиға, _ in селектор_a916db4e.select(.1):
                деректер = Оқиға.fileobj.read(65536)
                if деректер: журнал_жол.extend(деректер)
        return журнал_жол[Орындау_2:].decode('utf-8', 'replace')

    def басу_түйме(символ, 눌림=True): 원격.sendall(struct.pack('>BBHI', 4, int(눌림), 0, символ))

    def SMS_жіберу(Мәтін):
        Орындау_2 = len(журнал_жол)
        for таңба_мән in Мәтін:
            символ = 0xff0d if таңба_мән == '\n' else ord(таңба_мән) if ord(таңба_мән) < 256 else 0x1000000 | ord(таңба_мән)
            басу_түйме(символ); басу_түйме(символ, False)
        return Орындау_2

    def қоршам(Мәтін): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_жіберу(Мәтін+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Тік_лауазым, 눌림): 원격.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Тік_лауазым))

    def басу_мән(가로, Тік_лауазым): 가리키기(가로, Тік_лауазым, 1); 가리키기(가로, Тік_лауазым, 0)

    def нүктелік_кескін_сурет():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 нақты_деректер 너비를 쓴다.
        원격.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        сызба_мән = Image.new('RGB', (너비, 높이)); аймақ_мән = 0
        while True:
            종류 = 정확한값(원격, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ұзындық_мән = struct.unpack('>I', 정확한값(원격, 7)[3:])[0]; 정확한값(원격, ұзындық_мән); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(원격, 3)[1:])[0]
            for _ in range(개수):
                가로, Тік_лауазым, 폭, ұзындық_мән, кодтау_мән = struct.unpack('>HHHHi', 정확한값(원격, 12))
                assert кодтау_мән == 0 and 가로+폭 <= 너비 and Тік_лауазым+ұзындық_мән <= 높이
                сызба_мән.paste(Image.frombytes('RGB', (폭, ұзындық_мән), 정확한값(원격, 폭*ұзындық_мән*4), 'raw', 'BGRX'), (가로, Тік_лауазым))
                аймақ_мән += 폭*ұзындық_мән
            if аймақ_мән:
                assert аймақ_мән == 너비*높이, аймақ_мән
                return сызба_мән

    def чек_нүкте(координата_мән, 색):
        ең_соңғы_мерзім_мән = time.monotonic()+10
        while True:
            сызба_мән = нүктелік_кескін_сурет()
            if сызба_мән.getpixel(координата_мән) == 색: return сызба_мән
            if time.monotonic() > ең_соңғы_мерзім_мән: raise AssertionError((координата_мән, сызба_мән.getpixel(координата_мән), 색))

    def Жүктеп_салу_Файлдар(Аты, деректер): аудару_мән.storbinary('STOR '+Аты, io.BytesIO(деректер))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+өлшемді_өзгерту_Мәтін+' RGB32').encode() in журнал_жол
        print('BOOT:', өлшемді_өзгерту_Мәтін, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', журнал_жол).group(1))
        원격 = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(원격, 12) == b'RFB 003.008\n'; 원격.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(원격, 정확한값(원격, 1)[0]); 원격.sendall(b'\x01')
        assert 정확한값(원격, 4) == b'\0'*4; 원격.sendall(b'\x01')
        бастапқы_күй = 정확한값(원격, 24); assert struct.unpack('>HH', бастапқы_күй[:4]) == (너비, 높이)
        정확한값(원격, struct.unpack('>I', бастапқы_күй[20:])[0])
        원격.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        원격.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        чек_нүкте((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        чек_нүкте((너비-568, 높이-360), (32, 80, 144))
        Орындау_2 = len(журнал_жол); басу_мән(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Орындау_2)
        чек_нүкте((너비-568, 높이-360), (24, 32, 48))
        Орындау_2 = len(журнал_жол); басу_мән(80, 16); 기다리기(b'TERMINAL FOCUS 1', Орындау_2)
        қоршам('ftpd start')
        аудару_мән = ftplib.FTP(); аудару_мән.encoding = 'utf-8'; аудару_мән.connect('127.0.0.1', порт_нөмірі, timeout=20); аудару_мән.login()
        # C 경계 검사는 32비트 unsigned 음수 Түрлендіру_мән·клип 밖·빈 사각형을 포함한다.
        Неден = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(Сурет_салу_тік_төртбұрыш(너비,높이,0,0,0)) return 2;
    if(Сурет_салу_тік_төртбұрыш(너비,높이-1,1,1,0)!=-22) return 3;
    if(Сурет_салу_тік_төртбұрыш(너비-1,높이,1,1,0)!=-22) return 4;
    if(Сурет_салу_тік_төртбұрыш(-1,0,1,1,0)!=-22) return 5;
    if(Сурет_салу_тік_төртбұрыш(0,0,-1,1,0)!=-22) return 6;
    if(Сурет_салу_тік_төртбұрыш(너비-1,높이-1,1,1,0x332211)) return 7;
    жазу_файл_деректер(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Жүктеп_салу_Файлдар('화면시험.c', Неден.encode())
        assert 'exit 0' in қоршам('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_жіберу('run /화면시험\n'))
        чек_нүкте((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_жіберу('q'))
        Неден = '''from 한국어 import 화면크기, Сурет_салу_тік_төртбұрыш, 그림기다리기, Шығысы, жүйе_қате
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    Сурет_салу_тік_төртбұрыш(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except жүйе_қате as Қате:
    assert Қате.индекс == 22
Сурет_салу_тік_төртбұрыш(너비-1, 높이-1, 1, 1, 0x665544)
Шығысы("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Жүктеп_салу_Файлдар('화면시험.py', Неден.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_жіберу('python /화면시험.py\n'))
        чек_нүкте((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_жіберу('q'))
        Неден = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] Аргументтер) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new күй_ерекшелік("Өлшемі");
        try { 화면.тік_төртбұрыш(너비,높이-1,1,1,0); throw new күй_ерекшелік("клип"); }
        catch (дұрыс_емес_аргумент_ерекшелік Қате) { }
        화면.өшіру_енгізу(0x302018);
        화면.тік_төртбұрыш(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # ерекшелік 처리는 орналастыру javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = өлшем_жол/'해상도경계시험.java'
        경계원문.write_text(Неден.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(жоба_түбір/'dist/jkoros-native-korean.jar'), '-d', str(өлшем_жол), str(경계원문)])
        Жүктеп_салу_Файлдар('해상도경계시험.class', (өлшем_жол/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_жіберу('java 해상도경계시험\n'))
        чек_нүкте((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_жіберу('q'))
        # 게스트 javac의 тіреу_мән 문법으로 Өлшемі сұрау_мән·өшіру_енгізу·다섯 Аргументтер 그리기를 컴파일한다.
        Неден = '''public class 해상도시험 {
    public static void main(String[] Аргументтер) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.өшіру_енгізу(3153944);
        한국어.자체.화면.тік_төртбұрыш(너비-1,높이-1,1,1,10061943);
        한국어.자체.Шығысы.жазу_жол("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Жүктеп_салу_Файлдар('해상도시험.java', Неден.encode())
        НӘТИЖЕ = қоршам('javac 해상도시험.java'); assert 'exit 0' in НӘТИЖЕ, НӘТИЖЕ
        기다리기(b'JAVA RESOLUTION PASS', SMS_жіберу('java 해상도시험\n'))
        чек_нүкте((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_жіберу('q'))
        Жүктеп_салу_Файлдар('스윙시험.class', (өлшем_жол/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_жіберу('java 스윙시험\n'))
        가로, Тік_лауазым = (너비-400)//2, (높이-280)//2
        сызба_мән = чек_нүкте((가로, Тік_лауазым), (32, 80, 144))
        сызба_мән.save(str(өлшем_жол/(өлшемді_өзгерту_Мәтін+'.png')))
        Орындау_2 = len(журнал_жол); басу_мән(가로+80, Тік_лауазым+155)
        기다리기('SWING CLICK Аты'.encode(), Орындау_2)
        Орындау_2 = len(журнал_жол); басу_мән(가로+385, Тік_лауазым+15); 기다리기(b'jkoros-native> ', Орындау_2)
        assert 'AFTER_RESOLUTION' in қоршам('echo AFTER_RESOLUTION')
        print('PASS:', өлшемді_өзгерту_Мәтін, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if аудару_мән: аудару_мән.close()
        if 원격: 원격.close()
        if Процесс_мән.poll() is None:
            Процесс_мән.terminate()
            try: Процесс_мән.wait(timeout=8)
            except subprocess.TimeoutExpired: Процесс_мән.kill(); Процесс_мән.wait()
        селектор_a916db4e.close(); Процесс_мән.stdout.close()
        (өлшем_жол/(өлшемді_өзгерту_Мәтін+'.log')).write_bytes(журнал_жол)


def Орындау_2():
    өлшем_жол = жоба_түбір/'build/verification/resolution'; өлшем_жол.mkdir(parents=True, exist_ok=True)
    журнал_жол = {'passed': False, 'kernel_sha256': hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for дұрыс_емес_мән in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            НӘТИЖЕ = subprocess.run(['python3', str(жоба_түбір/'Құралдар/орындау_пәрмен.py'), '--resolution', дұрыс_емес_мән], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert НӘТИЖЕ.returncode == 2 and b'--resolution' in НӘТИЖЕ.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(өлшем_жол), str(жоба_түбір/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, өлшем_жол); журнал_жол['resolutions'].append([너비, 높이])
        журнал_жол.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (өлшем_жол/'report.json').write_text(json.dumps(журнал_жол, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Орындау_2()
