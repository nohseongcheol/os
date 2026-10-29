#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍


def 리눅스예제(ମାପ_ଡାଟା):
    ମାପ_ଡାଟା.mkdir(parents=True, exist_ok=True)
    for 원본자료, ନାମ in [('ଚଳାନ୍ତୁ.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'예제/리눅스ABI'/원본자료), '-o', str(ମାପ_ଡାଟା/ନାମ)])
    실행가능파일 = ମାପ_ଡାଟା/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(ମାପ_ଡାଟା/'start.o'), str(ମାପ_ଡାଟା/'hello.o')])
    ବିଷୟ_ମୂଲ୍ୟ = 실행가능파일.read_bytes()
    assert len(ବିଷୟ_ମୂଲ୍ୟ) <= 16384 and ବିଷୟ_ମୂଲ୍ୟ[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', ବିଷୟ_ମୂଲ୍ୟ, 16) == (2, 183) and b'JKOROS\0' not in ବିଷୟ_ମୂଲ୍ୟ
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(ମାପ_ଡାଟା)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (ମାପ_ଡାଟା/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def ଚଳାନ୍ତୁ():
    ମାପ_ଡାଟା = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/elf'
    ମାପ_ଡାଟା.mkdir(parents=True, exist_ok=True)
    (ମାପ_ଡାଟା/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(ମାପ_ଡାଟା)
    ମାପ = subprocess.check_output(['python3', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ଫାଇଲ୍.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ମାପ, ମାପ
    (ମାପ_ଡାଟା/'serial.log').write_text(ମାପ)
    원본=실행가능파일.read_bytes()
    ଅନୁପ୍ରୟୋଗ_ଶୀର୍ଷକ_ଅଫ୍_ସେଟ୍=struct.unpack_from('<Q',원본,32)[0]
    for ନାମ,ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ,ଫର୍ମାଟ୍_b87fd068,ମୂଲ୍ୟ in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ଅନୁପ୍ରୟୋଗ_ଶୀର୍ଷକ_ଅଫ୍_ସେଟ୍+4,'I',7),('kernel-address',ଅନୁପ୍ରୟୋଗ_ଶୀର୍ଷକ_ଅଫ୍_ସେଟ୍+16,'Q',0x400000)]:
        ଅବୈଧ_ଡାଟା=bytearray(원본);struct.pack_into('<'+ଫର୍ମାଟ୍_b87fd068,ଅବୈଧ_ଡାଟା,ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ,ମୂଲ୍ୟ)
        ପଥ=ମାପ_ଡାଟା/ନାମ;ପଥ.write_bytes(ଅବୈଧ_ଡାଟା)
        거부결과=subprocess.run(['python3',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ଫାଇଲ୍.py'),'--linux',str(ପଥ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(ନାମ,거부결과.stdout)
    ବୈଧକରଣ_ରିପୋର୍ଟ = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ମାପ_ଡାଟା/'report.json').write_text(json.dumps(ବୈଧକରଣ_ରିପୋର୍ଟ, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': ଚଳାନ୍ତୁ()
