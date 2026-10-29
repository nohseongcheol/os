#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ffynhonnell_coeden·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

prosiect_gwraidd = Path(__file__).resolve().parents[1]
저장소 = prosiect_gwraidd.parents[1]
cyrchfan_enw = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
llyfrgell = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_ffeil(LLWYBR):
    return hashlib.sha256(Path(LLWYBR).read_bytes()).hexdigest()


def 점검():
    for Enw in ('vendor/wolfssh', 'vendor/wolfssl', 'pell_VALUE/user_settings.h'):
        if (prosiect_gwraidd / Enw).exists():
            raise SystemExit('COSL 배포 Atal: 이전 GPL pell_VALUE 구현이 ffynhonnell_coeden 트리에 남아 있습니다: ' + Enw)
    wedi_i_wifro_VALUE = (prosiect_gwraidd / 'Rhwydwaith_pentwr/wedi_i_wifro_Rhwydwaith.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in wedi_i_wifro_VALUE or 'SPDX-License-Identifier: GPL' in wedi_i_wifro_VALUE:
        raise SystemExit('COSL 배포 Atal: BSD GENET 구현·고지 dilysu 필요')
    for Enw in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Enw).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Enw)
    symbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(prosiect_gwraidd / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symbol_VALUE):
        raise SystemExit('COSL 배포 Atal: 커널에 이전 GPL cyfrinair_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Enw in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Enw + r'$', symbol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Enw)
    with tempfile.TemporaryDirectory(dir=str(prosiect_gwraidd / 'build')) as 임시:
        llun_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(prosiect_gwraidd / 'build/kernel.elf'), str(llun_VALUE)])
        if hash_ffeil(llun_VALUE) != hash_ffeil(prosiect_gwraidd / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    adrodd_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_ffeil(prosiect_gwraidd / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Enw: hash_ffeil(prosiect_gwraidd / 'build' / Enw) for Enw in llyfrgell}}
    (prosiect_gwraidd / 'build/cosl-distribution-check.json').write_text(json.dumps(adrodd_VALUE, ensure_ascii=False, indent=2) + '\n')
    return adrodd_VALUE


def 묶기():
    adrodd_VALUE = 점검()
    배포 = prosiect_gwraidd / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(prosiect_gwraidd / 'build')) as 임시:
        Grŵp_VALUE = Path(임시) / 'jkoros-native-relink'
        Grŵp_VALUE.mkdir()
        def copïo_VALUE(원본, cymar_VALUE):
            cyrchfan_VALUE = Grŵp_VALUE / cymar_VALUE
            cyrchfan_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(cyrchfan_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(cyrchfan_VALUE))
        for Enw in cyrchfan_enw:
            copïo_VALUE(prosiect_gwraidd / 'build' / (Enw + '.o'), 'objects/' + Enw + '.o')
        for Enw in llyfrgell:
            copïo_VALUE(prosiect_gwraidd / 'build' / Enw, 'objects/' + Path(Enw).name)
        for Enw in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'defnyddiwr', '명명', 'peiriant', 'Rhwydwaith_pentwr/Rhwydwaith_pentwr.h', '부팅/Dolen_Llywio.ld',
                     'pell_VALUE/assh_config.h', 'pell_VALUE/config.h', 'pell_VALUE/ctype.h', 'pell_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            copïo_VALUE(prosiect_gwraidd / Enw, Enw)
        for Enw in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            copïo_VALUE(저장소 / Enw, Enw)
        for LLWYBR in sorted((prosiect_gwraidd / 'vendor').glob('LICENSE*')):
            copïo_VALUE(LLWYBR, 'vendor/' + LLWYBR.name)
        copïo_VALUE(prosiect_gwraidd / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        copïo_VALUE(prosiect_gwraidd / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        copïo_VALUE(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        copïo_VALUE(prosiect_gwraidd / 'Offer/재연결.py', 'relink.py')
        for LLWYBR in sorted((prosiect_gwraidd / 'build/user').glob('*.elf')):
            copïo_VALUE(LLWYBR, 'build/user/' + LLWYBR.name)
        for Enw in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            copïo_VALUE(prosiect_gwraidd / 'build/user' / (Enw + '.o'), 'build/user/' + Enw + '.o')
        for Enw in ('crt', 'aot-runtime', 'amser_rhedeg_iaith_gyffredin_Cymorth', 'Gweithredu_2', '미리번역', 'return_pont'):
            copïo_VALUE(prosiect_gwraidd / 'build/ccompiler' / (Enw + '.o'), 'build/ccompiler/' + Enw + '.o')
        명세 = dict(adrodd_VALUE, objects=['objects/' + Enw + '.o' for Enw in cyrchfan_enw],
                    libraries=['objects/' + Path(LLWYBR).name for LLWYBR in llyfrgell])
        (Grŵp_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Grŵp_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        targed = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / targed.name
        with tarfile.open(str(임시압축), 'w:gz') as Archif_VALUE:
            Archif_VALUE.add(str(Grŵp_VALUE), arcname=Grŵp_VALUE.name)
        임시압축.replace(targed)
    adrodd_VALUE['relink_archive_sha256'] = hash_ffeil(targed)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(adrodd_VALUE, ensure_ascii=False, indent=2) + '\n')
    return targed


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = 해석기.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
