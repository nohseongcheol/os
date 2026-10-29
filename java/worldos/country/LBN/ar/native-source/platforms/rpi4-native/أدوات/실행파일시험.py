#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from ينفذ_أمر import يعرض_جذر


def 리눅스예제(مقياس_بيانات):
    مقياس_بيانات.mkdir(parents=True, exist_ok=True)
    for 원본자료, اسم in [('تشغيل.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(يعرض_جذر/'예제/리눅스ABI'/원본자료), '-o', str(مقياس_بيانات/اسم)])
    실행가능파일 = مقياس_بيانات/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(مقياس_بيانات/'start.o'), str(مقياس_بيانات/'hello.o')])
    محتوى_قيمة = 실행가능파일.read_bytes()
    assert len(محتوى_قيمة) <= 16384 and محتوى_قيمة[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', محتوى_قيمة, 16) == (2, 183) and b'JKOROS\0' not in محتوى_قيمة
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    مقارنة_الأساس = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(مقياس_بيانات)).decode()
    assert مقارنة_الأساس == 예상결과, مقارنة_الأساس
    (مقياس_بيانات/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def تشغيل():
    مقياس_بيانات = يعرض_جذر/'build/verification/elf'
    مقياس_بيانات.mkdir(parents=True, exist_ok=True)
    (مقياس_بيانات/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(مقياس_بيانات)
    نتيجة = subprocess.check_output(['python3', str(يعرض_جذر/'أدوات/ينفذ_ملف.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in نتيجة, نتيجة
    (مقياس_بيانات/'serial.log').write_text(نتيجة)
    원본=실행가능파일.read_bytes()
    تطبيق_عنوان_إزاحة=struct.unpack_from('<Q',원본,32)[0]
    for اسم,إزاحة_قيمة,ينسق_b87fd068,قيمة in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',تطبيق_عنوان_إزاحة+4,'I',7),('kernel-address',تطبيق_عنوان_إزاحة+16,'Q',0x400000)]:
        غير_صالح_بيانات=bytearray(원본);struct.pack_into('<'+ينسق_b87fd068,غير_صالح_بيانات,إزاحة_قيمة,قيمة)
        مسار=مقياس_بيانات/اسم;مسار.write_bytes(غير_صالح_بيانات)
        거부결과=subprocess.run(['python3',str(يعرض_جذر/'أدوات/ينفذ_ملف.py'),'--linux',str(مسار)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(اسم,거부결과.stdout)
    التحقق_من_صحة_إبلاغ = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (مقياس_بيانات/'report.json').write_text(json.dumps(التحقق_من_صحة_إبلاغ, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': تشغيل()
