"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 정적 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from 원격설정 import 준비


def 원격만들기(기준, 번역기, 묶음도구, Axustes, 실행):
    Salida = 기준 / 'build/remote'
    Salida.mkdir(exist_ok=True)
    준비(기준)
    보안셸 = 기준 / 'vendor/libassh/src'
    암호 = 기준 / 'vendor/bearssl'
    핵심 = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [보안셸 / ('assh_' + Nome + '.c') for Nome in 핵심]
    for 패턴 in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(보안셸.glob(패턴))
    원본들 += [보안셸 / (Nome + '.c') for Nome in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Argumentu = Axustes + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 기준 / '원격', '-I', Salida, '-I', 보안셸,
                    '-I', 암호 / 'inc', '-I', 암호 / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(Nome, 경로들, 접두):
        목적들 = []
        for Camín in 경로들:
            목적 = Salida / (접두 + Camín.stem + '.o')
            실행([번역기] + Argumentu + ['-c', Camín, '-o', 목적])
            목적들.append(목적)
        with tempfile.TemporaryDirectory(dir=str(Salida)) as 임시:
            묶음 = Path(임시) / Nome
            실행([묶음도구, 'rcs', 묶음] + 목적들)
            묶음.replace(Salida / Nome)
        return Salida / Nome
    묶기('libassh.a', 원본들, 'assh-')
    (Salida / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(Camín.relative_to(기준)) for Camín in 원본들],
        'flags': list(map(str, Axustes)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [암호 / 'src' / (Nome + '.c') for Nome in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((기준 / '원격').glob('*.c')), '')
