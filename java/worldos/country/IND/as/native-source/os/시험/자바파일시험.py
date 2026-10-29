#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import ভাৰ্ছুৱেল_মেচিন, অৱস্থান
from 자바시험 import সম্পাদনা_মান, অতিথি_ফাইল

def নিষ্পাদন_আদেশ():
    পৰিমাপ = {}
    উৎস = (অৱস্থান.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        মেচিন = ভাৰ্ছুৱেল_মেচিন(অৱস্থান / ('build/kernel.' + 종류), 종류, নেটৱৰ্ক_মান=False)
        try:
            সম্পাদনা_মান(মেচিন, 'FileDemo.java', উৎস)
            মেচিন.কমান্ড('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for পুণৰাবৃত্তি_মান in range(2):
                নিৰ্গম = মেচিন.কমান্ড('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            প্রবিষ্ট_সূচী = মেচিন.কমান্ড('ls', ['java.txt  3 bytes'])
            মাপ = int(re.search(r'FileDemo.class\s+(\d+) bytes', প্রবিষ্ট_সূচী)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ডাইৰেক্টৰী_মান = Path(임시)
                অতিথি_ফাইল(মেচিন, 2, মাপ, ডাইৰেক্টৰী_মান / 'FileDemo.class')
                হ_ষ্ট = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ডাইৰেক্টৰী_মান), 'FileDemo'], cwd=str(ডাইৰেক্টৰী_মান), universal_newlines=True)
                assert হ_ষ্ট == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', হ_ষ্ট
                assert (ডাইৰেক্টৰী_মান / 'java.txt').read_bytes() == b'A\xffB'
            সম্পাদনা_মান(মেচিন, 'FileDemo.java', উৎস.replace('output.write(65);', 'output.close(); output.write(65);'))
            মেচিন.কমান্ড('javac FileDemo.java', ['Exit: 0'])
            মেচিন.কমান্ড('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            সম্পাদনা_মান(মেচিন, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            মেচিন.কমান্ড('javac FileDemo.java', ['Exit: 0'])
            মেচিন.কমান্ড('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            মেচিন.কমান্ড('run hello recovered', ['Exit: 0'])
            পৰিমাপ[종류] = মেচিন.লগ_শাৰী.decode('utf-8', 'replace')
        finally:
            মেচিন.বন্ধ_কৰক()
        print('PASS:', 종류, '게스트 Java নথিপত্ৰ সৃষ্টি_কৰক/이어쓰기/বাইট_মান/EOF/닫힘/বিফলতা_মান/OpenJDK 교차 নিষ্পাদন_আদেশ', flush=True)
    (অৱস্থান / 'build/자바파일시험.json').write_text(json.dumps(পৰিমাপ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    নিষ্পাদন_আদেশ()
