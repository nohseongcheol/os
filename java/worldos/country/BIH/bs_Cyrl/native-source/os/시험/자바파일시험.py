#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import 가상기계, 위치
from 자바시험 import уређивати_вриједност, 게스트파일

def 실행():
    결과 = {}
    извор = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        기계 = 가상기계(위치 / ('build/kernel.' + 종류), 종류, Мрежа_вриједност=False)
        try:
            уређивати_вриједност(기계, 'FileDemo.java', извор)
            기계.команда('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for понављање_вриједност in range(2):
                출력 = 기계.команда('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            унос_списак = 기계.команда('ls', ['java.txt  3 bytes'])
            подесити_величину = int(re.search(r'FileDemo.class\s+(\d+) bytes', унос_списак)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                директориј_вриједност = Path(임시)
                게스트파일(기계, 2, подесити_величину, директориј_вриједност / 'FileDemo.class')
                хост_рачунар = subprocess.check_output(['java', '-Xverify:all', '-cp', str(директориј_вриједност), 'FileDemo'], cwd=str(директориј_вриједност), universal_newlines=True)
                assert хост_рачунар == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', хост_рачунар
                assert (директориј_вриједност / 'java.txt').read_bytes() == b'A\xffB'
            уређивати_вриједност(기계, 'FileDemo.java', извор.replace('output.write(65);', 'output.close(); output.write(65);'))
            기계.команда('javac FileDemo.java', ['Exit: 0'])
            기계.команда('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            уређивати_вриједност(기계, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            기계.команда('javac FileDemo.java', ['Exit: 0'])
            기계.команда('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            기계.команда('run hello recovered', ['Exit: 0'])
            결과[종류] = 기계.дневник_рада_ред.decode('utf-8', 'replace')
        finally:
            기계.затворити()
        print('PASS:', 종류, '게스트 Java фајл 생성/이어쓰기/бајт_вриједност/EOF/닫힘/неуспјех_вриједност/OpenJDK 교차 실행', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    실행()
