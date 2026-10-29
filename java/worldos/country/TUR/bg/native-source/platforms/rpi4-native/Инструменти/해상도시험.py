#!/usr/bin/env python3
"""действителен_данни QEMU/VNC에서 화면 Размер·경계·Прозорец движа_се_стойност·Swing·언어별 그리기를 검사한다."""
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
from десктоп_Изглед import 정확한값
from изпълнявам_команда import проект_корен


def 해상도시험(너비, 높이, мярка_път):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); номер_на_порт = 임시.getsockname()[1]
    размер_Текст = '{}x{}'.format(너비, 높이)
    Процес_стойност = subprocess.Popen(['python3', str(проект_корен/'Инструменти/изпълнявам_команда.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(номер_на_порт), '--resolution', размер_Текст], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    свързан_елемент_за_избор_a916db4e = selectors.DefaultSelector(); свързан_елемент_за_избор_a916db4e.register(Процес_стойност.stdout, selectors.EVENT_READ)
    регистрирам_запис = bytearray(); отдалечен_стойност = None; прехвърлям_стойност = None

    def 기다리기(показвам_стойност, Стартиране=0):
        краен_срок_стойност = time.monotonic() + 60
        while показвам_стойност not in регистрирам_запис[Стартиране:]:
            if time.monotonic() > краен_срок_стойност or Процес_стойност.poll() is not None or b'HALTED' in регистрирам_запис or b'PANIC:' in регистрирам_запис:
                raise AssertionError(регистрирам_запис[Стартиране:].decode('utf-8', 'replace'))
            for Събитие, _ in свързан_елемент_за_избор_a916db4e.select(.1):
                данни = Събитие.fileobj.read(65536)
                if данни: регистрирам_запис.extend(данни)
        return регистрирам_запис[Стартиране:].decode('utf-8', 'replace')

    def кликвам_бутон(символ, 눌림=True): отдалечен_стойност.sendall(struct.pack('>BBHI', 4, int(눌림), 0, символ))

    def изпращане_на_SMS(Текст):
        Стартиране = len(регистрирам_запис)
        for знак_стойност in Текст:
            символ = 0xff0d if знак_стойност == '\n' else ord(знак_стойност) if ord(знак_стойност) < 256 else 0x1000000 | ord(знак_стойност)
            кликвам_бутон(символ); кликвам_бутон(символ, False)
        return Стартиране

    def обвивка(Текст): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', изпращане_на_SMS(Текст+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, вертикал_позиция, 눌림): отдалечен_стойност.sendall(struct.pack('>BBHH', 5, 눌림, 가로, вертикал_позиция))

    def кликвам_стойност(가로, вертикал_позиция): 가리키기(가로, вертикал_позиция, 1); 가리키기(가로, вертикал_позиция, 0)

    def побитово_представяне_снимка():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 действителен_данни 너비를 쓴다.
        отдалечен_стойност.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        чертеж_стойност = Image.new('RGB', (너비, 높이)); зона_стойност = 0
        while True:
            종류 = 정확한값(отдалечен_стойност, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', 정확한값(отдалечен_стойност, 7)[3:])[0]; 정확한값(отдалечен_стойност, 길이); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(отдалечен_стойност, 3)[1:])[0]
            for _ in range(개수):
                가로, вертикал_позиция, 폭, 길이, кодиране_стойност = struct.unpack('>HHHHi', 정확한값(отдалечен_стойност, 12))
                assert кодиране_стойност == 0 and 가로+폭 <= 너비 and вертикал_позиция+길이 <= 높이
                чертеж_стойност.paste(Image.frombytes('RGB', (폭, 길이), 정확한값(отдалечен_стойност, 폭*길이*4), 'raw', 'BGRX'), (가로, вертикал_позиция))
                зона_стойност += 폭*길이
            if зона_стойност:
                assert зона_стойност == 너비*높이, зона_стойност
                return чертеж_стойност

    def проверявам_пиксел(좌표, 색):
        краен_срок_стойност = time.monotonic()+10
        while True:
            чертеж_стойност = побитово_представяне_снимка()
            if чертеж_стойност.getpixel(좌표) == 색: return чертеж_стойност
            if time.monotonic() > краен_срок_стойност: raise AssertionError((좌표, чертеж_стойност.getpixel(좌표), 색))

    def качвам_Файлове(Име, данни): прехвърлям_стойност.storbinary('STOR '+Име, io.BytesIO(данни))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+размер_Текст+' RGB32').encode() in регистрирам_запис
        print('BOOT:', размер_Текст, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', регистрирам_запис).group(1))
        отдалечен_стойност = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(отдалечен_стойност, 12) == b'RFB 003.008\n'; отдалечен_стойност.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(отдалечен_стойност, 정확한값(отдалечен_стойност, 1)[0]); отдалечен_стойност.sendall(b'\x01')
        assert 정확한값(отдалечен_стойност, 4) == b'\0'*4; отдалечен_стойност.sendall(b'\x01')
        първоначално_състояние = 정확한값(отдалечен_стойност, 24); assert struct.unpack('>HH', първоначално_състояние[:4]) == (너비, 높이)
        정확한값(отдалечен_стойност, struct.unpack('>I', първоначално_състояние[20:])[0])
        отдалечен_стойност.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        отдалечен_стойност.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        проверявам_пиксел((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        проверявам_пиксел((너비-568, 높이-360), (32, 80, 144))
        Стартиране = len(регистрирам_запис); кликвам_стойност(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Стартиране)
        проверявам_пиксел((너비-568, 높이-360), (24, 32, 48))
        Стартиране = len(регистрирам_запис); кликвам_стойност(80, 16); 기다리기(b'TERMINAL FOCUS 1', Стартиране)
        обвивка('ftpd start')
        прехвърлям_стойност = ftplib.FTP(); прехвърлям_стойност.encoding = 'utf-8'; прехвърлям_стойност.connect('127.0.0.1', номер_на_порт, timeout=20); прехвърлям_стойност.login()
        # C 경계 검사는 32비트 unsigned 음수 преобразувам_стойност·клип 밖·빈 사각형을 포함한다.
        ИЗТОЧНИК = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(рисувам_правоъгълник(너비,높이,0,0,0)) return 2;
    if(рисувам_правоъгълник(너비,높이-1,1,1,0)!=-22) return 3;
    if(рисувам_правоъгълник(너비-1,높이,1,1,0)!=-22) return 4;
    if(рисувам_правоъгълник(-1,0,1,1,0)!=-22) return 5;
    if(рисувам_правоъгълник(0,0,-1,1,0)!=-22) return 6;
    if(рисувам_правоъгълник(너비-1,높이-1,1,1,0x332211)) return 7;
    записване_Файл_данни(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        качвам_Файлове('화면시험.c', ИЗТОЧНИК.encode())
        assert 'exit 0' in обвивка('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', изпращане_на_SMS('run /화면시험\n'))
        проверявам_пиксел((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', изпращане_на_SMS('q'))
        ИЗТОЧНИК = '''from Български import 화면크기, рисувам_правоъгълник, 그림기다리기, Изход, система_грешка
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    рисувам_правоъгълник(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except система_грешка as ГРЕШКА:
    assert ГРЕШКА.индекс == 22
рисувам_правоъгълник(너비-1, 높이-1, 1, 1, 0x665544)
Изход("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        качвам_Файлове('화면시험.py', ИЗТОЧНИК.encode())
        기다리기(b'PYTHON RESOLUTION PASS', изпращане_на_SMS('python /화면시험.py\n'))
        проверявам_пиксел((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', изпращане_на_SMS('q'))
        ИЗТОЧНИК = '''import Български.자체.*;
public class 해상도시험 {
    public static void main(String[] Параметри) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Състояние_изключение("Размер");
        try { 화면.правоъгълник(너비,높이-1,1,1,0); throw new Състояние_изключение("клип"); }
        catch (невалиден_аргумент_изключение ГРЕШКА) { }
        화면.изтривам_запис(0x302018);
        화면.правоъгълник(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # изключение 처리는 хост javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = мярка_път/'해상도경계시험.java'
        경계원문.write_text(ИЗТОЧНИК.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(проект_корен/'dist/jkoros-native-korean.jar'), '-d', str(мярка_път), str(경계원문)])
        качвам_Файлове('해상도경계시험.class', (мярка_път/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', изпращане_на_SMS('java 해상도경계시험\n'))
        проверявам_пиксел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', изпращане_на_SMS('q'))
        # 게스트 javac의 Поддръжка_стойност 문법으로 Размер заявка_стойност·изтривам_запис·다섯 Параметри 그리기를 컴파일한다.
        ИЗТОЧНИК = '''public class 해상도시험 {
    public static void main(String[] Параметри) {
        int 너비=Български.자체.화면.너비();
        int 높이=Български.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Български.자체.화면.изтривам_запис(3153944);
        Български.자체.화면.правоъгълник(너비-1,높이-1,1,1,10061943);
        Български.자체.Изход.записване_ред("JAVA RESOLUTION PASS");
        Български.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        качвам_Файлове('해상도시험.java', ИЗТОЧНИК.encode())
        РЕЗУЛТАТ = обвивка('javac 해상도시험.java'); assert 'exit 0' in РЕЗУЛТАТ, РЕЗУЛТАТ
        기다리기(b'JAVA RESOLUTION PASS', изпращане_на_SMS('java 해상도시험\n'))
        проверявам_пиксел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', изпращане_на_SMS('q'))
        качвам_Файлове('스윙시험.class', (мярка_път/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', изпращане_на_SMS('java 스윙시험\n'))
        가로, вертикал_позиция = (너비-400)//2, (높이-280)//2
        чертеж_стойност = проверявам_пиксел((가로, вертикал_позиция), (32, 80, 144))
        чертеж_стойност.save(str(мярка_път/(размер_Текст+'.png')))
        Стартиране = len(регистрирам_запис); кликвам_стойност(가로+80, вертикал_позиция+155)
        기다리기('SWING CLICK Име'.encode(), Стартиране)
        Стартиране = len(регистрирам_запис); кликвам_стойност(가로+385, вертикал_позиция+15); 기다리기(b'jkoros-native> ', Стартиране)
        assert 'AFTER_RESOLUTION' in обвивка('echo AFTER_RESOLUTION')
        print('PASS:', размер_Текст, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if прехвърлям_стойност: прехвърлям_стойност.close()
        if отдалечен_стойност: отдалечен_стойност.close()
        if Процес_стойност.poll() is None:
            Процес_стойност.terminate()
            try: Процес_стойност.wait(timeout=8)
            except subprocess.TimeoutExpired: Процес_стойност.kill(); Процес_стойност.wait()
        свързан_елемент_за_избор_a916db4e.close(); Процес_стойност.stdout.close()
        (мярка_път/(размер_Текст+'.log')).write_bytes(регистрирам_запис)


def Стартиране():
    мярка_път = проект_корен/'build/verification/resolution'; мярка_път.mkdir(parents=True, exist_ok=True)
    регистрирам_запис = {'passed': False, 'kernel_sha256': hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for невалиден_стойност in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            РЕЗУЛТАТ = subprocess.run(['python3', str(проект_корен/'Инструменти/изпълнявам_команда.py'), '--resolution', невалиден_стойност], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert РЕЗУЛТАТ.returncode == 2 and b'--resolution' in РЕЗУЛТАТ.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(мярка_път), str(проект_корен/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, мярка_път); регистрирам_запис['resolutions'].append([너비, 높이])
        регистрирам_запис.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (мярка_път/'report.json').write_text(json.dumps(регистрирам_запис, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Стартиране()
