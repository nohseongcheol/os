#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ujian_pengguna_rangkaian import mesin_maya, Kedudukan
from 자바시험 import edit_VALUE, tetamu_fail

def laksanakan_perintah():
    ukuran = {}
    SUMBER = (Kedudukan.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        mesin = mesin_maya(Kedudukan / ('build/kernel.' + 종류), 종류, rangkaian_VALUE=False)
        try:
            edit_VALUE(mesin, 'FileDemo.java', SUMBER)
            mesin.Perintah('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for lelaran_VALUE in range(2):
                출력 = mesin.Perintah('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            pemasukan_Senarai = mesin.Perintah('ls', ['java.txt  3 bytes'])
            Saiz = int(re.search(r'FileDemo.class\s+(\d+) bytes', pemasukan_Senarai)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                direktori_VALUE = Path(임시)
                tetamu_fail(mesin, 2, Saiz, direktori_VALUE / 'FileDemo.class')
                hos = subprocess.check_output(['java', '-Xverify:all', '-cp', str(direktori_VALUE), 'FileDemo'], cwd=str(direktori_VALUE), universal_newlines=True)
                assert hos == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', hos
                assert (direktori_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            edit_VALUE(mesin, 'FileDemo.java', SUMBER.replace('output.write(65);', 'output.close(); output.write(65);'))
            mesin.Perintah('javac FileDemo.java', ['Exit: 0'])
            mesin.Perintah('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            edit_VALUE(mesin, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            mesin.Perintah('javac FileDemo.java', ['Exit: 0'])
            mesin.Perintah('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            mesin.Perintah('run hello recovered', ['Exit: 0'])
            ukuran[종류] = mesin.LOG_baris.decode('utf-8', 'replace')
        finally:
            mesin.Tutup()
        print('PASS:', 종류, '게스트 Java Fail jana/이어쓰기/bait_VALUE/EOF/닫힘/kegagalan_VALUE/OpenJDK 교차 laksanakan_perintah', flush=True)
    (Kedudukan / 'build/자바파일시험.json').write_text(json.dumps(ukuran, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    laksanakan_perintah()
