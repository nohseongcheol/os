#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import ვირტუალური_კომპიუტერი, პოზიცია
from 자바시험 import რედაქტირება_მნიშვნელობა, სტუმარი_ფაილი

def შესრულება_ბრძანება():
    გაზომვა = {}
    წყარო = (პოზიცია.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        კომპიუტერი = ვირტუალური_კომპიუტერი(პოზიცია / ('build/kernel.' + 종류), 종류, ქსელი_მნიშვნელობა=False)
        try:
            რედაქტირება_მნიშვნელობა(კომპიუტერი, 'FileDemo.java', წყარო)
            კომპიუტერი.ბრძანება('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for იტერაცია_მნიშვნელობა in range(2):
                출력 = კომპიუტერი.ბრძანება('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            შენატანი_სია = კომპიუტერი.ბრძანება('ls', ['java.txt  3 bytes'])
            ზომა = int(re.search(r'FileDemo.class\s+(\d+) bytes', შენატანი_სია)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                საქაღალდე_მნიშვნელობა = Path(임시)
                სტუმარი_ფაილი(კომპიუტერი, 2, ზომა, საქაღალდე_მნიშვნელობა / 'FileDemo.class')
                მასპინძელი = subprocess.check_output(['java', '-Xverify:all', '-cp', str(საქაღალდე_მნიშვნელობა), 'FileDemo'], cwd=str(საქაღალდე_მნიშვნელობა), universal_newlines=True)
                assert მასპინძელი == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', მასპინძელი
                assert (საქაღალდე_მნიშვნელობა / 'java.txt').read_bytes() == b'A\xffB'
            რედაქტირება_მნიშვნელობა(კომპიუტერი, 'FileDemo.java', წყარო.replace('output.write(65);', 'output.close(); output.write(65);'))
            კომპიუტერი.ბრძანება('javac FileDemo.java', ['Exit: 0'])
            კომპიუტერი.ბრძანება('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            რედაქტირება_მნიშვნელობა(კომპიუტერი, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            კომპიუტერი.ბრძანება('javac FileDemo.java', ['Exit: 0'])
            კომპიუტერი.ბრძანება('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            კომპიუტერი.ბრძანება('run hello recovered', ['Exit: 0'])
            გაზომვა[종류] = კომპიუტერი.ჟურნალი_ჩაწერა.decode('utf-8', 'replace')
        finally:
            კომპიუტერი.დახურვა()
        print('PASS:', 종류, '게스트 Java ფაილი დაგენერირება/이어쓰기/ბაიტი_მნიშვნელობა/EOF/닫힘/მარცხი_მნიშვნელობა/OpenJDK 교차 შესრულება_ბრძანება', flush=True)
    (პოზიცია / 'build/자바파일시험.json').write_text(json.dumps(გაზომვა, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    შესრულება_ბრძანება()
