#!/usr/bin/env python3
"""verklig_data QEMU/VNC에서 skärmbild Storlek·gräns_värde·Fönster flytta_värde·Swing·언어별 그리기를 검사한다."""
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
from Dator_vy import EXAKT_värde
from köra_kommando import åtgärd_rot


def upplösning_test(너비, 높이, KR_väg):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); portnummer = 임시.getsockname()[1]
    storlek_SMS = '{}x{}'.format(너비, 높이)
    Process_värde = subprocess.Popen(['python3', str(åtgärd_rot/'verktyg/köra_kommando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portnummer), '--resolution', storlek_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    väljare_a916db4e = selectors.DefaultSelector(); väljare_a916db4e.register(Process_värde.stdout, selectors.EVENT_READ)
    LOG_POST = bytearray(); fjärr_värde = None; Överför_värde = None

    def 기다리기(visa_värde, Kör=0):
        måldatum_värde = time.monotonic() + 60
        while visa_värde not in LOG_POST[Kör:]:
            if time.monotonic() > måldatum_värde or Process_värde.poll() is not None or b'HALTED' in LOG_POST or b'PANIC:' in LOG_POST:
                raise AssertionError(LOG_POST[Kör:].decode('utf-8', 'replace'))
            for Händelse, _ in väljare_a916db4e.select(.1):
                data = Händelse.fileobj.read(65536)
                if data: LOG_POST.extend(data)
        return LOG_POST[Kör:].decode('utf-8', 'replace')

    def klick_knapp(symbol, 눌림=True): fjärr_värde.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def skicka_SMS(text):
        Kör = len(LOG_POST)
        for tecken_värde in text:
            symbol = 0xff0d if tecken_värde == '\n' else ord(tecken_värde) if ord(tecken_värde) < 256 else 0x1000000 | ord(tecken_värde)
            klick_knapp(symbol); klick_knapp(symbol, False)
        return Kör

    def Shell(text): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', skicka_SMS(text+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, bransch_placera, 눌림): fjärr_värde.sendall(struct.pack('>BBHH', 5, 눌림, 가로, bransch_placera))

    def klick_värde(가로, bransch_placera): 가리키기(가로, bransch_placera, 1); 가리키기(가로, bransch_placera, 0)

    def bitmapp_BILD():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 verklig_data 너비를 쓴다.
        fjärr_värde.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ritning_värde = Image.new('RGB', (너비, 높이)); yta_värde = 0
        while True:
            variant_värde = EXAKT_värde(fjärr_värde, 1)[0]
            if variant_värde == 2: continue
            if variant_värde == 3:
                längd_värde = struct.unpack('>I', EXAKT_värde(fjärr_värde, 7)[3:])[0]; EXAKT_värde(fjärr_värde, längd_värde); continue
            assert variant_värde == 0, variant_värde
            objekt_ANTAL = struct.unpack('>H', EXAKT_värde(fjärr_värde, 3)[1:])[0]
            for _ in range(objekt_ANTAL):
                가로, bransch_placera, 폭, längd_värde, kodning_värde = struct.unpack('>HHHHi', EXAKT_värde(fjärr_värde, 12))
                assert kodning_värde == 0 and 가로+폭 <= 너비 and bransch_placera+längd_värde <= 높이
                ritning_värde.paste(Image.frombytes('RGB', (폭, längd_värde), EXAKT_värde(fjärr_värde, 폭*längd_värde*4), 'raw', 'BGRX'), (가로, bransch_placera))
                yta_värde += 폭*längd_värde
            if yta_värde:
                assert yta_värde == 너비*높이, yta_värde
                return ritning_värde

    def check_bildpunkt(koordinat_värde, 색):
        måldatum_värde = time.monotonic()+10
        while True:
            ritning_värde = bitmapp_BILD()
            if ritning_värde.getpixel(koordinat_värde) == 색: return ritning_värde
            if time.monotonic() > måldatum_värde: raise AssertionError((koordinat_värde, ritning_värde.getpixel(koordinat_värde), 색))

    def Upload_Filer(Namn, data): Överför_värde.storbinary('STOR '+Namn, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+storlek_SMS+' RGB32').encode() in LOG_POST
        print('BOOT:', storlek_SMS, flush=True)
        fjärr_nummer = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_POST).group(1))
        fjärr_värde = socket.create_connection(('127.0.0.1', fjärr_nummer), timeout=20)
        assert EXAKT_värde(fjärr_värde, 12) == b'RFB 003.008\n'; fjärr_värde.sendall(b'RFB 003.008\n')
        assert 1 in EXAKT_värde(fjärr_värde, EXAKT_värde(fjärr_värde, 1)[0]); fjärr_värde.sendall(b'\x01')
        assert EXAKT_värde(fjärr_värde, 4) == b'\0'*4; fjärr_värde.sendall(b'\x01')
        starttillstånd = EXAKT_värde(fjärr_värde, 24); assert struct.unpack('>HH', starttillstånd[:4]) == (너비, 높이)
        EXAKT_värde(fjärr_värde, struct.unpack('>I', starttillstånd[20:])[0])
        fjärr_värde.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        fjärr_värde.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        check_bildpunkt((너비-1, 높이-1), (24, 32, 48))
        # skärmbild HÖGER 아래까지 이동한다. Föregående_objekt 640×480 gräns_värde 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        check_bildpunkt((너비-568, 높이-360), (32, 80, 144))
        Kör = len(LOG_POST); klick_värde(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Kör)
        check_bildpunkt((너비-568, 높이-360), (24, 32, 48))
        Kör = len(LOG_POST); klick_värde(80, 16); 기다리기(b'TERMINAL FOCUS 1', Kör)
        Shell('ftpd start')
        Överför_värde = ftplib.FTP(); Överför_värde.encoding = 'utf-8'; Överför_värde.connect('127.0.0.1', portnummer, timeout=20); Överför_värde.login()
        # C gräns_värde 검사는 32비트 unsigned 음수 KONVERTERA_värde·klipp 밖·빈 사각형을 포함한다.
        källfil = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(Rita_rektangel(너비,높이,0,0,0)) return 2;
    if(Rita_rektangel(너비,높이-1,1,1,0)!=-22) return 3;
    if(Rita_rektangel(너비-1,높이,1,1,0)!=-22) return 4;
    if(Rita_rektangel(-1,0,1,1,0)!=-22) return 5;
    if(Rita_rektangel(0,0,-1,1,0)!=-22) return 6;
    if(Rita_rektangel(너비-1,높이-1,1,1,0x332211)) return 7;
    skriva_fil_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Filer('test_skärmbild.c', källfil.encode())
        assert 'exit 0' in Shell('cc /test_skärmbild.c -o /test_skärmbild')
        기다리기(b'C RESOLUTION PASS', skicka_SMS('run /test_skärmbild\n'))
        check_bildpunkt((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', skicka_SMS('q'))
        källfil = '''from Svenska import skärmbild_storlek, Rita_rektangel, 그림기다리기, utmatningsposition, systemfel
너비, 높이 = skärmbild_storlek()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    Rita_rektangel(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except systemfel as fel:
    assert fel.INDEX == 22
Rita_rektangel(너비-1, 높이-1, 1, 1, 0x665544)
utmatningsposition("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Filer('test_skärmbild.py', källfil.encode())
        기다리기(b'PYTHON RESOLUTION PASS', skicka_SMS('python /test_skärmbild.py\n'))
        check_bildpunkt((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', skicka_SMS('q'))
        källfil = '''import Svenska.eget.*;
public class upplösning_test {
    public static void main(String[] argument) {
        int 너비=skärmbild.너비(), 높이=skärmbild.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new status_fel("Storlek");
        try { skärmbild.rektangel(너비,높이-1,1,1,0); throw new status_fel("klipp"); }
        catch (ogiltig_argument_fel fel) { }
        skärmbild.radera_post(0x302018);
        skärmbild.rektangel(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        skärmbild.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # fel_31f743d2 처리는 värd javac 결과를 eget JVM에 올려 검사한다.
        gräns_källa = KR_väg/'해상도경계시험.java'
        gräns_källa.write_text(källfil.replace('class upplösning_test', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(åtgärd_rot/'dist/jkoros-native-korean.jar'), '-d', str(KR_väg), str(gräns_källa)])
        Upload_Filer('해상도경계시험.class', (KR_väg/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', skicka_SMS('java 해상도경계시험\n'))
        check_bildpunkt((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', skicka_SMS('q'))
        # 게스트 javac의 stöd_värde 문법으로 Storlek fråga_värde·radera_post·다섯 argument 그리기를 컴파일한다.
        källfil = '''public class upplösning_test {
    public static void main(String[] argument) {
        int 너비=Svenska.eget.skärmbild.너비();
        int 높이=Svenska.eget.skärmbild.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Svenska.eget.skärmbild.radera_post(3153944);
        Svenska.eget.skärmbild.rektangel(너비-1,높이-1,1,1,10061943);
        Svenska.eget.utmatningsposition.skriva_rad("JAVA RESOLUTION PASS");
        Svenska.eget.skärmbild.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Filer('upplösning_test.java', källfil.encode())
        RESULTAT = Shell('javac upplösning_test.java'); assert 'exit 0' in RESULTAT, RESULTAT
        기다리기(b'JAVA RESOLUTION PASS', skicka_SMS('java upplösning_test\n'))
        check_bildpunkt((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', skicka_SMS('q'))
        Upload_Filer('Swing_test.class', (KR_väg/'Swing_test.class').read_bytes())
        기다리기(b'SWING READY', skicka_SMS('java Swing_test\n'))
        가로, bransch_placera = (너비-400)//2, (높이-280)//2
        ritning_värde = check_bildpunkt((가로, bransch_placera), (32, 80, 144))
        ritning_värde.save(str(KR_väg/(storlek_SMS+'.png')))
        Kör = len(LOG_POST); klick_värde(가로+80, bransch_placera+155)
        기다리기('SWING CLICK Namn'.encode(), Kör)
        Kör = len(LOG_POST); klick_värde(가로+385, bransch_placera+15); 기다리기(b'jkoros-native> ', Kör)
        assert 'AFTER_RESOLUTION' in Shell('echo AFTER_RESOLUTION')
        print('PASS:', storlek_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Överför_värde: Överför_värde.close()
        if fjärr_värde: fjärr_värde.close()
        if Process_värde.poll() is None:
            Process_värde.terminate()
            try: Process_värde.wait(timeout=8)
            except subprocess.TimeoutExpired: Process_värde.kill(); Process_värde.wait()
        väljare_a916db4e.close(); Process_värde.stdout.close()
        (KR_väg/(storlek_SMS+'.log')).write_bytes(LOG_POST)


def Kör():
    KR_väg = åtgärd_rot/'build/verification/resolution'; KR_väg.mkdir(parents=True, exist_ok=True)
    LOG_POST = {'passed': False, 'kernel_sha256': hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ogiltig_värde in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            RESULTAT = subprocess.run(['python3', str(åtgärd_rot/'verktyg/köra_kommando.py'), '--resolution', ogiltig_värde], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert RESULTAT.returncode == 2 and b'--resolution' in RESULTAT.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_väg), str(åtgärd_rot/'tester/자바/Swing_test.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            upplösning_test(너비, 높이, KR_väg); LOG_POST['resolutions'].append([너비, 높이])
        LOG_POST.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_väg/'report.json').write_text(json.dumps(LOG_POST, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Kör()
