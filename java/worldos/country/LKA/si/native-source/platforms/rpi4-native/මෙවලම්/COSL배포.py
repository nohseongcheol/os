#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL මූලය_රුක·재연결 자료를 함께 묶는다."""
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
ගමනාන්තය_නම = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ලේඛාගාරය = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def හෑෂ්_ගොනුව(මාර්_ගය):
    return hashlib.sha256(Path(මාර්_ගය).read_bytes()).hexdigest()


def 점검():
    for නම in ('vendor/wolfssh', 'vendor/wolfssl', 'දුරස්ථ_අගය/user_settings.h'):
        if (기준 / නම).exists():
            raise SystemExit('COSL 배포 නවතන්න: 이전 GPL දුරස්ථ_අගය 구현이 මූලය_රුක 트리에 남아 있습니다: ' + නම)
    පරිපථගත_අගය = (기준 / 'ජාලය_කැටිය/පරිපථගත_ජාලය.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in පරිපථගත_අගය or 'SPDX-License-Identifier: GPL' in පරිපථගත_අගය:
        raise SystemExit('COSL 배포 නවතන්න: BSD GENET 구현·고지 තහවුරු_කරන්න 필요')
    for නම in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / නම).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + නම)
    සංකේතය_අගය = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', සංකේතය_අගය):
        raise SystemExit('COSL 배포 නවතන්න: 커널에 이전 GPL මුර_පදය_අගය/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for නම in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + නම + r'$', සංකේතය_අගය, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + නම)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        අනුරුව_අගය = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(අනුරුව_අගය)])
        if හෑෂ්_ගොනුව(අනුරුව_අගය) != හෑෂ්_ගොනුව(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    වාර්තාව_අගය = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': හෑෂ්_ගොනුව(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {නම: හෑෂ්_ගොනුව(기준 / 'build' / නම) for නම in ලේඛාගාරය}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(වාර්තාව_අගය, ensure_ascii=False, indent=2) + '\n')
    return වාර්තාව_අගය


def 묶기():
    වාර්තාව_අගය = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        සමූහය_අගය = Path(임시) / 'jkoros-native-relink'
        සමූහය_අගය.mkdir()
        def ප්_රස්තාව_අගය(원본, සමානයා_අගය):
            ගමනාන්තය_අගය = සමූහය_අගය / සමානයා_අගය
            ගමනාන්තය_අගය.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ගමනාන්තය_අගය), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ගමනාන්තය_අගය))
        for නම in ගමනාන්තය_නම:
            ප්_රස්තාව_අගය(기준 / 'build' / (නම + '.o'), 'objects/' + නම + '.o')
        for නම in ලේඛාගාරය:
            ප්_රස්තාව_අගය(기준 / 'build' / නම, 'objects/' + Path(නම).name)
        for නම in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'පරිශීලක', '명명', 'යන්ත්_රය', 'ජාලය_කැටිය/ජාලය_කැටිය.h', '부팅/සබැඳිය_සැකැස්ම.ld',
                     'දුරස්ථ_අගය/assh_config.h', 'දුරස්ථ_අගය/config.h', 'දුරස්ථ_අගය/ctype.h', 'දුරස්ථ_අගය/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ප්_රස්තාව_අගය(기준 / නම, නම)
        for නම in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ප්_රස්තාව_අගය(저장소 / නම, නම)
        for මාර්_ගය in sorted((기준 / 'vendor').glob('LICENSE*')):
            ප්_රස්තාව_අගය(මාර්_ගය, 'vendor/' + මාර්_ගය.name)
        ප්_රස්තාව_අගය(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ප්_රස්තාව_අගය(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ප්_රස්තාව_අගය(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ප්_රස්තාව_අගය(기준 / 'මෙවලම්/재연결.py', 'relink.py')
        for මාර්_ගය in sorted((기준 / 'build/user').glob('*.elf')):
            ප්_රස්තාව_අගය(මාර්_ගය, 'build/user/' + මාර්_ගය.name)
        for නම in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ප්_රස්තාව_අගය(기준 / 'build/user' / (නම + '.o'), 'build/user/' + නම + '.o')
        for නම in ('crt', 'aot-runtime', 'පොදු_භාෂා_ධාවන_කාලය_සහාය', 'ක්_රියාත්මක_කරන්න_2', '미리번역', '되돌림'):
            ප්_රස්තාව_අගය(기준 / 'build/ccompiler' / (නම + '.o'), 'build/ccompiler/' + නම + '.o')
        명세 = dict(වාර්තාව_අගය, objects=['objects/' + නම + '.o' for නම in ගමනාන්තය_නම],
                    libraries=['objects/' + Path(මාර්_ගය).name for මාර්_ගය in ලේඛාගාරය])
        (සමූහය_අගය / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (සමූහය_අගය / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        ඉලක්කය = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ඉලක්කය.name
        with tarfile.open(str(임시압축), 'w:gz') as සංරක්ෂිතය_අගය:
            සංරක්ෂිතය_අගය.add(str(සමූහය_අගය), arcname=සමූහය_අගය.name)
        임시압축.replace(ඉලක්කය)
    වාර්තාව_අගය['relink_archive_sha256'] = හෑෂ්_ගොනුව(ඉලක්කය)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(වාර්තාව_අගය, ensure_ascii=False, indent=2) + '\n')
    return ඉලක්කය


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    අගය = 해석기.parse_args()
    if අගය.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
