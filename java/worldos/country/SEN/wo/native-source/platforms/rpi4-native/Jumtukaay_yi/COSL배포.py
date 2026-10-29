#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL Cosaan_tëralinuy_pàcc·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
jëmmukaay_tur = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
daaray_téere = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def caabiy_teqale_bi_bara_denc(Yoonu_jëmale):
    return hashlib.sha256(Path(Yoonu_jëmale).read_bytes()).hexdigest()


def 점검():
    for tur_253d1510 in ('vendor/wolfssh', 'vendor/wolfssl', 'lu_soree_xëyma/user_settings.h'):
        if (기준 / tur_253d1510).exists():
            raise SystemExit('COSL 배포 tees: 이전 GPL lu_soree_xëyma 구현이 Cosaan_tëralinuy_pàcc 트리에 남아 있습니다: ' + tur_253d1510)
    tënku_xëyma = (기준 / 'mbaal_Tegalo/tënku_mbaal.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in tënku_xëyma or 'SPDX-License-Identifier: GPL' in tënku_xëyma:
        raise SystemExit('COSL 배포 tees: BSD GENET 구현·고지 luñutu 필요')
    for tur_253d1510 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / tur_253d1510).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + tur_253d1510)
    sembóol_xëyma = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', sembóol_xëyma):
        raise SystemExit('COSL 배포 tees: 커널에 이전 GPL pasu_dugg_xëyma/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for tur_253d1510 in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + tur_253d1510 + r'$', sembóol_xëyma, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + tur_253d1510)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        nataal_xëyma = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(nataal_xëyma)])
        if caabiy_teqale_bi_bara_denc(nataal_xëyma) != caabiy_teqale_bi_bara_denc(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    tënk_xëyma = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': caabiy_teqale_bi_bara_denc(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {tur_253d1510: caabiy_teqale_bi_bara_denc(기준 / 'build' / tur_253d1510) for tur_253d1510 in daaray_téere}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(tënk_xëyma, ensure_ascii=False, indent=2) + '\n')
    return tënk_xëyma


def 묶기():
    tënk_xëyma = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        mboolo_xëyma = Path(임시) / 'jkoros-native-relink'
        mboolo_xëyma.mkdir()
        def mbokk_xëyma(원본, Nàttangoo_xëyma):
            jëmmukaay_xëyma = mboolo_xëyma / Nàttangoo_xëyma
            jëmmukaay_xëyma.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(jëmmukaay_xëyma), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(jëmmukaay_xëyma))
        for tur_253d1510 in jëmmukaay_tur:
            mbokk_xëyma(기준 / 'build' / (tur_253d1510 + '.o'), 'objects/' + tur_253d1510 + '.o')
        for tur_253d1510 in daaray_téere:
            mbokk_xëyma(기준 / 'build' / tur_253d1510, 'objects/' + Path(tur_253d1510).name)
        for tur_253d1510 in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'kiy_jariñoo_internet', '명명', 'masin', 'mbaal_Tegalo/mbaal_Tegalo.h', '부팅/lëkkale_Tëralin.ld',
                     'lu_soree_xëyma/assh_config.h', 'lu_soree_xëyma/config.h', 'lu_soree_xëyma/ctype.h', 'lu_soree_xëyma/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            mbokk_xëyma(기준 / tur_253d1510, tur_253d1510)
        for tur_253d1510 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            mbokk_xëyma(저장소 / tur_253d1510, tur_253d1510)
        for Yoonu_jëmale in sorted((기준 / 'vendor').glob('LICENSE*')):
            mbokk_xëyma(Yoonu_jëmale, 'vendor/' + Yoonu_jëmale.name)
        mbokk_xëyma(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        mbokk_xëyma(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        mbokk_xëyma(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        mbokk_xëyma(기준 / 'Jumtukaay_yi/재연결.py', 'relink.py')
        for Yoonu_jëmale in sorted((기준 / 'build/user').glob('*.elf')):
            mbokk_xëyma(Yoonu_jëmale, 'build/user/' + Yoonu_jëmale.name)
        for tur_253d1510 in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            mbokk_xëyma(기준 / 'build/user' / (tur_253d1510 + '.o'), 'build/user/' + tur_253d1510 + '.o')
        for tur_253d1510 in ('crt', 'aot-runtime', 'common_language_runtime_Ndimbal', 'daw', '미리번역', '되돌림'):
            mbokk_xëyma(기준 / 'build/ccompiler' / (tur_253d1510 + '.o'), 'build/ccompiler/' + tur_253d1510 + '.o')
        명세 = dict(tënk_xëyma, objects=['objects/' + tur_253d1510 + '.o' for tur_253d1510 in jëmmukaay_tur],
                    libraries=['objects/' + Path(Yoonu_jëmale).name for Yoonu_jëmale in daaray_téere])
        (mboolo_xëyma / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (mboolo_xëyma / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        luñu_name = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / luñu_name.name
        with tarfile.open(str(임시압축), 'w:gz') as denc_xëyma:
            denc_xëyma.add(str(mboolo_xëyma), arcname=mboolo_xëyma.name)
        임시압축.replace(luñu_name)
    tënk_xëyma['relink_archive_sha256'] = caabiy_teqale_bi_bara_denc(luñu_name)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(tënk_xëyma, ensure_ascii=False, indent=2) + '\n')
    return luñu_name


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    xëyma = 해석기.parse_args()
    if xëyma.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
