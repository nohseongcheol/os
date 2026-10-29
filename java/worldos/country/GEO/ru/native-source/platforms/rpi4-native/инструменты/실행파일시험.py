#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from 실행 import задача_корень


def 리눅스예제(KR_данные):
    KR_данные.mkdir(parents=True, exist_ok=True)
    for 원본자료, Название in [('запустить.S', 'start.o'), ('приветствие_ae353e94.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(задача_корень/'예제/리눅스ABI'/원본자료), '-o', str(KR_данные/Название)])
    исполняемый_фото = KR_данные/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(исполняемый_фото), str(KR_данные/'start.o'), str(KR_данные/'hello.o')])
    контент_ЗНАЧЕН = исполняемый_фото.read_bytes()
    assert len(контент_ЗНАЧЕН) <= 16384 and контент_ЗНАЧЕН[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', контент_ЗНАЧЕН, 16) == (2, 183) and b'JKOROS\0' not in контент_ЗНАЧЕН
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Сравнение_базовый_план = subprocess.check_output(['qemu-aarch64', str(исполняемый_фото), '한글인수'], cwd=str(KR_данные)).decode()
    assert Сравнение_базовый_план == 예상결과, Сравнение_базовый_план
    (KR_данные/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(исполняемый_фото)]))
    return исполняемый_фото, 예상결과


def запустить():
    KR_данные = задача_корень/'build/verification/elf'
    KR_данные.mkdir(parents=True, exist_ok=True)
    (KR_данные/'report.json').write_text('{"passed": false}\n')
    исполняемый_фото, 예상결과 = 리눅스예제(KR_данные)
    результат = subprocess.check_output(['python3', str(задача_корень/'инструменты/Выполнить_файл.py'), '--linux', str(исполняемый_фото), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in результат, результат
    (KR_данные/'serial.log').write_text(результат)
    원본=исполняемый_фото.read_bytes()
    программа_Заголовок_СМЕЩ=struct.unpack_from('<Q',원본,32)[0]
    for Название,СМЕЩ_ЗНАЧЕН,формат_b87fd068,ЗНАЧЕН in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',программа_Заголовок_СМЕЩ+4,'I',7),('kernel-address',программа_Заголовок_СМЕЩ+16,'Q',0x400000)]:
        неверный_данные=bytearray(원본);struct.pack_into('<'+формат_b87fd068,неверный_данные,СМЕЩ_ЗНАЧЕН,ЗНАЧЕН)
        путь=KR_данные/Название;путь.write_bytes(неверный_данные)
        거부결과=subprocess.run(['python3',str(задача_корень/'инструменты/Выполнить_файл.py'),'--linux',str(путь)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Название,거부결과.stdout)
    проверка_Отчет = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(исполняемый_фото.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_данные/'report.json').write_text(json.dumps(проверка_Отчет, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': запустить()
