#!/usr/bin/env python3
"""valorDistribución 묶음에서 libassh/TinyCC를 교체하고 propio 커널을 valorReintentar 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

raízProyecto = Path(__file__).resolve().parent


def ejecutarComando(textoPalabra):
    subprocess.check_call([str(valorEntradaElemento) for valorEntradaElemento in textoPalabra], cwd=str(raízProyecto))


def ponerEnMarcha():
    Analizador = argparse.ArgumentParser(description=__doc__)
    Analizador.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verificar')
    Analizador.add_argument('--libassh-archive', type=Path, help='별도로 modificarValor·컴파일한 libassh.a valorUsar')
    Analizador.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 valorReintentar 컴파일하고 커널에 탑재')
    Analizador.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    argumentos = Analizador.parse_args()
    especificación = json.loads((raízProyecto / 'relink.json').read_text())
    construirSistema = raízProyecto / 'build'
    paqueteNuevo = construirSistema / 'relinked'
    paqueteNuevo.mkdir(exist_ok=True)
    herramientaCompilador = os.environ.get('ARM64_CC', 'clang')
    conector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    herramientaArchivoComprimido = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    ajustesRemoto = json.loads((construirSistema / 'remote/libassh-build.json').read_text())
    ajustes = ajustesRemoto['flags']
    if argumentos.libassh_archive:
        paqueteSeguridad = argumentos.libassh_archive.resolve()
    else:
        destinos = []
        Encabezados = ['-I', raízProyecto / 'valorRemoto', '-I', raízProyecto / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for nombre in ajustesRemoto['sources']:
            valorDestino = paqueteNuevo / (Path(nombre).stem + '.o')
            ejecutarComando([herramientaCompilador] + ajustes + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + Encabezados +
                 ['-c', raízProyecto / nombre, '-o', valorDestino])
            destinos.append(valorDestino)
        paqueteSeguridad = paqueteNuevo / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(paqueteNuevo)) as valorTemporal:
            paqueteTemporal = Path(valorTemporal) / 'libassh.a'
            ejecutarComando([herramientaArchivoComprimido, 'rcs', paqueteTemporal] + destinos)
            paqueteTemporal.replace(paqueteSeguridad)
    if argumentos.tinycc:
        if not argumentos.sdk:
            Analizador.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        desarrollo = argumentos.sdk.resolve()
        valorAritmética = sorted((desarrollo / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not valorAritmética or not (desarrollo / 'usr/include/stdio.h').is_file():
            Analizador.error('SDK must contain ARM64 musl headers and libgcc.a')
        configurarActivado = [valorSelección for valorSelección in ajustes if valorSelección != '-mgeneral-regs-only']
        valorDestino = paqueteNuevo / 'herramientaCompilador.o'
        ejecutarComando([herramientaCompilador] + configurarActivado + ['-ffunction-sections', '-fdata-sections',
             '-I', raízProyecto / 'CompiladorC', '-I', raízProyecto / 'vendor/tinycc', '-I', raízProyecto / 'Usuario',
             '-I', construirSistema / 'ccompiler', '-isystem', desarrollo / 'usr/include', '-c', raízProyecto / 'CompiladorC/herramientaCompilador.c', '-o', valorDestino])
        ejecutarComando([conector, '--gc-sections', '-T', raízProyecto / 'Usuario/DisposiciónEnlace.ld', '-z', 'max-page-size=4096',
             '-o', construirSistema / 'user/cc.elf', construirSistema / 'user/start.o', construirSistema / 'user/runtime.o', valorDestino] +
             [construirSistema / 'ccompiler' / (nombre + '.o') for nombre in ('SoporteEntornoEjecución', 'ponerEnMarcha', 'tiempoDeAnticipado', 'puenteRetornar')] +
             [construirSistema / 'user' / (nombre + '.o') for nombre in ('jar', 'tinflate', 'crc32', 'adler32')] + [valorAritmética[-1]])
        valorCabecera = construirSistema / 'programs.h'
        valorCabecera.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda esIgual: esIgual.group(1) + str((construirSistema / 'user/cc.elf').stat().st_size), valorCabecera.read_text()))
        ejecutarComando([herramientaCompilador] + ajustes + ['-c', construirSistema / 'programs.S', '-o', raízProyecto / 'objects/programs.o'])
        ejecutarComando([herramientaCompilador] + ajustes + ['-std=c11', '-I', raízProyecto / 'posix-kor/arm64-native/Encabezados', '-I', construirSistema,
             '-c', raízProyecto / 'máquina/Usuario.c', '-o', raízProyecto / 'objects/user.o'])
    ejecutarComando([conector, '--gc-sections', '-T', raízProyecto / 'Arranque/DisposiciónEnlace.ld', '-o', paqueteNuevo / 'kernel.elf'] +
         [raízProyecto / ruta for ruta in especificación['objects']] + ['--start-group'] +
         [paqueteSeguridad if ruta == 'objects/libassh.a' else raízProyecto / ruta for ruta in especificación['libraries']] + ['--end-group'])
    ejecutarComando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', paqueteNuevo / 'kernel.elf', paqueteNuevo / 'kernel8.img'])
    archivoResumenHash = hashlib.sha256((paqueteNuevo / 'kernel8.img').read_bytes()).hexdigest()
    if argumentos.verify and archivoResumenHash != especificación['kernel_sha256']:
        raise SystemExit('extremoReconectar 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + archivoResumenHash)
    print('RELINK PASS', archivoResumenHash, paqueteNuevo / 'kernel8.img')


if __name__ == '__main__':
    ponerEnMarcha()
