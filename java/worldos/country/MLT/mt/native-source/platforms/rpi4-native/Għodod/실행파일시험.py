#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from eżegwixxa_kmand import pprojetta_għerq


def 리눅스예제(miżura_data):
    miżura_data.mkdir(parents=True, exist_ok=True)
    for 원본자료, isem in [('serje.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(pprojetta_għerq/'예제/리눅스ABI'/원본자료), '-o', str(miżura_data/isem)])
    실행가능파일 = miżura_data/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(miżura_data/'start.o'), str(miżura_data/'hello.o')])
    Kontenut_VALUE = 실행가능파일.read_bytes()
    assert len(Kontenut_VALUE) <= 16384 and Kontenut_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Kontenut_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Kontenut_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(miżura_data)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (miżura_data/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def serje():
    miżura_data = pprojetta_għerq/'build/verification/elf'
    miżura_data.mkdir(parents=True, exist_ok=True)
    (miżura_data/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(miżura_data)
    miżura = subprocess.check_output(['python3', str(pprojetta_għerq/'Għodod/eżegwixxa_fajl.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in miżura, miżura
    (miżura_data/'serial.log').write_text(miżura)
    원본=실행가능파일.read_bytes()
    programm_Intestazzjoni_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for isem,OFFSET_VALUE,format_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',programm_Intestazzjoni_OFFSET+4,'I',7),('kernel-address',programm_Intestazzjoni_OFFSET+16,'Q',0x400000)]:
        invalidu_data=bytearray(원본);struct.pack_into('<'+format_b87fd068,invalidu_data,OFFSET_VALUE,VALUE)
        mogħdija=miżura_data/isem;mogħdija.write_bytes(invalidu_data)
        거부결과=subprocess.run(['python3',str(pprojetta_għerq/'Għodod/eżegwixxa_fajl.py'),'--linux',str(mogħdija)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(isem,거부결과.stdout)
    validazzjoni_rapport = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (miżura_data/'report.json').write_text(json.dumps(validazzjoni_rapport, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': serje()
