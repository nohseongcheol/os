"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 statisk_värde 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from fjärr_Inställningar import Förbereda


def Skapa_fjärr(åtgärd_rot, kompilerare_verktyg, Arkiv_verktyg, Inställningar, köra_kommando):
    utmatningsposition = åtgärd_rot / 'build/remote'
    utmatningsposition.mkdir(exist_ok=True)
    Förbereda(åtgärd_rot)
    säker_Shell = åtgärd_rot / 'vendor/libassh/src'
    lösenord_värde = åtgärd_rot / 'vendor/bearssl'
    kärna = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [säker_Shell / ('assh_' + Namn + '.c') for Namn in kärna]
    for mönster_värde in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(säker_Shell.glob(mönster_värde))
    원본들 += [säker_Shell / (Namn + '.c') for Namn in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    argument = Inställningar + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', åtgärd_rot / 'fjärr_värde', '-I', utmatningsposition, '-I', säker_Shell,
                    '-I', lösenord_värde / 'inc', '-I', lösenord_värde / 'src', '-isystem', '/usr/include/newlib']
    def BIND_deltagare(Namn, väg_ange, 접두):
        목적들 = []
        for sökväg_2 in väg_ange:
            mål_värde = utmatningsposition / (접두 + sökväg_2.stem + '.o')
            köra_kommando([kompilerare_verktyg] + argument + ['-c', sökväg_2, '-o', mål_värde])
            목적들.append(mål_värde)
        with tempfile.TemporaryDirectory(dir=str(utmatningsposition)) as 임시:
            grupp_värde = Path(임시) / Namn
            köra_kommando([Arkiv_verktyg, 'rcs', grupp_värde] + 목적들)
            grupp_värde.replace(utmatningsposition / Namn)
        return utmatningsposition / Namn
    BIND_deltagare('libassh.a', 원본들, 'assh-')
    (utmatningsposition / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(sökväg_2.relative_to(åtgärd_rot)) for sökväg_2 in 원본들],
        'flags': list(map(str, Inställningar)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    dator_utan_operativsystem_källa = [lösenord_värde / 'src' / (Namn + '.c') for Namn in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_deltagare('libbearssl.a', dator_utan_operativsystem_källa, 'bear-')
    return BIND_deltagare('libremote.a', sorted((åtgärd_rot / 'fjärr_värde').glob('*.c')), '')
