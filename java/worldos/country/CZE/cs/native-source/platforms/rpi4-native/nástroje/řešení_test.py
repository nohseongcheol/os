#!/usr/bin/env python3
"""skutečný_data QEMU/VNC에서 화면 Velikost·mez_HODNOTA·Okno přesunout_HODNOTA·Swing·언어별 그리기를 검사한다."""
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
from Plocha_pohled import STEJNÉ_HODNOTA
from Provést_příkaz import akce_kořen


def řešení_test(너비, výška_HODNOTA, KV_cesta):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); číslo_portu = 임시.getsockname()[1]
    změnit_velikost_SMS = '{}x{}'.format(너비, výška_HODNOTA)
    Proces_HODNOTA = subprocess.Popen(['python3', str(akce_kořen/'nástroje/Provést_příkaz.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(číslo_portu), '--resolution', změnit_velikost_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor_a916db4e = selectors.DefaultSelector(); selektor_a916db4e.register(Proces_HODNOTA.stdout, selectors.EVENT_READ)
    LOGZ_ZÁZNAM = bytearray(); vzdálený_HODNOTA = None; přenos_HODNOTA = None

    def 기다리기(zobrazit_HODNOTA, Spustit_2=0):
        konečný_termín_HODNOTA = time.monotonic() + 60
        while zobrazit_HODNOTA not in LOGZ_ZÁZNAM[Spustit_2:]:
            if time.monotonic() > konečný_termín_HODNOTA or Proces_HODNOTA.poll() is not None or b'HALTED' in LOGZ_ZÁZNAM or b'PANIC:' in LOGZ_ZÁZNAM:
                raise AssertionError(LOGZ_ZÁZNAM[Spustit_2:].decode('utf-8', 'replace'))
            for Události, _ in selektor_a916db4e.select(.1):
                data = Události.fileobj.read(65536)
                if data: LOGZ_ZÁZNAM.extend(data)
        return LOGZ_ZÁZNAM[Spustit_2:].decode('utf-8', 'replace')

    def klepnout_tlačítko(symbol, 눌림=True): vzdálený_HODNOTA.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def poslat_SMS(text):
        Spustit_2 = len(LOGZ_ZÁZNAM)
        for znak_HODNOTA in text:
            symbol = 0xff0d if znak_HODNOTA == '\n' else ord(znak_HODNOTA) if ord(znak_HODNOTA) < 256 else 0x1000000 | ord(znak_HODNOTA)
            klepnout_tlačítko(symbol); klepnout_tlačítko(symbol, False)
        return Spustit_2

    def prostředí(text): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', poslat_SMS(text+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Svislá_pozice, 눌림): vzdálený_HODNOTA.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Svislá_pozice))

    def klepnout_HODNOTA(가로, Svislá_pozice): 가리키기(가로, Svislá_pozice, 1); 가리키기(가로, Svislá_pozice, 0)

    def rastrový_obrázek_image():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 skutečný_data 너비를 쓴다.
        vzdálený_HODNOTA.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, výška_HODNOTA))
        kreslení_HODNOTA = Image.new('RGB', (너비, výška_HODNOTA)); oblast_HODNOTA_9285603e = 0
        while True:
            Druh_HODNOTA = STEJNÉ_HODNOTA(vzdálený_HODNOTA, 1)[0]
            if Druh_HODNOTA == 2: continue
            if Druh_HODNOTA == 3:
                délka_HODNOTA = struct.unpack('>I', STEJNÉ_HODNOTA(vzdálený_HODNOTA, 7)[3:])[0]; STEJNÉ_HODNOTA(vzdálený_HODNOTA, délka_HODNOTA); continue
            assert Druh_HODNOTA == 0, Druh_HODNOTA
            zboží_POČET = struct.unpack('>H', STEJNÉ_HODNOTA(vzdálený_HODNOTA, 3)[1:])[0]
            for _ in range(zboží_POČET):
                가로, Svislá_pozice, 폭, délka_HODNOTA, Encoding_HODNOTA = struct.unpack('>HHHHi', STEJNÉ_HODNOTA(vzdálený_HODNOTA, 12))
                assert Encoding_HODNOTA == 0 and 가로+폭 <= 너비 and Svislá_pozice+délka_HODNOTA <= výška_HODNOTA
                kreslení_HODNOTA.paste(Image.frombytes('RGB', (폭, délka_HODNOTA), STEJNÉ_HODNOTA(vzdálený_HODNOTA, 폭*délka_HODNOTA*4), 'raw', 'BGRX'), (가로, Svislá_pozice))
                oblast_HODNOTA_9285603e += 폭*délka_HODNOTA
            if oblast_HODNOTA_9285603e:
                assert oblast_HODNOTA_9285603e == 너비*výška_HODNOTA, oblast_HODNOTA_9285603e
                return kreslení_HODNOTA

    def šek_pixel(souřadnice_HODNOTA, 색):
        konečný_termín_HODNOTA = time.monotonic()+10
        while True:
            kreslení_HODNOTA = rastrový_obrázek_image()
            if kreslení_HODNOTA.getpixel(souřadnice_HODNOTA) == 색: return kreslení_HODNOTA
            if time.monotonic() > konečný_termín_HODNOTA: raise AssertionError((souřadnice_HODNOTA, kreslení_HODNOTA.getpixel(souřadnice_HODNOTA), 색))

    def Upload_Files(Název, data): přenos_HODNOTA.storbinary('STOR '+Název, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+změnit_velikost_SMS+' RGB32').encode() in LOGZ_ZÁZNAM
        print('BOOT:', změnit_velikost_SMS, flush=True)
        vzdálený_číslo = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOGZ_ZÁZNAM).group(1))
        vzdálený_HODNOTA = socket.create_connection(('127.0.0.1', vzdálený_číslo), timeout=20)
        assert STEJNÉ_HODNOTA(vzdálený_HODNOTA, 12) == b'RFB 003.008\n'; vzdálený_HODNOTA.sendall(b'RFB 003.008\n')
        assert 1 in STEJNÉ_HODNOTA(vzdálený_HODNOTA, STEJNÉ_HODNOTA(vzdálený_HODNOTA, 1)[0]); vzdálený_HODNOTA.sendall(b'\x01')
        assert STEJNÉ_HODNOTA(vzdálený_HODNOTA, 4) == b'\0'*4; vzdálený_HODNOTA.sendall(b'\x01')
        počáteční_stav = STEJNÉ_HODNOTA(vzdálený_HODNOTA, 24); assert struct.unpack('>HH', počáteční_stav[:4]) == (너비, výška_HODNOTA)
        STEJNÉ_HODNOTA(vzdálený_HODNOTA, struct.unpack('>I', počáteční_stav[20:])[0])
        vzdálený_HODNOTA.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        vzdálený_HODNOTA.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        šek_pixel((너비-1, výška_HODNOTA-1), (24, 32, 48))
        # 화면 právo 아래까지 이동한다. Předchozí_zboží 640×480 mez_HODNOTA 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, výška_HODNOTA-360+12, 1); 가리키기(너비-568+28, výška_HODNOTA-360+12, 0)
        šek_pixel((너비-568, výška_HODNOTA-360), (32, 80, 144))
        Spustit_2 = len(LOGZ_ZÁZNAM); klepnout_HODNOTA(너비-20, výška_HODNOTA-345); 기다리기(b'TERMINAL FOCUS 1', Spustit_2)
        šek_pixel((너비-568, výška_HODNOTA-360), (24, 32, 48))
        Spustit_2 = len(LOGZ_ZÁZNAM); klepnout_HODNOTA(80, 16); 기다리기(b'TERMINAL FOCUS 1', Spustit_2)
        prostředí('ftpd start')
        přenos_HODNOTA = ftplib.FTP(); přenos_HODNOTA.encoding = 'utf-8'; přenos_HODNOTA.connect('127.0.0.1', číslo_portu, timeout=20); přenos_HODNOTA.login()
        # C mez_HODNOTA 검사는 32비트 unsigned 음수 CONVERT_HODNOTA·oříznout 밖·빈 사각형을 포함한다.
        zdrojový_soubor = '''#include <화면규약.h>
#include <Soubor_ABI.h>
int main(void) {
    unsigned 너비=화면너비(), výška_HODNOTA=화면높이();
    if(너비!=WIDTH || výška_HODNOTA!=HEIGHT) return 1;
    if(kreslit_obdélník(너비,výška_HODNOTA,0,0,0)) return 2;
    if(kreslit_obdélník(너비,výška_HODNOTA-1,1,1,0)!=-22) return 3;
    if(kreslit_obdélník(너비-1,výška_HODNOTA,1,1,0)!=-22) return 4;
    if(kreslit_obdélník(-1,0,1,1,0)!=-22) return 5;
    if(kreslit_obdélník(0,0,-1,1,0)!=-22) return 6;
    if(kreslit_obdélník(너비-1,výška_HODNOTA-1,1,1,0x332211)) return 7;
    zápis_Soubor_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(výška_HODNOTA))
        Upload_Files('화면시험.c', zdrojový_soubor.encode())
        assert 'exit 0' in prostředí('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', poslat_SMS('run /화면시험\n'))
        šek_pixel((너비-1, výška_HODNOTA-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', poslat_SMS('q'))
        zdrojový_soubor = '''from čeština import 화면크기, kreslit_obdélník, 그림기다리기, výstupní_pozice, chyba_systému
