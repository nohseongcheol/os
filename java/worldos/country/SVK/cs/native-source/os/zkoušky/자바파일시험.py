#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from test_uživatel_síť import virtuální_počítač, pozice
from 자바시험 import úprava_HODNOTA, host_Soubor

def Provést_příkaz():
    VÝSLEDEK = {}
    zdrojový_soubor = (pozice.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for Druh_HODNOTA in ('elf', 'iso'):
        počítač = virtuální_počítač(pozice / ('build/kernel.' + Druh_HODNOTA), Druh_HODNOTA, síť_HODNOTA=False)
        try:
            úprava_HODNOTA(počítač, 'FileDemo.java', zdrojový_soubor)
            počítač.příkaz('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_HODNOTA in range(2):
                výstupní_pozice = počítač.příkaz('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            položka_Seznam = počítač.příkaz('ls', ['java.txt  3 bytes'])
            Velikost = int(re.search(r'FileDemo.class\s+(\d+) bytes', položka_Seznam)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Adresář_HODNOTA = Path(임시)
                host_Soubor(počítač, 2, Velikost, Adresář_HODNOTA / 'FileDemo.class')
                hostit = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Adresář_HODNOTA), 'FileDemo'], cwd=str(Adresář_HODNOTA), universal_newlines=True)
                assert hostit == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', hostit
                assert (Adresář_HODNOTA / 'java.txt').read_bytes() == b'A\xffB'
            úprava_HODNOTA(počítač, 'FileDemo.java', zdrojový_soubor.replace('output.write(65);', 'output.close(); output.write(65);'))
            počítač.příkaz('javac FileDemo.java', ['Exit: 0'])
            počítač.příkaz('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            úprava_HODNOTA(počítač, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            počítač.příkaz('javac FileDemo.java', ['Exit: 0'])
            počítač.příkaz('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            počítač.příkaz('run hello recovered', ['Exit: 0'])
            VÝSLEDEK[Druh_HODNOTA] = počítač.LOGZ_ZÁZNAM.decode('utf-8', 'replace')
        finally:
            počítač.Zavřené()
        print('PASS:', Druh_HODNOTA, '게스트 Java název_souboru generovat/이어쓰기/bajt_HODNOTA/EOF/informační_systémy_uzavřeno/selhání_HODNOTA/OpenJDK 교차 Provést_příkaz', flush=True)
    (pozice / 'build/자바파일시험.json').write_text(json.dumps(VÝSLEDEK, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Provést_příkaz()
