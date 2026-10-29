#!/usr/bin/env python3
"""aktuellElementeintrag eigen ARM64 산출물을 검사하고 LGPL quelltextBaum·neuverbindenEndpunkt 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

projektWurzel = Path(__file__).resolve().parents[1]
ablageWurzel = projektWurzel.parents[1]
zielName = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
bibliothek = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def prüfsummeDatei(pfad):
    return hashlib.sha256(Path(pfad).read_bytes()).hexdigest()


def statuswertUntersuchen():
    for Name in ('vendor/wolfssh', 'vendor/wolfssl', 'entferntWert/user_settings.h'):
        if (projektWurzel / Name).exists():
            raise SystemExit('COSL verteilungWert stoppen: vorherigElementeintrag GPL entferntWert 구현이 quelltextBaum 트리에 남아 있습니다: ' + Name)
    verdrahtetWert = (projektWurzel / 'Netzwerkstapel/verdrahtetNetzwerk.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in verdrahtetWert or 'SPDX-License-Identifier: GPL' in verdrahtetWert:
        raise SystemExit('COSL verteilungWert stoppen: BSD GENET umsetzung·고지 überprüfen benötigtWert')
    for Name in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (ablageWurzel / Name).is_file():
            raise SystemExit('COSL verteilungWert 고지 fehlendMethode: ' + Name)
    symbolWert = subprocess.check_output(['aarch64-linux-gnu-nm', str(projektWurzel / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symbolWert):
        raise SystemExit('COSL verteilungWert stoppen: 커널에 vorherigElementeintrag GPL passwortWert/SSH 심볼이 남아 있습니다. erneutVersuchenWert 빌드하세요.')
    for Name in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Name + r'$', symbolWert, re.M):
            raise SystemExit('COSL 대체 umsetzung 누락: ' + Name)
    with tempfile.TemporaryDirectory(dir=str(projektWurzel / 'build')) as vorläufigWert:
        abbildWert = Path(vorläufigWert) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(projektWurzel / 'build/kernel.elf'), str(abbildWert)])
        if prüfsummeDatei(abbildWert) != prüfsummeDatei(projektWurzel / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    berichtWert = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': prüfsummeDatei(projektWurzel / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Name: prüfsummeDatei(projektWurzel / 'build' / Name) for Name in bibliothek}}
    (projektWurzel / 'build/cosl-distribution-check.json').write_text(json.dumps(berichtWert, ensure_ascii=False, indent=2) + '\n')
    return berichtWert


def AusführbündelPacken():
    berichtWert = statuswertUntersuchen()
    verteilungWert = projektWurzel / 'dist'
    verteilungWert.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(projektWurzel / 'build')) as vorläufigWert:
        gruppeWert = Path(vorläufigWert) / 'jkoros-native-relink'
        gruppeWert.mkdir()
        def wertKopieren(ursprünglich, gegenstelleWert):
            zielWert = gruppeWert / gegenstelleWert
            zielWert.parent.mkdir(parents=True, exist_ok=True)
            if ursprünglich.is_dir():
                shutil.copytree(str(ursprünglich), str(zielWert), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(ursprünglich), str(zielWert))
        for Name in zielName:
            wertKopieren(projektWurzel / 'build' / (Name + '.o'), 'objects/' + Name + '.o')
        for Name in bibliothek:
            wertKopieren(projektWurzel / 'build' / Name, 'objects/' + Path(Name).name)
        for Name in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'CÜbersetzer', 'Benutzer', 'benennung', 'maschine', 'Netzwerkstapel/Netzwerkstapel.h', 'Startvorgang/Bindungsanordnung.ld',
                     'entferntWert/assh_config.h', 'entferntWert/config.h', 'entferntWert/ctype.h', 'entferntWert/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSLVerteilungLeitfaden.md'):
            wertKopieren(projektWurzel / Name, Name)
        for Name in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            wertKopieren(ablageWurzel / Name, Name)
        for pfad in sorted((projektWurzel / 'vendor').glob('LICENSE*')):
            wertKopieren(pfad, 'vendor/' + pfad.name)
        wertKopieren(projektWurzel / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        wertKopieren(projektWurzel / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        wertKopieren(ablageWurzel / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        wertKopieren(projektWurzel / 'Werkzeuge/neuverbindenEndpunkt.py', 'relink.py')
        for pfad in sorted((projektWurzel / 'build/user').glob('*.elf')):
            wertKopieren(pfad, 'build/user/' + pfad.name)
        for Name in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            wertKopieren(projektWurzel / 'build/user' / (Name + '.o'), 'build/user/' + Name + '.o')
        for Name in ('crt', 'aot-runtime', 'LaufzeitUnterstützung', 'ausführenVorgang', 'vorabVonElementZeit', 'zurückkehrenBrücke'):
            wertKopieren(projektWurzel / 'build/ccompiler' / (Name + '.o'), 'build/ccompiler/' + Name + '.o')
        vorgabe = dict(berichtWert, objects=['objects/' + Name + '.o' for Name in zielName],
                    libraries=['objects/' + Path(pfad).name for pfad in bibliothek])
        (gruppeWert / 'relink.json').write_text(json.dumps(vorgabe, ensure_ascii=False, indent=2) + '\n')
        (gruppeWert / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in CÜbersetzer.
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
        zielobjektWert = verteilungWert / 'jkoros-native-relink.tar.gz'
        vorläufigArchiv = Path(vorläufigWert) / zielobjektWert.name
        with tarfile.open(str(vorläufigArchiv), 'w:gz') as archivWert:
            archivWert.add(str(gruppeWert), arcname=gruppeWert.name)
        vorläufigArchiv.replace(zielobjektWert)
    berichtWert['relink_archive_sha256'] = prüfsummeDatei(zielobjektWert)
    (verteilungWert / 'cosl-distribution.json').write_text(json.dumps(berichtWert, ensure_ascii=False, indent=2) + '\n')
    return zielobjektWert


if __name__ == '__main__':
    Strukturanalysierer = argparse.ArgumentParser(description=__doc__)
    Strukturanalysierer.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    Wert = Strukturanalysierer.parse_args()
    if Wert.command == 'bundle':
        print('COSL source/relink kit:', AusführbündelPacken())
    else:
        print(json.dumps(statuswertUntersuchen(), ensure_ascii=False, indent=2))
