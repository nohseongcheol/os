#!/usr/bin/env python3
"""현재 propi ARM64 산출물을 검사하고 LGPL font_arbre·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_rel = Path(__file__).resolve().parents[1]
dipòsit_rel = Project_rel.parents[1]
destinació_nom = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
biblioteca = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_arxiu(Camí):
    return hashlib.sha256(Path(Camí).read_bytes()).hexdigest()


def 점검():
    for Nom in ('vendor/wolfssh', 'vendor/wolfssl', 'remot_VALOR/user_settings.h'):
        if (Project_rel / Nom).exists():
            raise SystemExit('COSL 배포 Atura: 이전 GPL remot_VALOR 구현이 font_arbre 트리에 남아 있습니다: ' + Nom)
    per_cable_VALOR = (Project_rel / 'xarxa_Pila/per_cable_xarxa.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in per_cable_VALOR or 'SPDX-License-Identifier: GPL' in per_cable_VALOR:
        raise SystemExit('COSL 배포 Atura: BSD GENET 구현·고지 verificar 필요')
    for Nom in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (dipòsit_rel / Nom).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Nom)
    símbol_VALOR = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_rel / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', símbol_VALOR):
        raise SystemExit('COSL 배포 Atura: 커널에 이전 GPL contrasenya_VALOR/SSH 심볼이 남아 있습니다. tornar_ho_a_provar_VALOR 빌드하세요.')
    for Nom in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nom + r'$', símbol_VALOR, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Nom)
    with tempfile.TemporaryDirectory(dir=str(Project_rel / 'build')) as 임시:
        IMATGE_VALOR = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_rel / 'build/kernel.elf'), str(IMATGE_VALOR)])
        if hash_arxiu(IMATGE_VALOR) != hash_arxiu(Project_rel / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    informe_VALOR = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_arxiu(Project_rel / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nom: hash_arxiu(Project_rel / 'build' / Nom) for Nom in biblioteca}}
    (Project_rel / 'build/cosl-distribution-check.json').write_text(json.dumps(informe_VALOR, ensure_ascii=False, indent=2) + '\n')
    return informe_VALOR


def enllaçar_extrem():
    informe_VALOR = 점검()
    배포 = Project_rel / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_rel / 'build')) as 임시:
        Grup_VALOR = Path(임시) / 'jkoros-native-relink'
        Grup_VALOR.mkdir()
        def copiar_VALOR(원본, homòleg_VALOR):
            destinació_VALOR = Grup_VALOR / homòleg_VALOR
            destinació_VALOR.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(destinació_VALOR), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(destinació_VALOR))
        for Nom in destinació_nom:
            copiar_VALOR(Project_rel / 'build' / (Nom + '.o'), 'objects/' + Nom + '.o')
        for Nom in biblioteca:
            copiar_VALOR(Project_rel / 'build' / Nom, 'objects/' + Path(Nom).name)
        for Nom in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'usuari', '명명', 'màquina', 'xarxa_Pila/xarxa_Pila.h', '부팅/enllaç_disseny.ld',
                     'remot_VALOR/assh_config.h', 'remot_VALOR/config.h', 'remot_VALOR/ctype.h', 'remot_VALOR/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            copiar_VALOR(Project_rel / Nom, Nom)
        for Nom in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            copiar_VALOR(dipòsit_rel / Nom, Nom)
        for Camí in sorted((Project_rel / 'vendor').glob('LICENSE*')):
            copiar_VALOR(Camí, 'vendor/' + Camí.name)
        copiar_VALOR(Project_rel / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        copiar_VALOR(Project_rel / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        copiar_VALOR(dipòsit_rel / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        copiar_VALOR(Project_rel / 'Eines/재연결.py', 'relink.py')
        for Camí in sorted((Project_rel / 'build/user').glob('*.elf')):
            copiar_VALOR(Camí, 'build/user/' + Camí.name)
        for Nom in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            copiar_VALOR(Project_rel / 'build/user' / (Nom + '.o'), 'build/user/' + Nom + '.o')
        for Nom in ('crt', 'aot-runtime', '실행지원', 'Executa_2', '미리번역', 'tornar_les_tasques_pont'):
            copiar_VALOR(Project_rel / 'build/ccompiler' / (Nom + '.o'), 'build/ccompiler/' + Nom + '.o')
        명세 = dict(informe_VALOR, objects=['objects/' + Nom + '.o' for Nom in destinació_nom],
                    libraries=['objects/' + Path(Camí).name for Camí in biblioteca])
        (Grup_VALOR / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Grup_VALOR / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        objectiu = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / objectiu.name
        with tarfile.open(str(임시압축), 'w:gz') as Arxiu_VALOR:
            Arxiu_VALOR.add(str(Grup_VALOR), arcname=Grup_VALOR.name)
        임시압축.replace(objectiu)
    informe_VALOR['relink_archive_sha256'] = hash_arxiu(objectiu)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(informe_VALOR, ensure_ascii=False, indent=2) + '\n')
    return objectiu


if __name__ == '__main__':
    analitzador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analitzador_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALOR = analitzador_48ee4b1b.parse_args()
    if VALOR.command == 'bundle':
        print('COSL source/relink kit:', enllaçar_extrem())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
