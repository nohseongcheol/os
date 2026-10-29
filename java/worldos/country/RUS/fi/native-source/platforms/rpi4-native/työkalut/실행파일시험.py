#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Suorita_komento import aloite_juuri


def 리눅스예제(KR_data):
    KR_data.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nimi in [('Suorita_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(aloite_juuri/'예제/리눅스ABI'/원본자료), '-o', str(KR_data/Nimi)])
    suoritettava_tiedosto_KUVA = KR_data/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(suoritettava_tiedosto_KUVA), str(KR_data/'start.o'), str(KR_data/'hello.o')])
    Sisältö_ARVO = suoritettava_tiedosto_KUVA.read_bytes()
    assert len(Sisältö_ARVO) <= 16384 and Sisältö_ARVO[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Sisältö_ARVO, 16) == (2, 183) and b'JKOROS\0' not in Sisältö_ARVO
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Vertailu_perus = subprocess.check_output(['qemu-aarch64', str(suoritettava_tiedosto_KUVA), '한글인수'], cwd=str(KR_data)).decode()
    assert Vertailu_perus == 예상결과, Vertailu_perus
    (KR_data/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(suoritettava_tiedosto_KUVA)]))
    return suoritettava_tiedosto_KUVA, 예상결과


def Suorita_2():
    KR_data = aloite_juuri/'build/verification/elf'
    KR_data.mkdir(parents=True, exist_ok=True)
    (KR_data/'report.json').write_text('{"passed": false}\n')
    suoritettava_tiedosto_KUVA, 예상결과 = 리눅스예제(KR_data)
    TULOS = subprocess.check_output(['python3', str(aloite_juuri/'työkalut/Suorita_Tiedosto.py'), '--linux', str(suoritettava_tiedosto_KUVA), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in TULOS, TULOS
    (KR_data/'serial.log').write_text(TULOS)
    원본=suoritettava_tiedosto_KUVA.read_bytes()
    ohjelma_otsikko_SIIRTYMÄ=struct.unpack_from('<Q',원본,32)[0]
    for Nimi,SIIRTYMÄ_ARVO,muoto_b87fd068,ARVO in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ohjelma_otsikko_SIIRTYMÄ+4,'I',7),('kernel-address',ohjelma_otsikko_SIIRTYMÄ+16,'Q',0x400000)]:
        pätemätön_data=bytearray(원본);struct.pack_into('<'+muoto_b87fd068,pätemätön_data,SIIRTYMÄ_ARVO,ARVO)
        polku_2=KR_data/Nimi;polku_2.write_bytes(pätemätön_data)
        거부결과=subprocess.run(['python3',str(aloite_juuri/'työkalut/Suorita_Tiedosto.py'),'--linux',str(polku_2)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nimi,거부결과.stdout)
    vahvistus_raportti = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(suoritettava_tiedosto_KUVA.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_data/'report.json').write_text(json.dumps(vahvistus_raportti, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Suorita_2()
