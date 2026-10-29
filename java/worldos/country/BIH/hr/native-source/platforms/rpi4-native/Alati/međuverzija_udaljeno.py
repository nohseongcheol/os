"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 정적 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from udaljeno_Postavke import Pripremi


def Create_udaljeno(akcija_korijen, kompilator_alat, Arhiva_alat, Postavke, Izvrši_naredba):
    Izlaz = akcija_korijen / 'build/remote'
    Izlaz.mkdir(exist_ok=True)
    Pripremi(akcija_korijen)
    sigurno_ljuska = akcija_korijen / 'vendor/libassh/src'
    lozinka_VALUE = akcija_korijen / 'vendor/bearssl'
    jezgra_sustava = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [sigurno_ljuska / ('assh_' + Ime + '.c') for Ime in jezgra_sustava]
    for uzorak_VALUE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(sigurno_ljuska.glob(uzorak_VALUE))
    원본들 += [sigurno_ljuska / (Ime + '.c') for Ime in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Argumenti = Postavke + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', akcija_korijen / 'udaljeno_VALUE', '-I', Izlaz, '-I', sigurno_ljuska,
                    '-I', lozinka_VALUE / 'inc', '-I', lozinka_VALUE / 'src', '-isystem', '/usr/include/newlib']
    def BIND_sudionik(Ime, put_Popis, 접두):
        목적들 = []
        for PUTANJA in put_Popis:
            odredište_VALUE = Izlaz / (접두 + PUTANJA.stem + '.o')
            Izvrši_naredba([kompilator_alat] + Argumenti + ['-c', PUTANJA, '-o', odredište_VALUE])
            목적들.append(odredište_VALUE)
        with tempfile.TemporaryDirectory(dir=str(Izlaz)) as 임시:
            Grupa_VALUE = Path(임시) / Ime
            Izvrši_naredba([Arhiva_alat, 'rcs', Grupa_VALUE] + 목적들)
            Grupa_VALUE.replace(Izlaz / Ime)
        return Izlaz / Ime
    BIND_sudionik('libassh.a', 원본들, 'assh-')
    (Izlaz / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(PUTANJA.relative_to(akcija_korijen)) for PUTANJA in 원본들],
        'flags': list(map(str, Postavke)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    golo_računalo_izvor = [lozinka_VALUE / 'src' / (Ime + '.c') for Ime in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_sudionik('libbearssl.a', golo_računalo_izvor, 'bear-')
    return BIND_sudionik('libremote.a', sorted((akcija_korijen / 'udaljeno_VALUE').glob('*.c')), '')
