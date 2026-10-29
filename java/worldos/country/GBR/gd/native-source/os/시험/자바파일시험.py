#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import mas_fhìor_inneal, suidhich
from 자바시험 import deasaich_VALUE, aoigh_faidhle

def gnìomhaich_àithne():
    tomhas = {}
    tùs = (suidhich.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        inneal = mas_fhìor_inneal(suidhich / ('build/kernel.' + 종류), 종류, lìonra_VALUE=False)
        try:
            deasaich_VALUE(inneal, 'FileDemo.java', tùs)
            inneal.àithne('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ath_thriall_VALUE in range(2):
                출력 = inneal.àithne('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            cur_a_steach_Liosta = inneal.àithne('ls', ['java.txt  3 bytes'])
            atharraich_am_meud = int(re.search(r'FileDemo.class\s+(\d+) bytes', cur_a_steach_Liosta)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                eòlaire_VALUE = Path(임시)
                aoigh_faidhle(inneal, 2, atharraich_am_meud, eòlaire_VALUE / 'FileDemo.class')
                òstair = subprocess.check_output(['java', '-Xverify:all', '-cp', str(eòlaire_VALUE), 'FileDemo'], cwd=str(eòlaire_VALUE), universal_newlines=True)
                assert òstair == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', òstair
                assert (eòlaire_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            deasaich_VALUE(inneal, 'FileDemo.java', tùs.replace('output.write(65);', 'output.close(); output.write(65);'))
            inneal.àithne('javac FileDemo.java', ['Exit: 0'])
            inneal.àithne('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            deasaich_VALUE(inneal, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            inneal.àithne('javac FileDemo.java', ['Exit: 0'])
            inneal.àithne('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            inneal.àithne('run hello recovered', ['Exit: 0'])
            tomhas[종류] = inneal.LOG_ràgh.decode('utf-8', 'replace')
        finally:
            inneal.dùin()
        print('PASS:', 종류, '게스트 Java faidhle gin/이어쓰기/baidht_VALUE/EOF/닫힘/fàilligeadh_VALUE/OpenJDK 교차 gnìomhaich_àithne', flush=True)
    (suidhich / 'build/자바파일시험.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    gnìomhaich_àithne()
