#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import виртуалды_машина, Орны
from 자바시험 import өңдеу_мән, қонақ_файл

def орындау_пәрмен():
    НӘТИЖЕ = {}
    Неден = (Орны.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        компьютер = виртуалды_машина(Орны / ('build/kernel.' + 종류), 종류, желі_мән=False)
        try:
            өңдеу_мән(компьютер, 'FileDemo.java', Неден)
            компьютер.Команда('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for спринт_мән in range(2):
                Шығысы = компьютер.Команда('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            енгізу_Тізім = компьютер.Команда('ls', ['java.txt  3 bytes'])
            Өлшемі = int(re.search(r'FileDemo.class\s+(\d+) bytes', енгізу_Тізім)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                каталог_мән = Path(임시)
                қонақ_файл(компьютер, 2, Өлшемі, каталог_мән / 'FileDemo.class')
                орналастыру = subprocess.check_output(['java', '-Xverify:all', '-cp', str(каталог_мән), 'FileDemo'], cwd=str(каталог_мән), universal_newlines=True)
                assert орналастыру == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', орналастыру
                assert (каталог_мән / 'java.txt').read_bytes() == b'A\xffB'
            өңдеу_мән(компьютер, 'FileDemo.java', Неден.replace('output.write(65);', 'output.close(); output.write(65);'))
            компьютер.Команда('javac FileDemo.java', ['Exit: 0'])
            компьютер.Команда('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            өңдеу_мән(компьютер, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            компьютер.Команда('javac FileDemo.java', ['Exit: 0'])
            компьютер.Команда('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            компьютер.Команда('run hello recovered', ['Exit: 0'])
            НӘТИЖЕ[종류] = компьютер.журнал_жол.decode('utf-8', 'replace')
        finally:
            компьютер.Жабу()
        print('PASS:', 종류, '게스트 Java Файл жасау/이어쓰기/байт_мән/EOF/닫힘/қате_мән/OpenJDK 교차 орындау_пәрмен', flush=True)
    (Орны / 'build/자바파일시험.json').write_text(json.dumps(НӘТИЖЕ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    орындау_пәрмен()
