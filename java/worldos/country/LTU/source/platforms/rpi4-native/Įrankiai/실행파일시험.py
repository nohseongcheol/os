#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Vykdyti_komanda import Project_šaknis


def 리눅스예제(KR_duomenys):
    KR_duomenys.mkdir(parents=True, exist_ok=True)
    for 원본자료, Pavadinimas_2 in [('Paleisti.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Project_šaknis/'예제/리눅스ABI'/원본자료), '-o', str(KR_duomenys/Pavadinimas_2)])
    실행가능파일 = KR_duomenys/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(KR_duomenys/'start.o'), str(KR_duomenys/'hello.o')])
    Turinys_VALUE = 실행가능파일.read_bytes()
    assert len(Turinys_VALUE) <= 16384 and Turinys_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Turinys_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Turinys_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Palyginimas_bazinė_linija = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(KR_duomenys)).decode()
    assert Palyginimas_bazinė_linija == 예상결과, Palyginimas_bazinė_linija
    (KR_duomenys/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Paleisti():
    KR_duomenys = Project_šaknis/'build/verification/elf'
    KR_duomenys.mkdir(parents=True, exist_ok=True)
    (KR_duomenys/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(KR_duomenys)
    REZULTATAS = subprocess.check_output(['python3', str(Project_šaknis/'Įrankiai/Vykdyti_Failas.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in REZULTATAS, REZULTATAS
    (KR_duomenys/'serial.log').write_text(REZULTATAS)
    원본=실행가능파일.read_bytes()
    programa_Antraštė_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Pavadinimas_2,OFFSET_VALUE,formatas_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',programa_Antraštė_OFFSET+4,'I',7),('kernel-address',programa_Antraštė_OFFSET+16,'Q',0x400000)]:
        neleistinas_duomenys=bytearray(원본);struct.pack_into('<'+formatas_b87fd068,neleistinas_duomenys,OFFSET_VALUE,VALUE)
        KELIAS=KR_duomenys/Pavadinimas_2;KELIAS.write_bytes(neleistinas_duomenys)
        거부결과=subprocess.run(['python3',str(Project_šaknis/'Įrankiai/Vykdyti_Failas.py'),'--linux',str(KELIAS)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Pavadinimas_2,거부결과.stdout)
    tikrinimas_pranešti = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_duomenys/'report.json').write_text(json.dumps(tikrinimas_pranešti, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Paleisti()
