#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from үтәргә_команда import экранга_җибәрү_тамыр


def 리눅스예제(үлчәм_мәгълүмат):
    үлчәм_мәгълүмат.mkdir(parents=True, exist_ok=True)
    for 원본자료, исем in [('эшләтү.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(экранга_җибәрү_тамыр/'예제/리눅스ABI'/원본자료), '-o', str(үлчәм_мәгълүмат/исем)])
    실행가능파일 = үлчәм_мәгълүмат/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(үлчәм_мәгълүмат/'start.o'), str(үлчәм_мәгълүмат/'hello.o')])
    Эчтәлек_VALUE = 실행가능파일.read_bytes()
    assert len(Эчтәлек_VALUE) <= 16384 and Эчтәлек_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Эчтәлек_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Эчтәлек_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(үлчәм_мәгълүмат)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (үлчәм_мәгълүмат/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def эшләтү():
    үлчәм_мәгълүмат = экранга_җибәрү_тамыр/'build/verification/elf'
    үлчәм_мәгълүмат.mkdir(parents=True, exist_ok=True)
    (үлчәм_мәгълүмат/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(үлчәм_мәгълүмат)
    үлчәм = subprocess.check_output(['python3', str(экранга_җибәрү_тамыр/'Кораллар/үтәргә_файл.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in үлчәм, үлчәм
    (үлчәм_мәгълүмат/'serial.log').write_text(үлчәм)
    원본=실행가능파일.read_bytes()
    кушымта_Башлама_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for исем,OFFSET_VALUE,формат_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',кушымта_Башлама_OFFSET+4,'I',7),('kernel-address',кушымта_Башлама_OFFSET+16,'Q',0x400000)]:
        дөрес_булмаган_мәгълүмат=bytearray(원본);struct.pack_into('<'+формат_b87fd068,дөрес_булмаган_мәгълүмат,OFFSET_VALUE,VALUE)
        Yul=үлчәм_мәгълүмат/исем;Yul.write_bytes(дөрес_булмаган_мәгълүмат)
        거부결과=subprocess.run(['python3',str(экранга_җибәрү_тамыр/'Кораллар/үтәргә_файл.py'),'--linux',str(Yul)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(исем,거부결과.stdout)
    раслау_отчет = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (үлчәм_мәгълүмат/'report.json').write_text(json.dumps(раслау_отчет, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': эшләтү()
