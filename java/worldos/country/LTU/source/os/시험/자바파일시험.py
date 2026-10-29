#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import VM, Pozicija
from 자바시험 import redaguoti_VALUE, svečias_Failas

def Vykdyti_komanda():
    REZULTATAS = {}
    ŠALTINIS = (Pozicija.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        mašina = VM(Pozicija / ('build/kernel.' + 종류), 종류, tinklas_VALUE=False)
        try:
            redaguoti_VALUE(mašina, 'FileDemo.java', ŠALTINIS)
            mašina.Komanda('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprintas_VALUE in range(2):
                Išvestis = mašina.Komanda('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            įrašas_Sąrašas = mašina.Komanda('ls', ['java.txt  3 bytes'])
            Dydis = int(re.search(r'FileDemo.class\s+(\d+) bytes', įrašas_Sąrašas)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Katalogas_VALUE = Path(임시)
                svečias_Failas(mašina, 2, Dydis, Katalogas_VALUE / 'FileDemo.class')
                organizuoti = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Katalogas_VALUE), 'FileDemo'], cwd=str(Katalogas_VALUE), universal_newlines=True)
                assert organizuoti == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', organizuoti
                assert (Katalogas_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            redaguoti_VALUE(mašina, 'FileDemo.java', ŠALTINIS.replace('output.write(65);', 'output.close(); output.write(65);'))
            mašina.Komanda('javac FileDemo.java', ['Exit: 0'])
            mašina.Komanda('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            redaguoti_VALUE(mašina, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            mašina.Komanda('javac FileDemo.java', ['Exit: 0'])
            mašina.Komanda('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            mašina.Komanda('run hello recovered', ['Exit: 0'])
            REZULTATAS[종류] = mašina.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mašina.Užverti()
        print('PASS:', 종류, '게스트 Java Failas generuoti/이어쓰기/baitas_VALUE/EOF/informacinės_technologijos_uždaryta/triktis_VALUE/OpenJDK 교차 Vykdyti_komanda', flush=True)
    (Pozicija / 'build/자바파일시험.json').write_text(json.dumps(REZULTATAS, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Vykdyti_komanda()
