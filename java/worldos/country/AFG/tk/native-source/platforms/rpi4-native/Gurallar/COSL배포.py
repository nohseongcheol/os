#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL gor_agaç·재연결 자료를 함께 묶는다."""
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
barylmaly_ýer_at = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
Kitaphana = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def heş_kody_faýl(Ýol):
    return hashlib.sha256(Path(Ýol).read_bytes()).hexdigest()


def 점검():
    for Ad in ('vendor/wolfssh', 'vendor/wolfssl', 'uzakdan_baha/user_settings.h'):
        if (기준 / Ad).exists():
            raise SystemExit('COSL 배포 Dur: 이전 GPL uzakdan_baha 구현이 gor_agaç 트리에 남아 있습니다: ' + Ad)
    simli_baha = (기준 / 'Tor_Desse/simli_Tor.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in simli_baha or 'SPDX-License-Identifier: GPL' in simli_baha:
        raise SystemExit('COSL 배포 Dur: BSD GENET 구현·고지 barla 필요')
    for Ad in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Ad).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Ad)
    nyşan_baha = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', nyşan_baha):
        raise SystemExit('COSL 배포 Dur: 커널에 이전 GPL parol_baha/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Ad in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Ad + r'$', nyşan_baha, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Ad)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        surat_baha = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(surat_baha)])
        if heş_kody_faýl(surat_baha) != heş_kody_faýl(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    hasabat_baha = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': heş_kody_faýl(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Ad: heş_kody_faýl(기준 / 'build' / Ad) for Ad in Kitaphana}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(hasabat_baha, ensure_ascii=False, indent=2) + '\n')
    return hasabat_baha


def 묶기():
    hasabat_baha = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        topar_baha = Path(임시) / 'jkoros-native-relink'
        topar_baha.mkdir()
        def synp_baha(원본, deň_derejeli_düwün_baha):
            barylmaly_ýer_baha = topar_baha / deň_derejeli_düwün_baha
            barylmaly_ýer_baha.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(barylmaly_ýer_baha), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(barylmaly_ýer_baha))
        for Ad in barylmaly_ýer_at:
            synp_baha(기준 / 'build' / (Ad + '.o'), 'objects/' + Ad + '.o')
        for Ad in Kitaphana:
            synp_baha(기준 / 'build' / Ad, 'objects/' + Path(Ad).name)
        for Ad in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ulanyjy', '명명', 'kompýuter', 'Tor_Desse/Tor_Desse.h', '부팅/Bag_Ýerleşiş.ld',
                     'uzakdan_baha/assh_config.h', 'uzakdan_baha/config.h', 'uzakdan_baha/ctype.h', 'uzakdan_baha/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            synp_baha(기준 / Ad, Ad)
        for Ad in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            synp_baha(저장소 / Ad, Ad)
        for Ýol in sorted((기준 / 'vendor').glob('LICENSE*')):
            synp_baha(Ýol, 'vendor/' + Ýol.name)
        synp_baha(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        synp_baha(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        synp_baha(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        synp_baha(기준 / 'Gurallar/재연결.py', 'relink.py')
        for Ýol in sorted((기준 / 'build/user').glob('*.elf')):
            synp_baha(Ýol, 'build/user/' + Ýol.name)
        for Ad in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            synp_baha(기준 / 'build/user' / (Ad + '.o'), 'build/user/' + Ad + '.o')
        for Ad in ('crt', 'aot-runtime', 'umumy_dil_işlediş_gurşawy_Goldaw', 'Bitir', '미리번역', '되돌림'):
            synp_baha(기준 / 'build/ccompiler' / (Ad + '.o'), 'build/ccompiler/' + Ad + '.o')
        명세 = dict(hasabat_baha, objects=['objects/' + Ad + '.o' for Ad in barylmaly_ýer_at],
                    libraries=['objects/' + Path(Ýol).name for Ýol in Kitaphana])
        (topar_baha / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (topar_baha / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        niýet = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / niýet.name
        with tarfile.open(str(임시압축), 'w:gz') as Arhiw_baha:
            Arhiw_baha.add(str(topar_baha), arcname=topar_baha.name)
        임시압축.replace(niýet)
    hasabat_baha['relink_archive_sha256'] = heş_kody_faýl(niýet)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(hasabat_baha, ensure_ascii=False, indent=2) + '\n')
    return niýet


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    baha = 해석기.parse_args()
    if baha.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
