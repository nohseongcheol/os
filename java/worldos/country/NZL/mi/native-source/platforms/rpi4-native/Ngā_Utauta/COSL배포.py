#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL pūtake_rākau·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

whakaatu_pūtake = Path(__file__).resolve().parents[1]
저장소 = whakaatu_pūtake.parents[1]
ūnga_ingoa = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
puna = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_kōnae(ara):
    return hashlib.sha256(Path(ara).read_bytes()).hexdigest()


def 점검():
    for Ingoa in ('vendor/wolfssh', 'vendor/wolfssl', 'mamao_uara/user_settings.h'):
        if (whakaatu_pūtake / Ingoa).exists():
            raise SystemExit('COSL 배포 Whakamutua: 이전 GPL mamao_uara 구현이 pūtake_rākau 트리에 남아 있습니다: ' + Ingoa)
    whaiaho_uara = (whakaatu_pūtake / 'whatunga_Huinga/whaiaho_whatunga.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in whaiaho_uara or 'SPDX-License-Identifier: GPL' in whaiaho_uara:
        raise SystemExit('COSL 배포 Whakamutua: BSD GENET 구현·고지 manatoko 필요')
    for Ingoa in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Ingoa).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Ingoa)
    tohu_uara = subprocess.check_output(['aarch64-linux-gnu-nm', str(whakaatu_pūtake / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', tohu_uara):
        raise SystemExit('COSL 배포 Whakamutua: 커널에 이전 GPL kupuhipa_uara/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Ingoa in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Ingoa + r'$', tohu_uara, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Ingoa)
    with tempfile.TemporaryDirectory(dir=str(whakaatu_pūtake / 'build')) as 임시:
        IMAGE_uara = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(whakaatu_pūtake / 'build/kernel.elf'), str(IMAGE_uara)])
        if hash_kōnae(IMAGE_uara) != hash_kōnae(whakaatu_pūtake / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    pūrongo_uara = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_kōnae(whakaatu_pūtake / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Ingoa: hash_kōnae(whakaatu_pūtake / 'build' / Ingoa) for Ingoa in puna}}
    (whakaatu_pūtake / 'build/cosl-distribution-check.json').write_text(json.dumps(pūrongo_uara, ensure_ascii=False, indent=2) + '\n')
    return pūrongo_uara


def 묶기():
    pūrongo_uara = 점검()
    배포 = whakaatu_pūtake / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(whakaatu_pūtake / 'build')) as 임시:
        rōpū_uara = Path(임시) / 'jkoros-native-relink'
        rōpū_uara.mkdir()
        def tārua_uara(원본, hoa_uara):
            ūnga_uara = rōpū_uara / hoa_uara
            ūnga_uara.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ūnga_uara), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ūnga_uara))
        for Ingoa in ūnga_ingoa:
            tārua_uara(whakaatu_pūtake / 'build' / (Ingoa + '.o'), 'objects/' + Ingoa + '.o')
        for Ingoa in puna:
            tārua_uara(whakaatu_pūtake / 'build' / Ingoa, 'objects/' + Path(Ingoa).name)
        for Ingoa in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'kaiwhakamahi', '명명', 'mīhini', 'whatunga_Huinga/whatunga_Huinga.h', '부팅/Hono_Tahora.ld',
                     'mamao_uara/assh_config.h', 'mamao_uara/config.h', 'mamao_uara/ctype.h', 'mamao_uara/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            tārua_uara(whakaatu_pūtake / Ingoa, Ingoa)
        for Ingoa in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            tārua_uara(저장소 / Ingoa, Ingoa)
        for ara in sorted((whakaatu_pūtake / 'vendor').glob('LICENSE*')):
            tārua_uara(ara, 'vendor/' + ara.name)
        tārua_uara(whakaatu_pūtake / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        tārua_uara(whakaatu_pūtake / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        tārua_uara(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        tārua_uara(whakaatu_pūtake / 'Ngā_Utauta/재연결.py', 'relink.py')
        for ara in sorted((whakaatu_pūtake / 'build/user').glob('*.elf')):
            tārua_uara(ara, 'build/user/' + ara.name)
        for Ingoa in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            tārua_uara(whakaatu_pūtake / 'build/user' / (Ingoa + '.o'), 'build/user/' + Ingoa + '.o')
        for Ingoa in ('crt', 'aot-runtime', 'wāhaere_reo_noa_Tautoko', 'whakahaere', '미리번역', '되돌림'):
            tārua_uara(whakaatu_pūtake / 'build/ccompiler' / (Ingoa + '.o'), 'build/ccompiler/' + Ingoa + '.o')
        명세 = dict(pūrongo_uara, objects=['objects/' + Ingoa + '.o' for Ingoa in ūnga_ingoa],
                    libraries=['objects/' + Path(ara).name for ara in puna])
        (rōpū_uara / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (rōpū_uara / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        ūnga = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ūnga.name
        with tarfile.open(str(임시압축), 'w:gz') as Pūranga_uara:
            Pūranga_uara.add(str(rōpū_uara), arcname=rōpū_uara.name)
        임시압축.replace(ūnga)
    pūrongo_uara['relink_archive_sha256'] = hash_kōnae(ūnga)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(pūrongo_uara, ensure_ascii=False, indent=2) + '\n')
    return ūnga


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    uara = 해석기.parse_args()
    if uara.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
