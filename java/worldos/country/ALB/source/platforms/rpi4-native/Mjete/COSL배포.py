#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL burim_degëzim·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_rrënjë = Path(__file__).resolve().parents[1]
depo_rrënjë = Project_rrënjë.parents[1]
vendmbërritje_emër = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
bibliotekë = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_skedar(POZICIONI):
    return hashlib.sha256(Path(POZICIONI).read_bytes()).hexdigest()


def 점검():
    for Emër in ('vendor/wolfssh', 'vendor/wolfssl', 'në_largësi_VALUE/user_settings.h'):
        if (Project_rrënjë / Emër).exists():
            raise SystemExit('COSL 배포 Ndalo: 이전 GPL në_largësi_VALUE 구현이 burim_degëzim 트리에 남아 있습니다: ' + Emër)
    i_lidhur_VALUE = (Project_rrënjë / 'rrjet_Stivë/i_lidhur_rrjet.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in i_lidhur_VALUE or 'SPDX-License-Identifier: GPL' in i_lidhur_VALUE:
        raise SystemExit('COSL 배포 Ndalo: BSD GENET 구현·고지 verifikoj 필요')
    for Emër in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (depo_rrënjë / Emër).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Emër)
    simbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_rrënjë / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbol_VALUE):
        raise SystemExit('COSL 배포 Ndalo: 커널에 이전 GPL fjalëkalim_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Emër in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Emër + r'$', simbol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Emër)
    with tempfile.TemporaryDirectory(dir=str(Project_rrënjë / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_rrënjë / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if hash_skedar(IMAGE_VALUE) != hash_skedar(Project_rrënjë / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    raport_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_skedar(Project_rrënjë / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Emër: hash_skedar(Project_rrënjë / 'build' / Emër) for Emër in bibliotekë}}
    (Project_rrënjë / 'build/cosl-distribution-check.json').write_text(json.dumps(raport_VALUE, ensure_ascii=False, indent=2) + '\n')
    return raport_VALUE


def 묶기():
    raport_VALUE = 점검()
    배포 = Project_rrënjë / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_rrënjë / 'build')) as 임시:
        grup_VALUE = Path(임시) / 'jkoros-native-relink'
        grup_VALUE.mkdir()
        def kopjoj_VALUE(원본, homolog_VALUE):
            vendmbërritje_VALUE = grup_VALUE / homolog_VALUE
            vendmbërritje_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(vendmbërritje_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(vendmbërritje_VALUE))
        for Emër in vendmbërritje_emër:
            kopjoj_VALUE(Project_rrënjë / 'build' / (Emër + '.o'), 'objects/' + Emër + '.o')
        for Emër in bibliotekë:
            kopjoj_VALUE(Project_rrënjë / 'build' / Emër, 'objects/' + Path(Emër).name)
        for Emër in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'përdorues', '명명', 'makinë', 'rrjet_Stivë/rrjet_Stivë.h', '부팅/lidh_Navigimi.ld',
                     'në_largësi_VALUE/assh_config.h', 'në_largësi_VALUE/config.h', 'në_largësi_VALUE/ctype.h', 'në_largësi_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopjoj_VALUE(Project_rrënjë / Emër, Emër)
        for Emër in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopjoj_VALUE(depo_rrënjë / Emër, Emër)
        for POZICIONI in sorted((Project_rrënjë / 'vendor').glob('LICENSE*')):
            kopjoj_VALUE(POZICIONI, 'vendor/' + POZICIONI.name)
        kopjoj_VALUE(Project_rrënjë / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopjoj_VALUE(Project_rrënjë / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopjoj_VALUE(depo_rrënjë / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopjoj_VALUE(Project_rrënjë / 'Mjete/재연결.py', 'relink.py')
        for POZICIONI in sorted((Project_rrënjë / 'build/user').glob('*.elf')):
            kopjoj_VALUE(POZICIONI, 'build/user/' + POZICIONI.name)
        for Emër in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopjoj_VALUE(Project_rrënjë / 'build/user' / (Emër + '.o'), 'build/user/' + Emër + '.o')
        for Emër in ('crt', 'aot-runtime', 'koha_e_ekzekutimit_të_gjuhës_së_zakonshme_Mbështetje', 'Ekzekuto', '미리번역', 'Kthe_urë'):
            kopjoj_VALUE(Project_rrënjë / 'build/ccompiler' / (Emër + '.o'), 'build/ccompiler/' + Emër + '.o')
        명세 = dict(raport_VALUE, objects=['objects/' + Emër + '.o' for Emër in vendmbërritje_emër],
                    libraries=['objects/' + Path(POZICIONI).name for POZICIONI in bibliotekë])
        (grup_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (grup_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        objektiv = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / objektiv.name
        with tarfile.open(str(임시압축), 'w:gz') as arkiv_VALUE:
            arkiv_VALUE.add(str(grup_VALUE), arcname=grup_VALUE.name)
        임시압축.replace(objektiv)
    raport_VALUE['relink_archive_sha256'] = hash_skedar(objektiv)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(raport_VALUE, ensure_ascii=False, indent=2) + '\n')
    return objektiv


if __name__ == '__main__':
    analizues_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizues_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = analizues_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
