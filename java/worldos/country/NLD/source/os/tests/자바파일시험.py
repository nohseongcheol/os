#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from test_gebruiker_net import VM, positie
from 자바시험 import Bewerk_WAARDE, gast_Bestand

def Uitvoeren_opdracht():
    resultaat = {}
    broncode = (positie.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for soort_WAARDE in ('elf', 'iso'):
        machine = VM(positie / ('build/kernel.' + soort_WAARDE), soort_WAARDE, net_WAARDE=False)
        try:
            Bewerk_WAARDE(machine, 'FileDemo.java', broncode)
            machine.opdracht('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_WAARDE in range(2):
                tekstuitvoer = machine.opdracht('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            invoer_Lijst_f07b3200 = machine.opdracht('ls', ['java.txt  3 bytes'])
            Grootte = int(re.search(r'FileDemo.class\s+(\d+) bytes', invoer_Lijst_f07b3200)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                map_WAARDE = Path(임시)
                gast_Bestand(machine, 2, Grootte, map_WAARDE / 'FileDemo.class')
                host = subprocess.check_output(['java', '-Xverify:all', '-cp', str(map_WAARDE), 'FileDemo'], cwd=str(map_WAARDE), universal_newlines=True)
                assert host == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', host
                assert (map_WAARDE / 'java.txt').read_bytes() == b'A\xffB'
            Bewerk_WAARDE(machine, 'FileDemo.java', broncode.replace('output.write(65);', 'output.close(); output.write(65);'))
            machine.opdracht('javac FileDemo.java', ['Exit: 0'])
            machine.opdracht('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Bewerk_WAARDE(machine, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            machine.opdracht('javac FileDemo.java', ['Exit: 0'])
            machine.opdracht('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            machine.opdracht('run hello recovered', ['Exit: 0'])
            resultaat[soort_WAARDE] = machine.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            machine.Sluiten()
        print('PASS:', soort_WAARDE, '게스트 Java bestand genereren/이어쓰기/byte_WAARDE/EOF/informatie_afgesloten/fout_WAARDE/OpenJDK 교차 Uitvoeren_opdracht', flush=True)
    (positie / 'build/자바파일시험.json').write_text(json.dumps(resultaat, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Uitvoeren_opdracht()
