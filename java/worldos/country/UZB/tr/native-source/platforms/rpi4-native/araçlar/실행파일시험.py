#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from yürütmek_komut import işlem_kök


def 리눅스예제(KR_veri):
    KR_veri.mkdir(parents=True, exist_ok=True)
    for 원본자료, İsim in [('çalıştır.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(işlem_kök/'예제/리눅스ABI'/원본자료), '-o', str(KR_veri/İsim)])
    yürütülebilir_RESİM = KR_veri/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(yürütülebilir_RESİM), str(KR_veri/'start.o'), str(KR_veri/'hello.o')])
    içerik_değer = yürütülebilir_RESİM.read_bytes()
    assert len(içerik_değer) <= 16384 and içerik_değer[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', içerik_değer, 16) == (2, 183) and b'JKOROS\0' not in içerik_değer
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Karşılaştırma_temel = subprocess.check_output(['qemu-aarch64', str(yürütülebilir_RESİM), '한글인수'], cwd=str(KR_veri)).decode()
    assert Karşılaştırma_temel == 예상결과, Karşılaştırma_temel
    (KR_veri/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(yürütülebilir_RESİM)]))
    return yürütülebilir_RESİM, 예상결과


def çalıştır():
    KR_veri = işlem_kök/'build/verification/elf'
    KR_veri.mkdir(parents=True, exist_ok=True)
    (KR_veri/'report.json').write_text('{"passed": false}\n')
    yürütülebilir_RESİM, 예상결과 = 리눅스예제(KR_veri)
    sonuç = subprocess.check_output(['python3', str(işlem_kök/'araçlar/yürütmek_Dosya.py'), '--linux', str(yürütülebilir_RESİM), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in sonuç, sonuç
    (KR_veri/'serial.log').write_text(sonuç)
    원본=yürütülebilir_RESİM.read_bytes()
    program_Başlık_Ofset=struct.unpack_from('<Q',원본,32)[0]
    for İsim,Ofset_değer,biçim_b87fd068,değer in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',program_Başlık_Ofset+4,'I',7),('kernel-address',program_Başlık_Ofset+16,'Q',0x400000)]:
        geçersiz_veri=bytearray(원본);struct.pack_into('<'+biçim_b87fd068,geçersiz_veri,Ofset_değer,değer)
        yol=KR_veri/İsim;yol.write_bytes(geçersiz_veri)
        거부결과=subprocess.run(['python3',str(işlem_kök/'araçlar/yürütmek_Dosya.py'),'--linux',str(yol)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(İsim,거부결과.stdout)
    doğrulama_Rapor = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(yürütülebilir_RESİM.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_veri/'report.json').write_text(json.dumps(doğrulama_Rapor, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': çalıştır()
