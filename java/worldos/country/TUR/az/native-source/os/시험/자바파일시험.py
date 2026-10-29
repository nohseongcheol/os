#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import virtual_maşın, yerinə_qoymaq
from 자바시험 import redaktə_VALUE, qonaq_fayl

def icra_etmək_əmr():
    ölçü = {}
    QAYNAQ = (yerinə_qoymaq.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        maşın = virtual_maşın(yerinə_qoymaq / ('build/kernel.' + 종류), 종류, Şəbəkə_VALUE=False)
        try:
            redaktə_VALUE(maşın, 'FileDemo.java', QAYNAQ)
            maşın.Əmr('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for iterasiya_VALUE in range(2):
                출력 = maşın.Əmr('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            daxiletmə_Siyahı = maşın.Əmr('ls', ['java.txt  3 bytes'])
            Böyüklük = int(re.search(r'FileDemo.class\s+(\d+) bytes', daxiletmə_Siyahı)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                kataloq_VALUE = Path(임시)
                qonaq_fayl(maşın, 2, Böyüklük, kataloq_VALUE / 'FileDemo.class')
                host = subprocess.check_output(['java', '-Xverify:all', '-cp', str(kataloq_VALUE), 'FileDemo'], cwd=str(kataloq_VALUE), universal_newlines=True)
                assert host == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', host
                assert (kataloq_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            redaktə_VALUE(maşın, 'FileDemo.java', QAYNAQ.replace('output.write(65);', 'output.close(); output.write(65);'))
            maşın.Əmr('javac FileDemo.java', ['Exit: 0'])
            maşın.Əmr('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            redaktə_VALUE(maşın, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            maşın.Əmr('javac FileDemo.java', ['Exit: 0'])
            maşın.Əmr('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            maşın.Əmr('run hello recovered', ['Exit: 0'])
            ölçü[종류] = maşın.LOG_yaz.decode('utf-8', 'replace')
        finally:
            maşın.Bağla()
        print('PASS:', 종류, '게스트 Java FAYL yarat/이어쓰기/bayt_VALUE/EOF/닫힘/xəta_VALUE/OpenJDK 교차 icra_etmək_əmr', flush=True)
    (yerinə_qoymaq / 'build/자바파일시험.json').write_text(json.dumps(ölçü, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    icra_etmək_əmr()
