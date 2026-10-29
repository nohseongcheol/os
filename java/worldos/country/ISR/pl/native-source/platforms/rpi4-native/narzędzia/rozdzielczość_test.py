#!/usr/bin/env python3
"""rzeczywisty_dane QEMU/VNC에서 화면 Rozmiar·granica_WARTOŚĆ·Okno przenosić_WARTOŚĆ·Swing·언어별 그리기를 검사한다."""
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
from Pulpit_Widok import PORÓWNAJ_WARTOŚĆ
from Wykonaj_polecenie import Project_korzeń


def rozdzielczość_test(너비, wysokość_WARTOŚĆ, KR_ścieżka):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); numer_portu = 임시.getsockname()[1]
    zmienić_rozmiar_SMS = '{}x{}'.format(너비, wysokość_WARTOŚĆ)
    Proces_WARTOŚĆ = subprocess.Popen(['python3', str(Project_korzeń/'narzędzia/Wykonaj_polecenie.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(numer_portu), '--resolution', zmienić_rozmiar_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor_a916db4e = selectors.DefaultSelector(); selektor_a916db4e.register(Proces_WARTOŚĆ.stdout, selectors.EVENT_READ)
    LOG_zapis = bytearray(); zdalny_WARTOŚĆ = None; transfer_WARTOŚĆ = None

    def 기다리기(program_WARTOŚĆ, Uruchom_2=0):
        termin_ostateczny_WARTOŚĆ = time.monotonic() + 60
        while program_WARTOŚĆ not in LOG_zapis[Uruchom_2:]:
            if time.monotonic() > termin_ostateczny_WARTOŚĆ or Proces_WARTOŚĆ.poll() is not None or b'HALTED' in LOG_zapis or b'PANIC:' in LOG_zapis:
                raise AssertionError(LOG_zapis[Uruchom_2:].decode('utf-8', 'replace'))
            for Wydarzenie, _ in selektor_a916db4e.select(.1):
                dane = Wydarzenie.fileobj.read(65536)
                if dane: LOG_zapis.extend(dane)
        return LOG_zapis[Uruchom_2:].decode('utf-8', 'replace')

    def klikać_przycisk(symbol, 눌림=True): zdalny_WARTOŚĆ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def wysłać_SMS_a(tekst):
        Uruchom_2 = len(LOG_zapis)
        for znak_WARTOŚĆ in tekst:
            symbol = 0xff0d if znak_WARTOŚĆ == '\n' else ord(znak_WARTOŚĆ) if ord(znak_WARTOŚĆ) < 256 else 0x1000000 | ord(znak_WARTOŚĆ)
            klikać_przycisk(symbol); klikać_przycisk(symbol, False)
        return Uruchom_2

    def powłoka(tekst): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', wysłać_SMS_a(tekst+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, gałąź_stanowisko, 눌림): zdalny_WARTOŚĆ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, gałąź_stanowisko))

    def klikać_WARTOŚĆ(가로, gałąź_stanowisko): 가리키기(가로, gałąź_stanowisko, 1); 가리키기(가로, gałąź_stanowisko, 0)

    def mapa_bitowa_OBRAZ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 rzeczywisty_dane 너비를 쓴다.
        zdalny_WARTOŚĆ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, wysokość_WARTOŚĆ))
        rysunek_WARTOŚĆ = Image.new('RGB', (너비, wysokość_WARTOŚĆ)); obszar_WARTOŚĆ_9285603e = 0
        while True:
            Rodzaj_WARTOŚĆ = PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 1)[0]
            if Rodzaj_WARTOŚĆ == 2: continue
            if Rodzaj_WARTOŚĆ == 3:
                długość_WARTOŚĆ = struct.unpack('>I', PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 7)[3:])[0]; PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, długość_WARTOŚĆ); continue
            assert Rodzaj_WARTOŚĆ == 0, Rodzaj_WARTOŚĆ
            towar_ILE_LICZB = struct.unpack('>H', PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 3)[1:])[0]
            for _ in range(towar_ILE_LICZB):
                가로, gałąź_stanowisko, 폭, długość_WARTOŚĆ, Encoding_WARTOŚĆ = struct.unpack('>HHHHi', PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 12))
                assert Encoding_WARTOŚĆ == 0 and 가로+폭 <= 너비 and gałąź_stanowisko+długość_WARTOŚĆ <= wysokość_WARTOŚĆ
                rysunek_WARTOŚĆ.paste(Image.frombytes('RGB', (폭, długość_WARTOŚĆ), PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 폭*długość_WARTOŚĆ*4), 'raw', 'BGRX'), (가로, gałąź_stanowisko))
                obszar_WARTOŚĆ_9285603e += 폭*długość_WARTOŚĆ
            if obszar_WARTOŚĆ_9285603e:
                assert obszar_WARTOŚĆ_9285603e == 너비*wysokość_WARTOŚĆ, obszar_WARTOŚĆ_9285603e
                return rysunek_WARTOŚĆ

    def czek_piksel(współrzędna_WARTOŚĆ, 색):
        termin_ostateczny_WARTOŚĆ = time.monotonic()+10
        while True:
            rysunek_WARTOŚĆ = mapa_bitowa_OBRAZ()
            if rysunek_WARTOŚĆ.getpixel(współrzędna_WARTOŚĆ) == 색: return rysunek_WARTOŚĆ
            if time.monotonic() > termin_ostateczny_WARTOŚĆ: raise AssertionError((współrzędna_WARTOŚĆ, rysunek_WARTOŚĆ.getpixel(współrzędna_WARTOŚĆ), 색))

    def Upload_Files(Nazwa, dane): transfer_WARTOŚĆ.storbinary('STOR '+Nazwa, io.BytesIO(dane))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+zmienić_rozmiar_SMS+' RGB32').encode() in LOG_zapis
        print('BOOT:', zmienić_rozmiar_SMS, flush=True)
        zdalny_identyfikator = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_zapis).group(1))
        zdalny_WARTOŚĆ = socket.create_connection(('127.0.0.1', zdalny_identyfikator), timeout=20)
        assert PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 12) == b'RFB 003.008\n'; zdalny_WARTOŚĆ.sendall(b'RFB 003.008\n')
        assert 1 in PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 1)[0]); zdalny_WARTOŚĆ.sendall(b'\x01')
        assert PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 4) == b'\0'*4; zdalny_WARTOŚĆ.sendall(b'\x01')
        stan_początkowy = PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 24); assert struct.unpack('>HH', stan_początkowy[:4]) == (너비, wysokość_WARTOŚĆ)
        PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, struct.unpack('>I', stan_początkowy[20:])[0])
        zdalny_WARTOŚĆ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        zdalny_WARTOŚĆ.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        czek_piksel((너비-1, wysokość_WARTOŚĆ-1), (24, 32, 48))
        # 화면 PRAWY 아래까지 이동한다. Wstecz_towar 640×480 granica_WARTOŚĆ 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, wysokość_WARTOŚĆ-360+12, 1); 가리키기(너비-568+28, wysokość_WARTOŚĆ-360+12, 0)
        czek_piksel((너비-568, wysokość_WARTOŚĆ-360), (32, 80, 144))
        Uruchom_2 = len(LOG_zapis); klikać_WARTOŚĆ(너비-20, wysokość_WARTOŚĆ-345); 기다리기(b'TERMINAL FOCUS 1', Uruchom_2)
        czek_piksel((너비-568, wysokość_WARTOŚĆ-360), (24, 32, 48))
        Uruchom_2 = len(LOG_zapis); klikać_WARTOŚĆ(80, 16); 기다리기(b'TERMINAL FOCUS 1', Uruchom_2)
        powłoka('ftpd start')
        transfer_WARTOŚĆ = ftplib.FTP(); transfer_WARTOŚĆ.encoding = 'utf-8'; transfer_WARTOŚĆ.connect('127.0.0.1', numer_portu, timeout=20); transfer_WARTOŚĆ.login()
        # C granica_WARTOŚĆ 검사는 32비트 unsigned negatywny_WARTOŚĆ KONWERTUJ_WARTOŚĆ·obcinać 밖·빈 사각형을 포함한다.
        plik_źródłowy = '''#include <화면규약.h>
#include <Plik_ABI.h>
int main(void) {
    unsigned 너비=화면너비(), wysokość_WARTOŚĆ=화면높이();
    if(너비!=WIDTH || wysokość_WARTOŚĆ!=HEIGHT) return 1;
    if(rysować_prostokąt(너비,wysokość_WARTOŚĆ,0,0,0)) return 2;
    if(rysować_prostokąt(너비,wysokość_WARTOŚĆ-1,1,1,0)!=-22) return 3;
    if(rysować_prostokąt(너비-1,wysokość_WARTOŚĆ,1,1,0)!=-22) return 4;
    if(rysować_prostokąt(-1,0,1,1,0)!=-22) return 5;
    if(rysować_prostokąt(0,0,-1,1,0)!=-22) return 6;
    if(rysować_prostokąt(너비-1,wysokość_WARTOŚĆ-1,1,1,0x332211)) return 7;
    zapis_Plik_dane(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(wysokość_WARTOŚĆ))
        Upload_Files('화면시험.c', plik_źródłowy.encode())
        assert 'exit 0' in powłoka('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', wysłać_SMS_a('run /화면시험\n'))
        czek_piksel((너비-1, wysokość_WARTOŚĆ-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', wysłać_SMS_a('q'))
        plik_źródłowy = '''from polski import 화면크기, rysować_prostokąt, 그림기다리기, pozycja_wyjścia, błąd_systemu
