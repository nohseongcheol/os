#!/usr/bin/env python3
"""分發值 묶음에서 libassh/TinyCC를 교체하고 內建 커널을 重試值 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

項目根 = Path(__file__).resolve().parent


def 執行命令(機器字文本):
    subprocess.check_call([str(條目值) for 條目值 in 機器字文本], cwd=str(項目根))


def 運行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 驗證')
    解析器.add_argument('--libassh-archive', type=Path, help='별도로 修改值·컴파일한 libassh.a 使用值')
    解析器.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 重試值 컴파일하고 커널에 탑재')
    解析器.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    實參 = 解析器.parse_args()
    規格 = json.loads((項目根 / 'relink.json').read_text())
    構建系統 = 項目根 / 'build'
    新建捆綁 = 構建系統 / 'relinked'
    新建捆綁.mkdir(exist_ok=True)
    編譯器工具 = os.environ.get('ARM64_CC', 'clang')
    連接器 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    存檔工具 = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    遠程設置 = json.loads((構建系統 / 'remote/libassh-build.json').read_text())
    設置 = 遠程設置['flags']
    if 實參.libassh_archive:
        安全性捆綁 = 實參.libassh_archive.resolve()
    else:
        目的地列 = []
        頭文件 = ['-I', 項目根 / '遠程值', '-I', 項目根 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for 名稱 in 遠程設置['sources']:
            目的地址值 = 新建捆綁 / (Path(名稱).stem + '.o')
            執行命令([編譯器工具] + 設置 + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 頭文件 +
                 ['-c', 項目根 / 名稱, '-o', 目的地址值])
            目的地列.append(目的地址值)
        安全性捆綁 = 新建捆綁 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(新建捆綁)) as 臨時值:
            臨時捆綁 = Path(臨時值) / 'libassh.a'
            執行命令([存檔工具, 'rcs', 臨時捆綁] + 目的地列)
            臨時捆綁.replace(安全性捆綁)
    if 實參.tinycc:
        if not 實參.sdk:
            解析器.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        開發 = 實參.sdk.resolve()
        算術值 = sorted((開發 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 算術值 or not (開發 / 'usr/include/stdio.h').is_file():
            解析器.error('SDK must contain ARM64 musl headers and libgcc.a')
        啓用側設定配置 = [選中狀態值 for 選中狀態值 in 設置 if 選中狀態值 != '-mgeneral-regs-only']
        目的地址值 = 新建捆綁 / '編譯器工具.o'
        執行命令([編譯器工具] + 啓用側設定配置 + ['-ffunction-sections', '-fdata-sections',
             '-I', 項目根 / 'C編譯器', '-I', 項目根 / 'vendor/tinycc', '-I', 項目根 / '使用者',
             '-I', 構建系統 / 'ccompiler', '-isystem', 開發 / 'usr/include', '-c', 項目根 / 'C編譯器/編譯器工具.c', '-o', 目的地址值])
        執行命令([連接器, '--gc-sections', '-T', 項目根 / '使用者/鏈接佈局.ld', '-z', 'max-page-size=4096',
             '-o', 構建系統 / 'user/cc.elf', 構建系統 / 'user/start.o', 構建系統 / 'user/runtime.o', 目的地址值] +
             [構建系統 / 'ccompiler' / (名稱 + '.o') for 名稱 in ('運行時支持', '運行', '提前所屬時間', '發回橋接')] +
             [構建系統 / 'user' / (名稱 + '.o') for 名稱 in ('jar', 'tinflate', 'crc32', 'adler32')] + [算術值[-1]])
        頭值 = 構建系統 / 'programs.h'
        頭值.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 是否相等: 是否相等.group(1) + str((構建系統 / 'user/cc.elf').stat().st_size), 頭值.read_text()))
        執行命令([編譯器工具] + 設置 + ['-c', 構建系統 / 'programs.S', '-o', 項目根 / 'objects/programs.o'])
        執行命令([編譯器工具] + 設置 + ['-std=c11', '-I', 項目根 / 'posix-kor/arm64-native/頭文件', '-I', 構建系統,
             '-c', 項目根 / '計算機/使用者.c', '-o', 項目根 / 'objects/user.o'])
    執行命令([連接器, '--gc-sections', '-T', 項目根 / '啓動/鏈接佈局.ld', '-o', 新建捆綁 / 'kernel.elf'] +
         [項目根 / 路徑 for 路徑 in 規格['objects']] + ['--start-group'] +
         [安全性捆綁 if 路徑 == 'objects/libassh.a' else 項目根 / 路徑 for 路徑 in 規格['libraries']] + ['--end-group'])
    執行命令([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 新建捆綁 / 'kernel.elf', 新建捆綁 / 'kernel8.img'])
    哈希檔案 = hashlib.sha256((新建捆綁 / 'kernel8.img').read_bytes()).hexdigest()
    if 實參.verify and 哈希檔案 != 規格['kernel_sha256']:
        raise SystemExit('重新連接端點 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + 哈希檔案)
    print('RELINK PASS', 哈希檔案, 新建捆綁 / 'kernel8.img')


if __name__ == '__main__':
    運行()
