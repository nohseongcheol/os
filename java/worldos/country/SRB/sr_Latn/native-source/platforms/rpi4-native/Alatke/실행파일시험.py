#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Izvrši_komanda import radnja_koren


def 리눅스예제(KR_podaci):
    KR_podaci.mkdir(parents=True, exist_ok=True)
    for 원본자료, ime in [('koristiti.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(radnja_koren/'예제/리눅스ABI'/원본자료), '-o', str(KR_podaci/ime)])
    실행가능파일 = KR_podaci/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(KR_podaci/'start.o'), str(KR_podaci/'hello.o')])
    Sadržaj_VALUE = 실행가능파일.read_bytes()
    assert len(Sadržaj_VALUE) <= 16384 and Sadržaj_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Sadržaj_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Sadržaj_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Poređenje_osnova = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(KR_podaci)).decode()
    assert Poređenje_osnova == 예상결과, Poređenje_osnova
    (KR_podaci/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def koristiti():
    KR_podaci = radnja_koren/'build/verification/elf'
    KR_podaci.mkdir(parents=True, exist_ok=True)
    (KR_podaci/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(KR_podaci)
    KR = subprocess.check_output(['python3', str(radnja_koren/'Alatke/Izvrši_Datoteka.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in KR, KR
    (KR_podaci/'serial.log').write_text(KR)
    원본=실행가능파일.read_bytes()
    program_Zaglavlje_Pomak=struct.unpack_from('<Q',원본,32)[0]
    for ime,Pomak_VALUE,format_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',program_Zaglavlje_Pomak+4,'I',7),('kernel-address',program_Zaglavlje_Pomak+16,'Q',0x400000)]:
        nevažeći_podaci=bytearray(원본);struct.pack_into('<'+format_b87fd068,nevažeći_podaci,Pomak_VALUE,VALUE)
        putanja=KR_podaci/ime;putanja.write_bytes(nevažeći_podaci)
        거부결과=subprocess.run(['python3',str(radnja_koren/'Alatke/Izvrši_Datoteka.py'),'--linux',str(putanja)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(ime,거부결과.stdout)
    provera_valjanosti_izveštaj = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_podaci/'report.json').write_text(json.dumps(provera_valjanosti_izveštaj, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': koristiti()
