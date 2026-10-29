#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from ausféieren_Befeel import projezéieren_Racinn


def 리눅스예제(Mooss_Daten):
    Mooss_Daten.mkdir(parents=True, exist_ok=True)
    for 원본자료, Numm in [('Laf.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(projezéieren_Racinn/'예제/리눅스ABI'/원본자료), '-o', str(Mooss_Daten/Numm)])
    실행가능파일 = Mooss_Daten/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(Mooss_Daten/'start.o'), str(Mooss_Daten/'hello.o')])
    Inhalt_VALUE = 실행가능파일.read_bytes()
    assert len(Inhalt_VALUE) <= 16384 and Inhalt_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Inhalt_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Inhalt_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(Mooss_Daten)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (Mooss_Daten/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Laf():
    Mooss_Daten = projezéieren_Racinn/'build/verification/elf'
    Mooss_Daten.mkdir(parents=True, exist_ok=True)
    (Mooss_Daten/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(Mooss_Daten)
    Mooss = subprocess.check_output(['python3', str(projezéieren_Racinn/'Tools/ausféieren_Fichier.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in Mooss, Mooss
    (Mooss_Daten/'serial.log').write_text(Mooss)
    원본=실행가능파일.read_bytes()
    App_En_tête_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Numm,OFFSET_VALUE,Format_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',App_En_tête_OFFSET+4,'I',7),('kernel-address',App_En_tête_OFFSET+16,'Q',0x400000)]:
        ongëlteg_Daten=bytearray(원본);struct.pack_into('<'+Format_b87fd068,ongëlteg_Daten,OFFSET_VALUE,VALUE)
        Wee=Mooss_Daten/Numm;Wee.write_bytes(ongëlteg_Daten)
        거부결과=subprocess.run(['python3',str(projezéieren_Racinn/'Tools/ausféieren_Fichier.py'),'--linux',str(Wee)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Numm,거부결과.stdout)
    Validatioun_mellen = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (Mooss_Daten/'report.json').write_text(json.dumps(Validatioun_mellen, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Laf()
