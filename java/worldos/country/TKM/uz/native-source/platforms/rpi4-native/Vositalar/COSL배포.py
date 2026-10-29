#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL manba_daraxt·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_ildiz = Path(__file__).resolve().parents[1]
repozitoriy_ildiz = Project_ildiz.parents[1]
ko_chirish_joyi_nom = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
kutubxona = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def tasodifiy_ma_lumot_fayl(yo_l):
    return hashlib.sha256(Path(yo_l).read_bytes()).hexdigest()


def 점검():
    for Nomi in ('vendor/wolfssh', 'vendor/wolfssl', 'masofaviy_VALUE/user_settings.h'):
        if (Project_ildiz / Nomi).exists():
            raise SystemExit('COSL 배포 Toʻxtatish: 이전 GPL masofaviy_VALUE 구현이 manba_daraxt 트리에 남아 있습니다: ' + Nomi)
    o_tkazish_VALUE = (Project_ildiz / 'Tarmoq_Stack/o_tkazish_Tarmoq.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in o_tkazish_VALUE or 'SPDX-License-Identifier: GPL' in o_tkazish_VALUE:
        raise SystemExit('COSL 배포 Toʻxtatish: BSD GENET 구현·고지 tasdiqlamoq 필요')
    for Nomi in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (repozitoriy_ildiz / Nomi).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Nomi)
    ramz_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_ildiz / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', ramz_VALUE):
        raise SystemExit('COSL 배포 Toʻxtatish: 커널에 이전 GPL parol_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Nomi in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nomi + r'$', ramz_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Nomi)
    with tempfile.TemporaryDirectory(dir=str(Project_ildiz / 'build')) as 임시:
        rasm_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_ildiz / 'build/kernel.elf'), str(rasm_VALUE)])
        if tasodifiy_ma_lumot_fayl(rasm_VALUE) != tasodifiy_ma_lumot_fayl(Project_ildiz / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    hisobot_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': tasodifiy_ma_lumot_fayl(Project_ildiz / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nomi: tasodifiy_ma_lumot_fayl(Project_ildiz / 'build' / Nomi) for Nomi in kutubxona}}
    (Project_ildiz / 'build/cosl-distribution-check.json').write_text(json.dumps(hisobot_VALUE, ensure_ascii=False, indent=2) + '\n')
    return hisobot_VALUE


def 묶기():
    hisobot_VALUE = 점검()
    배포 = Project_ildiz / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_ildiz / 'build')) as 임시:
        Guruh_VALUE = Path(임시) / 'jkoros-native-relink'
        Guruh_VALUE.mkdir()
        def namuna_VALUE(원본, bir_rangli_VALUE):
            ko_chirish_joyi_VALUE = Guruh_VALUE / bir_rangli_VALUE
            ko_chirish_joyi_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ko_chirish_joyi_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ko_chirish_joyi_VALUE))
        for Nomi in ko_chirish_joyi_nom:
            namuna_VALUE(Project_ildiz / 'build' / (Nomi + '.o'), 'objects/' + Nomi + '.o')
        for Nomi in kutubxona:
            namuna_VALUE(Project_ildiz / 'build' / Nomi, 'objects/' + Path(Nomi).name)
        for Nomi in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'foydalanuvchi', '명명', '기계', 'Tarmoq_Stack/Tarmoq_Stack.h', '부팅/ulash_Maket.ld',
                     'masofaviy_VALUE/assh_config.h', 'masofaviy_VALUE/config.h', 'masofaviy_VALUE/ctype.h', 'masofaviy_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            namuna_VALUE(Project_ildiz / Nomi, Nomi)
        for Nomi in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            namuna_VALUE(repozitoriy_ildiz / Nomi, Nomi)
        for yo_l in sorted((Project_ildiz / 'vendor').glob('LICENSE*')):
            namuna_VALUE(yo_l, 'vendor/' + yo_l.name)
        namuna_VALUE(Project_ildiz / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        namuna_VALUE(Project_ildiz / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        namuna_VALUE(repozitoriy_ildiz / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        namuna_VALUE(Project_ildiz / 'Vositalar/재연결.py', 'relink.py')
        for yo_l in sorted((Project_ildiz / 'build/user').glob('*.elf')):
            namuna_VALUE(yo_l, 'build/user/' + yo_l.name)
        for Nomi in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            namuna_VALUE(Project_ildiz / 'build/user' / (Nomi + '.o'), 'build/user/' + Nomi + '.o')
        for Nomi in ('crt', 'aot-runtime', 'umumiy_til_ish_jarayoni_madad', 'Bajarish', '미리번역', '되돌림'):
            namuna_VALUE(Project_ildiz / 'build/ccompiler' / (Nomi + '.o'), 'build/ccompiler/' + Nomi + '.o')
        명세 = dict(hisobot_VALUE, objects=['objects/' + Nomi + '.o' for Nomi in ko_chirish_joyi_nom],
                    libraries=['objects/' + Path(yo_l).name for yo_l in kutubxona])
        (Guruh_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Guruh_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        nishon = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / nishon.name
        with tarfile.open(str(임시압축), 'w:gz') as Arxiv_VALUE:
            Arxiv_VALUE.add(str(Guruh_VALUE), arcname=Guruh_VALUE.name)
        임시압축.replace(nishon)
    hisobot_VALUE['relink_archive_sha256'] = tasodifiy_ma_lumot_fayl(nishon)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(hisobot_VALUE, ensure_ascii=False, indent=2) + '\n')
    return nishon


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = parser_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
