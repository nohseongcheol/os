#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import वर्चुअल_मशीन, स्थान
from 자바시험 import संपादन_मान, अतिथि_फ़ाइल

def निष्पादित_करें_आदेश():
    परिणाम = {}
    स्रोत = (स्थान.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        यंत्र = वर्चुअल_मशीन(स्थान / ('build/kernel.' + 종류), 종류, नेटवर्क_मान=False)
        try:
            संपादन_मान(यंत्र, 'FileDemo.java', स्रोत)
            यंत्र.आदेश('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for पुनरावृति_मान in range(2):
                निर्गम = यंत्र.आदेश('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            एन्ट्री_सूची = यंत्र.आदेश('ls', ['java.txt  3 bytes'])
            आकार = int(re.search(r'FileDemo.class\s+(\d+) bytes', एन्ट्री_सूची)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                डायरेक्टरी_मान = Path(임시)
                अतिथि_फ़ाइल(यंत्र, 2, आकार, डायरेक्टरी_मान / 'FileDemo.class')
                आयोजक = subprocess.check_output(['java', '-Xverify:all', '-cp', str(डायरेक्टरी_मान), 'FileDemo'], cwd=str(डायरेक्टरी_मान), universal_newlines=True)
                assert आयोजक == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', आयोजक
                assert (डायरेक्टरी_मान / 'java.txt').read_bytes() == b'A\xffB'
            संपादन_मान(यंत्र, 'FileDemo.java', स्रोत.replace('output.write(65);', 'output.close(); output.write(65);'))
            यंत्र.आदेश('javac FileDemo.java', ['Exit: 0'])
            यंत्र.आदेश('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            संपादन_मान(यंत्र, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            यंत्र.आदेश('javac FileDemo.java', ['Exit: 0'])
            यंत्र.आदेश('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            यंत्र.आदेश('run hello recovered', ['Exit: 0'])
            परिणाम[종류] = यंत्र.लॉग_रिकॉर्ड.decode('utf-8', 'replace')
        finally:
            यंत्र.बंदकरें()
        print('PASS:', 종류, '게스트 Java संचिका जनरेट_करें/이어쓰기/बाइट_मान/EOF/닫힘/विफलता_मान/OpenJDK 교차 निष्पादित_करें_आदेश', flush=True)
    (स्थान / 'build/자바파일시험.json').write_text(json.dumps(परिणाम, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    निष्पादित_करें_आदेश()
