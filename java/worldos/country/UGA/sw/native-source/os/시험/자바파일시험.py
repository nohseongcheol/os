#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import pepe_mashine, 위치
from 자바시험 import hariri_thamani, mgeni_faili

def tekeleza_amri():
    결과 = {}
    chanzo = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        mashine = pepe_mashine(위치 / ('build/kernel.' + 종류), 종류, Mtandao_thamani=False)
        try:
            hariri_thamani(mashine, 'FileDemo.java', chanzo)
            mashine.amri('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_thamani in range(2):
                출력 = mashine.amri('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ingizo_Orodha = mashine.amri('ls', ['java.txt  3 bytes'])
            panga_ukubwa = int(re.search(r'FileDemo.class\s+(\d+) bytes', ingizo_Orodha)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Saraka_thamani = Path(임시)
                mgeni_faili(mashine, 2, panga_ukubwa, Saraka_thamani / 'FileDemo.class')
                mwenyeji = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Saraka_thamani), 'FileDemo'], cwd=str(Saraka_thamani), universal_newlines=True)
                assert mwenyeji == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', mwenyeji
                assert (Saraka_thamani / 'java.txt').read_bytes() == b'A\xffB'
            hariri_thamani(mashine, 'FileDemo.java', chanzo.replace('output.write(65);', 'output.close(); output.write(65);'))
            mashine.amri('javac FileDemo.java', ['Exit: 0'])
            mashine.amri('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            hariri_thamani(mashine, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            mashine.amri('javac FileDemo.java', ['Exit: 0'])
            mashine.amri('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            mashine.amri('run hello recovered', ['Exit: 0'])
            결과[종류] = mashine.batli_REKODI.decode('utf-8', 'replace')
        finally:
            mashine.funga()
        print('PASS:', 종류, '게스트 Java faili 생성/이어쓰기/baiti_thamani/EOF/닫힘/kushindwa_thamani/OpenJDK 교차 tekeleza_amri', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    tekeleza_amri()
