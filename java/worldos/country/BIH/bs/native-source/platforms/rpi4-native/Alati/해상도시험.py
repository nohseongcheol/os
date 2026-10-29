#!/usr/bin/env python3
"""stvaran_podaci QEMU/VNC에서 화면 Veličina·경계·prozor pomaći_VALUE·Swing·언어별 그리기를 검사한다."""
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
from Izvrši_komanda import projicirati_koijen


def 해상도시험(너비, 높이, mjera_put):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); broj_priključka = 임시.getsockname()[1]
    podesiti_veličinu_SMS = '{}x{}'.format(너비, 높이)
    proces_VALUE = subprocess.Popen(['python3', str(projicirati_koijen/'Alati/Izvrši_komanda.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(broj_priključka), '--resolution', podesiti_veličinu_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    birač_a916db4e = selectors.DefaultSelector(); birač_a916db4e.register(proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_red = bytearray(); udaljeno_VALUE = None; prijenos_VALUE = None

    def 기다리기(program_VALUE, Pokreni=0):
        마감 = time.monotonic() + 60
        while program_VALUE not in LOG_red[Pokreni:]:
            if time.monotonic() > 마감 or proces_VALUE.poll() is not None or b'HALTED' in LOG_red or b'PANIC:' in LOG_red:
                raise AssertionError(LOG_red[Pokreni:].decode('utf-8', 'replace'))
            for događaj, _ in birač_a916db4e.select(.1):
                podaci = događaj.fileobj.read(65536)
                if podaci: LOG_red.extend(podaci)
        return LOG_red[Pokreni:].decode('utf-8', 'replace')

    def klik_dugme(simbol, 눌림=True): udaljeno_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def slati_SMS(Tekst):
        Pokreni = len(LOG_red)
        for znak_VALUE in Tekst:
            simbol = 0xff0d if znak_VALUE == '\n' else ord(znak_VALUE) if ord(znak_VALUE) < 256 else 0x1000000 | ord(znak_VALUE)
            klik_dugme(simbol); klik_dugme(simbol, False)
        return Pokreni

    def ljuska(Tekst): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', slati_SMS(Tekst+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Vertikalno_položaj, 눌림): udaljeno_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikalno_položaj))

    def klik_VALUE(가로, Vertikalno_položaj): 가리키기(가로, Vertikalno_položaj, 1); 가리키기(가로, Vertikalno_položaj, 0)

    def rasterska_slika_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 stvaran_podaci 너비를 쓴다.
        udaljeno_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ucrtavanje_VALUE = Image.new('RGB', (너비, 높이)); oblast_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(udaljeno_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                dužina_VALUE = struct.unpack('>I', EXACT_VALUE(udaljeno_VALUE, 7)[3:])[0]; EXACT_VALUE(udaljeno_VALUE, dužina_VALUE); continue
            assert 종류 == 0, 종류
            stavka_COUNT = struct.unpack('>H', EXACT_VALUE(udaljeno_VALUE, 3)[1:])[0]
            for _ in range(stavka_COUNT):
                가로, Vertikalno_položaj, 폭, dužina_VALUE, kodiranje_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(udaljeno_VALUE, 12))
                assert kodiranje_VALUE == 0 and 가로+폭 <= 너비 and Vertikalno_položaj+dužina_VALUE <= 높이
                ucrtavanje_VALUE.paste(Image.frombytes('RGB', (폭, dužina_VALUE), EXACT_VALUE(udaljeno_VALUE, 폭*dužina_VALUE*4), 'raw', 'BGRX'), (가로, Vertikalno_položaj))
                oblast_VALUE_9285603e += 폭*dužina_VALUE
            if oblast_VALUE_9285603e:
                assert oblast_VALUE_9285603e == 너비*높이, oblast_VALUE_9285603e
                return ucrtavanje_VALUE

    def ček_pel(koordinata_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            ucrtavanje_VALUE = rasterska_slika_IMAGE()
            if ucrtavanje_VALUE.getpixel(koordinata_VALUE) == 색: return ucrtavanje_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinata_VALUE, ucrtavanje_VALUE.getpixel(koordinata_VALUE), 색))

    def Upload_Fajlovi(Naziv, podaci): prijenos_VALUE.storbinary('STOR '+Naziv, io.BytesIO(podaci))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+podesiti_veličinu_SMS+' RGB32').encode() in LOG_red
        print('BOOT:', podesiti_veličinu_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_red).group(1))
        udaljeno_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(udaljeno_VALUE, 12) == b'RFB 003.008\n'; udaljeno_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(udaljeno_VALUE, EXACT_VALUE(udaljeno_VALUE, 1)[0]); udaljeno_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(udaljeno_VALUE, 4) == b'\0'*4; udaljeno_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(udaljeno_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(udaljeno_VALUE, struct.unpack('>I', 초기[20:])[0])
        udaljeno_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        udaljeno_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ček_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ček_pel((너비-568, 높이-360), (32, 80, 144))
        Pokreni = len(LOG_red); klik_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Pokreni)
        ček_pel((너비-568, 높이-360), (24, 32, 48))
        Pokreni = len(LOG_red); klik_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Pokreni)
        ljuska('ftpd start')
        prijenos_VALUE = ftplib.FTP(); prijenos_VALUE.encoding = 'utf-8'; prijenos_VALUE.connect('127.0.0.1', broj_priključka, timeout=20); prijenos_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·isječak 밖·빈 사각형을 포함한다.
        IZVOR = '''#include <화면규약.h>
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
    pisati_fajl_podaci(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fajlovi('화면시험.c', IZVOR.encode())
        assert 'exit 0' in ljuska('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', slati_SMS('run /화면시험\n'))
        ček_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', slati_SMS('q'))
        IZVOR = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, Ispis, sistem_greška
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistem_greška as GRESKA:
    assert GRESKA.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Ispis("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fajlovi('화면시험.py', IZVOR.encode())
        기다리기(b'PYTHON RESOLUTION PASS', slati_SMS('python /화면시험.py\n'))
        ček_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', slati_SMS('q'))
        IZVOR = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] Argumenti) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new stanje_izuzetak("Veličina");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new stanje_izuzetak("isječak"); }
        catch (nevažeće_argument_izuzetak GRESKA) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # izuzetak 처리는 organizator javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = mjera_put/'해상도경계시험.java'
        경계원문.write_text(IZVOR.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projicirati_koijen/'dist/jkoros-native-korean.jar'), '-d', str(mjera_put), str(경계원문)])
        Upload_Fajlovi('해상도경계시험.class', (mjera_put/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', slati_SMS('java 해상도경계시험\n'))
        ček_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', slati_SMS('q'))
        # 게스트 javac의 Podrška_VALUE 문법으로 Veličina upit_VALUE·지우기·다섯 Argumenti 그리기를 컴파일한다.
        IZVOR = '''public class 해상도시험 {
    public static void main(String[] Argumenti) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.Ispis.pisati_redak("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fajlovi('해상도시험.java', IZVOR.encode())
        mjera = ljuska('javac 해상도시험.java'); assert 'exit 0' in mjera, mjera
        기다리기(b'JAVA RESOLUTION PASS', slati_SMS('java 해상도시험\n'))
        ček_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', slati_SMS('q'))
        Upload_Fajlovi('스윙시험.class', (mjera_put/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', slati_SMS('java 스윙시험\n'))
        가로, Vertikalno_položaj = (너비-400)//2, (높이-280)//2
        ucrtavanje_VALUE = ček_pel((가로, Vertikalno_položaj), (32, 80, 144))
        ucrtavanje_VALUE.save(str(mjera_put/(podesiti_veličinu_SMS+'.png')))
        Pokreni = len(LOG_red); klik_VALUE(가로+80, Vertikalno_položaj+155)
        기다리기('SWING CLICK Naziv'.encode(), Pokreni)
        Pokreni = len(LOG_red); klik_VALUE(가로+385, Vertikalno_položaj+15); 기다리기(b'jkoros-native> ', Pokreni)
        assert 'AFTER_RESOLUTION' in ljuska('echo AFTER_RESOLUTION')
        print('PASS:', podesiti_veličinu_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if prijenos_VALUE: prijenos_VALUE.close()
        if udaljeno_VALUE: udaljeno_VALUE.close()
        if proces_VALUE.poll() is None:
            proces_VALUE.terminate()
            try: proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: proces_VALUE.kill(); proces_VALUE.wait()
        birač_a916db4e.close(); proces_VALUE.stdout.close()
        (mjera_put/(podesiti_veličinu_SMS+'.log')).write_bytes(LOG_red)


def Pokreni():
    mjera_put = projicirati_koijen/'build/verification/resolution'; mjera_put.mkdir(parents=True, exist_ok=True)
    LOG_red = {'passed': False, 'kernel_sha256': hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for nevažeće_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            mjera = subprocess.run(['python3', str(projicirati_koijen/'Alati/Izvrši_komanda.py'), '--resolution', nevažeće_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert mjera.returncode == 2 and b'--resolution' in mjera.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(mjera_put), str(projicirati_koijen/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, mjera_put); LOG_red['resolutions'].append([너비, 높이])
        LOG_red.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (mjera_put/'report.json').write_text(json.dumps(LOG_red, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Pokreni()
