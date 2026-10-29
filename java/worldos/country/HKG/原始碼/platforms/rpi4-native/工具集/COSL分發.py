#!/usr/bin/env python3
"""當前項目 內建 ARM64 산출물을 검사하고 LGPL 原始碼樹·重新連接端點 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

項目根 = Path(__file__).resolve().parents[1]
代碼庫根 = 項目根.parents[1]
目的地址名稱 = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
庫 = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def 哈希檔案(路徑):
    return hashlib.sha256(Path(路徑).read_bytes()).hexdigest()


def 審查狀態():
    for 名稱 in ('vendor/wolfssh', 'vendor/wolfssl', '遠程值/user_settings.h'):
        if (項目根 / 名稱).exists():
            raise SystemExit('COSL 分發值 停止: 上一個項目 GPL 遠程值 구현이 原始碼樹 트리에 남아 있습니다: ' + 名稱)
    有線值 = (項目根 / '通信網絡/有線網路.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in 有線值 or 'SPDX-License-Identifier: GPL' in 有線值:
        raise SystemExit('COSL 分發值 停止: BSD GENET 實現·고지 驗證 所需條件值')
    for 名稱 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (代碼庫根 / 名稱).is_file():
            raise SystemExit('COSL 分發值 고지 缺失方法: ' + 名稱)
    符號值 = subprocess.check_output(['aarch64-linux-gnu-nm', str(項目根 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', 符號值):
        raise SystemExit('COSL 分發值 停止: 커널에 上一個項目 GPL 密碼值/SSH 심볼이 남아 있습니다. 重試值 빌드하세요.')
    for 名稱 in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + 名稱 + r'$', 符號值, re.M):
            raise SystemExit('COSL 대체 實現 누락: ' + 名稱)
    with tempfile.TemporaryDirectory(dir=str(項目根 / 'build')) as 臨時值:
        映像值 = Path(臨時值) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(項目根 / 'build/kernel.elf'), str(映像值)])
        if 哈希檔案(映像值) != 哈希檔案(項目根 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    報告值 = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': 哈希檔案(項目根 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {名稱: 哈希檔案(項目根 / 'build' / 名稱) for 名稱 in 庫}}
    (項目根 / 'build/cosl-distribution-check.json').write_text(json.dumps(報告值, ensure_ascii=False, indent=2) + '\n')
    return 報告值


def 可執行束打包():
    報告值 = 審查狀態()
    分發值 = 項目根 / 'dist'
    分發值.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(項目根 / 'build')) as 臨時值:
        組值 = Path(臨時值) / 'jkoros-native-relink'
        組值.mkdir()
        def 複製值(原始, 對端值):
            目的地址值 = 組值 / 對端值
            目的地址值.parent.mkdir(parents=True, exist_ok=True)
            if 原始.is_dir():
                shutil.copytree(str(原始), str(目的地址值), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(原始), str(目的地址值))
        for 名稱 in 目的地址名稱:
            複製值(項目根 / 'build' / (名稱 + '.o'), 'objects/' + 名稱 + '.o')
        for 名稱 in 庫:
            複製值(項目根 / 'build' / 名稱, 'objects/' + Path(名稱).name)
        for 名稱 in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C編譯器', '使用者', '命名', '計算機', '通信網絡/通信網絡.h', '啓動/鏈接佈局.ld',
                     '遠程值/assh_config.h', '遠程值/config.h', '遠程值/ctype.h', '遠程值/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL分發指南.md'):
            複製值(項目根 / 名稱, 名稱)
        for 名稱 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            複製值(代碼庫根 / 名稱, 名稱)
        for 路徑 in sorted((項目根 / 'vendor').glob('LICENSE*')):
            複製值(路徑, 'vendor/' + 路徑.name)
        複製值(項目根 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        複製值(項目根 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        複製值(代碼庫根 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        複製值(項目根 / '工具集/重新連接端點.py', 'relink.py')
        for 路徑 in sorted((項目根 / 'build/user').glob('*.elf')):
            複製值(路徑, 'build/user/' + 路徑.name)
        for 名稱 in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            複製值(項目根 / 'build/user' / (名稱 + '.o'), 'build/user/' + 名稱 + '.o')
        for 名稱 in ('crt', 'aot-runtime', '運行時支持', '運行', '提前所屬時間', '發回橋接'):
            複製值(項目根 / 'build/ccompiler' / (名稱 + '.o'), 'build/ccompiler/' + 名稱 + '.o')
        規格 = dict(報告值, objects=['objects/' + 名稱 + '.o' for 名稱 in 目的地址名稱],
                    libraries=['objects/' + Path(路徑).name for 路徑 in 庫])
        (組值 / 'relink.json').write_text(json.dumps(規格, ensure_ascii=False, indent=2) + '\n')
        (組值 / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C編譯器.
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
        目標值 = 分發值 / 'jkoros-native-relink.tar.gz'
        臨時存檔 = Path(臨時值) / 目標值.name
        with tarfile.open(str(臨時存檔), 'w:gz') as 存檔值:
            存檔值.add(str(組值), arcname=組值.name)
        臨時存檔.replace(目標值)
    報告值['relink_archive_sha256'] = 哈希檔案(目標值)
    (分發值 / 'cosl-distribution.json').write_text(json.dumps(報告值, ensure_ascii=False, indent=2) + '\n')
    return 目標值


if __name__ == '__main__':
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    值 = 解析器.parse_args()
    if 值.command == 'bundle':
        print('COSL source/relink kit:', 可執行束打包())
    else:
        print(json.dumps(審查狀態(), ensure_ascii=False, indent=2))
