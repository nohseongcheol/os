#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from executar_comando import Project_raíz


def 리눅스예제(medida_datos):
    medida_datos.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nome in [('Executar_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(Project_raíz/'예제/리눅스ABI'/원본자료), '-o', str(medida_datos/Nome)])
    실행가능파일 = medida_datos/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(medida_datos/'start.o'), str(medida_datos/'hello.o')])
    Contido_VALOR = 실행가능파일.read_bytes()
    assert len(Contido_VALOR) <= 16384 and Contido_VALOR[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Contido_VALOR, 16) == (2, 183) and b'JKOROS\0' not in Contido_VALOR
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Comparación_liña_base = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(medida_datos)).decode()
    assert Comparación_liña_base == 예상결과, Comparación_liña_base
    (medida_datos/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def Executar_2():
    medida_datos = Project_raíz/'build/verification/elf'
    medida_datos.mkdir(parents=True, exist_ok=True)
    (medida_datos/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(medida_datos)
    RESULTANTE = subprocess.check_output(['python3', str(Project_raíz/'Ferramentas/executar_Ficheiro.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in RESULTANTE, RESULTANTE
    (medida_datos/'serial.log').write_text(RESULTANTE)
    원본=실행가능파일.read_bytes()
    apl_Cabeceira_DESPRAZAMENTO=struct.unpack_from('<Q',원본,32)[0]
    for Nome,DESPRAZAMENTO_VALOR,formato_b87fd068,VALOR in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',apl_Cabeceira_DESPRAZAMENTO+4,'I',7),('kernel-address',apl_Cabeceira_DESPRAZAMENTO+16,'Q',0x400000)]:
        non_válido_datos=bytearray(원본);struct.pack_into('<'+formato_b87fd068,non_válido_datos,DESPRAZAMENTO_VALOR,VALOR)
        CAMIÑO=medida_datos/Nome;CAMIÑO.write_bytes(non_válido_datos)
        거부결과=subprocess.run(['python3',str(Project_raíz/'Ferramentas/executar_Ficheiro.py'),'--linux',str(CAMIÑO)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nome,거부결과.stdout)
    validación_informe = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (medida_datos/'report.json').write_text(json.dumps(validación_informe, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': Executar_2()
