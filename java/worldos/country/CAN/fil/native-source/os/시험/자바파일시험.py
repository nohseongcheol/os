#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import virtual_machine, posisyon
from 자바시험 import edit_VALUE, bisita_file

def Mag_execute_utos():
    sukat = {}
    pinagmulan = (posisyon.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        machine = virtual_machine(posisyon / ('build/kernel.' + 종류), 종류, Network_VALUE=False)
        try:
            edit_VALUE(machine, 'FileDemo.java', pinagmulan)
            machine.utos('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALUE in range(2):
                출력 = machine.utos('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            pagpasok_list = machine.utos('ls', ['java.txt  3 bytes'])
            sukat_82232621 = int(re.search(r'FileDemo.class\s+(\d+) bytes', pagpasok_list)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Directory_VALUE = Path(임시)
                bisita_file(machine, 2, sukat_82232621, Directory_VALUE / 'FileDemo.class')
                host = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Directory_VALUE), 'FileDemo'], cwd=str(Directory_VALUE), universal_newlines=True)
                assert host == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', host
                assert (Directory_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            edit_VALUE(machine, 'FileDemo.java', pinagmulan.replace('output.write(65);', 'output.close(); output.write(65);'))
            machine.utos('javac FileDemo.java', ['Exit: 0'])
            machine.utos('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            edit_VALUE(machine, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            machine.utos('javac FileDemo.java', ['Exit: 0'])
            machine.utos('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            machine.utos('run hello recovered', ['Exit: 0'])
            sukat[종류] = machine.LOG_hanay.decode('utf-8', 'replace')
        finally:
            machine.isara()
        print('PASS:', 종류, '게스트 Java file mag_generate/이어쓰기/byte_VALUE/EOF/닫힘/pagpalya_VALUE/OpenJDK 교차 Mag_execute_utos', flush=True)
    (posisyon / 'build/자바파일시험.json').write_text(json.dumps(sukat, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Mag_execute_utos()
