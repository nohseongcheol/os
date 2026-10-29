#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import виртуал_компьютер, 위치
from 자바시험 import засварлах_утга, 게스트파일

def Гүйцэтгэх_команд():
    결과 = {}
    ЭХ = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        компьютер = виртуал_компьютер(위치 / ('build/kernel.' + 종류), 종류, Сүлжээ_утга=False)
        try:
            засварлах_утга(компьютер, 'FileDemo.java', ЭХ)
            компьютер.Тушаал('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for давталт_утга in range(2):
                출력 = компьютер.Тушаал('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            оролт_Жагсаалт = компьютер.Тушаал('ls', ['java.txt  3 bytes'])
            Хэмжээ = int(re.search(r'FileDemo.class\s+(\d+) bytes', оролт_Жагсаалт)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                лавлах_утга = Path(임시)
                게스트파일(компьютер, 2, Хэмжээ, лавлах_утга / 'FileDemo.class')
                хост = subprocess.check_output(['java', '-Xverify:all', '-cp', str(лавлах_утга), 'FileDemo'], cwd=str(лавлах_утга), universal_newlines=True)
                assert хост == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', хост
                assert (лавлах_утга / 'java.txt').read_bytes() == b'A\xffB'
            засварлах_утга(компьютер, 'FileDemo.java', ЭХ.replace('output.write(65);', 'output.close(); output.write(65);'))
            компьютер.Тушаал('javac FileDemo.java', ['Exit: 0'])
            компьютер.Тушаал('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            засварлах_утга(компьютер, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            компьютер.Тушаал('javac FileDemo.java', ['Exit: 0'])
            компьютер.Тушаал('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            компьютер.Тушаал('run hello recovered', ['Exit: 0'])
            결과[종류] = компьютер.бичих_мөр_6e8b375a.decode('utf-8', 'replace')
        finally:
            компьютер.Хаах()
        print('PASS:', 종류, '게스트 Java Файл 생성/이어쓰기/байт_утга/EOF/닫힘/гэмтэл_утга/OpenJDK 교차 Гүйцэтгэх_команд', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Гүйцэтгэх_команд()
