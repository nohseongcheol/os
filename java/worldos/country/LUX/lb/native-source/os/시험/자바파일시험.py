#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import virtuell_Computer, positionéieren
from 자바시험 import Editéieren_VALUE, Gaascht_Fichier

def ausféieren_Befeel():
    Mooss = {}
    Quell = (positionéieren.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        Computer = virtuell_Computer(positionéieren / ('build/kernel.' + 종류), 종류, Reseau_VALUE=False)
        try:
            Editéieren_VALUE(Computer, 'FileDemo.java', Quell)
            Computer.Befeel('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for Iteratioun_VALUE in range(2):
                출력 = Computer.Befeel('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            Agab_Lëscht = Computer.Befeel('ls', ['java.txt  3 bytes'])
            d_Gréisst_veränneren = int(re.search(r'FileDemo.class\s+(\d+) bytes', Agab_Lëscht)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Verzeechnes_VALUE = Path(임시)
                Gaascht_Fichier(Computer, 2, d_Gréisst_veränneren, Verzeechnes_VALUE / 'FileDemo.class')
                Host = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Verzeechnes_VALUE), 'FileDemo'], cwd=str(Verzeechnes_VALUE), universal_newlines=True)
                assert Host == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', Host
                assert (Verzeechnes_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            Editéieren_VALUE(Computer, 'FileDemo.java', Quell.replace('output.write(65);', 'output.close(); output.write(65);'))
            Computer.Befeel('javac FileDemo.java', ['Exit: 0'])
            Computer.Befeel('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Editéieren_VALUE(Computer, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            Computer.Befeel('javac FileDemo.java', ['Exit: 0'])
            Computer.Befeel('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            Computer.Befeel('run hello recovered', ['Exit: 0'])
            Mooss[종류] = Computer.LOG_Rei.decode('utf-8', 'replace')
        finally:
            Computer.Clôture()
        print('PASS:', 종류, '게스트 Java Fichier generéieren/이어쓰기/Byte_VALUE/EOF/닫힘/Feeler_VALUE/OpenJDK 교차 ausféieren_Befeel', flush=True)
    (positionéieren / 'build/자바파일시험.json').write_text(json.dumps(Mooss, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ausféieren_Befeel()
