"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 тұрақты_мән 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from 원격설정 import Дайындау


def 원격만들기(жоба_түбір, 번역기, Мұрағат_құрал, Баптаулар, орындау_пәрмен):
    Шығысы = жоба_түбір / 'build/remote'
    Шығысы.mkdir(exist_ok=True)
    Дайындау(жоба_түбір)
    қауіпсіз_қоршам = жоба_түбір / 'vendor/libassh/src'
    құпиясөз_мән = жоба_түбір / 'vendor/bearssl'
    ядро = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [қауіпсіз_қоршам / ('assh_' + Аты + '.c') for Аты in ядро]
    for үлгі_мән in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(қауіпсіз_қоршам.glob(үлгі_мән))
    원본들 += [қауіпсіз_қоршам / (Аты + '.c') for Аты in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Аргументтер = Баптаулар + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', жоба_түбір / '원격', '-I', Шығысы, '-I', қауіпсіз_қоршам,
                    '-I', құпиясөз_мән / 'inc', '-I', құпиясөз_мән / 'src', '-isystem', '/usr/include/newlib']
    def байланыстыру_қатысушы(Аты, жол_Тізім_4d1a5003, 접두):
        목적들 = []
        for Жол_2 in жол_Тізім_4d1a5003:
            тағайындау_мән = Шығысы / (접두 + Жол_2.stem + '.o')
            орындау_пәрмен([번역기] + Аргументтер + ['-c', Жол_2, '-o', тағайындау_мән])
            목적들.append(тағайындау_мән)
        with tempfile.TemporaryDirectory(dir=str(Шығысы)) as 임시:
            Топ_мән = Path(임시) / Аты
            орындау_пәрмен([Мұрағат_құрал, 'rcs', Топ_мән] + 목적들)
            Топ_мән.replace(Шығысы / Аты)
        return Шығысы / Аты
    байланыстыру_қатысушы('libassh.a', 원본들, 'assh-')
    (Шығысы / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(Жол_2.relative_to(жоба_түбір)) for Жол_2 in 원본들],
        'flags': list(map(str, Баптаулар)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [құпиясөз_мән / 'src' / (Аты + '.c') for Аты in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    байланыстыру_қатысушы('libbearssl.a', 베어원문, 'bear-')
    return байланыстыру_қатысушы('libremote.a', sorted((жоба_түбір / '원격').glob('*.c')), '')
