#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Esegui_comando import azione_radice


def 리눅스예제(KR_dati):
    KR_dati.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nome in [('avvia.S', 'start.o'), ('messaggio_di_saluto_ae353e94.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(azione_radice/'예제/리눅스ABI'/원본자료), '-o', str(KR_dati/Nome)])
    eseguibile_foto = KR_dati/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(eseguibile_foto), str(KR_dati/'start.o'), str(KR_dati/'hello.o')])
    Contenuto_VALORE = eseguibile_foto.read_bytes()
    assert len(Contenuto_VALORE) <= 16384 and Contenuto_VALORE[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Contenuto_VALORE, 16) == (2, 183) and b'JKOROS\0' not in Contenuto_VALORE
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Confronto_di_base = subprocess.check_output(['qemu-aarch64', str(eseguibile_foto), '한글인수'], cwd=str(KR_dati)).decode()
    assert Confronto_di_base == 예상결과, Confronto_di_base
    (KR_dati/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(eseguibile_foto)]))
    return eseguibile_foto, 예상결과


def avvia():
    KR_dati = azione_radice/'build/verification/elf'
    KR_dati.mkdir(parents=True, exist_ok=True)
    (KR_dati/'report.json').write_text('{"passed": false}\n')
    eseguibile_foto, 예상결과 = 리눅스예제(KR_dati)
    risultato = subprocess.check_output(['python3', str(azione_radice/'strumenti/Esegui_File.py'), '--linux', str(eseguibile_foto), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in risultato, risultato
    (KR_dati/'serial.log').write_text(risultato)
    원본=eseguibile_foto.read_bytes()
    app_Intestazione_SCARTO=struct.unpack_from('<Q',원본,32)[0]
    for Nome,SCARTO_VALORE,formato_b87fd068,VALORE in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',app_Intestazione_SCARTO+4,'I',7),('kernel-address',app_Intestazione_SCARTO+16,'Q',0x400000)]:
        non_valida_dati=bytearray(원본);struct.pack_into('<'+formato_b87fd068,non_valida_dati,SCARTO_VALORE,VALORE)
        percorso=KR_dati/Nome;percorso.write_bytes(non_valida_dati)
        거부결과=subprocess.run(['python3',str(azione_radice/'strumenti/Esegui_File.py'),'--linux',str(percorso)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nome,거부결과.stdout)
    convalida_Report = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(eseguibile_foto.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (KR_dati/'report.json').write_text(json.dumps(convalida_Report, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': avvia()
