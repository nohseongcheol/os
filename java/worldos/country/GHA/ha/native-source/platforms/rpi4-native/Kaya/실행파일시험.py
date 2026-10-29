#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from gudanar_Umarni import 기준


def 리눅스예제(결과자료):
    결과자료.mkdir(parents=True, exist_ok=True)
    for 원본자료, Suna in [('Tafiyar_da.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(기준/'예제/리눅스ABI'/원본자료), '-o', str(결과자료/Suna)])
    실행가능파일 = 결과자료/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(결과자료/'start.o'), str(결과자료/'hello.o')])
    kunshiya_Daraja = 실행가능파일.read_bytes()
    assert len(kunshiya_Daraja) <= 16384 and kunshiya_Daraja[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', kunshiya_Daraja, 16) == (2, 183) and b'JKOROS\0' not in kunshiya_Daraja
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Kwatantawa_Ginshiken_aiki = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(결과자료)).decode()
    assert Kwatantawa_Ginshiken_aiki == 예상결과, Kwatantawa_Ginshiken_aiki
    (결과자료/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Tafiyar_da():
    결과자료 = 기준/'build/verification/elf'
    결과자료.mkdir(parents=True, exist_ok=True)
    (결과자료/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(결과자료)
    결과 = subprocess.check_output(['python3', str(기준/'Kaya/gudanar_Fayil.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in 결과, 결과
    (결과자료/'serial.log').write_text(결과)
    원본=실행가능파일.read_bytes()
    Shiri_Kai_Sassautawa=struct.unpack_from('<Q',원본,32)[0]
    for Suna,Sassautawa_Daraja,zubi_b87fd068,Daraja in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',Shiri_Kai_Sassautawa+4,'I',7),('kernel-address',Shiri_Kai_Sassautawa+16,'Q',0x400000)]:
        mara_ƙarfi_Tarin_bayani=bytearray(원본);struct.pack_into('<'+zubi_b87fd068,mara_ƙarfi_Tarin_bayani,Sassautawa_Daraja,Daraja)
        Hanyar_shiga=결과자료/Suna;Hanyar_shiga.write_bytes(mara_ƙarfi_Tarin_bayani)
        거부결과=subprocess.run(['python3',str(기준/'Kaya/gudanar_Fayil.py'),'--linux',str(Hanyar_shiga)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Suna,거부결과.stdout)
    amincewa_Rahoto = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (결과자료/'report.json').write_text(json.dumps(amincewa_Rahoto, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Tafiyar_da()
