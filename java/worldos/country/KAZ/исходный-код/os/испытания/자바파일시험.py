#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from тест_пользователь_сеть import VM, позиция
from 자바시험 import правка_ЗНАЧЕН, гость_файл

def 실행():
    результат = {}
    исходныйКод = (позиция.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for Вид_ЗНАЧЕН in ('elf', 'iso'):
        компьютер_5eb260fa = VM(позиция / ('build/kernel.' + Вид_ЗНАЧЕН), Вид_ЗНАЧЕН, сеть_ЗНАЧЕН=False)
        try:
            правка_ЗНАЧЕН(компьютер_5eb260fa, 'FileDemo.java', исходныйКод)
            компьютер_5eb260fa.команда('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for спринт_ЗНАЧЕН in range(2):
                текстовыйВывод = компьютер_5eb260fa.команда('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ввод_Список = компьютер_5eb260fa.команда('ls', ['java.txt  3 bytes'])
            Размер = int(re.search(r'FileDemo.class\s+(\d+) bytes', ввод_Список)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Каталог_ЗНАЧЕН = Path(임시)
                гость_файл(компьютер_5eb260fa, 2, Размер, Каталог_ЗНАЧЕН / 'FileDemo.class')
                узел = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Каталог_ЗНАЧЕН), 'FileDemo'], cwd=str(Каталог_ЗНАЧЕН), universal_newlines=True)
                assert узел == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', узел
                assert (Каталог_ЗНАЧЕН / 'java.txt').read_bytes() == b'A\xffB'
            правка_ЗНАЧЕН(компьютер_5eb260fa, 'FileDemo.java', исходныйКод.replace('output.write(65);', 'output.close(); output.write(65);'))
            компьютер_5eb260fa.команда('javac FileDemo.java', ['Exit: 0'])
            компьютер_5eb260fa.команда('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            правка_ЗНАЧЕН(компьютер_5eb260fa, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            компьютер_5eb260fa.команда('javac FileDemo.java', ['Exit: 0'])
            компьютер_5eb260fa.команда('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            компьютер_5eb260fa.команда('run hello recovered', ['Exit: 0'])
            результат[Вид_ЗНАЧЕН] = компьютер_5eb260fa.LOG_ЗАПИСЬ.decode('utf-8', 'replace')
        finally:
            компьютер_5eb260fa.Закрыть()
        print('PASS:', Вид_ЗНАЧЕН, '게스트 Java файл генерировать/이어쓰기/байт_ЗНАЧЕН/EOF/ИТ_службы_закрыто/сбой_ЗНАЧЕН/OpenJDK 교차 실행', flush=True)
    (позиция / 'build/자바파일시험.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    실행()