너비, wysokość_WARTOŚĆ = 화면크기()
assert (너비, wysokość_WARTOŚĆ) == (WIDTH, HEIGHT)
try:
    rysować_prostokąt(너비, wysokość_WARTOŚĆ-1, 1, 1, 0)
    raise AssertionError("boundary")
except błąd_systemu as błąd:
    assert błąd.INDEKS == 22
rysować_prostokąt(너비-1, wysokość_WARTOŚĆ-1, 1, 1, 0x665544)
pozycja_wyjścia("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(wysokość_WARTOŚĆ))
        Upload_Files('화면시험.py', plik_źródłowy.encode())
        기다리기(b'PYTHON RESOLUTION PASS', wysłać_SMS_a('python /화면시험.py\n'))
        czek_piksel((너비-1, wysokość_WARTOŚĆ-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', wysłać_SMS_a('q'))
        plik_źródłowy = '''import polski.własny.*;
public class rozdzielczość_test {
    public static void main(String[] argumenty) {
        int 너비=화면.너비(), wysokość_WARTOŚĆ=화면.wysokość_WARTOŚĆ();
        if (너비!=WIDTH || wysokość_WARTOŚĆ!=HEIGHT) throw new Stan_wyjątek("Rozmiar");
        try { 화면.prostokąt(너비,wysokość_WARTOŚĆ-1,1,1,0); throw new Stan_wyjątek("obcinać"); }
        catch (nieważny_argument_wyjątek błąd) { }
        화면.usunąć_wpis(0x302018);
        화면.prostokąt(너비-1,wysokość_WARTOŚĆ-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(wysokość_WARTOŚĆ))
        # wyjątek 처리는 host javac 결과를 własny JVM에 올려 검사한다.
        granica_źródło = KR_ścieżka/'해상도경계시험.java'
        granica_źródło.write_text(plik_źródłowy.replace('class rozdzielczość_test', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_korzeń/'dist/jkoros-native-korean.jar'), '-d', str(KR_ścieżka), str(granica_źródło)])
        Upload_Files('해상도경계시험.class', (KR_ścieżka/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', wysłać_SMS_a('java 해상도경계시험\n'))
        czek_piksel((너비-1, wysokość_WARTOŚĆ-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', wysłać_SMS_a('q'))
        # 게스트 javac의 wsparcie_WARTOŚĆ 문법으로 Rozmiar zapytanie_WARTOŚĆ·usunąć_wpis·다섯 argumenty 그리기를 컴파일한다.
        plik_źródłowy = '''public class rozdzielczość_test {
    public static void main(String[] argumenty) {
        int 너비=polski.własny.화면.너비();
        int wysokość_WARTOŚĆ=polski.własny.화면.wysokość_WARTOŚĆ();
        if (너비!=WIDTH || wysokość_WARTOŚĆ!=HEIGHT) return;
        polski.własny.화면.usunąć_wpis(3153944);
        polski.własny.화면.prostokąt(너비-1,wysokość_WARTOŚĆ-1,1,1,10061943);
        polski.własny.pozycja_wyjścia.zapis_linia("JAVA RESOLUTION PASS");
        polski.własny.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(wysokość_WARTOŚĆ))
        Upload_Files('rozdzielczość_test.java', plik_źródłowy.encode())
        WYNIK = powłoka('javac rozdzielczość_test.java'); assert 'exit 0' in WYNIK, WYNIK
        기다리기(b'JAVA RESOLUTION PASS', wysłać_SMS_a('java rozdzielczość_test\n'))
        czek_piksel((너비-1, wysokość_WARTOŚĆ-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', wysłać_SMS_a('q'))
        Upload_Files('Swing_test.class', (KR_ścieżka/'Swing_test.class').read_bytes())
        기다리기(b'SWING READY', wysłać_SMS_a('java Swing_test\n'))
        가로, gałąź_stanowisko = (너비-400)//2, (wysokość_WARTOŚĆ-280)//2
        rysunek_WARTOŚĆ = czek_piksel((가로, gałąź_stanowisko), (32, 80, 144))
        rysunek_WARTOŚĆ.save(str(KR_ścieżka/(zmienić_rozmiar_SMS+'.png')))
        Uruchom_2 = len(LOG_zapis); klikać_WARTOŚĆ(가로+80, gałąź_stanowisko+155)
        기다리기('SWING CLICK Nazwa'.encode(), Uruchom_2)
        Uruchom_2 = len(LOG_zapis); klikać_WARTOŚĆ(가로+385, gałąź_stanowisko+15); 기다리기(b'jkoros-native> ', Uruchom_2)
        assert 'AFTER_RESOLUTION' in powłoka('echo AFTER_RESOLUTION')
        print('PASS:', zmienić_rozmiar_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if transfer_WARTOŚĆ: transfer_WARTOŚĆ.close()
        if zdalny_WARTOŚĆ: zdalny_WARTOŚĆ.close()
        if Proces_WARTOŚĆ.poll() is None:
            Proces_WARTOŚĆ.terminate()
            try: Proces_WARTOŚĆ.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces_WARTOŚĆ.kill(); Proces_WARTOŚĆ.wait()
        selektor_a916db4e.close(); Proces_WARTOŚĆ.stdout.close()
        (KR_ścieżka/(zmienić_rozmiar_SMS+'.log')).write_bytes(LOG_zapis)


def Uruchom_2():
    KR_ścieżka = Project_korzeń/'build/verification/resolution'; KR_ścieżka.mkdir(parents=True, exist_ok=True)
    LOG_zapis = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for nieważny_WARTOŚĆ in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            WYNIK = subprocess.run(['python3', str(Project_korzeń/'narzędzia/Wykonaj_polecenie.py'), '--resolution', nieważny_WARTOŚĆ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert WYNIK.returncode == 2 and b'--resolution' in WYNIK.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_ścieżka), str(Project_korzeń/'testy/자바/Swing_test.java')])
        for 너비, wysokość_WARTOŚĆ in ((1920,1080), (1280,720), (640,480)):
            rozdzielczość_test(너비, wysokość_WARTOŚĆ, KR_ścieżka); LOG_zapis['resolutions'].append([너비, wysokość_WARTOŚĆ])
        LOG_zapis.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_ścieżka/'report.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Uruchom_2()
