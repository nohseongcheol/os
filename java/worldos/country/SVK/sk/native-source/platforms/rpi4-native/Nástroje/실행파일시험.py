#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Vykonať_príkaz import akcia_koreň


def 리눅스예제(KR_údaje):
    KR_údaje.mkdir(parents=True, exist_ok=True)
    for 원본자료, Názov in [('Spustiť_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(akcia_koreň/'예제/리눅스ABI'/원본자료), '-o', str(KR_údaje/Názov)])
    spustiteľný_súbor_IMAGE = KR_údaje/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(spustiteľný_súbor_IMAGE), str(KR_údaje/'start.o'), str(KR_údaje/'hello.o')])
    obsah_VALUE = spustiteľný_súbor_IMAGE.read_bytes()
    assert len(obsah_VALUE) <= 16384 and obsah_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', obsah_VALUE, 16) == (2, 183) and b'JKOROS\0' not in obsah_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Porovnanie_pôvodný_plán = subprocess.check_output(['qemu-aarch64', str(spustiteľný_súbor_IMAGE), '한글인수'], cwd=str(KR_údaje)).decode()
    assert Porovnanie_pôvodný_plán == 예상결과, Porovnanie_pôvodný_plán
    (KR_údaje/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(spustiteľný_súbor_IMAGE)]))
    return spustiteľný_súbor_IMAGE, 예상결과


def Spustiť_2():
    KR_údaje = akcia_koreň/'build/verification/elf'
    KR_údaje.mkdir(parents=True, exist_ok=True)
    (KR_údaje/'report.json').write_text('{"passed": false}\n')
    spustiteľný_súbor_IMAGE, 예상결과 = 리눅스예제(KR_údaje)
    KR = subprocess.check_output(['python3', str(akcia_koreň/'Nástroje/Vykonať_Súbor.py'), '--linux', str(spustiteľný_súbor_IMAGE), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in KR, KR
    (KR_údaje/'serial.log').write_text(KR)
    원본=spustiteľný_súbor_IMAGE.read_bytes()
    program_Nadpis_Posun=struct.unpack_from('<Q',원본,32)[0]
    for Názov,Posun_VALUE,formát_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',program_Nadpis_Posun+4,'I',7),('kernel-address',program_Nadpis_Posun+16,'Q',0x400000)]:
        neplatné_údaje=bytearray(원본);struct.pack_into('<'+formát_b87fd068,neplatné_údaje,Posun_VALUE,VALUE)
        Cesta=KR_údaje/Názov;Cesta.write_bytes(neplatné_údaje)
        거부결과=subprocess.run(['python3',str(akcia_koreň/'Nástroje/Vykonať_Súbor.py'),'--linux',str(Cesta)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Názov,거부결과.stdout)
    overenie_správa = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(spustiteľný_súbor_IMAGE.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_údaje/'report.json').write_text(json.dumps(overenie_správa, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Spustiť_2()
