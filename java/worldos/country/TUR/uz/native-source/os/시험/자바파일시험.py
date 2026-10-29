#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import 가상기계, Holati
from 자바시험 import tahrirlamoq_VALUE, mehmon_fayl

def bajarmoq_buyruq():
    o_lchov = {}
    manba = (Holati.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        기계 = 가상기계(Holati / ('build/kernel.' + 종류), 종류, Tarmoq_VALUE=False)
        try:
            tahrirlamoq_VALUE(기계, 'FileDemo.java', manba)
            기계.Buyruq('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALUE in range(2):
                출력 = 기계.Buyruq('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            kiritish_Ro_yxat = 기계.Buyruq('ls', ['java.txt  3 bytes'])
            Hajmi = int(re.search(r'FileDemo.class\s+(\d+) bytes', kiritish_Ro_yxat)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                katalog_VALUE = Path(임시)
                mehmon_fayl(기계, 2, Hajmi, katalog_VALUE / 'FileDemo.class')
                tashkilotchi = subprocess.check_output(['java', '-Xverify:all', '-cp', str(katalog_VALUE), 'FileDemo'], cwd=str(katalog_VALUE), universal_newlines=True)
                assert tashkilotchi == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', tashkilotchi
                assert (katalog_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            tahrirlamoq_VALUE(기계, 'FileDemo.java', manba.replace('output.write(65);', 'output.close(); output.write(65);'))
            기계.Buyruq('javac FileDemo.java', ['Exit: 0'])
            기계.Buyruq('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            tahrirlamoq_VALUE(기계, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            기계.Buyruq('javac FileDemo.java', ['Exit: 0'])
            기계.Buyruq('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            기계.Buyruq('run hello recovered', ['Exit: 0'])
            o_lchov[종류] = 기계.LOG_satr.decode('utf-8', 'replace')
        finally:
            기계.Yopish()
        print('PASS:', 종류, '게스트 Java Fayl generatsiiyalash/이어쓰기/bayt_VALUE/EOF/닫힘/to_xtab_qolish_VALUE/OpenJDK 교차 bajarmoq_buyruq', flush=True)
    (Holati / 'build/자바파일시험.json').write_text(json.dumps(o_lchov, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    bajarmoq_buyruq()
