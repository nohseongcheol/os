#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import 가상기계, ځای
from 자바시험 import سمون_ارزښت, 게스트파일

def 실행():
    결과 = {}
    سرچينه = (ځای.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        기계 = 가상기계(ځای / ('build/kernel.' + 종류), 종류, جال_ارزښت=False)
        try:
            سمون_ارزښت(기계, 'FileDemo.java', سرچينه)
            기계.بولۍ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for تکرار_ارزښت in range(2):
                출력 = 기계.بولۍ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            목록 = 기계.بولۍ('ls', ['java.txt  3 bytes'])
            کچ = int(re.search(r'FileDemo.class\s+(\d+) bytes', 목록)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                نوملړ_ارزښت = Path(임시)
                게스트파일(기계, 2, کچ, نوملړ_ارزښت / 'FileDemo.class')
                کوربه = subprocess.check_output(['java', '-Xverify:all', '-cp', str(نوملړ_ارزښت), 'FileDemo'], cwd=str(نوملړ_ارزښت), universal_newlines=True)
                assert کوربه == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', کوربه
                assert (نوملړ_ارزښت / 'java.txt').read_bytes() == b'A\xffB'
            سمون_ارزښت(기계, 'FileDemo.java', سرچينه.replace('output.write(65);', 'output.close(); output.write(65);'))
            기계.بولۍ('javac FileDemo.java', ['Exit: 0'])
            기계.بولۍ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            سمون_ارزښت(기계, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            기계.بولۍ('javac FileDemo.java', ['Exit: 0'])
            기계.بولۍ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            기계.بولۍ('run hello recovered', ['Exit: 0'])
            결과[종류] = 기계.خبرال_کیل.decode('utf-8', 'replace')
        finally:
            기계.بندول()
        print('PASS:', 종류, '게스트 Java دوتنه 생성/이어쓰기/بايټ_ارزښت/EOF/닫힘/پاتېينه_ارزښت/OpenJDK 교차 실행', flush=True)
    (ځای / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    실행()
