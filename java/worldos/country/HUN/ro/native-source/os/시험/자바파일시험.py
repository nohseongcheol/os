#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import VM, Poziție
from 자바시험 import edita_VALUE, invitat_Fișier

def executa_comandă():
    KR = {}
    SURSĂ = (Poziție.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        mașină = VM(Poziție / ('build/kernel.' + 종류), 종류, rețea_VALUE=False)
        try:
            edita_VALUE(mașină, 'FileDemo.java', SURSĂ)
            mașină.Comandă('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALUE in range(2):
                Rezultat = mașină.Comandă('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            intrare_Listă = mașină.Comandă('ls', ['java.txt  3 bytes'])
            Mărime = int(re.search(r'FileDemo.class\s+(\d+) bytes', intrare_Listă)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Director_VALUE = Path(임시)
                invitat_Fișier(mașină, 2, Mărime, Director_VALUE / 'FileDemo.class')
                gazdă = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Director_VALUE), 'FileDemo'], cwd=str(Director_VALUE), universal_newlines=True)
                assert gazdă == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', gazdă
                assert (Director_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            edita_VALUE(mașină, 'FileDemo.java', SURSĂ.replace('output.write(65);', 'output.close(); output.write(65);'))
            mașină.Comandă('javac FileDemo.java', ['Exit: 0'])
            mașină.Comandă('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            edita_VALUE(mașină, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            mașină.Comandă('javac FileDemo.java', ['Exit: 0'])
            mașină.Comandă('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            mașină.Comandă('run hello recovered', ['Exit: 0'])
            KR[종류] = mașină.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mașină.Închide()
        print('PASS:', 종류, '게스트 Java Fișier genera/이어쓰기/byte_VALUE/EOF/닫힘/eroare_VALUE/OpenJDK 교차 executa_comandă', flush=True)
    (Poziție / 'build/자바파일시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    executa_comandă()
