#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from შესრულება_ბრძანება import პროეცირება_ფესვი


def 리눅스예제(გაზომვა_მონაცემები):
    გაზომვა_მონაცემები.mkdir(parents=True, exist_ok=True)
    for 원본자료, სახელი in [('გაშვება.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(პროეცირება_ფესვი/'예제/리눅스ABI'/원본자료), '-o', str(გაზომვა_მონაცემები/სახელი)])
    실행가능파일 = გაზომვა_მონაცემები/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(გაზომვა_მონაცემები/'start.o'), str(გაზომვა_მონაცემები/'hello.o')])
    შიგთავსი_მნიშვნელობა = 실행가능파일.read_bytes()
    assert len(შიგთავსი_მნიშვნელობა) <= 16384 and შიგთავსი_მნიშვნელობა[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', შიგთავსი_მნიშვნელობა, 16) == (2, 183) and b'JKOROS\0' not in შიგთავსი_მნიშვნელობა
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(გაზომვა_მონაცემები)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (გაზომვა_მონაცემები/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def გაშვება():
    გაზომვა_მონაცემები = პროეცირება_ფესვი/'build/verification/elf'
    გაზომვა_მონაცემები.mkdir(parents=True, exist_ok=True)
    (გაზომვა_მონაცემები/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(გაზომვა_მონაცემები)
    გაზომვა = subprocess.check_output(['python3', str(პროეცირება_ფესვი/'ხელსაწყოები/შესრულება_ფაილი.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in გაზომვა, გაზომვა
    (გაზომვა_მონაცემები/'serial.log').write_text(გაზომვა)
    원본=실행가능파일.read_bytes()
    აპი_ზედა_კოლონტიტული_ოფსეტი=struct.unpack_from('<Q',원본,32)[0]
    for სახელი,ოფსეტი_მნიშვნელობა,ფორმატი_b87fd068,მნიშვნელობა in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',აპი_ზედა_კოლონტიტული_ოფსეტი+4,'I',7),('kernel-address',აპი_ზედა_კოლონტიტული_ოფსეტი+16,'Q',0x400000)]:
        არასწორი_მონაცემები=bytearray(원본);struct.pack_into('<'+ფორმატი_b87fd068,არასწორი_მონაცემები,ოფსეტი_მნიშვნელობა,მნიშვნელობა)
        გეზი=გაზომვა_მონაცემები/სახელი;გეზი.write_bytes(არასწორი_მონაცემები)
        거부결과=subprocess.run(['python3',str(პროეცირება_ფესვი/'ხელსაწყოები/შესრულება_ფაილი.py'),'--linux',str(გეზი)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(სახელი,거부결과.stdout)
    გადამოწმება_ანგარიში = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (გაზომვა_მონაცემები/'report.json').write_text(json.dumps(გადამოწმება_ანგარიში, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': გაშვება()
