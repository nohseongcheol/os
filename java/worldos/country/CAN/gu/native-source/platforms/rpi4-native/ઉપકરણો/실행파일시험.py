#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ


def 리눅스예제(પરિમાણ_ડેટા):
    પરિમાણ_ડેટા.mkdir(parents=True, exist_ok=True)
    for 원본자료, નામ in [('ચલાવો_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(પ્રોજેક્ટ_રૂટ/'예제/리눅스ABI'/원본자료), '-o', str(પરિમાણ_ડેટા/નામ)])
    실행가능파일 = પરિમાણ_ડેટા/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(પરિમાણ_ડેટા/'start.o'), str(પરિમાણ_ડેટા/'hello.o')])
    સામગ્રી_મૂલ્ય = 실행가능파일.read_bytes()
    assert len(સામગ્રી_મૂલ્ય) <= 16384 and સામગ્રી_મૂલ્ય[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', સામગ્રી_મૂલ્ય, 16) == (2, 183) and b'JKOROS\0' not in સામગ્રી_મૂલ્ય
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(પરિમાણ_ડેટા)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (પરિમાણ_ડેટા/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def ચલાવો_2():
    પરિમાણ_ડેટા = પ્રોજેક્ટ_રૂટ/'build/verification/elf'
    પરિમાણ_ડેટા.mkdir(parents=True, exist_ok=True)
    (પરિમાણ_ડેટા/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(પરિમાણ_ડેટા)
    પરિમાણ = subprocess.check_output(['python3', str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/અમલ_કરો_ફાઇલ.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in પરિમાણ, પરિમાણ
    (પરિમાણ_ડેટા/'serial.log').write_text(પરિમાણ)
    원본=실행가능파일.read_bytes()
    એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ=struct.unpack_from('<Q',원본,32)[0]
    for નામ,ઑફસેટ_મૂલ્ય,સ્વરૂપ_b87fd068,મૂલ્ય in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ+4,'I',7),('kernel-address',એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ+16,'Q',0x400000)]:
        અમાન્ય_ડેટા=bytearray(원본);struct.pack_into('<'+સ્વરૂપ_b87fd068,અમાન્ય_ડેટા,ઑફસેટ_મૂલ્ય,મૂલ્ય)
        પથ=પરિમાણ_ડેટા/નામ;પથ.write_bytes(અમાન્ય_ડેટા)
        거부결과=subprocess.run(['python3',str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/અમલ_કરો_ફાઇલ.py'),'--linux',str(પથ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(નામ,거부결과.stdout)
    માન્યતા_અહેવાલ = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (પરિમાણ_ડેટા/'report.json').write_text(json.dumps(માન્યતા_અહેવાલ, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': ચલાવો_2()
