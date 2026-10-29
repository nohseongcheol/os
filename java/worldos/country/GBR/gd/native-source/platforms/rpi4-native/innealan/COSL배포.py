#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL tùs_craobh·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

tilg_freumh = Path(__file__).resolve().parents[1]
저장소 = tilg_freumh.parents[1]
ceann_uidhe_ainm = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
leabhar_lann = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hais_faidhle(Slighe):
    return hashlib.sha256(Path(Slighe).read_bytes()).hexdigest()


def 점검():
    for Ainm in ('vendor/wolfssh', 'vendor/wolfssl', 'cian_VALUE/user_settings.h'):
        if (tilg_freumh / Ainm).exists():
            raise SystemExit('COSL 배포 Stad: 이전 GPL cian_VALUE 구현이 tùs_craobh 트리에 남아 있습니다: ' + Ainm)
    유선 = (tilg_freumh / 'lìonra_stac/유선망.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in 유선 or 'SPDX-License-Identifier: GPL' in 유선:
        raise SystemExit('COSL 배포 Stad: BSD GENET 구현·고지 dearbh 필요')
    for Ainm in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Ainm).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Ainm)
    samhla_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(tilg_freumh / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', samhla_VALUE):
        raise SystemExit('COSL 배포 Stad: 커널에 이전 GPL facal_faire_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Ainm in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Ainm + r'$', samhla_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Ainm)
    with tempfile.TemporaryDirectory(dir=str(tilg_freumh / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(tilg_freumh / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if hais_faidhle(IMAGE_VALUE) != hais_faidhle(tilg_freumh / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    aithisg_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hais_faidhle(tilg_freumh / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Ainm: hais_faidhle(tilg_freumh / 'build' / Ainm) for Ainm in leabhar_lann}}
    (tilg_freumh / 'build/cosl-distribution-check.json').write_text(json.dumps(aithisg_VALUE, ensure_ascii=False, indent=2) + '\n')
    return aithisg_VALUE


def 묶기():
    aithisg_VALUE = 점검()
    배포 = tilg_freumh / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(tilg_freumh / 'build')) as 임시:
        buidheann_VALUE = Path(임시) / 'jkoros-native-relink'
        buidheann_VALUE.mkdir()
        def ionstans_VALUE(원본, seise_VALUE):
            ceann_uidhe_VALUE = buidheann_VALUE / seise_VALUE
            ceann_uidhe_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ceann_uidhe_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ceann_uidhe_VALUE))
        for Ainm in ceann_uidhe_ainm:
            ionstans_VALUE(tilg_freumh / 'build' / (Ainm + '.o'), 'objects/' + Ainm + '.o')
        for Ainm in leabhar_lann:
            ionstans_VALUE(tilg_freumh / 'build' / Ainm, 'objects/' + Path(Ainm).name)
        for Ainm in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'cleachdaiche', '명명', 'inneal', 'lìonra_stac/lìonra_stac.h', '부팅/ceangal_co_dhealbhachd.ld',
                     'cian_VALUE/assh_config.h', 'cian_VALUE/config.h', 'cian_VALUE/ctype.h', 'cian_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ionstans_VALUE(tilg_freumh / Ainm, Ainm)
        for Ainm in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ionstans_VALUE(저장소 / Ainm, Ainm)
        for Slighe in sorted((tilg_freumh / 'vendor').glob('LICENSE*')):
            ionstans_VALUE(Slighe, 'vendor/' + Slighe.name)
        ionstans_VALUE(tilg_freumh / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ionstans_VALUE(tilg_freumh / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ionstans_VALUE(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ionstans_VALUE(tilg_freumh / 'innealan/재연결.py', 'relink.py')
        for Slighe in sorted((tilg_freumh / 'build/user').glob('*.elf')):
            ionstans_VALUE(Slighe, 'build/user/' + Slighe.name)
        for Ainm in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ionstans_VALUE(tilg_freumh / 'build/user' / (Ainm + '.o'), 'build/user/' + Ainm + '.o')
        for Ainm in ('crt', 'aot-runtime', 'Common_Language_Runtime_taic', 'ruith', '미리번역', 'return_drochaid'):
            ionstans_VALUE(tilg_freumh / 'build/ccompiler' / (Ainm + '.o'), 'build/ccompiler/' + Ainm + '.o')
        명세 = dict(aithisg_VALUE, objects=['objects/' + Ainm + '.o' for Ainm in ceann_uidhe_ainm],
                    libraries=['objects/' + Path(Slighe).name for Slighe in leabhar_lann])
        (buidheann_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (buidheann_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        targaid = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / targaid.name
        with tarfile.open(str(임시압축), 'w:gz') as taisg_VALUE:
            taisg_VALUE.add(str(buidheann_VALUE), arcname=buidheann_VALUE.name)
        임시압축.replace(targaid)
    aithisg_VALUE['relink_archive_sha256'] = hais_faidhle(targaid)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(aithisg_VALUE, ensure_ascii=False, indent=2) + '\n')
    return targaid


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = 해석기.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
