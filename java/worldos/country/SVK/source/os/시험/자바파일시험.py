#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from test_používateľ_sieť import virtuálny_počítač, Pozícia
from 자바시험 import úprava_VALUE, hosť_Súbor

def Vykonať_príkaz():
    KR = {}
    ZDROJ = (Pozícia.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        počítač_5eb260fa = virtuálny_počítač(Pozícia / ('build/kernel.' + 종류), 종류, sieť_VALUE=False)
        try:
            úprava_VALUE(počítač_5eb260fa, 'FileDemo.java', ZDROJ)
            počítač_5eb260fa.Príkaz('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for šprint_VALUE in range(2):
                Výstup = počítač_5eb260fa.Príkaz('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            položka_Zoznam = počítač_5eb260fa.Príkaz('ls', ['java.txt  3 bytes'])
            Veľkosť = int(re.search(r'FileDemo.class\s+(\d+) bytes', položka_Zoznam)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Adresár_VALUE = Path(임시)
                hosť_Súbor(počítač_5eb260fa, 2, Veľkosť, Adresár_VALUE / 'FileDemo.class')
                hostiteľ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Adresár_VALUE), 'FileDemo'], cwd=str(Adresár_VALUE), universal_newlines=True)
                assert hostiteľ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', hostiteľ
                assert (Adresár_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            úprava_VALUE(počítač_5eb260fa, 'FileDemo.java', ZDROJ.replace('output.write(65);', 'output.close(); output.write(65);'))
            počítač_5eb260fa.Príkaz('javac FileDemo.java', ['Exit: 0'])
            počítač_5eb260fa.Príkaz('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            úprava_VALUE(počítač_5eb260fa, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            počítač_5eb260fa.Príkaz('javac FileDemo.java', ['Exit: 0'])
            počítač_5eb260fa.Príkaz('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            počítač_5eb260fa.Príkaz('run hello recovered', ['Exit: 0'])
            KR[종류] = počítač_5eb260fa.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            počítač_5eb260fa.Zatvoriť()
        print('PASS:', 종류, '게스트 Java Súbor generovať/이어쓰기/Byte_VALUE/EOF/닫힘/zlyhanie_VALUE/OpenJDK 교차 Vykonať_príkaz', flush=True)
    (Pozícia / 'build/자바파일시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Vykonať_príkaz()
