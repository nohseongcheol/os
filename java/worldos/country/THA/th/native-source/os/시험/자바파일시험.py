#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from การทดสอบ_ผู้ใช้_เครือข่าย import เครื่องเสมือน, ตําแหน่ง
from 자바시험 import แก้ไข_ค่า, ผู้เยี่ยมชม_แฟ้ม

def ดําเนินการ_คําสั่ง():
    ผลลัพธ์ = {}
    รหัสต้นฉบับ = (ตําแหน่ง.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        เครื่อง = เครื่องเสมือน(ตําแหน่ง / ('build/kernel.' + 종류), 종류, เครือข่าย_ค่า=False)
        try:
            แก้ไข_ค่า(เครื่อง, 'FileDemo.java', รหัสต้นฉบับ)
            เครื่อง.คําสั่ง('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for สปรินต์_ค่า in range(2):
                ข้อความออก = เครื่อง.คําสั่ง('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            รายการ_รายการ = เครื่อง.คําสั่ง('ls', ['java.txt  3 bytes'])
            ขนาด = int(re.search(r'FileDemo.class\s+(\d+) bytes', รายการ_รายการ)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ไดเรกทอรี_ค่า = Path(임시)
                ผู้เยี่ยมชม_แฟ้ม(เครื่อง, 2, ขนาด, ไดเรกทอรี_ค่า / 'FileDemo.class')
                โฮสต์ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ไดเรกทอรี_ค่า), 'FileDemo'], cwd=str(ไดเรกทอรี_ค่า), universal_newlines=True)
                assert โฮสต์ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', โฮสต์
                assert (ไดเรกทอรี_ค่า / 'java.txt').read_bytes() == b'A\xffB'
            แก้ไข_ค่า(เครื่อง, 'FileDemo.java', รหัสต้นฉบับ.replace('output.write(65);', 'output.close(); output.write(65);'))
            เครื่อง.คําสั่ง('javac FileDemo.java', ['Exit: 0'])
            เครื่อง.คําสั่ง('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            แก้ไข_ค่า(เครื่อง, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            เครื่อง.คําสั่ง('javac FileDemo.java', ['Exit: 0'])
            เครื่อง.คําสั่ง('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            เครื่อง.คําสั่ง('run hello recovered', ['Exit: 0'])
            ผลลัพธ์[종류] = เครื่อง.บันทึก_สถิติ.decode('utf-8', 'replace')
        finally:
            เครื่อง.ปิด()
        print('PASS:', 종류, '게스트 Java แฟ้ม สร้าง_167eff27/이어쓰기/ไบต์_ค่า/EOF/เทคโนโลยีสารสนเทศ_ปิด/ความล้มเหลว_ค่า/OpenJDK 교차 ดําเนินการ_คําสั่ง', flush=True)
    (ตําแหน่ง / 'build/자바파일시험.json').write_text(json.dumps(ผลลัพธ์, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ดําเนินการ_คําสั่ง()
