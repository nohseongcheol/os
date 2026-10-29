#!/usr/bin/env python3
"""nykyinen_kohde oma ARM64 산출물을 검사하고 LGPL lähde_puu·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

aloite_juuri = Path(__file__).resolve().parents[1]
säilö_juuri = aloite_juuri.parents[1]
kohde_nimi = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
kirjasto = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hajautusarvo_Tiedosto(polku_2):
    return hashlib.sha256(Path(polku_2).read_bytes()).hexdigest()


def 점검():
    for Nimi in ('vendor/wolfssh', 'vendor/wolfssl', 'etä_ARVO/user_settings.h'):
        if (aloite_juuri / Nimi).exists():
            raise SystemExit('COSL jakelu_ARVO Pysäytä: Edellinen_kohde GPL etä_ARVO 구현이 lähde_puu 트리에 남아 있습니다: ' + Nimi)
    lanka_ARVO = (aloite_juuri / 'verkko_Pino/lanka_verkko.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in lanka_ARVO or 'SPDX-License-Identifier: GPL' in lanka_ARVO:
        raise SystemExit('COSL jakelu_ARVO Pysäytä: BSD GENET toteutus·고지 tarkistaa 필요')
    for Nimi in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (säilö_juuri / Nimi).is_file():
            raise SystemExit('COSL jakelu_ARVO 고지 없음: ' + Nimi)
    symboli_ARVO = subprocess.check_output(['aarch64-linux-gnu-nm', str(aloite_juuri / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symboli_ARVO):
        raise SystemExit('COSL jakelu_ARVO Pysäytä: 커널에 Edellinen_kohde GPL salasana_ARVO/SSH 심볼이 남아 있습니다. yrittää_uudelleen_ARVO 빌드하세요.')
    for Nimi in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nimi + r'$', symboli_ARVO, re.M):
            raise SystemExit('COSL 대체 toteutus 누락: ' + Nimi)
    with tempfile.TemporaryDirectory(dir=str(aloite_juuri / 'build')) as 임시:
        KUVA_ARVO = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(aloite_juuri / 'build/kernel.elf'), str(KUVA_ARVO)])
        if hajautusarvo_Tiedosto(KUVA_ARVO) != hajautusarvo_Tiedosto(aloite_juuri / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    raportti_ARVO = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hajautusarvo_Tiedosto(aloite_juuri / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nimi: hajautusarvo_Tiedosto(aloite_juuri / 'build' / Nimi) for Nimi in kirjasto}}
    (aloite_juuri / 'build/cosl-distribution-check.json').write_text(json.dumps(raportti_ARVO, ensure_ascii=False, indent=2) + '\n')
    return raportti_ARVO


def BIND_päätepiste():
    raportti_ARVO = 점검()
    jakelu_ARVO = aloite_juuri / 'dist'
    jakelu_ARVO.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(aloite_juuri / 'build')) as 임시:
        Ryhmä_ARVO = Path(임시) / 'jkoros-native-relink'
        Ryhmä_ARVO.mkdir()
        def kopioida_ARVO(원본, vertaissolmu_ARVO):
            kohde_ARVO = Ryhmä_ARVO / vertaissolmu_ARVO
            kohde_ARVO.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(kohde_ARVO), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(kohde_ARVO))
        for Nimi in kohde_nimi:
            kopioida_ARVO(aloite_juuri / 'build' / (Nimi + '.o'), 'objects/' + Nimi + '.o')
        for Nimi in kirjasto:
            kopioida_ARVO(aloite_juuri / 'build' / Nimi, 'objects/' + Path(Nimi).name)
        for Nimi in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_kääntäjä', 'käyttäjätila', '명명', 'kone', 'verkko_Pino/verkko_Pino.h', 'koneen_käynnistys/linkitysasettelu.ld',
                     'etä_ARVO/assh_config.h', 'etä_ARVO/config.h', 'etä_ARVO/ctype.h', 'etä_ARVO/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopioida_ARVO(aloite_juuri / Nimi, Nimi)
        for Nimi in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopioida_ARVO(säilö_juuri / Nimi, Nimi)
        for polku_2 in sorted((aloite_juuri / 'vendor').glob('LICENSE*')):
            kopioida_ARVO(polku_2, 'vendor/' + polku_2.name)
        kopioida_ARVO(aloite_juuri / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopioida_ARVO(aloite_juuri / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopioida_ARVO(säilö_juuri / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopioida_ARVO(aloite_juuri / 'työkalut/재연결.py', 'relink.py')
        for polku_2 in sorted((aloite_juuri / 'build/user').glob('*.elf')):
            kopioida_ARVO(polku_2, 'build/user/' + polku_2.name)
        for Nimi in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopioida_ARVO(aloite_juuri / 'build/user' / (Nimi + '.o'), 'build/user/' + Nimi + '.o')
        for Nimi in ('crt', 'aot-runtime', 'CLR_Tuki', 'Suorita_2', '미리번역', 'palauttaa_silta'):
            kopioida_ARVO(aloite_juuri / 'build/ccompiler' / (Nimi + '.o'), 'build/ccompiler/' + Nimi + '.o')
        määritys = dict(raportti_ARVO, objects=['objects/' + Nimi + '.o' for Nimi in kohde_nimi],
                    libraries=['objects/' + Path(polku_2).name for polku_2 in kirjasto])
        (Ryhmä_ARVO / 'relink.json').write_text(json.dumps(määritys, ensure_ascii=False, indent=2) + '\n')
        (Ryhmä_ARVO / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_kääntäjä.
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
        tavoite = jakelu_ARVO / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / tavoite.name
        with tarfile.open(str(임시압축), 'w:gz') as Arkisto_ARVO:
            Arkisto_ARVO.add(str(Ryhmä_ARVO), arcname=Ryhmä_ARVO.name)
        임시압축.replace(tavoite)
    raportti_ARVO['relink_archive_sha256'] = hajautusarvo_Tiedosto(tavoite)
    (jakelu_ARVO / 'cosl-distribution.json').write_text(json.dumps(raportti_ARVO, ensure_ascii=False, indent=2) + '\n')
    return tavoite


if __name__ == '__main__':
    jäsennin_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    jäsennin_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ARVO = jäsennin_48ee4b1b.parse_args()
    if ARVO.command == 'bundle':
        print('COSL source/relink kit:', BIND_päätepiste())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
