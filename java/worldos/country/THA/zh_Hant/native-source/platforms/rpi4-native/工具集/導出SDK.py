#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from 執行命令 import 項目根


def 運行():
    分發路徑 = 項目根 / 'dist'
    分發路徑.mkdir(exist_ok=True)
    POSIX = 項目根.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(項目根 / 'build')) as 工作中路徑:
        開發工具套件 = Path(工作中路徑) / 'jkoros-native-sdk'
        檔案列表 = {
            項目根.parents[1] / 'LICENSE': 'LICENSE',
            項目根.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            項目根 / '工具集/SDK編譯.py': 'compile.py',
            項目根 / '使用者/調用.h': 'include/調用.h',
            項目根 / '命名/計算機連接名稱列.h': '命名/計算機連接名稱列.h',
            項目根 / '使用者/鏈接佈局.ld': 'user.ld',
            POSIX / '頭文件/檔案ABI.h': 'include/檔案ABI.h',
            POSIX / '頭文件/網路ABI.h': 'include/網路ABI.h',
            項目根 / 'build/user/start.o': 'lib/start.o',
            項目根 / 'build/user/runtime.o': 'lib/runtime.o',
            項目根 / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            項目根 / '使用者/檔案例.cpp': 'examples/檔案例.cpp',
            項目根 / '範例/韓文字母編碼方式/問候例.c': 'examples/問候例.c',
            項目根 / '範例/韓文字母編碼方式/流值.c': 'examples/流值.c',
            項目根 / '範例/韓文字母編碼方式/問候例.cpp': 'examples/問候例.cpp',
            項目根 / '使用者/通信範例.cpp': 'examples/通信範例.cpp',
            項目根 / 'build/user/demo.elf': 'examples/demo.elf',
            項目根 / 'build/user/network.elf': 'examples/network.elf',
        }
        捆綁構建清單 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 原始資料, 目標值 in 檔案列表.items():
            目的地址資料地址 = 開發工具套件 / 目標值
            目的地址資料地址.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(原始資料), str(目的地址資料地址))
            捆綁構建清單['sha256'][目標值] = hashlib.sha256(目的地址資料地址.read_bytes()).hexdigest()
        (開發工具套件 / 'manifest.json').write_text(json.dumps(捆綁構建清單, indent=2) + '\n')
        (開發工具套件 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/檔案例.cpp -o demo.elf\n'
            'python3 compile.py examples/問候例.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int 開始用戶程式(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: 工具集/執行命令.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 工具集/執行檔案.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 用戶實際參數個數()/用戶實際參數() in 調用.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        存檔 = Path(工作中路徑) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(存檔), 'w:gz') as 結果資料:
            結果資料.add(str(開發工具套件), arcname=開發工具套件.name)
        存檔.replace(分發路徑 / 存檔.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        編譯器存檔 = Path(工作中路徑) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(編譯器存檔), 'w:gz') as 結果資料:
            for 名稱 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                結果資料.add(str(項目根.parents[1] / 名稱), arcname='jkoros-native/' + 名稱)
            for 相對路徑 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C編譯器', '使用者', '命名',
                             '工具集/構建C編譯器.py', '工具集/構建用戶空間.py', '檔案傳送與編譯過程.md'):
                結果資料.add(str(項目根 / 相對路徑), arcname='jkoros-native/' + 相對路徑)
            for 名稱 in ('crt.o', 'aot-runtime.o', '運行時支持.o', '運行.o', '提前所屬時間.o', '發回橋接.o'):
                目的地址檔案 = 項目根 / 'build/ccompiler' / 名稱
                結果資料.add(str(目的地址檔案), arcname='jkoros-native/relink/' + 名稱)
            for 名稱 in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                結果資料.add(str(項目根 / 'build/user' / 名稱), arcname='jkoros-native/relink/user/' + 名稱)
            結果資料.add(str(項目根 / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            結果資料.add(str(POSIX), arcname='posix-kor/arm64-native')
        編譯器存檔.replace(分發路徑 / 編譯器存檔.name)
    print('SDK:', 分發路徑 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    運行()
