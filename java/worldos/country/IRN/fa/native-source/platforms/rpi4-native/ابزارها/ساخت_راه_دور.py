"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 ایستا_مقدار 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from راه_دور_تنظیمات import آماده_کردن


def ایجاد_راه_دور(نمایش_دادن_جذر, 번역기, آرشیو_ابزار, تنظیمات, اجرا_فرمان):
    خروجی = نمایش_دادن_جذر / 'build/remote'
    خروجی.mkdir(exist_ok=True)
    آماده_کردن(نمایش_دادن_جذر)
    ایمن_واسط = نمایش_دادن_جذر / 'vendor/libassh/src'
    رمز_عبور_مقدار = نمایش_دادن_جذر / 'vendor/bearssl'
    هسته = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [ایمن_واسط / ('assh_' + نام + '.c') for نام in هسته]
    for الگو_مقدار in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(ایمن_واسط.glob(الگو_مقدار))
    원본들 += [ایمن_واسط / (نام + '.c') for نام in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    نشانوندها = تنظیمات + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', نمایش_دادن_جذر / 'راه_دور_مقدار', '-I', خروجی, '-I', ایمن_واسط,
                    '-I', رمز_عبور_مقدار / 'inc', '-I', رمز_عبور_مقدار / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(نام, مسیر_لیست, 접두):
        목적들 = []
        for مسیر in مسیر_لیست:
            مقصد_مقدار = خروجی / (접두 + مسیر.stem + '.o')
            اجرا_فرمان([번역기] + نشانوندها + ['-c', مسیر, '-o', مقصد_مقدار])
            목적들.append(مقصد_مقدار)
        with tempfile.TemporaryDirectory(dir=str(خروجی)) as 임시:
            گروه_مقدار = Path(임시) / نام
            اجرا_فرمان([آرشیو_ابزار, 'rcs', گروه_مقدار] + 목적들)
            گروه_مقدار.replace(خروجی / نام)
        return خروجی / نام
    묶기('libassh.a', 원본들, 'assh-')
    (خروجی / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(مسیر.relative_to(نمایش_دادن_جذر)) for مسیر in 원본들],
        'flags': list(map(str, تنظیمات)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [رمز_عبور_مقدار / 'src' / (نام + '.c') for نام in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((نمایش_دادن_جذر / 'راه_دور_مقدار').glob('*.c')), '')
