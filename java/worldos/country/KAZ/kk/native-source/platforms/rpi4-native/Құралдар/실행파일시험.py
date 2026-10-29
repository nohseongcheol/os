#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from орындау_пәрмен import жоба_түбір


def 리눅스예제(өлшем_деректер):
    өлшем_деректер.mkdir(parents=True, exist_ok=True)
    for 원본자료, Аты in [('Орындау_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(жоба_түбір/'예제/리눅스ABI'/원본자료), '-o', str(өлшем_деректер/Аты)])
    실행가능파일 = өлшем_деректер/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(өлшем_деректер/'start.o'), str(өлшем_деректер/'hello.o')])
    мазмұн_мән = 실행가능파일.read_bytes()
    assert len(мазмұн_мән) <= 16384 and мазмұн_мән[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', мазмұн_мән, 16) == (2, 183) and b'JKOROS\0' not in мазмұн_мән
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Салыстыру_негізгі_жоспар = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(өлшем_деректер)).decode()
    assert Салыстыру_негізгі_жоспар == 예상결과, Салыстыру_негізгі_жоспар
    (өлшем_деректер/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Орындау_2():
    өлшем_деректер = жоба_түбір/'build/verification/elf'
    өлшем_деректер.mkdir(parents=True, exist_ok=True)
    (өлшем_деректер/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(өлшем_деректер)
    НӘТИЖЕ = subprocess.check_output(['python3', str(жоба_түбір/'Құралдар/орындау_файл.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in НӘТИЖЕ, НӘТИЖЕ
    (өлшем_деректер/'serial.log').write_text(НӘТИЖЕ)
    원본=실행가능파일.read_bytes()
    бағдарлама_Тақырып_жылжыту=struct.unpack_from('<Q',원본,32)[0]
    for Аты,жылжыту_мән_450fc799,пішім_b87fd068,мән in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',бағдарлама_Тақырып_жылжыту+4,'I',7),('kernel-address',бағдарлама_Тақырып_жылжыту+16,'Q',0x400000)]:
        дұрыс_емес_деректер=bytearray(원본);struct.pack_into('<'+пішім_b87fd068,дұрыс_емес_деректер,жылжыту_мән_450fc799,мән)
        Жол_2=өлшем_деректер/Аты;Жол_2.write_bytes(дұрыс_емес_деректер)
        거부결과=subprocess.run(['python3',str(жоба_түбір/'Құралдар/орындау_файл.py'),'--linux',str(Жол_2)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Аты,거부결과.stdout)
    тексерім_есеп = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (өлшем_деректер/'report.json').write_text(json.dumps(тексерім_есеп, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Орындау_2()
