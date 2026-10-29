#!/usr/bin/env python3
"""tähtaja_piires_kaup oma ARM64 산출물을 검사하고 LGPL lähe_puu·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_juur = Path(__file__).resolve().parents[1]
hoidla_juur = Project_juur.parents[1]
sihtkoht_nimetus = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
teek = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def räsikood_Fail(RADA):
    return hashlib.sha256(Path(RADA).read_bytes()).hexdigest()


def 점검():
    for Nimi_2 in ('vendor/wolfssh', 'vendor/wolfssl', 'kauge_VALUE/user_settings.h'):
        if (Project_juur / Nimi_2).exists():
            raise SystemExit('COSL turustus_VALUE Peata: 이전 GPL kauge_VALUE 구현이 lähe_puu 트리에 남아 있습니다: ' + Nimi_2)
    juhtmega_ühendatud_VALUE = (Project_juur / 'võrk_Virn/juhtmega_ühendatud_võrk.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in juhtmega_ühendatud_VALUE or 'SPDX-License-Identifier: GPL' in juhtmega_ühendatud_VALUE:
        raise SystemExit('COSL turustus_VALUE Peata: BSD GENET 구현·고지 kinnitama 필요')
    for Nimi_2 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (hoidla_juur / Nimi_2).is_file():
            raise SystemExit('COSL turustus_VALUE 고지 없음: ' + Nimi_2)
    sümbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_juur / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', sümbol_VALUE):
        raise SystemExit('COSL turustus_VALUE Peata: 커널에 이전 GPL parool_VALUE/SSH 심볼이 남아 있습니다. uuesti_proovima_VALUE 빌드하세요.')
    for Nimi_2 in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nimi_2 + r'$', sümbol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Nimi_2)
    with tempfile.TemporaryDirectory(dir=str(Project_juur / 'build')) as 임시:
        pilt_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_juur / 'build/kernel.elf'), str(pilt_VALUE)])
        if räsikood_Fail(pilt_VALUE) != räsikood_Fail(Project_juur / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    aruanne_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': räsikood_Fail(Project_juur / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nimi_2: räsikood_Fail(Project_juur / 'build' / Nimi_2) for Nimi_2 in teek}}
    (Project_juur / 'build/cosl-distribution-check.json').write_text(json.dumps(aruanne_VALUE, ensure_ascii=False, indent=2) + '\n')
    return aruanne_VALUE


def BIND_osaleja():
    aruanne_VALUE = 점검()
    turustus_VALUE = Project_juur / 'dist'
    turustus_VALUE.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_juur / 'build')) as 임시:
        Rühm_VALUE = Path(임시) / 'jkoros-native-relink'
        Rühm_VALUE.mkdir()
        def eksemplar_VALUE(원본, partner_VALUE):
            sihtkoht_VALUE = Rühm_VALUE / partner_VALUE
            sihtkoht_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(sihtkoht_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(sihtkoht_VALUE))
        for Nimi_2 in sihtkoht_nimetus:
            eksemplar_VALUE(Project_juur / 'build' / (Nimi_2 + '.o'), 'objects/' + Nimi_2 + '.o')
        for Nimi_2 in teek:
            eksemplar_VALUE(Project_juur / 'build' / Nimi_2, 'objects/' + Path(Nimi_2).name)
        for Nimi_2 in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '_15_kompilaator', 'kasutaja', '명명', 'arvuti', 'võrk_Virn/võrk_Virn.h', '부팅/Link_küljend.ld',
                     'kauge_VALUE/assh_config.h', 'kauge_VALUE/config.h', 'kauge_VALUE/ctype.h', 'kauge_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            eksemplar_VALUE(Project_juur / Nimi_2, Nimi_2)
        for Nimi_2 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            eksemplar_VALUE(hoidla_juur / Nimi_2, Nimi_2)
        for RADA in sorted((Project_juur / 'vendor').glob('LICENSE*')):
            eksemplar_VALUE(RADA, 'vendor/' + RADA.name)
        eksemplar_VALUE(Project_juur / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        eksemplar_VALUE(Project_juur / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        eksemplar_VALUE(hoidla_juur / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        eksemplar_VALUE(Project_juur / 'Tööriistad/재연결.py', 'relink.py')
        for RADA in sorted((Project_juur / 'build/user').glob('*.elf')):
            eksemplar_VALUE(RADA, 'build/user/' + RADA.name)
        for Nimi_2 in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            eksemplar_VALUE(Project_juur / 'build/user' / (Nimi_2 + '.o'), 'build/user/' + Nimi_2 + '.o')
        for Nimi_2 in ('crt', 'aot-runtime', 'CLR_tugi', 'Käivita_2', '미리번역', 'tagasi_saatma_sild'):
            eksemplar_VALUE(Project_juur / 'build/ccompiler' / (Nimi_2 + '.o'), 'build/ccompiler/' + Nimi_2 + '.o')
        명세 = dict(aruanne_VALUE, objects=['objects/' + Nimi_2 + '.o' for Nimi_2 in sihtkoht_nimetus],
                    libraries=['objects/' + Path(RADA).name for RADA in teek])
        (Rühm_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Rühm_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in _15_kompilaator.
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
        siht = turustus_VALUE / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / siht.name
        with tarfile.open(str(임시압축), 'w:gz') as Arhiiv_VALUE:
            Arhiiv_VALUE.add(str(Rühm_VALUE), arcname=Rühm_VALUE.name)
        임시압축.replace(siht)
    aruanne_VALUE['relink_archive_sha256'] = räsikood_Fail(siht)
    (turustus_VALUE / 'cosl-distribution.json').write_text(json.dumps(aruanne_VALUE, ensure_ascii=False, indent=2) + '\n')
    return siht


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = parser_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', BIND_osaleja())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
