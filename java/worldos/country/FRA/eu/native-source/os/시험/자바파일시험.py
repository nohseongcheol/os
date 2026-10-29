#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import makina_birtual, Posizioa
from 자바시험 import edizio_balio, gonbidatu_fitxategi

def exekutatu_komando():
    EMAITZA = {}
    ITURBURUA = (Posizioa.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        gailu = makina_birtual(Posizioa / ('build/kernel.' + 종류), 종류, sare_balio=False)
        try:
            edizio_balio(gailu, 'FileDemo.java', ITURBURUA)
            gailu.Komandoa('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for iterazio_balio in range(2):
                Irteera = gailu.Komandoa('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            sarrera_Zerrenda = gailu.Komandoa('ls', ['java.txt  3 bytes'])
            Tamaina = int(re.search(r'FileDemo.class\s+(\d+) bytes', sarrera_Zerrenda)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                direktorio_balio = Path(임시)
                gonbidatu_fitxategi(gailu, 2, Tamaina, direktorio_balio / 'FileDemo.class')
                Ostalari = subprocess.check_output(['java', '-Xverify:all', '-cp', str(direktorio_balio), 'FileDemo'], cwd=str(direktorio_balio), universal_newlines=True)
                assert Ostalari == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', Ostalari
                assert (direktorio_balio / 'java.txt').read_bytes() == b'A\xffB'
            edizio_balio(gailu, 'FileDemo.java', ITURBURUA.replace('output.write(65);', 'output.close(); output.write(65);'))
            gailu.Komandoa('javac FileDemo.java', ['Exit: 0'])
            gailu.Komandoa('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            edizio_balio(gailu, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            gailu.Komandoa('javac FileDemo.java', ['Exit: 0'])
            gailu.Komandoa('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            gailu.Komandoa('run hello recovered', ['Exit: 0'])
            EMAITZA[종류] = gailu.LOG_marka.decode('utf-8', 'replace')
        finally:
            gailu.Itxi()
        print('PASS:', 종류, '게스트 Java Fitxategia sortu/이어쓰기/byte_balio/EOF/닫힘/hutsegite_balio/OpenJDK 교차 exekutatu_komando', flush=True)
    (Posizioa / 'build/자바파일시험.json').write_text(json.dumps(EMAITZA, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    exekutatu_komando()
