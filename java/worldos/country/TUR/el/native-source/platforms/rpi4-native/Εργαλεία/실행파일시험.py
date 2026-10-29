#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from εκτελώ_εντολή import έργο_ρίζα


def 리눅스예제(μέτρηση_δεδομένα):
    μέτρηση_δεδομένα.mkdir(parents=True, exist_ok=True)
    for 원본자료, Όνομα in [('Εκτέλεση_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(έργο_ρίζα/'예제/리눅스ABI'/원본자료), '-o', str(μέτρηση_δεδομένα/Όνομα)])
    εκτελέσιμο_εικόνα = μέτρηση_δεδομένα/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(εκτελέσιμο_εικόνα), str(μέτρηση_δεδομένα/'start.o'), str(μέτρηση_δεδομένα/'hello.o')])
    Περιεχόμενο_τιμή = εκτελέσιμο_εικόνα.read_bytes()
    assert len(Περιεχόμενο_τιμή) <= 16384 and Περιεχόμενο_τιμή[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Περιεχόμενο_τιμή, 16) == (2, 183) and b'JKOROS\0' not in Περιεχόμενο_τιμή
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Σύγκριση_γραμμή_βάσης = subprocess.check_output(['qemu-aarch64', str(εκτελέσιμο_εικόνα), '한글인수'], cwd=str(μέτρηση_δεδομένα)).decode()
    assert Σύγκριση_γραμμή_βάσης == 예상결과, Σύγκριση_γραμμή_βάσης
    (μέτρηση_δεδομένα/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(εκτελέσιμο_εικόνα)]))
    return εκτελέσιμο_εικόνα, 예상결과


def Εκτέλεση_2():
    μέτρηση_δεδομένα = έργο_ρίζα/'build/verification/elf'
    μέτρηση_δεδομένα.mkdir(parents=True, exist_ok=True)
    (μέτρηση_δεδομένα/'report.json').write_text('{"passed": false}\n')
    εκτελέσιμο_εικόνα, 예상결과 = 리눅스예제(μέτρηση_δεδομένα)
    μέτρηση = subprocess.check_output(['python3', str(έργο_ρίζα/'Εργαλεία/εκτελώ_Αρχείο.py'), '--linux', str(εκτελέσιμο_εικόνα), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in μέτρηση, μέτρηση
    (μέτρηση_δεδομένα/'serial.log').write_text(μέτρηση)
    원본=εκτελέσιμο_εικόνα.read_bytes()
    εφαρμογή_κεφαλίδα_Υπέρθεση=struct.unpack_from('<Q',원본,32)[0]
    for Όνομα,Υπέρθεση_τιμή,μορφή_b87fd068,τιμή in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',εφαρμογή_κεφαλίδα_Υπέρθεση+4,'I',7),('kernel-address',εφαρμογή_κεφαλίδα_Υπέρθεση+16,'Q',0x400000)]:
        άκυρος_δεδομένα=bytearray(원본);struct.pack_into('<'+μορφή_b87fd068,άκυρος_δεδομένα,Υπέρθεση_τιμή,τιμή)
        ΔΙΑΔΡΟΜΗ=μέτρηση_δεδομένα/Όνομα;ΔΙΑΔΡΟΜΗ.write_bytes(άκυρος_δεδομένα)
        거부결과=subprocess.run(['python3',str(έργο_ρίζα/'Εργαλεία/εκτελώ_Αρχείο.py'),'--linux',str(ΔΙΑΔΡΟΜΗ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Όνομα,거부결과.stdout)
    επικύρωση_έκθεση = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(εκτελέσιμο_εικόνα.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (μέτρηση_δεδομένα/'report.json').write_text(json.dumps(επικύρωση_έκθεση, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Εκτέλεση_2()
