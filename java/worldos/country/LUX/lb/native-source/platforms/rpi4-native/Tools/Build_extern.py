"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 statesch_VALUE 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from extern_Astellungen import Préparéieren


def Create_extern(projezéieren_Racinn, 번역기, Archiv_Tool, Astellungen, ausféieren_Befeel):
    출력 = projezéieren_Racinn / 'build/remote'
    출력.mkdir(exist_ok=True)
    Préparéieren(projezéieren_Racinn)
    sécher_Shell = projezéieren_Racinn / 'vendor/libassh/src'
    Passwuert_VALUE = projezéieren_Racinn / 'vendor/bearssl'
    Kernel = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [sécher_Shell / ('assh_' + Numm + '.c') for Numm in Kernel]
    for Modell_VALUE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(sécher_Shell.glob(Modell_VALUE))
    원본들 += [sécher_Shell / (Numm + '.c') for Numm in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Astellungen + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', projezéieren_Racinn / 'extern_VALUE', '-I', 출력, '-I', sécher_Shell,
                    '-I', Passwuert_VALUE / 'inc', '-I', Passwuert_VALUE / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(Numm, Wee_Lëscht, 접두):
        목적들 = []
        for Wee in Wee_Lëscht:
            Zil_VALUE = 출력 / (접두 + Wee.stem + '.o')
            ausféieren_Befeel([번역기] + 인수 + ['-c', Wee, '-o', Zil_VALUE])
            목적들.append(Zil_VALUE)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            Grupp_VALUE = Path(임시) / Numm
            ausféieren_Befeel([Archiv_Tool, 'rcs', Grupp_VALUE] + 목적들)
            Grupp_VALUE.replace(출력 / Numm)
        return 출력 / Numm
    묶기('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(Wee.relative_to(projezéieren_Racinn)) for Wee in 원본들],
        'flags': list(map(str, Astellungen)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [Passwuert_VALUE / 'src' / (Numm + '.c') for Numm in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((projezéieren_Racinn / 'extern_VALUE').glob('*.c')), '')
