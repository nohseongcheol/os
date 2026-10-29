#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from keyra_skipun import verk_rót


def 리눅스예제(mæld_stærð_gögn):
    mæld_stærð_gögn.mkdir(parents=True, exist_ok=True)
    for 원본자료, Heiti in [('Keyra_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(verk_rót/'예제/리눅스ABI'/원본자료), '-o', str(mæld_stærð_gögn/Heiti)])
    실행가능파일 = mæld_stærð_gögn/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(mæld_stærð_gögn/'start.o'), str(mæld_stærð_gögn/'hello.o')])
    Efni_VALUE = 실행가능파일.read_bytes()
    assert len(Efni_VALUE) <= 16384 and Efni_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Efni_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Efni_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Samanburður_grunnlína = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(mæld_stærð_gögn)).decode()
    assert Samanburður_grunnlína == 예상결과, Samanburður_grunnlína
    (mæld_stærð_gögn/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Keyra_2():
    mæld_stærð_gögn = verk_rót/'build/verification/elf'
    mæld_stærð_gögn.mkdir(parents=True, exist_ok=True)
    (mæld_stærð_gögn/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(mæld_stærð_gögn)
    NIÐURSTAÐA = subprocess.check_output(['python3', str(verk_rót/'Verkfæri/keyra_skrá.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in NIÐURSTAÐA, NIÐURSTAÐA
    (mæld_stærð_gögn/'serial.log').write_text(NIÐURSTAÐA)
    원본=실행가능파일.read_bytes()
    forrit_Haus_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Heiti,OFFSET_VALUE,snið_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',forrit_Haus_OFFSET+4,'I',7),('kernel-address',forrit_Haus_OFFSET+16,'Q',0x400000)]:
        ógilt_gögn=bytearray(원본);struct.pack_into('<'+snið_b87fd068,ógilt_gögn,OFFSET_VALUE,VALUE)
        SLÓÐ=mæld_stærð_gögn/Heiti;SLÓÐ.write_bytes(ógilt_gögn)
        거부결과=subprocess.run(['python3',str(verk_rót/'Verkfæri/keyra_skrá.py'),'--linux',str(SLÓÐ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Heiti,거부결과.stdout)
    prófun_skrá = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (mæld_stærð_gögn/'report.json').write_text(json.dumps(prófun_skrá, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Keyra_2()
