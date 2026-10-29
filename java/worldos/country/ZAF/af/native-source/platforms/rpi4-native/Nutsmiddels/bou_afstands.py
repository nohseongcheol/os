"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 staties_VALUE 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from afstands_Instellings import Maak_gereed


def Skep_afstands(Project_wortel, 번역기, Argief_nutsmiddel, Instellings, uitvoer_bevel):
    Afvoer = Project_wortel / 'build/remote'
    Afvoer.mkdir(exist_ok=True)
    Maak_gereed(Project_wortel)
    beveiligde_dop = Project_wortel / 'vendor/libassh/src'
    wagwoord_VALUE = Project_wortel / 'vendor/bearssl'
    kern = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [beveiligde_dop / ('assh_' + Naam + '.c') for Naam in kern]
    for patroon_VALUE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(beveiligde_dop.glob(patroon_VALUE))
    원본들 += [beveiligde_dop / (Naam + '.c') for Naam in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Instellings + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', Project_wortel / 'afstands_VALUE', '-I', Afvoer, '-I', beveiligde_dop,
                    '-I', wagwoord_VALUE / 'inc', '-I', wagwoord_VALUE / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(Naam, pad_Lys, 접두):
        목적들 = []
        for Pad in pad_Lys:
            bestemming_VALUE = Afvoer / (접두 + Pad.stem + '.o')
            uitvoer_bevel([번역기] + 인수 + ['-c', Pad, '-o', bestemming_VALUE])
            목적들.append(bestemming_VALUE)
        with tempfile.TemporaryDirectory(dir=str(Afvoer)) as 임시:
            Groep_VALUE = Path(임시) / Naam
            uitvoer_bevel([Argief_nutsmiddel, 'rcs', Groep_VALUE] + 목적들)
            Groep_VALUE.replace(Afvoer / Naam)
        return Afvoer / Naam
    묶기('libassh.a', 원본들, 'assh-')
    (Afvoer / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(Pad.relative_to(Project_wortel)) for Pad in 원본들],
        'flags': list(map(str, Instellings)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [wagwoord_VALUE / 'src' / (Naam + '.c') for Naam in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((Project_wortel / 'afstands_VALUE').glob('*.c')), '')
