#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import مجازي_مشين, 위치
from 자바시험 import تدوين_قدر, 게스트파일

def تعميل_ڪرڻ_حڪم():
    결과 = {}
    ماخذ = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        مشين = مجازي_مشين(위치 / ('build/kernel.' + 종류), 종류, نيٽ_ورڪ_قدر=False)
        try:
            تدوين_قدر(مشين, 'FileDemo.java', ماخذ)
            مشين.حڪم('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for دهرائڻ_قدر in range(2):
                출력 = مشين.حڪم('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            داخلا_فهرست = مشين.حڪم('ls', ['java.txt  3 bytes'])
            سائيز = int(re.search(r'FileDemo.class\s+(\d+) bytes', داخلا_فهرست)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ڊائريڪٽري_قدر = Path(임시)
                게스트파일(مشين, 2, سائيز, ڊائريڪٽري_قدر / 'FileDemo.class')
                مهمان = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ڊائريڪٽري_قدر), 'FileDemo'], cwd=str(ڊائريڪٽري_قدر), universal_newlines=True)
                assert مهمان == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', مهمان
                assert (ڊائريڪٽري_قدر / 'java.txt').read_bytes() == b'A\xffB'
            تدوين_قدر(مشين, 'FileDemo.java', ماخذ.replace('output.write(65);', 'output.close(); output.write(65);'))
            مشين.حڪم('javac FileDemo.java', ['Exit: 0'])
            مشين.حڪم('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            تدوين_قدر(مشين, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            مشين.حڪم('javac FileDemo.java', ['Exit: 0'])
            مشين.حڪم('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            مشين.حڪم('run hello recovered', ['Exit: 0'])
            결과[종류] = مشين.لاگ_صف.decode('utf-8', 'replace')
        finally:
            مشين.بند_ڪرڻ()
        print('PASS:', 종류, '게스트 Java فائل 생성/이어쓰기/بائٽ_قدر/EOF/닫힘/ناڪامي_قدر/OpenJDK 교차 تعميل_ڪرڻ_حڪم', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    تعميل_ڪرڻ_حڪم()
