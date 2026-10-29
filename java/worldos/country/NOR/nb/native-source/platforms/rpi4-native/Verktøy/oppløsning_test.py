#!/usr/bin/env python3
"""faktisk_data QEMU/VNC에서 skjermbilde Størrelse·grense_VERDI·Vindu flytte_VERDI_83b651b8·Swing·언어별 그리기를 검사한다."""
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
from stasjonær_vise import EKSAKT_VERDI
from Utfør_kommando import speile_rot


def oppløsning_test(너비, 높이, KR_bane):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); portnummer = 임시.getsockname()[1]
    skalere_SMS = '{}x{}'.format(너비, 높이)
    Prosess_VERDI = subprocess.Popen(['python3', str(speile_rot/'Verktøy/Utfør_kommando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portnummer), '--resolution', skalere_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    velger_a916db4e = selectors.DefaultSelector(); velger_a916db4e.register(Prosess_VERDI.stdout, selectors.EVENT_READ)
    LOG_POST = bytearray(); ekstern_VERDI_28edcfa1 = None; overføre_VERDI = None

    def 기다리기(vise_VERDI_487749b8, Kjør_2=0):
        tidsfrist_VERDI = time.monotonic() + 60
        while vise_VERDI_487749b8 not in LOG_POST[Kjør_2:]:
            if time.monotonic() > tidsfrist_VERDI or Prosess_VERDI.poll() is not None or b'HALTED' in LOG_POST or b'PANIC:' in LOG_POST:
                raise AssertionError(LOG_POST[Kjør_2:].decode('utf-8', 'replace'))
            for Hendelse, _ in velger_a916db4e.select(.1):
                data = Hendelse.fileobj.read(65536)
                if data: LOG_POST.extend(data)
        return LOG_POST[Kjør_2:].decode('utf-8', 'replace')

    def klikk_knapp(symbol, 눌림=True): ekstern_VERDI_28edcfa1.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def send_SMS(Tekst):
        Kjør_2 = len(LOG_POST)
        for tegn_VERDI in Tekst:
            symbol = 0xff0d if tegn_VERDI == '\n' else ord(tegn_VERDI) if ord(tegn_VERDI) < 256 else 0x1000000 | ord(tegn_VERDI)
            klikk_knapp(symbol); klikk_knapp(symbol, False)
        return Kjør_2

    def Shell(Tekst): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', send_SMS(Tekst+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, vertikal_plassere, 눌림): ekstern_VERDI_28edcfa1.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikal_plassere))

    def klikk_VERDI(가로, vertikal_plassere): 가리키기(가로, vertikal_plassere, 1); 가리키기(가로, vertikal_plassere, 0)

    def punktgrafikk_BILDE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 faktisk_data 너비를 쓴다.
        ekstern_VERDI_28edcfa1.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        tegning_VERDI = Image.new('RGB', (너비, 높이)); område_VERDI_9285603e = 0
        while True:
            종류 = EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                lengde_VERDI = struct.unpack('>I', EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 7)[3:])[0]; EKSAKT_VERDI(ekstern_VERDI_28edcfa1, lengde_VERDI); continue
            assert 종류 == 0, 종류
            vare_ANTALL = struct.unpack('>H', EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 3)[1:])[0]
            for _ in range(vare_ANTALL):
                가로, vertikal_plassere, 폭, lengde_VERDI, koding_VERDI = struct.unpack('>HHHHi', EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 12))
                assert koding_VERDI == 0 and 가로+폭 <= 너비 and vertikal_plassere+lengde_VERDI <= 높이
                tegning_VERDI.paste(Image.frombytes('RGB', (폭, lengde_VERDI), EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 폭*lengde_VERDI*4), 'raw', 'BGRX'), (가로, vertikal_plassere))
                område_VERDI_9285603e += 폭*lengde_VERDI
            if område_VERDI_9285603e:
                assert område_VERDI_9285603e == 너비*높이, område_VERDI_9285603e
                return tegning_VERDI

    def sjekk_piksel(koordinat_VERDI, 색):
        tidsfrist_VERDI = time.monotonic()+10
        while True:
            tegning_VERDI = punktgrafikk_BILDE()
            if tegning_VERDI.getpixel(koordinat_VERDI) == 색: return tegning_VERDI
            if time.monotonic() > tidsfrist_VERDI: raise AssertionError((koordinat_VERDI, tegning_VERDI.getpixel(koordinat_VERDI), 색))

    def Upload_Filer(Navn, data): overføre_VERDI.storbinary('STOR '+Navn, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+skalere_SMS+' RGB32').encode() in LOG_POST
        print('BOOT:', skalere_SMS, flush=True)
        ekstern_nummer = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_POST).group(1))
        ekstern_VERDI_28edcfa1 = socket.create_connection(('127.0.0.1', ekstern_nummer), timeout=20)
        assert EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 12) == b'RFB 003.008\n'; ekstern_VERDI_28edcfa1.sendall(b'RFB 003.008\n')
        assert 1 in EKSAKT_VERDI(ekstern_VERDI_28edcfa1, EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 1)[0]); ekstern_VERDI_28edcfa1.sendall(b'\x01')
        assert EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 4) == b'\0'*4; ekstern_VERDI_28edcfa1.sendall(b'\x01')
        opprinnelig_tilstand = EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 24); assert struct.unpack('>HH', opprinnelig_tilstand[:4]) == (너비, 높이)
        EKSAKT_VERDI(ekstern_VERDI_28edcfa1, struct.unpack('>I', opprinnelig_tilstand[20:])[0])
        ekstern_VERDI_28edcfa1.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ekstern_VERDI_28edcfa1.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        sjekk_piksel((너비-1, 높이-1), (24, 32, 48))
        # skjermbilde HØYRE 아래까지 이동한다. Forrige_vare 640×480 grense_VERDI 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        sjekk_piksel((너비-568, 높이-360), (32, 80, 144))
        Kjør_2 = len(LOG_POST); klikk_VERDI(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Kjør_2)
        sjekk_piksel((너비-568, 높이-360), (24, 32, 48))
        Kjør_2 = len(LOG_POST); klikk_VERDI(80, 16); 기다리기(b'TERMINAL FOCUS 1', Kjør_2)
        Shell('ftpd start')
        overføre_VERDI = ftplib.FTP(); overføre_VERDI.encoding = 'utf-8'; overføre_VERDI.connect('127.0.0.1', portnummer, timeout=20); overføre_VERDI.login()
        # C grense_VERDI 검사는 32비트 unsigned 음수 KONVERTER_VERDI·klippe 밖·빈 사각형을 포함한다.
        KILDE = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(Tegn_rektangel(너비,높이,0,0,0)) return 2;
    if(Tegn_rektangel(너비,높이-1,1,1,0)!=-22) return 3;
    if(Tegn_rektangel(너비-1,높이,1,1,0)!=-22) return 4;
    if(Tegn_rektangel(-1,0,1,1,0)!=-22) return 5;
    if(Tegn_rektangel(0,0,-1,1,0)!=-22) return 6;
    if(Tegn_rektangel(너비-1,높이-1,1,1,0x332211)) return 7;
    skrive_Fil_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Filer('test_skjermbilde.c', KILDE.encode())
        assert 'exit 0' in Shell('cc /test_skjermbilde.c -o /test_skjermbilde')
        기다리기(b'C RESOLUTION PASS', send_SMS('run /test_skjermbilde\n'))
        sjekk_piksel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', send_SMS('q'))
        KILDE = '''from norsk import skjermbilde_skalere, Tegn_rektangel, 그림기다리기, Utgang, systemfeil
너비, 높이 = skjermbilde_skalere()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    Tegn_rektangel(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except systemfeil as feil:
    assert feil.INDEKS == 22
Tegn_rektangel(너비-1, 높이-1, 1, 1, 0x665544)
Utgang("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Filer('test_skjermbilde.py', KILDE.encode())
        기다리기(b'PYTHON RESOLUTION PASS', send_SMS('python /test_skjermbilde.py\n'))
        sjekk_piksel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', send_SMS('q'))
        KILDE = '''import norsk.eget.*;
