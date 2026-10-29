#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import ምናባዊ_ማሽን, አካባቢ
from 자바시험 import አርትዕ_እሴት, እንግዳ_ፋይል

def ፈጽም_ትእዛዝ():
    ልኬት = {}
    ምንጭ = (አካባቢ.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        ማሽን = ምናባዊ_ማሽን(አካባቢ / ('build/kernel.' + 종류), 종류, መረብ_እሴት=False)
        try:
            አርትዕ_እሴት(ማሽን, 'FileDemo.java', ምንጭ)
            ማሽን.ትእዛዝ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ሽምጥ_እሴት in range(2):
                ውጤት = ማሽን.ትእዛዝ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ምዝግብ_ዝርዝር = ማሽን.ትእዛዝ('ls', ['java.txt  3 bytes'])
            መጠን = int(re.search(r'FileDemo.class\s+(\d+) bytes', ምዝግብ_ዝርዝር)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ማውጫ_እሴት = Path(임시)
                እንግዳ_ፋይል(ማሽን, 2, መጠን, ማውጫ_እሴት / 'FileDemo.class')
                አዘጋጅ_b78e430d = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ማውጫ_እሴት), 'FileDemo'], cwd=str(ማውጫ_እሴት), universal_newlines=True)
                assert አዘጋጅ_b78e430d == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', አዘጋጅ_b78e430d
                assert (ማውጫ_እሴት / 'java.txt').read_bytes() == b'A\xffB'
            አርትዕ_እሴት(ማሽን, 'FileDemo.java', ምንጭ.replace('output.write(65);', 'output.close(); output.write(65);'))
            ማሽን.ትእዛዝ('javac FileDemo.java', ['Exit: 0'])
            ማሽን.ትእዛዝ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            አርትዕ_እሴት(ማሽን, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            ማሽን.ትእዛዝ('javac FileDemo.java', ['Exit: 0'])
            ማሽን.ትእዛዝ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            ማሽን.ትእዛዝ('run hello recovered', ['Exit: 0'])
            ልኬት[종류] = ማሽን.መዝግብ_ረድፍ.decode('utf-8', 'replace')
        finally:
            ማሽን.መዝጊያ()
        print('PASS:', 종류, '게스트 Java ፋይል አዘጋጅ/이어쓰기/ባይት_እሴት/EOF/닫힘/ተስኖት_እሴት/OpenJDK 교차 ፈጽም_ትእዛዝ', flush=True)
    (አካባቢ / 'build/자바파일시험.json').write_text(json.dumps(ልኬት, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ፈጽም_ትእዛዝ()
