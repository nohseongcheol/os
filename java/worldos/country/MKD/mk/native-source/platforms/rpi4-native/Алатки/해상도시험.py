#!/usr/bin/env python3
"""реален_податоци QEMU/VNC에서 화면 Големина·경계·прозорец премести_VALUE·Swing·언어별 그리기를 검사한다."""
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
from десктоп_Приказ import EXACT_VALUE
from Изврши_наредба import Project_корен


def 해상도시험(너비, 높이, мерка_патека):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); број_на_порта = 임시.getsockname()[1]
    големина_СМС = '{}x{}'.format(너비, 높이)
    Процес_VALUE = subprocess.Popen(['python3', str(Project_корен/'Алатки/Изврши_наредба.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(број_на_порта), '--resolution', големина_СМС], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    избирач_a916db4e = selectors.DefaultSelector(); избирач_a916db4e.register(Процес_VALUE.stdout, selectors.EVENT_READ)
    LOG_ред = bytearray(); далечинскo_VALUE = None; пренос_VALUE = None

    def 기다리기(прикажи_VALUE, Изврши_2=0):
        마감 = time.monotonic() + 60
        while прикажи_VALUE not in LOG_ред[Изврши_2:]:
            if time.monotonic() > 마감 or Процес_VALUE.poll() is not None or b'HALTED' in LOG_ред or b'PANIC:' in LOG_ред:
                raise AssertionError(LOG_ред[Изврши_2:].decode('utf-8', 'replace'))
            for настан, _ in избирач_a916db4e.select(.1):
                податоци = настан.fileobj.read(65536)
                if податоци: LOG_ред.extend(податоци)
        return LOG_ред[Изврши_2:].decode('utf-8', 'replace')

    def кликни_копче(симбол, 눌림=True): далечинскo_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, симбол))

    def испрати_СМС(Текст):
        Изврши_2 = len(LOG_ред)
        for знак_VALUE in Текст:
            симбол = 0xff0d if знак_VALUE == '\n' else ord(знак_VALUE) if ord(знак_VALUE) < 256 else 0x1000000 | ord(знак_VALUE)
            кликни_копче(симбол); кликни_копче(симбол, False)
        return Изврши_2

    def обвивка(Текст): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', испрати_СМС(Текст+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, вертикала_позиционирање, 눌림): далечинскo_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, вертикала_позиционирање))

    def кликни_VALUE(가로, вертикала_позиционирање): 가리키기(가로, вертикала_позиционирање, 1); 가리키기(가로, вертикала_позиционирање, 0)

    def бит_мапа_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 реален_податоци 너비를 쓴다.
        далечинскo_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        цртеж_VALUE = Image.new('RGB', (너비, 높이)); област_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(далечинскo_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                должина_VALUE = struct.unpack('>I', EXACT_VALUE(далечинскo_VALUE, 7)[3:])[0]; EXACT_VALUE(далечинскo_VALUE, должина_VALUE); continue
            assert 종류 == 0, 종류
            ставка_COUNT = struct.unpack('>H', EXACT_VALUE(далечинскo_VALUE, 3)[1:])[0]
            for _ in range(ставка_COUNT):
                가로, вертикала_позиционирање, 폭, должина_VALUE, кодирање_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(далечинскo_VALUE, 12))
                assert кодирање_VALUE == 0 and 가로+폭 <= 너비 and вертикала_позиционирање+должина_VALUE <= 높이
                цртеж_VALUE.paste(Image.frombytes('RGB', (폭, должина_VALUE), EXACT_VALUE(далечинскo_VALUE, 폭*должина_VALUE*4), 'raw', 'BGRX'), (가로, вертикала_позиционирање))
                област_VALUE_9285603e += 폭*должина_VALUE
            if област_VALUE_9285603e:
                assert област_VALUE_9285603e == 너비*높이, област_VALUE_9285603e
                return цртеж_VALUE

    def провери_пиксел(координата_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            цртеж_VALUE = бит_мапа_IMAGE()
            if цртеж_VALUE.getpixel(координата_VALUE) == 색: return цртеж_VALUE
            if time.monotonic() > 마감: raise AssertionError((координата_VALUE, цртеж_VALUE.getpixel(координата_VALUE), 색))

    def постави_Датотеки(Име, податоци): пренос_VALUE.storbinary('STOR '+Име, io.BytesIO(податоци))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+големина_СМС+' RGB32').encode() in LOG_ред
        print('BOOT:', големина_СМС, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_ред).group(1))
        далечинскo_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(далечинскo_VALUE, 12) == b'RFB 003.008\n'; далечинскo_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(далечинскo_VALUE, EXACT_VALUE(далечинскo_VALUE, 1)[0]); далечинскo_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(далечинскo_VALUE, 4) == b'\0'*4; далечинскo_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(далечинскo_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(далечинскo_VALUE, struct.unpack('>I', 초기[20:])[0])
        далечинскo_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        далечинскo_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        провери_пиксел((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        провери_пиксел((너비-568, 높이-360), (32, 80, 144))
        Изврши_2 = len(LOG_ред); кликни_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Изврши_2)
        провери_пиксел((너비-568, 높이-360), (24, 32, 48))
        Изврши_2 = len(LOG_ред); кликни_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Изврши_2)
        обвивка('ftpd start')
        пренос_VALUE = ftplib.FTP(); пренос_VALUE.encoding = 'utf-8'; пренос_VALUE.connect('127.0.0.1', број_на_порта, timeout=20); пренос_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·клип 밖·빈 사각형을 포함한다.
        ИЗВОР = '''#include <화면규약.h>
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
    запиши_датотека_податоци(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        постави_Датотеки('화면시험.c', ИЗВОР.encode())
        assert 'exit 0' in обвивка('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', испрати_СМС('run /화면시험\n'))
        провери_пиксел((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', испрати_СМС('q'))
        ИЗВОР = '''from Македонски import 화면크기, 네모그리기, 그림기다리기, 출력, систем_грешка
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except систем_грешка as ГРЕШКА:
    assert ГРЕШКА.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        постави_Датотеки('화면시험.py', ИЗВОР.encode())
        기다리기(b'PYTHON RESOLUTION PASS', испрати_СМС('python /화면시험.py\n'))
        провери_пиксел((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', испрати_СМС('q'))
        ИЗВОР = '''import Македонски.자체.*;
public class 해상도시험 {
    public static void main(String[] Аргументи) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new статус_исклучок("Големина");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new статус_исклучок("клип"); }
        catch (неважечки_аргумент_исклучок ГРЕШКА) { }
        화면.избриши_внес(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # исклучок 처리는 вдоми javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = мерка_патека/'해상도경계시험.java'
        경계원문.write_text(ИЗВОР.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_корен/'dist/jkoros-native-korean.jar'), '-d', str(мерка_патека), str(경계원문)])
        постави_Датотеки('해상도경계시험.class', (мерка_патека/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', испрати_СМС('java 해상도경계시험\n'))
        провери_пиксел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', испрати_СМС('q'))
        # 게스트 javac의 Поддршка_VALUE 문법으로 Големина прашалник_VALUE·избриши_внес·다섯 Аргументи 그리기를 컴파일한다.
        ИЗВОР = '''public class 해상도시험 {
    public static void main(String[] Аргументи) {
        int 너비=Македонски.자체.화면.너비();
        int 높이=Македонски.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Македонски.자체.화면.избриши_внес(3153944);
        Македонски.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        Македонски.자체.출력.запиши_ред("JAVA RESOLUTION PASS");
        Македонски.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        постави_Датотеки('해상도시험.java', ИЗВОР.encode())
        мерка = обвивка('javac 해상도시험.java'); assert 'exit 0' in мерка, мерка
        기다리기(b'JAVA RESOLUTION PASS', испрати_СМС('java 해상도시험\n'))
        провери_пиксел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', испрати_СМС('q'))
        постави_Датотеки('스윙시험.class', (мерка_патека/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', испрати_СМС('java 스윙시험\n'))
        가로, вертикала_позиционирање = (너비-400)//2, (높이-280)//2
        цртеж_VALUE = провери_пиксел((가로, вертикала_позиционирање), (32, 80, 144))
        цртеж_VALUE.save(str(мерка_патека/(големина_СМС+'.png')))
        Изврши_2 = len(LOG_ред); кликни_VALUE(가로+80, вертикала_позиционирање+155)
        기다리기('SWING CLICK Име'.encode(), Изврши_2)
        Изврши_2 = len(LOG_ред); кликни_VALUE(가로+385, вертикала_позиционирање+15); 기다리기(b'jkoros-native> ', Изврши_2)
        assert 'AFTER_RESOLUTION' in обвивка('echo AFTER_RESOLUTION')
        print('PASS:', големина_СМС, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if пренос_VALUE: пренос_VALUE.close()
        if далечинскo_VALUE: далечинскo_VALUE.close()
        if Процес_VALUE.poll() is None:
            Процес_VALUE.terminate()
            try: Процес_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Процес_VALUE.kill(); Процес_VALUE.wait()
        избирач_a916db4e.close(); Процес_VALUE.stdout.close()
        (мерка_патека/(големина_СМС+'.log')).write_bytes(LOG_ред)


def Изврши_2():
    мерка_патека = Project_корен/'build/verification/resolution'; мерка_патека.mkdir(parents=True, exist_ok=True)
    LOG_ред = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for неважечки_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            мерка = subprocess.run(['python3', str(Project_корен/'Алатки/Изврши_наредба.py'), '--resolution', неважечки_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert мерка.returncode == 2 and b'--resolution' in мерка.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(мерка_патека), str(Project_корен/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, мерка_патека); LOG_ред['resolutions'].append([너비, 높이])
        LOG_ред.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (мерка_патека/'report.json').write_text(json.dumps(LOG_ред, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Изврши_2()
