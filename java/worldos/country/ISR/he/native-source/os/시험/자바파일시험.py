#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from נסה_משתמש_רשת import מחשב_וירטואלי, מיקום
from 자바시험 import ערוך_ערך, אורח_קובץ

def לבצע_פקודה():
    תוצאה = {}
    קודמקור = (מיקום.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        מחשב = מחשב_וירטואלי(מיקום / ('build/kernel.' + 종류), 종류, רשת_ערך=False)
        try:
            ערוך_ערך(מחשב, 'FileDemo.java', קודמקור)
            מחשב.פקודה('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for סבב_ערך in range(2):
                פלטטקסט = מחשב.פקודה('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ערך_רשימה = מחשב.פקודה('ls', ['java.txt  3 bytes'])
            גודל = int(re.search(r'FileDemo.class\s+(\d+) bytes', ערך_רשימה)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                מדריך_ערך = Path(임시)
                אורח_קובץ(מחשב, 2, גודל, מדריך_ערך / 'FileDemo.class')
                ארח = subprocess.check_output(['java', '-Xverify:all', '-cp', str(מדריך_ערך), 'FileDemo'], cwd=str(מדריך_ערך), universal_newlines=True)
                assert ארח == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', ארח
                assert (מדריך_ערך / 'java.txt').read_bytes() == b'A\xffB'
            ערוך_ערך(מחשב, 'FileDemo.java', קודמקור.replace('output.write(65);', 'output.close(); output.write(65);'))
            מחשב.פקודה('javac FileDemo.java', ['Exit: 0'])
            מחשב.פקודה('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            ערוך_ערך(מחשב, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            מחשב.פקודה('javac FileDemo.java', ['Exit: 0'])
            מחשב.פקודה('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            מחשב.פקודה('run hello recovered', ['Exit: 0'])
            תוצאה[종류] = מחשב.לרשום_שיא.decode('utf-8', 'replace')
        finally:
            מחשב.סגירה()
        print('PASS:', 종류, '게스트 Java קובץ יצר/이어쓰기/בית_ערך/EOF/מערכות_מידע_נסגר/כשל_ערך/OpenJDK 교차 לבצע_פקודה', flush=True)
    (מיקום / 'build/자바파일시험.json').write_text(json.dumps(תוצאה, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    לבצע_פקודה()