public class oppløsning_test {
    public static void main(String[] Argumenter) {
        int 너비=skjermbilde.너비(), 높이=skjermbilde.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new status_unntak("Størrelse");
        try { skjermbilde.rektangel(너비,높이-1,1,1,0); throw new status_unntak("klippe"); }
        catch (ugyldig_argument_unntak feil) { }
        skjermbilde.slette_oppføring(0x302018);
        skjermbilde.rektangel(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        skjermbilde.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # unntak 처리는 vert javac 결과를 eget JVM에 올려 검사한다.
        grense_kilde = KR_bane/'해상도경계시험.java'
        grense_kilde.write_text(KILDE.replace('class oppløsning_test', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(speile_rot/'dist/jkoros-native-korean.jar'), '-d', str(KR_bane), str(grense_kilde)])
        Upload_Filer('해상도경계시험.class', (KR_bane/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', send_SMS('java 해상도경계시험\n'))
        sjekk_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', send_SMS('q'))
        # 게스트 javac의 støtte_VERDI 문법으로 Størrelse spørre_VERDI·slette_oppføring·다섯 Argumenter 그리기를 컴파일한다.
        KILDE = '''public class oppløsning_test {
    public static void main(String[] Argumenter) {
        int 너비=norsk.eget.skjermbilde.너비();
        int 높이=norsk.eget.skjermbilde.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        norsk.eget.skjermbilde.slette_oppføring(3153944);
        norsk.eget.skjermbilde.rektangel(너비-1,높이-1,1,1,10061943);
        norsk.eget.Utgang.skrive_linje("JAVA RESOLUTION PASS");
        norsk.eget.skjermbilde.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Filer('oppløsning_test.java', KILDE.encode())
        KR = Shell('javac oppløsning_test.java'); assert 'exit 0' in KR, KR
        기다리기(b'JAVA RESOLUTION PASS', send_SMS('java oppløsning_test\n'))
        sjekk_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', send_SMS('q'))
        Upload_Filer('Swing_test.class', (KR_bane/'Swing_test.class').read_bytes())
        기다리기(b'SWING READY', send_SMS('java Swing_test\n'))
        가로, vertikal_plassere = (너비-400)//2, (높이-280)//2
        tegning_VERDI = sjekk_piksel((가로, vertikal_plassere), (32, 80, 144))
        tegning_VERDI.save(str(KR_bane/(skalere_SMS+'.png')))
        Kjør_2 = len(LOG_POST); klikk_VERDI(가로+80, vertikal_plassere+155)
        기다리기('SWING CLICK Navn'.encode(), Kjør_2)
        Kjør_2 = len(LOG_POST); klikk_VERDI(가로+385, vertikal_plassere+15); 기다리기(b'jkoros-native> ', Kjør_2)
        assert 'AFTER_RESOLUTION' in Shell('echo AFTER_RESOLUTION')
        print('PASS:', skalere_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if overføre_VERDI: overføre_VERDI.close()
        if ekstern_VERDI_28edcfa1: ekstern_VERDI_28edcfa1.close()
        if Prosess_VERDI.poll() is None:
            Prosess_VERDI.terminate()
            try: Prosess_VERDI.wait(timeout=8)
            except subprocess.TimeoutExpired: Prosess_VERDI.kill(); Prosess_VERDI.wait()
        velger_a916db4e.close(); Prosess_VERDI.stdout.close()
        (KR_bane/(skalere_SMS+'.log')).write_bytes(LOG_POST)


def Kjør_2():
    KR_bane = speile_rot/'build/verification/resolution'; KR_bane.mkdir(parents=True, exist_ok=True)
    LOG_POST = {'passed': False, 'kernel_sha256': hashlib.sha256((speile_rot/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ugyldig_VERDI in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            KR = subprocess.run(['python3', str(speile_rot/'Verktøy/Utfør_kommando.py'), '--resolution', ugyldig_VERDI], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert KR.returncode == 2 and b'--resolution' in KR.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_bane), str(speile_rot/'시험/자바/Swing_test.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            oppløsning_test(너비, 높이, KR_bane); LOG_POST['resolutions'].append([너비, 높이])
        LOG_POST.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_bane/'report.json').write_text(json.dumps(LOG_POST, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Kjør_2()
