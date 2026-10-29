"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 ولاړ_ارزښت 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from 원격설정 import 준비


def 원격만들기(기준, 번역기, ارشیف_توکى, امستنې, 실행):
    출력 = 기준 / 'build/remote'
    출력.mkdir(exist_ok=True)
    준비(기준)
    보안셸 = 기준 / 'vendor/libassh/src'
    تېرنويى_ارزښت = 기준 / 'vendor/bearssl'
    نوغی = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [보안셸 / ('assh_' + نوم + '.c') for نوم in نوغی]
    for بېلګه_ارزښت in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(보안셸.glob(بېلګه_ارزښت))
    원본들 += [보안셸 / (نوم + '.c') for نوم in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = امستنې + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 기준 / '원격', '-I', 출력, '-I', 보안셸,
                    '-I', تېرنويى_ارزښت / 'inc', '-I', تېرنويى_ارزښت / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(نوم, 경로들, 접두):
        목적들 = []
        for يونلور in 경로들:
            موخه_ارزښت = 출력 / (접두 + يونلور.stem + '.o')
            실행([번역기] + 인수 + ['-c', يونلور, '-o', موخه_ارزښت])
            목적들.append(موخه_ارزښت)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            ډله_ارزښت = Path(임시) / نوم
            실행([ارشیف_توکى, 'rcs', ډله_ارزښت] + 목적들)
            ډله_ارزښت.replace(출력 / نوم)
        return 출력 / نوم
    묶기('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(يونلور.relative_to(기준)) for يونلور in 원본들],
        'flags': list(map(str, امستنې)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [تېرنويى_ارزښت / 'src' / (نوم + '.c') for نوم in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((기준 / '원격').glob('*.c')), '')
