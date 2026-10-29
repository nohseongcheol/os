#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស


def 리눅스예제(ការវាស់វែង_ទិន្នន័យ):
    ការវាស់វែង_ទិន្នន័យ.mkdir(parents=True, exist_ok=True)
    for 원본자료, ឈ្មោះ in [('រត់.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(បញ្ចាំង_ឬស/'예제/리눅스ABI'/원본자료), '-o', str(ការវាស់វែង_ទិន្នន័យ/ឈ្មោះ)])
    실행가능파일 = ការវាស់វែង_ទិន្នន័យ/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(ការវាស់វែង_ទិន្នន័យ/'start.o'), str(ការវាស់វែង_ទិន្នន័យ/'hello.o')])
    មាតិកា_តំលៃ = 실행가능파일.read_bytes()
    assert len(មាតិកា_តំលៃ) <= 16384 and មាតិកា_តំលៃ[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', មាតិកា_តំលៃ, 16) == (2, 183) and b'JKOROS\0' not in មាតិកា_តំលៃ
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    ការប្រៀបធៀប_បន្ទាត់គោល = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(ការវាស់វែង_ទិន្នន័យ)).decode()
    assert ការប្រៀបធៀប_បន្ទាត់គោល == 예상결과, ការប្រៀបធៀប_បន្ទាត់គោល
    (ការវាស់វែង_ទិន្នន័យ/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def រត់():
    ការវាស់វែង_ទិន្នន័យ = បញ្ចាំង_ឬស/'build/verification/elf'
    ការវាស់វែង_ទិន្នន័យ.mkdir(parents=True, exist_ok=True)
    (ការវាស់វែង_ទិន្នន័យ/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(ការវាស់វែង_ទិន្នន័យ)
    ការវាស់វែង = subprocess.check_output(['python3', str(បញ្ចាំង_ឬស/'ឧបករណ៍/អនុវត្ត_ឯកសារ.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ការវាស់វែង, ការវាស់វែង
    (ការវាស់វែង_ទិន្នន័យ/'serial.log').write_text(ការវាស់វែង)
    원본=실행가능파일.read_bytes()
    កម្មវិធី_បឋមកថា_ការបែង_ភាគ=struct.unpack_from('<Q',원본,32)[0]
    for ឈ្មោះ,ការបែង_ភាគ_តំលៃ,ទំរង់_b87fd068,តំលៃ in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',កម្មវិធី_បឋមកថា_ការបែង_ភាគ+4,'I',7),('kernel-address',កម្មវិធី_បឋមកថា_ការបែង_ភាគ+16,'Q',0x400000)]:
        មិនត្រឹមត្រូវ_ទិន្នន័យ=bytearray(원본);struct.pack_into('<'+ទំរង់_b87fd068,មិនត្រឹមត្រូវ_ទិន្នន័យ,ការបែង_ភាគ_តំលៃ,តំលៃ)
        ផ្លូវ=ការវាស់វែង_ទិន្នន័យ/ឈ្មោះ;ផ្លូវ.write_bytes(មិនត្រឹមត្រូវ_ទិន្នន័យ)
        거부결과=subprocess.run(['python3',str(បញ្ចាំង_ឬស/'ឧបករណ៍/អនុវត្ត_ឯកសារ.py'),'--linux',str(ផ្លូវ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(ឈ្មោះ,거부결과.stdout)
    សុពលភាព_រាយការណ៍ = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((បញ្ចាំង_ឬស/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ការវាស់វែង_ទិន្នន័យ/'report.json').write_text(json.dumps(សុពលភាព_រាយការណ៍, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': រត់()
