#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from laksanakan_perintah import projek_akar


def 리눅스예제(ukuran_data):
    ukuran_data.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nama in [('Jalan.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(projek_akar/'예제/리눅스ABI'/원본자료), '-o', str(ukuran_data/Nama)])
    fail_boleh_laku_imej = ukuran_data/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(fail_boleh_laku_imej), str(ukuran_data/'start.o'), str(ukuran_data/'hello.o')])
    Kandungan_VALUE = fail_boleh_laku_imej.read_bytes()
    assert len(Kandungan_VALUE) <= 16384 and Kandungan_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Kandungan_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Kandungan_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Perbandingan_garis_asas = subprocess.check_output(['qemu-aarch64', str(fail_boleh_laku_imej), '한글인수'], cwd=str(ukuran_data)).decode()
    assert Perbandingan_garis_asas == 예상결과, Perbandingan_garis_asas
    (ukuran_data/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(fail_boleh_laku_imej)]))
    return fail_boleh_laku_imej, 예상결과


def Jalan():
    ukuran_data = projek_akar/'build/verification/elf'
    ukuran_data.mkdir(parents=True, exist_ok=True)
    (ukuran_data/'report.json').write_text('{"passed": false}\n')
    fail_boleh_laku_imej, 예상결과 = 리눅스예제(ukuran_data)
    ukuran = subprocess.check_output(['python3', str(projek_akar/'alat/laksanakan_fail.py'), '--linux', str(fail_boleh_laku_imej), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ukuran, ukuran
    (ukuran_data/'serial.log').write_text(ukuran)
    원본=fail_boleh_laku_imej.read_bytes()
    aplikasi_Pengepala_Ofset=struct.unpack_from('<Q',원본,32)[0]
    for Nama,Ofset_VALUE,format_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',aplikasi_Pengepala_Ofset+4,'I',7),('kernel-address',aplikasi_Pengepala_Ofset+16,'Q',0x400000)]:
        tak_sah_data=bytearray(원본);struct.pack_into('<'+format_b87fd068,tak_sah_data,Ofset_VALUE,VALUE)
        LALUAN=ukuran_data/Nama;LALUAN.write_bytes(tak_sah_data)
        거부결과=subprocess.run(['python3',str(projek_akar/'alat/laksanakan_fail.py'),'--linux',str(LALUAN)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nama,거부결과.stdout)
    pensahihan_lapor = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(fail_boleh_laku_imej.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ukuran_data/'report.json').write_text(json.dumps(pensahihan_lapor, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Jalan()
