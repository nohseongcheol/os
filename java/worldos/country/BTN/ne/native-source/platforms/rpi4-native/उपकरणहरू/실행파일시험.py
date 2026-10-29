#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट


def 리눅스예제(मापन_लगत):
    मापन_लगत.mkdir(parents=True, exist_ok=True)
    for 원본자료, नाम in [('चलाउनुहोस्.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(परियोजना_रूट/'예제/리눅스ABI'/원본자료), '-o', str(मापन_लगत/नाम)])
    실행가능파일 = मापन_लगत/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(मापन_लगत/'start.o'), str(मापन_लगत/'hello.o')])
    सामग्री_मान = 실행가능파일.read_bytes()
    assert len(सामग्री_मान) <= 16384 and सामग्री_मान[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', सामग्री_मान, 16) == (2, 183) and b'JKOROS\0' not in सामग्री_मान
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    तुलना_आधाररेखा = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(मापन_लगत)).decode()
    assert तुलना_आधाररेखा == 예상결과, तुलना_आधाररेखा
    (मापन_लगत/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def चलाउनुहोस्():
    मापन_लगत = परियोजना_रूट/'build/verification/elf'
    मापन_लगत.mkdir(parents=True, exist_ok=True)
    (मापन_लगत/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(मापन_लगत)
    मापन = subprocess.check_output(['python3', str(परियोजना_रूट/'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_फाइल.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in मापन, मापन
    (मापन_लगत/'serial.log').write_text(मापन)
    원본=실행가능파일.read_bytes()
    अनुप्रयोग_हेडर_अफसेट=struct.unpack_from('<Q',원본,32)[0]
    for नाम,अफसेट_मान,ढाँचा_b87fd068,मान in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',अनुप्रयोग_हेडर_अफसेट+4,'I',7),('kernel-address',अनुप्रयोग_हेडर_अफसेट+16,'Q',0x400000)]:
        अवैधानिक_लगत=bytearray(원본);struct.pack_into('<'+ढाँचा_b87fd068,अवैधानिक_लगत,अफसेट_मान,मान)
        मार्ग=मापन_लगत/नाम;मार्ग.write_bytes(अवैधानिक_लगत)
        거부결과=subprocess.run(['python3',str(परियोजना_रूट/'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_फाइल.py'),'--linux',str(मार्ग)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(नाम,거부결과.stdout)
    वैधानिकता_रिपोर्ट = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (मापन_लगत/'report.json').write_text(json.dumps(वैधानिकता_रिपोर्ट, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': चलाउनुहोस्()
