#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from végrehajt_parancs import teendő_gyök


def 리눅스예제(KR_adat):
    KR_adat.mkdir(parents=True, exist_ok=True)
    for 원본자료, Név in [('Futtatás.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(teendő_gyök/'예제/리눅스ABI'/원본자료), '-o', str(KR_adat/Név)])
    végrehajtható_KÉP = KR_adat/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(végrehajtható_KÉP), str(KR_adat/'start.o'), str(KR_adat/'hello.o')])
    Tartalom_ÉRTÉK = végrehajtható_KÉP.read_bytes()
    assert len(Tartalom_ÉRTÉK) <= 16384 and Tartalom_ÉRTÉK[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Tartalom_ÉRTÉK, 16) == (2, 183) and b'JKOROS\0' not in Tartalom_ÉRTÉK
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Összehasonlítás_alap = subprocess.check_output(['qemu-aarch64', str(végrehajtható_KÉP), '한글인수'], cwd=str(KR_adat)).decode()
    assert Összehasonlítás_alap == 예상결과, Összehasonlítás_alap
    (KR_adat/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(végrehajtható_KÉP)]))
    return végrehajtható_KÉP, 예상결과


def Futtatás():
    KR_adat = teendő_gyök/'build/verification/elf'
    KR_adat.mkdir(parents=True, exist_ok=True)
    (KR_adat/'report.json').write_text('{"passed": false}\n')
    végrehajtható_KÉP, 예상결과 = 리눅스예제(KR_adat)
    KR = subprocess.check_output(['python3', str(teendő_gyök/'Eszközök/végrehajt_Fájl.py'), '--linux', str(végrehajtható_KÉP), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in KR, KR
    (KR_adat/'serial.log').write_text(KR)
    원본=végrehajtható_KÉP.read_bytes()
    app_fejléc_Ofszet=struct.unpack_from('<Q',원본,32)[0]
    for Név,Ofszet_ÉRTÉK,formáz_b87fd068,ÉRTÉK in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',app_fejléc_Ofszet+4,'I',7),('kernel-address',app_fejléc_Ofszet+16,'Q',0x400000)]:
        alaptalan_adat=bytearray(원본);struct.pack_into('<'+formáz_b87fd068,alaptalan_adat,Ofszet_ÉRTÉK,ÉRTÉK)
        ÚTVONAL=KR_adat/Név;ÚTVONAL.write_bytes(alaptalan_adat)
        거부결과=subprocess.run(['python3',str(teendő_gyök/'Eszközök/végrehajt_Fájl.py'),'--linux',str(ÚTVONAL)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Név,거부결과.stdout)
    ellenőrzés_jelent = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(végrehajtható_KÉP.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_adat/'report.json').write_text(json.dumps(ellenőrzés_jelent, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Futtatás()
