#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from exekutatu_komando import Project_erro


def 리눅스예제(neurria_datuak):
    neurria_datuak.mkdir(parents=True, exist_ok=True)
    for 원본자료, Izena in [('Exekutatu_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Project_erro/'예제/리눅스ABI'/원본자료), '-o', str(neurria_datuak/Izena)])
    실행가능파일 = neurria_datuak/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(neurria_datuak/'start.o'), str(neurria_datuak/'hello.o')])
    eduki_balio = 실행가능파일.read_bytes()
    assert len(eduki_balio) <= 16384 and eduki_balio[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', eduki_balio, 16) == (2, 183) and b'JKOROS\0' not in eduki_balio
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Konparazioa_oinarri = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(neurria_datuak)).decode()
    assert Konparazioa_oinarri == 예상결과, Konparazioa_oinarri
    (neurria_datuak/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Exekutatu_2():
    neurria_datuak = Project_erro/'build/verification/elf'
    neurria_datuak.mkdir(parents=True, exist_ok=True)
    (neurria_datuak/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(neurria_datuak)
    EMAITZA = subprocess.check_output(['python3', str(Project_erro/'Tresnak/exekutatu_fitxategi.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in EMAITZA, EMAITZA
    (neurria_datuak/'serial.log').write_text(EMAITZA)
    원본=실행가능파일.read_bytes()
    aplik_goiburu_Geruzak=struct.unpack_from('<Q',원본,32)[0]
    for Izena,Geruzak_balio,formatu_b87fd068,balio in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',aplik_goiburu_Geruzak+4,'I',7),('kernel-address',aplik_goiburu_Geruzak+16,'Q',0x400000)]:
        baliogabe_datuak=bytearray(원본);struct.pack_into('<'+formatu_b87fd068,baliogabe_datuak,Geruzak_balio,balio)
        Bide_izena=neurria_datuak/Izena;Bide_izena.write_bytes(baliogabe_datuak)
        거부결과=subprocess.run(['python3',str(Project_erro/'Tresnak/exekutatu_fitxategi.py'),'--linux',str(Bide_izena)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Izena,거부결과.stdout)
    balidazio_txosten = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (neurria_datuak/'report.json').write_text(json.dumps(balidazio_txosten, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Exekutatu_2()
