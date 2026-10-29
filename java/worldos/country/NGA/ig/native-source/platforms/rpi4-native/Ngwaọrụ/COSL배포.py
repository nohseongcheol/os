#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ebensìbịa_èsèrèsè_osisi·재연결 자료를 함께 묶는다."""
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
ebemwèga_akara_ahà = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ọbaakwụkwọ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def di_ike_ọbọakwụkwọ(ụzọ_ozi):
    return hashlib.sha256(Path(ụzọ_ozi).read_bytes()).hexdigest()


def 점검():
    for Aha in ('vendor/wolfssh', 'vendor/wolfssl', 'ebe_dị̀anyā_valuu/user_settings.h'):
        if (기준 / Aha).exists():
            raise SystemExit('COSL 배포 Kwụsị: 이전 GPL ebe_dị̀anyā_valuu 구현이 ebensìbịa_èsèrèsè_osisi 트리에 남아 있습니다: ' + Aha)
    èjìrìwayàrụ_valuu = (기준 / 'Netwọọkụ_ikpo/èjìrìwayàrụ_Netwọọkụ.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in èjìrìwayàrụ_valuu or 'SPDX-License-Identifier: GPL' in èjìrìwayàrụ_valuu:
        raise SystemExit('COSL 배포 Kwụsị: BSD GENET 구현·고지 nkwàdo_eziokwū 필요')
    for Aha in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Aha).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Aha)
    adimara_valuu = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', adimara_valuu):
        raise SystemExit('COSL 배포 Kwụsị: 커널에 이전 GPL okwuntughe_valuu/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Aha in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Aha + r'$', adimara_valuu, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Aha)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        foto_valuu = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(foto_valuu)])
        if di_ike_ọbọakwụkwọ(foto_valuu) != di_ike_ọbọakwụkwọ(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    akụkọ_valuu = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': di_ike_ọbọakwụkwọ(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Aha: di_ike_ọbọakwụkwọ(기준 / 'build' / Aha) for Aha in ọbaakwụkwọ}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(akụkọ_valuu, ensure_ascii=False, indent=2) + '\n')
    return akụkọ_valuu


def 묶기():
    akụkọ_valuu = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        otu_valuu = Path(임시) / 'jkoros-native-relink'
        otu_valuu.mkdir()
        def ṅomie_valuu(원본, ibè_valuu):
            ebemwèga_valuu = otu_valuu / ibè_valuu
            ebemwèga_valuu.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ebemwèga_valuu), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ebemwèga_valuu))
        for Aha in ebemwèga_akara_ahà:
            ṅomie_valuu(기준 / 'build' / (Aha + '.o'), 'objects/' + Aha + '.o')
        for Aha in ọbaakwụkwọ:
            ṅomie_valuu(기준 / 'build' / Aha, 'objects/' + Path(Aha).name)
        for Aha in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'òjìàrụ', '명명', 'ngwa_komputa', 'Netwọọkụ_ikpo/Netwọọkụ_ikpo.h', '부팅/Njikọ_Nhàzi.ld',
                     'ebe_dị̀anyā_valuu/assh_config.h', 'ebe_dị̀anyā_valuu/config.h', 'ebe_dị̀anyā_valuu/ctype.h', 'ebe_dị̀anyā_valuu/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ṅomie_valuu(기준 / Aha, Aha)
        for Aha in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ṅomie_valuu(저장소 / Aha, Aha)
        for ụzọ_ozi in sorted((기준 / 'vendor').glob('LICENSE*')):
            ṅomie_valuu(ụzọ_ozi, 'vendor/' + ụzọ_ozi.name)
        ṅomie_valuu(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ṅomie_valuu(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ṅomie_valuu(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ṅomie_valuu(기준 / 'Ngwaọrụ/재연결.py', 'relink.py')
        for ụzọ_ozi in sorted((기준 / 'build/user').glob('*.elf')):
            ṅomie_valuu(ụzọ_ozi, 'build/user/' + ụzọ_ozi.name)
        for Aha in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ṅomie_valuu(기준 / 'build/user' / (Aha + '.o'), 'build/user/' + Aha + '.o')
        for Aha in ('crt', 'aot-runtime', 'ọgịga_oge_otu_asụsụ_nkwado', 'Bido', '미리번역', '되돌림'):
            ṅomie_valuu(기준 / 'build/ccompiler' / (Aha + '.o'), 'build/ccompiler/' + Aha + '.o')
        명세 = dict(akụkọ_valuu, objects=['objects/' + Aha + '.o' for Aha in ebemwèga_akara_ahà],
                    libraries=['objects/' + Path(ụzọ_ozi).name for ụzọ_ozi in ọbaakwụkwọ])
        (otu_valuu / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (otu_valuu / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        ebenlereanya = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ebenlereanya.name
        with tarfile.open(str(임시압축), 'w:gz') as ọkpụ_valuu:
            ọkpụ_valuu.add(str(otu_valuu), arcname=otu_valuu.name)
        임시압축.replace(ebenlereanya)
    akụkọ_valuu['relink_archive_sha256'] = di_ike_ọbọakwụkwọ(ebenlereanya)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(akụkọ_valuu, ensure_ascii=False, indent=2) + '\n')
    return ebenlereanya


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    valuu = 해석기.parse_args()
    if valuu.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
