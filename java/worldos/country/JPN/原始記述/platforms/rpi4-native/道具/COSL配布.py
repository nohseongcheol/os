#!/usr/bin/env python3
"""現在項目 内蔵 ARM64 산출물을 검사하고 LGPL ソース木·再接続通信端点 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

計画根 = Path(__file__).resolve().parents[1]
保管庫根 = 計画根.parents[1]
宛先名前 = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ライブラリ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ハッシュファイル(経路):
    return hashlib.sha256(Path(経路).read_bytes()).hexdigest()


def 状況調査():
    for 名前 in ('vendor/wolfssh', 'vendor/wolfssl', '遠隔値/user_settings.h'):
        if (計画根 / 名前).exists():
            raise SystemExit('COSL 配布値 停止: 前回項目 GPL 遠隔値 구현이 ソース木 트리에 남아 있습니다: ' + 名前)
    結線済み値 = (計画根 / '通信網/結線済み通信網.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in 結線済み値 or 'SPDX-License-Identifier: GPL' in 結線済み値:
        raise SystemExit('COSL 配布値 停止: BSD GENET 実装·고지 検証 必要値')
    for 名前 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (保管庫根 / 名前).is_file():
            raise SystemExit('COSL 配布値 고지 未存在メソッド: ' + 名前)
    記号値 = subprocess.check_output(['aarch64-linux-gnu-nm', str(計画根 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', 記号値):
        raise SystemExit('COSL 配布値 停止: 커널에 前回項目 GPL 合言葉値/SSH 심볼이 남아 있습니다. 再試行処理値 빌드하세요.')
    for 名前 in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + 名前 + r'$', 記号値, re.M):
            raise SystemExit('COSL 대체 実装 누락: ' + 名前)
    with tempfile.TemporaryDirectory(dir=str(計画根 / 'build')) as 一時値:
        イメージ値 = Path(一時値) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(計画根 / 'build/kernel.elf'), str(イメージ値)])
        if ハッシュファイル(イメージ値) != ハッシュファイル(計画根 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    報告値 = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ハッシュファイル(計画根 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {名前: ハッシュファイル(計画根 / 'build' / 名前) for 名前 in ライブラリ}}
    (計画根 / 'build/cosl-distribution-check.json').write_text(json.dumps(報告値, ensure_ascii=False, indent=2) + '\n')
    return 報告値


def 実行束梱包():
    報告値 = 状況調査()
    配布値 = 計画根 / 'dist'
    配布値.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(計画根 / 'build')) as 一時値:
        集合値 = Path(一時値) / 'jkoros-native-relink'
        集合値.mkdir()
        def 値複写(原本, 通信相手値):
            宛先値 = 集合値 / 通信相手値
            宛先値.parent.mkdir(parents=True, exist_ok=True)
            if 原本.is_dir():
                shutil.copytree(str(原本), str(宛先値), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(原本), str(宛先値))
        for 名前 in 宛先名前:
            値複写(計画根 / 'build' / (名前 + '.o'), 'objects/' + 名前 + '.o')
        for 名前 in ライブラリ:
            値複写(計画根 / 'build' / 名前, 'objects/' + Path(名前).name)
        for 名前 in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'Cコンパイラ', '利用者', '命名', '機械', '通信網/通信網.h', '起動/連結配置.ld',
                     '遠隔値/assh_config.h', '遠隔値/config.h', '遠隔値/ctype.h', '遠隔値/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL配布手引.md'):
            値複写(計画根 / 名前, 名前)
        for 名前 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            値複写(保管庫根 / 名前, 名前)
        for 経路 in sorted((計画根 / 'vendor').glob('LICENSE*')):
            値複写(経路, 'vendor/' + 経路.name)
        値複写(計画根 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        値複写(計画根 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        値複写(保管庫根 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        値複写(計画根 / '道具/再接続通信端点.py', 'relink.py')
        for 経路 in sorted((計画根 / 'build/user').glob('*.elf')):
            値複写(経路, 'build/user/' + 経路.name)
        for 名前 in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            値複写(計画根 / 'build/user' / (名前 + '.o'), 'build/user/' + 名前 + '.o')
        for 名前 in ('crt', 'aot-runtime', '実行環境支援', '起動処理', '事前用時間', '復帰橋渡し'):
            値複写(計画根 / 'build/ccompiler' / (名前 + '.o'), 'build/ccompiler/' + 名前 + '.o')
        仕様 = dict(報告値, objects=['objects/' + 名前 + '.o' for 名前 in 宛先名前],
                    libraries=['objects/' + Path(経路).name for 経路 in ライブラリ])
        (集合値 / 'relink.json').write_text(json.dumps(仕様, ensure_ascii=False, indent=2) + '\n')
        (集合値 / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in Cコンパイラ.
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
        対象値 = 配布値 / 'jkoros-native-relink.tar.gz'
        一時書庫 = Path(一時値) / 対象値.name
        with tarfile.open(str(一時書庫), 'w:gz') as 書庫値:
            書庫値.add(str(集合値), arcname=集合値.name)
        一時書庫.replace(対象値)
    報告値['relink_archive_sha256'] = ハッシュファイル(対象値)
    (配布値 / 'cosl-distribution.json').write_text(json.dumps(報告値, ensure_ascii=False, indent=2) + '\n')
    return 対象値


if __name__ == '__main__':
    構文解析器 = argparse.ArgumentParser(description=__doc__)
    構文解析器.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    値 = 構文解析器.parse_args()
    if 値.command == 'bundle':
        print('COSL source/relink kit:', 実行束梱包())
    else:
        print(json.dumps(状況調査(), ensure_ascii=False, indent=2))
