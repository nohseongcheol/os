"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 tuli_thamani 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from kwa_mbali_Mipangilio import Andaa


def unda_kwa_mbali(기준, 번역기, Hifadhi_zana, Mipangilio, tekeleza_amri):
    출력 = 기준 / 'build/remote'
    출력.mkdir(exist_ok=True)
    Andaa(기준)
    salama_sheli = 기준 / 'vendor/libassh/src'
    nywila_thamani = 기준 / 'vendor/bearssl'
    kiini = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [salama_sheli / ('assh_' + Jina + '.c') for Jina in kiini]
    for ruwaza_thamani in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(salama_sheli.glob(ruwaza_thamani))
    원본들 += [salama_sheli / (Jina + '.c') for Jina in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Mipangilio + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 기준 / 'kwa_mbali_thamani', '-I', 출력, '-I', salama_sheli,
                    '-I', nywila_thamani / 'inc', '-I', nywila_thamani / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(Jina, njia_Orodha, 접두):
        목적들 = []
        for njia in njia_Orodha:
            fikio_thamani = 출력 / (접두 + njia.stem + '.o')
            tekeleza_amri([번역기] + 인수 + ['-c', njia, '-o', fikio_thamani])
            목적들.append(fikio_thamani)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            Kikundi_thamani = Path(임시) / Jina
            tekeleza_amri([Hifadhi_zana, 'rcs', Kikundi_thamani] + 목적들)
            Kikundi_thamani.replace(출력 / Jina)
        return 출력 / Jina
    묶기('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(njia.relative_to(기준)) for njia in 원본들],
        'flags': list(map(str, Mipangilio)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [nywila_thamani / 'src' / (Jina + '.c') for Jina in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((기준 / 'kwa_mbali_thamani').glob('*.c')), '')
