"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 ngaguquki_inani 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from kude_Amasethingi import Hlela


def yakha_kude(기준, 번역기, londoloza_ithuluzi, Izinhlelo, yenza_umyalo):
    출력 = 기준 / 'build/remote'
    출력.mkdir(exist_ok=True)
    Hlela(기준)
    ivikelekile_isihumushi_miyalelo = 기준 / 'vendor/libassh/src'
    iphasiwedi_inani = 기준 / 'vendor/bearssl'
    ikhenela = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [ivikelekile_isihumushi_miyalelo / ('assh_' + Igama + '.c') for Igama in ikhenela]
    for iphethini_inani in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(ivikelekile_isihumushi_miyalelo.glob(iphethini_inani))
    원본들 += [ivikelekile_isihumushi_miyalelo / (Igama + '.c') for Igama in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Izinhlelo + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 기준 / 'kude_inani', '-I', 출력, '-I', ivikelekile_isihumushi_miyalelo,
                    '-I', iphasiwedi_inani / 'inc', '-I', iphasiwedi_inani / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(Igama, umzila_Uhlu, 접두):
        목적들 = []
        for Indlela_2 in umzila_Uhlu:
            isikhumulo_inani = 출력 / (접두 + Indlela_2.stem + '.o')
            yenza_umyalo([번역기] + 인수 + ['-c', Indlela_2, '-o', isikhumulo_inani])
            목적들.append(isikhumulo_inani)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            iqoqo_inani = Path(임시) / Igama
            yenza_umyalo([londoloza_ithuluzi, 'rcs', iqoqo_inani] + 목적들)
            iqoqo_inani.replace(출력 / Igama)
        return 출력 / Igama
    묶기('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(Indlela_2.relative_to(기준)) for Indlela_2 in 원본들],
        'flags': list(map(str, Izinhlelo)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [iphasiwedi_inani / 'src' / (Igama + '.c') for Igama in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((기준 / 'kude_inani').glob('*.c')), '')
