#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import fíorúil_meaisín, suíomh
from 자바시험 import cuir_in_eagar_VALUE, aoi_comhad

def Rith_ordú():
    tomhas = {}
    FOINSE = (suíomh.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        meaisín = fíorúil_meaisín(suíomh / ('build/kernel.' + 종류), 종류, Líonra_VALUE=False)
        try:
            cuir_in_eagar_VALUE(meaisín, 'FileDemo.java', FOINSE)
            meaisín.Ordú('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for atriall_VALUE in range(2):
                Aschur = meaisín.Ordú('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            iontráil_Liosta = meaisín.Ordú('ls', ['java.txt  3 bytes'])
            Méid = int(re.search(r'FileDemo.class\s+(\d+) bytes', iontráil_Liosta)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                eolaire_VALUE = Path(임시)
                aoi_comhad(meaisín, 2, Méid, eolaire_VALUE / 'FileDemo.class')
                óstach = subprocess.check_output(['java', '-Xverify:all', '-cp', str(eolaire_VALUE), 'FileDemo'], cwd=str(eolaire_VALUE), universal_newlines=True)
                assert óstach == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', óstach
                assert (eolaire_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            cuir_in_eagar_VALUE(meaisín, 'FileDemo.java', FOINSE.replace('output.write(65);', 'output.close(); output.write(65);'))
            meaisín.Ordú('javac FileDemo.java', ['Exit: 0'])
            meaisín.Ordú('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            cuir_in_eagar_VALUE(meaisín, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            meaisín.Ordú('javac FileDemo.java', ['Exit: 0'])
            meaisín.Ordú('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            meaisín.Ordú('run hello recovered', ['Exit: 0'])
            tomhas[종류] = meaisín.LOG_ró.decode('utf-8', 'replace')
        finally:
            meaisín.Dún()
        print('PASS:', 종류, '게스트 Java Comhad giniúint/이어쓰기/beart_VALUE/EOF/닫힘/teip_VALUE/OpenJDK 교차 Rith_ordú', flush=True)
    (suíomh / 'build/자바파일시험.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Rith_ordú()
