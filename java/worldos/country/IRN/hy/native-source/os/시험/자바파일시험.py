#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import վիրտուալ_մեքենա, Դիրք
from 자바시험 import խմբագրել_արժեք, հյուր_նիշք

def կատարել_հրաման():
    չափ = {}
    ԱՂԲՅՈՒՐ = (Դիրք.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        մեքենա = վիրտուալ_մեքենա(Դիրք / ('build/kernel.' + 종류), 종류, Ցանց_արժեք=False)
        try:
            խմբագրել_արժեք(մեքենա, 'FileDemo.java', ԱՂԲՅՈՒՐ)
            մեքենա.Հրահանգ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for բազմակրկնություն_արժեք in range(2):
                Ելք = մեքենա.Հրահանգ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            մուտքագրում_Ցուցակ = մեքենա.Հրահանգ('ls', ['java.txt  3 bytes'])
            Չափս = int(re.search(r'FileDemo.class\s+(\d+) bytes', մուտքագրում_Ցուցակ)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                գրացուցակ_արժեք = Path(임시)
                հյուր_նիշք(մեքենա, 2, Չափս, գրացուցակ_արժեք / 'FileDemo.class')
                հոստ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(գրացուցակ_արժեք), 'FileDemo'], cwd=str(գրացուցակ_արժեք), universal_newlines=True)
                assert հոստ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', հոստ
                assert (գրացուցակ_արժեք / 'java.txt').read_bytes() == b'A\xffB'
            խմբագրել_արժեք(մեքենա, 'FileDemo.java', ԱՂԲՅՈՒՐ.replace('output.write(65);', 'output.close(); output.write(65);'))
            մեքենա.Հրահանգ('javac FileDemo.java', ['Exit: 0'])
            մեքենա.Հրահանգ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            խմբագրել_արժեք(մեքենա, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            մեքենա.Հրահանգ('javac FileDemo.java', ['Exit: 0'])
            մեքենա.Հրահանգ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            մեքենա.Հրահանգ('run hello recovered', ['Exit: 0'])
            չափ[종류] = մեքենա.մատյան_տող.decode('utf-8', 'replace')
        finally:
            մեքենա.Փակ()
        print('PASS:', 종류, '게스트 Java Ֆայլ արտադրել/이어쓰기/բայթ_արժեք/EOF/닫힘/ձախողում_արժեք/OpenJDK 교차 կատարել_հրաման', flush=True)
    (Դիրք / 'build/자바파일시험.json').write_text(json.dumps(չափ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    կատարել_հրաման()
