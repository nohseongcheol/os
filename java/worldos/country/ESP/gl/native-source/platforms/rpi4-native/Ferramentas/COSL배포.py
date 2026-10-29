#!/usr/bin/env python3
"""ao_corrente_elemento 자체 ARM64 산출물을 검사하고 LGPL fonte_árbore·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_raíz = Path(__file__).resolve().parents[1]
repositorio_raíz = Project_raíz.parents[1]
destino_nome = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
biblioteca = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_Ficheiro(CAMIÑO):
    return hashlib.sha256(Path(CAMIÑO).read_bytes()).hexdigest()


def 점검():
    for Nome in ('vendor/wolfssh', 'vendor/wolfssl', 'remoto_VALOR/user_settings.h'):
        if (Project_raíz / Nome).exists():
            raise SystemExit('COSL 배포 Deter: 이전 GPL remoto_VALOR 구현이 fonte_árbore 트리에 남아 있습니다: ' + Nome)
    con_fíos_VALOR = (Project_raíz / 'Rede_Montón/con_fíos_Rede.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in con_fíos_VALOR or 'SPDX-License-Identifier: GPL' in con_fíos_VALOR:
        raise SystemExit('COSL 배포 Deter: BSD GENET 구현·고지 verificar 필요')
    for Nome in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (repositorio_raíz / Nome).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Nome)
    símbolo_VALOR = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_raíz / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', símbolo_VALOR):
        raise SystemExit('COSL 배포 Deter: 커널에 이전 GPL contrasinal_VALOR/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Nome in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nome + r'$', símbolo_VALOR, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Nome)
    with tempfile.TemporaryDirectory(dir=str(Project_raíz / 'build')) as 임시:
        IMAXE_VALOR = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_raíz / 'build/kernel.elf'), str(IMAXE_VALOR)])
        if hash_Ficheiro(IMAXE_VALOR) != hash_Ficheiro(Project_raíz / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    informe_VALOR = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_Ficheiro(Project_raíz / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nome: hash_Ficheiro(Project_raíz / 'build' / Nome) for Nome in biblioteca}}
    (Project_raíz / 'build/cosl-distribution-check.json').write_text(json.dumps(informe_VALOR, ensure_ascii=False, indent=2) + '\n')
    return informe_VALOR


def ligar_extremo():
    informe_VALOR = 점검()
    배포 = Project_raíz / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_raíz / 'build')) as 임시:
        Grupo_VALOR = Path(임시) / 'jkoros-native-relink'
        Grupo_VALOR.mkdir()
        def copiar_VALOR(원본, punto_VALOR):
            destino_VALOR = Grupo_VALOR / punto_VALOR
            destino_VALOR.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(destino_VALOR), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(destino_VALOR))
        for Nome in destino_nome:
            copiar_VALOR(Project_raíz / 'build' / (Nome + '.o'), 'objects/' + Nome + '.o')
        for Nome in biblioteca:
            copiar_VALOR(Project_raíz / 'build' / Nome, 'objects/' + Path(Nome).name)
        for Nome in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'usuario', '명명', 'máquina', 'Rede_Montón/Rede_Montón.h', '부팅/Ligar_deseño.ld',
                     'remoto_VALOR/assh_config.h', 'remoto_VALOR/config.h', 'remoto_VALOR/ctype.h', 'remoto_VALOR/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            copiar_VALOR(Project_raíz / Nome, Nome)
        for Nome in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            copiar_VALOR(repositorio_raíz / Nome, Nome)
        for CAMIÑO in sorted((Project_raíz / 'vendor').glob('LICENSE*')):
            copiar_VALOR(CAMIÑO, 'vendor/' + CAMIÑO.name)
        copiar_VALOR(Project_raíz / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        copiar_VALOR(Project_raíz / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        copiar_VALOR(repositorio_raíz / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        copiar_VALOR(Project_raíz / 'Ferramentas/재연결.py', 'relink.py')
        for CAMIÑO in sorted((Project_raíz / 'build/user').glob('*.elf')):
            copiar_VALOR(CAMIÑO, 'build/user/' + CAMIÑO.name)
        for Nome in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            copiar_VALOR(Project_raíz / 'build/user' / (Nome + '.o'), 'build/user/' + Nome + '.o')
        for Nome in ('crt', 'aot-runtime', '실행지원', 'Executar_2', '미리번역', 'devolver_ponte'):
            copiar_VALOR(Project_raíz / 'build/ccompiler' / (Nome + '.o'), 'build/ccompiler/' + Nome + '.o')
        명세 = dict(informe_VALOR, objects=['objects/' + Nome + '.o' for Nome in destino_nome],
                    libraries=['objects/' + Path(CAMIÑO).name for CAMIÑO in biblioteca])
        (Grupo_VALOR / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Grupo_VALOR / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in 시언어번역기.
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
        obxectivo_VALOR = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / obxectivo_VALOR.name
        with tarfile.open(str(임시압축), 'w:gz') as Arquivo_VALOR:
            Arquivo_VALOR.add(str(Grupo_VALOR), arcname=Grupo_VALOR.name)
        임시압축.replace(obxectivo_VALOR)
    informe_VALOR['relink_archive_sha256'] = hash_Ficheiro(obxectivo_VALOR)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(informe_VALOR, ensure_ascii=False, indent=2) + '\n')
    return obxectivo_VALOR


if __name__ == '__main__':
    analizador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizador_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALOR = analizador_48ee4b1b.parse_args()
    if VALOR.command == 'bundle':
        print('COSL source/relink kit:', ligar_extremo())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
