"""LGPL libassh와 MIT BearSSL을 각각 보존하여 重新連接端點 가능한 靜態值 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from 遠程設置 import 準備


def 創建遠程(項目根, 編譯器工具, 存檔工具, 設置, 執行命令):
    輸出 = 項目根 / 'build/remote'
    輸出.mkdir(exist_ok=True)
    準備(項目根)
    安全命令殼 = 項目根 / 'vendor/libassh/src'
    密碼值 = 項目根 / 'vendor/bearssl'
    內核 = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    原件列列表 = [安全命令殼 / ('assh_' + 名稱 + '.c') for 名稱 in 內核]
    for 樣式值 in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        原件列列表 += sorted(安全命令殼.glob(樣式值))
    原件列列表 += [安全命令殼 / (名稱 + '.c') for 名稱 in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    實參 = 設置 + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 項目根 / '遠程值', '-I', 輸出, '-I', 安全命令殼,
                    '-I', 密碼值 / 'inc', '-I', 密碼值 / 'src', '-isystem', '/usr/include/newlib']
    def 可執行束打包(名稱, 路徑列表, 前綴值):
        目的地列 = []
        for 路徑 in 路徑列表:
            目的地址值 = 輸出 / (前綴值 + 路徑.stem + '.o')
            執行命令([編譯器工具] + 實參 + ['-c', 路徑, '-o', 目的地址值])
            目的地列.append(目的地址值)
        with tempfile.TemporaryDirectory(dir=str(輸出)) as 臨時值:
            組值 = Path(臨時值) / 名稱
            執行命令([存檔工具, 'rcs', 組值] + 目的地列)
            組值.replace(輸出 / 名稱)
        return 輸出 / 名稱
    可執行束打包('libassh.a', 原件列列表, 'assh-')
    (輸出 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(路徑.relative_to(項目根)) for 路徑 in 原件列列表],
        'flags': list(map(str, 設置)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    裸機器層原始碼 = [密碼值 / 'src' / (名稱 + '.c') for 名稱 in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    可執行束打包('libbearssl.a', 裸機器層原始碼, 'bear-')
    return 可執行束打包('libremote.a', sorted((項目根 / '遠程值').glob('*.c')), '')
