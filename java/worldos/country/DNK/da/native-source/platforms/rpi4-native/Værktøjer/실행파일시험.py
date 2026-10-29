#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Udfør_kommando import To_do_rod


def 리눅스예제(KR_data):
    KR_data.mkdir(parents=True, exist_ok=True)
    for 원본자료, Navn in [('Kør_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(To_do_rod/'예제/리눅스ABI'/원본자료), '-o', str(KR_data/Navn)])
    eksekverbar_fil_Image = KR_data/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(eksekverbar_fil_Image), str(KR_data/'start.o'), str(KR_data/'hello.o')])
    Indhold_VÆRDI = eksekverbar_fil_Image.read_bytes()
    assert len(Indhold_VÆRDI) <= 16384 and Indhold_VÆRDI[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Indhold_VÆRDI, 16) == (2, 183) and b'JKOROS\0' not in Indhold_VÆRDI
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Sammenligning_baseline = subprocess.check_output(['qemu-aarch64', str(eksekverbar_fil_Image), '한글인수'], cwd=str(KR_data)).decode()
    assert Sammenligning_baseline == 예상결과, Sammenligning_baseline
    (KR_data/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(eksekverbar_fil_Image)]))
    return eksekverbar_fil_Image, 예상결과


def Kør_2():
    KR_data = To_do_rod/'build/verification/elf'
    KR_data.mkdir(parents=True, exist_ok=True)
    (KR_data/'report.json').write_text('{"passed": false}\n')
    eksekverbar_fil_Image, 예상결과 = 리눅스예제(KR_data)
    KR = subprocess.check_output(['python3', str(To_do_rod/'Værktøjer/Udfør_fil.py'), '--linux', str(eksekverbar_fil_Image), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in KR, KR
    (KR_data/'serial.log').write_text(KR)
    원본=eksekverbar_fil_Image.read_bytes()
    app_Header_FORSKYDNING=struct.unpack_from('<Q',원본,32)[0]
    for Navn,FORSKYDNING_VÆRDI,format_b87fd068,VÆRDI in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',app_Header_FORSKYDNING+4,'I',7),('kernel-address',app_Header_FORSKYDNING+16,'Q',0x400000)]:
        ugyldig_data=bytearray(원본);struct.pack_into('<'+format_b87fd068,ugyldig_data,FORSKYDNING_VÆRDI,VÆRDI)
        Sti=KR_data/Navn;Sti.write_bytes(ugyldig_data)
        거부결과=subprocess.run(['python3',str(To_do_rod/'Værktøjer/Udfør_fil.py'),'--linux',str(Sti)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Navn,거부결과.stdout)
    validering_rapport = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((To_do_rod/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(eksekverbar_fil_Image.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_data/'report.json').write_text(json.dumps(validering_rapport, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Kør_2()
