#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز


def 리눅스예제(ئۆلچەم_مەلۇمات):
    ئۆلچەم_مەلۇمات.mkdir(parents=True, exist_ok=True)
    for 원본자료, ئاتى in [('ئىجرا_قىل_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(كۆرسىتىش_يىلتىز/'예제/리눅스ABI'/원본자료), '-o', str(ئۆلچەم_مەلۇمات/ئاتى)])
    실행가능파일 = ئۆلچەم_مەلۇمات/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(ئۆلچەم_مەلۇمات/'start.o'), str(ئۆلچەم_مەلۇمات/'hello.o')])
    مەزمۇن_قىممىتى = 실행가능파일.read_bytes()
    assert len(مەزمۇن_قىممىتى) <= 16384 and مەزمۇن_قىممىتى[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', مەزمۇن_قىممىتى, 16) == (2, 183) and b'JKOROS\0' not in مەزمۇن_قىممىتى
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(ئۆلچەم_مەلۇمات)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (ئۆلچەم_مەلۇمات/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def ئىجرا_قىل_2():
    ئۆلچەم_مەلۇمات = كۆرسىتىش_يىلتىز/'build/verification/elf'
    ئۆلچەم_مەلۇمات.mkdir(parents=True, exist_ok=True)
    (ئۆلچەم_مەلۇمات/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(ئۆلچەم_مەلۇمات)
    ئۆلچەم = subprocess.check_output(['python3', str(كۆرسىتىش_يىلتىز/'قوراللار/ئىجرا_قىلىش_ھۆججەت.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ئۆلچەم, ئۆلچەم
    (ئۆلچەم_مەلۇمات/'serial.log').write_text(ئۆلچەم)
    원본=실행가능파일.read_bytes()
    ئەپ_بېشى_ئاغما=struct.unpack_from('<Q',원본,32)[0]
    for ئاتى,ئاغما_قىممىتى,فورمات_b87fd068,قىممىتى in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ئەپ_بېشى_ئاغما+4,'I',7),('kernel-address',ئەپ_بېشى_ئاغما+16,'Q',0x400000)]:
        ئۈنۈمسىز_مەلۇمات=bytearray(원본);struct.pack_into('<'+فورمات_b87fd068,ئۈنۈمسىز_مەلۇمات,ئاغما_قىممىتى,قىممىتى)
        يول=ئۆلچەم_مەلۇمات/ئاتى;يول.write_bytes(ئۈنۈمسىز_مەلۇمات)
        거부결과=subprocess.run(['python3',str(كۆرسىتىش_يىلتىز/'قوراللار/ئىجرا_قىلىش_ھۆججەت.py'),'--linux',str(يول)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(ئاتى,거부결과.stdout)
    دەلىللەش_خەۋەر = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((كۆرسىتىش_يىلتىز/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ئۆلچەم_مەلۇمات/'report.json').write_text(json.dumps(دەلىللەش_خەۋەر, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': ئىجرا_قىل_2()
