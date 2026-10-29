#!/usr/bin/env python3
"""фактично_дані QEMU/VNC에서 화면 Розмір·경계·Вікно переміщати_значення·Swing·언어별 그리기를 검사한다."""
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
from настільний_Вигляд import 정확한값
from Виконати_команда import Дії_корінь


def 해상도시험(너비, 높이, КР_шлях):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); номер_порту = 임시.getsockname()[1]
    змінювати_розмір_Текст = '{}x{}'.format(너비, 높이)
    процес_значення = subprocess.Popen(['python3', str(Дії_корінь/'інструменти/Виконати_команда.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(номер_порту), '--resolution', змінювати_розмір_Текст], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор_a916db4e = selectors.DefaultSelector(); селектор_a916db4e.register(процес_значення.stdout, selectors.EVENT_READ)
    журнал_запис = bytearray(); віддалений_значення = None; передача_значення = None

    def 기다리기(показувати_значення, запустити=0):
        крайнiй_термін_значення = time.monotonic() + 60
        while показувати_значення not in журнал_запис[запустити:]:
            if time.monotonic() > крайнiй_термін_значення or процес_значення.poll() is not None or b'HALTED' in журнал_запис or b'PANIC:' in журнал_запис:
                raise AssertionError(журнал_запис[запустити:].decode('utf-8', 'replace'))
            for Подія, _ in селектор_a916db4e.select(.1):
                дані = Подія.fileobj.read(65536)
                if дані: журнал_запис.extend(дані)
        return журнал_запис[запустити:].decode('utf-8', 'replace')

    def клік_кнопка(символ, 눌림=True): віддалений_значення.sendall(struct.pack('>BBHI', 4, int(눌림), 0, символ))

    def надіслати_SMS(текст):
        запустити = len(журнал_запис)
        for символ_значення_068c2631 in текст:
            символ = 0xff0d if символ_значення_068c2631 == '\n' else ord(символ_значення_068c2631) if ord(символ_значення_068c2631) < 256 else 0x1000000 | ord(символ_значення_068c2631)
            клік_кнопка(символ); клік_кнопка(символ, False)
        return запустити

    def оболонка(текст): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', надіслати_SMS(текст+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Вертикаль_посада, 눌림): віддалений_значення.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Вертикаль_посада))

    def клік_значення(가로, Вертикаль_посада): 가리키기(가로, Вертикаль_посада, 1); 가리키기(가로, Вертикаль_посада, 0)

    def бітова_карта_фото():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 фактично_дані 너비를 쓴다.
        віддалений_значення.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        малювання_значення = Image.new('RGB', (너비, 높이)); область_значення_9285603e = 0
        while True:
            종류 = 정확한값(віддалений_значення, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', 정확한값(віддалений_значення, 7)[3:])[0]; 정확한값(віддалений_значення, 길이); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(віддалений_значення, 3)[1:])[0]
            for _ in range(개수):
                가로, Вертикаль_посада, 폭, 길이, кодування_значення = struct.unpack('>HHHHi', 정확한값(віддалений_значення, 12))
                assert кодування_значення == 0 and 가로+폭 <= 너비 and Вертикаль_посада+길이 <= 높이
                малювання_значення.paste(Image.frombytes('RGB', (폭, 길이), 정확한값(віддалений_значення, 폭*길이*4), 'raw', 'BGRX'), (가로, Вертикаль_посада))
                область_значення_9285603e += 폭*길이
            if область_значення_9285603e:
                assert область_значення_9285603e == 너비*높이, область_значення_9285603e
                return малювання_значення

    def перевіряти_елемент_зображення(좌표, 색):
        крайнiй_термін_значення = time.monotonic()+10
        while True:
            малювання_значення = бітова_карта_фото()
            if малювання_значення.getpixel(좌표) == 색: return малювання_значення
            if time.monotonic() > крайнiй_термін_значення: raise AssertionError((좌표, малювання_значення.getpixel(좌표), 색))

    def передавати_Файли(Назва, дані): передача_значення.storbinary('STOR '+Назва, io.BytesIO(дані))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+змінювати_розмір_Текст+' RGB32').encode() in журнал_запис
        print('BOOT:', змінювати_розмір_Текст, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', журнал_запис).group(1))
        віддалений_значення = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(віддалений_значення, 12) == b'RFB 003.008\n'; віддалений_значення.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(віддалений_значення, 정확한값(віддалений_значення, 1)[0]); віддалений_значення.sendall(b'\x01')
        assert 정확한값(віддалений_значення, 4) == b'\0'*4; віддалений_значення.sendall(b'\x01')
        початковий_стан = 정확한값(віддалений_значення, 24); assert struct.unpack('>HH', початковий_стан[:4]) == (너비, 높이)
        정확한값(віддалений_значення, struct.unpack('>I', початковий_стан[20:])[0])
        віддалений_значення.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        віддалений_значення.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        перевіряти_елемент_зображення((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        перевіряти_елемент_зображення((너비-568, 높이-360), (32, 80, 144))
        запустити = len(журнал_запис); клік_значення(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', запустити)
        перевіряти_елемент_зображення((너비-568, 높이-360), (24, 32, 48))
        запустити = len(журнал_запис); клік_значення(80, 16); 기다리기(b'TERMINAL FOCUS 1', запустити)
        оболонка('ftpd start')
        передача_значення = ftplib.FTP(); передача_значення.encoding = 'utf-8'; передача_значення.connect('127.0.0.1', номер_порту, timeout=20); передача_значення.login()
        # C 경계 검사는 32비트 unsigned 음수 перетворити_значення·кліп 밖·빈 사각형을 포함한다.
        вихіднийКод = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(малювати_прямокутник(너비,높이,0,0,0)) return 2;
    if(малювати_прямокутник(너비,높이-1,1,1,0)!=-22) return 3;
    if(малювати_прямокутник(너비-1,높이,1,1,0)!=-22) return 4;
    if(малювати_прямокутник(-1,0,1,1,0)!=-22) return 5;
    if(малювати_прямокутник(0,0,-1,1,0)!=-22) return 6;
    if(малювати_прямокутник(너비-1,높이-1,1,1,0x332211)) return 7;
    записування_Файл_дані(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        передавати_Файли('화면시험.c', вихіднийКод.encode())
        assert 'exit 0' in оболонка('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', надіслати_SMS('run /화면시험\n'))
        перевіряти_елемент_зображення((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', надіслати_SMS('q'))
        вихіднийКод = '''from українська import 화면크기, малювати_прямокутник, 그림기다리기, Вивід, Система_помилка
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    малювати_прямокутник(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except Система_помилка as ПОМИЛКА:
    assert ПОМИЛКА.індекс == 22
малювати_прямокутник(너비-1, 높이-1, 1, 1, 0x665544)
Вивід("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        передавати_Файли('화면시험.py', вихіднийКод.encode())
        기다리기(b'PYTHON RESOLUTION PASS', надіслати_SMS('python /화면시험.py\n'))
        перевіряти_елемент_зображення((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', надіслати_SMS('q'))
        вихіднийКод = '''import українська.своє.*;
public class 해상도시험 {
    public static void main(String[] аргументи) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Стан_виняток("Розмір");
        try { 화면.прямокутник(너비,높이-1,1,1,0); throw new Стан_виняток("кліп"); }
        catch (недійсний_аргумент_виняток ПОМИЛКА) { }
        화면.видаляти_запис(0x302018);
        화면.прямокутник(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # виняток 처리는 хост javac 결과를 своє JVM에 올려 검사한다.
        경계원문 = КР_шлях/'해상도경계시험.java'
        경계원문.write_text(вихіднийКод.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Дії_корінь/'dist/jkoros-native-korean.jar'), '-d', str(КР_шлях), str(경계원문)])
        передавати_Файли('해상도경계시험.class', (КР_шлях/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', надіслати_SMS('java 해상도경계시험\n'))
        перевіряти_елемент_зображення((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', надіслати_SMS('q'))
        # 게스트 javac의 опора_значення 문법으로 Розмір запит_значення·видаляти_запис·다섯 аргументи 그리기를 컴파일한다.
        вихіднийКод = '''public class 해상도시험 {
    public static void main(String[] аргументи) {
        int 너비=українська.своє.화면.너비();
        int 높이=українська.своє.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        українська.своє.화면.видаляти_запис(3153944);
        українська.своє.화면.прямокутник(너비-1,높이-1,1,1,10061943);
        українська.своє.Вивід.записування_рядок("JAVA RESOLUTION PASS");
        українська.своє.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        передавати_Файли('해상도시험.java', вихіднийКод.encode())
        результат = оболонка('javac 해상도시험.java'); assert 'exit 0' in результат, результат
        기다리기(b'JAVA RESOLUTION PASS', надіслати_SMS('java 해상도시험\n'))
        перевіряти_елемент_зображення((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', надіслати_SMS('q'))
        передавати_Файли('스윙시험.class', (КР_шлях/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', надіслати_SMS('java 스윙시험\n'))
        가로, Вертикаль_посада = (너비-400)//2, (높이-280)//2
        малювання_значення = перевіряти_елемент_зображення((가로, Вертикаль_посада), (32, 80, 144))
        малювання_значення.save(str(КР_шлях/(змінювати_розмір_Текст+'.png')))
        запустити = len(журнал_запис); клік_значення(가로+80, Вертикаль_посада+155)
        기다리기('SWING CLICK Назва'.encode(), запустити)
        запустити = len(журнал_запис); клік_значення(가로+385, Вертикаль_посада+15); 기다리기(b'jkoros-native> ', запустити)
        assert 'AFTER_RESOLUTION' in оболонка('echo AFTER_RESOLUTION')
        print('PASS:', змінювати_розмір_Текст, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if передача_значення: передача_значення.close()
        if віддалений_значення: віддалений_значення.close()
        if процес_значення.poll() is None:
            процес_значення.terminate()
            try: процес_значення.wait(timeout=8)
            except subprocess.TimeoutExpired: процес_значення.kill(); процес_значення.wait()
        селектор_a916db4e.close(); процес_значення.stdout.close()
        (КР_шлях/(змінювати_розмір_Текст+'.log')).write_bytes(журнал_запис)


def запустити():
    КР_шлях = Дії_корінь/'build/verification/resolution'; КР_шлях.mkdir(parents=True, exist_ok=True)
    журнал_запис = {'passed': False, 'kernel_sha256': hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for недійсний_значення in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            результат = subprocess.run(['python3', str(Дії_корінь/'інструменти/Виконати_команда.py'), '--resolution', недійсний_значення], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert результат.returncode == 2 and b'--resolution' in результат.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(КР_шлях), str(Дії_корінь/'випробування/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, КР_шлях); журнал_запис['resolutions'].append([너비, 높이])
        журнал_запис.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (КР_шлях/'report.json').write_text(json.dumps(журнал_запис, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': запустити()
