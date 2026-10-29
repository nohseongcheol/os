#!/usr/bin/env python3
"""dejanski_podatki QEMU/VNC에서 화면 Velikost·경계·okno premikati_VALUE·Swing·언어별 그리기를 검사한다."""
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
from namizje_Pogled import EXACT_VALUE
from Izvedi_ukaz import pobuda_koren


def ločljivost_preskusiti(너비, višina_VALUE, KR_pot):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); številka_vrat = 임시.getsockname()[1]
    spremeniti_velikost_SMS = '{}x{}'.format(너비, višina_VALUE)
    Proces_VALUE = subprocess.Popen(['python3', str(pobuda_koren/'Orodja/Izvedi_ukaz.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(številka_vrat), '--resolution', spremeniti_velikost_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    izbirnik_a916db4e = selectors.DefaultSelector(); izbirnik_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_zapis = bytearray(); oddaljen_VALUE = None; Prenos_VALUE = None

    def 기다리기(oddaja_VALUE_487749b8, Zaženi=0):
        rok_VALUE = time.monotonic() + 60
        while oddaja_VALUE_487749b8 not in LOG_zapis[Zaženi:]:
            if time.monotonic() > rok_VALUE or Proces_VALUE.poll() is not None or b'HALTED' in LOG_zapis or b'PANIC:' in LOG_zapis:
                raise AssertionError(LOG_zapis[Zaženi:].decode('utf-8', 'replace'))
            for dogodek, _ in izbirnik_a916db4e.select(.1):
                podatki = dogodek.fileobj.read(65536)
                if podatki: LOG_zapis.extend(podatki)
        return LOG_zapis[Zaženi:].decode('utf-8', 'replace')

    def klik_gumb(simbol, 눌림=True): oddaljen_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def poslati_SMS(Besedilo):
        Zaženi = len(LOG_zapis)
        for znak_VALUE in Besedilo:
            simbol = 0xff0d if znak_VALUE == '\n' else ord(znak_VALUE) if ord(znak_VALUE) < 256 else 0x1000000 | ord(znak_VALUE)
            klik_gumb(simbol); klik_gumb(simbol, False)
        return Zaženi

    def lupina(Besedilo): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', poslati_SMS(Besedilo+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Navpično_položaj, 눌림): oddaljen_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Navpično_položaj))

    def klik_VALUE(가로, Navpično_položaj): 가리키기(가로, Navpično_položaj, 1); 가리키기(가로, Navpično_položaj, 0)

    def bitna_slika_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 dejanski_podatki 너비를 쓴다.
        oddaljen_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, višina_VALUE))
        risba_VALUE = Image.new('RGB', (너비, višina_VALUE)); območje_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(oddaljen_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(oddaljen_VALUE, 7)[3:])[0]; EXACT_VALUE(oddaljen_VALUE, 길이); continue
            assert 종류 == 0, 종류
            element_COUNT = struct.unpack('>H', EXACT_VALUE(oddaljen_VALUE, 3)[1:])[0]
            for _ in range(element_COUNT):
                가로, Navpično_položaj, 폭, 길이, kodiranje_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(oddaljen_VALUE, 12))
                assert kodiranje_VALUE == 0 and 가로+폭 <= 너비 and Navpično_položaj+길이 <= višina_VALUE
                risba_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(oddaljen_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, Navpično_položaj))
                območje_VALUE_9285603e += 폭*길이
            if območje_VALUE_9285603e:
                assert območje_VALUE_9285603e == 너비*višina_VALUE, območje_VALUE_9285603e
                return risba_VALUE

    def preveriti_slikovna_pika(좌표, 색):
        rok_VALUE = time.monotonic()+10
        while True:
            risba_VALUE = bitna_slika_IMAGE()
            if risba_VALUE.getpixel(좌표) == 색: return risba_VALUE
            if time.monotonic() > rok_VALUE: raise AssertionError((좌표, risba_VALUE.getpixel(좌표), 색))

    def Upload_Datoteke(Ime, podatki): Prenos_VALUE.storbinary('STOR '+Ime, io.BytesIO(podatki))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+spremeniti_velikost_SMS+' RGB32').encode() in LOG_zapis
        print('BOOT:', spremeniti_velikost_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_zapis).group(1))
        oddaljen_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(oddaljen_VALUE, 12) == b'RFB 003.008\n'; oddaljen_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(oddaljen_VALUE, EXACT_VALUE(oddaljen_VALUE, 1)[0]); oddaljen_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(oddaljen_VALUE, 4) == b'\0'*4; oddaljen_VALUE.sendall(b'\x01')
        začetno_stanje = EXACT_VALUE(oddaljen_VALUE, 24); assert struct.unpack('>HH', začetno_stanje[:4]) == (너비, višina_VALUE)
        EXACT_VALUE(oddaljen_VALUE, struct.unpack('>I', začetno_stanje[20:])[0])
        oddaljen_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        oddaljen_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        preveriti_slikovna_pika((너비-1, višina_VALUE-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, višina_VALUE-360+12, 1); 가리키기(너비-568+28, višina_VALUE-360+12, 0)
        preveriti_slikovna_pika((너비-568, višina_VALUE-360), (32, 80, 144))
        Zaženi = len(LOG_zapis); klik_VALUE(너비-20, višina_VALUE-345); 기다리기(b'TERMINAL FOCUS 1', Zaženi)
        preveriti_slikovna_pika((너비-568, višina_VALUE-360), (24, 32, 48))
        Zaženi = len(LOG_zapis); klik_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Zaženi)
        lupina('ftpd start')
        Prenos_VALUE = ftplib.FTP(); Prenos_VALUE.encoding = 'utf-8'; Prenos_VALUE.connect('127.0.0.1', številka_vrat, timeout=20); Prenos_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·izrezek 밖·빈 사각형을 포함한다.
        VIR = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), višina_VALUE=화면높이();
    if(너비!=WIDTH || višina_VALUE!=HEIGHT) return 1;
    if(risati_pravokotnik(너비,višina_VALUE,0,0,0)) return 2;
    if(risati_pravokotnik(너비,višina_VALUE-1,1,1,0)!=-22) return 3;
    if(risati_pravokotnik(너비-1,višina_VALUE,1,1,0)!=-22) return 4;
    if(risati_pravokotnik(-1,0,1,1,0)!=-22) return 5;
    if(risati_pravokotnik(0,0,-1,1,0)!=-22) return 6;
    if(risati_pravokotnik(너비-1,višina_VALUE-1,1,1,0x332211)) return 7;
    pisati_Datoteka_podatki(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(višina_VALUE))
        Upload_Datoteke('화면시험.c', VIR.encode())
        assert 'exit 0' in lupina('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', poslati_SMS('run /화면시험\n'))
        preveriti_slikovna_pika((너비-1, višina_VALUE-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', poslati_SMS('q'))
        VIR = '''from slovenščina import 화면크기, risati_pravokotnik, 그림기다리기, Izpis, sistemska_napaka
너비, višina_VALUE = 화면크기()
assert (너비, višina_VALUE) == (WIDTH, HEIGHT)
try:
    risati_pravokotnik(너비, višina_VALUE-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistemska_napaka as NAPAKA:
    assert NAPAKA.INDEX == 22
risati_pravokotnik(너비-1, višina_VALUE-1, 1, 1, 0x665544)
Izpis("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(višina_VALUE))
        Upload_Datoteke('화면시험.py', VIR.encode())
        기다리기(b'PYTHON RESOLUTION PASS', poslati_SMS('python /화면시험.py\n'))
        preveriti_slikovna_pika((너비-1, višina_VALUE-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', poslati_SMS('q'))
        VIR = '''import slovenščina.lastno.*;
public class ločljivost_preskusiti {
    public static void main(String[] Argumenti) {
        int 너비=화면.너비(), višina_VALUE=화면.višina_VALUE();
        if (너비!=WIDTH || višina_VALUE!=HEIGHT) throw new stanje_izjema("Velikost");
        try { 화면.pravokotnik(너비,višina_VALUE-1,1,1,0); throw new stanje_izjema("izrezek"); }
        catch (neveljaven_argument_izjema NAPAKA) { }
        화면.izbrisati_vnos(0x302018);
        화면.pravokotnik(너비-1,višina_VALUE-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(višina_VALUE))
        # izjema 처리는 gostiti javac 결과를 lastno JVM에 올려 검사한다.
        경계원문 = KR_pot/'해상도경계시험.java'
        경계원문.write_text(VIR.replace('class ločljivost_preskusiti', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(pobuda_koren/'dist/jkoros-native-korean.jar'), '-d', str(KR_pot), str(경계원문)])
        Upload_Datoteke('해상도경계시험.class', (KR_pot/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', poslati_SMS('java 해상도경계시험\n'))
        preveriti_slikovna_pika((너비-1, višina_VALUE-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', poslati_SMS('q'))
        # 게스트 javac의 Podpora_VALUE 문법으로 Velikost poizvedba_VALUE·izbrisati_vnos·다섯 Argumenti 그리기를 컴파일한다.
        VIR = '''public class ločljivost_preskusiti {
    public static void main(String[] Argumenti) {
        int 너비=slovenščina.lastno.화면.너비();
        int višina_VALUE=slovenščina.lastno.화면.višina_VALUE();
        if (너비!=WIDTH || višina_VALUE!=HEIGHT) return;
        slovenščina.lastno.화면.izbrisati_vnos(3153944);
        slovenščina.lastno.화면.pravokotnik(너비-1,višina_VALUE-1,1,1,10061943);
        slovenščina.lastno.Izpis.pisati_linija("JAVA RESOLUTION PASS");
        slovenščina.lastno.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(višina_VALUE))
        Upload_Datoteke('ločljivost_preskusiti.java', VIR.encode())
        REZULTAT = lupina('javac ločljivost_preskusiti.java'); assert 'exit 0' in REZULTAT, REZULTAT
        기다리기(b'JAVA RESOLUTION PASS', poslati_SMS('java ločljivost_preskusiti\n'))
        preveriti_slikovna_pika((너비-1, višina_VALUE-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', poslati_SMS('q'))
        Upload_Datoteke('Swing_preskusiti.class', (KR_pot/'Swing_preskusiti.class').read_bytes())
        기다리기(b'SWING READY', poslati_SMS('java Swing_preskusiti\n'))
        가로, Navpično_položaj = (너비-400)//2, (višina_VALUE-280)//2
        risba_VALUE = preveriti_slikovna_pika((가로, Navpično_položaj), (32, 80, 144))
        risba_VALUE.save(str(KR_pot/(spremeniti_velikost_SMS+'.png')))
        Zaženi = len(LOG_zapis); klik_VALUE(가로+80, Navpično_položaj+155)
        기다리기('SWING CLICK Ime'.encode(), Zaženi)
        Zaženi = len(LOG_zapis); klik_VALUE(가로+385, Navpično_položaj+15); 기다리기(b'jkoros-native> ', Zaženi)
        assert 'AFTER_RESOLUTION' in lupina('echo AFTER_RESOLUTION')
        print('PASS:', spremeniti_velikost_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Prenos_VALUE: Prenos_VALUE.close()
        if oddaljen_VALUE: oddaljen_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces_VALUE.kill(); Proces_VALUE.wait()
        izbirnik_a916db4e.close(); Proces_VALUE.stdout.close()
        (KR_pot/(spremeniti_velikost_SMS+'.log')).write_bytes(LOG_zapis)


def Zaženi():
    KR_pot = pobuda_koren/'build/verification/resolution'; KR_pot.mkdir(parents=True, exist_ok=True)
    LOG_zapis = {'passed': False, 'kernel_sha256': hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for neveljaven_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            REZULTAT = subprocess.run(['python3', str(pobuda_koren/'Orodja/Izvedi_ukaz.py'), '--resolution', neveljaven_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert REZULTAT.returncode == 2 and b'--resolution' in REZULTAT.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_pot), str(pobuda_koren/'시험/자바/Swing_preskusiti.java')])
        for 너비, višina_VALUE in ((1920,1080), (1280,720), (640,480)):
            ločljivost_preskusiti(너비, višina_VALUE, KR_pot); LOG_zapis['resolutions'].append([너비, višina_VALUE])
        LOG_zapis.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_pot/'report.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Zaženi()
