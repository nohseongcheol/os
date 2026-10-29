#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from preskusiti_uporabnik_mreža import navidezni_računalnik, Položaj
from 자바시험 import Uredi_VALUE, gost_Datoteka

def Izvedi_ukaz():
    REZULTAT = {}
    VIR = (Položaj.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        računalnik = navidezni_računalnik(Položaj / ('build/kernel.' + 종류), 종류, mreža_VALUE=False)
        try:
            Uredi_VALUE(računalnik, 'FileDemo.java', VIR)
            računalnik.Ukaz('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALUE in range(2):
                Izpis = računalnik.Ukaz('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            vnos_Seznam = računalnik.Ukaz('ls', ['java.txt  3 bytes'])
            Velikost = int(re.search(r'FileDemo.class\s+(\d+) bytes', vnos_Seznam)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Imenik_VALUE = Path(임시)
                gost_Datoteka(računalnik, 2, Velikost, Imenik_VALUE / 'FileDemo.class')
                gostiti = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Imenik_VALUE), 'FileDemo'], cwd=str(Imenik_VALUE), universal_newlines=True)
                assert gostiti == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', gostiti
                assert (Imenik_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            Uredi_VALUE(računalnik, 'FileDemo.java', VIR.replace('output.write(65);', 'output.close(); output.write(65);'))
            računalnik.Ukaz('javac FileDemo.java', ['Exit: 0'])
            računalnik.Ukaz('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Uredi_VALUE(računalnik, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            računalnik.Ukaz('javac FileDemo.java', ['Exit: 0'])
            računalnik.Ukaz('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            računalnik.Ukaz('run hello recovered', ['Exit: 0'])
            REZULTAT[종류] = računalnik.LOG_zapis.decode('utf-8', 'replace')
        finally:
            računalnik.Zapri()
        print('PASS:', 종류, '게스트 Java Datoteka ustvariti/이어쓰기/bajt_VALUE/EOF/닫힘/napaka_VALUE/OpenJDK 교차 Izvedi_ukaz', flush=True)
    (Položaj / 'build/자바파일시험.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Izvedi_ukaz()
