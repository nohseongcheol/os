#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट


def 리눅스예제(मेजप_डेटा):
    मेजप_डेटा.mkdir(parents=True, exist_ok=True)
    for 원본자료, नांव in [('चलोवप.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(प्रॉजॅक्ट_रूट/'예제/리눅스ABI'/원본자료), '-o', str(मेजप_डेटा/नांव)])
    실행가능파일 = मेजप_डेटा/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(मेजप_डेटा/'start.o'), str(मेजप_डेटा/'hello.o')])
    अनुक्रमणिका_मोल = 실행가능파일.read_bytes()
    assert len(अनुक्रमणिका_मोल) <= 16384 and अनुक्रमणिका_मोल[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', अनुक्रमणिका_मोल, 16) == (2, 183) and b'JKOROS\0' not in अनुक्रमणिका_मोल
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(मेजप_डेटा)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (मेजप_डेटा/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def चलोवप():
    मेजप_डेटा = प्रॉजॅक्ट_रूट/'build/verification/elf'
    मेजप_डेटा.mkdir(parents=True, exist_ok=True)
    (मेजप_डेटा/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(मेजप_डेटा)
    मेजप = subprocess.check_output(['python3', str(प्रॉजॅक्ट_रूट/'साधनां/पाळो_दिवचो_फायल.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in मेजप, मेजप
    (मेजप_डेटा/'serial.log').write_text(मेजप)
    원본=실행가능파일.read_bytes()
    एप्लिकेशन_माथाळो_ऑफसॅट=struct.unpack_from('<Q',원본,32)[0]
    for नांव,ऑफसॅट_मोल,स्वरूप_b87fd068,मोल in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',एप्लिकेशन_माथाळो_ऑफसॅट+4,'I',7),('kernel-address',एप्लिकेशन_माथाळो_ऑफसॅट+16,'Q',0x400000)]:
        अवैध_डेटा=bytearray(원본);struct.pack_into('<'+स्वरूप_b87fd068,अवैध_डेटा,ऑफसॅट_मोल,मोल)
        पाथ=मेजप_डेटा/नांव;पाथ.write_bytes(अवैध_डेटा)
        거부결과=subprocess.run(['python3',str(प्रॉजॅक्ट_रूट/'साधनां/पाळो_दिवचो_फायल.py'),'--linux',str(पाथ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(नांव,거부결과.stdout)
    वैधताय_अहवाल = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (मेजप_डेटा/'report.json').write_text(json.dumps(वैधताय_अहवाल, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': चलोवप()
