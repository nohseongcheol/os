#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL umthombo_isihlahla·재연결 자료를 함께 묶는다."""
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
isikhumulo_igama = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
umtapo = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def i_hash_ifayela(Indlela_2):
    return hashlib.sha256(Path(Indlela_2).read_bytes()).hexdigest()


def 점검():
    for Igama in ('vendor/wolfssh', 'vendor/wolfssl', 'kude_inani/user_settings.h'):
        if (기준 / Igama).exists():
            raise SystemExit('COSL 배포 Ima: 이전 GPL kude_inani 구현이 umthombo_isihlahla 트리에 남아 있습니다: ' + Igama)
    kunezintambo_inani = (기준 / 'iNethiwekhi_Isitaki/kunezintambo_iNethiwekhi.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in kunezintambo_inani or 'SPDX-License-Identifier: GPL' in kunezintambo_inani:
        raise SystemExit('COSL 배포 Ima: BSD GENET 구현·고지 qiniseka 필요')
    for Igama in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Igama).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Igama)
    uphawu_inani = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', uphawu_inani):
        raise SystemExit('COSL 배포 Ima: 커널에 이전 GPL iphasiwedi_inani/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Igama in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Igama + r'$', uphawu_inani, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Igama)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        isithombe_inani = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(isithombe_inani)])
        if i_hash_ifayela(isithombe_inani) != i_hash_ifayela(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    umbiko_inani = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': i_hash_ifayela(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Igama: i_hash_ifayela(기준 / 'build' / Igama) for Igama in umtapo}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(umbiko_inani, ensure_ascii=False, indent=2) + '\n')
    return umbiko_inani


def 묶기():
    umbiko_inani = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        iqoqo_inani = Path(임시) / 'jkoros-native-relink'
        iqoqo_inani.mkdir()
        def kopisha_inani(원본, untanga_inani):
            isikhumulo_inani = iqoqo_inani / untanga_inani
            isikhumulo_inani.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(isikhumulo_inani), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(isikhumulo_inani))
        for Igama in isikhumulo_igama:
            kopisha_inani(기준 / 'build' / (Igama + '.o'), 'objects/' + Igama + '.o')
        for Igama in umtapo:
            kopisha_inani(기준 / 'build' / Igama, 'objects/' + Path(Igama).name)
        for Igama in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'umsebenzisi', '명명', 'umshini', 'iNethiwekhi_Isitaki/iNethiwekhi_Isitaki.h', '부팅/xhuma_I_layout.ld',
                     'kude_inani/assh_config.h', 'kude_inani/config.h', 'kude_inani/ctype.h', 'kude_inani/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopisha_inani(기준 / Igama, Igama)
        for Igama in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopisha_inani(저장소 / Igama, Igama)
        for Indlela_2 in sorted((기준 / 'vendor').glob('LICENSE*')):
            kopisha_inani(Indlela_2, 'vendor/' + Indlela_2.name)
        kopisha_inani(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopisha_inani(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopisha_inani(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopisha_inani(기준 / 'Amathuluzi/재연결.py', 'relink.py')
        for Indlela_2 in sorted((기준 / 'build/user').glob('*.elf')):
            kopisha_inani(Indlela_2, 'build/user/' + Indlela_2.name)
        for Igama in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopisha_inani(기준 / 'build/user' / (Igama + '.o'), 'build/user/' + Igama + '.o')
        for Igama in ('crt', 'aot-runtime', 'isikhathi_sokusebenza_solimi_esivamile_uxhaso', 'Sebenzisa', '미리번역', '되돌림'):
            kopisha_inani(기준 / 'build/ccompiler' / (Igama + '.o'), 'build/ccompiler/' + Igama + '.o')
        명세 = dict(umbiko_inani, objects=['objects/' + Igama + '.o' for Igama in isikhumulo_igama],
                    libraries=['objects/' + Path(Indlela_2).name for Indlela_2 in umtapo])
        (iqoqo_inani / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (iqoqo_inani / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        impokophelo = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / impokophelo.name
        with tarfile.open(str(임시압축), 'w:gz') as londoloza_inani:
            londoloza_inani.add(str(iqoqo_inani), arcname=iqoqo_inani.name)
        임시압축.replace(impokophelo)
    umbiko_inani['relink_archive_sha256'] = i_hash_ifayela(impokophelo)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(umbiko_inani, ensure_ascii=False, indent=2) + '\n')
    return impokophelo


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    inani = 해석기.parse_args()
    if inani.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
