#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import தோற்றநிலை_இயந்திரம், இடம்
from 자바시험 import திருத்து_மதிப்பு, விருந்தினர்_கோப்பு

def இயக்கு_கட்டளை():
    அளவிடக்கூடியது = {}
    மூலக்_கோப்பு = (இடம்.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        இயந்திரம் = தோற்றநிலை_இயந்திரம்(இடம் / ('build/kernel.' + 종류), 종류, பிணையம்_மதிப்பு=False)
        try:
            திருத்து_மதிப்பு(இயந்திரம், 'FileDemo.java', மூலக்_கோப்பு)
            இயந்திரம்.கட்டளை('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for மீள்செயல்_மதிப்பு in range(2):
                வெளியீட்டு_இடம் = இயந்திரம்.கட்டளை('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            உள்ளீடு_பட்டியல் = இயந்திரம்.கட்டளை('ls', ['java.txt  3 bytes'])
            அளவு = int(re.search(r'FileDemo.class\s+(\d+) bytes', உள்ளீடு_பட்டியல்)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                கோப்பகம்_மதிப்பு = Path(임시)
                விருந்தினர்_கோப்பு(இயந்திரம், 2, அளவு, கோப்பகம்_மதிப்பு / 'FileDemo.class')
                ஓம்பு = subprocess.check_output(['java', '-Xverify:all', '-cp', str(கோப்பகம்_மதிப்பு), 'FileDemo'], cwd=str(கோப்பகம்_மதிப்பு), universal_newlines=True)
                assert ஓம்பு == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', ஓம்பு
                assert (கோப்பகம்_மதிப்பு / 'java.txt').read_bytes() == b'A\xffB'
            திருத்து_மதிப்பு(இயந்திரம், 'FileDemo.java', மூலக்_கோப்பு.replace('output.write(65);', 'output.close(); output.write(65);'))
            இயந்திரம்.கட்டளை('javac FileDemo.java', ['Exit: 0'])
            இயந்திரம்.கட்டளை('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            திருத்து_மதிப்பு(இயந்திரம், 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            இயந்திரம்.கட்டளை('javac FileDemo.java', ['Exit: 0'])
            இயந்திரம்.கட்டளை('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            இயந்திரம்.கட்டளை('run hello recovered', ['Exit: 0'])
            அளவிடக்கூடியது[종류] = இயந்திரம்.பதிவு_பதிவு.decode('utf-8', 'replace')
        finally:
            இயந்திரம்.மூடு()
        print('PASS:', 종류, '게스트 Java கோப்பின்_பெயர் உருவாக்குக/이어쓰기/பைட்_மதிப்பு/EOF/닫힘/செயலிழப்பு_மதிப்பு/OpenJDK 교차 இயக்கு_கட்டளை', flush=True)
    (இடம் / 'build/자바파일시험.json').write_text(json.dumps(அளவிடக்கூடியது, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    இயக்கு_கட்டளை()
