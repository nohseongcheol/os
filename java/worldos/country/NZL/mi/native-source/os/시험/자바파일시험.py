#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import mariko_mīhini, tūranga
from 자바시험 import whakatika_uara, manuhiri_kōnae

def kawe_tono():
    mēhua = {}
    pūtake = (tūranga.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        mīhini = mariko_mīhini(tūranga / ('build/kernel.' + 종류), 종류, whatunga_uara=False)
        try:
            whakatika_uara(mīhini, 'FileDemo.java', pūtake)
            mīhini.tono('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for whitiauau_uara in range(2):
                출력 = mīhini.tono('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            tāurunga_Rārangi = mīhini.tono('ls', ['java.txt  3 bytes'])
            rahi = int(re.search(r'FileDemo.class\s+(\d+) bytes', tāurunga_Rārangi)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                whaiaronga_uara = Path(임시)
                manuhiri_kōnae(mīhini, 2, rahi, whaiaronga_uara / 'FileDemo.class')
                taurima = subprocess.check_output(['java', '-Xverify:all', '-cp', str(whaiaronga_uara), 'FileDemo'], cwd=str(whaiaronga_uara), universal_newlines=True)
                assert taurima == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', taurima
                assert (whaiaronga_uara / 'java.txt').read_bytes() == b'A\xffB'
            whakatika_uara(mīhini, 'FileDemo.java', pūtake.replace('output.write(65);', 'output.close(); output.write(65);'))
            mīhini.tono('javac FileDemo.java', ['Exit: 0'])
            mīhini.tono('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            whakatika_uara(mīhini, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            mīhini.tono('javac FileDemo.java', ['Exit: 0'])
            mīhini.tono('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            mīhini.tono('run hello recovered', ['Exit: 0'])
            mēhua[종류] = mīhini.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mīhini.Kati()
        print('PASS:', 종류, '게스트 Java Kōnae waihanga/이어쓰기/paita_uara/EOF/닫힘/rahunga_uara/OpenJDK 교차 kawe_tono', flush=True)
    (tūranga / 'build/자바파일시험.json').write_text(json.dumps(mēhua, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    kawe_tono()
