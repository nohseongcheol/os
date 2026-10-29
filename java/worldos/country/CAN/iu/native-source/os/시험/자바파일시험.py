#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import 가상기계, 위치
from 자바시험 import aaqqigiarli_atuutilik, 게스트파일

def 실행():
    결과 = {}
    pivviujuq = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        기계 = 가상기계(위치 / ('build/kernel.' + 종류), 종류, Kasuqatigiitsimajut_atuutilik=False)
        try:
            aaqqigiarli_atuutilik(기계, 'FileDemo.java', pivviujuq)
            기계.piqujijjut('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for utiqtaqtuq_atuutilik in range(2):
                출력 = 기계.piqujijjut('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            Iliniku_Titiqpalliagaq = 기계.piqujijjut('ls', ['java.txt  3 bytes'])
            anininga = int(re.search(r'FileDemo.class\s+(\d+) bytes', Iliniku_Titiqpalliagaq)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                tukimuagutiit_atuutilik = Path(임시)
                게스트파일(기계, 2, anininga, tukimuagutiit_atuutilik / 'FileDemo.class')
                tuttarvik = subprocess.check_output(['java', '-Xverify:all', '-cp', str(tukimuagutiit_atuutilik), 'FileDemo'], cwd=str(tukimuagutiit_atuutilik), universal_newlines=True)
                assert tuttarvik == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', tuttarvik
                assert (tukimuagutiit_atuutilik / 'java.txt').read_bytes() == b'A\xffB'
            aaqqigiarli_atuutilik(기계, 'FileDemo.java', pivviujuq.replace('output.write(65);', 'output.close(); output.write(65);'))
            기계.piqujijjut('javac FileDemo.java', ['Exit: 0'])
            기계.piqujijjut('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            aaqqigiarli_atuutilik(기계, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            기계.piqujijjut('javac FileDemo.java', ['Exit: 0'])
            기계.piqujijjut('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            기계.piqujijjut('run hello recovered', ['Exit: 0'])
            결과[종류] = 기계.papattivik_sanimukutaak.decode('utf-8', 'replace')
        finally:
            기계.matuli()
        print('PASS:', 종류, '게스트 Java ini 생성/이어쓰기/byte_atuutilik/EOF/닫힘/itigaqtuq_atuutilik/OpenJDK 교차 실행', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    실행()
