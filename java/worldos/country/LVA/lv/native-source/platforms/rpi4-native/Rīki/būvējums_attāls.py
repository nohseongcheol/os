"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 정적 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from attāls_Iestatījumi import Sagatavot


def atvērt_attāls(Project_sakne, kompilators_rīks, Arhīvs_rīks, Uzstādījumi, Izpildīt_komanda):
    Izvade = Project_sakne / 'build/remote'
    Izvade.mkdir(exist_ok=True)
    Sagatavot(Project_sakne)
    drošs_čaula = Project_sakne / 'vendor/libassh/src'
    parole_VALUE = Project_sakne / 'vendor/bearssl'
    kodols = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [drošs_čaula / ('assh_' + Nosaukums + '.c') for Nosaukums in kodols]
    for raksts_VALUE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(drošs_čaula.glob(raksts_VALUE))
    원본들 += [drošs_čaula / (Nosaukums + '.c') for Nosaukums in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Parametri = Uzstādījumi + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', Project_sakne / 'attāls_VALUE', '-I', Izvade, '-I', drošs_čaula,
                    '-I', parole_VALUE / 'inc', '-I', parole_VALUE / 'src', '-isystem', '/usr/include/newlib']
    def BIND_dalībnieks(Nosaukums, ceļš_Saraksts, 접두):
        목적들 = []
        for CEĻŠ in ceļš_Saraksts:
            mērķis_VALUE = Izvade / (접두 + CEĻŠ.stem + '.o')
            Izpildīt_komanda([kompilators_rīks] + Parametri + ['-c', CEĻŠ, '-o', mērķis_VALUE])
            목적들.append(mērķis_VALUE)
        with tempfile.TemporaryDirectory(dir=str(Izvade)) as 임시:
            Grupa_VALUE = Path(임시) / Nosaukums
            Izpildīt_komanda([Arhīvs_rīks, 'rcs', Grupa_VALUE] + 목적들)
            Grupa_VALUE.replace(Izvade / Nosaukums)
        return Izvade / Nosaukums
    BIND_dalībnieks('libassh.a', 원본들, 'assh-')
    (Izvade / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(CEĻŠ.relative_to(Project_sakne)) for CEĻŠ in 원본들],
        'flags': list(map(str, Uzstādījumi)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    dators_bez_operētājsistēmas_avots = [parole_VALUE / 'src' / (Nosaukums + '.c') for Nosaukums in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_dalībnieks('libbearssl.a', dators_bez_operētājsistēmas_avots, 'bear-')
    return BIND_dalībnieks('libremote.a', sorted((Project_sakne / 'attāls_VALUE').glob('*.c')), '')
