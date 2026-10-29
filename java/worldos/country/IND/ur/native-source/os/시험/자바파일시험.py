#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import مجازی_مشین, مقام
from 자바시험 import تدوین_قدر, مہمان_فائل

def نفاذ_کریں_حکم():
    پیمائش = {}
    ماخذ_فائل = (مقام.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        مشین = مجازی_مشین(مقام / ('build/kernel.' + 종류), 종류, نیٹ_ورک_قدر=False)
        try:
            تدوین_قدر(مشین, 'FileDemo.java', ماخذ_فائل)
            مشین.حکم('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for تکرار_قدر in range(2):
                اخراج_کا_مقام = مشین.حکم('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            اندراج_فہرست = مشین.حکم('ls', ['java.txt  3 bytes'])
            حجم = int(re.search(r'FileDemo.class\s+(\d+) bytes', اندراج_فہرست)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ڈائریکٹری_قدر = Path(임시)
                مہمان_فائل(مشین, 2, حجم, ڈائریکٹری_قدر / 'FileDemo.class')
                میزبان = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ڈائریکٹری_قدر), 'FileDemo'], cwd=str(ڈائریکٹری_قدر), universal_newlines=True)
                assert میزبان == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', میزبان
                assert (ڈائریکٹری_قدر / 'java.txt').read_bytes() == b'A\xffB'
            تدوین_قدر(مشین, 'FileDemo.java', ماخذ_فائل.replace('output.write(65);', 'output.close(); output.write(65);'))
            مشین.حکم('javac FileDemo.java', ['Exit: 0'])
            مشین.حکم('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            تدوین_قدر(مشین, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            مشین.حکم('javac FileDemo.java', ['Exit: 0'])
            مشین.حکم('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            مشین.حکم('run hello recovered', ['Exit: 0'])
            پیمائش[종류] = مشین.لاگ_صف.decode('utf-8', 'replace')
        finally:
            مشین.بند_کریں()
        print('PASS:', 종류, '게스트 Java فائل_کا_نام تخلیق_کرنا/이어쓰기/بائٹ_قدر/EOF/닫힘/ناکامی_قدر/OpenJDK 교차 نفاذ_کریں_حکم', flush=True)
    (مقام / 'build/자바파일시험.json').write_text(json.dumps(پیمائش, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    نفاذ_کریں_حکم()
