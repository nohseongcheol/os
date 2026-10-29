#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from اجرا_فرمان import نمایش_دادن_جذر


def 리눅스예제(سنجش_داده_ها):
    سنجش_داده_ها.mkdir(parents=True, exist_ok=True)
    for 원본자료, نام in [('اجرا_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(نمایش_دادن_جذر/'예제/리눅스ABI'/원본자료), '-o', str(سنجش_داده_ها/نام)])
    실행가능파일 = سنجش_داده_ها/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(سنجش_داده_ها/'start.o'), str(سنجش_داده_ها/'hello.o')])
    محتوا_مقدار = 실행가능파일.read_bytes()
    assert len(محتوا_مقدار) <= 16384 and محتوا_مقدار[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', محتوا_مقدار, 16) == (2, 183) and b'JKOROS\0' not in محتوا_مقدار
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    مقایسه_پایه = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(سنجش_داده_ها)).decode()
    assert مقایسه_پایه == 예상결과, مقایسه_پایه
    (سنجش_داده_ها/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def اجرا_2():
    سنجش_داده_ها = نمایش_دادن_جذر/'build/verification/elf'
    سنجش_داده_ها.mkdir(parents=True, exist_ok=True)
    (سنجش_داده_ها/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(سنجش_داده_ها)
    سنجش = subprocess.check_output(['python3', str(نمایش_دادن_جذر/'ابزارها/اجرا_فایل.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in سنجش, سنجش
    (سنجش_داده_ها/'serial.log').write_text(سنجش)
    원본=실행가능파일.read_bytes()
    برنامه_سرصفحه_جابجایی_لایه_ای=struct.unpack_from('<Q',원본,32)[0]
    for نام,جابجایی_لایه_ای_مقدار,قالب_b87fd068,مقدار in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',برنامه_سرصفحه_جابجایی_لایه_ای+4,'I',7),('kernel-address',برنامه_سرصفحه_جابجایی_لایه_ای+16,'Q',0x400000)]:
        بی_اعتبار_داده_ها=bytearray(원본);struct.pack_into('<'+قالب_b87fd068,بی_اعتبار_داده_ها,جابجایی_لایه_ای_مقدار,مقدار)
        مسیر=سنجش_داده_ها/نام;مسیر.write_bytes(بی_اعتبار_داده_ها)
        거부결과=subprocess.run(['python3',str(نمایش_دادن_جذر/'ابزارها/اجرا_فایل.py'),'--linux',str(مسیر)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(نام,거부결과.stdout)
    اعتبارسنجی_گزارش = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (سنجش_داده_ها/'report.json').write_text(json.dumps(اعتبارسنجی_گزارش, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': اجرا_2()
