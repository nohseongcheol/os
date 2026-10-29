#!/usr/bin/env python3
"""todellinen_data QEMU/VNC에서 화면 Koko·rajattu_alue_ARVO·Ikkuna siirrä_ARVO_83b651b8·Swing·언어별 그리기를 검사한다."""
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
from työpöytä_Näkymä import VERTAA_ARVO
from Suorita_komento import aloite_juuri


def tarkkuus_testi(너비, 높이, KR_polku):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); portin_numero = 임시.getsockname()[1]
    muuttaa_kokoa_SMS = '{}x{}'.format(너비, 높이)
    prosessi_ARVO = subprocess.Popen(['python3', str(aloite_juuri/'työkalut/Suorita_komento.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portin_numero), '--resolution', muuttaa_kokoa_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    valitsin_a916db4e = selectors.DefaultSelector(); valitsin_a916db4e.register(prosessi_ARVO.stdout, selectors.EVENT_READ)
    LOG_TIETUE = bytearray(); etä_ARVO = None; Siirrä_ARVO = None

    def 기다리기(näyttää_ARVO, Suorita_2=0):
        määräaika_ARVO = time.monotonic() + 60
        while näyttää_ARVO not in LOG_TIETUE[Suorita_2:]:
            if time.monotonic() > määräaika_ARVO or prosessi_ARVO.poll() is not None or b'HALTED' in LOG_TIETUE or b'PANIC:' in LOG_TIETUE:
                raise AssertionError(LOG_TIETUE[Suorita_2:].decode('utf-8', 'replace'))
            for Tapahtuma, _ in valitsin_a916db4e.select(.1):
                data = Tapahtuma.fileobj.read(65536)
                if data: LOG_TIETUE.extend(data)
        return LOG_TIETUE[Suorita_2:].decode('utf-8', 'replace')

    def osoittaa_painike(symboli, 눌림=True): etä_ARVO.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symboli))

    def lähettää_tekstiviesti(teksti):
        Suorita_2 = len(LOG_TIETUE)
        for merkki_ARVO in teksti:
            symboli = 0xff0d if merkki_ARVO == '\n' else ord(merkki_ARVO) if ord(merkki_ARVO) < 256 else 0x1000000 | ord(merkki_ARVO)
            osoittaa_painike(symboli); osoittaa_painike(symboli, False)
        return Suorita_2

    def liittymä(teksti): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', lähettää_tekstiviesti(teksti+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, toimiala_toimi, 눌림): etä_ARVO.sendall(struct.pack('>BBHH', 5, 눌림, 가로, toimiala_toimi))

    def osoittaa_ARVO(가로, toimiala_toimi): 가리키기(가로, toimiala_toimi, 1); 가리키기(가로, toimiala_toimi, 0)

    def bittikartta_KUVA():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 todellinen_data 너비를 쓴다.
        etä_ARVO.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        piirustus_ARVO = Image.new('RGB', (너비, 높이)); alue_ARVO_9285603e = 0
        while True:
            종류 = VERTAA_ARVO(etä_ARVO, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                kesto_ARVO = struct.unpack('>I', VERTAA_ARVO(etä_ARVO, 7)[3:])[0]; VERTAA_ARVO(etä_ARVO, kesto_ARVO); continue
            assert 종류 == 0, 종류
            kohde_LASKE = struct.unpack('>H', VERTAA_ARVO(etä_ARVO, 3)[1:])[0]
            for _ in range(kohde_LASKE):
                가로, toimiala_toimi, 폭, kesto_ARVO, koodaus_ARVO = struct.unpack('>HHHHi', VERTAA_ARVO(etä_ARVO, 12))
                assert koodaus_ARVO == 0 and 가로+폭 <= 너비 and toimiala_toimi+kesto_ARVO <= 높이
                piirustus_ARVO.paste(Image.frombytes('RGB', (폭, kesto_ARVO), VERTAA_ARVO(etä_ARVO, 폭*kesto_ARVO*4), 'raw', 'BGRX'), (가로, toimiala_toimi))
                alue_ARVO_9285603e += 폭*kesto_ARVO
            if alue_ARVO_9285603e:
                assert alue_ARVO_9285603e == 너비*높이, alue_ARVO_9285603e
                return piirustus_ARVO

    def sekki_kuvapiste(koordinaatti_ARVO, 색):
        määräaika_ARVO = time.monotonic()+10
        while True:
            piirustus_ARVO = bittikartta_KUVA()
            if piirustus_ARVO.getpixel(koordinaatti_ARVO) == 색: return piirustus_ARVO
            if time.monotonic() > määräaika_ARVO: raise AssertionError((koordinaatti_ARVO, piirustus_ARVO.getpixel(koordinaatti_ARVO), 색))

    def Upload_Files(Nimi, data): Siirrä_ARVO.storbinary('STOR '+Nimi, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+muuttaa_kokoa_SMS+' RGB32').encode() in LOG_TIETUE
        print('BOOT:', muuttaa_kokoa_SMS, flush=True)
        etä_numero = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_TIETUE).group(1))
        etä_ARVO = socket.create_connection(('127.0.0.1', etä_numero), timeout=20)
        assert VERTAA_ARVO(etä_ARVO, 12) == b'RFB 003.008\n'; etä_ARVO.sendall(b'RFB 003.008\n')
        assert 1 in VERTAA_ARVO(etä_ARVO, VERTAA_ARVO(etä_ARVO, 1)[0]); etä_ARVO.sendall(b'\x01')
        assert VERTAA_ARVO(etä_ARVO, 4) == b'\0'*4; etä_ARVO.sendall(b'\x01')
        alkutila = VERTAA_ARVO(etä_ARVO, 24); assert struct.unpack('>HH', alkutila[:4]) == (너비, 높이)
        VERTAA_ARVO(etä_ARVO, struct.unpack('>I', alkutila[20:])[0])
        etä_ARVO.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        etä_ARVO.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        sekki_kuvapiste((너비-1, 높이-1), (24, 32, 48))
        # 화면 OIKEA 아래까지 이동한다. Edellinen_kohde 640×480 rajattu_alue_ARVO 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        sekki_kuvapiste((너비-568, 높이-360), (32, 80, 144))
        Suorita_2 = len(LOG_TIETUE); osoittaa_ARVO(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Suorita_2)
        sekki_kuvapiste((너비-568, 높이-360), (24, 32, 48))
        Suorita_2 = len(LOG_TIETUE); osoittaa_ARVO(80, 16); 기다리기(b'TERMINAL FOCUS 1', Suorita_2)
        liittymä('ftpd start')
        Siirrä_ARVO = ftplib.FTP(); Siirrä_ARVO.encoding = 'utf-8'; Siirrä_ARVO.connect('127.0.0.1', portin_numero, timeout=20); Siirrä_ARVO.login()
        # C rajattu_alue_ARVO 검사는 32비트 unsigned 음수 MUUNNA_ARVO·leikata 밖·빈 사각형을 포함한다.
        lähdetiedosto = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(Piirrä_suorakulmio(너비,높이,0,0,0)) return 2;
    if(Piirrä_suorakulmio(너비,높이-1,1,1,0)!=-22) return 3;
    if(Piirrä_suorakulmio(너비-1,높이,1,1,0)!=-22) return 4;
    if(Piirrä_suorakulmio(-1,0,1,1,0)!=-22) return 5;
    if(Piirrä_suorakulmio(0,0,-1,1,0)!=-22) return 6;
    if(Piirrä_suorakulmio(너비-1,높이-1,1,1,0x332211)) return 7;
    kirjoitus_Tiedosto_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Files('화면시험.c', lähdetiedosto.encode())
        assert 'exit 0' in liittymä('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', lähettää_tekstiviesti('run /화면시험\n'))
        sekki_kuvapiste((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', lähettää_tekstiviesti('q'))
        lähdetiedosto = '''from suomi import 화면크기, Piirrä_suorakulmio, 그림기다리기, tulostuspaikka, järjestelmävirhe
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    Piirrä_suorakulmio(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except järjestelmävirhe as VIRHE:
    assert VIRHE.INDEKSI == 22
Piirrä_suorakulmio(너비-1, 높이-1, 1, 1, 0x665544)
tulostuspaikka("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Files('화면시험.py', lähdetiedosto.encode())
        기다리기(b'PYTHON RESOLUTION PASS', lähettää_tekstiviesti('python /화면시험.py\n'))
        sekki_kuvapiste((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', lähettää_tekstiviesti('q'))
        lähdetiedosto = '''import suomi.oma.*;
public class tarkkuus_testi {
    public static void main(String[] argumentit) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Tila_poikkeus("Koko");
        try { 화면.suorakulmio(너비,높이-1,1,1,0); throw new Tila_poikkeus("leikata"); }
        catch (pätemätön_argumentti_poikkeus VIRHE) { }
        화면.poistaa_merkintä_c8dbc399(0x302018);
        화면.suorakulmio(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # poikkeus 처리는 isäntä javac 결과를 oma JVM에 올려 검사한다.
        rajattu_alue_lähde = KR_polku/'해상도경계시험.java'
        rajattu_alue_lähde.write_text(lähdetiedosto.replace('class tarkkuus_testi', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(aloite_juuri/'dist/jkoros-native-korean.jar'), '-d', str(KR_polku), str(rajattu_alue_lähde)])
        Upload_Files('해상도경계시험.class', (KR_polku/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', lähettää_tekstiviesti('java 해상도경계시험\n'))
        sekki_kuvapiste((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', lähettää_tekstiviesti('q'))
        # 게스트 javac의 Tuki_ARVO 문법으로 Koko kysely_ARVO·poistaa_merkintä_c8dbc399·다섯 argumentit 그리기를 컴파일한다.
        lähdetiedosto = '''public class tarkkuus_testi {
    public static void main(String[] argumentit) {
        int 너비=suomi.oma.화면.너비();
        int 높이=suomi.oma.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        suomi.oma.화면.poistaa_merkintä_c8dbc399(3153944);
        suomi.oma.화면.suorakulmio(너비-1,높이-1,1,1,10061943);
        suomi.oma.tulostuspaikka.kirjoitus_rivi("JAVA RESOLUTION PASS");
        suomi.oma.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Files('tarkkuus_testi.java', lähdetiedosto.encode())
        TULOS = liittymä('javac tarkkuus_testi.java'); assert 'exit 0' in TULOS, TULOS
        기다리기(b'JAVA RESOLUTION PASS', lähettää_tekstiviesti('java tarkkuus_testi\n'))
        sekki_kuvapiste((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', lähettää_tekstiviesti('q'))
        Upload_Files('swing_testi.class', (KR_polku/'swing_testi.class').read_bytes())
        기다리기(b'SWING READY', lähettää_tekstiviesti('java swing_testi\n'))
        가로, toimiala_toimi = (너비-400)//2, (높이-280)//2
        piirustus_ARVO = sekki_kuvapiste((가로, toimiala_toimi), (32, 80, 144))
        piirustus_ARVO.save(str(KR_polku/(muuttaa_kokoa_SMS+'.png')))
        Suorita_2 = len(LOG_TIETUE); osoittaa_ARVO(가로+80, toimiala_toimi+155)
        기다리기('SWING CLICK Nimi'.encode(), Suorita_2)
        Suorita_2 = len(LOG_TIETUE); osoittaa_ARVO(가로+385, toimiala_toimi+15); 기다리기(b'jkoros-native> ', Suorita_2)
        assert 'AFTER_RESOLUTION' in liittymä('echo AFTER_RESOLUTION')
        print('PASS:', muuttaa_kokoa_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Siirrä_ARVO: Siirrä_ARVO.close()
        if etä_ARVO: etä_ARVO.close()
        if prosessi_ARVO.poll() is None:
            prosessi_ARVO.terminate()
            try: prosessi_ARVO.wait(timeout=8)
            except subprocess.TimeoutExpired: prosessi_ARVO.kill(); prosessi_ARVO.wait()
        valitsin_a916db4e.close(); prosessi_ARVO.stdout.close()
        (KR_polku/(muuttaa_kokoa_SMS+'.log')).write_bytes(LOG_TIETUE)


def Suorita_2():
    KR_polku = aloite_juuri/'build/verification/resolution'; KR_polku.mkdir(parents=True, exist_ok=True)
    LOG_TIETUE = {'passed': False, 'kernel_sha256': hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for pätemätön_ARVO in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            TULOS = subprocess.run(['python3', str(aloite_juuri/'työkalut/Suorita_komento.py'), '--resolution', pätemätön_ARVO], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert TULOS.returncode == 2 and b'--resolution' in TULOS.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_polku), str(aloite_juuri/'testit/자바/swing_testi.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            tarkkuus_testi(너비, 높이, KR_polku); LOG_TIETUE['resolutions'].append([너비, 높이])
        LOG_TIETUE.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_polku/'report.json').write_text(json.dumps(LOG_TIETUE, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Suorita_2()
