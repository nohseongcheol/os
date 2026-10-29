#!/usr/bin/env python3
"""Regolari_articolo nativo ARM64 산출물을 검사하고 LGPL fonte_albero·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

azione_radice = Path(__file__).resolve().parents[1]
radice_del_repository = azione_radice.parents[1]
meta_nome = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
Catalogo = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_File(percorso):
    return hashlib.sha256(Path(percorso).read_bytes()).hexdigest()


def 점검():
    for Nome in ('vendor/wolfssh', 'vendor/wolfssl', 'remoto_VALORE/user_settings.h'):
        if (azione_radice / Nome).exists():
            raise SystemExit('COSL distribuzione_VALORE Ferma: Indietro_articolo GPL remoto_VALORE 구현이 fonte_albero 트리에 남아 있습니다: ' + Nome)
    cablato_VALORE = (azione_radice / 'rete_Pila/cablato_rete.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in cablato_VALORE or 'SPDX-License-Identifier: GPL' in cablato_VALORE:
        raise SystemExit('COSL distribuzione_VALORE Ferma: BSD GENET implementazione·고지 verificare 필요')
    for Nome in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (radice_del_repository / Nome).is_file():
            raise SystemExit('COSL distribuzione_VALORE 고지 없음: ' + Nome)
    simbolo_VALORE = subprocess.check_output(['aarch64-linux-gnu-nm', str(azione_radice / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbolo_VALORE):
        raise SystemExit('COSL distribuzione_VALORE Ferma: 커널에 Indietro_articolo GPL password_VALORE/SSH 심볼이 남아 있습니다. retry_VALORE 빌드하세요.')
    for Nome in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nome + r'$', simbolo_VALORE, re.M):
            raise SystemExit('COSL 대체 implementazione 누락: ' + Nome)
    with tempfile.TemporaryDirectory(dir=str(azione_radice / 'build')) as 임시:
        foto_VALORE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(azione_radice / 'build/kernel.elf'), str(foto_VALORE)])
        if hash_File(foto_VALORE) != hash_File(azione_radice / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    Report_VALORE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_File(azione_radice / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nome: hash_File(azione_radice / 'build' / Nome) for Nome in Catalogo}}
    (azione_radice / 'build/cosl-distribution-check.json').write_text(json.dumps(Report_VALORE, ensure_ascii=False, indent=2) + '\n')
    return Report_VALORE


def BIND_endpoint():
    Report_VALORE = 점검()
    distribuzione_VALORE = azione_radice / 'dist'
    distribuzione_VALORE.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(azione_radice / 'build')) as 임시:
        gruppo_VALORE = Path(임시) / 'jkoros-native-relink'
        gruppo_VALORE.mkdir()
        def copiare_VALORE(원본, peer_VALORE):
            meta_VALORE = gruppo_VALORE / peer_VALORE
            meta_VALORE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(meta_VALORE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(meta_VALORE))
        for Nome in meta_nome:
            copiare_VALORE(azione_radice / 'build' / (Nome + '.o'), 'objects/' + Nome + '.o')
        for Nome in Catalogo:
            copiare_VALORE(azione_radice / 'build' / Nome, 'objects/' + Path(Nome).name)
        for Nome in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_compilatore', 'spazio_utente', '명명', 'computer', 'rete_Pila/rete_Pila.h', 'avvio_macchina/disposizione_di_collegamento.ld',
                     'remoto_VALORE/assh_config.h', 'remoto_VALORE/config.h', 'remoto_VALORE/ctype.h', 'remoto_VALORE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            copiare_VALORE(azione_radice / Nome, Nome)
        for Nome in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            copiare_VALORE(radice_del_repository / Nome, Nome)
        for percorso in sorted((azione_radice / 'vendor').glob('LICENSE*')):
            copiare_VALORE(percorso, 'vendor/' + percorso.name)
        copiare_VALORE(azione_radice / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        copiare_VALORE(azione_radice / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        copiare_VALORE(radice_del_repository / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        copiare_VALORE(azione_radice / 'strumenti/재연결.py', 'relink.py')
        for percorso in sorted((azione_radice / 'build/user').glob('*.elf')):
            copiare_VALORE(percorso, 'build/user/' + percorso.name)
        for Nome in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            copiare_VALORE(azione_radice / 'build/user' / (Nome + '.o'), 'build/user/' + Nome + '.o')
        for Nome in ('crt', 'aot-runtime', 'CLR_Supporto', 'avvia', '미리번역', 'Reso_bridge'):
            copiare_VALORE(azione_radice / 'build/ccompiler' / (Nome + '.o'), 'build/ccompiler/' + Nome + '.o')
        specifica = dict(Report_VALORE, objects=['objects/' + Nome + '.o' for Nome in meta_nome],
                    libraries=['objects/' + Path(percorso).name for percorso in Catalogo])
        (gruppo_VALORE / 'relink.json').write_text(json.dumps(specifica, ensure_ascii=False, indent=2) + '\n')
        (gruppo_VALORE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_compilatore.
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
        target = distribuzione_VALORE / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / target.name
        with tarfile.open(str(임시압축), 'w:gz') as Archivio_VALORE:
            Archivio_VALORE.add(str(gruppo_VALORE), arcname=gruppo_VALORE.name)
        임시압축.replace(target)
    Report_VALORE['relink_archive_sha256'] = hash_File(target)
    (distribuzione_VALORE / 'cosl-distribution.json').write_text(json.dumps(Report_VALORE, ensure_ascii=False, indent=2) + '\n')
    return target


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALORE = parser_48ee4b1b.parse_args()
    if VALORE.command == 'bundle':
        print('COSL source/relink kit:', BIND_endpoint())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
