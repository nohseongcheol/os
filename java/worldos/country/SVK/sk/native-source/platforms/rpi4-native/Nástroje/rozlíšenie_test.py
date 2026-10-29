#!/usr/bin/env python3
"""skutočný_údaje QEMU/VNC에서 화면 Veľkosť·경계·Okno premiestniť_VALUE·Swing·언어별 그리기를 검사한다."""
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
from počítač_zobraziť import EXACT_VALUE
from Vykonať_príkaz import akcia_koreň


def rozlíšenie_test(너비, výška_VALUE, KR_cesta):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); číslo_portu = 임시.getsockname()[1]
    zmeniť_veľkosť_SMS = '{}x{}'.format(너비, výška_VALUE)
    Proces_VALUE = subprocess.Popen(['python3', str(akcia_koreň/'Nástroje/Vykonať_príkaz.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(číslo_portu), '--resolution', zmeniť_veľkosť_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor_a916db4e = selectors.DefaultSelector(); selektor_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); vzdialený_VALUE = None; prenos_VALUE = None

    def 기다리기(zobraziť_VALUE_487749b8, Spustiť_2=0):
        termín_VALUE = time.monotonic() + 60
        while zobraziť_VALUE_487749b8 not in LOG_RECORD[Spustiť_2:]:
            if time.monotonic() > termín_VALUE or Proces_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[Spustiť_2:].decode('utf-8', 'replace'))
            for Udalosť, _ in selektor_a916db4e.select(.1):
                údaje = Udalosť.fileobj.read(65536)
                if údaje: LOG_RECORD.extend(údaje)
        return LOG_RECORD[Spustiť_2:].decode('utf-8', 'replace')

    def kliknúť_tlačidlo(symbol, 눌림=True): vzdialený_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def odoslať_SMS_správu(Spracovanie_textu):
        Spustiť_2 = len(LOG_RECORD)
        for znak_VALUE in Spracovanie_textu:
            symbol = 0xff0d if znak_VALUE == '\n' else ord(znak_VALUE) if ord(znak_VALUE) < 256 else 0x1000000 | ord(znak_VALUE)
            kliknúť_tlačidlo(symbol); kliknúť_tlačidlo(symbol, False)
        return Spustiť_2

    def 셸(Spracovanie_textu): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', odoslať_SMS_správu(Spracovanie_textu+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, vertikála_pozícia, 눌림): vzdialený_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikála_pozícia))

    def kliknúť_VALUE(가로, vertikála_pozícia): 가리키기(가로, vertikála_pozícia, 1); 가리키기(가로, vertikála_pozícia, 0)

    def bitová_mapa_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 skutočný_údaje 너비를 쓴다.
        vzdialený_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, výška_VALUE))
        kresba_VALUE = Image.new('RGB', (너비, výška_VALUE)); oblasť_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(vzdialený_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                dĺžka_VALUE = struct.unpack('>I', EXACT_VALUE(vzdialený_VALUE, 7)[3:])[0]; EXACT_VALUE(vzdialený_VALUE, dĺžka_VALUE); continue
            assert 종류 == 0, 종류
            položka_COUNT = struct.unpack('>H', EXACT_VALUE(vzdialený_VALUE, 3)[1:])[0]
            for _ in range(položka_COUNT):
                가로, vertikála_pozícia, 폭, dĺžka_VALUE, kódovanie_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(vzdialený_VALUE, 12))
                assert kódovanie_VALUE == 0 and 가로+폭 <= 너비 and vertikála_pozícia+dĺžka_VALUE <= výška_VALUE
                kresba_VALUE.paste(Image.frombytes('RGB', (폭, dĺžka_VALUE), EXACT_VALUE(vzdialený_VALUE, 폭*dĺžka_VALUE*4), 'raw', 'BGRX'), (가로, vertikála_pozícia))
                oblasť_VALUE_9285603e += 폭*dĺžka_VALUE
            if oblasť_VALUE_9285603e:
                assert oblasť_VALUE_9285603e == 너비*výška_VALUE, oblasť_VALUE_9285603e
                return kresba_VALUE

    def skontrolovať_pixel(súradnica_VALUE, 색):
        termín_VALUE = time.monotonic()+10
        while True:
            kresba_VALUE = bitová_mapa_IMAGE()
            if kresba_VALUE.getpixel(súradnica_VALUE) == 색: return kresba_VALUE
            if time.monotonic() > termín_VALUE: raise AssertionError((súradnica_VALUE, kresba_VALUE.getpixel(súradnica_VALUE), 색))

    def nahrať_Súbory(Názov, údaje): prenos_VALUE.storbinary('STOR '+Názov, io.BytesIO(údaje))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+zmeniť_veľkosť_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', zmeniť_veľkosť_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        vzdialený_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(vzdialený_VALUE, 12) == b'RFB 003.008\n'; vzdialený_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(vzdialený_VALUE, EXACT_VALUE(vzdialený_VALUE, 1)[0]); vzdialený_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(vzdialený_VALUE, 4) == b'\0'*4; vzdialený_VALUE.sendall(b'\x01')
        počiatočný_stav = EXACT_VALUE(vzdialený_VALUE, 24); assert struct.unpack('>HH', počiatočný_stav[:4]) == (너비, výška_VALUE)
        EXACT_VALUE(vzdialený_VALUE, struct.unpack('>I', počiatočný_stav[20:])[0])
        vzdialený_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        vzdialený_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        skontrolovať_pixel((너비-1, výška_VALUE-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, výška_VALUE-360+12, 1); 가리키기(너비-568+28, výška_VALUE-360+12, 0)
        skontrolovať_pixel((너비-568, výška_VALUE-360), (32, 80, 144))
        Spustiť_2 = len(LOG_RECORD); kliknúť_VALUE(너비-20, výška_VALUE-345); 기다리기(b'TERMINAL FOCUS 1', Spustiť_2)
        skontrolovať_pixel((너비-568, výška_VALUE-360), (24, 32, 48))
        Spustiť_2 = len(LOG_RECORD); kliknúť_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Spustiť_2)
        셸('ftpd start')
        prenos_VALUE = ftplib.FTP(); prenos_VALUE.encoding = 'utf-8'; prenos_VALUE.connect('127.0.0.1', číslo_portu, timeout=20); prenos_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·klip 밖·빈 사각형을 포함한다.
        ZDROJ = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), výška_VALUE=화면높이();
    if(너비!=WIDTH || výška_VALUE!=HEIGHT) return 1;
    if(kresliť_obdĺžnik(너비,výška_VALUE,0,0,0)) return 2;
    if(kresliť_obdĺžnik(너비,výška_VALUE-1,1,1,0)!=-22) return 3;
    if(kresliť_obdĺžnik(너비-1,výška_VALUE,1,1,0)!=-22) return 4;
    if(kresliť_obdĺžnik(-1,0,1,1,0)!=-22) return 5;
    if(kresliť_obdĺžnik(0,0,-1,1,0)!=-22) return 6;
    if(kresliť_obdĺžnik(너비-1,výška_VALUE-1,1,1,0x332211)) return 7;
    zapísať_Súbor_údaje(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(výška_VALUE))
        nahrať_Súbory('화면시험.c', ZDROJ.encode())
        assert 'exit 0' in 셸('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', odoslať_SMS_správu('run /화면시험\n'))
        skontrolovať_pixel((너비-1, výška_VALUE-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', odoslať_SMS_správu('q'))
        ZDROJ = '''from Slovenský import 화면크기, kresliť_obdĺžnik, 그림기다리기, Výstup, systém_Chyba
너비, výška_VALUE = 화면크기()
assert (너비, výška_VALUE) == (WIDTH, HEIGHT)
try:
    kresliť_obdĺžnik(너비, výška_VALUE-1, 1, 1, 0)
    raise AssertionError("boundary")
except systém_Chyba as chyba:
    assert chyba.INDEX == 22
kresliť_obdĺžnik(너비-1, výška_VALUE-1, 1, 1, 0x665544)
Výstup("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(výška_VALUE))
        nahrať_Súbory('화면시험.py', ZDROJ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', odoslať_SMS_správu('python /화면시험.py\n'))
        skontrolovať_pixel((너비-1, výška_VALUE-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', odoslať_SMS_správu('q'))
        ZDROJ = '''import Slovenský.vlastné.*;
public class rozlíšenie_test {
    public static void main(String[] Argumenty) {
        int 너비=화면.너비(), výška_VALUE=화면.výška_VALUE();
        if (너비!=WIDTH || výška_VALUE!=HEIGHT) throw new Stav_výnimka("Veľkosť");
        try { 화면.obdĺžnik(너비,výška_VALUE-1,1,1,0); throw new Stav_výnimka("klip"); }
        catch (neplatné_argument_výnimka chyba) { }
        화면.vymazať_položka(0x302018);
        화면.obdĺžnik(너비-1,výška_VALUE-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(výška_VALUE))
        # výnimka 처리는 hostiteľ javac 결과를 vlastné JVM에 올려 검사한다.
        경계원문 = KR_cesta/'해상도경계시험.java'
        경계원문.write_text(ZDROJ.replace('class rozlíšenie_test', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(akcia_koreň/'dist/jkoros-native-korean.jar'), '-d', str(KR_cesta), str(경계원문)])
        nahrať_Súbory('해상도경계시험.class', (KR_cesta/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', odoslať_SMS_správu('java 해상도경계시험\n'))
        skontrolovať_pixel((너비-1, výška_VALUE-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', odoslať_SMS_správu('q'))
        # 게스트 javac의 Podpora_VALUE 문법으로 Veľkosť dotaz_VALUE·vymazať_položka·다섯 Argumenty 그리기를 컴파일한다.
        ZDROJ = '''public class rozlíšenie_test {
    public static void main(String[] Argumenty) {
        int 너비=Slovenský.vlastné.화면.너비();
        int výška_VALUE=Slovenský.vlastné.화면.výška_VALUE();
        if (너비!=WIDTH || výška_VALUE!=HEIGHT) return;
        Slovenský.vlastné.화면.vymazať_položka(3153944);
        Slovenský.vlastné.화면.obdĺžnik(너비-1,výška_VALUE-1,1,1,10061943);
        Slovenský.vlastné.Výstup.zapísať_linka("JAVA RESOLUTION PASS");
        Slovenský.vlastné.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(výška_VALUE))
        nahrať_Súbory('rozlíšenie_test.java', ZDROJ.encode())
        KR = 셸('javac rozlíšenie_test.java'); assert 'exit 0' in KR, KR
        기다리기(b'JAVA RESOLUTION PASS', odoslať_SMS_správu('java rozlíšenie_test\n'))
        skontrolovať_pixel((너비-1, výška_VALUE-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', odoslať_SMS_správu('q'))
        nahrať_Súbory('Swing_test.class', (KR_cesta/'Swing_test.class').read_bytes())
        기다리기(b'SWING READY', odoslať_SMS_správu('java Swing_test\n'))
        가로, vertikála_pozícia = (너비-400)//2, (výška_VALUE-280)//2
        kresba_VALUE = skontrolovať_pixel((가로, vertikála_pozícia), (32, 80, 144))
        kresba_VALUE.save(str(KR_cesta/(zmeniť_veľkosť_SMS+'.png')))
        Spustiť_2 = len(LOG_RECORD); kliknúť_VALUE(가로+80, vertikála_pozícia+155)
        기다리기('SWING CLICK Názov'.encode(), Spustiť_2)
        Spustiť_2 = len(LOG_RECORD); kliknúť_VALUE(가로+385, vertikála_pozícia+15); 기다리기(b'jkoros-native> ', Spustiť_2)
        assert 'AFTER_RESOLUTION' in 셸('echo AFTER_RESOLUTION')
        print('PASS:', zmeniť_veľkosť_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if prenos_VALUE: prenos_VALUE.close()
        if vzdialený_VALUE: vzdialený_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces_VALUE.kill(); Proces_VALUE.wait()
        selektor_a916db4e.close(); Proces_VALUE.stdout.close()
        (KR_cesta/(zmeniť_veľkosť_SMS+'.log')).write_bytes(LOG_RECORD)


def Spustiť_2():
    KR_cesta = akcia_koreň/'build/verification/resolution'; KR_cesta.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'kernel_sha256': hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for neplatné_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            KR = subprocess.run(['python3', str(akcia_koreň/'Nástroje/Vykonať_príkaz.py'), '--resolution', neplatné_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert KR.returncode == 2 and b'--resolution' in KR.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_cesta), str(akcia_koreň/'시험/자바/Swing_test.java')])
        for 너비, výška_VALUE in ((1920,1080), (1280,720), (640,480)):
            rozlíšenie_test(너비, výška_VALUE, KR_cesta); LOG_RECORD['resolutions'].append([너비, výška_VALUE])
        LOG_RECORD.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_cesta/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Spustiť_2()
