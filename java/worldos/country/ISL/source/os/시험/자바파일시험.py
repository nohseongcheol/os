#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import sýndar_vél, Staðsetning
from 자바시험 import breyta_VALUE, gestur_skrá

def keyra_skipun():
    NIÐURSTAÐA = {}
    Uppruni = (Staðsetning.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        vél = sýndar_vél(Staðsetning / ('build/kernel.' + 종류), 종류, Net_VALUE=False)
        try:
            breyta_VALUE(vél, 'FileDemo.java', Uppruni)
            vél.Skipun('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ítrekun_VALUE in range(2):
                úttak = vél.Skipun('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            færsla_Listi = vél.Skipun('ls', ['java.txt  3 bytes'])
            Stærð = int(re.search(r'FileDemo.class\s+(\d+) bytes', færsla_Listi)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                skráasafn_VALUE = Path(임시)
                gestur_skrá(vél, 2, Stærð, skráasafn_VALUE / 'FileDemo.class')
                hýsa = subprocess.check_output(['java', '-Xverify:all', '-cp', str(skráasafn_VALUE), 'FileDemo'], cwd=str(skráasafn_VALUE), universal_newlines=True)
                assert hýsa == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', hýsa
                assert (skráasafn_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            breyta_VALUE(vél, 'FileDemo.java', Uppruni.replace('output.write(65);', 'output.close(); output.write(65);'))
            vél.Skipun('javac FileDemo.java', ['Exit: 0'])
            vél.Skipun('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            breyta_VALUE(vél, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            vél.Skipun('javac FileDemo.java', ['Exit: 0'])
            vél.Skipun('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            vél.Skipun('run hello recovered', ['Exit: 0'])
            NIÐURSTAÐA[종류] = vél.LOG_lína.decode('utf-8', 'replace')
        finally:
            vél.Loka()
        print('PASS:', 종류, '게스트 Java Skrá skapa/이어쓰기/bæti_VALUE/EOF/upplýsingatækni_lokað/bilun_VALUE/OpenJDK 교차 keyra_skipun', flush=True)
    (Staðsetning / 'build/자바파일시험.json').write_text(json.dumps(NIÐURSTAÐA, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    keyra_skipun()
