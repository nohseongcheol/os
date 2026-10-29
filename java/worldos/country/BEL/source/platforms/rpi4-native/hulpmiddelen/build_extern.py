"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 statisch_WAARDE 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from extern_Instellingen import Bereid_voor


def maken_extern(Taken_wortel, compiler_hulpmiddel, Archief_hulpmiddel, Instellingen, Uitvoeren_opdracht):
    tekstuitvoer = Taken_wortel / 'build/remote'
    tekstuitvoer.mkdir(exist_ok=True)
    Bereid_voor(Taken_wortel)
    veilig_Shell = Taken_wortel / 'vendor/libassh/src'
    wachtwoord_WAARDE = Taken_wortel / 'vendor/bearssl'
    Kern = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [veilig_Shell / ('assh_' + Naam + '.c') for Naam in Kern]
    for patroon_WAARDE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(veilig_Shell.glob(patroon_WAARDE))
    원본들 += [veilig_Shell / (Naam + '.c') for Naam in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    argumenten = Instellingen + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', Taken_wortel / 'extern_WAARDE_28edcfa1', '-I', tekstuitvoer, '-I', veilig_Shell,
                    '-I', wachtwoord_WAARDE / 'inc', '-I', wachtwoord_WAARDE / 'src', '-isystem', '/usr/include/newlib']
    def BIND_eindpunt(Naam, pad_Lijst, 접두):
        목적들 = []
        for pad in pad_Lijst:
            doel_WAARDE = tekstuitvoer / (접두 + pad.stem + '.o')
            Uitvoeren_opdracht([compiler_hulpmiddel] + argumenten + ['-c', pad, '-o', doel_WAARDE])
            목적들.append(doel_WAARDE)
        with tempfile.TemporaryDirectory(dir=str(tekstuitvoer)) as 임시:
            Groep_WAARDE = Path(임시) / Naam
            Uitvoeren_opdracht([Archief_hulpmiddel, 'rcs', Groep_WAARDE] + 목적들)
            Groep_WAARDE.replace(tekstuitvoer / Naam)
        return tekstuitvoer / Naam
    BIND_eindpunt('libassh.a', 원본들, 'assh-')
    (tekstuitvoer / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(pad.relative_to(Taken_wortel)) for pad in 원본들],
        'flags': list(map(str, Instellingen)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    bare_metalcomputer_bron = [wachtwoord_WAARDE / 'src' / (Naam + '.c') for Naam in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_eindpunt('libbearssl.a', bare_metalcomputer_bron, 'bear-')
    return BIND_eindpunt('libremote.a', sorted((Taken_wortel / 'extern_WAARDE_28edcfa1').glob('*.c')), '')
