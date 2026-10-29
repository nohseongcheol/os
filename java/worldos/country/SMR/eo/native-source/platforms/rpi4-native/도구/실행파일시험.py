#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from 실행 import 기준


def 리눅스예제(결과자료):
    결과자료.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nomo in [('Ruli.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(기준/'예제/리눅스ABI'/원본자료), '-o', str(결과자료/Nomo)])
    실행가능파일 = 결과자료/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(결과자료/'start.o'), str(결과자료/'hello.o')])
    내용 = 실행가능파일.read_bytes()
    assert len(내용) <= 16384 and 내용[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', 내용, 16) == (2, 183) and b'JKOROS\0' not in 내용
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(결과자료)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (결과자료/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Ruli():
    결과자료 = 기준/'build/verification/elf'
    결과자료.mkdir(parents=True, exist_ok=True)
    (결과자료/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(결과자료)
    결과 = subprocess.check_output(['python3', str(기준/'도구/파일실행.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in 결과, 결과
    (결과자료/'serial.log').write_text(결과)
    원본=실행가능파일.read_bytes()
    프로그램머리변위=struct.unpack_from('<Q',원본,32)[0]
    for Nomo,변위,형식지정,값 in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',프로그램머리변위+4,'I',7),('kernel-address',프로그램머리변위+16,'Q',0x400000)]:
        잘못된자료=bytearray(원본);struct.pack_into('<'+형식지정,잘못된자료,변위,값)
        Vojo=결과자료/Nomo;Vojo.write_bytes(잘못된자료)
        거부결과=subprocess.run(['python3',str(기준/'도구/파일실행.py'),'--linux',str(Vojo)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nomo,거부결과.stdout)
    검증기록 = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (결과자료/'report.json').write_text(json.dumps(검증기록, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Ruli()
