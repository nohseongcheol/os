"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 정적 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from nuotolinis_Parametrai import Parengti


def kurti_nuotolinis(Project_šaknis, kompiliatorius_įrankis, Archyvas_įrankis, Nustatymai, Vykdyti_komanda):
    Išvestis = Project_šaknis / 'build/remote'
    Išvestis.mkdir(exist_ok=True)
    Parengti(Project_šaknis)
    saugus_apvalkalas = Project_šaknis / 'vendor/libassh/src'
    slaptažodis_VALUE = Project_šaknis / 'vendor/bearssl'
    branduolys = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [saugus_apvalkalas / ('assh_' + Pavadinimas_2 + '.c') for Pavadinimas_2 in branduolys]
    for raštas_VALUE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(saugus_apvalkalas.glob(raštas_VALUE))
    원본들 += [saugus_apvalkalas / (Pavadinimas_2 + '.c') for Pavadinimas_2 in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Argumentai = Nustatymai + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', Project_šaknis / 'nuotolinis_VALUE', '-I', Išvestis, '-I', saugus_apvalkalas,
                    '-I', slaptažodis_VALUE / 'inc', '-I', slaptažodis_VALUE / 'src', '-isystem', '/usr/include/newlib']
    def BIND_dalyvis(Pavadinimas_2, kelias_Sąrašas, 접두):
        목적들 = []
        for KELIAS in kelias_Sąrašas:
            vieta_VALUE = Išvestis / (접두 + KELIAS.stem + '.o')
            Vykdyti_komanda([kompiliatorius_įrankis] + Argumentai + ['-c', KELIAS, '-o', vieta_VALUE])
            목적들.append(vieta_VALUE)
        with tempfile.TemporaryDirectory(dir=str(Išvestis)) as 임시:
            Grupė_VALUE = Path(임시) / Pavadinimas_2
            Vykdyti_komanda([Archyvas_įrankis, 'rcs', Grupė_VALUE] + 목적들)
            Grupė_VALUE.replace(Išvestis / Pavadinimas_2)
        return Išvestis / Pavadinimas_2
    BIND_dalyvis('libassh.a', 원본들, 'assh-')
    (Išvestis / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(KELIAS.relative_to(Project_šaknis)) for KELIAS in 원본들],
        'flags': list(map(str, Nustatymai)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    kompiuteris_be_operacinės_sistemos_šaltinis = [slaptažodis_VALUE / 'src' / (Pavadinimas_2 + '.c') for Pavadinimas_2 in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_dalyvis('libbearssl.a', kompiuteris_be_operacinės_sistemos_šaltinis, 'bear-')
    return BIND_dalyvis('libremote.a', sorted((Project_šaknis / 'nuotolinis_VALUE').glob('*.c')), '')
