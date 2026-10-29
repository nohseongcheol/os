#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం


def 리눅스예제(ప్రమాణం_డేటా):
    ప్రమాణం_డేటా.mkdir(parents=True, exist_ok=True)
    for 원본자료, పేరు in [('నడుపుము.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(ప్రొజెక్ట్_మూలం/'예제/리눅스ABI'/원본자료), '-o', str(ప్రమాణం_డేటా/పేరు)])
    실행가능파일 = ప్రమాణం_డేటా/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(ప్రమాణం_డేటా/'start.o'), str(ప్రమాణం_డేటా/'hello.o')])
    విషయం_మూల్యం = 실행가능파일.read_bytes()
    assert len(విషయం_మూల్యం) <= 16384 and విషయం_మూల్యం[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', విషయం_మూల్యం, 16) == (2, 183) and b'JKOROS\0' not in విషయం_మూల్యం
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    పోలిక_ఆధారరేఖ = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(ప్రమాణం_డేటా)).decode()
    assert పోలిక_ఆధారరేఖ == 예상결과, పోలిక_ఆధారరేఖ
    (ప్రమాణం_డేటా/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def నడుపుము():
    ప్రమాణం_డేటా = ప్రొజెక్ట్_మూలం/'build/verification/elf'
    ప్రమాణం_డేటా.mkdir(parents=True, exist_ok=True)
    (ప్రమాణం_డేటా/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(ప్రమాణం_డేటా)
    ప్రమాణం = subprocess.check_output(['python3', str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/అమలు_చేయి_ఫైలు.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ప్రమాణం, ప్రమాణం
    (ప్రమాణం_డేటా/'serial.log').write_text(ప్రమాణం)
    원본=실행가능파일.read_bytes()
    అనువర్తనం_శీర్షిక_ఆఫ్_సెట్=struct.unpack_from('<Q',원본,32)[0]
    for పేరు,ఆఫ్_సెట్_మూల్యం,ఆకృతి_b87fd068,మూల్యం in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',అనువర్తనం_శీర్షిక_ఆఫ్_సెట్+4,'I',7),('kernel-address',అనువర్తనం_శీర్షిక_ఆఫ్_సెట్+16,'Q',0x400000)]:
        చెల్లని_డేటా=bytearray(원본);struct.pack_into('<'+ఆకృతి_b87fd068,చెల్లని_డేటా,ఆఫ్_సెట్_మూల్యం,మూల్యం)
        పాత్=ప్రమాణం_డేటా/పేరు;పాత్.write_bytes(చెల్లని_డేటా)
        거부결과=subprocess.run(['python3',str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/అమలు_చేయి_ఫైలు.py'),'--linux',str(పాత్)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(పేరు,거부결과.stdout)
    నిర్ధారణ_నివేదిక = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ప్రమాణం_డేటా/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': నడుపుము()
