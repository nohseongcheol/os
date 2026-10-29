#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Täida_käsk import Project_juur


def 리눅스예제(näitaja_andmed):
    näitaja_andmed.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nimi_2 in [('Käivita_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Project_juur/'예제/리눅스ABI'/원본자료), '-o', str(näitaja_andmed/Nimi_2)])
    실행가능파일 = näitaja_andmed/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(näitaja_andmed/'start.o'), str(näitaja_andmed/'hello.o')])
    Sisu_VALUE = 실행가능파일.read_bytes()
    assert len(Sisu_VALUE) <= 16384 and Sisu_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Sisu_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Sisu_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Võrdlus_alusjoon = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(näitaja_andmed)).decode()
    assert Võrdlus_alusjoon == 예상결과, Võrdlus_alusjoon
    (näitaja_andmed/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Käivita_2():
    näitaja_andmed = Project_juur/'build/verification/elf'
    näitaja_andmed.mkdir(parents=True, exist_ok=True)
    (näitaja_andmed/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(näitaja_andmed)
    TULEMUS = subprocess.check_output(['python3', str(Project_juur/'Tööriistad/Täida_Fail.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in TULEMUS, TULEMUS
    (näitaja_andmed/'serial.log').write_text(TULEMUS)
    원본=실행가능파일.read_bytes()
    programm_Päis_nihe=struct.unpack_from('<Q',원본,32)[0]
    for Nimi_2,nihe_VALUE,vorming_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',programm_Päis_nihe+4,'I',7),('kernel-address',programm_Päis_nihe+16,'Q',0x400000)]:
        kehtetu_andmed=bytearray(원본);struct.pack_into('<'+vorming_b87fd068,kehtetu_andmed,nihe_VALUE,VALUE)
        RADA=näitaja_andmed/Nimi_2;RADA.write_bytes(kehtetu_andmed)
        거부결과=subprocess.run(['python3',str(Project_juur/'Tööriistad/Täida_Fail.py'),'--linux',str(RADA)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nimi_2,거부결과.stdout)
    kinnitamine_aruanne = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (näitaja_andmed/'report.json').write_text(json.dumps(kinnitamine_aruanne, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Käivita_2()
