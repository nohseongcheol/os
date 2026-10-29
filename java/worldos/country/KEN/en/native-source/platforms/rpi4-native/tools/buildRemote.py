"""LGPL libassh와 MIT BearSSL을 각각 보존하여 reconnectEndpoint 가능한 staticValue 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from remoteSettings import prepare


def createRemote(projectRoot, compilerTool, archiveTool, settings, executeCommand):
    Output = projectRoot / 'build/remote'
    Output.mkdir(exist_ok=True)
    prepare(projectRoot)
    secureShell = projectRoot / 'vendor/libassh/src'
    passwordValue = projectRoot / 'vendor/bearssl'
    Kernel = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    originalsList = [secureShell / ('assh_' + name + '.c') for name in Kernel]
    for patternValue in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        originalsList += sorted(secureShell.glob(patternValue))
    originalsList += [secureShell / (name + '.c') for name in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    arguments = settings + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', projectRoot / 'remoteValue', '-I', Output, '-I', secureShell,
                    '-I', passwordValue / 'inc', '-I', passwordValue / 'src', '-isystem', '/usr/include/newlib']
    def bindEndpoint(name, pathList, prefixValue):
        destinations = []
        for path in pathList:
            destinationValue = Output / (prefixValue + path.stem + '.o')
            executeCommand([compilerTool] + arguments + ['-c', path, '-o', destinationValue])
            destinations.append(destinationValue)
        with tempfile.TemporaryDirectory(dir=str(Output)) as temporaryValue:
            groupValue = Path(temporaryValue) / name
            executeCommand([archiveTool, 'rcs', groupValue] + destinations)
            groupValue.replace(Output / name)
        return Output / name
    bindEndpoint('libassh.a', originalsList, 'assh-')
    (Output / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(path.relative_to(projectRoot)) for path in originalsList],
        'flags': list(map(str, settings)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    bareMetalSource = [passwordValue / 'src' / (name + '.c') for name in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    bindEndpoint('libbearssl.a', bareMetalSource, 'bear-')
    return bindEndpoint('libremote.a', sorted((projectRoot / 'remoteValue').glob('*.c')), '')
