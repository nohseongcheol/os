"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 정적 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from vzdialený_Nastavenia import Pripraviť


def Create_vzdialený(akcia_koreň, kompilátor_nástroj, Archív_nástroj, Nastavenia, Vykonať_príkaz):
    Výstup = akcia_koreň / 'build/remote'
    Výstup.mkdir(exist_ok=True)
    Pripraviť(akcia_koreň)
    보안셸 = akcia_koreň / 'vendor/libassh/src'
    heslo_VALUE = akcia_koreň / 'vendor/bearssl'
    jadro = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [보안셸 / ('assh_' + Názov + '.c') for Názov in jadro]
    for vzor_VALUE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(보안셸.glob(vzor_VALUE))
    원본들 += [보안셸 / (Názov + '.c') for Názov in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Argumenty = Nastavenia + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', akcia_koreň / 'vzdialený_VALUE', '-I', Výstup, '-I', 보안셸,
                    '-I', heslo_VALUE / 'inc', '-I', heslo_VALUE / 'src', '-isystem', '/usr/include/newlib']
    def BIND_účastník(Názov, cesta_Zoznam, 접두):
        목적들 = []
        for Cesta in cesta_Zoznam:
            cieľ_VALUE = Výstup / (접두 + Cesta.stem + '.o')
            Vykonať_príkaz([kompilátor_nástroj] + Argumenty + ['-c', Cesta, '-o', cieľ_VALUE])
            목적들.append(cieľ_VALUE)
        with tempfile.TemporaryDirectory(dir=str(Výstup)) as 임시:
            Skupina_VALUE = Path(임시) / Názov
            Vykonať_príkaz([Archív_nástroj, 'rcs', Skupina_VALUE] + 목적들)
            Skupina_VALUE.replace(Výstup / Názov)
        return Výstup / Názov
    BIND_účastník('libassh.a', 원본들, 'assh-')
    (Výstup / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(Cesta.relative_to(akcia_koreň)) for Cesta in 원본들],
        'flags': list(map(str, Nastavenia)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    čistý_počítač_zdroj = [heslo_VALUE / 'src' / (Názov + '.c') for Názov in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_účastník('libbearssl.a', čistý_počítač_zdroj, 'bear-')
    return BIND_účastník('libremote.a', sorted((akcia_koreň / 'vzdialený_VALUE').glob('*.c')), '')
