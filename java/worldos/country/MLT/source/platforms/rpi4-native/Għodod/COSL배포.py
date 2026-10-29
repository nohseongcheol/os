#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL sors_siġra·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

pprojetta_għerq = Path(__file__).resolve().parents[1]
저장소 = pprojetta_għerq.parents[1]
destinazzjoni_isem = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
librerija = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_fajl(mogħdija):
    return hashlib.sha256(Path(mogħdija).read_bytes()).hexdigest()


def 점검():
    for isem in ('vendor/wolfssh', 'vendor/wolfssl', 'mill_bogħod_VALUE/user_settings.h'):
        if (pprojetta_għerq / isem).exists():
            raise SystemExit('COSL 배포 waqqaf: 이전 GPL mill_bogħod_VALUE 구현이 sors_siġra 트리에 남아 있습니다: ' + isem)
    wwajerjat_VALUE = (pprojetta_għerq / 'netwerk_Munzell/wwajerjat_netwerk.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in wwajerjat_VALUE or 'SPDX-License-Identifier: GPL' in wwajerjat_VALUE:
        raise SystemExit('COSL 배포 waqqaf: BSD GENET 구현·고지 vverifika 필요')
    for isem in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / isem).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + isem)
    simbolu_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(pprojetta_għerq / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbolu_VALUE):
        raise SystemExit('COSL 배포 waqqaf: 커널에 이전 GPL password_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for isem in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + isem + r'$', simbolu_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + isem)
    with tempfile.TemporaryDirectory(dir=str(pprojetta_għerq / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(pprojetta_għerq / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if hash_fajl(IMAGE_VALUE) != hash_fajl(pprojetta_għerq / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    rapport_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_fajl(pprojetta_għerq / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {isem: hash_fajl(pprojetta_għerq / 'build' / isem) for isem in librerija}}
    (pprojetta_għerq / 'build/cosl-distribution-check.json').write_text(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2) + '\n')
    return rapport_VALUE


def 묶기():
    rapport_VALUE = 점검()
    배포 = pprojetta_għerq / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(pprojetta_għerq / 'build')) as 임시:
        grupp_VALUE = Path(임시) / 'jkoros-native-relink'
        grupp_VALUE.mkdir()
        def kkopja_VALUE(원본, peer_VALUE):
            destinazzjoni_VALUE = grupp_VALUE / peer_VALUE
            destinazzjoni_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(destinazzjoni_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(destinazzjoni_VALUE))
        for isem in destinazzjoni_isem:
            kkopja_VALUE(pprojetta_għerq / 'build' / (isem + '.o'), 'objects/' + isem + '.o')
        for isem in librerija:
            kkopja_VALUE(pprojetta_għerq / 'build' / isem, 'objects/' + Path(isem).name)
        for isem in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'utent', '명명', 'kompjuter', 'netwerk_Munzell/netwerk_Munzell.h', '부팅/Link_Tqassim.ld',
                     'mill_bogħod_VALUE/assh_config.h', 'mill_bogħod_VALUE/config.h', 'mill_bogħod_VALUE/ctype.h', 'mill_bogħod_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kkopja_VALUE(pprojetta_għerq / isem, isem)
        for isem in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kkopja_VALUE(저장소 / isem, isem)
        for mogħdija in sorted((pprojetta_għerq / 'vendor').glob('LICENSE*')):
            kkopja_VALUE(mogħdija, 'vendor/' + mogħdija.name)
        kkopja_VALUE(pprojetta_għerq / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kkopja_VALUE(pprojetta_għerq / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kkopja_VALUE(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kkopja_VALUE(pprojetta_għerq / 'Għodod/재연결.py', 'relink.py')
        for mogħdija in sorted((pprojetta_għerq / 'build/user').glob('*.elf')):
            kkopja_VALUE(mogħdija, 'build/user/' + mogħdija.name)
        for isem in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kkopja_VALUE(pprojetta_għerq / 'build/user' / (isem + '.o'), 'build/user/' + isem + '.o')
        for isem in ('crt', 'aot-runtime', 'tħaddim_tal_lingwa_komuni_Appoġġ', 'serje', '미리번역', '되돌림'):
            kkopja_VALUE(pprojetta_għerq / 'build/ccompiler' / (isem + '.o'), 'build/ccompiler/' + isem + '.o')
        명세 = dict(rapport_VALUE, objects=['objects/' + isem + '.o' for isem in destinazzjoni_isem],
                    libraries=['objects/' + Path(mogħdija).name for mogħdija in librerija])
        (grupp_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (grupp_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        mira = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / mira.name
        with tarfile.open(str(임시압축), 'w:gz') as Arkivju_VALUE:
            Arkivju_VALUE.add(str(grupp_VALUE), arcname=grupp_VALUE.name)
        임시압축.replace(mira)
    rapport_VALUE['relink_archive_sha256'] = hash_fajl(mira)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2) + '\n')
    return mira


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = 해석기.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
