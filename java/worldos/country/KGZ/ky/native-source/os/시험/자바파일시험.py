#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import виртуалдык_машина, Турган_жери
from 자바시험 import түзөтүү_маани, 게스트파일

def аткаруу_буйрук():
    결과 = {}
    Булак = (Турган_жери.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        машина = виртуалдык_машина(Турган_жери / ('build/kernel.' + 종류), 종류, Желе_маани=False)
        try:
            түзөтүү_маани(машина, 'FileDemo.java', Булак)
            машина.Команда('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for итерация_маани in range(2):
                Чыгыш = машина.Команда('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            киргизме_жазуу_Тизме = машина.Команда('ls', ['java.txt  3 bytes'])
            Өлчөмү = int(re.search(r'FileDemo.class\s+(\d+) bytes', киргизме_жазуу_Тизме)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                каталог_маани = Path(임시)
                게스트파일(машина, 2, Өлчөмү, каталог_маани / 'FileDemo.class')
                кабылдоо = subprocess.check_output(['java', '-Xverify:all', '-cp', str(каталог_маани), 'FileDemo'], cwd=str(каталог_маани), universal_newlines=True)
                assert кабылдоо == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', кабылдоо
                assert (каталог_маани / 'java.txt').read_bytes() == b'A\xffB'
            түзөтүү_маани(машина, 'FileDemo.java', Булак.replace('output.write(65);', 'output.close(); output.write(65);'))
            машина.Команда('javac FileDemo.java', ['Exit: 0'])
            машина.Команда('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            түзөтүү_маани(машина, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            машина.Команда('javac FileDemo.java', ['Exit: 0'])
            машина.Команда('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            машина.Команда('run hello recovered', ['Exit: 0'])
            결과[종류] = машина.жазуу_катар.decode('utf-8', 'replace')
        finally:
            машина.Жабуу()
        print('PASS:', 종류, '게스트 Java Файл 생성/이어쓰기/байт_маани/EOF/닫힘/натыйжасыз_маани/OpenJDK 교차 аткаруу_буйрук', flush=True)
    (Турган_жери / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    аткаруу_буйрук()
