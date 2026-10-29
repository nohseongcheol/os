#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import виртуална_машина, Позиция
from 자바시험 import редакция_стойност, гост_Файл

def изпълнявам_команда():
    РЕЗУЛТАТ = {}
    ИЗТОЧНИК = (Позиция.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        машина = виртуална_машина(Позиция / ('build/kernel.' + 종류), 종류, мрежа_стойност=False)
        try:
            редакция_стойност(машина, 'FileDemo.java', ИЗТОЧНИК)
            машина.Команда('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for спринт_стойност in range(2):
                Изход = машина.Команда('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            запис_Списък = машина.Команда('ls', ['java.txt  3 bytes'])
            Размер = int(re.search(r'FileDemo.class\s+(\d+) bytes', запис_Списък)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                указател_стойност = Path(임시)
                гост_Файл(машина, 2, Размер, указател_стойност / 'FileDemo.class')
                хост = subprocess.check_output(['java', '-Xverify:all', '-cp', str(указател_стойност), 'FileDemo'], cwd=str(указател_стойност), universal_newlines=True)
                assert хост == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', хост
                assert (указател_стойност / 'java.txt').read_bytes() == b'A\xffB'
            редакция_стойност(машина, 'FileDemo.java', ИЗТОЧНИК.replace('output.write(65);', 'output.close(); output.write(65);'))
            машина.Команда('javac FileDemo.java', ['Exit: 0'])
            машина.Команда('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            редакция_стойност(машина, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            машина.Команда('javac FileDemo.java', ['Exit: 0'])
            машина.Команда('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            машина.Команда('run hello recovered', ['Exit: 0'])
            РЕЗУЛТАТ[종류] = машина.регистрирам_запис.decode('utf-8', 'replace')
        finally:
            машина.Затворен()
        print('PASS:', 종류, '게스트 Java Файл генерирам/이어쓰기/байт_стойност/EOF/닫힘/отказ_стойност/OpenJDK 교차 изпълнявам_команда', flush=True)
    (Позиция / 'build/자바파일시험.json').write_text(json.dumps(РЕЗУЛТАТ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    изпълнявам_команда()
