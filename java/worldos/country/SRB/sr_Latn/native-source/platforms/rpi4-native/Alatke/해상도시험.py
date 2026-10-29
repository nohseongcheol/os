#!/usr/bin/env python3
"""stvarni_podaci QEMU/VNC에서 화면 promeniti_veličinu·경계·prozor premestiti_VALUE·Swing·언어별 그리기를 검사한다."""
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
from desktop_Prikaz import EXACT_VALUE
from Izvrši_komanda import radnja_koren


def 해상도시험(너비, 높이, KR_putanja):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); broj_porta = 임시.getsockname()[1]
    promeniti_veličinu_SMS = '{}x{}'.format(너비, 높이)
    Proces_VALUE = subprocess.Popen(['python3', str(radnja_koren/'Alatke/Izvrši_komanda.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(broj_porta), '--resolution', promeniti_veličinu_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    birač_a916db4e = selectors.DefaultSelector(); birač_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_snimi = bytearray(); udaljen_VALUE = None; prenos_VALUE = None

    def 기다리기(emisija_VALUE, koristiti=0):
        krajnji_rok_VALUE = time.monotonic() + 60
        while emisija_VALUE not in LOG_snimi[koristiti:]:
            if time.monotonic() > krajnji_rok_VALUE or Proces_VALUE.poll() is not None or b'HALTED' in LOG_snimi or b'PANIC:' in LOG_snimi:
                raise AssertionError(LOG_snimi[koristiti:].decode('utf-8', 'replace'))
            for događaj, _ in birač_a916db4e.select(.1):
                podaci = događaj.fileobj.read(65536)
                if podaci: LOG_snimi.extend(podaci)
        return LOG_snimi[koristiti:].decode('utf-8', 'replace')

    def klik_taster(simbol, 눌림=True): udaljen_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def poslati_SMS_poruku(SMS):
        koristiti = len(LOG_snimi)
        for znak_VALUE in SMS:
            simbol = 0xff0d if znak_VALUE == '\n' else ord(znak_VALUE) if ord(znak_VALUE) < 256 else 0x1000000 | ord(znak_VALUE)
            klik_taster(simbol); klik_taster(simbol, False)
        return koristiti

    def ljuska(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', poslati_SMS_poruku(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, vertikala_pozicija, 눌림): udaljen_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikala_pozicija))

    def klik_VALUE(가로, vertikala_pozicija): 가리키기(가로, vertikala_pozicija, 1); 가리키기(가로, vertikala_pozicija, 0)

    def raster_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 stvarni_podaci 너비를 쓴다.
        udaljen_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        crtež_VALUE = Image.new('RGB', (너비, 높이)); oblast_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(udaljen_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(udaljen_VALUE, 7)[3:])[0]; EXACT_VALUE(udaljen_VALUE, 길이); continue
            assert 종류 == 0, 종류
            stavka_COUNT = struct.unpack('>H', EXACT_VALUE(udaljen_VALUE, 3)[1:])[0]
            for _ in range(stavka_COUNT):
                가로, vertikala_pozicija, 폭, 길이, kodiranje_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(udaljen_VALUE, 12))
                assert kodiranje_VALUE == 0 and 가로+폭 <= 너비 and vertikala_pozicija+길이 <= 높이
                crtež_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(udaljen_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, vertikala_pozicija))
                oblast_VALUE_9285603e += 폭*길이
            if oblast_VALUE_9285603e:
                assert oblast_VALUE_9285603e == 너비*높이, oblast_VALUE_9285603e
                return crtež_VALUE

    def proveriti_piksel(좌표, 색):
        krajnji_rok_VALUE = time.monotonic()+10
        while True:
            crtež_VALUE = raster_IMAGE()
            if crtež_VALUE.getpixel(좌표) == 색: return crtež_VALUE
            if time.monotonic() > krajnji_rok_VALUE: raise AssertionError((좌표, crtež_VALUE.getpixel(좌표), 색))

    def Otprema_Datoteke(ime, podaci): prenos_VALUE.storbinary('STOR '+ime, io.BytesIO(podaci))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+promeniti_veličinu_SMS+' RGB32').encode() in LOG_snimi
        print('BOOT:', promeniti_veličinu_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_snimi).group(1))
        udaljen_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(udaljen_VALUE, 12) == b'RFB 003.008\n'; udaljen_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(udaljen_VALUE, EXACT_VALUE(udaljen_VALUE, 1)[0]); udaljen_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(udaljen_VALUE, 4) == b'\0'*4; udaljen_VALUE.sendall(b'\x01')
        početno_stanje = EXACT_VALUE(udaljen_VALUE, 24); assert struct.unpack('>HH', početno_stanje[:4]) == (너비, 높이)
        EXACT_VALUE(udaljen_VALUE, struct.unpack('>I', početno_stanje[20:])[0])
        udaljen_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        udaljen_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        proveriti_piksel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        proveriti_piksel((너비-568, 높이-360), (32, 80, 144))
        koristiti = len(LOG_snimi); klik_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', koristiti)
        proveriti_piksel((너비-568, 높이-360), (24, 32, 48))
        koristiti = len(LOG_snimi); klik_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', koristiti)
        ljuska('ftpd start')
        prenos_VALUE = ftplib.FTP(); prenos_VALUE.encoding = 'utf-8'; prenos_VALUE.connect('127.0.0.1', broj_porta, timeout=20); prenos_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·klip 밖·빈 사각형을 포함한다.
        izvor = '''#include <화면규약.h>
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
    파일자료쓰기(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Otprema_Datoteke('화면시험.c', izvor.encode())
        assert 'exit 0' in ljuska('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', poslati_SMS_poruku('run /화면시험\n'))
        proveriti_piksel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', poslati_SMS_poruku('q'))
        izvor = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, sistem_greška
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistem_greška as greška:
    assert greška.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Otprema_Datoteke('화면시험.py', izvor.encode())
        기다리기(b'PYTHON RESOLUTION PASS', poslati_SMS_poruku('python /화면시험.py\n'))
        proveriti_piksel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', poslati_SMS_poruku('q'))
        izvor = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Status_izuzetak("promeniti_veličinu");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new Status_izuzetak("klip"); }
        catch (nevažeći_argument_izuzetak greška) { }
        화면.obrisati_stavka(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # izuzetak 처리는 host javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = KR_putanja/'해상도경계시험.java'
        경계원문.write_text(izvor.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(radnja_koren/'dist/jkoros-native-korean.jar'), '-d', str(KR_putanja), str(경계원문)])
        Otprema_Datoteke('해상도경계시험.class', (KR_putanja/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', poslati_SMS_poruku('java 해상도경계시험\n'))
        proveriti_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', poslati_SMS_poruku('q'))
        # 게스트 javac의 Podrška_VALUE 문법으로 promeniti_veličinu upit_VALUE·obrisati_stavka·다섯 인수 그리기를 컴파일한다.
        izvor = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.obrisati_stavka(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.줄쓰기("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Otprema_Datoteke('해상도시험.java', izvor.encode())
        KR = ljuska('javac 해상도시험.java'); assert 'exit 0' in KR, KR
        기다리기(b'JAVA RESOLUTION PASS', poslati_SMS_poruku('java 해상도시험\n'))
        proveriti_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', poslati_SMS_poruku('q'))
        Otprema_Datoteke('스윙시험.class', (KR_putanja/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', poslati_SMS_poruku('java 스윙시험\n'))
        가로, vertikala_pozicija = (너비-400)//2, (높이-280)//2
        crtež_VALUE = proveriti_piksel((가로, vertikala_pozicija), (32, 80, 144))
        crtež_VALUE.save(str(KR_putanja/(promeniti_veličinu_SMS+'.png')))
        koristiti = len(LOG_snimi); klik_VALUE(가로+80, vertikala_pozicija+155)
        기다리기('SWING CLICK ime'.encode(), koristiti)
        koristiti = len(LOG_snimi); klik_VALUE(가로+385, vertikala_pozicija+15); 기다리기(b'jkoros-native> ', koristiti)
        assert 'AFTER_RESOLUTION' in ljuska('echo AFTER_RESOLUTION')
        print('PASS:', promeniti_veličinu_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if prenos_VALUE: prenos_VALUE.close()
        if udaljen_VALUE: udaljen_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces_VALUE.kill(); Proces_VALUE.wait()
        birač_a916db4e.close(); Proces_VALUE.stdout.close()
        (KR_putanja/(promeniti_veličinu_SMS+'.log')).write_bytes(LOG_snimi)


def koristiti():
    KR_putanja = radnja_koren/'build/verification/resolution'; KR_putanja.mkdir(parents=True, exist_ok=True)
    LOG_snimi = {'passed': False, 'kernel_sha256': hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for nevažeći_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            KR = subprocess.run(['python3', str(radnja_koren/'Alatke/Izvrši_komanda.py'), '--resolution', nevažeći_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert KR.returncode == 2 and b'--resolution' in KR.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_putanja), str(radnja_koren/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, KR_putanja); LOG_snimi['resolutions'].append([너비, 높이])
        LOG_snimi.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_putanja/'report.json').write_text(json.dumps(LOG_snimi, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': koristiti()
