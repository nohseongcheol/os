"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 статычны_значэнне 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from аддалены_Налады import Падрыхтаваць


def стварыць_аддалены(기준, 번역기, Архіў_інструмент, Усталёўкі, выканаць_каманда):
    Выхад = 기준 / 'build/remote'
    Выхад.mkdir(exist_ok=True)
    Падрыхтаваць(기준)
    бяспечны_абалонка = 기준 / 'vendor/libassh/src'
    пароль_значэнне = 기준 / 'vendor/bearssl'
    ядро = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [бяспечны_абалонка / ('assh_' + Назва + '.c') for Назва in ядро]
    for узор_значэнне in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(бяспечны_абалонка.glob(узор_значэнне))
    원본들 += [бяспечны_абалонка / (Назва + '.c') for Назва in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Усталёўкі + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 기준 / 'аддалены_значэнне', '-I', Выхад, '-I', бяспечны_абалонка,
                    '-I', пароль_значэнне / 'inc', '-I', пароль_значэнне / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(Назва, шлях_Спіс, 접두):
        목적들 = []
        for ШЛЯХ in шлях_Спіс:
            прызначэнне_значэнне_a0fbc067 = Выхад / (접두 + ШЛЯХ.stem + '.o')
            выканаць_каманда([번역기] + 인수 + ['-c', ШЛЯХ, '-o', прызначэнне_значэнне_a0fbc067])
            목적들.append(прызначэнне_значэнне_a0fbc067)
        with tempfile.TemporaryDirectory(dir=str(Выхад)) as 임시:
            Група_значэнне = Path(임시) / Назва
            выканаць_каманда([Архіў_інструмент, 'rcs', Група_значэнне] + 목적들)
            Група_значэнне.replace(Выхад / Назва)
        return Выхад / Назва
    묶기('libassh.a', 원본들, 'assh-')
    (Выхад / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(ШЛЯХ.relative_to(기준)) for ШЛЯХ in 원본들],
        'flags': list(map(str, Усталёўкі)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [пароль_значэнне / 'src' / (Назва + '.c') for Назва in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((기준 / 'аддалены_значэнне').glob('*.c')), '')
