#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from bajarmoq_buyruq import Project_ildiz


def 리눅스예제(o_lchov_ma_lumotlar):
    o_lchov_ma_lumotlar.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nomi in [('Bajarish.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Project_ildiz/'예제/리눅스ABI'/원본자료), '-o', str(o_lchov_ma_lumotlar/Nomi)])
    실행가능파일 = o_lchov_ma_lumotlar/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(o_lchov_ma_lumotlar/'start.o'), str(o_lchov_ma_lumotlar/'hello.o')])
    tarkib_VALUE = 실행가능파일.read_bytes()
    assert len(tarkib_VALUE) <= 16384 and tarkib_VALUE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', tarkib_VALUE, 16) == (2, 183) and b'JKOROS\0' not in tarkib_VALUE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Taqqoslama_bazaviy_koʻrsatkich = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(o_lchov_ma_lumotlar)).decode()
    assert Taqqoslama_bazaviy_koʻrsatkich == 예상결과, Taqqoslama_bazaviy_koʻrsatkich
    (o_lchov_ma_lumotlar/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Bajarish():
    o_lchov_ma_lumotlar = Project_ildiz/'build/verification/elf'
    o_lchov_ma_lumotlar.mkdir(parents=True, exist_ok=True)
    (o_lchov_ma_lumotlar/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(o_lchov_ma_lumotlar)
    o_lchov = subprocess.check_output(['python3', str(Project_ildiz/'Vositalar/bajarmoq_fayl.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in o_lchov, o_lchov
    (o_lchov_ma_lumotlar/'serial.log').write_text(o_lchov)
    원본=실행가능파일.read_bytes()
    ilova_Sarlavha_OFFSET=struct.unpack_from('<Q',원본,32)[0]
    for Nomi,OFFSET_VALUE,format_b87fd068,VALUE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ilova_Sarlavha_OFFSET+4,'I',7),('kernel-address',ilova_Sarlavha_OFFSET+16,'Q',0x400000)]:
        xato_ma_lumotlar=bytearray(원본);struct.pack_into('<'+format_b87fd068,xato_ma_lumotlar,OFFSET_VALUE,VALUE)
        yo_l=o_lchov_ma_lumotlar/Nomi;yo_l.write_bytes(xato_ma_lumotlar)
        거부결과=subprocess.run(['python3',str(Project_ildiz/'Vositalar/bajarmoq_fayl.py'),'--linux',str(yo_l)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nomi,거부결과.stdout)
    tasdiq_hisobot = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (o_lchov_ma_lumotlar/'report.json').write_text(json.dumps(tasdiq_hisobot, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Bajarish()