너비, výška_HODNOTA = 화면크기()
assert (너비, výška_HODNOTA) == (WIDTH, HEIGHT)
try:
    kreslit_obdélník(너비, výška_HODNOTA-1, 1, 1, 0)
    raise AssertionError("boundary")
except chyba_systému as chyba:
    assert chyba.INDEX == 22
kreslit_obdélník(너비-1, výška_HODNOTA-1, 1, 1, 0x665544)
výstupní_pozice("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(výška_HODNOTA))
        Upload_Files('화면시험.py', zdrojový_soubor.encode())
        기다리기(b'PYTHON RESOLUTION PASS', poslat_SMS('python /화면시험.py\n'))
        šek_pixel((너비-1, výška_HODNOTA-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', poslat_SMS('q'))
        zdrojový_soubor = '''import čeština.vlastní.*;
public class řešení_test {
    public static void main(String[] argumenty) {
        int 너비=화면.너비(), výška_HODNOTA=화면.výška_HODNOTA();
        if (너비!=WIDTH || výška_HODNOTA!=HEIGHT) throw new Stav_výjimka("Velikost");
        try { 화면.obdélník(너비,výška_HODNOTA-1,1,1,0); throw new Stav_výjimka("oříznout"); }
        catch (neplatný_argument_výjimka chyba) { }
        화면.vymazat_položka(0x302018);
        화면.obdélník(너비-1,výška_HODNOTA-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(výška_HODNOTA))
        # výjimka 처리는 hostit javac 결과를 vlastní JVM에 올려 검사한다.
        mez_zdroj = KV_cesta/'해상도경계시험.java'
        mez_zdroj.write_text(zdrojový_soubor.replace('class řešení_test', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(akce_kořen/'dist/jkoros-native-korean.jar'), '-d', str(KV_cesta), str(mez_zdroj)])
        Upload_Files('해상도경계시험.class', (KV_cesta/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', poslat_SMS('java 해상도경계시험\n'))
        šek_pixel((너비-1, výška_HODNOTA-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', poslat_SMS('q'))
        # 게스트 javac의 vzpěra_HODNOTA 문법으로 Velikost dotaz_HODNOTA·vymazat_položka·다섯 argumenty 그리기를 컴파일한다.
        zdrojový_soubor = '''public class řešení_test {
    public static void main(String[] argumenty) {
        int 너비=čeština.vlastní.화면.너비();
        int výška_HODNOTA=čeština.vlastní.화면.výška_HODNOTA();
        if (너비!=WIDTH || výška_HODNOTA!=HEIGHT) return;
        čeština.vlastní.화면.vymazat_položka(3153944);
        čeština.vlastní.화면.obdélník(너비-1,výška_HODNOTA-1,1,1,10061943);
        čeština.vlastní.výstupní_pozice.zápis_čára("JAVA RESOLUTION PASS");
        čeština.vlastní.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(výška_HODNOTA))
        Upload_Files('řešení_test.java', zdrojový_soubor.encode())
        VÝSLEDEK = prostředí('javac řešení_test.java'); assert 'exit 0' in VÝSLEDEK, VÝSLEDEK
        기다리기(b'JAVA RESOLUTION PASS', poslat_SMS('java řešení_test\n'))
        šek_pixel((너비-1, výška_HODNOTA-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', poslat_SMS('q'))
        Upload_Files('Swing_test.class', (KV_cesta/'Swing_test.class').read_bytes())
        기다리기(b'SWING READY', poslat_SMS('java Swing_test\n'))
        가로, Svislá_pozice = (너비-400)//2, (výška_HODNOTA-280)//2
        kreslení_HODNOTA = šek_pixel((가로, Svislá_pozice), (32, 80, 144))
        kreslení_HODNOTA.save(str(KV_cesta/(změnit_velikost_SMS+'.png')))
        Spustit_2 = len(LOGZ_ZÁZNAM); klepnout_HODNOTA(가로+80, Svislá_pozice+155)
        기다리기('SWING CLICK Název'.encode(), Spustit_2)
        Spustit_2 = len(LOGZ_ZÁZNAM); klepnout_HODNOTA(가로+385, Svislá_pozice+15); 기다리기(b'jkoros-native> ', Spustit_2)
        assert 'AFTER_RESOLUTION' in prostředí('echo AFTER_RESOLUTION')
        print('PASS:', změnit_velikost_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if přenos_HODNOTA: přenos_HODNOTA.close()
        if vzdálený_HODNOTA: vzdálený_HODNOTA.close()
        if Proces_HODNOTA.poll() is None:
            Proces_HODNOTA.terminate()
            try: Proces_HODNOTA.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces_HODNOTA.kill(); Proces_HODNOTA.wait()
        selektor_a916db4e.close(); Proces_HODNOTA.stdout.close()
        (KV_cesta/(změnit_velikost_SMS+'.log')).write_bytes(LOGZ_ZÁZNAM)


def Spustit_2():
    KV_cesta = akce_kořen/'build/verification/resolution'; KV_cesta.mkdir(parents=True, exist_ok=True)
    LOGZ_ZÁZNAM = {'passed': False, 'kernel_sha256': hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for neplatný_HODNOTA in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            VÝSLEDEK = subprocess.run(['python3', str(akce_kořen/'nástroje/Provést_příkaz.py'), '--resolution', neplatný_HODNOTA], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert VÝSLEDEK.returncode == 2 and b'--resolution' in VÝSLEDEK.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KV_cesta), str(akce_kořen/'zkoušky/자바/Swing_test.java')])
        for 너비, výška_HODNOTA in ((1920,1080), (1280,720), (640,480)):
            řešení_test(너비, výška_HODNOTA, KV_cesta); LOGZ_ZÁZNAM['resolutions'].append([너비, výška_HODNOTA])
        LOGZ_ZÁZNAM.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KV_cesta/'report.json').write_text(json.dumps(LOGZ_ZÁZNAM, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Spustit_2()
