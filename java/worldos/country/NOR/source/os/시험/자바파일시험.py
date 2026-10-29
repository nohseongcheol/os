#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from test_bruker_nettverk import VM, Posisjon
from 자바시험 import Rediger_VERDI, gjest_Fil

def Utfør_kommando():
    KR = {}
    KILDE = (Posisjon.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        maskin = VM(Posisjon / ('build/kernel.' + 종류), 종류, nettverk_VERDI=False)
        try:
            Rediger_VERDI(maskin, 'FileDemo.java', KILDE)
            maskin.Kommando('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VERDI in range(2):
                Utgang = maskin.Kommando('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            oppføring_Liste = maskin.Kommando('ls', ['java.txt  3 bytes'])
            Størrelse = int(re.search(r'FileDemo.class\s+(\d+) bytes', oppføring_Liste)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                katalog_VERDI = Path(임시)
                gjest_Fil(maskin, 2, Størrelse, katalog_VERDI / 'FileDemo.class')
                vert = subprocess.check_output(['java', '-Xverify:all', '-cp', str(katalog_VERDI), 'FileDemo'], cwd=str(katalog_VERDI), universal_newlines=True)
                assert vert == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', vert
                assert (katalog_VERDI / 'java.txt').read_bytes() == b'A\xffB'
            Rediger_VERDI(maskin, 'FileDemo.java', KILDE.replace('output.write(65);', 'output.close(); output.write(65);'))
            maskin.Kommando('javac FileDemo.java', ['Exit: 0'])
            maskin.Kommando('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Rediger_VERDI(maskin, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            maskin.Kommando('javac FileDemo.java', ['Exit: 0'])
            maskin.Kommando('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            maskin.Kommando('run hello recovered', ['Exit: 0'])
            KR[종류] = maskin.LOG_POST.decode('utf-8', 'replace')
        finally:
            maskin.Lukk()
        print('PASS:', 종류, '게스트 Java Fil generere/이어쓰기/byte_VERDI/EOF/informasjonssystemer_lukket/feil_VERDI/OpenJDK 교차 Utfør_kommando', flush=True)
    (Posisjon / 'build/자바파일시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Utfør_kommando()
