#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from köra_kommando import åtgärd_rot


def 리눅스예제(KR_data):
    KR_data.mkdir(parents=True, exist_ok=True)
    for 원본자료, Namn in [('Kör.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(åtgärd_rot/'예제/리눅스ABI'/원본자료), '-o', str(KR_data/Namn)])
    körbar_fil_BILD = KR_data/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(körbar_fil_BILD), str(KR_data/'start.o'), str(KR_data/'hello.o')])
    Innehåll_värde = körbar_fil_BILD.read_bytes()
    assert len(Innehåll_värde) <= 16384 and Innehåll_värde[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Innehåll_värde, 16) == (2, 183) and b'JKOROS\0' not in Innehåll_värde
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Jämförelse_baslinje = subprocess.check_output(['qemu-aarch64', str(körbar_fil_BILD), '한글인수'], cwd=str(KR_data)).decode()
    assert Jämförelse_baslinje == 예상결과, Jämförelse_baslinje
    (KR_data/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(körbar_fil_BILD)]))
    return körbar_fil_BILD, 예상결과


def Kör():
    KR_data = åtgärd_rot/'build/verification/elf'
    KR_data.mkdir(parents=True, exist_ok=True)
    (KR_data/'report.json').write_text('{"passed": false}\n')
    körbar_fil_BILD, 예상결과 = 리눅스예제(KR_data)
    RESULTAT = subprocess.check_output(['python3', str(åtgärd_rot/'verktyg/köra_fil.py'), '--linux', str(körbar_fil_BILD), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in RESULTAT, RESULTAT
    (KR_data/'serial.log').write_text(RESULTAT)
    원본=körbar_fil_BILD.read_bytes()
    app_huvud_FÖRSKJUTNING=struct.unpack_from('<Q',원본,32)[0]
    for Namn,FÖRSKJUTNING_värde,format_b87fd068,värde in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',app_huvud_FÖRSKJUTNING+4,'I',7),('kernel-address',app_huvud_FÖRSKJUTNING+16,'Q',0x400000)]:
        ogiltig_data=bytearray(원본);struct.pack_into('<'+format_b87fd068,ogiltig_data,FÖRSKJUTNING_värde,värde)
        sökväg_2=KR_data/Namn;sökväg_2.write_bytes(ogiltig_data)
        거부결과=subprocess.run(['python3',str(åtgärd_rot/'verktyg/köra_fil.py'),'--linux',str(sökväg_2)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Namn,거부결과.stdout)
    validering_Rapport = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(körbar_fil_BILD.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_data/'report.json').write_text(json.dumps(validering_Rapport, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Kör()
