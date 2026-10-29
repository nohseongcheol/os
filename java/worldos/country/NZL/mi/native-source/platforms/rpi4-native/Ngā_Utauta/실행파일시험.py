#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from kawe_tono import whakaatu_pūtake


def 리눅스예제(mēhua_raraunga):
    mēhua_raraunga.mkdir(parents=True, exist_ok=True)
    for 원본자료, Ingoa in [('whakahaere.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(whakaatu_pūtake/'예제/리눅스ABI'/원본자료), '-o', str(mēhua_raraunga/Ingoa)])
    실행가능파일 = mēhua_raraunga/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(mēhua_raraunga/'start.o'), str(mēhua_raraunga/'hello.o')])
    Ihirangi_uara = 실행가능파일.read_bytes()
    assert len(Ihirangi_uara) <= 16384 and Ihirangi_uara[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Ihirangi_uara, 16) == (2, 183) and b'JKOROS\0' not in Ihirangi_uara
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(mēhua_raraunga)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (mēhua_raraunga/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def whakahaere():
    mēhua_raraunga = whakaatu_pūtake/'build/verification/elf'
    mēhua_raraunga.mkdir(parents=True, exist_ok=True)
    (mēhua_raraunga/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(mēhua_raraunga)
    mēhua = subprocess.check_output(['python3', str(whakaatu_pūtake/'Ngā_Utauta/kawe_kōnae.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in mēhua, mēhua
    (mēhua_raraunga/'serial.log').write_text(mēhua)
    원본=실행가능파일.read_bytes()
    kaupapa_Pane_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Ingoa,OFFSET_uara,hōputu_b87fd068,uara in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',kaupapa_Pane_OFFSET+4,'I',7),('kernel-address',kaupapa_Pane_OFFSET+16,'Q',0x400000)]:
        muhu_raraunga=bytearray(원본);struct.pack_into('<'+hōputu_b87fd068,muhu_raraunga,OFFSET_uara,uara)
        ara=mēhua_raraunga/Ingoa;ara.write_bytes(muhu_raraunga)
        거부결과=subprocess.run(['python3',str(whakaatu_pūtake/'Ngā_Utauta/kawe_kōnae.py'),'--linux',str(ara)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Ingoa,거부결과.stdout)
    whakamana_pūrongo = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (mēhua_raraunga/'report.json').write_text(json.dumps(whakamana_pūrongo, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': whakahaere()
