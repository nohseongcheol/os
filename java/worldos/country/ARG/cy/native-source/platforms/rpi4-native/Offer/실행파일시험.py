#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Gweithredu_gorchymyn import prosiect_gwraidd


def 리눅스예제(mesur_data):
    mesur_data.mkdir(parents=True, exist_ok=True)
    for 원본자료, Enw in [('Gweithredu_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(prosiect_gwraidd/'예제/리눅스ABI'/원본자료), '-o', str(mesur_data/Enw)])
    실행가능파일 = mesur_data/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(mesur_data/'start.o'), str(mesur_data/'hello.o')])
    Cynnwys_VALUE = 실행가능파일.read_bytes()
    assert len(Cynnwys_VALUE) <= 16384 and Cynnwys_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Cynnwys_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Cynnwys_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(mesur_data)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (mesur_data/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Gweithredu_2():
    mesur_data = prosiect_gwraidd/'build/verification/elf'
    mesur_data.mkdir(parents=True, exist_ok=True)
    (mesur_data/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(mesur_data)
    mesur = subprocess.check_output(['python3', str(prosiect_gwraidd/'Offer/Gweithredu_ffeil.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in mesur, mesur
    (mesur_data/'serial.log').write_text(mesur)
    원본=실행가능파일.read_bytes()
    Rhaglen_Pennyn_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Enw,OFFSET_VALUE,fformat_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',Rhaglen_Pennyn_OFFSET+4,'I',7),('kernel-address',Rhaglen_Pennyn_OFFSET+16,'Q',0x400000)]:
        annilys_data=bytearray(원본);struct.pack_into('<'+fformat_b87fd068,annilys_data,OFFSET_VALUE,VALUE)
        LLWYBR=mesur_data/Enw;LLWYBR.write_bytes(annilys_data)
        거부결과=subprocess.run(['python3',str(prosiect_gwraidd/'Offer/Gweithredu_ffeil.py'),'--linux',str(LLWYBR)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Enw,거부결과.stdout)
    dilysu_adrodd = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((prosiect_gwraidd/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (mesur_data/'report.json').write_text(json.dumps(dilysu_adrodd, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Gweithredu_2()
