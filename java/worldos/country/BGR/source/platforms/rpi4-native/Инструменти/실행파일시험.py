#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from изпълнявам_команда import проект_корен


def 리눅스예제(мярка_данни):
    мярка_данни.mkdir(parents=True, exist_ok=True)
    for 원본자료, Име in [('Стартиране.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(проект_корен/'예제/리눅스ABI'/원본자료), '-o', str(мярка_данни/Име)])
    실행가능파일 = мярка_данни/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(мярка_данни/'start.o'), str(мярка_данни/'hello.o')])
    Съдържание_стойност = 실행가능파일.read_bytes()
    assert len(Съдържание_стойност) <= 16384 and Съдържание_стойност[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Съдържание_стойност, 16) == (2, 183) and b'JKOROS\0' not in Съдържание_стойност
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Сравнение_Базова_линия = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(мярка_данни)).decode()
    assert Сравнение_Базова_линия == 예상결과, Сравнение_Базова_линия
    (мярка_данни/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Стартиране():
    мярка_данни = проект_корен/'build/verification/elf'
    мярка_данни.mkdir(parents=True, exist_ok=True)
    (мярка_данни/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(мярка_данни)
    РЕЗУЛТАТ = subprocess.check_output(['python3', str(проект_корен/'Инструменти/изпълнявам_Файл.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in РЕЗУЛТАТ, РЕЗУЛТАТ
    (мярка_данни/'serial.log').write_text(РЕЗУЛТАТ)
    원본=실행가능파일.read_bytes()
    програма_Заглавка_Изместване=struct.unpack_from('<Q',원본,32)[0]
    for Име,Изместване_стойност,формат_b87fd068,стойност in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',програма_Заглавка_Изместване+4,'I',7),('kernel-address',програма_Заглавка_Изместване+16,'Q',0x400000)]:
        невалиден_данни=bytearray(원본);struct.pack_into('<'+формат_b87fd068,невалиден_данни,Изместване_стойност,стойност)
        ПЪТ=мярка_данни/Име;ПЪТ.write_bytes(невалиден_данни)
        거부결과=subprocess.run(['python3',str(проект_корен/'Инструменти/изпълнявам_Файл.py'),'--linux',str(ПЪТ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Име,거부결과.stdout)
    проверка_отчет = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (мярка_данни/'report.json').write_text(json.dumps(проверка_отчет, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Стартиране()
