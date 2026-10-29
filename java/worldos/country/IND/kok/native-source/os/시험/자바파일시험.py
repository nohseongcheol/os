#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import भ्रामक_यंत्र, स्थिती
from 자바시험 import संपादन_करचें_मोल, सोयरो_फायल

def पाळो_दिवचो_आदेश():
    मेजप = {}
    स्त्रोत = (स्थिती.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        यंत्र = भ्रामक_यंत्र(स्थिती / ('build/kernel.' + 종류), 종류, नॅटवर्क_मोल=False)
        try:
            संपादन_करचें_मोल(यंत्र, 'FileDemo.java', स्त्रोत)
            यंत्र.आदेश('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for परतवण_मोल in range(2):
                출력 = यंत्र.आदेश('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            प्रवेश_सुची = यंत्र.आदेश('ls', ['java.txt  3 bytes'])
            आवाठ = int(re.search(r'FileDemo.class\s+(\d+) bytes', प्रवेश_सुची)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                नामावळ_मोल = Path(임시)
                सोयरो_फायल(यंत्र, 2, आवाठ, नामावळ_मोल / 'FileDemo.class')
                येजमान = subprocess.check_output(['java', '-Xverify:all', '-cp', str(नामावळ_मोल), 'FileDemo'], cwd=str(नामावळ_मोल), universal_newlines=True)
                assert येजमान == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', येजमान
                assert (नामावळ_मोल / 'java.txt').read_bytes() == b'A\xffB'
            संपादन_करचें_मोल(यंत्र, 'FileDemo.java', स्त्रोत.replace('output.write(65);', 'output.close(); output.write(65);'))
            यंत्र.आदेश('javac FileDemo.java', ['Exit: 0'])
            यंत्र.आदेश('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            संपादन_करचें_मोल(यंत्र, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            यंत्र.आदेश('javac FileDemo.java', ['Exit: 0'])
            यंत्र.आदेश('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            यंत्र.आदेश('run hello recovered', ['Exit: 0'])
            मेजप[종류] = यंत्र.LOG_नोंद.decode('utf-8', 'replace')
        finally:
            यंत्र.शेवट()
        print('PASS:', 종류, '게스트 Java फायल तयार_करचें/이어쓰기/बायट_मोल/EOF/닫힘/अपेस_मोल/OpenJDK 교차 पाळो_दिवचो_आदेश', flush=True)
    (स्थिती / 'build/자바파일시험.json').write_text(json.dumps(मेजप, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    पाळो_दिवचो_आदेश()
