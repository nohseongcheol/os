#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Jalankan_perintah import Tugas_akar


def 리눅스예제(KR_data):
    KR_data.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nama_2 in [('jalankan.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Tugas_akar/'예제/리눅스ABI'/원본자료), '-o', str(KR_data/Nama_2)])
    실행가능파일 = KR_data/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(KR_data/'start.o'), str(KR_data/'hello.o')])
    Isi_VALUE = 실행가능파일.read_bytes()
    assert len(Isi_VALUE) <= 16384 and Isi_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Isi_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Isi_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Perbandingan_acuan_dasar = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(KR_data)).decode()
    assert Perbandingan_acuan_dasar == 예상결과, Perbandingan_acuan_dasar
    (KR_data/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def jalankan():
    KR_data = Tugas_akar/'build/verification/elf'
    KR_data.mkdir(parents=True, exist_ok=True)
    (KR_data/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(KR_data)
    hasil = subprocess.check_output(['python3', str(Tugas_akar/'alat/Jalankan_file.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in hasil, hasil
    (KR_data/'serial.log').write_text(hasil)
    원본=실행가능파일.read_bytes()
    apl_judul_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Nama_2,OFFSET_VALUE,format_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',apl_judul_OFFSET+4,'I',7),('kernel-address',apl_judul_OFFSET+16,'Q',0x400000)]:
        tidak_sahih_data=bytearray(원본);struct.pack_into('<'+format_b87fd068,tidak_sahih_data,OFFSET_VALUE,VALUE)
        jalur=KR_data/Nama_2;jalur.write_bytes(tidak_sahih_data)
        거부결과=subprocess.run(['python3',str(Tugas_akar/'alat/Jalankan_file.py'),'--linux',str(jalur)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nama_2,거부결과.stdout)
    validasi_lapor = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_data/'report.json').write_text(json.dumps(validasi_lapor, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': jalankan()
