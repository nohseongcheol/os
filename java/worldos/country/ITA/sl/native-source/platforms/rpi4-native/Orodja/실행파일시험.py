#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Izvedi_ukaz import pobuda_koren


def 리눅스예제(KR_podatki):
    KR_podatki.mkdir(parents=True, exist_ok=True)
    for 원본자료, Ime in [('Zaženi.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(pobuda_koren/'예제/리눅스ABI'/원본자료), '-o', str(KR_podatki/Ime)])
    실행가능파일 = KR_podatki/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(KR_podatki/'start.o'), str(KR_podatki/'hello.o')])
    vsebina_VALUE = 실행가능파일.read_bytes()
    assert len(vsebina_VALUE) <= 16384 and vsebina_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', vsebina_VALUE, 16) == (2, 183) and b'JKOROS\0' not in vsebina_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Primerjava_osnova = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(KR_podatki)).decode()
    assert Primerjava_osnova == 예상결과, Primerjava_osnova
    (KR_podatki/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Zaženi():
    KR_podatki = pobuda_koren/'build/verification/elf'
    KR_podatki.mkdir(parents=True, exist_ok=True)
    (KR_podatki/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(KR_podatki)
    REZULTAT = subprocess.check_output(['python3', str(pobuda_koren/'Orodja/Izvedi_Datoteka.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in REZULTAT, REZULTAT
    (KR_podatki/'serial.log').write_text(REZULTAT)
    원본=실행가능파일.read_bytes()
    aplikacija_Glava_odmik=struct.unpack_from('<Q',원본,32)[0]
    for Ime,odmik_VALUE,oblika_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',aplikacija_Glava_odmik+4,'I',7),('kernel-address',aplikacija_Glava_odmik+16,'Q',0x400000)]:
        neveljaven_podatki=bytearray(원본);struct.pack_into('<'+oblika_b87fd068,neveljaven_podatki,odmik_VALUE,VALUE)
        POT=KR_podatki/Ime;POT.write_bytes(neveljaven_podatki)
        거부결과=subprocess.run(['python3',str(pobuda_koren/'Orodja/Izvedi_Datoteka.py'),'--linux',str(POT)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Ime,거부결과.stdout)
    preverjanje_veljavnosti_prijavi = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_podatki/'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Zaženi()
