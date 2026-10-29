#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL pinagmulan_balangkas·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_root = Path(__file__).resolve().parents[1]
repository_root = Project_root.parents[1]
patutunguhan_pangalan = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
library = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def 점검():
    for pangalan in ('vendor/wolfssh', 'vendor/wolfssl', 'malayuan_VALUE/user_settings.h'):
        if (Project_root / pangalan).exists():
            raise SystemExit('COSL 배포 Hinto: 이전 GPL malayuan_VALUE 구현이 pinagmulan_balangkas 트리에 남아 있습니다: ' + pangalan)
    naka_wire_VALUE = (Project_root / 'Network_Stack/naka_wire_Network.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in naka_wire_VALUE or 'SPDX-License-Identifier: GPL' in naka_wire_VALUE:
        raise SystemExit('COSL 배포 Hinto: BSD GENET 구현·고지 tiyakin_kumpirmahin 필요')
    for pangalan in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (repository_root / pangalan).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + pangalan)
    simbolo_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_root / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbolo_VALUE):
        raise SystemExit('COSL 배포 Hinto: 커널에 이전 GPL password_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for pangalan in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + pangalan + r'$', simbolo_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + pangalan)
    with tempfile.TemporaryDirectory(dir=str(Project_root / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_root / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if hash_file(IMAGE_VALUE) != hash_file(Project_root / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ulat_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_file(Project_root / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {pangalan: hash_file(Project_root / 'build' / pangalan) for pangalan in library}}
    (Project_root / 'build/cosl-distribution-check.json').write_text(json.dumps(ulat_VALUE, ensure_ascii=False, indent=2) + '\n')
    return ulat_VALUE


def 묶기():
    ulat_VALUE = 점검()
    배포 = Project_root / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_root / 'build')) as 임시:
        Grupo_VALUE = Path(임시) / 'jkoros-native-relink'
        Grupo_VALUE.mkdir()
        def gumawa_ng_kopya_VALUE(원본, peer_VALUE):
            patutunguhan_VALUE = Grupo_VALUE / peer_VALUE
            patutunguhan_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(patutunguhan_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(patutunguhan_VALUE))
        for pangalan in patutunguhan_pangalan:
            gumawa_ng_kopya_VALUE(Project_root / 'build' / (pangalan + '.o'), 'objects/' + pangalan + '.o')
        for pangalan in library:
            gumawa_ng_kopya_VALUE(Project_root / 'build' / pangalan, 'objects/' + Path(pangalan).name)
        for pangalan in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'gumagamit', '명명', 'machine', 'Network_Stack/Network_Stack.h', '부팅/Link_Layout.ld',
                     'malayuan_VALUE/assh_config.h', 'malayuan_VALUE/config.h', 'malayuan_VALUE/ctype.h', 'malayuan_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            gumawa_ng_kopya_VALUE(Project_root / pangalan, pangalan)
        for pangalan in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            gumawa_ng_kopya_VALUE(repository_root / pangalan, pangalan)
        for path in sorted((Project_root / 'vendor').glob('LICENSE*')):
            gumawa_ng_kopya_VALUE(path, 'vendor/' + path.name)
        gumawa_ng_kopya_VALUE(Project_root / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        gumawa_ng_kopya_VALUE(Project_root / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        gumawa_ng_kopya_VALUE(repository_root / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        gumawa_ng_kopya_VALUE(Project_root / 'Mga_Tool/재연결.py', 'relink.py')
        for path in sorted((Project_root / 'build/user').glob('*.elf')):
            gumawa_ng_kopya_VALUE(path, 'build/user/' + path.name)
        for pangalan in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            gumawa_ng_kopya_VALUE(Project_root / 'build/user' / (pangalan + '.o'), 'build/user/' + pangalan + '.o')
        for pangalan in ('crt', 'aot-runtime', 'common_language_runtime_Suporta', 'run', '미리번역', '되돌림'):
            gumawa_ng_kopya_VALUE(Project_root / 'build/ccompiler' / (pangalan + '.o'), 'build/ccompiler/' + pangalan + '.o')
        명세 = dict(ulat_VALUE, objects=['objects/' + pangalan + '.o' for pangalan in patutunguhan_pangalan],
                    libraries=['objects/' + Path(path).name for path in library])
        (Grupo_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Grupo_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        layunin = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / layunin.name
        with tarfile.open(str(임시압축), 'w:gz') as Archive_VALUE:
            Archive_VALUE.add(str(Grupo_VALUE), arcname=Grupo_VALUE.name)
        임시압축.replace(layunin)
    ulat_VALUE['relink_archive_sha256'] = hash_file(layunin)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ulat_VALUE, ensure_ascii=False, indent=2) + '\n')
    return layunin


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = parser_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
