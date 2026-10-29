#!/usr/bin/env python3
"""개인 接通狀態 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from 遠程設置 import 準備
from COSL分發 import 目的地址名稱, 庫

項目根 = Path(__file__).resolve().parents[1]


def 運行():
    輸出 = 項目根 / 'build/verification/password-length'
    輸出.mkdir(parents=True, exist_ok=True)
    個人設置 = 項目根 / 'build/remote/access.json'
    原始設置 = 個人設置.read_bytes()
    報告值 = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 臨時值:
            測試工作區 = Path(臨時值)
            設置路徑 = 測試工作區 / 'build/remote'
            設置路徑.mkdir(parents=True)
            設置檔案 = 設置路徑 / 'access.json'
            def 寫入設置(資料):
                設置檔案.write_text(json.dumps(資料, ensure_ascii=False) + '\n')
                設置檔案.chmod(0o600)
            def 驗證設置(命令殼, 屏幕):
                寫入設置({'user': 'user', 'ssh_password': 命令殼, 'vnc_password': 屏幕})
                原始 = 設置檔案.read_bytes()
                準備(測試工作區)
                assert 設置檔案.read_bytes() == 原始, 'Settings were rewritten'
                頭值 = (設置路徑 / '配置檔.h').read_text()
                是否相等 = re.search(r'屏幕密碼\[\] = \{([^}]+)\}', 頭值)
                assert 是否相等 and len(是否相等.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (設置路徑 / '配置檔.h').stat().st_mode & 0o777 == 0o600
            for 命令殼, 屏幕 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                驗證設置(命令殼, 屏幕)
            報告值['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for 更改值, 條目值 in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                資料 = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                資料.update(更改值)
                寫入設置(資料)
                try:
                    準備(測試工作區)
                except SystemExit as 錯誤:
                    assert 條目值 in str(錯誤), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + 條目值)
            報告值['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            設置 = json.loads((項目根 / 'build/remote/libassh-build.json').read_text())['flags']
            編譯器工具 = os.environ.get('ARM64_CC', 'clang')
            連接器 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            存檔工具 = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def 執行命令(實參, 日誌記錄):
                subprocess.run(list(map(str, 實參)), cwd=str(項目根), stdout=日誌記錄,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for 名稱, 命令殼, 屏幕 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + 名稱, flush=True)
                驗證設置(命令殼, 屏幕)
                結果 = 輸出 / 名稱
                結果.mkdir(exist_ok=True)
                with (結果 / 'build.log').open('wb') as 日誌記錄:
                    目的地列 = []
                    for 原始 in sorted((項目根 / '遠程值').glob('*.c')):
                        目的地址值 = 測試工作區 / (原始.stem + '.o')
                        執行命令([編譯器工具] + 設置 + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', 設置路徑, '-I', 項目根 / '遠程值', '-I', 項目根 / 'vendor/libassh/src',
                             '-I', 項目根 / 'vendor/bearssl/inc', '-I', 項目根 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 原始, '-o', 目的地址值], 日誌記錄)
                        目的地列.append(目的地址值)
                    遠程捆綁 = 測試工作區 / 'libremote.a'
                    執行命令([存檔工具, 'rcs', 遠程捆綁] + 目的地列, 日誌記錄)
                    執行命令([連接器, '--gc-sections', '-T', 項目根 / '啓動/鏈接佈局.ld', '-o', 測試工作區 / 'kernel.elf'] +
                         [項目根 / 'build' / (名稱 + '.o') for 名稱 in 目的地址名稱] + ['--start-group'] +
                         [遠程捆綁 if 路徑 == 'remote/libremote.a' else 項目根 / 'build' / 路徑 for 路徑 in 庫] + ['--end-group'], 日誌記錄)
                    執行命令([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         測試工作區 / 'kernel.elf', 測試工作區 / 'kernel8.img'], 日誌記錄)
                with (結果 / 'remote-test.log').open('wb') as 日誌記錄:
                    執行命令(['python3', 項目根 / '工具集/遠程連接狀態測試.py', '--kernel', 測試工作區 / 'kernel8.img',
                         '--access', 設置檔案, '--output', 結果], 日誌記錄)
                有效性校驗 = json.loads((結果 / 'report.json').read_text())
                assert 有效性校驗['passed']
                報告值['checks'].append(名稱 + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        報告值['passed'] = True
    finally:
        報告值['personal_settings_unchanged'] = 個人設置.read_bytes() == 原始設置
        if not 報告值['personal_settings_unchanged']:
            報告值['passed'] = False
        報告值['kernel_sha256'] = hashlib.sha256((項目根 / 'build/kernel8.img').read_bytes()).hexdigest()
        (輸出 / 'report.json').write_text(json.dumps(報告值, ensure_ascii=False, indent=2) + '\n')
    assert 報告值['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(報告值, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    運行()
