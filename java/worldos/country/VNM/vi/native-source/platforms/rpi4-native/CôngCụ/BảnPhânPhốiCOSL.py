#!/usr/bin/env python3
"""phầnMụcHiệnTại tựThân ARM64 산출물을 검사하고 LGPL câyNguồn·điểmCuốiKếtNốiLại 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

gốcCâyDựÁn = Path(__file__).resolve().parents[1]
gốcCâyKhoNguồn = gốcCâyDựÁn.parents[1]
tênĐích = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
thưViện = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def tệpMãBăm(đườngDẫn):
    return hashlib.sha256(Path(đườngDẫn).read_bytes()).hexdigest()


def xemXétTrạngThái():
    for tên in ('vendor/wolfssh', 'vendor/wolfssl', 'giáTrịTừXa/user_settings.h'):
        if (gốcCâyDựÁn / tên).exists():
            raise SystemExit('COSL giáTrịBảnPhânPhối dừng: phầnMụcTrướcĐó GPL giáTrịTừXa 구현이 câyNguồn 트리에 남아 있습니다: ' + tên)
    giáTrịHữuTuyến = (gốcCâyDựÁn / 'NgănXếpMạng/mạngHữuTuyến.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in giáTrịHữuTuyến or 'SPDX-License-Identifier: GPL' in giáTrịHữuTuyến:
        raise SystemExit('COSL giáTrịBảnPhânPhối dừng: BSD GENET phầnCàiĐặt·고지 xácMinh giáTrịCầnĐến')
    for tên in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (gốcCâyKhoNguồn / tên).is_file():
            raise SystemExit('COSL giáTrịBảnPhânPhối 고지 phươngThứcThiếu: ' + tên)
    giáTrịKýHiệu = subprocess.check_output(['aarch64-linux-gnu-nm', str(gốcCâyDựÁn / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', giáTrịKýHiệu):
        raise SystemExit('COSL giáTrịBảnPhânPhối dừng: 커널에 phầnMụcTrướcĐó GPL giáTrịMậtKhẩu/SSH 심볼이 남아 있습니다. giáTrịThửLại 빌드하세요.')
    for tên in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + tên + r'$', giáTrịKýHiệu, re.M):
            raise SystemExit('COSL 대체 phầnCàiĐặt 누락: ' + tên)
    with tempfile.TemporaryDirectory(dir=str(gốcCâyDựÁn / 'build')) as giáTrịTạm:
        giáTrịẢnh = Path(giáTrịTạm) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(gốcCâyDựÁn / 'build/kernel.elf'), str(giáTrịẢnh)])
        if tệpMãBăm(giáTrịẢnh) != tệpMãBăm(gốcCâyDựÁn / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    giáTrịBáoCáo = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': tệpMãBăm(gốcCâyDựÁn / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {tên: tệpMãBăm(gốcCâyDựÁn / 'build' / tên) for tên in thưViện}}
    (gốcCâyDựÁn / 'build/cosl-distribution-check.json').write_text(json.dumps(giáTrịBáoCáo, ensure_ascii=False, indent=2) + '\n')
    return giáTrịBáoCáo


def GóiTệpThựcThi():
    giáTrịBáoCáo = xemXétTrạngThái()
    giáTrịBảnPhânPhối = gốcCâyDựÁn / 'dist'
    giáTrịBảnPhânPhối.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(gốcCâyDựÁn / 'build')) as giáTrịTạm:
        giáTrịNhóm = Path(giáTrịTạm) / 'jkoros-native-relink'
        giáTrịNhóm.mkdir()
        def saoChépGiáTrị(nguyênBản, giáTrịĐốiTác):
            giáTrịĐích = giáTrịNhóm / giáTrịĐốiTác
            giáTrịĐích.parent.mkdir(parents=True, exist_ok=True)
            if nguyênBản.is_dir():
                shutil.copytree(str(nguyênBản), str(giáTrịĐích), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(nguyênBản), str(giáTrịĐích))
        for tên in tênĐích:
            saoChépGiáTrị(gốcCâyDựÁn / 'build' / (tên + '.o'), 'objects/' + tên + '.o')
        for tên in thưViện:
            saoChépGiáTrị(gốcCâyDựÁn / 'build' / tên, 'objects/' + Path(tên).name)
        for tên in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'TrìnhBiênDịchC', 'NgườiDùng', 'cáchĐặtTên', 'máy', 'NgănXếpMạng/NgănXếpMạng.h', 'KhởiĐộng/BốTríLiênKết.ld',
                     'giáTrịTừXa/assh_config.h', 'giáTrịTừXa/config.h', 'giáTrịTừXa/ctype.h', 'giáTrịTừXa/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'HướngDẫnBảnPhânPhốiCOSL.md'):
            saoChépGiáTrị(gốcCâyDựÁn / tên, tên)
        for tên in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            saoChépGiáTrị(gốcCâyKhoNguồn / tên, tên)
        for đườngDẫn in sorted((gốcCâyDựÁn / 'vendor').glob('LICENSE*')):
            saoChépGiáTrị(đườngDẫn, 'vendor/' + đườngDẫn.name)
        saoChépGiáTrị(gốcCâyDựÁn / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        saoChépGiáTrị(gốcCâyDựÁn / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        saoChépGiáTrị(gốcCâyKhoNguồn / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        saoChépGiáTrị(gốcCâyDựÁn / 'CôngCụ/điểmCuốiKếtNốiLại.py', 'relink.py')
        for đườngDẫn in sorted((gốcCâyDựÁn / 'build/user').glob('*.elf')):
            saoChépGiáTrị(đườngDẫn, 'build/user/' + đườngDẫn.name)
        for tên in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            saoChépGiáTrị(gốcCâyDựÁn / 'build/user' / (tên + '.o'), 'build/user/' + tên + '.o')
        for tên in ('crt', 'aot-runtime', 'HỗTrợMôiTrườngChạy', 'chạy', 'thờiGianCủaTrước', 'cầuNốiTrảVề'):
            saoChépGiáTrị(gốcCâyDựÁn / 'build/ccompiler' / (tên + '.o'), 'build/ccompiler/' + tên + '.o')
        đặcTả = dict(giáTrịBáoCáo, objects=['objects/' + tên + '.o' for tên in tênĐích],
                    libraries=['objects/' + Path(đườngDẫn).name for đườngDẫn in thưViện])
        (giáTrịNhóm / 'relink.json').write_text(json.dumps(đặcTả, ensure_ascii=False, indent=2) + '\n')
        (giáTrịNhóm / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in TrìnhBiênDịchC.
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
        giáTrịĐốiĐích = giáTrịBảnPhânPhối / 'jkoros-native-relink.tar.gz'
        khoLưuTrữTạm = Path(giáTrịTạm) / giáTrịĐốiĐích.name
        with tarfile.open(str(khoLưuTrữTạm), 'w:gz') as giáTrịKhoLưuTrữ:
            giáTrịKhoLưuTrữ.add(str(giáTrịNhóm), arcname=giáTrịNhóm.name)
        khoLưuTrữTạm.replace(giáTrịĐốiĐích)
    giáTrịBáoCáo['relink_archive_sha256'] = tệpMãBăm(giáTrịĐốiĐích)
    (giáTrịBảnPhânPhối / 'cosl-distribution.json').write_text(json.dumps(giáTrịBáoCáo, ensure_ascii=False, indent=2) + '\n')
    return giáTrịĐốiĐích


if __name__ == '__main__':
    BộPhânTích = argparse.ArgumentParser(description=__doc__)
    BộPhânTích.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    giáTrị = BộPhânTích.parse_args()
    if giáTrị.command == 'bundle':
        print('COSL source/relink kit:', GóiTệpThựcThi())
    else:
        print(json.dumps(xemXétTrạngThái(), ensure_ascii=False, indent=2))
