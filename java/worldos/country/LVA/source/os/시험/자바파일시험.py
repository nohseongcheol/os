#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import VM, Novietojums
from 자바시험 import Rediģēt_VALUE, viesis_Fails

def Izpildīt_komanda():
    mērs = {}
    AVOTS = (Novietojums.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        mašīna = VM(Novietojums / ('build/kernel.' + 종류), 종류, tīkls_VALUE=False)
        try:
            Rediģēt_VALUE(mašīna, 'FileDemo.java', AVOTS)
            mašīna.Komanda('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprints_VALUE in range(2):
                Izvade = mašīna.Komanda('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ievade_Saraksts = mašīna.Komanda('ls', ['java.txt  3 bytes'])
            Izmērs = int(re.search(r'FileDemo.class\s+(\d+) bytes', ievade_Saraksts)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Direktorijs_VALUE = Path(임시)
                viesis_Fails(mašīna, 2, Izmērs, Direktorijs_VALUE / 'FileDemo.class')
                viesot = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Direktorijs_VALUE), 'FileDemo'], cwd=str(Direktorijs_VALUE), universal_newlines=True)
                assert viesot == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', viesot
                assert (Direktorijs_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            Rediģēt_VALUE(mašīna, 'FileDemo.java', AVOTS.replace('output.write(65);', 'output.close(); output.write(65);'))
            mašīna.Komanda('javac FileDemo.java', ['Exit: 0'])
            mašīna.Komanda('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Rediģēt_VALUE(mašīna, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            mašīna.Komanda('javac FileDemo.java', ['Exit: 0'])
            mašīna.Komanda('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            mašīna.Komanda('run hello recovered', ['Exit: 0'])
            mērs[종류] = mašīna.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mašīna.Aizvērt()
        print('PASS:', 종류, '게스트 Java Fails ģenerēt/이어쓰기/byte_VALUE/EOF/informācijas_tehnoloģija_slēgts/kļūme_VALUE/OpenJDK 교차 Izpildīt_komanda', flush=True)
    (Novietojums / 'build/자바파일시험.json').write_text(json.dumps(mērs, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Izpildīt_komanda()
