#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import ବାସ୍ତବ_ମେସିନ୍, ଅବସ୍ଥାନ
from 자바시험 import ସଂପାଦନା_ମୂଲ୍ୟ, ଅତିଥି_ଫାଇଲ୍

def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ():
    ମାପ = {}
    ଉତ୍ସ = (ଅବସ୍ଥାନ.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        ମେସିନ୍ = ବାସ୍ତବ_ମେସିନ୍(ଅବସ୍ଥାନ / ('build/kernel.' + 종류), 종류, ନେଟ୍_ୱାର୍କ୍_ମୂଲ୍ୟ=False)
        try:
            ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'FileDemo.java', ଉତ୍ସ)
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ବାରମ୍ବାର_ମୂଲ୍ୟ in range(2):
                ନିର୍ଗମ = ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ଏଣ୍ଟ୍ରି_ତାଲିକା = ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('ls', ['java.txt  3 bytes'])
            ଆକାର = int(re.search(r'FileDemo.class\s+(\d+) bytes', ଏଣ୍ଟ୍ରି_ତାଲିକା)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ = Path(임시)
                ଅତିଥି_ଫାଇଲ୍(ମେସିନ୍, 2, ଆକାର, ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'FileDemo.class')
                ଆୟୋଜକ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ), 'FileDemo'], cwd=str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ), universal_newlines=True)
                assert ଆୟୋଜକ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', ଆୟୋଜକ
                assert (ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'java.txt').read_bytes() == b'A\xffB'
            ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'FileDemo.java', ଉତ୍ସ.replace('output.write(65);', 'output.close(); output.write(65);'))
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac FileDemo.java', ['Exit: 0'])
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac FileDemo.java', ['Exit: 0'])
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run hello recovered', ['Exit: 0'])
            ମାପ[종류] = ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି.decode('utf-8', 'replace')
        finally:
            ମେସିନ୍.ବନ୍ଦ_କରନ୍ତୁ()
        print('PASS:', 종류, '게스트 Java ଫାଇଲ ସୃଷ୍ଟି_କରିବା/이어쓰기/ବାଇଟ୍_ମୂଲ୍ୟ/EOF/닫힘/ବିଫଳତା_ମୂଲ୍ୟ/OpenJDK 교차 ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ', flush=True)
    (ଅବସ୍ଥାନ / 'build/자바파일시험.json').write_text(json.dumps(ମାପ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
