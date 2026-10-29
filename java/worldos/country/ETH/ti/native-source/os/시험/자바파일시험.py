#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import መሳሊ_ማሽን, 위치
from 자바시험 import ምዕራይ_ዋጋ, 게스트파일

def ተግብር_ትእዛዝ():
    결과 = {}
    ምንጪ = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        ማሽን = መሳሊ_ማሽን(위치 / ('build/kernel.' + 종류), 종류, ማሕበራዊ_ኔትወርክ_ዋጋ=False)
        try:
            ምዕራይ_ዋጋ(ማሽን, 'FileDemo.java', ምንጪ)
            ማሽን.ትእዛዝ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ዝርዝር_ዋጋ in range(2):
                출력 = ማሽን.ትእዛዝ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ምእታው_ዝርዝር = ማሽን.ትእዛዝ('ls', ['java.txt  3 bytes'])
            መጠን = int(re.search(r'FileDemo.class\s+(\d+) bytes', ምእታው_ዝርዝር)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ሓባሪ_ማህደር_ዋጋ = Path(임시)
                게스트파일(ማሽን, 2, መጠን, ሓባሪ_ማህደር_ዋጋ / 'FileDemo.class')
                አዐንግድ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ሓባሪ_ማህደር_ዋጋ), 'FileDemo'], cwd=str(ሓባሪ_ማህደር_ዋጋ), universal_newlines=True)
                assert አዐንግድ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', አዐንግድ
                assert (ሓባሪ_ማህደር_ዋጋ / 'java.txt').read_bytes() == b'A\xffB'
            ምዕራይ_ዋጋ(ማሽን, 'FileDemo.java', ምንጪ.replace('output.write(65);', 'output.close(); output.write(65);'))
            ማሽን.ትእዛዝ('javac FileDemo.java', ['Exit: 0'])
            ማሽን.ትእዛዝ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            ምዕራይ_ዋጋ(ማሽን, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            ማሽን.ትእዛዝ('javac FileDemo.java', ['Exit: 0'])
            ማሽን.ትእዛዝ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            ማሽን.ትእዛዝ('run hello recovered', ['Exit: 0'])
            결과[종류] = ማሽን.ምዝጉብ_ሪጋ.decode('utf-8', 'replace')
        finally:
            ማሽን.ዕጸው()
        print('PASS:', 종류, '게스트 Java ፋይል 생성/이어쓰기/ባይት_ዋጋ/EOF/닫힘/ፍሽለት_ዋጋ/OpenJDK 교차 ተግብር_ትእዛዝ', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ተግብር_ትእዛዝ()
