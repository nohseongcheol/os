#!/usr/bin/env python3
"""стваран_подаци QEMU/VNC에서 화면 Величина·경계·Прозор помаћи_вриједност·Swing·언어별 그리기를 검사한다."""
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
from десктоп_Приказ import 정확한값
from Изврши_команда import пројектовати_корен


def 해상도시험(너비, 높이, мера_пут):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); број_порта = 임시.getsockname()[1]
    подесити_величину_Текст = '{}x{}'.format(너비, 높이)
    Процес_вриједност = subprocess.Popen(['python3', str(пројектовати_корен/'Алатке/Изврши_команда.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(број_порта), '--resolution', подесити_величину_Текст], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    бирач_a916db4e = selectors.DefaultSelector(); бирач_a916db4e.register(Процес_вриједност.stdout, selectors.EVENT_READ)
    евиденција_ред = bytearray(); удаљен_вриједност = None; пренос_вриједност = None

    def 기다리기(емисија_вриједност, Покрени=0):
        마감 = time.monotonic() + 60
        while емисија_вриједност not in евиденција_ред[Покрени:]:
            if time.monotonic() > 마감 or Процес_вриједност.poll() is not None or b'HALTED' in евиденција_ред or b'PANIC:' in евиденција_ред:
                raise AssertionError(евиденција_ред[Покрени:].decode('utf-8', 'replace'))
            for Догађај, _ in бирач_a916db4e.select(.1):
                подаци = Догађај.fileobj.read(65536)
                if подаци: евиденција_ред.extend(подаци)
        return евиденција_ред[Покрени:].decode('utf-8', 'replace')

    def клик_дугме(симбол, 눌림=True): удаљен_вриједност.sendall(struct.pack('>BBHI', 4, int(눌림), 0, симбол))

    def послати_СМС_поруку(Текст):
        Покрени = len(евиденција_ред)
        for знак_вриједност in Текст:
            симбол = 0xff0d if знак_вриједност == '\n' else ord(знак_вриједност) if ord(знак_вриједност) < 256 else 0x1000000 | ord(знак_вриједност)
            клик_дугме(симбол); клик_дугме(симбол, False)
        return Покрени

    def љуска(Текст): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', послати_СМС_поруку(Текст+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, вертикала_позиција, 눌림): удаљен_вриједност.sendall(struct.pack('>BBHH', 5, 눌림, 가로, вертикала_позиција))

    def клик_вриједност(가로, вертикала_позиција): 가리키기(가로, вертикала_позиција, 1); 가리키기(가로, вертикала_позиција, 0)

    def растерска_слика_слика():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 стваран_подаци 너비를 쓴다.
        удаљен_вриједност.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        цртеж_вриједност = Image.new('RGB', (너비, 높이)); област_вриједност_9285603e = 0
        while True:
            종류 = 정확한값(удаљен_вриједност, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                дужина_вриједност = struct.unpack('>I', 정확한값(удаљен_вриједност, 7)[3:])[0]; 정확한값(удаљен_вриједност, дужина_вриједност); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(удаљен_вриједност, 3)[1:])[0]
            for _ in range(개수):
                가로, вертикала_позиција, 폭, дужина_вриједност, кодирање_вриједност = struct.unpack('>HHHHi', 정확한값(удаљен_вриједност, 12))
                assert кодирање_вриједност == 0 and 가로+폭 <= 너비 and вертикала_позиција+дужина_вриједност <= 높이
                цртеж_вриједност.paste(Image.frombytes('RGB', (폭, дужина_вриједност), 정확한값(удаљен_вриједност, 폭*дужина_вриједност*4), 'raw', 'BGRX'), (가로, вертикала_позиција))
                област_вриједност_9285603e += 폭*дужина_вриједност
            if област_вриједност_9285603e:
                assert област_вриједност_9285603e == 너비*높이, област_вриједност_9285603e
                return цртеж_вриједност

    def чек_пиксел(координата_вриједност, 색):
        마감 = time.monotonic()+10
        while True:
            цртеж_вриједност = растерска_слика_слика()
            if цртеж_вриједност.getpixel(координата_вриједност) == 색: return цртеж_вриједност
            if time.monotonic() > 마감: raise AssertionError((координата_вриједност, цртеж_вриједност.getpixel(координата_вриједност), 색))

    def Отпрема_Фајлови(Назив, подаци): пренос_вриједност.storbinary('STOR '+Назив, io.BytesIO(подаци))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+подесити_величину_Текст+' RGB32').encode() in евиденција_ред
        print('BOOT:', подесити_величину_Текст, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', евиденција_ред).group(1))
        удаљен_вриједност = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(удаљен_вриједност, 12) == b'RFB 003.008\n'; удаљен_вриједност.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(удаљен_вриједност, 정확한값(удаљен_вриједност, 1)[0]); удаљен_вриједност.sendall(b'\x01')
        assert 정확한값(удаљен_вриједност, 4) == b'\0'*4; удаљен_вриједност.sendall(b'\x01')
        초기 = 정확한값(удаљен_вриједност, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(удаљен_вриједност, struct.unpack('>I', 초기[20:])[0])
        удаљен_вриједност.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        удаљен_вриједност.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        чек_пиксел((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        чек_пиксел((너비-568, 높이-360), (32, 80, 144))
        Покрени = len(евиденција_ред); клик_вриједност(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Покрени)
        чек_пиксел((너비-568, 높이-360), (24, 32, 48))
        Покрени = len(евиденција_ред); клик_вриједност(80, 16); 기다리기(b'TERMINAL FOCUS 1', Покрени)
        љуска('ftpd start')
        пренос_вриједност = ftplib.FTP(); пренос_вриједност.encoding = 'utf-8'; пренос_вриједност.connect('127.0.0.1', број_порта, timeout=20); пренос_вриједност.login()
        # C 경계 검사는 32비트 unsigned 음수 конвертовати_вриједност·клип 밖·빈 사각형을 포함한다.
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
    писати_фајл_подаци(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Отпрема_Фајлови('화면시험.c', ИЗВОР.encode())
        assert 'exit 0' in љуска('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', послати_СМС_поруку('run /화면시험\n'))
        чек_пиксел((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', послати_СМС_поруку('q'))
        ИЗВОР = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, Излаз, систем_грешка
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except систем_грешка as ГРЕШКА:
    assert ГРЕШКА.индекс == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Излаз("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Отпрема_Фајлови('화면시험.py', ИЗВОР.encode())
        기다리기(b'PYTHON RESOLUTION PASS', послати_СМС_поруку('python /화면시험.py\n'))
        чек_пиксел((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', послати_СМС_поруку('q'))
        ИЗВОР = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] Аргументи) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new стање_изузетак("Величина");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new стање_изузетак("клип"); }
        catch (неважеће_аргумент_изузетак ГРЕШКА) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # изузетак 처리는 хост javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = мера_пут/'해상도경계시험.java'
        경계원문.write_text(ИЗВОР.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(пројектовати_корен/'dist/jkoros-native-korean.jar'), '-d', str(мера_пут), str(경계원문)])
        Отпрема_Фајлови('해상도경계시험.class', (мера_пут/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', послати_СМС_поруку('java 해상도경계시험\n'))
        чек_пиксел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', послати_СМС_поруку('q'))
        # 게스트 javac의 Подршка_вриједност 문법으로 Величина упит_вриједност·지우기·다섯 Аргументи 그리기를 컴파일한다.
        ИЗВОР = '''public class 해상도시험 {
    public static void main(String[] Аргументи) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.Излаз.писати_редак("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Отпрема_Фајлови('해상도시험.java', ИЗВОР.encode())
        ИСХОД = љуска('javac 해상도시험.java'); assert 'exit 0' in ИСХОД, ИСХОД
        기다리기(b'JAVA RESOLUTION PASS', послати_СМС_поруку('java 해상도시험\n'))
        чек_пиксел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', послати_СМС_поруку('q'))
        Отпрема_Фајлови('스윙시험.class', (мера_пут/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', послати_СМС_поруку('java 스윙시험\n'))
        가로, вертикала_позиција = (너비-400)//2, (높이-280)//2
        цртеж_вриједност = чек_пиксел((가로, вертикала_позиција), (32, 80, 144))
        цртеж_вриједност.save(str(мера_пут/(подесити_величину_Текст+'.png')))
        Покрени = len(евиденција_ред); клик_вриједност(가로+80, вертикала_позиција+155)
        기다리기('SWING CLICK Назив'.encode(), Покрени)
        Покрени = len(евиденција_ред); клик_вриједност(가로+385, вертикала_позиција+15); 기다리기(b'jkoros-native> ', Покрени)
        assert 'AFTER_RESOLUTION' in љуска('echo AFTER_RESOLUTION')
        print('PASS:', подесити_величину_Текст, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if пренос_вриједност: пренос_вриједност.close()
        if удаљен_вриједност: удаљен_вриједност.close()
        if Процес_вриједност.poll() is None:
            Процес_вриједност.terminate()
            try: Процес_вриједност.wait(timeout=8)
            except subprocess.TimeoutExpired: Процес_вриједност.kill(); Процес_вриједност.wait()
        бирач_a916db4e.close(); Процес_вриједност.stdout.close()
        (мера_пут/(подесити_величину_Текст+'.log')).write_bytes(евиденција_ред)


def Покрени():
    мера_пут = пројектовати_корен/'build/verification/resolution'; мера_пут.mkdir(parents=True, exist_ok=True)
    евиденција_ред = {'passed': False, 'kernel_sha256': hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for неважеће_вриједност in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ИСХОД = subprocess.run(['python3', str(пројектовати_корен/'Алатке/Изврши_команда.py'), '--resolution', неважеће_вриједност], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ИСХОД.returncode == 2 and b'--resolution' in ИСХОД.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(мера_пут), str(пројектовати_корен/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, мера_пут); евиденција_ред['resolutions'].append([너비, 높이])
        евиденција_ред.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (мера_пут/'report.json').write_text(json.dumps(евиденција_ред, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Покрени()
