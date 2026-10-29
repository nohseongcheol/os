#!/usr/bin/env python3
"""tegelik_andmed QEMU/VNC에서 화면 Suurus·경계·aken liigutama_VALUE·Swing·언어별 그리기를 검사한다."""
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
from töölaud_Kuva import EXACT_VALUE
from Täida_käsk import Project_juur


def 해상도시험(너비, 높이, näitaja_tee):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); pordinumber = 임시.getsockname()[1]
    suurust_muutma_SMS = '{}x{}'.format(너비, 높이)
    Joonis_VALUE = subprocess.Popen(['python3', str(Project_juur/'Tööriistad/Täida_käsk.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(pordinumber), '--resolution', suurust_muutma_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    valija_a916db4e = selectors.DefaultSelector(); valija_a916db4e.register(Joonis_VALUE.stdout, selectors.EVENT_READ)
    LOG_kirje = bytearray(); kauge_VALUE = None; Edasta_VALUE = None

    def 기다리기(saade_VALUE, Käivita_2=0):
        tähtaeg_VALUE = time.monotonic() + 60
        while saade_VALUE not in LOG_kirje[Käivita_2:]:
            if time.monotonic() > tähtaeg_VALUE or Joonis_VALUE.poll() is not None or b'HALTED' in LOG_kirje or b'PANIC:' in LOG_kirje:
                raise AssertionError(LOG_kirje[Käivita_2:].decode('utf-8', 'replace'))
            for Sündmus, _ in valija_a916db4e.select(.1):
                andmed = Sündmus.fileobj.read(65536)
                if andmed: LOG_kirje.extend(andmed)
        return LOG_kirje[Käivita_2:].decode('utf-8', 'replace')

    def klõps_nupp(sümbol, 눌림=True): kauge_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, sümbol))

    def SMSi_saatmine(Tekst):
        Käivita_2 = len(LOG_kirje)
        for märk_VALUE in Tekst:
            sümbol = 0xff0d if märk_VALUE == '\n' else ord(märk_VALUE) if ord(märk_VALUE) < 256 else 0x1000000 | ord(märk_VALUE)
            klõps_nupp(sümbol); klõps_nupp(sümbol, False)
        return Käivita_2

    def kest(Tekst): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMSi_saatmine(Tekst+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, vertikaal_ametikoht, 눌림): kauge_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikaal_ametikoht))

    def klõps_VALUE(가로, vertikaal_ametikoht): 가리키기(가로, vertikaal_ametikoht, 1); 가리키기(가로, vertikaal_ametikoht, 0)

    def bittraster_pilt():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 tegelik_andmed 너비를 쓴다.
        kauge_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        joonis_VALUE = Image.new('RGB', (너비, 높이)); ala_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(kauge_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(kauge_VALUE, 7)[3:])[0]; EXACT_VALUE(kauge_VALUE, 길이); continue
            assert 종류 == 0, 종류
            kaup_COUNT = struct.unpack('>H', EXACT_VALUE(kauge_VALUE, 3)[1:])[0]
            for _ in range(kaup_COUNT):
                가로, vertikaal_ametikoht, 폭, 길이, kodeerimine_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(kauge_VALUE, 12))
                assert kodeerimine_VALUE == 0 and 가로+폭 <= 너비 and vertikaal_ametikoht+길이 <= 높이
                joonis_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(kauge_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, vertikaal_ametikoht))
                ala_VALUE_9285603e += 폭*길이
            if ala_VALUE_9285603e:
                assert ala_VALUE_9285603e == 너비*높이, ala_VALUE_9285603e
                return joonis_VALUE

    def tšekk_piksel(좌표, 색):
        tähtaeg_VALUE = time.monotonic()+10
        while True:
            joonis_VALUE = bittraster_pilt()
            if joonis_VALUE.getpixel(좌표) == 색: return joonis_VALUE
            if time.monotonic() > tähtaeg_VALUE: raise AssertionError((좌표, joonis_VALUE.getpixel(좌표), 색))

    def Upload_Failid(Nimi_2, andmed): Edasta_VALUE.storbinary('STOR '+Nimi_2, io.BytesIO(andmed))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+suurust_muutma_SMS+' RGB32').encode() in LOG_kirje
        print('BOOT:', suurust_muutma_SMS, flush=True)
        kauge_number = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_kirje).group(1))
        kauge_VALUE = socket.create_connection(('127.0.0.1', kauge_number), timeout=20)
        assert EXACT_VALUE(kauge_VALUE, 12) == b'RFB 003.008\n'; kauge_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(kauge_VALUE, EXACT_VALUE(kauge_VALUE, 1)[0]); kauge_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(kauge_VALUE, 4) == b'\0'*4; kauge_VALUE.sendall(b'\x01')
        lähteolek = EXACT_VALUE(kauge_VALUE, 24); assert struct.unpack('>HH', lähteolek[:4]) == (너비, 높이)
        EXACT_VALUE(kauge_VALUE, struct.unpack('>I', lähteolek[20:])[0])
        kauge_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        kauge_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        tšekk_piksel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        tšekk_piksel((너비-568, 높이-360), (32, 80, 144))
        Käivita_2 = len(LOG_kirje); klõps_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Käivita_2)
        tšekk_piksel((너비-568, 높이-360), (24, 32, 48))
        Käivita_2 = len(LOG_kirje); klõps_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Käivita_2)
        kest('ftpd start')
        Edasta_VALUE = ftplib.FTP(); Edasta_VALUE.encoding = 'utf-8'; Edasta_VALUE.connect('127.0.0.1', pordinumber, timeout=20); Edasta_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·klipp 밖·빈 사각형을 포함한다.
        ALLIKAS = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(Joonista_ristkülik(너비,높이,0,0,0)) return 2;
    if(Joonista_ristkülik(너비,높이-1,1,1,0)!=-22) return 3;
    if(Joonista_ristkülik(너비-1,높이,1,1,0)!=-22) return 4;
    if(Joonista_ristkülik(-1,0,1,1,0)!=-22) return 5;
    if(Joonista_ristkülik(0,0,-1,1,0)!=-22) return 6;
    if(Joonista_ristkülik(너비-1,높이-1,1,1,0x332211)) return 7;
    kirjutamine_Fail_andmed(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Failid('화면시험.c', ALLIKAS.encode())
        assert 'exit 0' in kest('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMSi_saatmine('run /화면시험\n'))
        tšekk_piksel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMSi_saatmine('q'))
        ALLIKAS = '''from Eesti import 화면크기, Joonista_ristkülik, 그림기다리기, Väljund, süsteem_tõrge
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    Joonista_ristkülik(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except süsteem_tõrge as VIGA:
    assert VIGA.INDEX == 22
Joonista_ristkülik(너비-1, 높이-1, 1, 1, 0x665544)
Väljund("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Failid('화면시험.py', ALLIKAS.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMSi_saatmine('python /화면시험.py\n'))
        tšekk_piksel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMSi_saatmine('q'))
        ALLIKAS = '''import Eesti.oma.*;
public class 해상도시험 {
    public static void main(String[] Argumendid) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Olek_erand("Suurus");
        try { 화면.ristkülik(너비,높이-1,1,1,0); throw new Olek_erand("klipp"); }
        catch (kehtetu_argument_erand VIGA) { }
        화면.kustutama_kirje(0x302018);
        화면.ristkülik(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # erand 처리는 host javac 결과를 oma JVM에 올려 검사한다.
        경계원문 = näitaja_tee/'해상도경계시험.java'
        경계원문.write_text(ALLIKAS.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_juur/'dist/jkoros-native-korean.jar'), '-d', str(näitaja_tee), str(경계원문)])
        Upload_Failid('해상도경계시험.class', (näitaja_tee/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMSi_saatmine('java 해상도경계시험\n'))
        tšekk_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMSi_saatmine('q'))
        # 게스트 javac의 tugi_VALUE 문법으로 Suurus päring_VALUE·kustutama_kirje·다섯 Argumendid 그리기를 컴파일한다.
        ALLIKAS = '''public class 해상도시험 {
    public static void main(String[] Argumendid) {
        int 너비=Eesti.oma.화면.너비();
        int 높이=Eesti.oma.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Eesti.oma.화면.kustutama_kirje(3153944);
        Eesti.oma.화면.ristkülik(너비-1,높이-1,1,1,10061943);
        Eesti.oma.Väljund.kirjutamine_liin("JAVA RESOLUTION PASS");
        Eesti.oma.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Failid('해상도시험.java', ALLIKAS.encode())
        TULEMUS = kest('javac 해상도시험.java'); assert 'exit 0' in TULEMUS, TULEMUS
        기다리기(b'JAVA RESOLUTION PASS', SMSi_saatmine('java 해상도시험\n'))
        tšekk_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMSi_saatmine('q'))
        Upload_Failid('스윙시험.class', (näitaja_tee/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMSi_saatmine('java 스윙시험\n'))
        가로, vertikaal_ametikoht = (너비-400)//2, (높이-280)//2
        joonis_VALUE = tšekk_piksel((가로, vertikaal_ametikoht), (32, 80, 144))
        joonis_VALUE.save(str(näitaja_tee/(suurust_muutma_SMS+'.png')))
        Käivita_2 = len(LOG_kirje); klõps_VALUE(가로+80, vertikaal_ametikoht+155)
        기다리기('SWING CLICK Nimi_2'.encode(), Käivita_2)
        Käivita_2 = len(LOG_kirje); klõps_VALUE(가로+385, vertikaal_ametikoht+15); 기다리기(b'jkoros-native> ', Käivita_2)
        assert 'AFTER_RESOLUTION' in kest('echo AFTER_RESOLUTION')
        print('PASS:', suurust_muutma_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Edasta_VALUE: Edasta_VALUE.close()
        if kauge_VALUE: kauge_VALUE.close()
        if Joonis_VALUE.poll() is None:
            Joonis_VALUE.terminate()
            try: Joonis_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Joonis_VALUE.kill(); Joonis_VALUE.wait()
        valija_a916db4e.close(); Joonis_VALUE.stdout.close()
        (näitaja_tee/(suurust_muutma_SMS+'.log')).write_bytes(LOG_kirje)


def Käivita_2():
    näitaja_tee = Project_juur/'build/verification/resolution'; näitaja_tee.mkdir(parents=True, exist_ok=True)
    LOG_kirje = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for kehtetu_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            TULEMUS = subprocess.run(['python3', str(Project_juur/'Tööriistad/Täida_käsk.py'), '--resolution', kehtetu_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert TULEMUS.returncode == 2 and b'--resolution' in TULEMUS.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(näitaja_tee), str(Project_juur/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, näitaja_tee); LOG_kirje['resolutions'].append([너비, 높이])
        LOG_kirje.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (näitaja_tee/'report.json').write_text(json.dumps(LOG_kirje, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Käivita_2()
