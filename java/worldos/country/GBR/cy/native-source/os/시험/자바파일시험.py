#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import rhith_peiriant, safle
from 자바시험 import Golygu_VALUE, gwestai_ffeil

def Gweithredu_gorchymyn():
    mesur = {}
    FFYNHONNELL = (safle.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        peiriant = rhith_peiriant(safle / ('build/kernel.' + 종류), 종류, Rhwydwaith_VALUE=False)
        try:
            Golygu_VALUE(peiriant, 'FileDemo.java', FFYNHONNELL)
            peiriant.Gorchymyn('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for iteriad_VALUE in range(2):
                Allbwn = peiriant.Gorchymyn('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            cofnod_Rhestr = peiriant.Gorchymyn('ls', ['java.txt  3 bytes'])
            Maint = int(re.search(r'FileDemo.class\s+(\d+) bytes', cofnod_Rhestr)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                cyfeiriadur_VALUE = Path(임시)
                gwestai_ffeil(peiriant, 2, Maint, cyfeiriadur_VALUE / 'FileDemo.class')
                lletya = subprocess.check_output(['java', '-Xverify:all', '-cp', str(cyfeiriadur_VALUE), 'FileDemo'], cwd=str(cyfeiriadur_VALUE), universal_newlines=True)
                assert lletya == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', lletya
                assert (cyfeiriadur_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            Golygu_VALUE(peiriant, 'FileDemo.java', FFYNHONNELL.replace('output.write(65);', 'output.close(); output.write(65);'))
            peiriant.Gorchymyn('javac FileDemo.java', ['Exit: 0'])
            peiriant.Gorchymyn('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Golygu_VALUE(peiriant, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            peiriant.Gorchymyn('javac FileDemo.java', ['Exit: 0'])
            peiriant.Gorchymyn('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            peiriant.Gorchymyn('run hello recovered', ['Exit: 0'])
            mesur[종류] = peiriant.LOG_rhes.decode('utf-8', 'replace')
        finally:
            peiriant.Cau()
        print('PASS:', 종류, '게스트 Java Ffeil cynhyrchu/이어쓰기/beit_VALUE/EOF/닫힘/methiant_VALUE/OpenJDK 교차 Gweithredu_gorchymyn', flush=True)
    (safle / 'build/자바파일시험.json').write_text(json.dumps(mesur, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Gweithredu_gorchymyn()
