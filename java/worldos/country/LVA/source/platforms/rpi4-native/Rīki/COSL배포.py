#!/usr/bin/env python3
"""pašreizējais_krājums savs ARM64 산출물을 검사하고 LGPL avots_koks·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_sakne = Path(__file__).resolve().parents[1]
repozitorijs_sakne = Project_sakne.parents[1]
mērķis_nosaukums = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
bibliotēka = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def jaukšana_Fails(CEĻŠ):
    return hashlib.sha256(Path(CEĻŠ).read_bytes()).hexdigest()


def 점검():
    for Nosaukums in ('vendor/wolfssh', 'vendor/wolfssl', 'attāls_VALUE/user_settings.h'):
        if (Project_sakne / Nosaukums).exists():
            raise SystemExit('COSL sadale_VALUE Pārtraukt: 이전 GPL attāls_VALUE 구현이 avots_koks 트리에 남아 있습니다: ' + Nosaukums)
    vadu_VALUE = (Project_sakne / 'tīkls_kopa/vadu_tīkls.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in vadu_VALUE or 'SPDX-License-Identifier: GPL' in vadu_VALUE:
        raise SystemExit('COSL sadale_VALUE Pārtraukt: BSD GENET 구현·고지 verificēt 필요')
    for Nosaukums in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (repozitorijs_sakne / Nosaukums).is_file():
            raise SystemExit('COSL sadale_VALUE 고지 없음: ' + Nosaukums)
    simbols_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_sakne / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbols_VALUE):
        raise SystemExit('COSL sadale_VALUE Pārtraukt: 커널에 이전 GPL parole_VALUE/SSH 심볼이 남아 있습니다. mēģināt_vēlreiz_VALUE 빌드하세요.')
    for Nosaukums in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nosaukums + r'$', simbols_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Nosaukums)
    with tempfile.TemporaryDirectory(dir=str(Project_sakne / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_sakne / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if jaukšana_Fails(IMAGE_VALUE) != jaukšana_Fails(Project_sakne / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ziņot_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': jaukšana_Fails(Project_sakne / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nosaukums: jaukšana_Fails(Project_sakne / 'build' / Nosaukums) for Nosaukums in bibliotēka}}
    (Project_sakne / 'build/cosl-distribution-check.json').write_text(json.dumps(ziņot_VALUE, ensure_ascii=False, indent=2) + '\n')
    return ziņot_VALUE


def BIND_dalībnieks():
    ziņot_VALUE = 점검()
    sadale_VALUE = Project_sakne / 'dist'
    sadale_VALUE.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_sakne / 'build')) as 임시:
        Grupa_VALUE = Path(임시) / 'jkoros-native-relink'
        Grupa_VALUE.mkdir()
        def kopēt_VALUE(원본, vienranga_VALUE):
            mērķis_VALUE = Grupa_VALUE / vienranga_VALUE
            mērķis_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(mērķis_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(mērķis_VALUE))
        for Nosaukums in mērķis_nosaukums:
            kopēt_VALUE(Project_sakne / 'build' / (Nosaukums + '.o'), 'objects/' + Nosaukums + '.o')
        for Nosaukums in bibliotēka:
            kopēt_VALUE(Project_sakne / 'build' / Nosaukums, 'objects/' + Path(Nosaukums).name)
        for Nosaukums in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_kompilators', 'lietotājs', '명명', 'mašīna', 'tīkls_kopa/tīkls_kopa.h', '부팅/Saite_shēma.ld',
                     'attāls_VALUE/assh_config.h', 'attāls_VALUE/config.h', 'attāls_VALUE/ctype.h', 'attāls_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopēt_VALUE(Project_sakne / Nosaukums, Nosaukums)
        for Nosaukums in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopēt_VALUE(repozitorijs_sakne / Nosaukums, Nosaukums)
        for CEĻŠ in sorted((Project_sakne / 'vendor').glob('LICENSE*')):
            kopēt_VALUE(CEĻŠ, 'vendor/' + CEĻŠ.name)
        kopēt_VALUE(Project_sakne / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopēt_VALUE(Project_sakne / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopēt_VALUE(repozitorijs_sakne / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopēt_VALUE(Project_sakne / 'Rīki/재연결.py', 'relink.py')
        for CEĻŠ in sorted((Project_sakne / 'build/user').glob('*.elf')):
            kopēt_VALUE(CEĻŠ, 'build/user/' + CEĻŠ.name)
        for Nosaukums in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopēt_VALUE(Project_sakne / 'build/user' / (Nosaukums + '.o'), 'build/user/' + Nosaukums + '.o')
        for Nosaukums in ('crt', 'aot-runtime', 'CLR_Atbalsts', 'Palaist', '미리번역', 'atdot_tilts'):
            kopēt_VALUE(Project_sakne / 'build/ccompiler' / (Nosaukums + '.o'), 'build/ccompiler/' + Nosaukums + '.o')
        명세 = dict(ziņot_VALUE, objects=['objects/' + Nosaukums + '.o' for Nosaukums in mērķis_nosaukums],
                    libraries=['objects/' + Path(CEĻŠ).name for CEĻŠ in bibliotēka])
        (Grupa_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Grupa_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_kompilators.
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
        mērķis = sadale_VALUE / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / mērķis.name
        with tarfile.open(str(임시압축), 'w:gz') as Arhīvs_VALUE:
            Arhīvs_VALUE.add(str(Grupa_VALUE), arcname=Grupa_VALUE.name)
        임시압축.replace(mērķis)
    ziņot_VALUE['relink_archive_sha256'] = jaukšana_Fails(mērķis)
    (sadale_VALUE / 'cosl-distribution.json').write_text(json.dumps(ziņot_VALUE, ensure_ascii=False, indent=2) + '\n')
    return mērķis


if __name__ == '__main__':
    parsētājs_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parsētājs_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = parsētājs_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', BIND_dalībnieks())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
