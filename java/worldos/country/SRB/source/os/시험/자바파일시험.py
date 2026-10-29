#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import виртуелно_рачунар, Положај
from 자바시험 import Уреди_вриједност, гост_фајл

def Изврши_команда():
    ИСХОД = {}
    ИЗВОР = (Положај.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        рачунар = виртуелно_рачунар(Положај / ('build/kernel.' + 종류), 종류, Мрежа_вриједност=False)
        try:
            Уреди_вриједност(рачунар, 'FileDemo.java', ИЗВОР)
            рачунар.Наредба('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for спринт_вриједност in range(2):
                Излаз = рачунар.Наредба('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            унос_Листа = рачунар.Наредба('ls', ['java.txt  3 bytes'])
            Величина = int(re.search(r'FileDemo.class\s+(\d+) bytes', унос_Листа)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                именик_вриједност = Path(임시)
                гост_фајл(рачунар, 2, Величина, именик_вриједност / 'FileDemo.class')
                хост = subprocess.check_output(['java', '-Xverify:all', '-cp', str(именик_вриједност), 'FileDemo'], cwd=str(именик_вриједност), universal_newlines=True)
                assert хост == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', хост
                assert (именик_вриједност / 'java.txt').read_bytes() == b'A\xffB'
            Уреди_вриједност(рачунар, 'FileDemo.java', ИЗВОР.replace('output.write(65);', 'output.close(); output.write(65);'))
            рачунар.Наредба('javac FileDemo.java', ['Exit: 0'])
            рачунар.Наредба('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Уреди_вриједност(рачунар, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            рачунар.Наредба('javac FileDemo.java', ['Exit: 0'])
            рачунар.Наредба('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            рачунар.Наредба('run hello recovered', ['Exit: 0'])
            ИСХОД[종류] = рачунар.евиденција_ред.decode('utf-8', 'replace')
        finally:
            рачунар.Затворен()
        print('PASS:', 종류, '게스트 Java Датотека генерисати/이어쓰기/бајт_вриједност/EOF/닫힘/неуспјех_вриједност/OpenJDK 교차 Изврши_команда', flush=True)
    (Положај / 'build/자바파일시험.json').write_text(json.dumps(ИСХОД, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Изврши_команда()
