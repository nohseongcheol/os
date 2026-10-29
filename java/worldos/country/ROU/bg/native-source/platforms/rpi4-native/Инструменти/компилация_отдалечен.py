"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 정적 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from отдалечен_Настройки import Подготвяне


def Създаване_отдалечен(проект_корен, компилатор_инструмент, Архив_инструмент, Настройки, изпълнявам_команда):
    Изход = проект_корен / 'build/remote'
    Изход.mkdir(exist_ok=True)
    Подготвяне(проект_корен)
    защитен_обвивка = проект_корен / 'vendor/libassh/src'
    парола_стойност = проект_корен / 'vendor/bearssl'
    ядро = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [защитен_обвивка / ('assh_' + Име + '.c') for Име in ядро]
    for шарка_стойност in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(защитен_обвивка.glob(шарка_стойност))
    원본들 += [защитен_обвивка / (Име + '.c') for Име in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Параметри = Настройки + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', проект_корен / 'отдалечен_стойност', '-I', Изход, '-I', защитен_обвивка,
                    '-I', парола_стойност / 'inc', '-I', парола_стойност / 'src', '-isystem', '/usr/include/newlib']
    def обвързвам_участник(Име, път_Списък, 접두):
        목적들 = []
        for ПЪТ in път_Списък:
            местоназначение_стойност = Изход / (접두 + ПЪТ.stem + '.o')
            изпълнявам_команда([компилатор_инструмент] + Параметри + ['-c', ПЪТ, '-o', местоназначение_стойност])
            목적들.append(местоназначение_стойност)
        with tempfile.TemporaryDirectory(dir=str(Изход)) as 임시:
            Група_стойност = Path(임시) / Име
            изпълнявам_команда([Архив_инструмент, 'rcs', Група_стойност] + 목적들)
            Група_стойност.replace(Изход / Име)
        return Изход / Име
    обвързвам_участник('libassh.a', 원본들, 'assh-')
    (Изход / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(ПЪТ.relative_to(проект_корен)) for ПЪТ in 원본들],
        'flags': list(map(str, Настройки)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    компютър_без_операционна_система_източник = [парола_стойност / 'src' / (Име + '.c') for Име in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    обвързвам_участник('libbearssl.a', компютър_без_операционна_система_източник, 'bear-')
    return обвързвам_участник('libremote.a', sorted((проект_корен / 'отдалечен_стойност').glob('*.c')), '')
