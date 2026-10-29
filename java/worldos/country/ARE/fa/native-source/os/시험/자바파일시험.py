#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import مجازی_دستگاه, مرتب_کردن
from 자바시험 import ویرایش_مقدار, مهمان_فایل

def اجرا_فرمان():
    سنجش = {}
    مبداء = (مرتب_کردن.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        دستگاه = مجازی_دستگاه(مرتب_کردن / ('build/kernel.' + 종류), 종류, شبکه_مقدار=False)
        try:
            ویرایش_مقدار(دستگاه, 'FileDemo.java', مبداء)
            دستگاه.فرمان('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for تکرار_مقدار in range(2):
                خروجی = دستگاه.فرمان('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ورودی_لیست = دستگاه.فرمان('ls', ['java.txt  3 bytes'])
            اندازه = int(re.search(r'FileDemo.class\s+(\d+) bytes', ورودی_لیست)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                فهرست_مقدار_e5561a2b = Path(임시)
                مهمان_فایل(دستگاه, 2, اندازه, فهرست_مقدار_e5561a2b / 'FileDemo.class')
                میزبان = subprocess.check_output(['java', '-Xverify:all', '-cp', str(فهرست_مقدار_e5561a2b), 'FileDemo'], cwd=str(فهرست_مقدار_e5561a2b), universal_newlines=True)
                assert میزبان == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', میزبان
                assert (فهرست_مقدار_e5561a2b / 'java.txt').read_bytes() == b'A\xffB'
            ویرایش_مقدار(دستگاه, 'FileDemo.java', مبداء.replace('output.write(65);', 'output.close(); output.write(65);'))
            دستگاه.فرمان('javac FileDemo.java', ['Exit: 0'])
            دستگاه.فرمان('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            ویرایش_مقدار(دستگاه, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            دستگاه.فرمان('javac FileDemo.java', ['Exit: 0'])
            دستگاه.فرمان('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            دستگاه.فرمان('run hello recovered', ['Exit: 0'])
            سنجش[종류] = دستگاه.واقعه_نگار_ردیف.decode('utf-8', 'replace')
        finally:
            دستگاه.بستن()
        print('PASS:', 종류, '게스트 Java پرونده ایجاد/이어쓰기/بایت_مقدار/EOF/닫힘/عدم_موفقیت_مقدار/OpenJDK 교차 اجرا_فرمان', flush=True)
    (مرتب_کردن / 'build/자바파일시험.json').write_text(json.dumps(سنجش, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    اجرا_فرمان()
