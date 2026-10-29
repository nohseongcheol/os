#!/usr/bin/env python3
"""bieżący_towar własny ARM64 산출물을 검사하고 LGPL źródło_drzewo·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_korzeń = Path(__file__).resolve().parents[1]
repozytorium_korzeń = Project_korzeń.parents[1]
cel_nazwa = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
biblioteka = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def skrót_Plik(ścieżka_2):
    return hashlib.sha256(Path(ścieżka_2).read_bytes()).hexdigest()


def 점검():
    for Nazwa in ('vendor/wolfssh', 'vendor/wolfssl', 'zdalny_WARTOŚĆ/user_settings.h'):
        if (Project_korzeń / Nazwa).exists():
            raise SystemExit('COSL dystrybucja_WARTOŚĆ Zatrzymaj: Wstecz_towar GPL zdalny_WARTOŚĆ 구현이 źródło_drzewo 트리에 남아 있습니다: ' + Nazwa)
    przewodowy_WARTOŚĆ = (Project_korzeń / 'sieć_Stos/przewodowy_sieć.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in przewodowy_WARTOŚĆ or 'SPDX-License-Identifier: GPL' in przewodowy_WARTOŚĆ:
        raise SystemExit('COSL dystrybucja_WARTOŚĆ Zatrzymaj: BSD GENET implementacja·고지 확인 필요')
    for Nazwa in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (repozytorium_korzeń / Nazwa).is_file():
            raise SystemExit('COSL dystrybucja_WARTOŚĆ 고지 없음: ' + Nazwa)
    symbol_WARTOŚĆ = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_korzeń / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symbol_WARTOŚĆ):
        raise SystemExit('COSL dystrybucja_WARTOŚĆ Zatrzymaj: 커널에 Wstecz_towar GPL hasło_WARTOŚĆ/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Nazwa in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nazwa + r'$', symbol_WARTOŚĆ, re.M):
            raise SystemExit('COSL 대체 implementacja 누락: ' + Nazwa)
    with tempfile.TemporaryDirectory(dir=str(Project_korzeń / 'build')) as 임시:
        OBRAZ_WARTOŚĆ = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_korzeń / 'build/kernel.elf'), str(OBRAZ_WARTOŚĆ)])
        if skrót_Plik(OBRAZ_WARTOŚĆ) != skrót_Plik(Project_korzeń / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    Raport_WARTOŚĆ = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': skrót_Plik(Project_korzeń / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nazwa: skrót_Plik(Project_korzeń / 'build' / Nazwa) for Nazwa in biblioteka}}
    (Project_korzeń / 'build/cosl-distribution-check.json').write_text(json.dumps(Raport_WARTOŚĆ, ensure_ascii=False, indent=2) + '\n')
    return Raport_WARTOŚĆ


def BIND_uczestnik():
    Raport_WARTOŚĆ = 점검()
    dystrybucja_WARTOŚĆ = Project_korzeń / 'dist'
    dystrybucja_WARTOŚĆ.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_korzeń / 'build')) as 임시:
        grupa_WARTOŚĆ = Path(임시) / 'jkoros-native-relink'
        grupa_WARTOŚĆ.mkdir()
        def kopiować_WARTOŚĆ(원본, węzeł_równorzędny_WARTOŚĆ):
            cel_WARTOŚĆ = grupa_WARTOŚĆ / węzeł_równorzędny_WARTOŚĆ
            cel_WARTOŚĆ.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(cel_WARTOŚĆ), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(cel_WARTOŚĆ))
        for Nazwa in cel_nazwa:
            kopiować_WARTOŚĆ(Project_korzeń / 'build' / (Nazwa + '.o'), 'objects/' + Nazwa + '.o')
        for Nazwa in biblioteka:
            kopiować_WARTOŚĆ(Project_korzeń / 'build' / Nazwa, 'objects/' + Path(Nazwa).name)
        for Nazwa in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_kompilator', 'przestrzeń_użytkownika', '명명', 'maszyna', 'sieć_Stos/sieć_Stos.h', 'rozruch_maszyny/układ_konsolidacji.ld',
                     'zdalny_WARTOŚĆ/assh_config.h', 'zdalny_WARTOŚĆ/config.h', 'zdalny_WARTOŚĆ/ctype.h', 'zdalny_WARTOŚĆ/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopiować_WARTOŚĆ(Project_korzeń / Nazwa, Nazwa)
        for Nazwa in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopiować_WARTOŚĆ(repozytorium_korzeń / Nazwa, Nazwa)
        for ścieżka_2 in sorted((Project_korzeń / 'vendor').glob('LICENSE*')):
            kopiować_WARTOŚĆ(ścieżka_2, 'vendor/' + ścieżka_2.name)
        kopiować_WARTOŚĆ(Project_korzeń / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopiować_WARTOŚĆ(Project_korzeń / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopiować_WARTOŚĆ(repozytorium_korzeń / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopiować_WARTOŚĆ(Project_korzeń / 'narzędzia/재연결.py', 'relink.py')
        for ścieżka_2 in sorted((Project_korzeń / 'build/user').glob('*.elf')):
            kopiować_WARTOŚĆ(ścieżka_2, 'build/user/' + ścieżka_2.name)
        for Nazwa in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopiować_WARTOŚĆ(Project_korzeń / 'build/user' / (Nazwa + '.o'), 'build/user/' + Nazwa + '.o')
        for Nazwa in ('crt', 'aot-runtime', 'CLR_wsparcie', 'Uruchom_2', '미리번역', 'Zwrot_mostek'):
            kopiować_WARTOŚĆ(Project_korzeń / 'build/ccompiler' / (Nazwa + '.o'), 'build/ccompiler/' + Nazwa + '.o')
        명세 = dict(Raport_WARTOŚĆ, objects=['objects/' + Nazwa + '.o' for Nazwa in cel_nazwa],
                    libraries=['objects/' + Path(ścieżka_2).name for ścieżka_2 in biblioteka])
        (grupa_WARTOŚĆ / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (grupa_WARTOŚĆ / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_kompilator.
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
        wartość_docelowa = dystrybucja_WARTOŚĆ / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / wartość_docelowa.name
        with tarfile.open(str(임시압축), 'w:gz') as Archiwum_WARTOŚĆ:
            Archiwum_WARTOŚĆ.add(str(grupa_WARTOŚĆ), arcname=grupa_WARTOŚĆ.name)
        임시압축.replace(wartość_docelowa)
    Raport_WARTOŚĆ['relink_archive_sha256'] = skrót_Plik(wartość_docelowa)
    (dystrybucja_WARTOŚĆ / 'cosl-distribution.json').write_text(json.dumps(Raport_WARTOŚĆ, ensure_ascii=False, indent=2) + '\n')
    return wartość_docelowa


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    WARTOŚĆ = parser_48ee4b1b.parse_args()
    if WARTOŚĆ.command == 'bundle':
        print('COSL source/relink kit:', BIND_uczestnik())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
