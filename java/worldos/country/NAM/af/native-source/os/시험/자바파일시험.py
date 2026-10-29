#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import virtueel_masjien, Posisie
from 자바시험 import redigeer_VALUE, gas_lêer

def uitvoer_bevel():
    maatreël = {}
    Bron = (Posisie.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        masjien = virtueel_masjien(Posisie / ('build/kernel.' + 종류), 종류, Netwerk_VALUE=False)
        try:
            redigeer_VALUE(masjien, 'FileDemo.java', Bron)
            masjien.Opdrag('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALUE in range(2):
                Afvoer = masjien.Opdrag('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            inskrywing_Lys = masjien.Opdrag('ls', ['java.txt  3 bytes'])
            Grootte = int(re.search(r'FileDemo.class\s+(\d+) bytes', inskrywing_Lys)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                gids_VALUE = Path(임시)
                gas_lêer(masjien, 2, Grootte, gids_VALUE / 'FileDemo.class')
                hou = subprocess.check_output(['java', '-Xverify:all', '-cp', str(gids_VALUE), 'FileDemo'], cwd=str(gids_VALUE), universal_newlines=True)
                assert hou == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', hou
                assert (gids_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            redigeer_VALUE(masjien, 'FileDemo.java', Bron.replace('output.write(65);', 'output.close(); output.write(65);'))
            masjien.Opdrag('javac FileDemo.java', ['Exit: 0'])
            masjien.Opdrag('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            redigeer_VALUE(masjien, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            masjien.Opdrag('javac FileDemo.java', ['Exit: 0'])
            masjien.Opdrag('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            masjien.Opdrag('run hello recovered', ['Exit: 0'])
            maatreël[종류] = masjien.LOG_ry.decode('utf-8', 'replace')
        finally:
            masjien.Sluit()
        print('PASS:', 종류, '게스트 Java Lêer genereer/이어쓰기/greep_VALUE/EOF/닫힘/faling_VALUE/OpenJDK 교차 uitvoer_bevel', flush=True)
    (Posisie / 'build/자바파일시험.json').write_text(json.dumps(maatreël, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    uitvoer_bevel()
