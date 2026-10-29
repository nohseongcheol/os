"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 정적 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from udaljen_Postavke import Pripremi


def Create_udaljen(radnja_koren, kompajler_alatka, Arhiva_alatka, Postavke, Izvrši_komanda):
    출력 = radnja_koren / 'build/remote'
    출력.mkdir(exist_ok=True)
    Pripremi(radnja_koren)
    bezbedan_ljuska = radnja_koren / 'vendor/libassh/src'
    lozinka_VALUE = radnja_koren / 'vendor/bearssl'
    jezgro = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [bezbedan_ljuska / ('assh_' + ime + '.c') for ime in jezgro]
    for šara_VALUE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(bezbedan_ljuska.glob(šara_VALUE))
    원본들 += [bezbedan_ljuska / (ime + '.c') for ime in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Postavke + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', radnja_koren / 'udaljen_VALUE', '-I', 출력, '-I', bezbedan_ljuska,
                    '-I', lozinka_VALUE / 'inc', '-I', lozinka_VALUE / 'src', '-isystem', '/usr/include/newlib']
    def povezati_učesnik(ime, putanja_Lista, 접두):
        목적들 = []
        for putanja in putanja_Lista:
            odredište_VALUE = 출력 / (접두 + putanja.stem + '.o')
            Izvrši_komanda([kompajler_alatka] + 인수 + ['-c', putanja, '-o', odredište_VALUE])
            목적들.append(odredište_VALUE)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            Grupa_VALUE = Path(임시) / ime
            Izvrši_komanda([Arhiva_alatka, 'rcs', Grupa_VALUE] + 목적들)
            Grupa_VALUE.replace(출력 / ime)
        return 출력 / ime
    povezati_učesnik('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(putanja.relative_to(radnja_koren)) for putanja in 원본들],
        'flags': list(map(str, Postavke)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    računar_bez_operativnog_sistema_izvor = [lozinka_VALUE / 'src' / (ime + '.c') for ime in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    povezati_učesnik('libbearssl.a', računar_bez_operativnog_sistema_izvor, 'bear-')
    return povezati_učesnik('libremote.a', sorted((radnja_koren / 'udaljen_VALUE').glob('*.c')), '')
