#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from يختبر_مستخدم_شبكة import جهاز_ظاهري, موضع
from 자바시험 import يحرر_قيمة, ضيف_ملف

def ينفذ_أمر():
    نتيجة = {}
    مصدر = (موضع.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        جهاز = جهاز_ظاهري(موضع / ('build/kernel.' + 종류), 종류, شبكة_قيمة=False)
        try:
            يحرر_قيمة(جهاز, 'FileDemo.java', مصدر)
            جهاز.أمر('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for تكرار_قيمة in range(2):
                مخرجات = جهاز.أمر('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            إدخال_قائمة_f07b3200 = جهاز.أمر('ls', ['java.txt  3 bytes'])
            حجم = int(re.search(r'FileDemo.class\s+(\d+) bytes', إدخال_قائمة_f07b3200)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                دليل_قيمة = Path(임시)
                ضيف_ملف(جهاز, 2, حجم, دليل_قيمة / 'FileDemo.class')
                مضيف = subprocess.check_output(['java', '-Xverify:all', '-cp', str(دليل_قيمة), 'FileDemo'], cwd=str(دليل_قيمة), universal_newlines=True)
                assert مضيف == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', مضيف
                assert (دليل_قيمة / 'java.txt').read_bytes() == b'A\xffB'
            يحرر_قيمة(جهاز, 'FileDemo.java', مصدر.replace('output.write(65);', 'output.close(); output.write(65);'))
            جهاز.أمر('javac FileDemo.java', ['Exit: 0'])
            جهاز.أمر('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            يحرر_قيمة(جهاز, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            جهاز.أمر('javac FileDemo.java', ['Exit: 0'])
            جهاز.أمر('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            جهاز.أمر('run hello recovered', ['Exit: 0'])
            نتيجة[종류] = جهاز.سجل_سجل.decode('utf-8', 'replace')
        finally:
            جهاز.إغلاق()
        print('PASS:', 종류, '게스트 Java ملف إنشاء/이어쓰기/بايت_قيمة/EOF/أنظمة_المعلومات_مغلق/فشل_قيمة/OpenJDK 교차 ينفذ_أمر', flush=True)
    (موضع / 'build/자바파일시험.json').write_text(json.dumps(نتيجة, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ينفذ_أمر()
