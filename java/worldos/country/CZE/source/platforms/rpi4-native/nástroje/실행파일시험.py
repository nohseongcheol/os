#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Provést_příkaz import akce_kořen


def 리눅스예제(KV_data):
    KV_data.mkdir(parents=True, exist_ok=True)
    for 원본자료, Název in [('Spustit_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(akce_kořen/'예제/리눅스ABI'/원본자료), '-o', str(KV_data/Název)])
    spustitelný_image = KV_data/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(spustitelný_image), str(KV_data/'start.o'), str(KV_data/'hello.o')])
    Obsah_HODNOTA = spustitelný_image.read_bytes()
    assert len(Obsah_HODNOTA) <= 16384 and Obsah_HODNOTA[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Obsah_HODNOTA, 16) == (2, 183) and b'JKOROS\0' not in Obsah_HODNOTA
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Porovnání_účaří = subprocess.check_output(['qemu-aarch64', str(spustitelný_image), '한글인수'], cwd=str(KV_data)).decode()
    assert Porovnání_účaří == 예상결과, Porovnání_účaří
    (KV_data/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(spustitelný_image)]))
    return spustitelný_image, 예상결과


def Spustit_2():
    KV_data = akce_kořen/'build/verification/elf'
    KV_data.mkdir(parents=True, exist_ok=True)
    (KV_data/'report.json').write_text('{"passed": false}\n')
    spustitelný_image, 예상결과 = 리눅스예제(KV_data)
    VÝSLEDEK = subprocess.check_output(['python3', str(akce_kořen/'nástroje/Provést_Soubor.py'), '--linux', str(spustitelný_image), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in VÝSLEDEK, VÝSLEDEK
    (KV_data/'serial.log').write_text(VÝSLEDEK)
    원본=spustitelný_image.read_bytes()
    program_Nadpis_POSUN=struct.unpack_from('<Q',원본,32)[0]
    for Název,POSUN_HODNOTA,formát_b87fd068,HODNOTA in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',program_Nadpis_POSUN+4,'I',7),('kernel-address',program_Nadpis_POSUN+16,'Q',0x400000)]:
        neplatný_data=bytearray(원본);struct.pack_into('<'+formát_b87fd068,neplatný_data,POSUN_HODNOTA,HODNOTA)
        cesta_2=KV_data/Název;cesta_2.write_bytes(neplatný_data)
        거부결과=subprocess.run(['python3',str(akce_kořen/'nástroje/Provést_Soubor.py'),'--linux',str(cesta_2)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Název,거부결과.stdout)
    ověření_Zpráva = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(spustitelný_image.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KV_data/'report.json').write_text(json.dumps(ověření_Zpráva, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Spustit_2()
