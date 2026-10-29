#!/usr/bin/env python3
"""현재 eigin ARM64 산출물을 검사하고 LGPL uppruni_tré·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

verk_rót = Path(__file__).resolve().parents[1]
gagnageymsla_rót = verk_rót.parents[1]
endastaður_heiti = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
safn = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def tæting_skrá(SLÓÐ):
    return hashlib.sha256(Path(SLÓÐ).read_bytes()).hexdigest()


def 점검():
    for Heiti in ('vendor/wolfssh', 'vendor/wolfssl', 'fjartengdur_VALUE/user_settings.h'):
        if (verk_rót / Heiti).exists():
            raise SystemExit('COSL dreifing_VALUE Stopp: 이전 GPL fjartengdur_VALUE 구현이 uppruni_tré 트리에 남아 있습니다: ' + Heiti)
    vírað_VALUE = (verk_rót / 'Net_bunki/vírað_Net.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in vírað_VALUE or 'SPDX-License-Identifier: GPL' in vírað_VALUE:
        raise SystemExit('COSL dreifing_VALUE Stopp: BSD GENET 구현·고지 sannprófa 필요')
    for Heiti in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (gagnageymsla_rót / Heiti).is_file():
            raise SystemExit('COSL dreifing_VALUE 고지 없음: ' + Heiti)
    tákn_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(verk_rót / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', tákn_VALUE):
        raise SystemExit('COSL dreifing_VALUE Stopp: 커널에 이전 GPL aðgangsorð_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Heiti in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Heiti + r'$', tákn_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Heiti)
    with tempfile.TemporaryDirectory(dir=str(verk_rót / 'build')) as 임시:
        mynd_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(verk_rót / 'build/kernel.elf'), str(mynd_VALUE)])
        if tæting_skrá(mynd_VALUE) != tæting_skrá(verk_rót / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    skrá_VALUE_ddf2aaf3 = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': tæting_skrá(verk_rót / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Heiti: tæting_skrá(verk_rót / 'build' / Heiti) for Heiti in safn}}
    (verk_rót / 'build/cosl-distribution-check.json').write_text(json.dumps(skrá_VALUE_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    return skrá_VALUE_ddf2aaf3


def BIND_endastöð():
    skrá_VALUE_ddf2aaf3 = 점검()
    dreifing_VALUE = verk_rót / 'dist'
    dreifing_VALUE.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(verk_rót / 'build')) as 임시:
        Hópur_VALUE = Path(임시) / 'jkoros-native-relink'
        Hópur_VALUE.mkdir()
        def afrita_VALUE(원본, jafningi_VALUE):
            endastaður_VALUE = Hópur_VALUE / jafningi_VALUE
            endastaður_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(endastaður_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(endastaður_VALUE))
        for Heiti in endastaður_heiti:
            afrita_VALUE(verk_rót / 'build' / (Heiti + '.o'), 'objects/' + Heiti + '.o')
        for Heiti in safn:
            afrita_VALUE(verk_rót / 'build' / Heiti, 'objects/' + Path(Heiti).name)
        for Heiti in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'notandi', '명명', 'vél', 'Net_bunki/Net_bunki.h', '부팅/tengja_útlit.ld',
                     'fjartengdur_VALUE/assh_config.h', 'fjartengdur_VALUE/config.h', 'fjartengdur_VALUE/ctype.h', 'fjartengdur_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            afrita_VALUE(verk_rót / Heiti, Heiti)
        for Heiti in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            afrita_VALUE(gagnageymsla_rót / Heiti, Heiti)
        for SLÓÐ in sorted((verk_rót / 'vendor').glob('LICENSE*')):
            afrita_VALUE(SLÓÐ, 'vendor/' + SLÓÐ.name)
        afrita_VALUE(verk_rót / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        afrita_VALUE(verk_rót / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        afrita_VALUE(gagnageymsla_rót / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        afrita_VALUE(verk_rót / 'Verkfæri/재연결.py', 'relink.py')
        for SLÓÐ in sorted((verk_rót / 'build/user').glob('*.elf')):
            afrita_VALUE(SLÓÐ, 'build/user/' + SLÓÐ.name)
        for Heiti in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            afrita_VALUE(verk_rót / 'build/user' / (Heiti + '.o'), 'build/user/' + Heiti + '.o')
        for Heiti in ('crt', 'aot-runtime', 'CLR_Aðstoð', 'Keyra_2', '미리번역', 'skila_brú'):
            afrita_VALUE(verk_rót / 'build/ccompiler' / (Heiti + '.o'), 'build/ccompiler/' + Heiti + '.o')
        명세 = dict(skrá_VALUE_ddf2aaf3, objects=['objects/' + Heiti + '.o' for Heiti in endastaður_heiti],
                    libraries=['objects/' + Path(SLÓÐ).name for SLÓÐ in safn])
        (Hópur_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Hópur_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        markmið = dreifing_VALUE / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / markmið.name
        with tarfile.open(str(임시압축), 'w:gz') as Safn_VALUE:
            Safn_VALUE.add(str(Hópur_VALUE), arcname=Hópur_VALUE.name)
        임시압축.replace(markmið)
    skrá_VALUE_ddf2aaf3['relink_archive_sha256'] = tæting_skrá(markmið)
    (dreifing_VALUE / 'cosl-distribution.json').write_text(json.dumps(skrá_VALUE_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    return markmið


if __name__ == '__main__':
    þáttari_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    þáttari_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = þáttari_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', BIND_endastöð())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
