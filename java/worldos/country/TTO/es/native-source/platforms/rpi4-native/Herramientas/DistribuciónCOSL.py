#!/usr/bin/env python3
"""elementoListaActual propio ARM64 산출물을 검사하고 LGPL árbolFuente·extremoReconectar 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

raízProyecto = Path(__file__).resolve().parents[1]
raízRepositorio = raízProyecto.parents[1]
nombreDestino = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
biblioteca = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def archivoResumenHash(ruta):
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def inspeccionarEstadoValor():
    for nombre in ('vendor/wolfssh', 'vendor/wolfssl', 'valorRemoto/user_settings.h'):
        if (raízProyecto / nombre).exists():
            raise SystemExit('COSL valorDistribución detener: elementoListaElementoPrevio GPL valorRemoto 구현이 árbolFuente 트리에 남아 있습니다: ' + nombre)
    valorCableado = (raízProyecto / 'PilaRed/redCableado.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in valorCableado or 'SPDX-License-Identifier: GPL' in valorCableado:
        raise SystemExit('COSL valorDistribución detener: BSD GENET implementación·고지 verificar valorNecesario')
    for nombre in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (raízRepositorio / nombre).is_file():
            raise SystemExit('COSL valorDistribución 고지 métodoAusente: ' + nombre)
    valorSímbolo = subprocess.check_output(['aarch64-linux-gnu-nm', str(raízProyecto / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', valorSímbolo):
        raise SystemExit('COSL valorDistribución detener: 커널에 elementoListaElementoPrevio GPL valorContraseña/SSH 심볼이 남아 있습니다. valorReintentar 빌드하세요.')
    for nombre in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + nombre + r'$', valorSímbolo, re.M):
            raise SystemExit('COSL 대체 implementación 누락: ' + nombre)
    with tempfile.TemporaryDirectory(dir=str(raízProyecto / 'build')) as valorTemporal:
        valorImagen = Path(valorTemporal) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(raízProyecto / 'build/kernel.elf'), str(valorImagen)])
        if archivoResumenHash(valorImagen) != archivoResumenHash(raízProyecto / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    valorInforme = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': archivoResumenHash(raízProyecto / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {nombre: archivoResumenHash(raízProyecto / 'build' / nombre) for nombre in biblioteca}}
    (raízProyecto / 'build/cosl-distribution-check.json').write_text(json.dumps(valorInforme, ensure_ascii=False, indent=2) + '\n')
    return valorInforme


def EmpaquetarEjecutables():
    valorInforme = inspeccionarEstadoValor()
    valorDistribución = raízProyecto / 'dist'
    valorDistribución.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(raízProyecto / 'build')) as valorTemporal:
        valorGrupo = Path(valorTemporal) / 'jkoros-native-relink'
        valorGrupo.mkdir()
        def copiarValor(original, valorParRed):
            valorDestino = valorGrupo / valorParRed
            valorDestino.parent.mkdir(parents=True, exist_ok=True)
            if original.is_dir():
                shutil.copytree(str(original), str(valorDestino), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(original), str(valorDestino))
        for nombre in nombreDestino:
            copiarValor(raízProyecto / 'build' / (nombre + '.o'), 'objects/' + nombre + '.o')
        for nombre in biblioteca:
            copiarValor(raízProyecto / 'build' / nombre, 'objects/' + Path(nombre).name)
        for nombre in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'CompiladorC', 'Usuario', 'denominación', 'máquina', 'PilaRed/PilaRed.h', 'Arranque/DisposiciónEnlace.ld',
                     'valorRemoto/assh_config.h', 'valorRemoto/config.h', 'valorRemoto/ctype.h', 'valorRemoto/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'GuíaDistribuciónCOSL.md'):
            copiarValor(raízProyecto / nombre, nombre)
        for nombre in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            copiarValor(raízRepositorio / nombre, nombre)
        for ruta in sorted((raízProyecto / 'vendor').glob('LICENSE*')):
            copiarValor(ruta, 'vendor/' + ruta.name)
        copiarValor(raízProyecto / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        copiarValor(raízProyecto / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        copiarValor(raízRepositorio / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        copiarValor(raízProyecto / 'Herramientas/extremoReconectar.py', 'relink.py')
        for ruta in sorted((raízProyecto / 'build/user').glob('*.elf')):
            copiarValor(ruta, 'build/user/' + ruta.name)
        for nombre in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            copiarValor(raízProyecto / 'build/user' / (nombre + '.o'), 'build/user/' + nombre + '.o')
        for nombre in ('crt', 'aot-runtime', 'SoporteEntornoEjecución', 'ponerEnMarcha', 'tiempoDeAnticipado', 'puenteRetornar'):
            copiarValor(raízProyecto / 'build/ccompiler' / (nombre + '.o'), 'build/ccompiler/' + nombre + '.o')
        especificación = dict(valorInforme, objects=['objects/' + nombre + '.o' for nombre in nombreDestino],
                    libraries=['objects/' + Path(ruta).name for ruta in biblioteca])
        (valorGrupo / 'relink.json').write_text(json.dumps(especificación, ensure_ascii=False, indent=2) + '\n')
        (valorGrupo / 'README.md').write_text('''# jkoros native LGPL source and relink kit

This kit accompanies the matching kernel image. Retain it with binary distributions.
Application terms: LICENSE. Library terms: vendor/libassh/COPYING and vendor/tinycc/COPYING.
Other notices: THIRD_PARTY_NOTICES.md. COSL does not override the LGPL permissions.
This product includes software developed by Bill Paul.

Host dependencies: Python 3, Clang supporting aarch64-none-elf, libnewlib-dev headers,
and aarch64-linux-gnu binutils. No Linux kernel is linked into the guest.

From this extracted directory:

    python3 relink.py --verify

This recompiles libassh from the included source/configuration and relinks the kernel.
The original unmodified library must produce the recorded kernel SHA256.
To change libassh, edit vendor/libassh/src, then run without --verify.
Alternatively: python3 relink.py --libassh-archive /path/to/modified/libassh.a

TinyCC source is included in vendor/tinycc; the native port is in CompiladorC.
To rebuild a modified TinyCC and replace its embedded executable:

    python3 relink.py --tinycc --sdk /path/to/alpine-arm64-rootfs

Use the same Alpine 3.24.2 ARM64 SDK headers and GCC 15.2.0 libgcc runtime as the
original build (jkoros/platforms/rpi4: make prepare-runtime; see that platform's docs).
The SDK is a host build prerequisite and is not included here. Its libgcc exception
and GPL text are in vendor/LICENSE.libgcc-runtime and vendor/LICENSE.gcc-gpl3.
GCC sources: https://gcc.gnu.org/pub/gcc/releases/gcc-15.2.0/
Both the cc ELF size table and user/program objects are regenerated when --tinycc is used.
Output: build/relinked/kernel8.img. Boot it using the same Pi4 firmware/config or QEMU
runner as the original image. There is no signature lock against modified libraries.

This is a relink kit for one device image. Objects contain the same embedded device
key as that image. Keep personal development images and build/remote credentials
out of public source uploads; provision appropriate images for recipients.
''')
        valorObjetivo = valorDistribución / 'jkoros-native-relink.tar.gz'
        archivoComprimidoTemporal = Path(valorTemporal) / valorObjetivo.name
        with tarfile.open(str(archivoComprimidoTemporal), 'w:gz') as valorArchivoComprimido:
            valorArchivoComprimido.add(str(valorGrupo), arcname=valorGrupo.name)
        archivoComprimidoTemporal.replace(valorObjetivo)
    valorInforme['relink_archive_sha256'] = archivoResumenHash(valorObjetivo)
    (valorDistribución / 'cosl-distribution.json').write_text(json.dumps(valorInforme, ensure_ascii=False, indent=2) + '\n')
    return valorObjetivo


if __name__ == '__main__':
    Analizador = argparse.ArgumentParser(description=__doc__)
    Analizador.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    valor = Analizador.parse_args()
    if valor.command == 'bundle':
        print('COSL source/relink kit:', EmpaquetarEjecutables())
    else:
        print(json.dumps(inspeccionarEstadoValor(), ensure_ascii=False, indent=2))
