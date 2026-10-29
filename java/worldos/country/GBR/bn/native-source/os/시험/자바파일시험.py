#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import কল্পিত_মেশিন, অবস্থান
from 자바시험 import সম্পাদন_মান, অতিথি_ফাইল

def কার্যকর_করুন_আদেশ():
    পরিমাপ = {}
    উৎস_নথি = (অবস্থান.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        মেশিন = কল্পিত_মেশিন(অবস্থান / ('build/kernel.' + 종류), 종류, নেটওয়ার্ক_মান=False)
        try:
            সম্পাদন_মান(মেশিন, 'FileDemo.java', উৎস_নথি)
            মেশিন.আদেশ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for পুনরুক্তি_মান in range(2):
                নির্গম = মেশিন.আদেশ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ভুক্তি_তালিকা = মেশিন.আদেশ('ls', ['java.txt  3 bytes'])
            আকার = int(re.search(r'FileDemo.class\s+(\d+) bytes', ভুক্তি_তালিকা)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ডিরেক্টরি_মান = Path(임시)
                অতিথি_ফাইল(মেশিন, 2, আকার, ডিরেক্টরি_মান / 'FileDemo.class')
                হোস্ট = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ডিরেক্টরি_মান), 'FileDemo'], cwd=str(ডিরেক্টরি_মান), universal_newlines=True)
                assert হোস্ট == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', হোস্ট
                assert (ডিরেক্টরি_মান / 'java.txt').read_bytes() == b'A\xffB'
            সম্পাদন_মান(মেশিন, 'FileDemo.java', উৎস_নথি.replace('output.write(65);', 'output.close(); output.write(65);'))
            মেশিন.আদেশ('javac FileDemo.java', ['Exit: 0'])
            মেশিন.আদেশ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            সম্পাদন_মান(মেশিন, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            মেশিন.আদেশ('javac FileDemo.java', ['Exit: 0'])
            মেশিন.আদেশ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            মেশিন.আদেশ('run hello recovered', ['Exit: 0'])
            পরিমাপ[종류] = মেশিন.লগ_সারি.decode('utf-8', 'replace')
        finally:
            মেশিন.বন্ধ_করুন()
        print('PASS:', 종류, '게스트 Java নথির_নাম সৃষ্টি_করুন/이어쓰기/বাইট_মান/EOF/닫힘/বিফলতা_মান/OpenJDK 교차 কার্যকর_করুন_আদেশ', flush=True)
    (অবস্থান / 'build/자바파일시험.json').write_text(json.dumps(পরিমাপ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    কার্যকর_করুন_আদেশ()
