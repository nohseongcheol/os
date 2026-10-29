#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from uitvoer_bevel import Project_wortel


def 리눅스예제(maatreël_data):
    maatreël_data.mkdir(parents=True, exist_ok=True)
    for 원본자료, Naam in [('Loop.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Project_wortel/'예제/리눅스ABI'/원본자료), '-o', str(maatreël_data/Naam)])
    실행가능파일 = maatreël_data/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(maatreël_data/'start.o'), str(maatreël_data/'hello.o')])
    Inhoud_VALUE = 실행가능파일.read_bytes()
    assert len(Inhoud_VALUE) <= 16384 and Inhoud_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Inhoud_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Inhoud_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Vergelyking_basislyn = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(maatreël_data)).decode()
    assert Vergelyking_basislyn == 예상결과, Vergelyking_basislyn
    (maatreël_data/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Loop():
    maatreël_data = Project_wortel/'build/verification/elf'
    maatreël_data.mkdir(parents=True, exist_ok=True)
    (maatreël_data/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(maatreël_data)
    maatreël = subprocess.check_output(['python3', str(Project_wortel/'Nutsmiddels/uitvoer_lêer.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in maatreël, maatreël
    (maatreël_data/'serial.log').write_text(maatreël)
    원본=실행가능파일.read_bytes()
    program_Loopkop_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Naam,OFFSET_VALUE,formaat_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',program_Loopkop_OFFSET+4,'I',7),('kernel-address',program_Loopkop_OFFSET+16,'Q',0x400000)]:
        ongeldig_data=bytearray(원본);struct.pack_into('<'+formaat_b87fd068,ongeldig_data,OFFSET_VALUE,VALUE)
        Pad=maatreël_data/Naam;Pad.write_bytes(ongeldig_data)
        거부결과=subprocess.run(['python3',str(Project_wortel/'Nutsmiddels/uitvoer_lêer.py'),'--linux',str(Pad)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Naam,거부결과.stdout)
    validering_verslag = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (maatreël_data/'report.json').write_text(json.dumps(validering_verslag, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Loop()
