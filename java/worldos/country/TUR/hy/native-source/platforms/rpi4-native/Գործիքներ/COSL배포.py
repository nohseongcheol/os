#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL աղբյուր_ծառ·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

արձակել_արմատ = Path(__file__).resolve().parents[1]
저장소 = արձակել_արմատ.parents[1]
նպատակակետ_անուն = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
դարան = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def պատահական_տվյալներ_նիշք(Ճանապարհ):
    return hashlib.sha256(Path(Ճանապարհ).read_bytes()).hexdigest()


def 점검():
    for Անուն in ('vendor/wolfssh', 'vendor/wolfssl', 'հեռակա_արժեք/user_settings.h'):
        if (արձակել_արմատ / Անուն).exists():
            raise SystemExit('COSL 배포 Կանգառ: 이전 GPL հեռակա_արժեք 구현이 աղբյուր_ծառ 트리에 남아 있습니다: ' + Անուն)
    լարային_արժեք = (արձակել_արմատ / 'Ցանց_Շեղջ/լարային_Ցանց.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in լարային_արժեք or 'SPDX-License-Identifier: GPL' in լարային_արժեք:
        raise SystemExit('COSL 배포 Կանգառ: BSD GENET 구현·고지 հաստատել 필요')
    for Անուն in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Անուն).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Անուն)
    նշան_արժեք = subprocess.check_output(['aarch64-linux-gnu-nm', str(արձակել_արմատ / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', նշան_արժեք):
        raise SystemExit('COSL 배포 Կանգառ: 커널에 이전 GPL գաղտնաբառ_արժեք/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Անուն in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Անուն + r'$', նշան_արժեք, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Անուն)
    with tempfile.TemporaryDirectory(dir=str(արձակել_արմատ / 'build')) as 임시:
        նկար_արժեք = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(արձակել_արմատ / 'build/kernel.elf'), str(նկար_արժեք)])
        if պատահական_տվյալներ_նիշք(նկար_արժեք) != պատահական_տվյալներ_նիշք(արձակել_արմատ / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    զեկույց_արժեք = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': պատահական_տվյալներ_նիշք(արձակել_արմատ / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Անուն: պատահական_տվյալներ_նիշք(արձակել_արմատ / 'build' / Անուն) for Անուն in դարան}}
    (արձակել_արմատ / 'build/cosl-distribution-check.json').write_text(json.dumps(զեկույց_արժեք, ensure_ascii=False, indent=2) + '\n')
    return զեկույց_արժեք


def 묶기():
    զեկույց_արժեք = 점검()
    배포 = արձակել_արմատ / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(արձակել_արմատ / 'build')) as 임시:
        խումբ_արժեք = Path(임시) / 'jkoros-native-relink'
        խումբ_արժեք.mkdir()
        def պատճեն_արժեք(원본, հավասարազոր_սարք_արժեք):
            նպատակակետ_արժեք = խումբ_արժեք / հավասարազոր_սարք_արժեք
            նպատակակետ_արժեք.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(նպատակակետ_արժեք), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(նպատակակետ_արժեք))
        for Անուն in նպատակակետ_անուն:
            պատճեն_արժեք(արձակել_արմատ / 'build' / (Անուն + '.o'), 'objects/' + Անուն + '.o')
        for Անուն in դարան:
            պատճեն_արժեք(արձակել_արմատ / 'build' / Անուն, 'objects/' + Path(Անուն).name)
        for Անուն in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'օգտվող', '명명', 'մեքենա', 'Ցանց_Շեղջ/Ցանց_Շեղջ.h', '부팅/կապ_Դասավորություն.ld',
                     'հեռակա_արժեք/assh_config.h', 'հեռակա_արժեք/config.h', 'հեռակա_արժեք/ctype.h', 'հեռակա_արժեք/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            պատճեն_արժեք(արձակել_արմատ / Անուն, Անուն)
        for Անուն in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            պատճեն_արժեք(저장소 / Անուն, Անուն)
        for Ճանապարհ in sorted((արձակել_արմատ / 'vendor').glob('LICENSE*')):
            պատճեն_արժեք(Ճանապարհ, 'vendor/' + Ճանապարհ.name)
        պատճեն_արժեք(արձակել_արմատ / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        պատճեն_արժեք(արձակել_արմատ / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        պատճեն_արժեք(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        պատճեն_արժեք(արձակել_արմատ / 'Գործիքներ/재연결.py', 'relink.py')
        for Ճանապարհ in sorted((արձակել_արմատ / 'build/user').glob('*.elf')):
            պատճեն_արժեք(Ճանապարհ, 'build/user/' + Ճանապարհ.name)
        for Անուն in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            պատճեն_արժեք(արձակել_արմատ / 'build/user' / (Անուն + '.o'), 'build/user/' + Անուն + '.o')
        for Անուն in ('crt', 'aot-runtime', 'սովորական_լեզվի_աշխատաժամանակ_Աջակցում', 'Գործարկել', '미리번역', 'վերադարձնել_կամուրջ'):
            պատճեն_արժեք(արձակել_արմատ / 'build/ccompiler' / (Անուն + '.o'), 'build/ccompiler/' + Անուն + '.o')
        명세 = dict(զեկույց_արժեք, objects=['objects/' + Անուն + '.o' for Անուն in նպատակակետ_անուն],
                    libraries=['objects/' + Path(Ճանապարհ).name for Ճանապարհ in դարան])
        (խումբ_արժեք / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (խումբ_արժեք / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        թիրախ = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / թիրախ.name
        with tarfile.open(str(임시압축), 'w:gz') as Պահոց_արժեք:
            Պահոց_արժեք.add(str(խումբ_արժեք), arcname=խումբ_արժեք.name)
        임시압축.replace(թիրախ)
    զեկույց_արժեք['relink_archive_sha256'] = պատահական_տվյալներ_նիշք(թիրախ)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(զեկույց_արժեք, ensure_ascii=False, indent=2) + '\n')
    return թիրախ


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    արժեք = 해석기.parse_args()
    if արժեք.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
