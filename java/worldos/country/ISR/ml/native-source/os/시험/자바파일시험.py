#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import അയഥാര്_ഥ_മെഷീൻ, സ്ഥാനം
from 자바시험 import ചിട്ടപ്പെടുത്തല്_മൂല്യം, അതിഥി_ഫയല്

def നടപ്പാക്കുക_കമാന്_ഡ്():
    അളവ് = {}
    ഉറവിടം = (സ്ഥാനം.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        മെഷീൻ = അയഥാര്_ഥ_മെഷീൻ(സ്ഥാനം / ('build/kernel.' + 종류), 종류, നെറ്റ്_വർക്ക്_മൂല്യം=False)
        try:
            ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'FileDemo.java', ഉറവിടം)
            മെഷീൻ.ആജ്ഞ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ആവര്_ത്തനം_മൂല്യം in range(2):
                ഫലം = മെഷീൻ.ആജ്ഞ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            എന്_ട്രി_ലിസ്റ്റ് = മെഷീൻ.ആജ്ഞ('ls', ['java.txt  3 bytes'])
            വലിപ്പം = int(re.search(r'FileDemo.class\s+(\d+) bytes', എന്_ട്രി_ലിസ്റ്റ്)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ഡയറക്ടറി_മൂല്യം = Path(임시)
                അതിഥി_ഫയല്(മെഷീൻ, 2, വലിപ്പം, ഡയറക്ടറി_മൂല്യം / 'FileDemo.class')
                ഹോസ്റ്റ് = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ഡയറക്ടറി_മൂല്യം), 'FileDemo'], cwd=str(ഡയറക്ടറി_മൂല്യം), universal_newlines=True)
                assert ഹോസ്റ്റ് == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', ഹോസ്റ്റ്
                assert (ഡയറക്ടറി_മൂല്യം / 'java.txt').read_bytes() == b'A\xffB'
            ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'FileDemo.java', ഉറവിടം.replace('output.write(65);', 'output.close(); output.write(65);'))
            മെഷീൻ.ആജ്ഞ('javac FileDemo.java', ['Exit: 0'])
            മെഷീൻ.ആജ്ഞ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            മെഷീൻ.ആജ്ഞ('javac FileDemo.java', ['Exit: 0'])
            മെഷീൻ.ആജ്ഞ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            മെഷീൻ.ആജ്ഞ('run hello recovered', ['Exit: 0'])
            അളവ്[종류] = മെഷീൻ.ലോഗ്_രേഖ.decode('utf-8', 'replace')
        finally:
            മെഷീൻ.അടയ്ക്കു()
        print('PASS:', 종류, '게스트 Java ഫയല് സൃഷ്_ടിക്കുക/이어쓰기/బైట్_മൂല്യം/EOF/닫힘/പരാജയം_മൂല്യം/OpenJDK 교차 നടപ്പാക്കുക_കമാന്_ഡ്', flush=True)
    (സ്ഥാനം / 'build/자바파일시험.json').write_text(json.dumps(അളവ്, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    നടപ്പാക്കുക_കമാന്_ഡ്()
