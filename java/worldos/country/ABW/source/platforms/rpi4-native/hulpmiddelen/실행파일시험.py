#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Uitvoeren_opdracht import Taken_wortel


def 리눅스예제(HR_gegevens):
    HR_gegevens.mkdir(parents=True, exist_ok=True)
    for 원본자료, Naam in [('starten.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Taken_wortel/'예제/리눅스ABI'/원본자료), '-o', str(HR_gegevens/Naam)])
    uitvoerbaar_kopie = HR_gegevens/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(uitvoerbaar_kopie), str(HR_gegevens/'start.o'), str(HR_gegevens/'hello.o')])
    Inhoud_WAARDE = uitvoerbaar_kopie.read_bytes()
    assert len(Inhoud_WAARDE) <= 16384 and Inhoud_WAARDE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Inhoud_WAARDE, 16) == (2, 183) and b'JKOROS\0' not in Inhoud_WAARDE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Vergelijking_basislijn = subprocess.check_output(['qemu-aarch64', str(uitvoerbaar_kopie), '한글인수'], cwd=str(HR_gegevens)).decode()
    assert Vergelijking_basislijn == 예상결과, Vergelijking_basislijn
    (HR_gegevens/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(uitvoerbaar_kopie)]))
    return uitvoerbaar_kopie, 예상결과


def starten():
    HR_gegevens = Taken_wortel/'build/verification/elf'
    HR_gegevens.mkdir(parents=True, exist_ok=True)
    (HR_gegevens/'report.json').write_text('{"passed": false}\n')
    uitvoerbaar_kopie, 예상결과 = 리눅스예제(HR_gegevens)
    resultaat = subprocess.check_output(['python3', str(Taken_wortel/'hulpmiddelen/Uitvoeren_Bestand.py'), '--linux', str(uitvoerbaar_kopie), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in resultaat, resultaat
    (HR_gegevens/'serial.log').write_text(resultaat)
    원본=uitvoerbaar_kopie.read_bytes()
    app_header_VERSCHUIVING=struct.unpack_from('<Q',원본,32)[0]
    for Naam,VERSCHUIVING_WAARDE,opmaak_b87fd068,WAARDE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',app_header_VERSCHUIVING+4,'I',7),('kernel-address',app_header_VERSCHUIVING+16,'Q',0x400000)]:
        nietig_gegevens=bytearray(원본);struct.pack_into('<'+opmaak_b87fd068,nietig_gegevens,VERSCHUIVING_WAARDE,WAARDE)
        pad=HR_gegevens/Naam;pad.write_bytes(nietig_gegevens)
        거부결과=subprocess.run(['python3',str(Taken_wortel/'hulpmiddelen/Uitvoeren_Bestand.py'),'--linux',str(pad)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Naam,거부결과.stdout)
    validatie_Rapport = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(uitvoerbaar_kopie.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (HR_gegevens/'report.json').write_text(json.dumps(validatie_Rapport, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': starten()
