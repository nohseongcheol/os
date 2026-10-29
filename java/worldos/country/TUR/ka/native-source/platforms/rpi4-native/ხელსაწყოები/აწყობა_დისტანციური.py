"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 სტატიკური_მნიშვნელობა 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from დისტანციური_პარამეტრები import მომზადება


def შექმნა_დისტანციური(პროეცირება_ფესვი, 번역기, არქივი_ხელსაწყო, პარამეტრები, შესრულება_ბრძანება):
    출력 = პროეცირება_ფესვი / 'build/remote'
    출력.mkdir(exist_ok=True)
    მომზადება(პროეცირება_ფესვი)
    უსაფრთხო_გარემო = პროეცირება_ფესვი / 'vendor/libassh/src'
    პაროლი_მნიშვნელობა = პროეცირება_ფესვი / 'vendor/bearssl'
    ბირთვი = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [უსაფრთხო_გარემო / ('assh_' + სახელი + '.c') for სახელი in ბირთვი]
    for ნიმუში_მნიშვნელობა in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(უსაფრთხო_გარემო.glob(ნიმუში_მნიშვნელობა))
    원본들 += [უსაფრთხო_გარემო / (სახელი + '.c') for სახელი in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = პარამეტრები + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', პროეცირება_ფესვი / 'დისტანციური_მნიშვნელობა', '-I', 출력, '-I', უსაფრთხო_გარემო,
                    '-I', პაროლი_მნიშვნელობა / 'inc', '-I', პაროლი_მნიშვნელობა / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(სახელი, მდებარეობა_სია, 접두):
        목적들 = []
        for გეზი in მდებარეობა_სია:
            მიმართულება_მნიშვნელობა = 출력 / (접두 + გეზი.stem + '.o')
            შესრულება_ბრძანება([번역기] + 인수 + ['-c', გეზი, '-o', მიმართულება_მნიშვნელობა])
            목적들.append(მიმართულება_მნიშვნელობა)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            ჯგუფი_მნიშვნელობა = Path(임시) / სახელი
            შესრულება_ბრძანება([არქივი_ხელსაწყო, 'rcs', ჯგუფი_მნიშვნელობა] + 목적들)
            ჯგუფი_მნიშვნელობა.replace(출력 / სახელი)
        return 출력 / სახელი
    묶기('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(გეზი.relative_to(პროეცირება_ფესვი)) for გეზი in 원본들],
        'flags': list(map(str, პარამეტრები)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [პაროლი_მნიშვნელობა / 'src' / (სახელი + '.c') for სახელი in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((პროეცირება_ფესვი / 'დისტანციური_მნიშვნელობა').glob('*.c')), '')
