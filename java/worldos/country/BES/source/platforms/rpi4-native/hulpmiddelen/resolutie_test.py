#!/usr/bin/env python3
"""werkelijk_gegevens QEMU/VNC에서 scherm Grootte·grens_WAARDE·Venster verplaatsen_WAARDE_83b651b8·Swing·언어별 그리기를 검사한다."""
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
from pc_Weergave import GELIJK_WAARDE
from Uitvoeren_opdracht import Taken_wortel


def resolutie_test(너비, hoogte_WAARDE, HR_pad):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); poortnummer = 임시.getsockname()[1]
    formaat_wijzigen_sms = '{}x{}'.format(너비, hoogte_WAARDE)
    Proces_WAARDE = subprocess.Popen(['python3', str(Taken_wortel/'hulpmiddelen/Uitvoeren_opdracht.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(poortnummer), '--resolution', formaat_wijzigen_sms], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selector_a916db4e = selectors.DefaultSelector(); selector_a916db4e.register(Proces_WAARDE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); extern_WAARDE_28edcfa1 = None; transfer_WAARDE = None

    def 기다리기(weergeven_WAARDE, starten=0):
        deadline_WAARDE = time.monotonic() + 60
        while weergeven_WAARDE not in LOG_RECORD[starten:]:
            if time.monotonic() > deadline_WAARDE or Proces_WAARDE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[starten:].decode('utf-8', 'replace'))
            for Gebeurtenis, _ in selector_a916db4e.select(.1):
                gegevens = Gebeurtenis.fileobj.read(65536)
                if gegevens: LOG_RECORD.extend(gegevens)
        return LOG_RECORD[starten:].decode('utf-8', 'replace')

    def click_knop(symbool, 눌림=True): extern_WAARDE_28edcfa1.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbool))

    def sms_en(tekst):
        starten = len(LOG_RECORD)
        for teken_WAARDE in tekst:
            symbool = 0xff0d if teken_WAARDE == '\n' else ord(teken_WAARDE) if ord(teken_WAARDE) < 256 else 0x1000000 | ord(teken_WAARDE)
            click_knop(symbool); click_knop(symbool, False)
        return starten

    def Shell(tekst): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', sms_en(tekst+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Verticaal_functie, 눌림): extern_WAARDE_28edcfa1.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Verticaal_functie))

    def click_WAARDE(가로, Verticaal_functie): 가리키기(가로, Verticaal_functie, 1); 가리키기(가로, Verticaal_functie, 0)

    def bitmap_kopie():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 werkelijk_gegevens 너비를 쓴다.
        extern_WAARDE_28edcfa1.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, hoogte_WAARDE))
        tekening_WAARDE = Image.new('RGB', (너비, hoogte_WAARDE)); gebied_WAARDE_9285603e = 0
        while True:
            soort_WAARDE = GELIJK_WAARDE(extern_WAARDE_28edcfa1, 1)[0]
            if soort_WAARDE == 2: continue
            if soort_WAARDE == 3:
                tijdsduur_WAARDE = struct.unpack('>I', GELIJK_WAARDE(extern_WAARDE_28edcfa1, 7)[3:])[0]; GELIJK_WAARDE(extern_WAARDE_28edcfa1, tijdsduur_WAARDE); continue
            assert soort_WAARDE == 0, soort_WAARDE
            item_AANTAL = struct.unpack('>H', GELIJK_WAARDE(extern_WAARDE_28edcfa1, 3)[1:])[0]
            for _ in range(item_AANTAL):
                가로, Verticaal_functie, 폭, tijdsduur_WAARDE, Encoding_WAARDE = struct.unpack('>HHHHi', GELIJK_WAARDE(extern_WAARDE_28edcfa1, 12))
                assert Encoding_WAARDE == 0 and 가로+폭 <= 너비 and Verticaal_functie+tijdsduur_WAARDE <= hoogte_WAARDE
                tekening_WAARDE.paste(Image.frombytes('RGB', (폭, tijdsduur_WAARDE), GELIJK_WAARDE(extern_WAARDE_28edcfa1, 폭*tijdsduur_WAARDE*4), 'raw', 'BGRX'), (가로, Verticaal_functie))
                gebied_WAARDE_9285603e += 폭*tijdsduur_WAARDE
            if gebied_WAARDE_9285603e:
                assert gebied_WAARDE_9285603e == 너비*hoogte_WAARDE, gebied_WAARDE_9285603e
                return tekening_WAARDE

    def cheque_pixel(coördinaat_WAARDE, 색):
        deadline_WAARDE = time.monotonic()+10
        while True:
            tekening_WAARDE = bitmap_kopie()
            if tekening_WAARDE.getpixel(coördinaat_WAARDE) == 색: return tekening_WAARDE
            if time.monotonic() > deadline_WAARDE: raise AssertionError((coördinaat_WAARDE, tekening_WAARDE.getpixel(coördinaat_WAARDE), 색))

    def Upload_Files(Naam, gegevens): transfer_WAARDE.storbinary('STOR '+Naam, io.BytesIO(gegevens))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+formaat_wijzigen_sms+' RGB32').encode() in LOG_RECORD
        print('BOOT:', formaat_wijzigen_sms, flush=True)
        extern_nummer = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        extern_WAARDE_28edcfa1 = socket.create_connection(('127.0.0.1', extern_nummer), timeout=20)
        assert GELIJK_WAARDE(extern_WAARDE_28edcfa1, 12) == b'RFB 003.008\n'; extern_WAARDE_28edcfa1.sendall(b'RFB 003.008\n')
        assert 1 in GELIJK_WAARDE(extern_WAARDE_28edcfa1, GELIJK_WAARDE(extern_WAARDE_28edcfa1, 1)[0]); extern_WAARDE_28edcfa1.sendall(b'\x01')
        assert GELIJK_WAARDE(extern_WAARDE_28edcfa1, 4) == b'\0'*4; extern_WAARDE_28edcfa1.sendall(b'\x01')
        begintoestand = GELIJK_WAARDE(extern_WAARDE_28edcfa1, 24); assert struct.unpack('>HH', begintoestand[:4]) == (너비, hoogte_WAARDE)
        GELIJK_WAARDE(extern_WAARDE_28edcfa1, struct.unpack('>I', begintoestand[20:])[0])
        extern_WAARDE_28edcfa1.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        extern_WAARDE_28edcfa1.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        cheque_pixel((너비-1, hoogte_WAARDE-1), (24, 32, 48))
        # scherm recht 아래까지 이동한다. Vorige_item 640×480 grens_WAARDE 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, hoogte_WAARDE-360+12, 1); 가리키기(너비-568+28, hoogte_WAARDE-360+12, 0)
        cheque_pixel((너비-568, hoogte_WAARDE-360), (32, 80, 144))
        starten = len(LOG_RECORD); click_WAARDE(너비-20, hoogte_WAARDE-345); 기다리기(b'TERMINAL FOCUS 1', starten)
        cheque_pixel((너비-568, hoogte_WAARDE-360), (24, 32, 48))
        starten = len(LOG_RECORD); click_WAARDE(80, 16); 기다리기(b'TERMINAL FOCUS 1', starten)
        Shell('ftpd start')
        transfer_WAARDE = ftplib.FTP(); transfer_WAARDE.encoding = 'utf-8'; transfer_WAARDE.connect('127.0.0.1', poortnummer, timeout=20); transfer_WAARDE.login()
        # C grens_WAARDE 검사는 32비트 unsigned 음수 CONVERTEREN_WAARDE·clip 밖·빈 사각형을 포함한다.
        broncode = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), hoogte_WAARDE=scherm_hoogte();
    if(너비!=WIDTH || hoogte_WAARDE!=HEIGHT) return 1;
    if(Tekenen_rechthoek(너비,hoogte_WAARDE,0,0,0)) return 2;
    if(Tekenen_rechthoek(너비,hoogte_WAARDE-1,1,1,0)!=-22) return 3;
    if(Tekenen_rechthoek(너비-1,hoogte_WAARDE,1,1,0)!=-22) return 4;
    if(Tekenen_rechthoek(-1,0,1,1,0)!=-22) return 5;
    if(Tekenen_rechthoek(0,0,-1,1,0)!=-22) return 6;
    if(Tekenen_rechthoek(너비-1,hoogte_WAARDE-1,1,1,0x332211)) return 7;
    schrijven_Bestand_gegevens(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(hoogte_WAARDE))
        Upload_Files('test_scherm.c', broncode.encode())
        assert 'exit 0' in Shell('cc /test_scherm.c -o /test_scherm')
        기다리기(b'C RESOLUTION PASS', sms_en('run /test_scherm\n'))
        cheque_pixel((너비-1, hoogte_WAARDE-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', sms_en('q'))
        broncode = '''from Nederlands import scherm_formaat_wijzigen, Tekenen_rechthoek, 그림기다리기, tekstuitvoer, systeemfout
너비, hoogte_WAARDE = scherm_formaat_wijzigen()
assert (너비, hoogte_WAARDE) == (WIDTH, HEIGHT)
try:
    Tekenen_rechthoek(너비, hoogte_WAARDE-1, 1, 1, 0)
    raise AssertionError("boundary")
except systeemfout as fout:
    assert fout.INDEX == 22
Tekenen_rechthoek(너비-1, hoogte_WAARDE-1, 1, 1, 0x665544)
tekstuitvoer("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(hoogte_WAARDE))
        Upload_Files('test_scherm.py', broncode.encode())
        기다리기(b'PYTHON RESOLUTION PASS', sms_en('python /test_scherm.py\n'))
        cheque_pixel((너비-1, hoogte_WAARDE-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', sms_en('q'))
        broncode = '''import Nederlands.Eigen.*;
public class resolutie_test {
    public static void main(String[] argumenten) {
        int 너비=scherm.너비(), hoogte_WAARDE=scherm.hoogte_WAARDE();
        if (너비!=WIDTH || hoogte_WAARDE!=HEIGHT) throw new Status_uitzondering("Grootte");
        try { scherm.rechthoek(너비,hoogte_WAARDE-1,1,1,0); throw new Status_uitzondering("clip"); }
        catch (nietig_argument_uitzondering fout) { }
        scherm.wissen_invoer(0x302018);
        scherm.rechthoek(너비-1,hoogte_WAARDE-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        scherm.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(hoogte_WAARDE))
        # uitzondering 처리는 host javac 결과를 Eigen JVM에 올려 검사한다.
        grens_bron = HR_pad/'해상도경계시험.java'
        grens_bron.write_text(broncode.replace('class resolutie_test', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Taken_wortel/'dist/jkoros-native-korean.jar'), '-d', str(HR_pad), str(grens_bron)])
        Upload_Files('해상도경계시험.class', (HR_pad/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', sms_en('java 해상도경계시험\n'))
        cheque_pixel((너비-1, hoogte_WAARDE-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', sms_en('q'))
        # 게스트 javac의 steun_WAARDE 문법으로 Grootte query_WAARDE·wissen_invoer·다섯 argumenten 그리기를 컴파일한다.
        broncode = '''public class resolutie_test {
    public static void main(String[] argumenten) {
        int 너비=Nederlands.Eigen.scherm.너비();
        int hoogte_WAARDE=Nederlands.Eigen.scherm.hoogte_WAARDE();
        if (너비!=WIDTH || hoogte_WAARDE!=HEIGHT) return;
        Nederlands.Eigen.scherm.wissen_invoer(3153944);
        Nederlands.Eigen.scherm.rechthoek(너비-1,hoogte_WAARDE-1,1,1,10061943);
        Nederlands.Eigen.tekstuitvoer.schrijven_lijn("JAVA RESOLUTION PASS");
        Nederlands.Eigen.scherm.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(hoogte_WAARDE))
        Upload_Files('resolutie_test.java', broncode.encode())
        resultaat = Shell('javac resolutie_test.java'); assert 'exit 0' in resultaat, resultaat
        기다리기(b'JAVA RESOLUTION PASS', sms_en('java resolutie_test\n'))
        cheque_pixel((너비-1, hoogte_WAARDE-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', sms_en('q'))
        Upload_Files('Swing_test.class', (HR_pad/'Swing_test.class').read_bytes())
        기다리기(b'SWING READY', sms_en('java Swing_test\n'))
        가로, Verticaal_functie = (너비-400)//2, (hoogte_WAARDE-280)//2
        tekening_WAARDE = cheque_pixel((가로, Verticaal_functie), (32, 80, 144))
        tekening_WAARDE.save(str(HR_pad/(formaat_wijzigen_sms+'.png')))
        starten = len(LOG_RECORD); click_WAARDE(가로+80, Verticaal_functie+155)
        기다리기('SWING CLICK Naam'.encode(), starten)
        starten = len(LOG_RECORD); click_WAARDE(가로+385, Verticaal_functie+15); 기다리기(b'jkoros-native> ', starten)
        assert 'AFTER_RESOLUTION' in Shell('echo AFTER_RESOLUTION')
        print('PASS:', formaat_wijzigen_sms, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if transfer_WAARDE: transfer_WAARDE.close()
        if extern_WAARDE_28edcfa1: extern_WAARDE_28edcfa1.close()
        if Proces_WAARDE.poll() is None:
            Proces_WAARDE.terminate()
            try: Proces_WAARDE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces_WAARDE.kill(); Proces_WAARDE.wait()
        selector_a916db4e.close(); Proces_WAARDE.stdout.close()
        (HR_pad/(formaat_wijzigen_sms+'.log')).write_bytes(LOG_RECORD)


def starten():
    HR_pad = Taken_wortel/'build/verification/resolution'; HR_pad.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'kernel_sha256': hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for nietig_WAARDE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            resultaat = subprocess.run(['python3', str(Taken_wortel/'hulpmiddelen/Uitvoeren_opdracht.py'), '--resolution', nietig_WAARDE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert resultaat.returncode == 2 and b'--resolution' in resultaat.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(HR_pad), str(Taken_wortel/'tests/자바/Swing_test.java')])
        for 너비, hoogte_WAARDE in ((1920,1080), (1280,720), (640,480)):
            resolutie_test(너비, hoogte_WAARDE, HR_pad); LOG_RECORD['resolutions'].append([너비, hoogte_WAARDE])
        LOG_RECORD.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (HR_pad/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': starten()
