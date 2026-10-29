#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL سرچینه_ونه·재연결 자료를 함께 묶는다."""
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
목적이름 = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
کتابتون = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def 해시(يونلور):
    return hashlib.sha256(Path(يونلور).read_bytes()).hexdigest()


def 점검():
    for نوم in ('vendor/wolfssh', 'vendor/wolfssl', '원격/user_settings.h'):
        if (기준 / نوم).exists():
            raise SystemExit('COSL 배포 تمول: 이전 GPL 원격 구현이 سرچینه_ونه 트리에 남아 있습니다: ' + نوم)
    سیم_پیوسته_شوی_ارزښت = (기준 / '통신망/سیم_پیوسته_شوی_جال.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in سیم_پیوسته_شوی_ارزښت or 'SPDX-License-Identifier: GPL' in سیم_پیوسته_شوی_ارزښت:
        raise SystemExit('COSL 배포 تمول: BSD GENET 구현·고지 확인 필요')
    for نوم in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / نوم).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + نوم)
    심볼 = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', 심볼):
        raise SystemExit('COSL 배포 تمول: 커널에 이전 GPL تېرنويى_ارزښت/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for نوم in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + نوم + r'$', 심볼, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + نوم)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        انځور_ارزښت = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(انځور_ارزښت)])
        if 해시(انځور_ارزښت) != 해시(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    راپور_ارزښت = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': 해시(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {نوم: 해시(기준 / 'build' / نوم) for نوم in کتابتون}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(راپور_ارزښت, ensure_ascii=False, indent=2) + '\n')
    return راپور_ارزښت


def 묶기():
    راپور_ارزښت = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        ډله_ارزښت = Path(임시) / 'jkoros-native-relink'
        ډله_ارزښت.mkdir()
        def بېلګه_ارزښت_37b3d3b1(원본, جوړه_ارزښت):
            موخه_ارزښت = ډله_ارزښت / جوړه_ارزښت
            موخه_ارزښت.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(موخه_ارزښت), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(موخه_ارزښت))
        for نوم in 목적이름:
            بېلګه_ارزښت_37b3d3b1(기준 / 'build' / (نوم + '.o'), 'objects/' + نوم + '.o')
        for نوم in کتابتون:
            بېلګه_ارزښت_37b3d3b1(기준 / 'build' / نوم, 'objects/' + Path(نوم).name)
        for نوم in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'کارن', '명명', '기계', '통신망/통신망.h', '부팅/پيوند_هډوانه.ld',
                     '원격/assh_config.h', '원격/config.h', '원격/ctype.h', '원격/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            بېلګه_ارزښت_37b3d3b1(기준 / نوم, نوم)
        for نوم in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            بېلګه_ارزښت_37b3d3b1(저장소 / نوم, نوم)
        for يونلور in sorted((기준 / 'vendor').glob('LICENSE*')):
            بېلګه_ارزښت_37b3d3b1(يونلور, 'vendor/' + يونلور.name)
        بېلګه_ارزښت_37b3d3b1(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        بېلګه_ارزښت_37b3d3b1(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        بېلګه_ارزښت_37b3d3b1(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        بېلګه_ارزښت_37b3d3b1(기준 / '도구/재연결.py', 'relink.py')
        for يونلور in sorted((기준 / 'build/user').glob('*.elf')):
            بېلګه_ارزښت_37b3d3b1(يونلور, 'build/user/' + يونلور.name)
        for نوم in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            بېلګه_ارزښت_37b3d3b1(기준 / 'build/user' / (نوم + '.o'), 'build/user/' + نوم + '.o')
        for نوم in ('crt', 'aot-runtime', '실행지원', 'ځغلول', '미리번역', '되돌림'):
            بېلګه_ارزښت_37b3d3b1(기준 / 'build/ccompiler' / (نوم + '.o'), 'build/ccompiler/' + نوم + '.o')
        명세 = dict(راپور_ارزښت, objects=['objects/' + نوم + '.o' for نوم in 목적이름],
                    libraries=['objects/' + Path(يونلور).name for يونلور in کتابتون])
        (ډله_ارزښت / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (ډله_ارزښت / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        대상 = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / 대상.name
        with tarfile.open(str(임시압축), 'w:gz') as ارشیف_ارزښت:
            ارشیف_ارزښت.add(str(ډله_ارزښت), arcname=ډله_ارزښت.name)
        임시압축.replace(대상)
    راپور_ارزښت['relink_archive_sha256'] = 해시(대상)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(راپور_ارزښت, ensure_ascii=False, indent=2) + '\n')
    return 대상


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ارزښت = 해석기.parse_args()
    if ارزښت.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
