#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import luy_feeñ_te_jëmmadi_masin, 위치
from 자바시험 import soppi_xëyma, gan_bara_denc

def def_ndigel():
    결과 = {}
    Cosaan = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        masin = luy_feeñ_te_jëmmadi_masin(위치 / ('build/kernel.' + 종류), 종류, mbaal_xëyma=False)
        try:
            soppi_xëyma(masin, 'FileDemo.java', Cosaan)
            masin.ndigel('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for baamtu_xëyma in range(2):
                출력 = masin.ndigel('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            dugal_xabaar_lim = masin.ndigel('ls', ['java.txt  3 bytes'])
            tolluwaay = int(re.search(r'FileDemo.class\s+(\d+) bytes', dugal_xabaar_lim)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                dàmb_xëyma = Path(임시)
                gan_bara_denc(masin, 2, tolluwaay, dàmb_xëyma / 'FileDemo.class')
                dalal = subprocess.check_output(['java', '-Xverify:all', '-cp', str(dàmb_xëyma), 'FileDemo'], cwd=str(dàmb_xëyma), universal_newlines=True)
                assert dalal == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', dalal
                assert (dàmb_xëyma / 'java.txt').read_bytes() == b'A\xffB'
            soppi_xëyma(masin, 'FileDemo.java', Cosaan.replace('output.write(65);', 'output.close(); output.write(65);'))
            masin.ndigel('javac FileDemo.java', ['Exit: 0'])
            masin.ndigel('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            soppi_xëyma(masin, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            masin.ndigel('javac FileDemo.java', ['Exit: 0'])
            masin.ndigel('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            masin.ndigel('run hello recovered', ['Exit: 0'])
            결과[종류] = masin.làq_Dënk.decode('utf-8', 'replace')
        finally:
            masin.Tej()
        print('PASS:', 종류, '게스트 Java bara_denc 생성/이어쓰기/okte_xëyma/EOF/닫힘/foo_xëyma/OpenJDK 교차 def_ndigel', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    def_ndigel()
