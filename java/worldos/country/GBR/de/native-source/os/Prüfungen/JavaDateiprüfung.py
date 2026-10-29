#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from benutzerNetzwerkPrüfung import VirtuelleMaschine, position
from JavaPrüfung import bearbeitenWert, gastDatei

def befehlAusführen():
    ergebnis = {}
    Quelltext = (position.parent / 'posix-kor/JavaBeispiel/FileDemo.java').read_text()
    for artWert in ('elf', 'iso'):
        maschine = VirtuelleMaschine(position / ('build/kernel.' + artWert), artWert, netzwerkWert=False)
        try:
            bearbeitenWert(maschine, 'FileDemo.java', Quelltext)
            maschine.befehl('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for wiederholungsschrittWert in range(2):
                Ausgabe = maschine.befehl('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            eintragListe = maschine.befehl('ls', ['java.txt  3 bytes'])
            größe = int(re.search(r'FileDemo.class\s+(\d+) bytes', eintragListe)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as vorläufigWert:
                verzeichnisWert = Path(vorläufigWert)
                gastDatei(maschine, 2, größe, verzeichnisWert / 'FileDemo.class')
                Wirtssystem = subprocess.check_output(['java', '-Xverify:all', '-cp', str(verzeichnisWert), 'FileDemo'], cwd=str(verzeichnisWert), universal_newlines=True)
                assert Wirtssystem == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', Wirtssystem
                assert (verzeichnisWert / 'java.txt').read_bytes() == b'A\xffB'
            bearbeitenWert(maschine, 'FileDemo.java', Quelltext.replace('output.write(65);', 'output.close(); output.write(65);'))
            maschine.befehl('javac FileDemo.java', ['Exit: 0'])
            maschine.befehl('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            bearbeitenWert(maschine, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            maschine.befehl('javac FileDemo.java', ['Exit: 0'])
            maschine.befehl('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            maschine.befehl('run hello recovered', ['Exit: 0'])
            ergebnis[artWert] = maschine.protokolldateiAufzeichnung.decode('utf-8', 'replace')
        finally:
            maschine.schließen()
        print('PASS:', artWert, '게스트 Java Datei generieren/fortsetzungAnhängen/byteWert/EOF/istGeschlossen/fehlschlagWert/OpenJDK 교차 befehlAusführen', flush=True)
    (position / 'build/JavaDateiprüfung.json').write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    befehlAusführen()
