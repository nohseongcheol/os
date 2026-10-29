#!/usr/bin/env python3
"""бодит_өгөгдөл QEMU/VNC에서 화면 Хэмжээ·경계·цонх зөөх_утга·Swing·언어별 그리기를 검사한다."""
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
from дэлгэц_харах import 정확한값
from Гүйцэтгэх_команд import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    хэмжээ_Бичвэр = '{}x{}'.format(너비, 높이)
    үйл_явц_утга = subprocess.Popen(['python3', str(기준/'Хэрэгслүүд/Гүйцэтгэх_команд.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', хэмжээ_Бичвэр], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    сонгогч_a916db4e = selectors.DefaultSelector(); сонгогч_a916db4e.register(үйл_явц_утга.stdout, selectors.EVENT_READ)
    бичих_мөр_6e8b375a = bytearray(); алсын_утга = None; дамжуулах_утга = None

    def 기다리기(үзүүлэх_утга, Ажиллуулах=0):
        마감 = time.monotonic() + 60
        while үзүүлэх_утга not in бичих_мөр_6e8b375a[Ажиллуулах:]:
            if time.monotonic() > 마감 or үйл_явц_утга.poll() is not None or b'HALTED' in бичих_мөр_6e8b375a or b'PANIC:' in бичих_мөр_6e8b375a:
                raise AssertionError(бичих_мөр_6e8b375a[Ажиллуулах:].decode('utf-8', 'replace'))
            for үйлдэл, _ in сонгогч_a916db4e.select(.1):
                өгөгдөл = үйлдэл.fileobj.read(65536)
                if өгөгдөл: бичих_мөр_6e8b375a.extend(өгөгдөл)
        return бичих_мөр_6e8b375a[Ажиллуулах:].decode('utf-8', 'replace')

    def товших_товч(тэмдэг, 눌림=True): алсын_утга.sendall(struct.pack('>BBHI', 4, int(눌림), 0, тэмдэг))

    def SMS_илгээх(Бичвэр):
        Ажиллуулах = len(бичих_мөр_6e8b375a)
        for тэмдэгт_утга in Бичвэр:
            тэмдэг = 0xff0d if тэмдэгт_утга == '\n' else ord(тэмдэгт_утга) if ord(тэмдэгт_утга) < 256 else 0x1000000 | ord(тэмдэгт_утга)
            товших_товч(тэмдэг); товших_товч(тэмдэг, False)
        return Ажиллуулах

    def бүрхүүл(Бичвэр): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_илгээх(Бичвэр+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): алсын_утга.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def товших_утга(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def цэглэвэр_зураг_зураг():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 бодит_өгөгдөл 너비를 쓴다.
        алсын_утга.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        зураг_утга_c143fe9e = Image.new('RGB', (너비, 높이)); газар_утга = 0
        while True:
            종류 = 정확한값(алсын_утга, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                урт_утга = struct.unpack('>I', 정확한값(алсын_утга, 7)[3:])[0]; 정확한값(алсын_утга, урт_утга); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(алсын_утга, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, урт_утга, кодчлол_утга = struct.unpack('>HHHHi', 정확한값(алсын_утга, 12))
                assert кодчлол_утга == 0 and 가로+폭 <= 너비 and 세로+урт_утга <= 높이
                зураг_утга_c143fe9e.paste(Image.frombytes('RGB', (폭, урт_утга), 정확한값(алсын_утга, 폭*урт_утга*4), 'raw', 'BGRX'), (가로, 세로))
                газар_утга += 폭*урт_утга
            if газар_утга:
                assert газар_утга == 너비*높이, газар_утга
                return зураг_утга_c143fe9e

    def чек_нягтрал_186c1328(координат_утга, 색):
        마감 = time.monotonic()+10
        while True:
            зураг_утга_c143fe9e = цэглэвэр_зураг_зураг()
            if зураг_утга_c143fe9e.getpixel(координат_утга) == 색: return зураг_утга_c143fe9e
            if time.monotonic() > 마감: raise AssertionError((координат_утга, зураг_утга_c143fe9e.getpixel(координат_утга), 색))

    def байршуулах_Файлууд(Нэр, өгөгдөл): дамжуулах_утга.storbinary('STOR '+Нэр, io.BytesIO(өгөгдөл))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+хэмжээ_Бичвэр+' RGB32').encode() in бичих_мөр_6e8b375a
        print('BOOT:', хэмжээ_Бичвэр, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', бичих_мөр_6e8b375a).group(1))
        алсын_утга = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(алсын_утга, 12) == b'RFB 003.008\n'; алсын_утга.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(алсын_утга, 정확한값(алсын_утга, 1)[0]); алсын_утга.sendall(b'\x01')
        assert 정확한값(алсын_утга, 4) == b'\0'*4; алсын_утга.sendall(b'\x01')
        초기 = 정확한값(алсын_утга, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(алсын_утга, struct.unpack('>I', 초기[20:])[0])
        алсын_утга.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        алсын_утга.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        чек_нягтрал_186c1328((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        чек_нягтрал_186c1328((너비-568, 높이-360), (32, 80, 144))
        Ажиллуулах = len(бичих_мөр_6e8b375a); товших_утга(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Ажиллуулах)
        чек_нягтрал_186c1328((너비-568, 높이-360), (24, 32, 48))
        Ажиллуулах = len(бичих_мөр_6e8b375a); товших_утга(80, 16); 기다리기(b'TERMINAL FOCUS 1', Ажиллуулах)
        бүрхүүл('ftpd start')
        дамжуулах_утга = ftplib.FTP(); дамжуулах_утга.encoding = 'utf-8'; дамжуулах_утга.connect('127.0.0.1', 접속번호, timeout=20); дамжуулах_утга.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·клип 밖·빈 사각형을 포함한다.
        ЭХ = '''#include <화면규약.h>
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
    бичих_файл_өгөгдөл(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        байршуулах_Файлууд('화면시험.c', ЭХ.encode())
        assert 'exit 0' in бүрхүүл('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_илгээх('run /화면시험\n'))
        чек_нягтрал_186c1328((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_илгээх('q'))
        ЭХ = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, систем_алдаа
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except систем_алдаа as Алдаа:
    assert Алдаа.индекс == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        байршуулах_Файлууд('화면시험.py', ЭХ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_илгээх('python /화면시험.py\n'))
        чек_нягтрал_186c1328((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_илгээх('q'))
        ЭХ = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("Хэмжээ");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("клип"); }
        catch (잘못된인수예외 Алдаа) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 хост javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(ЭХ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        байршуулах_Файлууд('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_илгээх('java 해상도경계시험\n'))
        чек_нягтрал_186c1328((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_илгээх('q'))
        # 게스트 javac의 тусламж_утга 문법으로 Хэмжээ асуулга_утга·지우기·다섯 인수 그리기를 컴파일한다.
        ЭХ = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.бичих_мөр("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        байршуулах_Файлууд('해상도시험.java', ЭХ.encode())
        결과 = бүрхүүл('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', SMS_илгээх('java 해상도시험\n'))
        чек_нягтрал_186c1328((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_илгээх('q'))
        байршуулах_Файлууд('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_илгээх('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        зураг_утга_c143fe9e = чек_нягтрал_186c1328((가로, 세로), (32, 80, 144))
        зураг_утга_c143fe9e.save(str(결과경로/(хэмжээ_Бичвэр+'.png')))
        Ажиллуулах = len(бичих_мөр_6e8b375a); товших_утга(가로+80, 세로+155)
        기다리기('SWING CLICK Нэр'.encode(), Ажиллуулах)
        Ажиллуулах = len(бичих_мөр_6e8b375a); товших_утга(가로+385, 세로+15); 기다리기(b'jkoros-native> ', Ажиллуулах)
        assert 'AFTER_RESOLUTION' in бүрхүүл('echo AFTER_RESOLUTION')
        print('PASS:', хэмжээ_Бичвэр, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if дамжуулах_утга: дамжуулах_утга.close()
        if алсын_утга: алсын_утга.close()
        if үйл_явц_утга.poll() is None:
            үйл_явц_утга.terminate()
            try: үйл_явц_утга.wait(timeout=8)
            except subprocess.TimeoutExpired: үйл_явц_утга.kill(); үйл_явц_утга.wait()
        сонгогч_a916db4e.close(); үйл_явц_утга.stdout.close()
        (결과경로/(хэмжээ_Бичвэр+'.log')).write_bytes(бичих_мөр_6e8b375a)


def Ажиллуулах():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    бичих_мөр_6e8b375a = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for буруу_утга in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Хэрэгслүүд/Гүйцэтгэх_команд.py'), '--resolution', буруу_утга], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); бичих_мөр_6e8b375a['resolutions'].append([너비, 높이])
        бичих_мөр_6e8b375a.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(бичих_мөр_6e8b375a, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Ажиллуулах()
