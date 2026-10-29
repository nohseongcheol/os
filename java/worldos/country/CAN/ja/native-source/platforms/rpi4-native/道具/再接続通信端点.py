#!/usr/bin/env python3
"""配布値 묶음에서 libassh/TinyCC를 교체하고 内蔵 커널을 再試行処理値 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

計画根 = Path(__file__).resolve().parent


def 命令実行(語本文):
    subprocess.check_call([str(入口値) for 入口値 in 語本文], cwd=str(計画根))


def 起動処理():
    構文解析器 = argparse.ArgumentParser(description=__doc__)
    構文解析器.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 検証')
    構文解析器.add_argument('--libassh-archive', type=Path, help='별도로 値改変·컴파일한 libassh.a 使用値')
    構文解析器.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 再試行処理値 컴파일하고 커널에 탑재')
    構文解析器.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    引数 = 構文解析器.parse_args()
    仕様 = json.loads((計画根 / 'relink.json').read_text())
    システム構築 = 計画根 / 'build'
    新規束 = システム構築 / 'relinked'
    新規束.mkdir(exist_ok=True)
    コンパイラ道具要素 = os.environ.get('ARM64_CC', 'clang')
    接続器 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    書庫道具要素 = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    遠隔設定値 = json.loads((システム構築 / 'remote/libassh-build.json').read_text())
    設定値 = 遠隔設定値['flags']
    if 引数.libassh_archive:
        安全性束 = 引数.libassh_archive.resolve()
    else:
        宛先一覧 = []
        ヘッダー = ['-I', 計画根 / '遠隔値', '-I', 計画根 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for 名前 in 遠隔設定値['sources']:
            宛先値 = 新規束 / (Path(名前).stem + '.o')
            命令実行([コンパイラ道具要素] + 設定値 + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + ヘッダー +
                 ['-c', 計画根 / 名前, '-o', 宛先値])
            宛先一覧.append(宛先値)
        安全性束 = 新規束 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(新規束)) as 一時値:
            一時束 = Path(一時値) / 'libassh.a'
            命令実行([書庫道具要素, 'rcs', 一時束] + 宛先一覧)
            一時束.replace(安全性束)
    if 引数.tinycc:
        if not 引数.sdk:
            構文解析器.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        開発 = 引数.sdk.resolve()
        算術値 = sorted((開発 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 算術値 or not (開発 / 'usr/include/stdio.h').is_file():
            構文解析器.error('SDK must contain ARM64 musl headers and libgcc.a')
        有効側構成 = [選択状態値 for 選択状態値 in 設定値 if 選択状態値 != '-mgeneral-regs-only']
        宛先値 = 新規束 / 'コンパイラ道具要素.o'
        命令実行([コンパイラ道具要素] + 有効側構成 + ['-ffunction-sections', '-fdata-sections',
             '-I', 計画根 / 'Cコンパイラ', '-I', 計画根 / 'vendor/tinycc', '-I', 計画根 / '利用者',
             '-I', システム構築 / 'ccompiler', '-isystem', 開発 / 'usr/include', '-c', 計画根 / 'Cコンパイラ/コンパイラ道具要素.c', '-o', 宛先値])
        命令実行([接続器, '--gc-sections', '-T', 計画根 / '利用者/連結配置.ld', '-z', 'max-page-size=4096',
             '-o', システム構築 / 'user/cc.elf', システム構築 / 'user/start.o', システム構築 / 'user/runtime.o', 宛先値] +
             [システム構築 / 'ccompiler' / (名前 + '.o') for 名前 in ('実行環境支援', '起動処理', '事前用時間', '復帰橋渡し')] +
             [システム構築 / 'user' / (名前 + '.o') for 名前 in ('jar', 'tinflate', 'crc32', 'adler32')] + [算術値[-1]])
        先頭部値 = システム構築 / 'programs.h'
        先頭部値.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 判定等価: 判定等価.group(1) + str((システム構築 / 'user/cc.elf').stat().st_size), 先頭部値.read_text()))
        命令実行([コンパイラ道具要素] + 設定値 + ['-c', システム構築 / 'programs.S', '-o', 計画根 / 'objects/programs.o'])
        命令実行([コンパイラ道具要素] + 設定値 + ['-std=c11', '-I', 計画根 / 'posix-kor/arm64-native/ヘッダー', '-I', システム構築,
             '-c', 計画根 / '機械/利用者.c', '-o', 計画根 / 'objects/user.o'])
    命令実行([接続器, '--gc-sections', '-T', 計画根 / '起動/連結配置.ld', '-o', 新規束 / 'kernel.elf'] +
         [計画根 / 経路 for 経路 in 仕様['objects']] + ['--start-group'] +
         [安全性束 if 経路 == 'objects/libassh.a' else 計画根 / 経路 for 経路 in 仕様['libraries']] + ['--end-group'])
    命令実行([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 新規束 / 'kernel.elf', 新規束 / 'kernel8.img'])
    ハッシュファイル = hashlib.sha256((新規束 / 'kernel8.img').read_bytes()).hexdigest()
    if 引数.verify and ハッシュファイル != 仕様['kernel_sha256']:
        raise SystemExit('再接続通信端点 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ハッシュファイル)
    print('RELINK PASS', ハッシュファイル, 新規束 / 'kernel8.img')


if __name__ == '__main__':
    起動処理()
