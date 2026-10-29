"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 statig_VALUE 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from pell_Gosodiadau import Paratoi


def Creu_pell(prosiect_gwraidd, 번역기, Archif_offeryn, Gosodiadau, Gweithredu_gorchymyn):
    Allbwn = prosiect_gwraidd / 'build/remote'
    Allbwn.mkdir(exist_ok=True)
    Paratoi(prosiect_gwraidd)
    diogel_cragen = prosiect_gwraidd / 'vendor/libassh/src'
    cyfrinair_VALUE = prosiect_gwraidd / 'vendor/bearssl'
    cnewyllyn = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [diogel_cragen / ('assh_' + Enw + '.c') for Enw in cnewyllyn]
    for patrwm_VALUE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(diogel_cragen.glob(patrwm_VALUE))
    원본들 += [diogel_cragen / (Enw + '.c') for Enw in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Gosodiadau + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', prosiect_gwraidd / 'pell_VALUE', '-I', Allbwn, '-I', diogel_cragen,
                    '-I', cyfrinair_VALUE / 'inc', '-I', cyfrinair_VALUE / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(Enw, llwybr_Rhestr, 접두):
        목적들 = []
        for LLWYBR in llwybr_Rhestr:
            cyrchfan_VALUE = Allbwn / (접두 + LLWYBR.stem + '.o')
            Gweithredu_gorchymyn([번역기] + 인수 + ['-c', LLWYBR, '-o', cyrchfan_VALUE])
            목적들.append(cyrchfan_VALUE)
        with tempfile.TemporaryDirectory(dir=str(Allbwn)) as 임시:
            Grŵp_VALUE = Path(임시) / Enw
            Gweithredu_gorchymyn([Archif_offeryn, 'rcs', Grŵp_VALUE] + 목적들)
            Grŵp_VALUE.replace(Allbwn / Enw)
        return Allbwn / Enw
    묶기('libassh.a', 원본들, 'assh-')
    (Allbwn / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(LLWYBR.relative_to(prosiect_gwraidd)) for LLWYBR in 원본들],
        'flags': list(map(str, Gosodiadau)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [cyfrinair_VALUE / 'src' / (Enw + '.c') for Enw in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((prosiect_gwraidd / 'pell_VALUE').glob('*.c')), '')
