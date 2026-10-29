#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Izvrši_komanda import projicirati_koijen


def 리눅스예제(mjera_podaci):
    mjera_podaci.mkdir(parents=True, exist_ok=True)
    for 원본자료, Naziv in [('Pokreni.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(projicirati_koijen/'예제/리눅스ABI'/원본자료), '-o', str(mjera_podaci/Naziv)])
    실행가능파일 = mjera_podaci/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(mjera_podaci/'start.o'), str(mjera_podaci/'hello.o')])
    Sadržaj_VALUE = 실행가능파일.read_bytes()
    assert len(Sadržaj_VALUE) <= 16384 and Sadržaj_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Sadržaj_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Sadržaj_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Poređenje_osnovna_linija = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(mjera_podaci)).decode()
    assert Poređenje_osnovna_linija == 예상결과, Poređenje_osnovna_linija
    (mjera_podaci/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Pokreni():
    mjera_podaci = projicirati_koijen/'build/verification/elf'
    mjera_podaci.mkdir(parents=True, exist_ok=True)
    (mjera_podaci/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(mjera_podaci)
    mjera = subprocess.check_output(['python3', str(projicirati_koijen/'Alati/Izvrši_fajl.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in mjera, mjera
    (mjera_podaci/'serial.log').write_text(mjera)
    원본=실행가능파일.read_bytes()
    program_Zaglavlje_Pomak=struct.unpack_from('<Q',원본,32)[0]
    for Naziv,Pomak_VALUE,format_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',program_Zaglavlje_Pomak+4,'I',7),('kernel-address',program_Zaglavlje_Pomak+16,'Q',0x400000)]:
        nevažeće_podaci=bytearray(원본);struct.pack_into('<'+format_b87fd068,nevažeće_podaci,Pomak_VALUE,VALUE)
        Putanja=mjera_podaci/Naziv;Putanja.write_bytes(nevažeće_podaci)
        거부결과=subprocess.run(['python3',str(projicirati_koijen/'Alati/Izvrši_fajl.py'),'--linux',str(Putanja)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Naziv,거부결과.stdout)
    provjera_izvještaj = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (mjera_podaci/'report.json').write_text(json.dumps(provjera_izvještaj, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Pokreni()
