#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import अवास्तविक_मेशिन, स्थिति
from 자바시험 import सम्पादन_गर्नुहोस्_मान, अतिथि_फाइल

def कार्यान्वयन_गर्नुहोस्_आदेश():
    मापन = {}
    स्रोत = (स्थिति.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        मेशिन = अवास्तविक_मेशिन(स्थिति / ('build/kernel.' + 종류), 종류, सञ्जाल_मान=False)
        try:
            सम्पादन_गर्नुहोस्_मान(मेशिन, 'FileDemo.java', स्रोत)
            मेशिन.आदेश('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for दोहर्_याउनु_मान in range(2):
                출력 = मेशिन.आदेश('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            प्रविष्टि_सूची = मेशिन.आदेश('ls', ['java.txt  3 bytes'])
            आकार = int(re.search(r'FileDemo.class\s+(\d+) bytes', प्रविष्टि_सूची)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                डाइरेक्टरी_मान = Path(임시)
                अतिथि_फाइल(मेशिन, 2, आकार, डाइरेक्टरी_मान / 'FileDemo.class')
                होस्ट = subprocess.check_output(['java', '-Xverify:all', '-cp', str(डाइरेक्टरी_मान), 'FileDemo'], cwd=str(डाइरेक्टरी_मान), universal_newlines=True)
                assert होस्ट == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', होस्ट
                assert (डाइरेक्टरी_मान / 'java.txt').read_bytes() == b'A\xffB'
            सम्पादन_गर्नुहोस्_मान(मेशिन, 'FileDemo.java', स्रोत.replace('output.write(65);', 'output.close(); output.write(65);'))
            मेशिन.आदेश('javac FileDemo.java', ['Exit: 0'])
            मेशिन.आदेश('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            सम्पादन_गर्नुहोस्_मान(मेशिन, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            मेशिन.आदेश('javac FileDemo.java', ['Exit: 0'])
            मेशिन.आदेश('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            मेशिन.आदेश('run hello recovered', ['Exit: 0'])
            मापन[종류] = मेशिन.लग_रेकर्ड.decode('utf-8', 'replace')
        finally:
            मेशिन.बन्दगर्नुहोस्()
        print('PASS:', 종류, '게스트 Java फाइल सिर्जना_गर्नुहोस्/이어쓰기/बाइट_मान/EOF/닫힘/विफल_मान/OpenJDK 교차 कार्यान्वयन_गर्नुहोस्_आदेश', flush=True)
    (स्थिति / 'build/자바파일시험.json').write_text(json.dumps(मापन, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    कार्यान्वयन_गर्नुहोस्_आदेश()
