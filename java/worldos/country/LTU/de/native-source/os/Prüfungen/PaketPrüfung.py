#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

position = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as vorläufigWert:
    verzeichnisWert = Path(vorläufigWert)
    grenzstelleWert = verzeichnisWert / '시험장치.java'
    grenzstelleWert.write_text('''
class Gerät { static int zeitstempelWert; static int millisekunden() { return zeitstempelWert++; } static void kurzzeitigTunAbgeben() {} }
class Zeichenterminal { static void schreiben(String Wert) {} static void nummerSchreiben(int Wert) {} }
class Netzwerktreiber {
    static int einAusgabeBasisAdresse = 1, übertragenAnzahl, anzahlEmpfangen;
    static int[] gerätAdresse = {0x52,0x54,0,0x12,0x34,0x56}, kürzlichWert;
    static int empfangen(int[] Daten) { return 0; }
    static int senden(int[] Daten, int Länge) { kürzlichWert = Daten.clone(); return Länge; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(verzeichnisWert), str(grenzstelleWert),
                    str(position / 'Quelltext/Netzwerkstapel.java'), str(position / 'Prüfungen/PaketPrüfung.java')], check=True)
    subprocess.run(['java', '-cp', str(verzeichnisWert), 'PaketPrüfung'], check=True, timeout=10)
