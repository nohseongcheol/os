"""LGPL libassh와 MIT BearSSL을 각각 보존하여 重新连接端点 가능한 静态值 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from 远程设置 import 准备


def 创建远程(项目根, 编译器工具, 存档工具, 设置, 执行命令):
    输出 = 项目根 / 'build/remote'
    输出.mkdir(exist_ok=True)
    准备(项目根)
    安全命令壳 = 项目根 / 'vendor/libassh/src'
    密码值 = 项目根 / 'vendor/bearssl'
    内核 = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    原件列列表 = [安全命令壳 / ('assh_' + 名称 + '.c') for 名称 in 内核]
    for 样式值 in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        原件列列表 += sorted(安全命令壳.glob(样式值))
    原件列列表 += [安全命令壳 / (名称 + '.c') for 名称 in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    实参 = 设置 + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 项目根 / '远程值', '-I', 输出, '-I', 安全命令壳,
                    '-I', 密码值 / 'inc', '-I', 密码值 / 'src', '-isystem', '/usr/include/newlib']
    def 可执行束打包(名称, 路径列表, 前缀值):
        目的地列 = []
        for 路径 in 路径列表:
            目的地址值 = 输出 / (前缀值 + 路径.stem + '.o')
            执行命令([编译器工具] + 实参 + ['-c', 路径, '-o', 目的地址值])
            目的地列.append(目的地址值)
        with tempfile.TemporaryDirectory(dir=str(输出)) as 临时值:
            组值 = Path(临时值) / 名称
            执行命令([存档工具, 'rcs', 组值] + 目的地列)
            组值.replace(输出 / 名称)
        return 输出 / 名称
    可执行束打包('libassh.a', 原件列列表, 'assh-')
    (输出 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(路径.relative_to(项目根)) for 路径 in 原件列列表],
        'flags': list(map(str, 设置)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    裸机器层源代码 = [密码值 / 'src' / (名称 + '.c') for 名称 in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    可执行束打包('libbearssl.a', 裸机器层源代码, 'bear-')
    return 可执行束打包('libremote.a', sorted((项目根 / '远程值').glob('*.c')), '')
