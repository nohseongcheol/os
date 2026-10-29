#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL эх_мод·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
товлосон_газар_нэр = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
сан = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(ЗАМ):
    return hashlib.sha256(Path(ЗАМ).read_bytes()).hexdigest()


def 점검():
    for Нэр in ('vendor/wolfssh', 'vendor/wolfssl', 'алсын_утга/user_settings.h'):
        if (기준 / Нэр).exists():
            raise SystemExit('COSL 배포 Зогс: 이전 GPL алсын_утга 구현이 эх_мод 트리에 남아 있습니다: ' + Нэр)
    утсаар_холбосон_утга = (기준 / 'Сүлжээ_давхцал/утсаар_холбосон_Сүлжээ.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in утсаар_холбосон_утга or 'SPDX-License-Identifier: GPL' in утсаар_холбосон_утга:
        raise SystemExit('COSL 배포 Зогс: BSD GENET 구현·고지 шалгах 필요')
    for Нэр in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Нэр).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Нэр)
    тэмдэг_утга = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', тэмдэг_утга):
        raise SystemExit('COSL 배포 Зогс: 커널에 이전 GPL нууц_үг_утга/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Нэр in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Нэр + r'$', тэмдэг_утга, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Нэр)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        зураг_утга = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(зураг_утга)])
        if Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(зураг_утга) != Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    тайлан_утга_ddf2aaf3 = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Нэр: Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(기준 / 'build' / Нэр) for Нэр in сан}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(тайлан_утга_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    return тайлан_утга_ddf2aaf3


def 묶기():
    тайлан_утга_ddf2aaf3 = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        бүлэг_утга = Path(임시) / 'jkoros-native-relink'
        бүлэг_утга.mkdir()
        def хуулах_утга(원본, ижил_түвшин_утга):
            товлосон_газар_утга = бүлэг_утга / ижил_түвшин_утга
            товлосон_газар_утга.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(товлосон_газар_утга), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(товлосон_газар_утга))
        for Нэр in товлосон_газар_нэр:
            хуулах_утга(기준 / 'build' / (Нэр + '.o'), 'objects/' + Нэр + '.o')
        for Нэр in сан:
            хуулах_утга(기준 / 'build' / Нэр, 'objects/' + Path(Нэр).name)
        for Нэр in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'хэрэглэгч', '명명', 'компьютер', 'Сүлжээ_давхцал/Сүлжээ_давхцал.h', '부팅/Холбох_Бүдүүвч.ld',
                     'алсын_утга/assh_config.h', 'алсын_утга/config.h', 'алсын_утга/ctype.h', 'алсын_утга/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            хуулах_утга(기준 / Нэр, Нэр)
        for Нэр in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            хуулах_утга(저장소 / Нэр, Нэр)
        for ЗАМ in sorted((기준 / 'vendor').glob('LICENSE*')):
            хуулах_утга(ЗАМ, 'vendor/' + ЗАМ.name)
        хуулах_утга(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        хуулах_утга(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        хуулах_утга(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        хуулах_утга(기준 / 'Хэрэгслүүд/재연결.py', 'relink.py')
        for ЗАМ in sorted((기준 / 'build/user').glob('*.elf')):
            хуулах_утга(ЗАМ, 'build/user/' + ЗАМ.name)
        for Нэр in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            хуулах_утга(기준 / 'build/user' / (Нэр + '.o'), 'build/user/' + Нэр + '.o')
        for Нэр in ('crt', 'aot-runtime', 'түгээмэл_хэлний_ажиллах_үе_тусламж', 'Ажиллуулах', '미리번역', '되돌림'):
            хуулах_утга(기준 / 'build/ccompiler' / (Нэр + '.o'), 'build/ccompiler/' + Нэр + '.o')
        명세 = dict(тайлан_утга_ddf2aaf3, objects=['objects/' + Нэр + '.o' for Нэр in товлосон_газар_нэр],
                    libraries=['objects/' + Path(ЗАМ).name for ЗАМ in сан])
        (бүлэг_утга / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (бүлэг_утга / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        зорилго = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / зорилго.name
        with tarfile.open(str(임시압축), 'w:gz') as Архив_утга:
            Архив_утга.add(str(бүлэг_утга), arcname=бүлэг_утга.name)
        임시압축.replace(зорилго)
    тайлан_утга_ddf2aaf3['relink_archive_sha256'] = Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(зорилго)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(тайлан_утга_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    return зорилго


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    утга = 해석기.parse_args()
    if утга.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
