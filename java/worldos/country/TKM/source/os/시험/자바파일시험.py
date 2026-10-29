#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import hyýaly_kompýuter, 위치
from 자바시험 import redaktirle_baha, 게스트파일

def ýerine_ýetir_buýruk():
    결과 = {}
    Çeşme = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        kompýuter = hyýaly_kompýuter(위치 / ('build/kernel.' + 종류), 종류, Tor_baha=False)
        try:
            redaktirle_baha(kompýuter, 'FileDemo.java', Çeşme)
            kompýuter.buýruk('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for iterasiýa_baha in range(2):
                출력 = kompýuter.buýruk('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            girizmeklik_Sanaw = kompýuter.buýruk('ls', ['java.txt  3 bytes'])
            Ululyk = int(re.search(r'FileDemo.class\s+(\d+) bytes', girizmeklik_Sanaw)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                katalog_baha = Path(임시)
                게스트파일(kompýuter, 2, Ululyk, katalog_baha / 'FileDemo.class')
                esasy = subprocess.check_output(['java', '-Xverify:all', '-cp', str(katalog_baha), 'FileDemo'], cwd=str(katalog_baha), universal_newlines=True)
                assert esasy == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', esasy
                assert (katalog_baha / 'java.txt').read_bytes() == b'A\xffB'
            redaktirle_baha(kompýuter, 'FileDemo.java', Çeşme.replace('output.write(65);', 'output.close(); output.write(65);'))
            kompýuter.buýruk('javac FileDemo.java', ['Exit: 0'])
            kompýuter.buýruk('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            redaktirle_baha(kompýuter, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            kompýuter.buýruk('javac FileDemo.java', ['Exit: 0'])
            kompýuter.buýruk('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            kompýuter.buýruk('run hello recovered', ['Exit: 0'])
            결과[종류] = kompýuter.hasaba_alyş_setir.decode('utf-8', 'replace')
        finally:
            kompýuter.Ýap()
        print('PASS:', 종류, '게스트 Java Faýl 생성/이어쓰기/baýt_baha/EOF/닫힘/näsazlyk_baha/OpenJDK 교차 ýerine_ýetir_buýruk', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ýerine_ýetir_buýruk()
