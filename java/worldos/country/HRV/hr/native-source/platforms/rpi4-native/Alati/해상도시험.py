#!/usr/bin/env python3
"""stvaran_podaci QEMU/VNC에서 화면 Veličina·경계·Prozor pomicati_se_VALUE·Swing·언어별 그리기를 검사한다."""
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
from stolni_Prikaz import EXACT_VALUE
from Izvrši_naredba import akcija_korijen


def 해상도시험(너비, 높이, KR_put):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); broj_priključka = 임시.getsockname()[1]
    promijeniti_veličinu_SMS = '{}x{}'.format(너비, 높이)
    Proces_VALUE = subprocess.Popen(['python3', str(akcija_korijen/'Alati/Izvrši_naredba.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(broj_priključka), '--resolution', promijeniti_veličinu_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    odabirač_a916db4e = selectors.DefaultSelector(); odabirač_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_zapis = bytearray(); udaljeno_VALUE = None; Prijenos_VALUE = None

    def 기다리기(emisija_VALUE, Pokreni=0):
        rok_za_dovršetak_VALUE = time.monotonic() + 60
        while emisija_VALUE not in LOG_zapis[Pokreni:]:
            if time.monotonic() > rok_za_dovršetak_VALUE or Proces_VALUE.poll() is not None or b'HALTED' in LOG_zapis or b'PANIC:' in LOG_zapis:
                raise AssertionError(LOG_zapis[Pokreni:].decode('utf-8', 'replace'))
            for Događaj, _ in odabirač_a916db4e.select(.1):
                podaci = Događaj.fileobj.read(65536)
                if podaci: LOG_zapis.extend(podaci)
        return LOG_zapis[Pokreni:].decode('utf-8', 'replace')

    def klik_tipka(simbol, 눌림=True): udaljeno_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def slanje_SMS_a(Tekst):
        Pokreni = len(LOG_zapis)
        for znak_VALUE in Tekst:
            simbol = 0xff0d if znak_VALUE == '\n' else ord(znak_VALUE) if ord(znak_VALUE) < 256 else 0x1000000 | ord(znak_VALUE)
            klik_tipka(simbol); klik_tipka(simbol, False)
        return Pokreni

    def ljuska(Tekst): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', slanje_SMS_a(Tekst+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Okomito_položaj, 눌림): udaljeno_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Okomito_položaj))

    def klik_VALUE(가로, Okomito_položaj): 가리키기(가로, Okomito_položaj, 1); 가리키기(가로, Okomito_položaj, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 stvaran_podaci 너비를 쓴다.
        udaljeno_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        crtež_VALUE = Image.new('RGB', (너비, 높이)); područje_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(udaljeno_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(udaljeno_VALUE, 7)[3:])[0]; EXACT_VALUE(udaljeno_VALUE, 길이); continue
            assert 종류 == 0, 종류
            artikl_COUNT = struct.unpack('>H', EXACT_VALUE(udaljeno_VALUE, 3)[1:])[0]
            for _ in range(artikl_COUNT):
                가로, Okomito_položaj, 폭, 길이, šifriranje_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(udaljeno_VALUE, 12))
                assert šifriranje_VALUE == 0 and 가로+폭 <= 너비 and Okomito_položaj+길이 <= 높이
                crtež_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(udaljeno_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, Okomito_položaj))
                područje_VALUE_9285603e += 폭*길이
            if područje_VALUE_9285603e:
                assert područje_VALUE_9285603e == 너비*높이, područje_VALUE_9285603e
                return crtež_VALUE

    def 화소확인(좌표, 색):
        rok_za_dovršetak_VALUE = time.monotonic()+10
        while True:
            crtež_VALUE = bitmap_IMAGE()
            if crtež_VALUE.getpixel(좌표) == 색: return crtež_VALUE
            if time.monotonic() > rok_za_dovršetak_VALUE: raise AssertionError((좌표, crtež_VALUE.getpixel(좌표), 색))

    def Prijenos_Datoteke(Ime, podaci): Prijenos_VALUE.storbinary('STOR '+Ime, io.BytesIO(podaci))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+promijeniti_veličinu_SMS+' RGB32').encode() in LOG_zapis
        print('BOOT:', promijeniti_veličinu_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_zapis).group(1))
        udaljeno_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(udaljeno_VALUE, 12) == b'RFB 003.008\n'; udaljeno_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(udaljeno_VALUE, EXACT_VALUE(udaljeno_VALUE, 1)[0]); udaljeno_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(udaljeno_VALUE, 4) == b'\0'*4; udaljeno_VALUE.sendall(b'\x01')
        početno_stanje = EXACT_VALUE(udaljeno_VALUE, 24); assert struct.unpack('>HH', početno_stanje[:4]) == (너비, 높이)
        EXACT_VALUE(udaljeno_VALUE, struct.unpack('>I', početno_stanje[20:])[0])
        udaljeno_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        udaljeno_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        화소확인((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        화소확인((너비-568, 높이-360), (32, 80, 144))
        Pokreni = len(LOG_zapis); klik_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Pokreni)
        화소확인((너비-568, 높이-360), (24, 32, 48))
        Pokreni = len(LOG_zapis); klik_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Pokreni)
        ljuska('ftpd start')
        Prijenos_VALUE = ftplib.FTP(); Prijenos_VALUE.encoding = 'utf-8'; Prijenos_VALUE.connect('127.0.0.1', broj_priključka, timeout=20); Prijenos_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·isječak 밖·빈 사각형을 포함한다.
        IZVOR = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(Crtanje_pravokutnik(너비,높이,0,0,0)) return 2;
    if(Crtanje_pravokutnik(너비,높이-1,1,1,0)!=-22) return 3;
    if(Crtanje_pravokutnik(너비-1,높이,1,1,0)!=-22) return 4;
    if(Crtanje_pravokutnik(-1,0,1,1,0)!=-22) return 5;
    if(Crtanje_pravokutnik(0,0,-1,1,0)!=-22) return 6;
    if(Crtanje_pravokutnik(너비-1,높이-1,1,1,0x332211)) return 7;
    zapisivanje_Datoteka_podaci(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Prijenos_Datoteke('화면시험.c', IZVOR.encode())
        assert 'exit 0' in ljuska('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', slanje_SMS_a('run /화면시험\n'))
        화소확인((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', slanje_SMS_a('q'))
        IZVOR = '''from hrvatski import 화면크기, Crtanje_pravokutnik, 그림기다리기, Izlaz, sustav_pogreška
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    Crtanje_pravokutnik(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sustav_pogreška as GREŠKA:
    assert GREŠKA.INDEX == 22
Crtanje_pravokutnik(너비-1, 높이-1, 1, 1, 0x665544)
Izlaz("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Prijenos_Datoteke('화면시험.py', IZVOR.encode())
        기다리기(b'PYTHON RESOLUTION PASS', slanje_SMS_a('python /화면시험.py\n'))
        화소확인((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', slanje_SMS_a('q'))
        IZVOR = '''import hrvatski.vlastiti.*;
public class 해상도시험 {
    public static void main(String[] Argumenti) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Stanje_iznimka("Veličina");
        try { 화면.pravokutnik(너비,높이-1,1,1,0); throw new Stanje_iznimka("isječak"); }
        catch (nevaljan_argument_iznimka GREŠKA) { }
        화면.izbrisati_unos(0x302018);
        화면.pravokutnik(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # iznimka 처리는 domaćin javac 결과를 vlastiti JVM에 올려 검사한다.
        경계원문 = KR_put/'해상도경계시험.java'
        경계원문.write_text(IZVOR.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(akcija_korijen/'dist/jkoros-native-korean.jar'), '-d', str(KR_put), str(경계원문)])
        Prijenos_Datoteke('해상도경계시험.class', (KR_put/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', slanje_SMS_a('java 해상도경계시험\n'))
        화소확인((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', slanje_SMS_a('q'))
        # 게스트 javac의 Podrška_VALUE 문법으로 Veličina upit_VALUE·izbrisati_unos·다섯 Argumenti 그리기를 컴파일한다.
        IZVOR = '''public class 해상도시험 {
    public static void main(String[] Argumenti) {
        int 너비=hrvatski.vlastiti.화면.너비();
        int 높이=hrvatski.vlastiti.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        hrvatski.vlastiti.화면.izbrisati_unos(3153944);
        hrvatski.vlastiti.화면.pravokutnik(너비-1,높이-1,1,1,10061943);
        hrvatski.vlastiti.Izlaz.zapisivanje_red("JAVA RESOLUTION PASS");
        hrvatski.vlastiti.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Prijenos_Datoteke('해상도시험.java', IZVOR.encode())
        REZULTAT = ljuska('javac 해상도시험.java'); assert 'exit 0' in REZULTAT, REZULTAT
        기다리기(b'JAVA RESOLUTION PASS', slanje_SMS_a('java 해상도시험\n'))
        화소확인((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', slanje_SMS_a('q'))
        Prijenos_Datoteke('스윙시험.class', (KR_put/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', slanje_SMS_a('java 스윙시험\n'))
        가로, Okomito_položaj = (너비-400)//2, (높이-280)//2
        crtež_VALUE = 화소확인((가로, Okomito_položaj), (32, 80, 144))
        crtež_VALUE.save(str(KR_put/(promijeniti_veličinu_SMS+'.png')))
        Pokreni = len(LOG_zapis); klik_VALUE(가로+80, Okomito_položaj+155)
        기다리기('SWING CLICK Ime'.encode(), Pokreni)
        Pokreni = len(LOG_zapis); klik_VALUE(가로+385, Okomito_položaj+15); 기다리기(b'jkoros-native> ', Pokreni)
        assert 'AFTER_RESOLUTION' in ljuska('echo AFTER_RESOLUTION')
        print('PASS:', promijeniti_veličinu_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Prijenos_VALUE: Prijenos_VALUE.close()
        if udaljeno_VALUE: udaljeno_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces_VALUE.kill(); Proces_VALUE.wait()
        odabirač_a916db4e.close(); Proces_VALUE.stdout.close()
        (KR_put/(promijeniti_veličinu_SMS+'.log')).write_bytes(LOG_zapis)


def Pokreni():
    KR_put = akcija_korijen/'build/verification/resolution'; KR_put.mkdir(parents=True, exist_ok=True)
    LOG_zapis = {'passed': False, 'kernel_sha256': hashlib.sha256((akcija_korijen/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for nevaljan_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            REZULTAT = subprocess.run(['python3', str(akcija_korijen/'Alati/Izvrši_naredba.py'), '--resolution', nevaljan_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert REZULTAT.returncode == 2 and b'--resolution' in REZULTAT.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_put), str(akcija_korijen/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, KR_put); LOG_zapis['resolutions'].append([너비, 높이])
        LOG_zapis.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_put/'report.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Pokreni()
