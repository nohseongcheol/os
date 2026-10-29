#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL مەنبە_دەرەخ·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]
저장소 = كۆرسىتىش_يىلتىز.parents[1]
نىشان_نامى = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ئامبار = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def چاچما_ھۆججەت(يول):
    return hashlib.sha256(Path(يول).read_bytes()).hexdigest()


def 점검():
    for ئاتى in ('vendor/wolfssh', 'vendor/wolfssl', 'يىراق_قىممىتى/user_settings.h'):
        if (كۆرسىتىش_يىلتىز / ئاتى).exists():
            raise SystemExit('COSL 배포 توختا: 이전 GPL يىراق_قىممىتى 구현이 مەنبە_دەرەخ 트리에 남아 있습니다: ' + ئاتى)
    유선 = (كۆرسىتىش_يىلتىز / 'تور_دۆۋە/유선망.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in 유선 or 'SPDX-License-Identifier: GPL' in 유선:
        raise SystemExit('COSL 배포 توختا: BSD GENET 구현·고지 دەلىللىمەك 필요')
    for ئاتى in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / ئاتى).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + ئاتى)
    بەلگە_قىممىتى = subprocess.check_output(['aarch64-linux-gnu-nm', str(كۆرسىتىش_يىلتىز / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', بەلگە_قىممىتى):
        raise SystemExit('COSL 배포 توختا: 커널에 이전 GPL پارول_قىممىتى/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for ئاتى in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + ئاتى + r'$', بەلگە_قىممىتى, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + ئاتى)
    with tempfile.TemporaryDirectory(dir=str(كۆرسىتىش_يىلتىز / 'build')) as 임시:
        رەسىم_قىممىتى = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(كۆرسىتىش_يىلتىز / 'build/kernel.elf'), str(رەسىم_قىممىتى)])
        if چاچما_ھۆججەت(رەسىم_قىممىتى) != چاچما_ھۆججەت(كۆرسىتىش_يىلتىز / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    خەۋەر_قىممىتى = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': چاچما_ھۆججەت(كۆرسىتىش_يىلتىز / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {ئاتى: چاچما_ھۆججەت(كۆرسىتىش_يىلتىز / 'build' / ئاتى) for ئاتى in ئامبار}}
    (كۆرسىتىش_يىلتىز / 'build/cosl-distribution-check.json').write_text(json.dumps(خەۋەر_قىممىتى, ensure_ascii=False, indent=2) + '\n')
    return خەۋەر_قىممىتى


def 묶기():
    خەۋەر_قىممىتى = 점검()
    배포 = كۆرسىتىش_يىلتىز / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(كۆرسىتىش_يىلتىز / 'build')) as 임시:
        توپ_قىممىتى = Path(임시) / 'jkoros-native-relink'
        توپ_قىممىتى.mkdir()
        def مىسال_قىممىتى(원본, باراۋەرلىك_قىممىتى):
            نىشان_قىممىتى = توپ_قىممىتى / باراۋەرلىك_قىممىتى
            نىشان_قىممىتى.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(نىشان_قىممىتى), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(نىشان_قىممىتى))
        for ئاتى in نىشان_نامى:
            مىسال_قىممىتى(كۆرسىتىش_يىلتىز / 'build' / (ئاتى + '.o'), 'objects/' + ئاتى + '.o')
        for ئاتى in ئامبار:
            مىسال_قىممىتى(كۆرسىتىش_يىلتىز / 'build' / ئاتى, 'objects/' + Path(ئاتى).name)
        for ئاتى in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ئىشلەتكۈچى', '명명', 'ماشىنا', 'تور_دۆۋە/تور_دۆۋە.h', '부팅/ئۇلانما_لايىھە.ld',
                     'يىراق_قىممىتى/assh_config.h', 'يىراق_قىممىتى/config.h', 'يىراق_قىممىتى/ctype.h', 'يىراق_قىممىتى/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            مىسال_قىممىتى(كۆرسىتىش_يىلتىز / ئاتى, ئاتى)
        for ئاتى in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            مىسال_قىممىتى(저장소 / ئاتى, ئاتى)
        for يول in sorted((كۆرسىتىش_يىلتىز / 'vendor').glob('LICENSE*')):
            مىسال_قىممىتى(يول, 'vendor/' + يول.name)
        مىسال_قىممىتى(كۆرسىتىش_يىلتىز / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        مىسال_قىممىتى(كۆرسىتىش_يىلتىز / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        مىسال_قىممىتى(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        مىسال_قىممىتى(كۆرسىتىش_يىلتىز / 'قوراللار/재연결.py', 'relink.py')
        for يول in sorted((كۆرسىتىش_يىلتىز / 'build/user').glob('*.elf')):
            مىسال_قىممىتى(يول, 'build/user/' + يول.name)
        for ئاتى in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            مىسال_قىممىتى(كۆرسىتىش_يىلتىز / 'build/user' / (ئاتى + '.o'), 'build/user/' + ئاتى + '.o')
        for ئاتى in ('crt', 'aot-runtime', 'ئورتاق_تىل_ئىجرا_ۋاقتى_قوللاش', 'ئىجرا_قىل_2', '미리번역', 'قايتۇرۇپ_بېرىش_كۆۋرۈك'):
            مىسال_قىممىتى(كۆرسىتىش_يىلتىز / 'build/ccompiler' / (ئاتى + '.o'), 'build/ccompiler/' + ئاتى + '.o')
        명세 = dict(خەۋەر_قىممىتى, objects=['objects/' + ئاتى + '.o' for ئاتى in نىشان_نامى],
                    libraries=['objects/' + Path(يول).name for يول in ئامبار])
        (توپ_قىممىتى / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (توپ_قىممىتى / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        نىشان = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / نىشان.name
        with tarfile.open(str(임시압축), 'w:gz') as ئارخىپ_قىممىتى:
            ئارخىپ_قىممىتى.add(str(توپ_قىممىتى), arcname=توپ_قىممىتى.name)
        임시압축.replace(نىشان)
    خەۋەر_قىممىتى['relink_archive_sha256'] = چاچما_ھۆججەت(نىشان)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(خەۋەر_قىممىتى, ensure_ascii=False, indent=2) + '\n')
    return نىشان


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    قىممىتى = 해석기.parse_args()
    if قىممىتى.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
