#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. แปล_แหล่ง 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from คอมไพเลอร์ import 컴파일오류

แสดง_ราก = Path(__file__).resolve().parent

class เครื่อง_รหัส_คอมไพเลอร์:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.พาธ_รายการ = [ข้อมูล.เส้นทาง for ข้อมูล in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def สร้าง_167eff27(자신, จุดเข้าใช้งาน, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            เมตริก_พาธ = Path(작업)/'generated.c'
            คําสั่ง = ['sh', str(แสดง_ราก/'미리번역.sh'), '--entry', จุดเข้าใช้งาน,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(เมตริก_พาธ)]
            if 범용문자표기: คําสั่ง.append('--ucn')
            for กําหนด_ค่า in 내보내기목록: คําสั่ง.extend(['--export', กําหนด_ค่า])
            คําสั่ง.extend(str(เส้นทาง) for เส้นทาง in 자신.พาธ_รายการ)
            ผลลัพธ์ = subprocess.run(คําสั่ง, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ผลลัพธ์.returncode: raise 컴파일오류(ผลลัพธ์.stderr.decode('utf-8', 'replace'))
            return เมตริก_พาธ.read_text()

def เรียกใช้งาน():
    raise SystemExit(subprocess.call(['sh', str(แสดง_ราก/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': เรียกใช้งาน()
