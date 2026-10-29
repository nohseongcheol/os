"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 statisk_VERDI 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from ekstern_Innstillinger import Forbered


def åpne_ekstern(speile_rot, kompilator_verktøy, Arkiv_verktøy, Innstillinger, Utfør_kommando):
    Utgang = speile_rot / 'build/remote'
    Utgang.mkdir(exist_ok=True)
    Forbered(speile_rot)
    sikker_Shell = speile_rot / 'vendor/libassh/src'
    passord_VERDI = speile_rot / 'vendor/bearssl'
    kjerne = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [sikker_Shell / ('assh_' + Navn + '.c') for Navn in kjerne]
    for mønster_VERDI in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(sikker_Shell.glob(mønster_VERDI))
    원본들 += [sikker_Shell / (Navn + '.c') for Navn in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Argumenter = Innstillinger + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', speile_rot / 'ekstern_VERDI_28edcfa1', '-I', Utgang, '-I', sikker_Shell,
                    '-I', passord_VERDI / 'inc', '-I', passord_VERDI / 'src', '-isystem', '/usr/include/newlib']
    def BIND_deltaker(Navn, bane_Liste, 접두):
        목적들 = []
        for Sti in bane_Liste:
            mål_VERDI = Utgang / (접두 + Sti.stem + '.o')
            Utfør_kommando([kompilator_verktøy] + Argumenter + ['-c', Sti, '-o', mål_VERDI])
            목적들.append(mål_VERDI)
        with tempfile.TemporaryDirectory(dir=str(Utgang)) as 임시:
            gruppe_VERDI = Path(임시) / Navn
            Utfør_kommando([Arkiv_verktøy, 'rcs', gruppe_VERDI] + 목적들)
            gruppe_VERDI.replace(Utgang / Navn)
        return Utgang / Navn
    BIND_deltaker('libassh.a', 원본들, 'assh-')
    (Utgang / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(Sti.relative_to(speile_rot)) for Sti in 원본들],
        'flags': list(map(str, Innstillinger)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    datamaskin_uten_operativsystem_kilde = [passord_VERDI / 'src' / (Navn + '.c') for Navn in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_deltaker('libbearssl.a', datamaskin_uten_operativsystem_kilde, 'bear-')
    return BIND_deltaker('libremote.a', sorted((speile_rot / 'ekstern_VERDI_28edcfa1').glob('*.c')), '')
