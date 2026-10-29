#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from icra_etmək_əmr import Project_kök


def 리눅스예제(ölçü_verilənlər):
    ölçü_verilənlər.mkdir(parents=True, exist_ok=True)
    for 원본자료, Ad in [('İcra_Et.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Project_kök/'예제/리눅스ABI'/원본자료), '-o', str(ölçü_verilənlər/Ad)])
    실행가능파일 = ölçü_verilənlər/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(ölçü_verilənlər/'start.o'), str(ölçü_verilənlər/'hello.o')])
    Məzmun_VALUE = 실행가능파일.read_bytes()
    assert len(Məzmun_VALUE) <= 16384 and Məzmun_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Məzmun_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Məzmun_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Müqayisə_baza_xətti = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(ölçü_verilənlər)).decode()
    assert Müqayisə_baza_xətti == 예상결과, Müqayisə_baza_xətti
    (ölçü_verilənlər/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def İcra_Et():
    ölçü_verilənlər = Project_kök/'build/verification/elf'
    ölçü_verilənlər.mkdir(parents=True, exist_ok=True)
    (ölçü_verilənlər/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(ölçü_verilənlər)
    ölçü = subprocess.check_output(['python3', str(Project_kök/'Alətlər/icra_etmək_fayl.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ölçü, ölçü
    (ölçü_verilənlər/'serial.log').write_text(ölçü)
    원본=실행가능파일.read_bytes()
    proqram_Başlıq_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Ad,OFFSET_VALUE,format_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',proqram_Başlıq_OFFSET+4,'I',7),('kernel-address',proqram_Başlıq_OFFSET+16,'Q',0x400000)]:
        yanlış_verilənlər=bytearray(원본);struct.pack_into('<'+format_b87fd068,yanlış_verilənlər,OFFSET_VALUE,VALUE)
        Cığır=ölçü_verilənlər/Ad;Cığır.write_bytes(yanlış_verilənlər)
        거부결과=subprocess.run(['python3',str(Project_kök/'Alətlər/icra_etmək_fayl.py'),'--linux',str(Cığır)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Ad,거부결과.stdout)
    yoxlama_hesabat = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ölçü_verilənlər/'report.json').write_text(json.dumps(yoxlama_hesabat, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': İcra_Et()
