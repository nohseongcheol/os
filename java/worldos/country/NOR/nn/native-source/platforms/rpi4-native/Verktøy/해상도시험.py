#!/usr/bin/env python3
"""faktisk_data QEMU/VNC에서 화면 Storleik·경계·vindauge flytte_VALUE·Swing·언어별 그리기를 검사한다."""
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
from stasjonær_vise import EXACT_VALUE
from Utfør_kommando import spegle_rot


def 해상도시험(너비, 높이, forretningsmål_bane):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); portnummer = 임시.getsockname()[1]
    endre_storleik_SMS = '{}x{}'.format(너비, 높이)
    Prosess_VALUE = subprocess.Popen(['python3', str(spegle_rot/'Verktøy/Utfør_kommando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portnummer), '--resolution', endre_storleik_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    veljar_a916db4e = selectors.DefaultSelector(); veljar_a916db4e.register(Prosess_VALUE.stdout, selectors.EVENT_READ)
    LOG_rad = bytearray(); fjern_VALUE = None; Overfør_VALUE = None

    def 기다리기(vise_VALUE_487749b8, Køyr_2=0):
        마감 = time.monotonic() + 60
        while vise_VALUE_487749b8 not in LOG_rad[Køyr_2:]:
            if time.monotonic() > 마감 or Prosess_VALUE.poll() is not None or b'HALTED' in LOG_rad or b'PANIC:' in LOG_rad:
                raise AssertionError(LOG_rad[Køyr_2:].decode('utf-8', 'replace'))
            for Hending, _ in veljar_a916db4e.select(.1):
                data = Hending.fileobj.read(65536)
                if data: LOG_rad.extend(data)
        return LOG_rad[Køyr_2:].decode('utf-8', 'replace')

    def klikk_knapp(symbol, 눌림=True): fjern_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def sende_SMS(Tekst):
        Køyr_2 = len(LOG_rad)
        for teikn_VALUE in Tekst:
            symbol = 0xff0d if teikn_VALUE == '\n' else ord(teikn_VALUE) if ord(teikn_VALUE) < 256 else 0x1000000 | ord(teikn_VALUE)
            klikk_knapp(symbol); klikk_knapp(symbol, False)
        return Køyr_2

    def grensesnitt(Tekst): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', sende_SMS(Tekst+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, vertikalvising_plassere, 눌림): fjern_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikalvising_plassere))

    def klikk_VALUE(가로, vertikalvising_plassere): 가리키기(가로, vertikalvising_plassere, 1); 가리키기(가로, vertikalvising_plassere, 0)

    def punktgrafikk_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 faktisk_data 너비를 쓴다.
        fjern_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        teikning_VALUE = Image.new('RGB', (너비, 높이)); felt_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(fjern_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                lengd_VALUE = struct.unpack('>I', EXACT_VALUE(fjern_VALUE, 7)[3:])[0]; EXACT_VALUE(fjern_VALUE, lengd_VALUE); continue
            assert 종류 == 0, 종류
            vare_COUNT = struct.unpack('>H', EXACT_VALUE(fjern_VALUE, 3)[1:])[0]
            for _ in range(vare_COUNT):
                가로, vertikalvising_plassere, 폭, lengd_VALUE, koding_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(fjern_VALUE, 12))
                assert koding_VALUE == 0 and 가로+폭 <= 너비 and vertikalvising_plassere+lengd_VALUE <= 높이
                teikning_VALUE.paste(Image.frombytes('RGB', (폭, lengd_VALUE), EXACT_VALUE(fjern_VALUE, 폭*lengd_VALUE*4), 'raw', 'BGRX'), (가로, vertikalvising_plassere))
                felt_VALUE_9285603e += 폭*lengd_VALUE
            if felt_VALUE_9285603e:
                assert felt_VALUE_9285603e == 너비*높이, felt_VALUE_9285603e
                return teikning_VALUE

    def sjekk_piksel(koordinat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            teikning_VALUE = punktgrafikk_IMAGE()
            if teikning_VALUE.getpixel(koordinat_VALUE) == 색: return teikning_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinat_VALUE, teikning_VALUE.getpixel(koordinat_VALUE), 색))

    def Upload_Filer(Namn, data): Overfør_VALUE.storbinary('STOR '+Namn, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+endre_storleik_SMS+' RGB32').encode() in LOG_rad
        print('BOOT:', endre_storleik_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_rad).group(1))
        fjern_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(fjern_VALUE, 12) == b'RFB 003.008\n'; fjern_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(fjern_VALUE, EXACT_VALUE(fjern_VALUE, 1)[0]); fjern_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(fjern_VALUE, 4) == b'\0'*4; fjern_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(fjern_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(fjern_VALUE, struct.unpack('>I', 초기[20:])[0])
        fjern_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        fjern_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        sjekk_piksel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        sjekk_piksel((너비-568, 높이-360), (32, 80, 144))
        Køyr_2 = len(LOG_rad); klikk_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Køyr_2)
        sjekk_piksel((너비-568, 높이-360), (24, 32, 48))
        Køyr_2 = len(LOG_rad); klikk_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Køyr_2)
        grensesnitt('ftpd start')
        Overfør_VALUE = ftplib.FTP(); Overfør_VALUE.encoding = 'utf-8'; Overfør_VALUE.connect('127.0.0.1', portnummer, timeout=20); Overfør_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·klipp 밖·빈 사각형을 포함한다.
        KJELDE = '''#include <화면규약.h>
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
    skrive_fil_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Filer('화면시험.c', KJELDE.encode())
        assert 'exit 0' in grensesnitt('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', sende_SMS('run /화면시험\n'))
        sjekk_piksel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', sende_SMS('q'))
        KJELDE = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, Utdata, system_feil
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except system_feil as FEIL:
    assert FEIL.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Utdata("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Filer('화면시험.py', KJELDE.encode())
        기다리기(b'PYTHON RESOLUTION PASS', sende_SMS('python /화면시험.py\n'))
        sjekk_piksel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', sende_SMS('q'))
        KJELDE = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] Argument) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new status_unntak("Storleik");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new status_unntak("klipp"); }
        catch (ugyldig_argument_unntak FEIL) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # unntak 처리는 vert javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = forretningsmål_bane/'해상도경계시험.java'
        경계원문.write_text(KJELDE.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(spegle_rot/'dist/jkoros-native-korean.jar'), '-d', str(forretningsmål_bane), str(경계원문)])
        Upload_Filer('해상도경계시험.class', (forretningsmål_bane/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', sende_SMS('java 해상도경계시험\n'))
        sjekk_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', sende_SMS('q'))
        # 게스트 javac의 støtte_VALUE 문법으로 Storleik spørjing_VALUE·지우기·다섯 Argument 그리기를 컴파일한다.
        KJELDE = '''public class 해상도시험 {
    public static void main(String[] Argument) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.Utdata.skrive_line("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Filer('해상도시험.java', KJELDE.encode())
        forretningsmål = grensesnitt('javac 해상도시험.java'); assert 'exit 0' in forretningsmål, forretningsmål
        기다리기(b'JAVA RESOLUTION PASS', sende_SMS('java 해상도시험\n'))
        sjekk_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', sende_SMS('q'))
        Upload_Filer('스윙시험.class', (forretningsmål_bane/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', sende_SMS('java 스윙시험\n'))
        가로, vertikalvising_plassere = (너비-400)//2, (높이-280)//2
        teikning_VALUE = sjekk_piksel((가로, vertikalvising_plassere), (32, 80, 144))
        teikning_VALUE.save(str(forretningsmål_bane/(endre_storleik_SMS+'.png')))
        Køyr_2 = len(LOG_rad); klikk_VALUE(가로+80, vertikalvising_plassere+155)
        기다리기('SWING CLICK Namn'.encode(), Køyr_2)
        Køyr_2 = len(LOG_rad); klikk_VALUE(가로+385, vertikalvising_plassere+15); 기다리기(b'jkoros-native> ', Køyr_2)
        assert 'AFTER_RESOLUTION' in grensesnitt('echo AFTER_RESOLUTION')
        print('PASS:', endre_storleik_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Overfør_VALUE: Overfør_VALUE.close()
        if fjern_VALUE: fjern_VALUE.close()
        if Prosess_VALUE.poll() is None:
            Prosess_VALUE.terminate()
            try: Prosess_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Prosess_VALUE.kill(); Prosess_VALUE.wait()
        veljar_a916db4e.close(); Prosess_VALUE.stdout.close()
        (forretningsmål_bane/(endre_storleik_SMS+'.log')).write_bytes(LOG_rad)


def Køyr_2():
    forretningsmål_bane = spegle_rot/'build/verification/resolution'; forretningsmål_bane.mkdir(parents=True, exist_ok=True)
    LOG_rad = {'passed': False, 'kernel_sha256': hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ugyldig_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            forretningsmål = subprocess.run(['python3', str(spegle_rot/'Verktøy/Utfør_kommando.py'), '--resolution', ugyldig_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert forretningsmål.returncode == 2 and b'--resolution' in forretningsmål.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(forretningsmål_bane), str(spegle_rot/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, forretningsmål_bane); LOG_rad['resolutions'].append([너비, 높이])
        LOG_rad.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (forretningsmål_bane/'report.json').write_text(json.dumps(LOG_rad, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Køyr_2()
