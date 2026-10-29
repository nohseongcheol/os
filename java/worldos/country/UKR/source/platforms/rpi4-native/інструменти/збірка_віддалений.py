"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 정적 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from віддалений_Настройки import Готувати


def Створення_віддалений(Дії_корінь, компілятор_інструмент, Архів_інструмент, Налаштування, Виконати_команда):
    Вивід = Дії_корінь / 'build/remote'
    Вивід.mkdir(exist_ok=True)
    Готувати(Дії_корінь)
    захищений_оболонка = Дії_корінь / 'vendor/libassh/src'
    пароль_значення = Дії_корінь / 'vendor/bearssl'
    Ядро = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [захищений_оболонка / ('assh_' + Назва + '.c') for Назва in Ядро]
    for взірець_значення in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(захищений_оболонка.glob(взірець_значення))
    원본들 += [захищений_оболонка / (Назва + '.c') for Назва in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    аргументи = Налаштування + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', Дії_корінь / 'віддалений_значення', '-I', Вивід, '-I', захищений_оболонка,
                    '-I', пароль_значення / 'inc', '-I', пароль_значення / 'src', '-isystem', '/usr/include/newlib']
    def зв_язувати_учасник(Назва, шлях_список, 접두):
        목적들 = []
        for шлях in шлях_список:
            місце_значення = Вивід / (접두 + шлях.stem + '.o')
            Виконати_команда([компілятор_інструмент] + аргументи + ['-c', шлях, '-o', місце_значення])
            목적들.append(місце_значення)
        with tempfile.TemporaryDirectory(dir=str(Вивід)) as 임시:
            Група_значення = Path(임시) / Назва
            Виконати_команда([Архів_інструмент, 'rcs', Група_значення] + 목적들)
            Група_значення.replace(Вивід / Назва)
        return Вивід / Назва
    зв_язувати_учасник('libassh.a', 원본들, 'assh-')
    (Вивід / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(шлях.relative_to(Дії_корінь)) for шлях in 원본들],
        'flags': list(map(str, Налаштування)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    комп_ютер_без_операційної_системи_джерело = [пароль_значення / 'src' / (Назва + '.c') for Назва in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    зв_язувати_учасник('libbearssl.a', комп_ютер_без_операційної_системи_джерело, 'bear-')
    return зв_язувати_учасник('libremote.a', sorted((Дії_корінь / 'віддалений_значення').glob('*.c')), '')
