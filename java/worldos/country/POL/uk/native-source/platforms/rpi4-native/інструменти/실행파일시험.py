#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Виконати_команда import Дії_корінь


def 리눅스예제(КР_дані):
    КР_дані.mkdir(parents=True, exist_ok=True)
    for 원본자료, Назва in [('запустити.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Дії_корінь/'예제/리눅스ABI'/원본자료), '-o', str(КР_дані/Назва)])
    실행가능파일 = КР_дані/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(КР_дані/'start.o'), str(КР_дані/'hello.o')])
    Вміст_значення = 실행가능파일.read_bytes()
    assert len(Вміст_значення) <= 16384 and Вміст_значення[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Вміст_значення, 16) == (2, 183) and b'JKOROS\0' not in Вміст_значення
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Порівняння_напрямна = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(КР_дані)).decode()
    assert Порівняння_напрямна == 예상결과, Порівняння_напрямна
    (КР_дані/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def запустити():
    КР_дані = Дії_корінь/'build/verification/elf'
    КР_дані.mkdir(parents=True, exist_ok=True)
    (КР_дані/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(КР_дані)
    результат = subprocess.check_output(['python3', str(Дії_корінь/'інструменти/Виконати_Файл.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in результат, результат
    (КР_дані/'serial.log').write_text(результат)
    원본=실행가능파일.read_bytes()
    програма_Заголовок_Зміщена_копія=struct.unpack_from('<Q',원본,32)[0]
    for Назва,Зміщена_копія_значення,формат_b87fd068,значення in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',програма_Заголовок_Зміщена_копія+4,'I',7),('kernel-address',програма_Заголовок_Зміщена_копія+16,'Q',0x400000)]:
        недійсний_дані=bytearray(원본);struct.pack_into('<'+формат_b87fd068,недійсний_дані,Зміщена_копія_значення,значення)
        шлях=КР_дані/Назва;шлях.write_bytes(недійсний_дані)
        거부결과=subprocess.run(['python3',str(Дії_корінь/'інструменти/Виконати_Файл.py'),'--linux',str(шлях)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Назва,거부결과.stdout)
    перевірка_звіт = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (КР_дані/'report.json').write_text(json.dumps(перевірка_звіт, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': запустити()
