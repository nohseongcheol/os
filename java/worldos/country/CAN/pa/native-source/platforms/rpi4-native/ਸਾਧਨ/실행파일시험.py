#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ


def 리눅스예제(ਮਾਪ_ਸਮੱਗਰੀ):
    ਮਾਪ_ਸਮੱਗਰੀ.mkdir(parents=True, exist_ok=True)
    for 원본자료, ਨਾਂ in [('ਚਲਾਓ_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'예제/리눅스ABI'/원본자료), '-o', str(ਮਾਪ_ਸਮੱਗਰੀ/ਨਾਂ)])
    실행가능파일 = ਮਾਪ_ਸਮੱਗਰੀ/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(ਮਾਪ_ਸਮੱਗਰੀ/'start.o'), str(ਮਾਪ_ਸਮੱਗਰੀ/'hello.o')])
    ਤਤਕਰਾ_ਕੀਮਤ = 실행가능파일.read_bytes()
    assert len(ਤਤਕਰਾ_ਕੀਮਤ) <= 16384 and ਤਤਕਰਾ_ਕੀਮਤ[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', ਤਤਕਰਾ_ਕੀਮਤ, 16) == (2, 183) and b'JKOROS\0' not in ਤਤਕਰਾ_ਕੀਮਤ
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(ਮਾਪ_ਸਮੱਗਰੀ)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (ਮਾਪ_ਸਮੱਗਰੀ/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def ਚਲਾਓ_2():
    ਮਾਪ_ਸਮੱਗਰੀ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/elf'
    ਮਾਪ_ਸਮੱਗਰੀ.mkdir(parents=True, exist_ok=True)
    (ਮਾਪ_ਸਮੱਗਰੀ/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(ਮਾਪ_ਸਮੱਗਰੀ)
    ਮਾਪ = subprocess.check_output(['python3', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ਮਾਪ, ਮਾਪ
    (ਮਾਪ_ਸਮੱਗਰੀ/'serial.log').write_text(ਮਾਪ)
    원본=실행가능파일.read_bytes()
    ਐਪਲੀਕੇਸ਼_ਸਿਰਲੇਖ_ਔਫਸੈਟ=struct.unpack_from('<Q',원본,32)[0]
    for ਨਾਂ,ਔਫਸੈਟ_ਕੀਮਤ,ਸਰੂਪ_b87fd068,ਕੀਮਤ in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ਐਪਲੀਕੇਸ਼_ਸਿਰਲੇਖ_ਔਫਸੈਟ+4,'I',7),('kernel-address',ਐਪਲੀਕੇਸ਼_ਸਿਰਲੇਖ_ਔਫਸੈਟ+16,'Q',0x400000)]:
        ਅਯੋਗ_ਸਮੱਗਰੀ=bytearray(원본);struct.pack_into('<'+ਸਰੂਪ_b87fd068,ਅਯੋਗ_ਸਮੱਗਰੀ,ਔਫਸੈਟ_ਕੀਮਤ,ਕੀਮਤ)
        ਮਾਰਗ=ਮਾਪ_ਸਮੱਗਰੀ/ਨਾਂ;ਮਾਰਗ.write_bytes(ਅਯੋਗ_ਸਮੱਗਰੀ)
        거부결과=subprocess.run(['python3',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ.py'),'--linux',str(ਮਾਰਗ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(ਨਾਂ,거부결과.stdout)
    ਮਾਨਤਾ_ਵਿਵਰਨ = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ਮਾਪ_ਸਮੱਗਰੀ/'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': ਚਲਾਓ_2()
