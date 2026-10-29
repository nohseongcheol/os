"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 정적 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from la_distanță_Setări import Pregătiți


def crea_la_distanță(Project_rădăcină, compilator_instrument, Arhivă_instrument, Setări, executa_comandă):
    Rezultat = Project_rădăcină / 'build/remote'
    Rezultat.mkdir(exist_ok=True)
    Pregătiți(Project_rădăcină)
    securizat_shell = Project_rădăcină / 'vendor/libassh/src'
    parolă_VALUE = Project_rădăcină / 'vendor/bearssl'
    nucleu = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [securizat_shell / ('assh_' + Nume + '.c') for Nume in nucleu]
    for model_VALUE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(securizat_shell.glob(model_VALUE))
    원본들 += [securizat_shell / (Nume + '.c') for Nume in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Argumente = Setări + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', Project_rădăcină / 'la_distanță_VALUE', '-I', Rezultat, '-I', securizat_shell,
                    '-I', parolă_VALUE / 'inc', '-I', parolă_VALUE / 'src', '-isystem', '/usr/include/newlib']
    def BIND_participant(Nume, cale_Listă, 접두):
        목적들 = []
        for Cale in cale_Listă:
            destinație_VALUE = Rezultat / (접두 + Cale.stem + '.o')
            executa_comandă([compilator_instrument] + Argumente + ['-c', Cale, '-o', destinație_VALUE])
            목적들.append(destinație_VALUE)
        with tempfile.TemporaryDirectory(dir=str(Rezultat)) as 임시:
            grup_VALUE = Path(임시) / Nume
            executa_comandă([Arhivă_instrument, 'rcs', grup_VALUE] + 목적들)
            grup_VALUE.replace(Rezultat / Nume)
        return Rezultat / Nume
    BIND_participant('libassh.a', 원본들, 'assh-')
    (Rezultat / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(Cale.relative_to(Project_rădăcină)) for Cale in 원본들],
        'flags': list(map(str, Setări)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    computer_fără_sistem_de_operare_sursă = [parolă_VALUE / 'src' / (Nume + '.c') for Nume in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_participant('libbearssl.a', computer_fără_sistem_de_operare_sursă, 'bear-')
    return BIND_participant('libremote.a', sorted((Project_rădăcină / 'la_distanță_VALUE').glob('*.c')), '')
