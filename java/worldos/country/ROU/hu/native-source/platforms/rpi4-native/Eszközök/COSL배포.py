#!/usr/bin/env python3
"""aktuális_cikk saját ARM64 산출물을 검사하고 LGPL forrás_fa·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

teendő_gyök = Path(__file__).resolve().parents[1]
adattár_gyök = teendő_gyök.parents[1]
cél_név = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
kódtár = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def kivonat_Fájl(ÚTVONAL):
    return hashlib.sha256(Path(ÚTVONAL).read_bytes()).hexdigest()


def 점검():
    for Név in ('vendor/wolfssh', 'vendor/wolfssl', 'távoli_ÉRTÉK/user_settings.h'):
        if (teendő_gyök / Név).exists():
            raise SystemExit('COSL elosztás_ÉRTÉK Leállítás: Előző_cikk GPL távoli_ÉRTÉK 구현이 forrás_fa 트리에 남아 있습니다: ' + Név)
    vezetékes_ÉRTÉK = (teendő_gyök / 'hálózat_Sor/vezetékes_hálózat.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in vezetékes_ÉRTÉK or 'SPDX-License-Identifier: GPL' in vezetékes_ÉRTÉK:
        raise SystemExit('COSL elosztás_ÉRTÉK Leállítás: BSD GENET 구현·고지 igazol 필요')
    for Név in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (adattár_gyök / Név).is_file():
            raise SystemExit('COSL elosztás_ÉRTÉK 고지 없음: ' + Név)
    szimbólum_ÉRTÉK = subprocess.check_output(['aarch64-linux-gnu-nm', str(teendő_gyök / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', szimbólum_ÉRTÉK):
        raise SystemExit('COSL elosztás_ÉRTÉK Leállítás: 커널에 Előző_cikk GPL jelszó_ÉRTÉK/SSH 심볼이 남아 있습니다. újrapróbál_ÉRTÉK 빌드하세요.')
    for Név in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Név + r'$', szimbólum_ÉRTÉK, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Név)
    with tempfile.TemporaryDirectory(dir=str(teendő_gyök / 'build')) as 임시:
        KÉP_ÉRTÉK = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(teendő_gyök / 'build/kernel.elf'), str(KÉP_ÉRTÉK)])
        if kivonat_Fájl(KÉP_ÉRTÉK) != kivonat_Fájl(teendő_gyök / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    jelent_ÉRTÉK = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': kivonat_Fájl(teendő_gyök / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Név: kivonat_Fájl(teendő_gyök / 'build' / Név) for Név in kódtár}}
    (teendő_gyök / 'build/cosl-distribution-check.json').write_text(json.dumps(jelent_ÉRTÉK, ensure_ascii=False, indent=2) + '\n')
    return jelent_ÉRTÉK


def BIND_végpont():
    jelent_ÉRTÉK = 점검()
    elosztás_ÉRTÉK = teendő_gyök / 'dist'
    elosztás_ÉRTÉK.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(teendő_gyök / 'build')) as 임시:
        Csoport_ÉRTÉK = Path(임시) / 'jkoros-native-relink'
        Csoport_ÉRTÉK.mkdir()
        def másol_ÉRTÉK(원본, társ_ÉRTÉK):
            cél_ÉRTÉK = Csoport_ÉRTÉK / társ_ÉRTÉK
            cél_ÉRTÉK.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(cél_ÉRTÉK), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(cél_ÉRTÉK))
        for Név in cél_név:
            másol_ÉRTÉK(teendő_gyök / 'build' / (Név + '.o'), 'objects/' + Név + '.o')
        for Név in kódtár:
            másol_ÉRTÉK(teendő_gyök / 'build' / Név, 'objects/' + Path(Név).name)
        for Név in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_fordítóprogram', 'felhasználó', '명명', 'gép', 'hálózat_Sor/hálózat_Sor.h', '부팅/csatol_Navigáció.ld',
                     'távoli_ÉRTÉK/assh_config.h', 'távoli_ÉRTÉK/config.h', 'távoli_ÉRTÉK/ctype.h', 'távoli_ÉRTÉK/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            másol_ÉRTÉK(teendő_gyök / Név, Név)
        for Név in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            másol_ÉRTÉK(adattár_gyök / Név, Név)
        for ÚTVONAL in sorted((teendő_gyök / 'vendor').glob('LICENSE*')):
            másol_ÉRTÉK(ÚTVONAL, 'vendor/' + ÚTVONAL.name)
        másol_ÉRTÉK(teendő_gyök / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        másol_ÉRTÉK(teendő_gyök / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        másol_ÉRTÉK(adattár_gyök / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        másol_ÉRTÉK(teendő_gyök / 'Eszközök/재연결.py', 'relink.py')
        for ÚTVONAL in sorted((teendő_gyök / 'build/user').glob('*.elf')):
            másol_ÉRTÉK(ÚTVONAL, 'build/user/' + ÚTVONAL.name)
        for Név in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            másol_ÉRTÉK(teendő_gyök / 'build/user' / (Név + '.o'), 'build/user/' + Név + '.o')
        for Név in ('crt', 'aot-runtime', 'CLR_támogat', 'Futtatás', '미리번역', 'visszaküld_híd'):
            másol_ÉRTÉK(teendő_gyök / 'build/ccompiler' / (Név + '.o'), 'build/ccompiler/' + Név + '.o')
        명세 = dict(jelent_ÉRTÉK, objects=['objects/' + Név + '.o' for Név in cél_név],
                    libraries=['objects/' + Path(ÚTVONAL).name for ÚTVONAL in kódtár])
        (Csoport_ÉRTÉK / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Csoport_ÉRTÉK / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_fordítóprogram.
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
        cél = elosztás_ÉRTÉK / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / cél.name
        with tarfile.open(str(임시압축), 'w:gz') as archív_ÉRTÉK:
            archív_ÉRTÉK.add(str(Csoport_ÉRTÉK), arcname=Csoport_ÉRTÉK.name)
        임시압축.replace(cél)
    jelent_ÉRTÉK['relink_archive_sha256'] = kivonat_Fájl(cél)
    (elosztás_ÉRTÉK / 'cosl-distribution.json').write_text(json.dumps(jelent_ÉRTÉK, ensure_ascii=False, indent=2) + '\n')
    return cél


if __name__ == '__main__':
    elemző_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    elemző_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ÉRTÉK = elemző_48ee4b1b.parse_args()
    if ÉRTÉK.command == 'bundle':
        print('COSL source/relink kit:', BIND_végpont())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
