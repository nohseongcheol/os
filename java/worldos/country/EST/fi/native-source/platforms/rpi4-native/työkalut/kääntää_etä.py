"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 staattinen_ARVO 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from etä_Asetukset import Valmistele


def Luo_etä(aloite_juuri, kääntäjä_työkalu, Arkisto_työkalu, Asetukset, Suorita_komento):
    tulostuspaikka = aloite_juuri / 'build/remote'
    tulostuspaikka.mkdir(exist_ok=True)
    Valmistele(aloite_juuri)
    suojattu_liittymä = aloite_juuri / 'vendor/libassh/src'
    salasana_ARVO = aloite_juuri / 'vendor/bearssl'
    ydin = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [suojattu_liittymä / ('assh_' + Nimi + '.c') for Nimi in ydin]
    for kuvio_ARVO in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(suojattu_liittymä.glob(kuvio_ARVO))
    원본들 += [suojattu_liittymä / (Nimi + '.c') for Nimi in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    argumentit = Asetukset + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', aloite_juuri / 'etä_ARVO', '-I', tulostuspaikka, '-I', suojattu_liittymä,
                    '-I', salasana_ARVO / 'inc', '-I', salasana_ARVO / 'src', '-isystem', '/usr/include/newlib']
    def BIND_päätepiste(Nimi, polku_luettelo, 접두):
        목적들 = []
        for polku_2 in polku_luettelo:
            kohde_ARVO = tulostuspaikka / (접두 + polku_2.stem + '.o')
            Suorita_komento([kääntäjä_työkalu] + argumentit + ['-c', polku_2, '-o', kohde_ARVO])
            목적들.append(kohde_ARVO)
        with tempfile.TemporaryDirectory(dir=str(tulostuspaikka)) as 임시:
            Ryhmä_ARVO = Path(임시) / Nimi
            Suorita_komento([Arkisto_työkalu, 'rcs', Ryhmä_ARVO] + 목적들)
            Ryhmä_ARVO.replace(tulostuspaikka / Nimi)
        return tulostuspaikka / Nimi
    BIND_päätepiste('libassh.a', 원본들, 'assh-')
    (tulostuspaikka / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(polku_2.relative_to(aloite_juuri)) for polku_2 in 원본들],
        'flags': list(map(str, Asetukset)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    käyttöjärjestelmätön_tietokone_lähde = [salasana_ARVO / 'src' / (Nimi + '.c') for Nimi in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_päätepiste('libbearssl.a', käyttöjärjestelmätön_tietokone_lähde, 'bear-')
    return BIND_päätepiste('libremote.a', sorted((aloite_juuri / 'etä_ARVO').glob('*.c')), '')
