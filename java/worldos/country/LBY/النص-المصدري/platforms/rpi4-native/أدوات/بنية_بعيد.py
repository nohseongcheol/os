"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 ثابت_قيمة_f430d3f5 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from بعيد_إعدادات import إعداد


def فتح_بعيد(يعرض_جذر, محول_برمجي_أداة, أرشيف_أداة, إعدادات, ينفذ_أمر):
    مخرجات = يعرض_جذر / 'build/remote'
    مخرجات.mkdir(exist_ok=True)
    إعداد(يعرض_جذر)
    보안셸 = يعرض_جذر / 'vendor/libassh/src'
    رمز_الوصول_قيمة = يعرض_جذر / 'vendor/bearssl'
    نواة = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [보안셸 / ('assh_' + اسم + '.c') for اسم in نواة]
    for نقش_قيمة in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(보안셸.glob(نقش_قيمة))
    원본들 += [보안셸 / (اسم + '.c') for اسم in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    وسائط = إعدادات + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', يعرض_جذر / 'بعيد_قيمة', '-I', مخرجات, '-I', 보안셸,
                    '-I', رمز_الوصول_قيمة / 'inc', '-I', رمز_الوصول_قيمة / 'src', '-isystem', '/usr/include/newlib']
    def يربط_المشارك(اسم, مسار_قائمة, 접두):
        목적들 = []
        for مسار in مسار_قائمة:
            وجهة_قيمة = مخرجات / (접두 + مسار.stem + '.o')
            ينفذ_أمر([محول_برمجي_أداة] + وسائط + ['-c', مسار, '-o', وجهة_قيمة])
            목적들.append(وجهة_قيمة)
        with tempfile.TemporaryDirectory(dir=str(مخرجات)) as 임시:
            يجمع_قيمة = Path(임시) / اسم
            ينفذ_أمر([أرشيف_أداة, 'rcs', يجمع_قيمة] + 목적들)
            يجمع_قيمة.replace(مخرجات / اسم)
        return مخرجات / اسم
    يربط_المشارك('libassh.a', 원본들, 'assh-')
    (مخرجات / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(مسار.relative_to(يعرض_جذر)) for مسار in 원본들],
        'flags': list(map(str, إعدادات)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    كمبيوتر_بلا_نظام_تشغيل_مصدر = [رمز_الوصول_قيمة / 'src' / (اسم + '.c') for اسم in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    يربط_المشارك('libbearssl.a', كمبيوتر_بلا_نظام_تشغيل_مصدر, 'bear-')
    return يربط_المشارك('libremote.a', sorted((يعرض_جذر / 'بعيد_قيمة').glob('*.c')), '')
