#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import VM, pozicija
from 자바시험 import Uredi_VALUE, gost_Datoteka

def Izvrši_komanda():
    KR = {}
    izvor = (pozicija.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        računar = VM(pozicija / ('build/kernel.' + 종류), 종류, Mreža_VALUE=False)
        try:
            Uredi_VALUE(računar, 'FileDemo.java', izvor)
            računar.komanda('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALUE in range(2):
                출력 = računar.komanda('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            stavka_Lista = računar.komanda('ls', ['java.txt  3 bytes'])
            promeniti_veličinu = int(re.search(r'FileDemo.class\s+(\d+) bytes', stavka_Lista)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Imenik_VALUE = Path(임시)
                gost_Datoteka(računar, 2, promeniti_veličinu, Imenik_VALUE / 'FileDemo.class')
                host = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Imenik_VALUE), 'FileDemo'], cwd=str(Imenik_VALUE), universal_newlines=True)
                assert host == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', host
                assert (Imenik_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            Uredi_VALUE(računar, 'FileDemo.java', izvor.replace('output.write(65);', 'output.close(); output.write(65);'))
            računar.komanda('javac FileDemo.java', ['Exit: 0'])
            računar.komanda('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Uredi_VALUE(računar, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            računar.komanda('javac FileDemo.java', ['Exit: 0'])
            računar.komanda('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            računar.komanda('run hello recovered', ['Exit: 0'])
            KR[종류] = računar.LOG_snimi.decode('utf-8', 'replace')
        finally:
            računar.Zatvori()
        print('PASS:', 종류, '게스트 Java Datoteka generisati/이어쓰기/bajt_VALUE/EOF/닫힘/otkazivanje_VALUE/OpenJDK 교차 Izvrši_komanda', flush=True)
    (pozicija / 'build/자바파일시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Izvrši_komanda()
