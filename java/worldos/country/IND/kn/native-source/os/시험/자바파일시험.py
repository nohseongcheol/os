#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import ಅಗೋಚರ_ಯಂತ್ರ, ಸ್ಥಾನ
from 자바시험 import ಸಂಪಾದನೆ_ಮೌಲ್ಯ, ಅತಿಥಿ_ಫೈಲ್

def ಪೂರೈಸು_ಆದೇಶ():
    ಮಾಪನ = {}
    ಮೂಲ = (ಸ್ಥಾನ.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        ಯಂತ್ರ = ಅಗೋಚರ_ಯಂತ್ರ(ಸ್ಥಾನ / ('build/kernel.' + 종류), 종류, ನೆಟ್_ವರ್ಕ್_ಮೌಲ್ಯ=False)
        try:
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'FileDemo.java', ಮೂಲ)
            ಯಂತ್ರ.ಆಜ್ಞೆ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ಸ್ಪ್ರಿಂಟ್_ಮೌಲ್ಯ in range(2):
                ಔಟ್_ಪುಟ್ = ಯಂತ್ರ.ಆಜ್ಞೆ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ನಮೂದು_ಪಟ್ಟಿ = ಯಂತ್ರ.ಆಜ್ಞೆ('ls', ['java.txt  3 bytes'])
            ಗಾತ್ರ = int(re.search(r'FileDemo.class\s+(\d+) bytes', ನಮೂದು_ಪಟ್ಟಿ)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ = Path(임시)
                ಅತಿಥಿ_ಫೈಲ್(ಯಂತ್ರ, 2, ಗಾತ್ರ, ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'FileDemo.class')
                ಹೋಸ್ಟ್ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ), 'FileDemo'], cwd=str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ), universal_newlines=True)
                assert ಹೋಸ್ಟ್ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', ಹೋಸ್ಟ್
                assert (ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'java.txt').read_bytes() == b'A\xffB'
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'FileDemo.java', ಮೂಲ.replace('output.write(65);', 'output.close(); output.write(65);'))
            ಯಂತ್ರ.ಆಜ್ಞೆ('javac FileDemo.java', ['Exit: 0'])
            ಯಂತ್ರ.ಆಜ್ಞೆ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            ಯಂತ್ರ.ಆಜ್ಞೆ('javac FileDemo.java', ['Exit: 0'])
            ಯಂತ್ರ.ಆಜ್ಞೆ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            ಯಂತ್ರ.ಆಜ್ಞೆ('run hello recovered', ['Exit: 0'])
            ಮಾಪನ[종류] = ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ.decode('utf-8', 'replace')
        finally:
            ಯಂತ್ರ.ಮುಚ್ಚು()
        print('PASS:', 종류, '게스트 Java ಕಡತ ರಚಿಸಿ/이어쓰기/ಬೈಟ್_ಮೌಲ್ಯ/EOF/닫힘/ವೈಫಲ್ಯ_ಮೌಲ್ಯ/OpenJDK 교차 ಪೂರೈಸು_ಆದೇಶ', flush=True)
    (ಸ್ಥಾನ / 'build/자바파일시험.json').write_text(json.dumps(ಮಾಪನ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ಪೂರೈಸು_ಆದೇಶ()
