#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ


def 리눅스예제(پیمائش_کوائف):
    پیمائش_کوائف.mkdir(parents=True, exist_ok=True)
    for 원본자료, نام in [('چلائیں.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(عکس_ڈالنا_روٹ/'예제/리눅스ABI'/원본자료), '-o', str(پیمائش_کوائف/نام)])
    실행가능파일 = پیمائش_کوائف/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(پیمائش_کوائف/'start.o'), str(پیمائش_کوائف/'hello.o')])
    مشمول_قدر = 실행가능파일.read_bytes()
    assert len(مشمول_قدر) <= 16384 and مشمول_قدر[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', مشمول_قدر, 16) == (2, 183) and b'JKOROS\0' not in مشمول_قدر
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(پیمائش_کوائف)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (پیمائش_کوائف/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def چلائیں():
    پیمائش_کوائف = عکس_ڈالنا_روٹ/'build/verification/elf'
    پیمائش_کوائف.mkdir(parents=True, exist_ok=True)
    (پیمائش_کوائف/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(پیمائش_کوائف)
    پیمائش = subprocess.check_output(['python3', str(عکس_ڈالنا_روٹ/'ٹولز/نفاذ_کریں_فائل.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in پیمائش, پیمائش
    (پیمائش_کوائف/'serial.log').write_text(پیمائش)
    원본=실행가능파일.read_bytes()
    ایپ_سرصفحہ_آفسٹ=struct.unpack_from('<Q',원본,32)[0]
    for نام,آفسٹ_قدر,وضع_b87fd068,قدر in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ایپ_سرصفحہ_آفسٹ+4,'I',7),('kernel-address',ایپ_سرصفحہ_آفسٹ+16,'Q',0x400000)]:
        بے_جواز_کوائف=bytearray(원본);struct.pack_into('<'+وضع_b87fd068,بے_جواز_کوائف,آفسٹ_قدر,قدر)
        راستہ_2=پیمائش_کوائف/نام;راستہ_2.write_bytes(بے_جواز_کوائف)
        거부결과=subprocess.run(['python3',str(عکس_ڈالنا_روٹ/'ٹولز/نفاذ_کریں_فائل.py'),'--linux',str(راستہ_2)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(نام,거부결과.stdout)
    توثیق_رپورٹ = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (پیمائش_کوائف/'report.json').write_text(json.dumps(توثیق_رپورٹ, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': چلائیں()
