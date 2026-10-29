#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from ดําเนินการ_คําสั่ง import แสดง_ราก


def 리눅스예제(เมตริก_ข้อมูล):
    เมตริก_ข้อมูล.mkdir(parents=True, exist_ok=True)
    for 원본자료, ชื่อ in [('เรียกใช้งาน.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(แสดง_ราก/'예제/리눅스ABI'/원본자료), '-o', str(เมตริก_ข้อมูล/ชื่อ)])
    แฟ้มปฏิบัติการ_รูป = เมตริก_ข้อมูล/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(แฟ้มปฏิบัติการ_รูป), str(เมตริก_ข้อมูล/'start.o'), str(เมตริก_ข้อมูล/'hello.o')])
    เนื้อหา_ค่า = แฟ้มปฏิบัติการ_รูป.read_bytes()
    assert len(เนื้อหา_ค่า) <= 16384 and เนื้อหา_ค่า[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', เนื้อหา_ค่า, 16) == (2, 183) and b'JKOROS\0' not in เนื้อหา_ค่า
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    การเปรียบเทียบ_ขั้นต้น = subprocess.check_output(['qemu-aarch64', str(แฟ้มปฏิบัติการ_รูป), '한글인수'], cwd=str(เมตริก_ข้อมูล)).decode()
    assert การเปรียบเทียบ_ขั้นต้น == 예상결과, การเปรียบเทียบ_ขั้นต้น
    (เมตริก_ข้อมูล/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(แฟ้มปฏิบัติการ_รูป)]))
    return แฟ้มปฏิบัติการ_รูป, 예상결과


def เรียกใช้งาน():
    เมตริก_ข้อมูล = แสดง_ราก/'build/verification/elf'
    เมตริก_ข้อมูล.mkdir(parents=True, exist_ok=True)
    (เมตริก_ข้อมูล/'report.json').write_text('{"passed": false}\n')
    แฟ้มปฏิบัติการ_รูป, 예상결과 = 리눅스예제(เมตริก_ข้อมูล)
    ผลลัพธ์ = subprocess.check_output(['python3', str(แสดง_ราก/'เครื่องมือ/ดําเนินการ_แฟ้ม.py'), '--linux', str(แฟ้มปฏิบัติการ_รูป), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ผลลัพธ์, ผลลัพธ์
    (เมตริก_ข้อมูล/'serial.log').write_text(ผลลัพธ์)
    원본=แฟ้มปฏิบัติการ_รูป.read_bytes()
    แอป_ส่วนหัว_ออฟเซต=struct.unpack_from('<Q',원본,32)[0]
    for ชื่อ,ออฟเซต_ค่า,รูปแบบ_b87fd068,ค่า in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',แอป_ส่วนหัว_ออฟเซต+4,'I',7),('kernel-address',แอป_ส่วนหัว_ออฟเซต+16,'Q',0x400000)]:
        ไม่ถูกต้อง_ข้อมูล=bytearray(원본);struct.pack_into('<'+รูปแบบ_b87fd068,ไม่ถูกต้อง_ข้อมูล,ออฟเซต_ค่า,ค่า)
        เส้นทาง=เมตริก_ข้อมูล/ชื่อ;เส้นทาง.write_bytes(ไม่ถูกต้อง_ข้อมูล)
        거부결과=subprocess.run(['python3',str(แสดง_ราก/'เครื่องมือ/ดําเนินการ_แฟ้ม.py'),'--linux',str(เส้นทาง)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(ชื่อ,거부결과.stdout)
    การตรวจสอบความถูกต้อง_รายงาน = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(แฟ้มปฏิบัติการ_รูป.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (เมตริก_ข้อมูล/'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': เรียกใช้งาน()
