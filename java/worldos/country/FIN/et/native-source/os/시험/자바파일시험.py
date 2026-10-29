#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import VM, Asukoht
from 자바시험 import muudatus_VALUE, külaline_Fail

def Täida_käsk():
    TULEMUS = {}
    ALLIKAS = (Asukoht.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        arvuti = VM(Asukoht / ('build/kernel.' + 종류), 종류, võrk_VALUE=False)
        try:
            muudatus_VALUE(arvuti, 'FileDemo.java', ALLIKAS)
            arvuti.Käsk('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALUE in range(2):
                Väljund = arvuti.Käsk('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            kirje_Loend = arvuti.Käsk('ls', ['java.txt  3 bytes'])
            Suurus = int(re.search(r'FileDemo.class\s+(\d+) bytes', kirje_Loend)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                kaust_VALUE = Path(임시)
                külaline_Fail(arvuti, 2, Suurus, kaust_VALUE / 'FileDemo.class')
                host = subprocess.check_output(['java', '-Xverify:all', '-cp', str(kaust_VALUE), 'FileDemo'], cwd=str(kaust_VALUE), universal_newlines=True)
                assert host == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', host
                assert (kaust_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            muudatus_VALUE(arvuti, 'FileDemo.java', ALLIKAS.replace('output.write(65);', 'output.close(); output.write(65);'))
            arvuti.Käsk('javac FileDemo.java', ['Exit: 0'])
            arvuti.Käsk('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            muudatus_VALUE(arvuti, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            arvuti.Käsk('javac FileDemo.java', ['Exit: 0'])
            arvuti.Käsk('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            arvuti.Käsk('run hello recovered', ['Exit: 0'])
            TULEMUS[종류] = arvuti.LOG_kirje.decode('utf-8', 'replace')
        finally:
            arvuti.Suletud()
        print('PASS:', 종류, '게스트 Java Fail genereerima/이어쓰기/bait_VALUE/EOF/infotehnoloogia_suletud/tõrge_VALUE/OpenJDK 교차 Täida_käsk', flush=True)
    (Asukoht / 'build/자바파일시험.json').write_text(json.dumps(TULEMUS, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Täida_käsk()
