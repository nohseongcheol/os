#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL orísun_ètò_afigijúwe·재연결 자료를 함께 묶는다."""
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
èbúté_orúkọ = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ibi_ìpamọ́ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def burú_fáìlì(ọ̀nà):
    return hashlib.sha256(Path(ọ̀nà).read_bytes()).hexdigest()


def 점검():
    for Orúkọ in ('vendor/wolfssh', 'vendor/wolfssl', 'Ìjìnnà_iye/user_settings.h'):
        if (기준 / Orúkọ).exists():
            raise SystemExit('COSL 배포 Dúró: 이전 GPL Ìjìnnà_iye 구현이 orísun_ètò_afigijúwe 트리에 남아 있습니다: ' + Orúkọ)
    aláfiwáyàsopọ̀_iye = (기준 / 'Alásopọ̀_kójọ/aláfiwáyàsopọ̀_Alásopọ̀.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in aláfiwáyàsopọ̀_iye or 'SPDX-License-Identifier: GPL' in aláfiwáyàsopọ̀_iye:
        raise SystemExit('COSL 배포 Dúró: BSD GENET 구현·고지 ridájú 필요')
    for Orúkọ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Orúkọ).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Orúkọ)
    àmì_iye = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', àmì_iye):
        raise SystemExit('COSL 배포 Dúró: 커널에 이전 GPL ọ̀rọ̀_aṣínà_iye/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Orúkọ in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Orúkọ + r'$', àmì_iye, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Orúkọ)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        àwòrán_iye = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(àwòrán_iye)])
        if burú_fáìlì(àwòrán_iye) != burú_fáìlì(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ìjábọ̀_iye = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': burú_fáìlì(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Orúkọ: burú_fáìlì(기준 / 'build' / Orúkọ) for Orúkọ in ibi_ìpamọ́}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(ìjábọ̀_iye, ensure_ascii=False, indent=2) + '\n')
    return ìjábọ̀_iye


def 묶기():
    ìjábọ̀_iye = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        Àjọṣe_iye = Path(임시) / 'jkoros-native-relink'
        Àjọṣe_iye.mkdir()
        def ṣẹ̀dà_iye(원본, ọ̀gbà_iye):
            èbúté_iye = Àjọṣe_iye / ọ̀gbà_iye
            èbúté_iye.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(èbúté_iye), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(èbúté_iye))
        for Orúkọ in èbúté_orúkọ:
            ṣẹ̀dà_iye(기준 / 'build' / (Orúkọ + '.o'), 'objects/' + Orúkọ + '.o')
        for Orúkọ in ibi_ìpamọ́:
            ṣẹ̀dà_iye(기준 / 'build' / Orúkọ, 'objects/' + Path(Orúkọ).name)
        for Orúkọ in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'aṣàmúlò', '명명', 'maṣíìnì', 'Alásopọ̀_kójọ/Alásopọ̀_kójọ.h', '부팅/ṣàsopọ̀_ètò_ìrísí.ld',
                     'Ìjìnnà_iye/assh_config.h', 'Ìjìnnà_iye/config.h', 'Ìjìnnà_iye/ctype.h', 'Ìjìnnà_iye/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ṣẹ̀dà_iye(기준 / Orúkọ, Orúkọ)
        for Orúkọ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ṣẹ̀dà_iye(저장소 / Orúkọ, Orúkọ)
        for ọ̀nà in sorted((기준 / 'vendor').glob('LICENSE*')):
            ṣẹ̀dà_iye(ọ̀nà, 'vendor/' + ọ̀nà.name)
        ṣẹ̀dà_iye(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ṣẹ̀dà_iye(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ṣẹ̀dà_iye(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ṣẹ̀dà_iye(기준 / 'Àwọn_irinṣẹ́/재연결.py', 'relink.py')
        for ọ̀nà in sorted((기준 / 'build/user').glob('*.elf')):
            ṣẹ̀dà_iye(ọ̀nà, 'build/user/' + ọ̀nà.name)
        for Orúkọ in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ṣẹ̀dà_iye(기준 / 'build/user' / (Orúkọ + '.o'), 'build/user/' + Orúkọ + '.o')
        for Orúkọ in ('crt', 'aot-runtime', 'àkókò_iṣẹ́_èdè_tówọ́pọ̀_àtìlẹ́yìn', 'Rọ́ọ̀nù', '미리번역', '되돌림'):
            ṣẹ̀dà_iye(기준 / 'build/ccompiler' / (Orúkọ + '.o'), 'build/ccompiler/' + Orúkọ + '.o')
        명세 = dict(ìjábọ̀_iye, objects=['objects/' + Orúkọ + '.o' for Orúkọ in èbúté_orúkọ],
                    libraries=['objects/' + Path(ọ̀nà).name for ọ̀nà in ibi_ìpamọ́])
        (Àjọṣe_iye / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Àjọṣe_iye / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        àfojúsùn = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / àfojúsùn.name
        with tarfile.open(str(임시압축), 'w:gz') as Ìpamọ_ọlọ́jọ́pípẹ́_iye:
            Ìpamọ_ọlọ́jọ́pípẹ́_iye.add(str(Àjọṣe_iye), arcname=Àjọṣe_iye.name)
        임시압축.replace(àfojúsùn)
    ìjábọ̀_iye['relink_archive_sha256'] = burú_fáìlì(àfojúsùn)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ìjábọ̀_iye, ensure_ascii=False, indent=2) + '\n')
    return àfojúsùn


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    iye = 해석기.parse_args()
    if iye.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
