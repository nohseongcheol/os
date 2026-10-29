#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Executa_ordre import Project_rel


def 리눅스예제(mesura_dades):
    mesura_dades.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nom in [('Executa_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Project_rel/'예제/리눅스ABI'/원본자료), '-o', str(mesura_dades/Nom)])
    실행가능파일 = mesura_dades/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(mesura_dades/'start.o'), str(mesura_dades/'hello.o')])
    contingut_VALOR = 실행가능파일.read_bytes()
    assert len(contingut_VALOR) <= 16384 and contingut_VALOR[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', contingut_VALOR, 16) == (2, 183) and b'JKOROS\0' not in contingut_VALOR
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Comparació_referència = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(mesura_dades)).decode()
    assert Comparació_referència == 예상결과, Comparació_referència
    (mesura_dades/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Executa_2():
    mesura_dades = Project_rel/'build/verification/elf'
    mesura_dades.mkdir(parents=True, exist_ok=True)
    (mesura_dades/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(mesura_dades)
    RESULTAT = subprocess.check_output(['python3', str(Project_rel/'Eines/Executa_arxiu.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in RESULTAT, RESULTAT
    (mesura_dades/'serial.log').write_text(RESULTAT)
    원본=실행가능파일.read_bytes()
    programa_Capçalera_DESPLAÇAMENT=struct.unpack_from('<Q',원본,32)[0]
    for Nom,DESPLAÇAMENT_VALOR,format_b87fd068,VALOR in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',programa_Capçalera_DESPLAÇAMENT+4,'I',7),('kernel-address',programa_Capçalera_DESPLAÇAMENT+16,'Q',0x400000)]:
        invàlid_dades=bytearray(원본);struct.pack_into('<'+format_b87fd068,invàlid_dades,DESPLAÇAMENT_VALOR,VALOR)
        Camí=mesura_dades/Nom;Camí.write_bytes(invàlid_dades)
        거부결과=subprocess.run(['python3',str(Project_rel/'Eines/Executa_arxiu.py'),'--linux',str(Camí)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nom,거부결과.stdout)
    validació_informe = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (mesura_dades/'report.json').write_text(json.dumps(validació_informe, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Executa_2()
