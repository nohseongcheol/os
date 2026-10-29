#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import virtualno_mašina, Pozicija
from 자바시험 import uređivati_VALUE, gost_fajl

def Izvrši_komanda():
    mjera = {}
    IZVOR = (Pozicija.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        mašina = virtualno_mašina(Pozicija / ('build/kernel.' + 종류), 종류, Mreža_VALUE=False)
        try:
            uređivati_VALUE(mašina, 'FileDemo.java', IZVOR)
            mašina.Naredba('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ponavljanje_VALUE in range(2):
                Ispis = mašina.Naredba('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            unos_spisak = mašina.Naredba('ls', ['java.txt  3 bytes'])
            Veličina = int(re.search(r'FileDemo.class\s+(\d+) bytes', unos_spisak)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Direktorij_VALUE = Path(임시)
                gost_fajl(mašina, 2, Veličina, Direktorij_VALUE / 'FileDemo.class')
                organizator = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Direktorij_VALUE), 'FileDemo'], cwd=str(Direktorij_VALUE), universal_newlines=True)
                assert organizator == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', organizator
                assert (Direktorij_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            uređivati_VALUE(mašina, 'FileDemo.java', IZVOR.replace('output.write(65);', 'output.close(); output.write(65);'))
            mašina.Naredba('javac FileDemo.java', ['Exit: 0'])
            mašina.Naredba('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            uređivati_VALUE(mašina, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            mašina.Naredba('javac FileDemo.java', ['Exit: 0'])
            mašina.Naredba('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            mašina.Naredba('run hello recovered', ['Exit: 0'])
            mjera[종류] = mašina.LOG_red.decode('utf-8', 'replace')
        finally:
            mašina.Zatvori()
        print('PASS:', 종류, '게스트 Java Fajl generirati/이어쓰기/bajt_VALUE/EOF/닫힘/neuspjeh_VALUE/OpenJDK 교차 Izvrši_komanda', flush=True)
    (Pozicija / 'build/자바파일시험.json').write_text(json.dumps(mjera, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Izvrši_komanda()
