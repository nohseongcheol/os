#!/usr/bin/env python3
"""em_dia_item nativo ARM64 산출물을 검사하고 LGPL fonte_árvore·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

ação_raiz = Path(__file__).resolve().parents[1]
repositório_raiz = ação_raiz.parents[1]
destino_nome = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
biblioteca = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_Arquivo(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def 점검():
    for Nome in ('vendor/wolfssh', 'vendor/wolfssl', 'remoto_VALOR/user_settings.h'):
        if (ação_raiz / Nome).exists():
            raise SystemExit('COSL distribuição_VALOR Parar: Anterior_item GPL remoto_VALOR 구현이 fonte_árvore 트리에 남아 있습니다: ' + Nome)
    com_fio_VALOR = (ação_raiz / 'rede_pilha/com_fio_rede.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in com_fio_VALOR or 'SPDX-License-Identifier: GPL' in com_fio_VALOR:
        raise SystemExit('COSL distribuição_VALOR Parar: BSD GENET implementação·고지 verificar 필요')
    for Nome in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (repositório_raiz / Nome).is_file():
            raise SystemExit('COSL distribuição_VALOR 고지 없음: ' + Nome)
    símbolo_VALOR = subprocess.check_output(['aarch64-linux-gnu-nm', str(ação_raiz / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', símbolo_VALOR):
        raise SystemExit('COSL distribuição_VALOR Parar: 커널에 Anterior_item GPL senha_VALOR/SSH 심볼이 남아 있습니다. repetir_VALOR 빌드하세요.')
    for Nome in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nome + r'$', símbolo_VALOR, re.M):
            raise SystemExit('COSL 대체 implementação 누락: ' + Nome)
    with tempfile.TemporaryDirectory(dir=str(ação_raiz / 'build')) as 임시:
        foto_VALOR = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(ação_raiz / 'build/kernel.elf'), str(foto_VALOR)])
        if hash_Arquivo(foto_VALOR) != hash_Arquivo(ação_raiz / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    relatar_VALOR = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_Arquivo(ação_raiz / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nome: hash_Arquivo(ação_raiz / 'build' / Nome) for Nome in biblioteca}}
    (ação_raiz / 'build/cosl-distribution-check.json').write_text(json.dumps(relatar_VALOR, ensure_ascii=False, indent=2) + '\n')
    return relatar_VALOR


def BIND_empresa():
    relatar_VALOR = 점검()
    distribuição_VALOR = ação_raiz / 'dist'
    distribuição_VALOR.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(ação_raiz / 'build')) as 임시:
        Grupo_VALOR = Path(임시) / 'jkoros-native-relink'
        Grupo_VALOR.mkdir()
        def copiar_VALOR(원본, par_VALOR):
            destino_VALOR = Grupo_VALOR / par_VALOR
            destino_VALOR.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(destino_VALOR), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(destino_VALOR))
        for Nome in destino_nome:
            copiar_VALOR(ação_raiz / 'build' / (Nome + '.o'), 'objects/' + Nome + '.o')
        for Nome in biblioteca:
            copiar_VALOR(ação_raiz / 'build' / Nome, 'objects/' + Path(Nome).name)
        for Nome in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_compilador', 'espaço_do_utilizador', '명명', 'computador', 'rede_pilha/rede_pilha.h', 'arranque_da_máquina/disposição_de_ligação.ld',
                     'remoto_VALOR/assh_config.h', 'remoto_VALOR/config.h', 'remoto_VALOR/ctype.h', 'remoto_VALOR/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            copiar_VALOR(ação_raiz / Nome, Nome)
        for Nome in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            copiar_VALOR(repositório_raiz / Nome, Nome)
        for caminho in sorted((ação_raiz / 'vendor').glob('LICENSE*')):
            copiar_VALOR(caminho, 'vendor/' + caminho.name)
        copiar_VALOR(ação_raiz / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        copiar_VALOR(ação_raiz / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        copiar_VALOR(repositório_raiz / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        copiar_VALOR(ação_raiz / 'ferramentas/재연결.py', 'relink.py')
        for caminho in sorted((ação_raiz / 'build/user').glob('*.elf')):
            copiar_VALOR(caminho, 'build/user/' + caminho.name)
        for Nome in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            copiar_VALOR(ação_raiz / 'build/user' / (Nome + '.o'), 'build/user/' + Nome + '.o')
        for Nome in ('crt', 'aot-runtime', 'SuporteExecução', 'iniciar', '미리번역', 'devolver_ponte'):
            copiar_VALOR(ação_raiz / 'build/ccompiler' / (Nome + '.o'), 'build/ccompiler/' + Nome + '.o')
        especificação = dict(relatar_VALOR, objects=['objects/' + Nome + '.o' for Nome in destino_nome],
                    libraries=['objects/' + Path(caminho).name for caminho in biblioteca])
        (Grupo_VALOR / 'relink.json').write_text(json.dumps(especificação, ensure_ascii=False, indent=2) + '\n')
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

TinyCC source is included in vendor/tinycc; the native port is in C_compilador.
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
        meta = distribuição_VALOR / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / meta.name
        with tarfile.open(str(임시압축), 'w:gz') as arquivo_VALOR:
            arquivo_VALOR.add(str(Grupo_VALOR), arcname=Grupo_VALOR.name)
        임시압축.replace(meta)
    relatar_VALOR['relink_archive_sha256'] = hash_Arquivo(meta)
    (distribuição_VALOR / 'cosl-distribution.json').write_text(json.dumps(relatar_VALOR, ensure_ascii=False, indent=2) + '\n')
    return meta


if __name__ == '__main__':
    analisador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analisador_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALOR = analisador_48ee4b1b.parse_args()
    if VALOR.command == 'bundle':
        print('COSL source/relink kit:', BIND_empresa())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
