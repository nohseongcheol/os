"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 statičen_VALUE 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from oddaljen_Nastavitve import Pripravi


def Ustvari_oddaljen(pobuda_koren, prevajalnik_orodje, Arhiv_orodje, Nastavitve, Izvedi_ukaz):
    Izpis = pobuda_koren / 'build/remote'
    Izpis.mkdir(exist_ok=True)
    Pripravi(pobuda_koren)
    varen_lupina = pobuda_koren / 'vendor/libassh/src'
    geslo_VALUE = pobuda_koren / 'vendor/bearssl'
    jedro = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [varen_lupina / ('assh_' + Ime + '.c') for Ime in jedro]
    for vzorec_VALUE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(varen_lupina.glob(vzorec_VALUE))
    원본들 += [varen_lupina / (Ime + '.c') for Ime in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Argumenti = Nastavitve + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', pobuda_koren / 'oddaljen_VALUE', '-I', Izpis, '-I', varen_lupina,
                    '-I', geslo_VALUE / 'inc', '-I', geslo_VALUE / 'src', '-isystem', '/usr/include/newlib']
    def BIND_končna_točka(Ime, pot_Seznam, 접두):
        목적들 = []
        for POT in pot_Seznam:
            cilj_VALUE = Izpis / (접두 + POT.stem + '.o')
            Izvedi_ukaz([prevajalnik_orodje] + Argumenti + ['-c', POT, '-o', cilj_VALUE])
            목적들.append(cilj_VALUE)
        with tempfile.TemporaryDirectory(dir=str(Izpis)) as 임시:
            Skupina_VALUE = Path(임시) / Ime
            Izvedi_ukaz([Arhiv_orodje, 'rcs', Skupina_VALUE] + 목적들)
            Skupina_VALUE.replace(Izpis / Ime)
        return Izpis / Ime
    BIND_končna_točka('libassh.a', 원본들, 'assh-')
    (Izpis / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(POT.relative_to(pobuda_koren)) for POT in 원본들],
        'flags': list(map(str, Nastavitve)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    goli_računalnik_vir = [geslo_VALUE / 'src' / (Ime + '.c') for Ime in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_končna_točka('libbearssl.a', goli_računalnik_vir, 'bear-')
    return BIND_končna_točka('libremote.a', sorted((pobuda_koren / 'oddaljen_VALUE').glob('*.c')), '')
