#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from կատարել_հրաման import արձակել_արմատ


def 리눅스예제(չափ_տվյալ):
    չափ_տվյալ.mkdir(parents=True, exist_ok=True)
    for 원본자료, Անուն in [('Գործարկել.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(արձակել_արմատ/'예제/리눅스ABI'/원본자료), '-o', str(չափ_տվյալ/Անուն)])
    실행가능파일 = չափ_տվյալ/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(չափ_տվյալ/'start.o'), str(չափ_տվյալ/'hello.o')])
    Բովանդակություն_արժեք = 실행가능파일.read_bytes()
    assert len(Բովանդակություն_արժեք) <= 16384 and Բովանդակություն_արժեք[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Բովանդակություն_արժեք, 16) == (2, 183) and b'JKOROS\0' not in Բովանդակություն_արժեք
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(չափ_տվյալ)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (չափ_տվյալ/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Գործարկել():
    չափ_տվյալ = արձակել_արմատ/'build/verification/elf'
    չափ_տվյալ.mkdir(parents=True, exist_ok=True)
    (չափ_տվյալ/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(չափ_տվյալ)
    չափ = subprocess.check_output(['python3', str(արձակել_արմատ/'Գործիքներ/կատարել_նիշք.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in չափ, չափ
    (չափ_տվյալ/'serial.log').write_text(չափ)
    원본=실행가능파일.read_bytes()
    ծրագիր_Վերնագիր_Տեղաշարժում=struct.unpack_from('<Q',원본,32)[0]
    for Անուն,Տեղաշարժում_արժեք,ձեւաչափ_b87fd068,արժեք in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ծրագիր_Վերնագիր_Տեղաշարժում+4,'I',7),('kernel-address',ծրագիր_Վերնագիր_Տեղաշարժում+16,'Q',0x400000)]:
        անվավեր_տվյալ=bytearray(원본);struct.pack_into('<'+ձեւաչափ_b87fd068,անվավեր_տվյալ,Տեղաշարժում_արժեք,արժեք)
        Ճանապարհ=չափ_տվյալ/Անուն;Ճանապարհ.write_bytes(անվավեր_տվյալ)
        거부결과=subprocess.run(['python3',str(արձակել_արմատ/'Գործիքներ/կատարել_նիշք.py'),'--linux',str(Ճանապարհ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Անուն,거부결과.stdout)
    վավերացում_զեկույց = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (չափ_տվյալ/'report.json').write_text(json.dumps(վավերացում_զեկույց, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Գործարկել()
