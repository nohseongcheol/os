#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL წყარო_ხე·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]
저장소 = პროეცირება_ფესვი.parents[1]
მიმართულება_სახელი = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ბიბლიოთეკა = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ჰეში_ფაილი(გეზი):
    return hashlib.sha256(Path(გეზი).read_bytes()).hexdigest()


def 점검():
    for სახელი in ('vendor/wolfssh', 'vendor/wolfssl', 'დისტანციური_მნიშვნელობა/user_settings.h'):
        if (პროეცირება_ფესვი / სახელი).exists():
            raise SystemExit('COSL 배포 შეჩერება: 이전 GPL დისტანციური_მნიშვნელობა 구현이 წყარო_ხე 트리에 남아 있습니다: ' + სახელი)
    სადენიანი_მნიშვნელობა = (პროეცირება_ფესვი / 'ქსელი_დასტა/სადენიანი_ქსელი.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in სადენიანი_მნიშვნელობა or 'SPDX-License-Identifier: GPL' in სადენიანი_მნიშვნელობა:
        raise SystemExit('COSL 배포 შეჩერება: BSD GENET 구현·고지 გადამოწმება 필요')
    for სახელი in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / სახელი).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + სახელი)
    სიმბოლო_მნიშვნელობა = subprocess.check_output(['aarch64-linux-gnu-nm', str(პროეცირება_ფესვი / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', სიმბოლო_მნიშვნელობა):
        raise SystemExit('COSL 배포 შეჩერება: 커널에 이전 GPL პაროლი_მნიშვნელობა/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for სახელი in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + სახელი + r'$', სიმბოლო_მნიშვნელობა, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + სახელი)
    with tempfile.TemporaryDirectory(dir=str(პროეცირება_ფესვი / 'build')) as 임시:
        ნახატი_მნიშვნელობა = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(პროეცირება_ფესვი / 'build/kernel.elf'), str(ნახატი_მნიშვნელობა)])
        if ჰეში_ფაილი(ნახატი_მნიშვნელობა) != ჰეში_ფაილი(პროეცირება_ფესვი / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ანგარიში_მნიშვნელობა = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ჰეში_ფაილი(პროეცირება_ფესვი / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {სახელი: ჰეში_ფაილი(პროეცირება_ფესვი / 'build' / სახელი) for სახელი in ბიბლიოთეკა}}
    (პროეცირება_ფესვი / 'build/cosl-distribution-check.json').write_text(json.dumps(ანგარიში_მნიშვნელობა, ensure_ascii=False, indent=2) + '\n')
    return ანგარიში_მნიშვნელობა


def 묶기():
    ანგარიში_მნიშვნელობა = 점검()
    배포 = პროეცირება_ფესვი / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(პროეცირება_ფესვი / 'build')) as 임시:
        ჯგუფი_მნიშვნელობა = Path(임시) / 'jkoros-native-relink'
        ჯგუფი_მნიშვნელობა.mkdir()
        def ასლი_მნიშვნელობა(원본, კვანძი_მნიშვნელობა_6a3b6fa7):
            მიმართულება_მნიშვნელობა = ჯგუფი_მნიშვნელობა / კვანძი_მნიშვნელობა_6a3b6fa7
            მიმართულება_მნიშვნელობა.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(მიმართულება_მნიშვნელობა), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(მიმართულება_მნიშვნელობა))
        for სახელი in მიმართულება_სახელი:
            ასლი_მნიშვნელობა(პროეცირება_ფესვი / 'build' / (სახელი + '.o'), 'objects/' + სახელი + '.o')
        for სახელი in ბიბლიოთეკა:
            ასლი_მნიშვნელობა(პროეცირება_ფესვი / 'build' / სახელი, 'objects/' + Path(სახელი).name)
        for სახელი in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'მომხმარებელი', '명명', 'კომპიუტერი', 'ქსელი_დასტა/ქსელი_დასტა.h', '부팅/ბმული_განლაგება.ld',
                     'დისტანციური_მნიშვნელობა/assh_config.h', 'დისტანციური_მნიშვნელობა/config.h', 'დისტანციური_მნიშვნელობა/ctype.h', 'დისტანციური_მნიშვნელობა/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ასლი_მნიშვნელობა(პროეცირება_ფესვი / სახელი, სახელი)
        for სახელი in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ასლი_მნიშვნელობა(저장소 / სახელი, სახელი)
        for გეზი in sorted((პროეცირება_ფესვი / 'vendor').glob('LICENSE*')):
            ასლი_მნიშვნელობა(გეზი, 'vendor/' + გეზი.name)
        ასლი_მნიშვნელობა(პროეცირება_ფესვი / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ასლი_მნიშვნელობა(პროეცირება_ფესვი / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ასლი_მნიშვნელობა(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ასლი_მნიშვნელობა(პროეცირება_ფესვი / 'ხელსაწყოები/재연결.py', 'relink.py')
        for გეზი in sorted((პროეცირება_ფესვი / 'build/user').glob('*.elf')):
            ასლი_მნიშვნელობა(გეზი, 'build/user/' + გეზი.name)
        for სახელი in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ასლი_მნიშვნელობა(პროეცირება_ფესვი / 'build/user' / (სახელი + '.o'), 'build/user/' + სახელი + '.o')
        for სახელი in ('crt', 'aot-runtime', 'საერთო_ენობრივი_გარემო_მხარდაჭერა', 'გაშვება', '미리번역', 'დაბრუნება_ხიდი'):
            ასლი_მნიშვნელობა(პროეცირება_ფესვი / 'build/ccompiler' / (სახელი + '.o'), 'build/ccompiler/' + სახელი + '.o')
        명세 = dict(ანგარიში_მნიშვნელობა, objects=['objects/' + სახელი + '.o' for სახელი in მიმართულება_სახელი],
                    libraries=['objects/' + Path(გეზი).name for გეზი in ბიბლიოთეკა])
        (ჯგუფი_მნიშვნელობა / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (ჯგუფი_მნიშვნელობა / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        მიზანი = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / მიზანი.name
        with tarfile.open(str(임시압축), 'w:gz') as არქივი_მნიშვნელობა:
            არქივი_მნიშვნელობა.add(str(ჯგუფი_მნიშვნელობა), arcname=ჯგუფი_მნიშვნელობა.name)
        임시압축.replace(მიზანი)
    ანგარიში_მნიშვნელობა['relink_archive_sha256'] = ჰეში_ფაილი(მიზანი)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ანგარიში_მნიშვნელობა, ensure_ascii=False, indent=2) + '\n')
    return მიზანი


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    მნიშვნელობა = 해석기.parse_args()
    if მნიშვნელობა.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
