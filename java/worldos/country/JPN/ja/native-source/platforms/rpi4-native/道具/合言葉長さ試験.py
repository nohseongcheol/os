#!/usr/bin/env python3
"""개인 接続状態 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from 遠隔設定値 import 用意
from COSL配布 import 宛先名前, ライブラリ

計画根 = Path(__file__).resolve().parents[1]


def 起動処理():
    出力 = 計画根 / 'build/verification/password-length'
    出力.mkdir(parents=True, exist_ok=True)
    個人設定値 = 計画根 / 'build/remote/access.json'
    原本設定値 = 個人設定値.read_bytes()
    報告値 = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 一時値:
            作業場試験 = Path(一時値)
            設定値経路 = 作業場試験 / 'build/remote'
            設定値経路.mkdir(parents=True)
            設定値ファイル = 設定値経路 / 'access.json'
            def 設定値書込(データ):
                設定値ファイル.write_text(json.dumps(データ, ensure_ascii=False) + '\n')
                設定値ファイル.chmod(0o600)
            def 設定値検証(シェル, 画面):
                設定値書込({'user': 'user', 'ssh_password': シェル, 'vnc_password': 画面})
                原本 = 設定値ファイル.read_bytes()
                用意(作業場試験)
                assert 設定値ファイル.read_bytes() == 原本, 'Settings were rewritten'
                先頭部値 = (設定値経路 / '動作設定.h').read_text()
                判定等価 = re.search(r'画面合言葉\[\] = \{([^}]+)\}', 先頭部値)
                assert 判定等価 and len(判定等価.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (設定値経路 / '動作設定.h').stat().st_mode & 0o777 == 0o600
            for シェル, 画面 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                設定値検証(シェル, 画面)
            報告値['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for 値変更, 入口値 in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                データ = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                データ.update(値変更)
                設定値書込(データ)
                try:
                    用意(作業場試験)
                except SystemExit as エラー:
                    assert 入口値 in str(エラー), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + 入口値)
            報告値['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            設定値 = json.loads((計画根 / 'build/remote/libassh-build.json').read_text())['flags']
            コンパイラ道具要素 = os.environ.get('ARM64_CC', 'clang')
            接続器 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            書庫道具要素 = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def 命令実行(引数, 履歴記録記録):
                subprocess.run(list(map(str, 引数)), cwd=str(計画根), stdout=履歴記録記録,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for 名前, シェル, 画面 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + 名前, flush=True)
                設定値検証(シェル, 画面)
                結果 = 出力 / 名前
                結果.mkdir(exist_ok=True)
                with (結果 / 'build.log').open('wb') as 履歴記録記録:
                    宛先一覧 = []
                    for 原本 in sorted((計画根 / '遠隔値').glob('*.c')):
                        宛先値 = 作業場試験 / (原本.stem + '.o')
                        命令実行([コンパイラ道具要素] + 設定値 + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', 設定値経路, '-I', 計画根 / '遠隔値', '-I', 計画根 / 'vendor/libassh/src',
                             '-I', 計画根 / 'vendor/bearssl/inc', '-I', 計画根 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 原本, '-o', 宛先値], 履歴記録記録)
                        宛先一覧.append(宛先値)
                    遠隔束 = 作業場試験 / 'libremote.a'
                    命令実行([書庫道具要素, 'rcs', 遠隔束] + 宛先一覧, 履歴記録記録)
                    命令実行([接続器, '--gc-sections', '-T', 計画根 / '起動/連結配置.ld', '-o', 作業場試験 / 'kernel.elf'] +
                         [計画根 / 'build' / (名前 + '.o') for 名前 in 宛先名前] + ['--start-group'] +
                         [遠隔束 if 経路 == 'remote/libremote.a' else 計画根 / 'build' / 経路 for 経路 in ライブラリ] + ['--end-group'], 履歴記録記録)
                    命令実行([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         作業場試験 / 'kernel.elf', 作業場試験 / 'kernel8.img'], 履歴記録記録)
                with (結果 / 'remote-test.log').open('wb') as 履歴記録記録:
                    命令実行(['python3', 計画根 / '道具/遠隔接続状態試験.py', '--kernel', 作業場試験 / 'kernel8.img',
                         '--access', 設定値ファイル, '--output', 結果], 履歴記録記録)
                妥当性検査 = json.loads((結果 / 'report.json').read_text())
                assert 妥当性検査['passed']
                報告値['checks'].append(名前 + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        報告値['passed'] = True
    finally:
        報告値['personal_settings_unchanged'] = 個人設定値.read_bytes() == 原本設定値
        if not 報告値['personal_settings_unchanged']:
            報告値['passed'] = False
        報告値['kernel_sha256'] = hashlib.sha256((計画根 / 'build/kernel8.img').read_bytes()).hexdigest()
        (出力 / 'report.json').write_text(json.dumps(報告値, ensure_ascii=False, indent=2) + '\n')
    assert 報告値['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(報告値, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    起動処理()
