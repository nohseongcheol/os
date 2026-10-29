#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import віртуальны_камп_ютар, Пазіцыя
from 자바시험 import рэдагаваць_значэнне, госць_файл

def выканаць_каманда():
    결과 = {}
    КРЫНІЦА = (Пазіцыя.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        камп_ютар = віртуальны_камп_ютар(Пазіцыя / ('build/kernel.' + 종류), 종류, Сетка_значэнне=False)
        try:
            рэдагаваць_значэнне(камп_ютар, 'FileDemo.java', КРЫНІЦА)
            камп_ютар.Загад('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for спрынт_значэнне in range(2):
                Выхад = камп_ютар.Загад('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            увядзенне_Спіс = камп_ютар.Загад('ls', ['java.txt  3 bytes'])
            Памер = int(re.search(r'FileDemo.class\s+(\d+) bytes', увядзенне_Спіс)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                каталог_значэнне = Path(임시)
                госць_файл(камп_ютар, 2, Памер, каталог_значэнне / 'FileDemo.class')
                вузел = subprocess.check_output(['java', '-Xverify:all', '-cp', str(каталог_значэнне), 'FileDemo'], cwd=str(каталог_значэнне), universal_newlines=True)
                assert вузел == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', вузел
                assert (каталог_значэнне / 'java.txt').read_bytes() == b'A\xffB'
            рэдагаваць_значэнне(камп_ютар, 'FileDemo.java', КРЫНІЦА.replace('output.write(65);', 'output.close(); output.write(65);'))
            камп_ютар.Загад('javac FileDemo.java', ['Exit: 0'])
            камп_ютар.Загад('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            рэдагаваць_значэнне(камп_ютар, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            камп_ютар.Загад('javac FileDemo.java', ['Exit: 0'])
            камп_ютар.Загад('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            камп_ютар.Загад('run hello recovered', ['Exit: 0'])
            결과[종류] = камп_ютар.журнал_запіс.decode('utf-8', 'replace')
        finally:
            камп_ютар.Закрыць()
        print('PASS:', 종류, '게스트 Java Файл 생성/이어쓰기/байт_значэнне/EOF/닫힘/няўдача_значэнне/OpenJDK 교차 выканаць_каманда', flush=True)
    (Пазіцыя / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    выканаць_каманда()
