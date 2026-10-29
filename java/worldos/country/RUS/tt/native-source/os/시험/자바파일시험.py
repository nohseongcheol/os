#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import виртуаль_машина, урнаштыру
from 자바시험 import төзәтү_VALUE, кунак_файл

def үтәргә_команда():
    үлчәм = {}
    чыганак = (урнаштыру.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        машина = виртуаль_машина(урнаштыру / ('build/kernel.' + 종류), 종류, Челтәр_VALUE=False)
        try:
            төзәтү_VALUE(машина, 'FileDemo.java', чыганак)
            машина.команда('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for итерация_VALUE in range(2):
                출력 = машина.команда('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            кертү_Исемлек = машина.команда('ls', ['java.txt  3 bytes'])
            үлчәмен_үзгәртү = int(re.search(r'FileDemo.class\s+(\d+) bytes', кертү_Исемлек)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                каталог_VALUE = Path(임시)
                кунак_файл(машина, 2, үлчәмен_үзгәртү, каталог_VALUE / 'FileDemo.class')
                хост = subprocess.check_output(['java', '-Xverify:all', '-cp', str(каталог_VALUE), 'FileDemo'], cwd=str(каталог_VALUE), universal_newlines=True)
                assert хост == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', хост
                assert (каталог_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            төзәтү_VALUE(машина, 'FileDemo.java', чыганак.replace('output.write(65);', 'output.close(); output.write(65);'))
            машина.команда('javac FileDemo.java', ['Exit: 0'])
            машина.команда('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            төзәтү_VALUE(машина, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            машина.команда('javac FileDemo.java', ['Exit: 0'])
            машина.команда('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            машина.команда('run hello recovered', ['Exit: 0'])
            үлчәм[종류] = машина.LOG_юл.decode('utf-8', 'replace')
        finally:
            машина.Yap()
        print('PASS:', 종류, '게스트 Java Birem булдыру/이어쓰기/байт_VALUE/EOF/닫힘/эштән_туктау_VALUE/OpenJDK 교차 үтәргә_команда', flush=True)
    (урнаштыру / 'build/자바파일시험.json').write_text(json.dumps(үлчәм, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    үтәргә_команда()
