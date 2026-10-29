#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from Executar_comando import ação_raiz


def 리눅스예제(RC_dados):
    RC_dados.mkdir(parents=True, exist_ok=True)
    for 원본자료, Nome in [('iniciar.S', 'start.o'), ('saudação_ae353e94.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(ação_raiz/'예제/리눅스ABI'/원본자료), '-o', str(RC_dados/Nome)])
    executável_foto = RC_dados/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(executável_foto), str(RC_dados/'start.o'), str(RC_dados/'hello.o')])
    Conteúdo_VALOR = executável_foto.read_bytes()
    assert len(Conteúdo_VALOR) <= 16384 and Conteúdo_VALOR[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', Conteúdo_VALOR, 16) == (2, 183) and b'JKOROS\0' not in Conteúdo_VALOR
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    Comparação_linha_de_base = subprocess.check_output(['qemu-aarch64', str(executável_foto), '한글인수'], cwd=str(RC_dados)).decode()
    assert Comparação_linha_de_base == 예상결과, Comparação_linha_de_base
    (RC_dados/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(executável_foto)]))
    return executável_foto, 예상결과


def iniciar():
    RC_dados = ação_raiz/'build/verification/elf'
    RC_dados.mkdir(parents=True, exist_ok=True)
    (RC_dados/'report.json').write_text('{"passed": false}\n')
    executável_foto, 예상결과 = 리눅스예제(RC_dados)
    resultado = subprocess.check_output(['python3', str(ação_raiz/'ferramentas/Executar_Arquivo.py'), '--linux', str(executável_foto), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in resultado, resultado
    (RC_dados/'serial.log').write_text(resultado)
    원본=executável_foto.read_bytes()
    app_Cabeçalho_DESLOC=struct.unpack_from('<Q',원본,32)[0]
    for Nome,DESLOC_VALOR,formato_b87fd068,VALOR in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',app_Cabeçalho_DESLOC+4,'I',7),('kernel-address',app_Cabeçalho_DESLOC+16,'Q',0x400000)]:
        inválido_dados=bytearray(원본);struct.pack_into('<'+formato_b87fd068,inválido_dados,DESLOC_VALOR,VALOR)
        caminho=RC_dados/Nome;caminho.write_bytes(inválido_dados)
        거부결과=subprocess.run(['python3',str(ação_raiz/'ferramentas/Executar_Arquivo.py'),'--linux',str(caminho)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(Nome,거부결과.stdout)
    validação_relatar = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(executável_foto.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (RC_dados/'report.json').write_text(json.dumps(validação_relatar, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': iniciar()
