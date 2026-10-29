#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Wykonaj_polecenie import Project_korzeń


def 리눅스예제(KR_dane):
    KR_dane.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nazwa in [('Uruchom_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Project_korzeń/'예제/리눅스ABI'/원본자료), '-o', str(KR_dane/Nazwa)])
    wykonywalny_OBRAZ = KR_dane/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(wykonywalny_OBRAZ), str(KR_dane/'start.o'), str(KR_dane/'hello.o')])
    treść_WARTOŚĆ_cb0f2404 = wykonywalny_OBRAZ.read_bytes()
    assert len(treść_WARTOŚĆ_cb0f2404) <= 16384 and treść_WARTOŚĆ_cb0f2404[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', treść_WARTOŚĆ_cb0f2404, 16) == (2, 183) and b'JKOROS\0' not in treść_WARTOŚĆ_cb0f2404
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Porównanie_plan_bazowy = subprocess.check_output(['qemu-aarch64', str(wykonywalny_OBRAZ), '한글인수'], cwd=str(KR_dane)).decode()
    assert Porównanie_plan_bazowy == 예상결과, Porównanie_plan_bazowy
    (KR_dane/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(wykonywalny_OBRAZ)]))
    return wykonywalny_OBRAZ, 예상결과


def Uruchom_2():
    KR_dane = Project_korzeń/'build/verification/elf'
    KR_dane.mkdir(parents=True, exist_ok=True)
    (KR_dane/'report.json').write_text('{"passed": false}\n')
    wykonywalny_OBRAZ, 예상결과 = 리눅스예제(KR_dane)
    WYNIK = subprocess.check_output(['python3', str(Project_korzeń/'narzędzia/Wykonaj_Plik.py'), '--linux', str(wykonywalny_OBRAZ), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in WYNIK, WYNIK
    (KR_dane/'serial.log').write_text(WYNIK)
    원본=wykonywalny_OBRAZ.read_bytes()
    program_Nagłówek_przesunąć=struct.unpack_from('<Q',원본,32)[0]
    for Nazwa,przesunąć_WARTOŚĆ_450fc799,format_b87fd068,WARTOŚĆ in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',program_Nagłówek_przesunąć+4,'I',7),('kernel-address',program_Nagłówek_przesunąć+16,'Q',0x400000)]:
        nieważny_dane=bytearray(원본);struct.pack_into('<'+format_b87fd068,nieważny_dane,przesunąć_WARTOŚĆ_450fc799,WARTOŚĆ)
        ścieżka_2=KR_dane/Nazwa;ścieżka_2.write_bytes(nieważny_dane)
        거부결과=subprocess.run(['python3',str(Project_korzeń/'narzędzia/Wykonaj_Plik.py'),'--linux',str(ścieżka_2)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nazwa,거부결과.stdout)
    walidacja_Raport = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(wykonywalny_OBRAZ.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_dane/'report.json').write_text(json.dumps(walidacja_Raport, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Uruchom_2()
