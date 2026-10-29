#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import مەۋھۇم_ماشىنا, ئورۇن
from 자바시험 import تەھرىرلەش_قىممىتى, مېھمان_ھۆججەت

def ئىجرا_قىلىش_بۇيرۇق():
    ئۆلچەم = {}
    مەنبە = (ئورۇن.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        ماشىنا = مەۋھۇم_ماشىنا(ئورۇن / ('build/kernel.' + 종류), 종류, تور_قىممىتى=False)
        try:
            تەھرىرلەش_قىممىتى(ماشىنا, 'FileDemo.java', مەنبە)
            ماشىنا.بۇيرۇق('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ئېنتىراتسىيە_قىممىتى in range(2):
                چىقار = ماشىنا.بۇيرۇق('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            كىرگۈزۈش_تىزىم = ماشىنا.بۇيرۇق('ls', ['java.txt  3 bytes'])
            چوڭلۇقى = int(re.search(r'FileDemo.class\s+(\d+) bytes', كىرگۈزۈش_تىزىم)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                مۇندەرىجە_قىممىتى = Path(임시)
                مېھمان_ھۆججەت(ماشىنا, 2, چوڭلۇقى, مۇندەرىجە_قىممىتى / 'FileDemo.class')
                باقار = subprocess.check_output(['java', '-Xverify:all', '-cp', str(مۇندەرىجە_قىممىتى), 'FileDemo'], cwd=str(مۇندەرىجە_قىممىتى), universal_newlines=True)
                assert باقار == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', باقار
                assert (مۇندەرىجە_قىممىتى / 'java.txt').read_bytes() == b'A\xffB'
            تەھرىرلەش_قىممىتى(ماشىنا, 'FileDemo.java', مەنبە.replace('output.write(65);', 'output.close(); output.write(65);'))
            ماشىنا.بۇيرۇق('javac FileDemo.java', ['Exit: 0'])
            ماشىنا.بۇيرۇق('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            تەھرىرلەش_قىممىتى(ماشىنا, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            ماشىنا.بۇيرۇق('javac FileDemo.java', ['Exit: 0'])
            ماشىنا.بۇيرۇق('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            ماشىنا.بۇيرۇق('run hello recovered', ['Exit: 0'])
            ئۆلچەم[종류] = ماشىنا.خاتىرە_قۇر.decode('utf-8', 'replace')
        finally:
            ماشىنا.ياپ()
        print('PASS:', 종류, '게스트 Java ھۆججەت ھاسىل_قىلىش/이어쓰기/بايت_قىممىتى/EOF/닫힘/مەغلۇپ_بولۇش_قىممىتى/OpenJDK 교차 ئىجرا_قىلىش_بۇيرۇق', flush=True)
    (ئورۇن / 'build/자바파일시험.json').write_text(json.dumps(ئۆلچەم, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ئىجرا_قىلىش_بۇيرۇق()
