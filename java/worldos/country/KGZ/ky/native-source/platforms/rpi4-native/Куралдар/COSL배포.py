#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL башат_дарак·재연결 자료를 함께 묶는다."""
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
көздөө_жайы_аты = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
жыйнак = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def хэш_файл(ЖОЛ):
    return hashlib.sha256(Path(ЖОЛ).read_bytes()).hexdigest()


def 점검():
    for Аты in ('vendor/wolfssh', 'vendor/wolfssl', 'алыскы_маани/user_settings.h'):
        if (기준 / Аты).exists():
            raise SystemExit('COSL 배포 Токтотуу: 이전 GPL алыскы_маани 구현이 башат_дарак 트리에 남아 있습니다: ' + Аты)
    зымдуу_маани = (기준 / 'Желе_стек/зымдуу_Желе.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in зымдуу_маани or 'SPDX-License-Identifier: GPL' in зымдуу_маани:
        raise SystemExit('COSL 배포 Токтотуу: BSD GENET 구현·고지 тууралыгын_аныктоо 필요')
    for Аты in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Аты).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Аты)
    символ_маани = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', символ_маани):
        raise SystemExit('COSL 배포 Токтотуу: 커널에 이전 GPL жашыруун_сөз_маани/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Аты in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Аты + r'$', символ_маани, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Аты)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        сүрөт_маани = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(сүрөт_маани)])
        if хэш_файл(сүрөт_маани) != хэш_файл(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    отчет_маани_ddf2aaf3 = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': хэш_файл(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Аты: хэш_файл(기준 / 'build' / Аты) for Аты in жыйнак}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(отчет_маани_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    return отчет_маани_ddf2aaf3


def 묶기():
    отчет_маани_ddf2aaf3 = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        топ_маани = Path(임시) / 'jkoros-native-relink'
        топ_маани.mkdir()
        def даана_маани(원본, бирдей_маани):
            көздөө_жайы_маани = топ_маани / бирдей_маани
            көздөө_жайы_маани.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(көздөө_жайы_маани), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(көздөө_жайы_маани))
        for Аты in көздөө_жайы_аты:
            даана_маани(기준 / 'build' / (Аты + '.o'), 'objects/' + Аты + '.o')
        for Аты in жыйнак:
            даана_маани(기준 / 'build' / Аты, 'objects/' + Path(Аты).name)
        for Аты in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'колдонуучу', '명명', 'машина', 'Желе_стек/Желе_стек.h', '부팅/Шилтеме_түзүлүш.ld',
                     'алыскы_маани/assh_config.h', 'алыскы_маани/config.h', 'алыскы_маани/ctype.h', 'алыскы_маани/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            даана_маани(기준 / Аты, Аты)
        for Аты in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            даана_маани(저장소 / Аты, Аты)
        for ЖОЛ in sorted((기준 / 'vendor').glob('LICENSE*')):
            даана_маани(ЖОЛ, 'vendor/' + ЖОЛ.name)
        даана_маани(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        даана_маани(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        даана_маани(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        даана_маани(기준 / 'Куралдар/재연결.py', 'relink.py')
        for ЖОЛ in sorted((기준 / 'build/user').glob('*.elf')):
            даана_маани(ЖОЛ, 'build/user/' + ЖОЛ.name)
        for Аты in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            даана_маани(기준 / 'build/user' / (Аты + '.o'), 'build/user/' + Аты + '.o')
        for Аты in ('crt', 'aot-runtime', 'кадимки_тилдин_аткаруу_убагы_Колдоо', 'Жүргүзүү', '미리번역', '되돌림'):
            даана_маани(기준 / 'build/ccompiler' / (Аты + '.o'), 'build/ccompiler/' + Аты + '.o')
        명세 = dict(отчет_маани_ddf2aaf3, objects=['objects/' + Аты + '.o' for Аты in көздөө_жайы_аты],
                    libraries=['objects/' + Path(ЖОЛ).name for ЖОЛ in жыйнак])
        (топ_маани / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (топ_маани / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        максат = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / максат.name
        with tarfile.open(str(임시압축), 'w:gz') as Архив_маани:
            Архив_маани.add(str(топ_маани), arcname=топ_маани.name)
        임시압축.replace(максат)
    отчет_маани_ddf2aaf3['relink_archive_sha256'] = хэш_файл(максат)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(отчет_маани_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    return максат


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    маани = 해석기.parse_args()
    if маани.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
