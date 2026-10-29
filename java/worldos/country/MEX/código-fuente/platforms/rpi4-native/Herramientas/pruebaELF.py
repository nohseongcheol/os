#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from ejecutarComando import raízProyecto


def ejemploLinux(datosResultado):
    datosResultado.mkdir(parents=True, exist_ok=True)
    for datosOriginal, nombre in [('ponerEnMarcha.S', 'start.o'), ('Saludo.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(raízProyecto/'Ejemplos/ABILinux'/datosOriginal), '-o', str(datosResultado/nombre)])
    imagenCódigoEjecutable = datosResultado/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(imagenCódigoEjecutable), str(datosResultado/'start.o'), str(datosResultado/'hello.o')])
    valorContenidoValor = imagenCódigoEjecutable.read_bytes()
    assert len(valorContenidoValor) <= 16384 and valorContenidoValor[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', valorContenidoValor, 16) == (2, 183) and b'JKOROS\0' not in valorContenidoValor
    esperado = 'LINUX ARM64 ELF PASS\n한글인수\n'
    líneaReferenciaComparación = subprocess.check_output(['qemu-aarch64', str(imagenCódigoEjecutable), '한글인수'], cwd=str(datosResultado)).decode()
    assert líneaReferenciaComparación == esperado, líneaReferenciaComparación
    (datosResultado/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(imagenCódigoEjecutable)]))
    return imagenCódigoEjecutable, esperado


def ponerEnMarcha():
    datosResultado = raízProyecto/'build/verification/elf'
    datosResultado.mkdir(parents=True, exist_ok=True)
    (datosResultado/'report.json').write_text('{"passed": false}\n')
    imagenCódigoEjecutable, esperado = ejemploLinux(datosResultado)
    resultado = subprocess.check_output(['python3', str(raízProyecto/'Herramientas/ejecutarArchivo.py'), '--linux', str(imagenCódigoEjecutable), '한글인수']).decode().replace('\r\n', '\n')
    assert esperado+'exit 0' in resultado, resultado
    (datosResultado/'serial.log').write_text(resultado)
    original=imagenCódigoEjecutable.read_bytes()
    desfaseEncabezadoPrograma=struct.unpack_from('<Q',original,32)[0]
    for nombre,valorDesfase,especificarFormato,valor in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',desfaseEncabezadoPrograma+4,'I',7),('kernel-address',desfaseEncabezadoPrograma+16,'Q',0x400000)]:
        datosInválido=bytearray(original);struct.pack_into('<'+especificarFormato,datosInválido,valorDesfase,valor)
        ruta=datosResultado/nombre;ruta.write_bytes(datosInválido)
        resultadoRechazo=subprocess.run(['python3',str(raízProyecto/'Herramientas/ejecutarArchivo.py'),'--linux',str(ruta)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert resultadoRechazo.returncode==1 and b'exit -8' in resultadoRechazo.stdout,(nombre,resultadoRechazo.stdout)
    informeValidación = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(imagenCódigoEjecutable.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (datosResultado/'report.json').write_text(json.dumps(informeValidación, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': ponerEnMarcha()
