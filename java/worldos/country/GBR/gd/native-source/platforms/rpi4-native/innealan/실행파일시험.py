#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from gnìomhaich_àithne import tilg_freumh


def 리눅스예제(tomhas_dàta):
    tomhas_dàta.mkdir(parents=True, exist_ok=True)
    for 원본자료, Ainm in [('ruith.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(tilg_freumh/'예제/리눅스ABI'/원본자료), '-o', str(tomhas_dàta/Ainm)])
    실행가능파일 = tomhas_dàta/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(tomhas_dàta/'start.o'), str(tomhas_dàta/'hello.o')])
    susbaint_VALUE = 실행가능파일.read_bytes()
    assert len(susbaint_VALUE) <= 16384 and susbaint_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', susbaint_VALUE, 16) == (2, 183) and b'JKOROS\0' not in susbaint_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(tomhas_dàta)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (tomhas_dàta/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def ruith():
    tomhas_dàta = tilg_freumh/'build/verification/elf'
    tomhas_dàta.mkdir(parents=True, exist_ok=True)
    (tomhas_dàta/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(tomhas_dàta)
    tomhas = subprocess.check_output(['python3', str(tilg_freumh/'innealan/gnìomhaich_faidhle.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in tomhas, tomhas
    (tomhas_dàta/'serial.log').write_text(tomhas)
    원본=실행가능파일.read_bytes()
    ap_bann_cinn_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Ainm,OFFSET_VALUE,fòrmat_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ap_bann_cinn_OFFSET+4,'I',7),('kernel-address',ap_bann_cinn_OFFSET+16,'Q',0x400000)]:
        mì_dhligheach_dàta=bytearray(원본);struct.pack_into('<'+fòrmat_b87fd068,mì_dhligheach_dàta,OFFSET_VALUE,VALUE)
        Slighe=tomhas_dàta/Ainm;Slighe.write_bytes(mì_dhligheach_dàta)
        거부결과=subprocess.run(['python3',str(tilg_freumh/'innealan/gnìomhaich_faidhle.py'),'--linux',str(Slighe)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Ainm,거부결과.stdout)
    dearbhadh_aithisg = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (tomhas_dàta/'report.json').write_text(json.dumps(dearbhadh_aithisg, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': ruith()
