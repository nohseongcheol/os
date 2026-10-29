#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Izpildīt_komanda import Project_sakne


def 리눅스예제(mērs_dati):
    mērs_dati.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nosaukums in [('Palaist.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Project_sakne/'예제/리눅스ABI'/원본자료), '-o', str(mērs_dati/Nosaukums)])
    izpildāms_fails_IMAGE = mērs_dati/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(izpildāms_fails_IMAGE), str(mērs_dati/'start.o'), str(mērs_dati/'hello.o')])
    Saturs_VALUE = izpildāms_fails_IMAGE.read_bytes()
    assert len(Saturs_VALUE) <= 16384 and Saturs_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Saturs_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Saturs_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Salīdzinājums_bāze = subprocess.check_output(['qemu-aarch64', str(izpildāms_fails_IMAGE), '한글인수'], cwd=str(mērs_dati)).decode()
    assert Salīdzinājums_bāze == 예상결과, Salīdzinājums_bāze
    (mērs_dati/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(izpildāms_fails_IMAGE)]))
    return izpildāms_fails_IMAGE, 예상결과


def Palaist():
    mērs_dati = Project_sakne/'build/verification/elf'
    mērs_dati.mkdir(parents=True, exist_ok=True)
    (mērs_dati/'report.json').write_text('{"passed": false}\n')
    izpildāms_fails_IMAGE, 예상결과 = 리눅스예제(mērs_dati)
    mērs = subprocess.check_output(['python3', str(Project_sakne/'Rīki/Izpildīt_Fails.py'), '--linux', str(izpildāms_fails_IMAGE), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in mērs, mērs
    (mērs_dati/'serial.log').write_text(mērs)
    원본=izpildāms_fails_IMAGE.read_bytes()
    programma_galvene_Nobīde=struct.unpack_from('<Q',원본,32)[0]
    for Nosaukums,Nobīde_VALUE,formāts_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',programma_galvene_Nobīde+4,'I',7),('kernel-address',programma_galvene_Nobīde+16,'Q',0x400000)]:
        nederīgs_dati=bytearray(원본);struct.pack_into('<'+formāts_b87fd068,nederīgs_dati,Nobīde_VALUE,VALUE)
        CEĻŠ=mērs_dati/Nosaukums;CEĻŠ.write_bytes(nederīgs_dati)
        거부결과=subprocess.run(['python3',str(Project_sakne/'Rīki/Izpildīt_Fails.py'),'--linux',str(CEĻŠ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nosaukums,거부결과.stdout)
    validācija_ziņot = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(izpildāms_fails_IMAGE.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (mērs_dati/'report.json').write_text(json.dumps(validācija_ziņot, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Palaist()
