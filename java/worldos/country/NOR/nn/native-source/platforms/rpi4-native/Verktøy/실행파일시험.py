#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Utfør_kommando import spegle_rot


def 리눅스예제(forretningsmål_data):
    forretningsmål_data.mkdir(parents=True, exist_ok=True)
    for 원본자료, Namn in [('Køyr_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(spegle_rot/'예제/리눅스ABI'/원본자료), '-o', str(forretningsmål_data/Namn)])
    실행가능파일 = forretningsmål_data/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(forretningsmål_data/'start.o'), str(forretningsmål_data/'hello.o')])
    Innhald_VALUE = 실행가능파일.read_bytes()
    assert len(Innhald_VALUE) <= 16384 and Innhald_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Innhald_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Innhald_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Samanlikning_grunnline = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(forretningsmål_data)).decode()
    assert Samanlikning_grunnline == 예상결과, Samanlikning_grunnline
    (forretningsmål_data/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Køyr_2():
    forretningsmål_data = spegle_rot/'build/verification/elf'
    forretningsmål_data.mkdir(parents=True, exist_ok=True)
    (forretningsmål_data/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(forretningsmål_data)
    forretningsmål = subprocess.check_output(['python3', str(spegle_rot/'Verktøy/Utfør_fil.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in forretningsmål, forretningsmål
    (forretningsmål_data/'serial.log').write_text(forretningsmål)
    원본=실행가능파일.read_bytes()
    app_hode_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Namn,OFFSET_VALUE,format_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',app_hode_OFFSET+4,'I',7),('kernel-address',app_hode_OFFSET+16,'Q',0x400000)]:
        ugyldig_data=bytearray(원본);struct.pack_into('<'+format_b87fd068,ugyldig_data,OFFSET_VALUE,VALUE)
        STIGE=forretningsmål_data/Namn;STIGE.write_bytes(ugyldig_data)
        거부결과=subprocess.run(['python3',str(spegle_rot/'Verktøy/Utfør_fil.py'),'--linux',str(STIGE)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Namn,거부결과.stdout)
    validering_rapport = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (forretningsmål_data/'report.json').write_text(json.dumps(validering_rapport, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Køyr_2()
