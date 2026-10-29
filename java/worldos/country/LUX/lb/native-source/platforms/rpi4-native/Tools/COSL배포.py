#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL Quell_Bamstruktur·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

projezéieren_Racinn = Path(__file__).resolve().parents[1]
저장소 = projezéieren_Racinn.parents[1]
Zil_Numm = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
Bibliothéik = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def Hash_Fichier(Wee):
    return hashlib.sha256(Path(Wee).read_bytes()).hexdigest()


def 점검():
    for Numm in ('vendor/wolfssh', 'vendor/wolfssl', 'extern_VALUE/user_settings.h'):
        if (projezéieren_Racinn / Numm).exists():
            raise SystemExit('COSL 배포 Stoppen: 이전 GPL extern_VALUE 구현이 Quell_Bamstruktur 트리에 남아 있습니다: ' + Numm)
    verkabelt_VALUE = (projezéieren_Racinn / 'Reseau_Stapel/verkabelt_Reseau.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in verkabelt_VALUE or 'SPDX-License-Identifier: GPL' in verkabelt_VALUE:
        raise SystemExit('COSL 배포 Stoppen: BSD GENET 구현·고지 verifizéieren 필요')
    for Numm in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Numm).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Numm)
    Symbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(projezéieren_Racinn / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', Symbol_VALUE):
        raise SystemExit('COSL 배포 Stoppen: 커널에 이전 GPL Passwuert_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Numm in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Numm + r'$', Symbol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Numm)
    with tempfile.TemporaryDirectory(dir=str(projezéieren_Racinn / 'build')) as 임시:
        Bild_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(projezéieren_Racinn / 'build/kernel.elf'), str(Bild_VALUE)])
        if Hash_Fichier(Bild_VALUE) != Hash_Fichier(projezéieren_Racinn / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    mellen_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': Hash_Fichier(projezéieren_Racinn / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Numm: Hash_Fichier(projezéieren_Racinn / 'build' / Numm) for Numm in Bibliothéik}}
    (projezéieren_Racinn / 'build/cosl-distribution-check.json').write_text(json.dumps(mellen_VALUE, ensure_ascii=False, indent=2) + '\n')
    return mellen_VALUE


def 묶기():
    mellen_VALUE = 점검()
    배포 = projezéieren_Racinn / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(projezéieren_Racinn / 'build')) as 임시:
        Grupp_VALUE = Path(임시) / 'jkoros-native-relink'
        Grupp_VALUE.mkdir()
        def Instanz_VALUE(원본, Peer_VALUE):
            Zil_VALUE = Grupp_VALUE / Peer_VALUE
            Zil_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(Zil_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(Zil_VALUE))
        for Numm in Zil_Numm:
            Instanz_VALUE(projezéieren_Racinn / 'build' / (Numm + '.o'), 'objects/' + Numm + '.o')
        for Numm in Bibliothéik:
            Instanz_VALUE(projezéieren_Racinn / 'build' / Numm, 'objects/' + Path(Numm).name)
        for Numm in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'Benotzer', '명명', 'Computer', 'Reseau_Stapel/Reseau_Stapel.h', '부팅/Link_Layout.ld',
                     'extern_VALUE/assh_config.h', 'extern_VALUE/config.h', 'extern_VALUE/ctype.h', 'extern_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            Instanz_VALUE(projezéieren_Racinn / Numm, Numm)
        for Numm in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            Instanz_VALUE(저장소 / Numm, Numm)
        for Wee in sorted((projezéieren_Racinn / 'vendor').glob('LICENSE*')):
            Instanz_VALUE(Wee, 'vendor/' + Wee.name)
        Instanz_VALUE(projezéieren_Racinn / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        Instanz_VALUE(projezéieren_Racinn / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        Instanz_VALUE(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        Instanz_VALUE(projezéieren_Racinn / 'Tools/재연결.py', 'relink.py')
        for Wee in sorted((projezéieren_Racinn / 'build/user').glob('*.elf')):
            Instanz_VALUE(Wee, 'build/user/' + Wee.name)
        for Numm in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            Instanz_VALUE(projezéieren_Racinn / 'build/user' / (Numm + '.o'), 'build/user/' + Numm + '.o')
        for Numm in ('crt', 'aot-runtime', 'Common_Language_Runtime_Support', 'Laf', '미리번역', '되돌림'):
            Instanz_VALUE(projezéieren_Racinn / 'build/ccompiler' / (Numm + '.o'), 'build/ccompiler/' + Numm + '.o')
        명세 = dict(mellen_VALUE, objects=['objects/' + Numm + '.o' for Numm in Zil_Numm],
                    libraries=['objects/' + Path(Wee).name for Wee in Bibliothéik])
        (Grupp_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Grupp_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        Zil = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / Zil.name
        with tarfile.open(str(임시압축), 'w:gz') as Archiv_VALUE:
            Archiv_VALUE.add(str(Grupp_VALUE), arcname=Grupp_VALUE.name)
        임시압축.replace(Zil)
    mellen_VALUE['relink_archive_sha256'] = Hash_Fichier(Zil)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(mellen_VALUE, ensure_ascii=False, indent=2) + '\n')
    return Zil


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = 해석기.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
