#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from testi_käyttäjä_verkko import VM, paikka
from 자바시험 import muutos_ARVO, vieras_Tiedosto

def Suorita_komento():
    TULOS = {}
    lähdetiedosto = (paikka.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        kone = VM(paikka / ('build/kernel.' + 종류), 종류, verkko_ARVO=False)
        try:
            muutos_ARVO(kone, 'FileDemo.java', lähdetiedosto)
            kone.komento('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprintti_ARVO in range(2):
                tulostuspaikka = kone.komento('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            merkintä_luettelo = kone.komento('ls', ['java.txt  3 bytes'])
            Koko = int(re.search(r'FileDemo.class\s+(\d+) bytes', merkintä_luettelo)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Directory_ARVO = Path(임시)
                vieras_Tiedosto(kone, 2, Koko, Directory_ARVO / 'FileDemo.class')
                isäntä = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Directory_ARVO), 'FileDemo'], cwd=str(Directory_ARVO), universal_newlines=True)
                assert isäntä == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', isäntä
                assert (Directory_ARVO / 'java.txt').read_bytes() == b'A\xffB'
            muutos_ARVO(kone, 'FileDemo.java', lähdetiedosto.replace('output.write(65);', 'output.close(); output.write(65);'))
            kone.komento('javac FileDemo.java', ['Exit: 0'])
            kone.komento('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            muutos_ARVO(kone, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            kone.komento('javac FileDemo.java', ['Exit: 0'])
            kone.komento('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            kone.komento('run hello recovered', ['Exit: 0'])
            TULOS[종류] = kone.LOG_TIETUE.decode('utf-8', 'replace')
        finally:
            kone.Sulje()
        print('PASS:', 종류, '게스트 Java tiedoston_nimi generoida/이어쓰기/tavu_ARVO/EOF/tietojärjestelmät_suljettu/virhe_ARVO/OpenJDK 교차 Suorita_komento', flush=True)
    (paikka / 'build/자바파일시험.json').write_text(json.dumps(TULOS, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Suorita_komento()
