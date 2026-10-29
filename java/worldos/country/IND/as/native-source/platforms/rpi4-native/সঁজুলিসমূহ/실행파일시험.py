#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from নিষ্পাদন_আদেশ import 기준


def 리눅스예제(পৰিমাপ_ডাটা):
    পৰিমাপ_ডাটা.mkdir(parents=True, exist_ok=True)
    for 원본자료, নাম in [('সঞ্চালন.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(기준/'예제/리눅스ABI'/원본자료), '-o', str(পৰিমাপ_ডাটা/নাম)])
    실행가능파일 = পৰিমাপ_ডাটা/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(পৰিমাপ_ডাটা/'start.o'), str(পৰিমাপ_ডাটা/'hello.o')])
    সামগ্ৰী_মান = 실행가능파일.read_bytes()
    assert len(সামগ্ৰী_মান) <= 16384 and সামগ্ৰী_মান[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', সামগ্ৰী_মান, 16) == (2, 183) and b'JKOROS\0' not in সামগ্ৰী_মান
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    তুলনা_আধাৰৰেখা = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(পৰিমাপ_ডাটা)).decode()
    assert তুলনা_আধাৰৰেখা == 예상결과, তুলনা_আধাৰৰেখা
    (পৰিমাপ_ডাটা/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def সঞ্চালন():
    পৰিমাপ_ডাটা = 기준/'build/verification/elf'
    পৰিমাপ_ডাটা.mkdir(parents=True, exist_ok=True)
    (পৰিমাপ_ডাটা/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(পৰিমাপ_ডাটা)
    পৰিমাপ = subprocess.check_output(['python3', str(기준/'সঁজুলিসমূহ/নিষ্পাদন_ফাইল.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in পৰিমাপ, পৰিমাপ
    (পৰিমাপ_ডাটা/'serial.log').write_text(পৰিমাপ)
    원본=실행가능파일.read_bytes()
    এপ্প্_শিৰো_অফছেট=struct.unpack_from('<Q',원본,32)[0]
    for নাম,অফছেট_মান,সজ্জা_b87fd068,মান in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',এপ্প্_শিৰো_অফছেট+4,'I',7),('kernel-address',এপ্প্_শিৰো_অফছেট+16,'Q',0x400000)]:
        অবৈধ_ডাটা=bytearray(원본);struct.pack_into('<'+সজ্জা_b87fd068,অবৈধ_ডাটা,অফছেট_মান,মান)
        পথ=পৰিমাপ_ডাটা/নাম;পথ.write_bytes(অবৈধ_ডাটা)
        거부결과=subprocess.run(['python3',str(기준/'সঁজুলিসমূহ/নিষ্পাদন_ফাইল.py'),'--linux',str(পথ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(নাম,거부결과.stdout)
    বৈধতা_ৰিপ_ৰ্ট = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (পৰিমাপ_ডাটা/'report.json').write_text(json.dumps(বৈধতা_ৰিপ_ৰ্ট, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': সঞ্চালন()
