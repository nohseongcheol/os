#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL mənbə_ağac·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_kök = Path(__file__).resolve().parents[1]
anbar_kök = Project_kök.parents[1]
təyinat_ad = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
kitabxana = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def heş_fayl(Cığır):
    return hashlib.sha256(Path(Cığır).read_bytes()).hexdigest()


def 점검():
    for Ad in ('vendor/wolfssh', 'vendor/wolfssl', 'uzaq_VALUE/user_settings.h'):
        if (Project_kök / Ad).exists():
            raise SystemExit('COSL 배포 Dayan: 이전 GPL uzaq_VALUE 구현이 mənbə_ağac 트리에 남아 있습니다: ' + Ad)
    naqilli_VALUE = (Project_kök / 'Şəbəkə_Yığın/naqilli_Şəbəkə.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in naqilli_VALUE or 'SPDX-License-Identifier: GPL' in naqilli_VALUE:
        raise SystemExit('COSL 배포 Dayan: BSD GENET 구현·고지 yoxlamaq 필요')
    for Ad in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (anbar_kök / Ad).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Ad)
    simvol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_kök / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simvol_VALUE):
        raise SystemExit('COSL 배포 Dayan: 커널에 이전 GPL parol_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Ad in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Ad + r'$', simvol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Ad)
    with tempfile.TemporaryDirectory(dir=str(Project_kök / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_kök / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if heş_fayl(IMAGE_VALUE) != heş_fayl(Project_kök / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    hesabat_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': heş_fayl(Project_kök / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Ad: heş_fayl(Project_kök / 'build' / Ad) for Ad in kitabxana}}
    (Project_kök / 'build/cosl-distribution-check.json').write_text(json.dumps(hesabat_VALUE, ensure_ascii=False, indent=2) + '\n')
    return hesabat_VALUE


def 묶기():
    hesabat_VALUE = 점검()
    배포 = Project_kök / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_kök / 'build')) as 임시:
        Qrup_VALUE = Path(임시) / 'jkoros-native-relink'
        Qrup_VALUE.mkdir()
        def nümunə_VALUE(원본, eynisəviyyəli_VALUE):
            təyinat_VALUE_a0fbc067 = Qrup_VALUE / eynisəviyyəli_VALUE
            təyinat_VALUE_a0fbc067.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(təyinat_VALUE_a0fbc067), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(təyinat_VALUE_a0fbc067))
        for Ad in təyinat_ad:
            nümunə_VALUE(Project_kök / 'build' / (Ad + '.o'), 'objects/' + Ad + '.o')
        for Ad in kitabxana:
            nümunə_VALUE(Project_kök / 'build' / Ad, 'objects/' + Path(Ad).name)
        for Ad in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'istifadəçi', '명명', 'maşın', 'Şəbəkə_Yığın/Şəbəkə_Yığın.h', '부팅/keçid_Düzüm.ld',
                     'uzaq_VALUE/assh_config.h', 'uzaq_VALUE/config.h', 'uzaq_VALUE/ctype.h', 'uzaq_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            nümunə_VALUE(Project_kök / Ad, Ad)
        for Ad in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            nümunə_VALUE(anbar_kök / Ad, Ad)
        for Cığır in sorted((Project_kök / 'vendor').glob('LICENSE*')):
            nümunə_VALUE(Cığır, 'vendor/' + Cığır.name)
        nümunə_VALUE(Project_kök / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        nümunə_VALUE(Project_kök / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        nümunə_VALUE(anbar_kök / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        nümunə_VALUE(Project_kök / 'Alətlər/재연결.py', 'relink.py')
        for Cığır in sorted((Project_kök / 'build/user').glob('*.elf')):
            nümunə_VALUE(Cığır, 'build/user/' + Cığır.name)
        for Ad in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            nümunə_VALUE(Project_kök / 'build/user' / (Ad + '.o'), 'build/user/' + Ad + '.o')
        for Ad in ('crt', 'aot-runtime', 'ümumi_dil_icrası_Dəstək', 'İcra_Et', '미리번역', 'geri_qaytarmaq_körpü'):
            nümunə_VALUE(Project_kök / 'build/ccompiler' / (Ad + '.o'), 'build/ccompiler/' + Ad + '.o')
        명세 = dict(hesabat_VALUE, objects=['objects/' + Ad + '.o' for Ad in təyinat_ad],
                    libraries=['objects/' + Path(Cığır).name for Cığır in kitabxana])
        (Qrup_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Qrup_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        hədəf = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / hədəf.name
        with tarfile.open(str(임시압축), 'w:gz') as Arxiv_VALUE:
            Arxiv_VALUE.add(str(Qrup_VALUE), arcname=Qrup_VALUE.name)
        임시압축.replace(hədəf)
    hesabat_VALUE['relink_archive_sha256'] = heş_fayl(hədəf)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(hesabat_VALUE, ensure_ascii=False, indent=2) + '\n')
    return hədəf


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = parser_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
