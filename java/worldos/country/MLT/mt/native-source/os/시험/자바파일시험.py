#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import virtwali_kompjuter, pożizzjoni
from 자바시험 import editja_VALUE, mistieden_fajl

def eżegwixxa_kmand():
    miżura = {}
    sors = (pożizzjoni.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        kompjuter = virtwali_kompjuter(pożizzjoni / ('build/kernel.' + 종류), 종류, netwerk_VALUE=False)
        try:
            editja_VALUE(kompjuter, 'FileDemo.java', sors)
            kompjuter.kmand('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for iterazzjoni_VALUE in range(2):
                출력 = kompjuter.kmand('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            entrata_Lista = kompjuter.kmand('ls', ['java.txt  3 bytes'])
            daqqas = int(re.search(r'FileDemo.class\s+(\d+) bytes', entrata_Lista)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                direttorju_VALUE = Path(임시)
                mistieden_fajl(kompjuter, 2, daqqas, direttorju_VALUE / 'FileDemo.class')
                host = subprocess.check_output(['java', '-Xverify:all', '-cp', str(direttorju_VALUE), 'FileDemo'], cwd=str(direttorju_VALUE), universal_newlines=True)
                assert host == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', host
                assert (direttorju_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            editja_VALUE(kompjuter, 'FileDemo.java', sors.replace('output.write(65);', 'output.close(); output.write(65);'))
            kompjuter.kmand('javac FileDemo.java', ['Exit: 0'])
            kompjuter.kmand('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            editja_VALUE(kompjuter, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            kompjuter.kmand('javac FileDemo.java', ['Exit: 0'])
            kompjuter.kmand('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            kompjuter.kmand('run hello recovered', ['Exit: 0'])
            miżura[종류] = kompjuter.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            kompjuter.agħlaq()
        print('PASS:', 종류, '게스트 Java fajl iġġenera/이어쓰기/byte_VALUE/EOF/닫힘/żball_VALUE/OpenJDK 교차 eżegwixxa_kmand', flush=True)
    (pożizzjoni / 'build/자바파일시험.json').write_text(json.dumps(miżura, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    eżegwixxa_kmand()
