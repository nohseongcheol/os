#!/usr/bin/env python3
"""โฮสต์ libc 없이 연결한 ไทย C 프로그램을 ค่าจริง_ข้อมูล ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from การทดสอบ_ผู้ใช้_เครือข่าย import เครื่องเสมือน

ตําแหน่ง = Path(__file__).resolve().parents[1]

def ดําเนินการ_คําสั่ง():
    ผลลัพธ์ = {}
    เซิร์ฟเวอร์_ค่า = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    เซิร์ฟเวอร์_ค่า.bind(('127.0.0.1', 0))
    เซิร์ฟเวอร์_ค่า.settimeout(0.1)
    หมายเลขพอร์ต = เซิร์ฟเวอร์_ค่า.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ข้อมูล, อีเมล = เซิร์ฟเวอร์_ค่า.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ข้อมูล)
            เซิร์ฟเวอร์_ค่า.sendto(ข้อมูล, อีเมล)
    ผู้ปฏิบัติงาน_ค่า = threading.Thread(target=되보내기, daemon=True)
    ผู้ปฏิบัติงาน_ค่า.start()
    try:
        for 종류 in ('elf', 'iso'):
            เครื่อง = เครื่องเสมือน(ตําแหน่ง / ('build/kernel.' + 종류), 종류)
            try:
                for สปรินต์_ค่า in range(2):
                    เครื่อง.คําสั่ง('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    เครื่อง.คําสั่ง('run posixudp ' + str(หมายเลขพอร์ต), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                เรียกใช้งาน = len(เครื่อง.บันทึก_สถิติ)
                เครื่อง.직렬.sendall(b'run posixinput\n')
                เครื่อง.ภาวะรอ('POSIX INPUT READY', เรียกใช้งาน)
                เครื่อง.직렬.sendall(b'abcdef')
                ข้อความออก = เครื่อง.ภาวะรอ('jkoros> ', เรียกใช้งาน)
                assert 'POSIX INPUT PASS' in ข้อความออก and 'Exit: 0' in ข้อความออก, ข้อความออก
                เครื่อง.คําสั่ง('javac Hello.java', ['Exit: 0'])
                เครื่อง.คําสั่ง('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                เครื่อง.คําสั่ง('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ผลลัพธ์[종류] = เครื่อง.บันทึก_สถิติ.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX แฟ้ม/공유 ตําแหน่ง/삭제 수명/อีเมล ป้องกัน_ค่า/UDP/표준 입력/기존 Java', flush=True)
            finally:
                เครื่อง.ปิด()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); ผู้ปฏิบัติงาน_ค่า.join(timeout=2); เซิร์ฟเวอร์_ค่า.close()
    ผลลัพธ์['host_datagrams'] = [ข้อมูล.decode() for ข้อมูล in 받은자료]
    (ตําแหน่ง / 'build/กรณี_การทดสอบ.json').write_text(json.dumps(ผลลัพธ์, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ดําเนินการ_คําสั่ง()
