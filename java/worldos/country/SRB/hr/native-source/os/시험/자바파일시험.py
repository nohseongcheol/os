#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import VM, Položaj
from 자바시험 import Uredi_VALUE, gost_Datoteka

def Izvrši_naredba():
    REZULTAT = {}
    IZVOR = (Položaj.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        stroj = VM(Položaj / ('build/kernel.' + 종류), 종류, mreža_VALUE=False)
        try:
            Uredi_VALUE(stroj, 'FileDemo.java', IZVOR)
            stroj.Naredba('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALUE in range(2):
                Izlaz = stroj.Naredba('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            unos_Popis = stroj.Naredba('ls', ['java.txt  3 bytes'])
            Veličina = int(re.search(r'FileDemo.class\s+(\d+) bytes', unos_Popis)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                imenik_VALUE = Path(임시)
                gost_Datoteka(stroj, 2, Veličina, imenik_VALUE / 'FileDemo.class')
                domaćin = subprocess.check_output(['java', '-Xverify:all', '-cp', str(imenik_VALUE), 'FileDemo'], cwd=str(imenik_VALUE), universal_newlines=True)
                assert domaćin == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', domaćin
                assert (imenik_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            Uredi_VALUE(stroj, 'FileDemo.java', IZVOR.replace('output.write(65);', 'output.close(); output.write(65);'))
            stroj.Naredba('javac FileDemo.java', ['Exit: 0'])
            stroj.Naredba('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Uredi_VALUE(stroj, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            stroj.Naredba('javac FileDemo.java', ['Exit: 0'])
            stroj.Naredba('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            stroj.Naredba('run hello recovered', ['Exit: 0'])
            REZULTAT[종류] = stroj.LOG_zapis.decode('utf-8', 'replace')
        finally:
            stroj.Zatvori()
        print('PASS:', 종류, '게스트 Java Datoteka generirati/이어쓰기/bajt_VALUE/EOF/닫힘/kvar_VALUE/OpenJDK 교차 Izvrši_naredba', flush=True)
    (Položaj / 'build/자바파일시험.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Izvrši_naredba()
