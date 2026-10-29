#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import virtual_makinë, Pozicioni
from 자바시험 import redaktim_VALUE, i_ftuar_skedar

def zbatoj_komandë():
    llogaritje = {}
    BURIMI = (Pozicioni.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        makinë = virtual_makinë(Pozicioni / ('build/kernel.' + 종류), 종류, rrjet_VALUE=False)
        try:
            redaktim_VALUE(makinë, 'FileDemo.java', BURIMI)
            makinë.Komanda('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for përsëritje_VALUE in range(2):
                출력 = makinë.Komanda('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            futje_Listë = makinë.Komanda('ls', ['java.txt  3 bytes'])
            Madhësi = int(re.search(r'FileDemo.class\s+(\d+) bytes', futje_Listë)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                direktori_VALUE = Path(임시)
                i_ftuar_skedar(makinë, 2, Madhësi, direktori_VALUE / 'FileDemo.class')
                pritës = subprocess.check_output(['java', '-Xverify:all', '-cp', str(direktori_VALUE), 'FileDemo'], cwd=str(direktori_VALUE), universal_newlines=True)
                assert pritës == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', pritës
                assert (direktori_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            redaktim_VALUE(makinë, 'FileDemo.java', BURIMI.replace('output.write(65);', 'output.close(); output.write(65);'))
            makinë.Komanda('javac FileDemo.java', ['Exit: 0'])
            makinë.Komanda('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            redaktim_VALUE(makinë, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            makinë.Komanda('javac FileDemo.java', ['Exit: 0'])
            makinë.Komanda('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            makinë.Komanda('run hello recovered', ['Exit: 0'])
            llogaritje[종류] = makinë.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            makinë.Mbyll()
        print('PASS:', 종류, '게스트 Java Kartelë gjeneroj/이어쓰기/bajt_VALUE/EOF/닫힘/dështim_VALUE/OpenJDK 교차 zbatoj_komandë', flush=True)
    (Pozicioni / 'build/자바파일시험.json').write_text(json.dumps(llogaritje, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    zbatoj_komandë()
