#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import مەجازی_مەکینه, 위치
from 자바시험 import بژار_نرخ, 게스트파일

def جێبەجێکردن_فەرمان():
    결과 = {}
    ژێدەر = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        مەکینه = مەجازی_مەکینه(위치 / ('build/kernel.' + 종류), 종류, تۆڕ_نرخ=False)
        try:
            بژار_نرخ(مەکینه, 'FileDemo.java', ژێدەر)
            مەکینه.فەرمان('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for دووبارەکردنەوە_نرخ in range(2):
                출력 = مەکینه.فەرمان('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            تێنووسین_لیست = مەکینه.فەرمان('ls', ['java.txt  3 bytes'])
            گۆڕینی_ئەندازە = int(re.search(r'FileDemo.class\s+(\d+) bytes', تێنووسین_لیست)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ڕێبەرنامە_نرخ = Path(임시)
                게스트파일(مەکینه, 2, گۆڕینی_ئەندازە, ڕێبەرنامە_نرخ / 'FileDemo.class')
                جێدەر = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ڕێبەرنامە_نرخ), 'FileDemo'], cwd=str(ڕێبەرنامە_نرخ), universal_newlines=True)
                assert جێدەر == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', جێدەر
                assert (ڕێبەرنامە_نرخ / 'java.txt').read_bytes() == b'A\xffB'
            بژار_نرخ(مەکینه, 'FileDemo.java', ژێدەر.replace('output.write(65);', 'output.close(); output.write(65);'))
            مەکینه.فەرمان('javac FileDemo.java', ['Exit: 0'])
            مەکینه.فەرمان('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            بژار_نرخ(مەکینه, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            مەکینه.فەرمان('javac FileDemo.java', ['Exit: 0'])
            مەکینه.فەرمان('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            مەکینه.فەرمان('run hello recovered', ['Exit: 0'])
            결과[종류] = مەکینه.تۆمار_ڕزن.decode('utf-8', 'replace')
        finally:
            مەکینه.داخستن()
        print('PASS:', 종류, '게스트 Java فایل 생성/이어쓰기/بایت_نرخ/EOF/닫힘/شکستهێنان_نرخ/OpenJDK 교차 جێبەجێکردن_فەرمان', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    جێبەجێکردن_فەرمان()
