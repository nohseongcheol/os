#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from teszt_felhasználó_hálózat import VM, Pozíció
from 자바시험 import szerkeszt_ÉRTÉK, vendég_Fájl

def végrehajt_parancs():
    KR = {}
    FORRÁS = (Pozíció.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for Altípus_ÉRTÉK in ('elf', 'iso'):
        gép = VM(Pozíció / ('build/kernel.' + Altípus_ÉRTÉK), Altípus_ÉRTÉK, hálózat_ÉRTÉK=False)
        try:
            szerkeszt_ÉRTÉK(gép, 'FileDemo.java', FORRÁS)
            gép.Parancs('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for futam_ÉRTÉK in range(2):
                Kimenet = gép.Parancs('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            bejegyzés_Lista = gép.Parancs('ls', ['java.txt  3 bytes'])
            Méret = int(re.search(r'FileDemo.class\s+(\d+) bytes', bejegyzés_Lista)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                címtár_ÉRTÉK = Path(임시)
                vendég_Fájl(gép, 2, Méret, címtár_ÉRTÉK / 'FileDemo.class')
                gazda = subprocess.check_output(['java', '-Xverify:all', '-cp', str(címtár_ÉRTÉK), 'FileDemo'], cwd=str(címtár_ÉRTÉK), universal_newlines=True)
                assert gazda == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', gazda
                assert (címtár_ÉRTÉK / 'java.txt').read_bytes() == b'A\xffB'
            szerkeszt_ÉRTÉK(gép, 'FileDemo.java', FORRÁS.replace('output.write(65);', 'output.close(); output.write(65);'))
            gép.Parancs('javac FileDemo.java', ['Exit: 0'])
            gép.Parancs('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            szerkeszt_ÉRTÉK(gép, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            gép.Parancs('javac FileDemo.java', ['Exit: 0'])
            gép.Parancs('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            gép.Parancs('run hello recovered', ['Exit: 0'])
            KR[Altípus_ÉRTÉK] = gép.LOG_REKORD.decode('utf-8', 'replace')
        finally:
            gép.Bezárás()
        print('PASS:', Altípus_ÉRTÉK, '게스트 Java Fájl generálás/이어쓰기/bájt_ÉRTÉK/EOF/informatikai_részleg_lezárt/hiba_ÉRTÉK/OpenJDK 교차 végrehajt_parancs', flush=True)
    (Pozíció / 'build/자바파일시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    végrehajt_parancs()
