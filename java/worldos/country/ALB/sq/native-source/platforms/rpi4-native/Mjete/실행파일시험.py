#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from zbatoj_komandë import Project_rrënjë


def 리눅스예제(llogaritje_të_dhëna):
    llogaritje_të_dhëna.mkdir(parents=True, exist_ok=True)
    for 원본자료, Emër in [('Ekzekuto.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Project_rrënjë/'예제/리눅스ABI'/원본자료), '-o', str(llogaritje_të_dhëna/Emër)])
    실행가능파일 = llogaritje_të_dhëna/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(llogaritje_të_dhëna/'start.o'), str(llogaritje_të_dhëna/'hello.o')])
    Përmbajtje_VALUE = 실행가능파일.read_bytes()
    assert len(Përmbajtje_VALUE) <= 16384 and Përmbajtje_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Përmbajtje_VALUE, 16) == (2, 183) and b'JKOROS\0' not in Përmbajtje_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Krahasim_vijëbazë = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(llogaritje_të_dhëna)).decode()
    assert Krahasim_vijëbazë == 예상결과, Krahasim_vijëbazë
    (llogaritje_të_dhëna/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Ekzekuto():
    llogaritje_të_dhëna = Project_rrënjë/'build/verification/elf'
    llogaritje_të_dhëna.mkdir(parents=True, exist_ok=True)
    (llogaritje_të_dhëna/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(llogaritje_të_dhëna)
    llogaritje = subprocess.check_output(['python3', str(Project_rrënjë/'Mjete/zbatoj_skedar.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in llogaritje, llogaritje
    (llogaritje_të_dhëna/'serial.log').write_text(llogaritje)
    원본=실행가능파일.read_bytes()
    program_Kreu_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Emër,OFFSET_VALUE,format_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',program_Kreu_OFFSET+4,'I',7),('kernel-address',program_Kreu_OFFSET+16,'Q',0x400000)]:
        i_pavlefshëm_të_dhëna=bytearray(원본);struct.pack_into('<'+format_b87fd068,i_pavlefshëm_të_dhëna,OFFSET_VALUE,VALUE)
        POZICIONI=llogaritje_të_dhëna/Emër;POZICIONI.write_bytes(i_pavlefshëm_të_dhëna)
        거부결과=subprocess.run(['python3',str(Project_rrënjë/'Mjete/zbatoj_skedar.py'),'--linux',str(POZICIONI)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Emër,거부결과.stdout)
    miratim_raport = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (llogaritje_të_dhëna/'report.json').write_text(json.dumps(miratim_raport, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Ekzekuto()
