"""LGPL libassh와 MIT BearSSL을 각각 보존하여 再接続通信端点 가능한 静的値 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from 遠隔設定値 import 用意


def 遠隔作成(計画根, コンパイラ道具要素, 書庫道具要素, 設定値, 命令実行):
    出力 = 計画根 / 'build/remote'
    出力.mkdir(exist_ok=True)
    用意(計画根)
    保安シェル = 計画根 / 'vendor/libassh/src'
    合言葉値 = 計画根 / 'vendor/bearssl'
    中核 = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    原本一覧一覧 = [保安シェル / ('assh_' + 名前 + '.c') for 名前 in 中核]
    for 模様値 in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        原本一覧一覧 += sorted(保安シェル.glob(模様値))
    原本一覧一覧 += [保安シェル / (名前 + '.c') for 名前 in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    引数 = 設定値 + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 計画根 / '遠隔値', '-I', 出力, '-I', 保安シェル,
                    '-I', 合言葉値 / 'inc', '-I', 合言葉値 / 'src', '-isystem', '/usr/include/newlib']
    def 実行束梱包(名前, 経路一覧, 接頭辞値):
        宛先一覧 = []
        for 経路 in 経路一覧:
            宛先値 = 出力 / (接頭辞値 + 経路.stem + '.o')
            命令実行([コンパイラ道具要素] + 引数 + ['-c', 経路, '-o', 宛先値])
            宛先一覧.append(宛先値)
        with tempfile.TemporaryDirectory(dir=str(出力)) as 一時値:
            集合値 = Path(一時値) / 名前
            命令実行([書庫道具要素, 'rcs', 集合値] + 宛先一覧)
            集合値.replace(出力 / 名前)
        return 出力 / 名前
    実行束梱包('libassh.a', 原本一覧一覧, 'assh-')
    (出力 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(経路.relative_to(計画根)) for 経路 in 原本一覧一覧],
        'flags': list(map(str, 設定値)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    裸機械層ソース = [合言葉値 / 'src' / (名前 + '.c') for 名前 in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    実行束梱包('libbearssl.a', 裸機械層ソース, 'bear-')
    return 実行束梱包('libremote.a', sorted((計画根 / '遠隔値').glob('*.c')), '')
