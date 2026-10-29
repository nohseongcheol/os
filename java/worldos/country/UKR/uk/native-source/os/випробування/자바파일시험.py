#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import ВМ, позиція
from 자바시험 import правка_значення, гість_Файл

def Виконати_команда():
    результат = {}
    вихіднийКод = (позиція.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        комп_ютер = ВМ(позиція / ('build/kernel.' + 종류), 종류, мережа_значення=False)
        try:
            правка_значення(комп_ютер, 'FileDemo.java', вихіднийКод)
            комп_ютер.команда('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for спринт_значення in range(2):
                Вивід = комп_ютер.команда('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            запис_список = комп_ютер.команда('ls', ['java.txt  3 bytes'])
            Розмір = int(re.search(r'FileDemo.class\s+(\d+) bytes', запис_список)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Каталог_значення = Path(임시)
                гість_Файл(комп_ютер, 2, Розмір, Каталог_значення / 'FileDemo.class')
                хост = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Каталог_значення), 'FileDemo'], cwd=str(Каталог_значення), universal_newlines=True)
                assert хост == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', хост
                assert (Каталог_значення / 'java.txt').read_bytes() == b'A\xffB'
            правка_значення(комп_ютер, 'FileDemo.java', вихіднийКод.replace('output.write(65);', 'output.close(); output.write(65);'))
            комп_ютер.команда('javac FileDemo.java', ['Exit: 0'])
            комп_ютер.команда('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            правка_значення(комп_ютер, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            комп_ютер.команда('javac FileDemo.java', ['Exit: 0'])
            комп_ютер.команда('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            комп_ютер.команда('run hello recovered', ['Exit: 0'])
            результат[종류] = комп_ютер.журнал_запис.decode('utf-8', 'replace')
        finally:
            комп_ютер.Закрити()
        print('PASS:', 종류, '게스트 Java файл генерувати/이어쓰기/байт_значення/EOF/닫힘/неполадка_значення/OpenJDK 교차 Виконати_команда', flush=True)
    (позиція / 'build/자바파일시험.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Виконати_команда()
