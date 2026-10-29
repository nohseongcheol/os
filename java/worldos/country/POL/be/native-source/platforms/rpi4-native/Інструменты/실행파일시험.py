#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from выканаць_каманда import 기준


def 리눅스예제(결과자료):
    결과자료.mkdir(parents=True, exist_ok=True)
    for 원본자료, Назва in [('Выканаць.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(기준/'예제/리눅스ABI'/원본자료), '-o', str(결과자료/Назва)])
    실행가능파일 = 결과자료/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(결과자료/'start.o'), str(결과자료/'hello.o')])
    кантэнт_значэнне = 실행가능파일.read_bytes()
    assert len(кантэнт_значэнне) <= 16384 and кантэнт_значэнне[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', кантэнт_значэнне, 16) == (2, 183) and b'JKOROS\0' not in кантэнт_значэнне
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Параўнанне_базавы_план = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(결과자료)).decode()
    assert Параўнанне_базавы_план == 예상결과, Параўнанне_базавы_план
    (결과자료/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Выканаць():
    결과자료 = 기준/'build/verification/elf'
    결과자료.mkdir(parents=True, exist_ok=True)
    (결과자료/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(결과자료)
    결과 = subprocess.check_output(['python3', str(기준/'Інструменты/выканаць_файл.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in 결과, 결과
    (결과자료/'serial.log').write_text(결과)
    원본=실행가능파일.read_bytes()
    праграма_Загаловак_Зрух=struct.unpack_from('<Q',원본,32)[0]
    for Назва,Зрух_значэнне,фармат_b87fd068,значэнне in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',праграма_Загаловак_Зрух+4,'I',7),('kernel-address',праграма_Загаловак_Зрух+16,'Q',0x400000)]:
        памылковы_дадзеныя=bytearray(원본);struct.pack_into('<'+фармат_b87fd068,памылковы_дадзеныя,Зрух_значэнне,значэнне)
        ШЛЯХ=결과자료/Назва;ШЛЯХ.write_bytes(памылковы_дадзеныя)
        거부결과=subprocess.run(['python3',str(기준/'Інструменты/выканаць_файл.py'),'--linux',str(ШЛЯХ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Назва,거부결과.stdout)
    праверка_справаздача = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (결과자료/'report.json').write_text(json.dumps(праверка_справаздача, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Выканаць()
