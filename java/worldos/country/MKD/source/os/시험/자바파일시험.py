#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import виртуелен_машина, Позиција
from 자바시험 import уреди_VALUE, гостин_датотека

def Изврши_наредба():
    мерка = {}
    ИЗВОР = (Позиција.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        машина = виртуелен_машина(Позиција / ('build/kernel.' + 종류), 종류, Мрежа_VALUE=False)
        try:
            уреди_VALUE(машина, 'FileDemo.java', ИЗВОР)
            машина.Команда('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for повторување_VALUE in range(2):
                출력 = машина.Команда('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            внес_Список = машина.Команда('ls', ['java.txt  3 bytes'])
            Големина = int(re.search(r'FileDemo.class\s+(\d+) bytes', внес_Список)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Именик_VALUE = Path(임시)
                гостин_датотека(машина, 2, Големина, Именик_VALUE / 'FileDemo.class')
                вдоми = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Именик_VALUE), 'FileDemo'], cwd=str(Именик_VALUE), universal_newlines=True)
                assert вдоми == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', вдоми
                assert (Именик_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            уреди_VALUE(машина, 'FileDemo.java', ИЗВОР.replace('output.write(65);', 'output.close(); output.write(65);'))
            машина.Команда('javac FileDemo.java', ['Exit: 0'])
            машина.Команда('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            уреди_VALUE(машина, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            машина.Команда('javac FileDemo.java', ['Exit: 0'])
            машина.Команда('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            машина.Команда('run hello recovered', ['Exit: 0'])
            мерка[종류] = машина.LOG_ред.decode('utf-8', 'replace')
        finally:
            машина.Затвори()
        print('PASS:', 종류, '게스트 Java Датотека генерира/이어쓰기/бајт_VALUE/EOF/닫힘/неуспех_VALUE/OpenJDK 교차 Изврши_наредба', flush=True)
    (Позиција / 'build/자바파일시험.json').write_text(json.dumps(мерка, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Изврши_наредба()
