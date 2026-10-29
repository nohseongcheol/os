#!/usr/bin/env python3
"""actueel_item Eigen ARM64 산출물을 검사하고 LGPL bron_structuur·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Taken_wortel = Path(__file__).resolve().parents[1]
opslagplaats_wortel = Taken_wortel.parents[1]
doel_naam = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
bibliotheek = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_Bestand(pad):
    return hashlib.sha256(Path(pad).read_bytes()).hexdigest()


def 점검():
    for Naam in ('vendor/wolfssh', 'vendor/wolfssl', 'extern_WAARDE_28edcfa1/user_settings.h'):
        if (Taken_wortel / Naam).exists():
            raise SystemExit('COSL distributie_WAARDE Stoppen: Vorige_item GPL extern_WAARDE_28edcfa1 구현이 bron_structuur 트리에 남아 있습니다: ' + Naam)
    bekabeld_WAARDE = (Taken_wortel / 'net_stack/bekabeld_net.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in bekabeld_WAARDE or 'SPDX-License-Identifier: GPL' in bekabeld_WAARDE:
        raise SystemExit('COSL distributie_WAARDE Stoppen: BSD GENET implementatie·고지 bevestigen 필요')
    for Naam in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (opslagplaats_wortel / Naam).is_file():
            raise SystemExit('COSL distributie_WAARDE 고지 없음: ' + Naam)
    symbool_WAARDE = subprocess.check_output(['aarch64-linux-gnu-nm', str(Taken_wortel / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symbool_WAARDE):
        raise SystemExit('COSL distributie_WAARDE Stoppen: 커널에 Vorige_item GPL wachtwoord_WAARDE/SSH 심볼이 남아 있습니다. opnieuw_proberen_WAARDE 빌드하세요.')
    for Naam in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Naam + r'$', symbool_WAARDE, re.M):
            raise SystemExit('COSL 대체 implementatie 누락: ' + Naam)
    with tempfile.TemporaryDirectory(dir=str(Taken_wortel / 'build')) as 임시:
        kopie_WAARDE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Taken_wortel / 'build/kernel.elf'), str(kopie_WAARDE)])
        if hash_Bestand(kopie_WAARDE) != hash_Bestand(Taken_wortel / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    Rapport_WAARDE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_Bestand(Taken_wortel / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Naam: hash_Bestand(Taken_wortel / 'build' / Naam) for Naam in bibliotheek}}
    (Taken_wortel / 'build/cosl-distribution-check.json').write_text(json.dumps(Rapport_WAARDE, ensure_ascii=False, indent=2) + '\n')
    return Rapport_WAARDE


def BIND_eindpunt():
    Rapport_WAARDE = 점검()
    distributie_WAARDE = Taken_wortel / 'dist'
    distributie_WAARDE.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Taken_wortel / 'build')) as 임시:
        Groep_WAARDE = Path(임시) / 'jkoros-native-relink'
        Groep_WAARDE.mkdir()
        def kopiëren_WAARDE(원본, peer_WAARDE):
            doel_WAARDE = Groep_WAARDE / peer_WAARDE
            doel_WAARDE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(doel_WAARDE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(doel_WAARDE))
        for Naam in doel_naam:
            kopiëren_WAARDE(Taken_wortel / 'build' / (Naam + '.o'), 'objects/' + Naam + '.o')
        for Naam in bibliotheek:
            kopiëren_WAARDE(Taken_wortel / 'build' / Naam, 'objects/' + Path(Naam).name)
        for Naam in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_compiler', 'gebruikersruimte', '명명', 'machine', 'net_stack/net_stack.h', 'machineopstart/koppelindeling.ld',
                     'extern_WAARDE_28edcfa1/assh_config.h', 'extern_WAARDE_28edcfa1/config.h', 'extern_WAARDE_28edcfa1/ctype.h', 'extern_WAARDE_28edcfa1/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopiëren_WAARDE(Taken_wortel / Naam, Naam)
        for Naam in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopiëren_WAARDE(opslagplaats_wortel / Naam, Naam)
        for pad in sorted((Taken_wortel / 'vendor').glob('LICENSE*')):
            kopiëren_WAARDE(pad, 'vendor/' + pad.name)
        kopiëren_WAARDE(Taken_wortel / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopiëren_WAARDE(Taken_wortel / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopiëren_WAARDE(opslagplaats_wortel / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopiëren_WAARDE(Taken_wortel / 'hulpmiddelen/재연결.py', 'relink.py')
        for pad in sorted((Taken_wortel / 'build/user').glob('*.elf')):
            kopiëren_WAARDE(pad, 'build/user/' + pad.name)
        for Naam in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopiëren_WAARDE(Taken_wortel / 'build/user' / (Naam + '.o'), 'build/user/' + Naam + '.o')
        for Naam in ('crt', 'aot-runtime', 'CLR_steun', 'starten', '미리번역', 'Retour_brug'):
            kopiëren_WAARDE(Taken_wortel / 'build/ccompiler' / (Naam + '.o'), 'build/ccompiler/' + Naam + '.o')
        specificatie = dict(Rapport_WAARDE, objects=['objects/' + Naam + '.o' for Naam in doel_naam],
                    libraries=['objects/' + Path(pad).name for pad in bibliotheek])
        (Groep_WAARDE / 'relink.json').write_text(json.dumps(specificatie, ensure_ascii=False, indent=2) + '\n')
        (Groep_WAARDE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_compiler.
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
        doel = distributie_WAARDE / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / doel.name
        with tarfile.open(str(임시압축), 'w:gz') as Archief_WAARDE:
            Archief_WAARDE.add(str(Groep_WAARDE), arcname=Groep_WAARDE.name)
        임시압축.replace(doel)
    Rapport_WAARDE['relink_archive_sha256'] = hash_Bestand(doel)
    (distributie_WAARDE / 'cosl-distribution.json').write_text(json.dumps(Rapport_WAARDE, ensure_ascii=False, indent=2) + '\n')
    return doel


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    WAARDE = parser_48ee4b1b.parse_args()
    if WAARDE.command == 'bundle':
        print('COSL source/relink kit:', BIND_eindpunt())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
