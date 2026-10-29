#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL pivviujuq_attavigiit·재연결 자료를 함께 묶는다."""
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
namunngarvik_atiq = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
tukisiurvik = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def 해시(aqqut):
    return hashlib.sha256(Path(aqqut).read_bytes()).hexdigest()


def 점검():
    for atiq in ('vendor/wolfssh', 'vendor/wolfssl', 'ungasittuq_atuutilik/user_settings.h'):
        if (기준 / atiq).exists():
            raise SystemExit('COSL 배포 nuqqarli: 이전 GPL ungasittuq_atuutilik 구현이 pivviujuq_attavigiit 트리에 남아 있습니다: ' + atiq)
    nukillautilik_atuutilik = (기준 / '통신망/nukillautilik_Kasuqatigiitsimajut.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in nukillautilik_atuutilik or 'SPDX-License-Identifier: GPL' in nukillautilik_atuutilik:
        raise SystemExit('COSL 배포 nuqqarli: BSD GENET 구현·고지 nalunairli_1aacb54c 필요')
    for atiq in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / atiq).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + atiq)
    심볼 = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', 심볼):
        raise SystemExit('COSL 배포 nuqqarli: 커널에 이전 GPL isirut_atuutilik/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for atiq in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + atiq + r'$', 심볼, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + atiq)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        ajjinnguaq_atuutilik = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(ajjinnguaq_atuutilik)])
        if 해시(ajjinnguaq_atuutilik) != 해시(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    unikkaaq_atuutilik = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': 해시(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {atiq: 해시(기준 / 'build' / atiq) for atiq in tukisiurvik}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(unikkaaq_atuutilik, ensure_ascii=False, indent=2) + '\n')
    return unikkaaq_atuutilik


def 묶기():
    unikkaaq_atuutilik = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        katinngajut_atuutilik = Path(임시) / 'jkoros-native-relink'
        katinngajut_atuutilik.mkdir()
        def ijjuarli_atuutilik(원본, ilagijaujuq_atuutilik):
            namunngarvik_atuutilik = katinngajut_atuutilik / ilagijaujuq_atuutilik
            namunngarvik_atuutilik.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(namunngarvik_atuutilik), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(namunngarvik_atuutilik))
        for atiq in namunngarvik_atiq:
            ijjuarli_atuutilik(기준 / 'build' / (atiq + '.o'), 'objects/' + atiq + '.o')
        for atiq in tukisiurvik:
            ijjuarli_atuutilik(기준 / 'build' / atiq, 'objects/' + Path(atiq).name)
        for atiq in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'atuqtuq', '명명', '기계', '통신망/통신망.h', '부팅/kasurvik_ilinganinga.ld',
                     'ungasittuq_atuutilik/assh_config.h', 'ungasittuq_atuutilik/config.h', 'ungasittuq_atuutilik/ctype.h', 'ungasittuq_atuutilik/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ijjuarli_atuutilik(기준 / atiq, atiq)
        for atiq in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ijjuarli_atuutilik(저장소 / atiq, atiq)
        for aqqut in sorted((기준 / 'vendor').glob('LICENSE*')):
            ijjuarli_atuutilik(aqqut, 'vendor/' + aqqut.name)
        ijjuarli_atuutilik(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ijjuarli_atuutilik(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ijjuarli_atuutilik(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ijjuarli_atuutilik(기준 / '도구/재연결.py', 'relink.py')
        for aqqut in sorted((기준 / 'build/user').glob('*.elf')):
            ijjuarli_atuutilik(aqqut, 'build/user/' + aqqut.name)
        for atiq in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ijjuarli_atuutilik(기준 / 'build/user' / (atiq + '.o'), 'build/user/' + atiq + '.o')
        for atiq in ('crt', 'aot-runtime', '실행지원', '시작', '미리번역', '되돌림'):
            ijjuarli_atuutilik(기준 / 'build/ccompiler' / (atiq + '.o'), 'build/ccompiler/' + atiq + '.o')
        명세 = dict(unikkaaq_atuutilik, objects=['objects/' + atiq + '.o' for atiq in namunngarvik_atiq],
                    libraries=['objects/' + Path(aqqut).name for aqqut in tukisiurvik])
        (katinngajut_atuutilik / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (katinngajut_atuutilik / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        turaagaq = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / turaagaq.name
        with tarfile.open(str(임시압축), 'w:gz') as tuqqurli_atuutilik_e917f8d5:
            tuqqurli_atuutilik_e917f8d5.add(str(katinngajut_atuutilik), arcname=katinngajut_atuutilik.name)
        임시압축.replace(turaagaq)
    unikkaaq_atuutilik['relink_archive_sha256'] = 해시(turaagaq)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(unikkaaq_atuutilik, ensure_ascii=False, indent=2) + '\n')
    return turaagaq


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    atuutilik = 해석기.parse_args()
    if atuutilik.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
