#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from 命令実行 import 計画根


def 起動処理():
    配布経路 = 計画根 / 'dist'
    配布経路.mkdir(exist_ok=True)
    POSIX = 計画根.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(計画根 / 'build')) as 作業中経路:
        開発道具一式 = Path(作業中経路) / 'jkoros-native-sdk'
        ファイル一覧 = {
            計画根.parents[1] / 'LICENSE': 'LICENSE',
            計画根.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            計画根 / '道具/SDKコンパイル.py': 'compile.py',
            計画根 / '利用者/呼出.h': 'include/呼出.h',
            計画根 / '命名/機械連結名前一覧.h': '命名/機械連結名前一覧.h',
            計画根 / '利用者/連結配置.ld': 'user.ld',
            POSIX / 'ヘッダー/ファイルABI.h': 'include/ファイルABI.h',
            POSIX / 'ヘッダー/通信網ABI.h': 'include/通信網ABI.h',
            計画根 / 'build/user/start.o': 'lib/start.o',
            計画根 / 'build/user/runtime.o': 'lib/runtime.o',
            計画根 / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            計画根 / '利用者/ファイル例.cpp': 'examples/ファイル例.cpp',
            計画根 / '用例/ハングル符号化方式/挨拶例.c': 'examples/挨拶例.c',
            計画根 / '用例/ハングル符号化方式/ストリーム値.c': 'examples/ストリーム値.c',
            計画根 / '用例/ハングル符号化方式/挨拶例.cpp': 'examples/挨拶例.cpp',
            計画根 / '利用者/通信用例.cpp': 'examples/通信用例.cpp',
            計画根 / 'build/user/demo.elf': 'examples/demo.elf',
            計画根 / 'build/user/network.elf': 'examples/network.elf',
        }
        束管理目録 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 原本データ, 対象値 in ファイル一覧.items():
            宛先データ番地 = 開発道具一式 / 対象値
            宛先データ番地.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(原本データ), str(宛先データ番地))
            束管理目録['sha256'][対象値] = hashlib.sha256(宛先データ番地.read_bytes()).hexdigest()
        (開発道具一式 / 'manifest.json').write_text(json.dumps(束管理目録, indent=2) + '\n')
        (開発道具一式 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ファイル例.cpp -o demo.elf\n'
            'python3 compile.py examples/挨拶例.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int 利用者プログラム開始処理(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: 道具/命令実行.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 道具/ファイル実行.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 利用者引数個数()/利用者引数() in 呼出.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        書庫 = Path(作業中経路) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(書庫), 'w:gz') as 結果データ:
            結果データ.add(str(開発道具一式), arcname=開発道具一式.name)
        書庫.replace(配布経路 / 書庫.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        コンパイラ書庫 = Path(作業中経路) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(コンパイラ書庫), 'w:gz') as 結果データ:
            for 名前 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                結果データ.add(str(計画根.parents[1] / 名前), arcname='jkoros-native/' + 名前)
            for 相対経路 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'Cコンパイラ', '利用者', '命名',
                             '道具/Cコンパイラ構築.py', '道具/利用者空間構築.py', 'ファイル転送論理積翻訳工程.md'):
                結果データ.add(str(計画根 / 相対経路), arcname='jkoros-native/' + 相対経路)
            for 名前 in ('crt.o', 'aot-runtime.o', '実行環境支援.o', '起動処理.o', '事前用時間.o', '復帰橋渡し.o'):
                宛先ファイル = 計画根 / 'build/ccompiler' / 名前
                結果データ.add(str(宛先ファイル), arcname='jkoros-native/relink/' + 名前)
            for 名前 in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                結果データ.add(str(計画根 / 'build/user' / 名前), arcname='jkoros-native/relink/user/' + 名前)
            結果データ.add(str(計画根 / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            結果データ.add(str(POSIX), arcname='posix-kor/arm64-native')
        コンパイラ書庫.replace(配布経路 / コンパイラ書庫.name)
    print('SDK:', 配布経路 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    起動処理()
