#!/usr/bin/env python3
"""tatsächlichDaten QEMU/VNC에서 Bildschirm größe·grenzstelleWert·fenster bewegenWert·Swing·언어별 그리기를 검사한다."""
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
from arbeitsflächeAnsicht import exaktWert
from befehlAusführen import projektWurzel


def AuflösungPrüfung(breiteWert, höheWert, ergebnisPfad):
    with socket.socket() as vorläufigWert:
        vorläufigWert.bind(('127.0.0.1', 0)); portNummer = vorläufigWert.getsockname()[1]
    größeText = '{}x{}'.format(breiteWert, höheWert)
    prozessWert = subprocess.Popen(['python3', str(projektWurzel/'Werkzeuge/befehlAusführen.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portNummer), '--resolution', größeText], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Auswähler = selectors.DefaultSelector(); Auswähler.register(prozessWert.stdout, selectors.EVENT_READ)
    protokolldateiAufzeichnung = bytearray(); entferntWert = None; übertragungWert = None

    def abwarten(wertAnzeigen, ausführenVorgang=0):
        fristWert = time.monotonic() + 60
        while wertAnzeigen not in protokolldateiAufzeichnung[ausführenVorgang:]:
            if time.monotonic() > fristWert or prozessWert.poll() is not None or b'HALTED' in protokolldateiAufzeichnung or b'PANIC:' in protokolldateiAufzeichnung:
                raise AssertionError(protokolldateiAufzeichnung[ausführenVorgang:].decode('utf-8', 'replace'))
            for ereignis, _ in Auswähler.select(.1):
                Daten = ereignis.fileobj.read(65536)
                if Daten: protokolldateiAufzeichnung.extend(Daten)
        return protokolldateiAufzeichnung[ausführenVorgang:].decode('utf-8', 'replace')

    def klickenSchaltfläche(symbol, istGedrückt=True): entferntWert.sendall(struct.pack('>BBHI', 4, int(istGedrückt), 0, symbol))

    def textSenden(Text):
        ausführenVorgang = len(protokolldateiAufzeichnung)
        for zeichenWert in Text:
            symbol = 0xff0d if zeichenWert == '\n' else ord(zeichenWert) if ord(zeichenWert) < 256 else 0x1000000 | ord(zeichenWert)
            klickenSchaltfläche(symbol); klickenSchaltfläche(symbol, False)
        return ausführenVorgang

    def befehlshülle(Text): return abwarten(b'\r\n__RESOLUTION_DONE__\r\n', textSenden(Text+'; echo __RESOLUTION_DONE__\n'))

    def punktAnStelle(waagerechtPosition, senkrechtPosition, istGedrückt): entferntWert.sendall(struct.pack('>BBHH', 5, istGedrückt, waagerechtPosition, senkrechtPosition))

    def klickenWert(waagerechtPosition, senkrechtPosition): punktAnStelle(waagerechtPosition, senkrechtPosition, 1); punktAnStelle(waagerechtPosition, senkrechtPosition, 0)

    def bitkarteAbbild():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 tatsächlichDaten 너비를 쓴다.
        entferntWert.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, breiteWert, höheWert))
        Zeichnung = Image.new('RGB', (breiteWert, höheWert)); flächeWert = 0
        while True:
            artWert = exaktWert(entferntWert, 1)[0]
            if artWert == 2: continue
            if artWert == 3:
                Länge = struct.unpack('>I', exaktWert(entferntWert, 7)[3:])[0]; exaktWert(entferntWert, Länge); continue
            assert artWert == 0, artWert
            elementeintragAnzahl = struct.unpack('>H', exaktWert(entferntWert, 3)[1:])[0]
            for _ in range(elementeintragAnzahl):
                waagerechtPosition, senkrechtPosition, breiteSpannweite, Länge, kodierungWert = struct.unpack('>HHHHi', exaktWert(entferntWert, 12))
                assert kodierungWert == 0 and waagerechtPosition+breiteSpannweite <= breiteWert and senkrechtPosition+Länge <= höheWert
                Zeichnung.paste(Image.frombytes('RGB', (breiteSpannweite, Länge), exaktWert(entferntWert, breiteSpannweite*Länge*4), 'raw', 'BGRX'), (waagerechtPosition, senkrechtPosition))
                flächeWert += breiteSpannweite*Länge
            if flächeWert:
                assert flächeWert == breiteWert*höheWert, flächeWert
                return Zeichnung

    def bildpunktPrüfen(koordinateWert, farbeWert):
        fristWert = time.monotonic()+10
        while True:
            Zeichnung = bitkarteAbbild()
            if Zeichnung.getpixel(koordinateWert) == farbeWert: return Zeichnung
            if time.monotonic() > fristWert: raise AssertionError((koordinateWert, Zeichnung.getpixel(koordinateWert), farbeWert))

    def hochladenDateien(Name, Daten): übertragungWert.storbinary('STOR '+Name, io.BytesIO(Daten))

    try:
        abwarten(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+größeText+' RGB32').encode() in protokolldateiAufzeichnung
        print('BOOT:', größeText, flush=True)
        entferntNummer = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', protokolldateiAufzeichnung).group(1))
        entferntWert = socket.create_connection(('127.0.0.1', entferntNummer), timeout=20)
        assert exaktWert(entferntWert, 12) == b'RFB 003.008\n'; entferntWert.sendall(b'RFB 003.008\n')
        assert 1 in exaktWert(entferntWert, exaktWert(entferntWert, 1)[0]); entferntWert.sendall(b'\x01')
        assert exaktWert(entferntWert, 4) == b'\0'*4; entferntWert.sendall(b'\x01')
        anfänglichStatuswert = exaktWert(entferntWert, 24); assert struct.unpack('>HH', anfänglichStatuswert[:4]) == (breiteWert, höheWert)
        exaktWert(entferntWert, struct.unpack('>I', anfänglichStatuswert[20:])[0])
        entferntWert.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        entferntWert.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        bildpunktPrüfen((breiteWert-1, höheWert-1), (24, 32, 48))
        # Bildschirm rechts 아래까지 이동한다. vorherigElementeintrag 640×480 grenzstelleWert 밖에서 X를 누른다.
        punktAnStelle(40, 60, 1); punktAnStelle(breiteWert-568+28, höheWert-360+12, 1); punktAnStelle(breiteWert-568+28, höheWert-360+12, 0)
        bildpunktPrüfen((breiteWert-568, höheWert-360), (32, 80, 144))
        ausführenVorgang = len(protokolldateiAufzeichnung); klickenWert(breiteWert-20, höheWert-345); abwarten(b'TERMINAL FOCUS 1', ausführenVorgang)
        bildpunktPrüfen((breiteWert-568, höheWert-360), (24, 32, 48))
        ausführenVorgang = len(protokolldateiAufzeichnung); klickenWert(80, 16); abwarten(b'TERMINAL FOCUS 1', ausführenVorgang)
        befehlshülle('ftpd start')
        übertragungWert = ftplib.FTP(); übertragungWert.encoding = 'utf-8'; übertragungWert.connect('127.0.0.1', portNummer, timeout=20); übertragungWert.login()
        # C grenzstelleWert 검사는 32비트 unsigned negativWert wertUmwandeln·beschneiden 밖·빈 사각형을 포함한다.
        Quelltext = '''#include <BildschirmABI.h>
#include <DateiABI.h>
int main(void) {
    unsigned breiteWert=bildschirmBreite(), höheWert=bildschirmHöhe();
    if(breiteWert!=WIDTH || höheWert!=HEIGHT) return 1;
    if(rechteckZeichnen(breiteWert,höheWert,0,0,0)) return 2;
    if(rechteckZeichnen(breiteWert,höheWert-1,1,1,0)!=-22) return 3;
    if(rechteckZeichnen(breiteWert-1,höheWert,1,1,0)!=-22) return 4;
    if(rechteckZeichnen(-1,0,1,1,0)!=-22) return 5;
    if(rechteckZeichnen(0,0,-1,1,0)!=-22) return 6;
    if(rechteckZeichnen(breiteWert-1,höheWert-1,1,1,0x332211)) return 7;
    dateiDatenSchreiben(1,"C RESOLUTION PASS\\n",18);
    fürZeichnungWarten(); return 0;
}
'''.replace('WIDTH', str(breiteWert)).replace('HEIGHT', str(höheWert))
        hochladenDateien('bildschirmPrüfung.c', Quelltext.encode())
        assert 'exit 0' in befehlshülle('cc /bildschirmPrüfung.c -o /bildschirmPrüfung')
        abwarten(b'C RESOLUTION PASS', textSenden('run /bildschirmPrüfung\n'))
        bildpunktPrüfen((breiteWert-1, höheWert-1), (17, 34, 51))
        abwarten(b'jkoros-native> ', textSenden('q'))
        Quelltext = '''from Deutsch import bildschirmGröße, rechteckZeichnen, fürZeichnungWarten, Ausgabe, SystemFehler
breiteWert, höheWert = bildschirmGröße()
assert (breiteWert, höheWert) == (WIDTH, HEIGHT)
try:
    rechteckZeichnen(breiteWert, höheWert-1, 1, 1, 0)
    raise AssertionError("boundary")
except SystemFehler as fehler:
    assert fehler.Nummer == 22
rechteckZeichnen(breiteWert-1, höheWert-1, 1, 1, 0x665544)
Ausgabe("PYTHON RESOLUTION PASS")
fürZeichnungWarten()
'''.replace('WIDTH', str(breiteWert)).replace('HEIGHT', str(höheWert))
        hochladenDateien('bildschirmPrüfung.py', Quelltext.encode())
        abwarten(b'PYTHON RESOLUTION PASS', textSenden('python /bildschirmPrüfung.py\n'))
        bildpunktPrüfen((breiteWert-1, höheWert-1), (68, 85, 102))
        abwarten(b'jkoros-native> ', textSenden('q'))
        Quelltext = '''import Deutsch.eigen.*;
public class AuflösungPrüfung {
    public static void main(String[] argumente) {
        int breiteWert=Bildschirm.breiteWert(), höheWert=Bildschirm.höheWert();
        if (breiteWert!=WIDTH || höheWert!=HEIGHT) throw new StatuswertAusnahme("größe");
        try { Bildschirm.rechteck(breiteWert,höheWert-1,1,1,0); throw new StatuswertAusnahme("beschneiden"); }
        catch (UngültigArgumentAusnahme fehler) { }
        Bildschirm.eintragTilgen(0x302018);
        Bildschirm.rechteck(breiteWert-1,höheWert-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        Bildschirm.abwarten();
    }
}
'''.replace('WIDTH', str(breiteWert)).replace('HEIGHT', str(höheWert))
        # ausnahme 처리는 Wirtssystem javac 결과를 eigen JVM에 올려 검사한다.
        grenzstelleQuelltext = ergebnisPfad/'해상도경계시험.java'
        grenzstelleQuelltext.write_text(Quelltext.replace('class AuflösungPrüfung', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projektWurzel/'dist/jkoros-native-korean.jar'), '-d', str(ergebnisPfad), str(grenzstelleQuelltext)])
        hochladenDateien('해상도경계시험.class', (ergebnisPfad/'해상도경계시험.class').read_bytes())
        abwarten(b'JAVA RESOLUTION PASS', textSenden('java 해상도경계시험\n'))
        bildpunktPrüfen((breiteWert-1, höheWert-1), (119, 136, 153))
        abwarten(b'jkoros-native> ', textSenden('q'))
        # 게스트 javac의 unterstützungWert 문법으로 größe abfragenWert·eintragTilgen·다섯 argumente 그리기를 컴파일한다.
        Quelltext = '''public class AuflösungPrüfung {
    public static void main(String[] argumente) {
        int breiteWert=Deutsch.eigen.Bildschirm.breiteWert();
        int höheWert=Deutsch.eigen.Bildschirm.höheWert();
        if (breiteWert!=WIDTH || höheWert!=HEIGHT) return;
        Deutsch.eigen.Bildschirm.eintragTilgen(3153944);
        Deutsch.eigen.Bildschirm.rechteck(breiteWert-1,höheWert-1,1,1,10061943);
        Deutsch.eigen.Ausgabe.zeileSchreiben("JAVA RESOLUTION PASS");
        Deutsch.eigen.Bildschirm.abwarten();
    }
}
'''.replace('WIDTH', str(breiteWert)).replace('HEIGHT', str(höheWert))
        hochladenDateien('AuflösungPrüfung.java', Quelltext.encode())
        ergebnis = befehlshülle('javac AuflösungPrüfung.java'); assert 'exit 0' in ergebnis, ergebnis
        abwarten(b'JAVA RESOLUTION PASS', textSenden('java AuflösungPrüfung\n'))
        bildpunktPrüfen((breiteWert-1, höheWert-1), (119, 136, 153))
        abwarten(b'jkoros-native> ', textSenden('q'))
        hochladenDateien('SwingPrüfung.class', (ergebnisPfad/'SwingPrüfung.class').read_bytes())
        abwarten(b'SWING READY', textSenden('java SwingPrüfung\n'))
        waagerechtPosition, senkrechtPosition = (breiteWert-400)//2, (höheWert-280)//2
        Zeichnung = bildpunktPrüfen((waagerechtPosition, senkrechtPosition), (32, 80, 144))
        Zeichnung.save(str(ergebnisPfad/(größeText+'.png')))
        ausführenVorgang = len(protokolldateiAufzeichnung); klickenWert(waagerechtPosition+80, senkrechtPosition+155)
        abwarten('SWING CLICK Name'.encode(), ausführenVorgang)
        ausführenVorgang = len(protokolldateiAufzeichnung); klickenWert(waagerechtPosition+385, senkrechtPosition+15); abwarten(b'jkoros-native> ', ausführenVorgang)
        assert 'AFTER_RESOLUTION' in befehlshülle('echo AFTER_RESOLUTION')
        print('PASS:', größeText, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if übertragungWert: übertragungWert.close()
        if entferntWert: entferntWert.close()
        if prozessWert.poll() is None:
            prozessWert.terminate()
            try: prozessWert.wait(timeout=8)
            except subprocess.TimeoutExpired: prozessWert.kill(); prozessWert.wait()
        Auswähler.close(); prozessWert.stdout.close()
        (ergebnisPfad/(größeText+'.log')).write_bytes(protokolldateiAufzeichnung)


def ausführenVorgang():
    ergebnisPfad = projektWurzel/'build/verification/resolution'; ergebnisPfad.mkdir(parents=True, exist_ok=True)
    protokolldateiAufzeichnung = {'passed': False, 'kernel_sha256': hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ungültigWert in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ergebnis = subprocess.run(['python3', str(projektWurzel/'Werkzeuge/befehlAusführen.py'), '--resolution', ungültigWert], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ergebnis.returncode == 2 and b'--resolution' in ergebnis.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ergebnisPfad), str(projektWurzel/'Prüfungen/Java/SwingPrüfung.java')])
        for breiteWert, höheWert in ((1920,1080), (1280,720), (640,480)):
            AuflösungPrüfung(breiteWert, höheWert, ergebnisPfad); protokolldateiAufzeichnung['resolutions'].append([breiteWert, höheWert])
        protokolldateiAufzeichnung.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (ergebnisPfad/'report.json').write_text(json.dumps(protokolldateiAufzeichnung, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ausführenVorgang()
