"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 ìdágún_iye 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from Ìjìnnà_Àwọn_ààtò import gbaradì


def Ṣẹ̀dá_Ìjìnnà(기준, 번역기, Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́, Àwọn_ààtò, ṣiṣẹ́_àṣẹ):
    출력 = 기준 / 'build/remote'
    출력.mkdir(exist_ok=True)
    gbaradì(기준)
    Tóláàbò_ṣẹ́ẹ̀lì = 기준 / 'vendor/libassh/src'
    ọ̀rọ̀_aṣínà_iye = 기준 / 'vendor/bearssl'
    kánẹ́ẹ̀lì = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [Tóláàbò_ṣẹ́ẹ̀lì / ('assh_' + Orúkọ + '.c') for Orúkọ in kánẹ́ẹ̀lì]
    for bátànì_iye in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(Tóláàbò_ṣẹ́ẹ̀lì.glob(bátànì_iye))
    원본들 += [Tóláàbò_ṣẹ́ẹ̀lì / (Orúkọ + '.c') for Orúkọ in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Àwọn_ààtò + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 기준 / 'Ìjìnnà_iye', '-I', 출력, '-I', Tóláàbò_ṣẹ́ẹ̀lì,
                    '-I', ọ̀rọ̀_aṣínà_iye / 'inc', '-I', ọ̀rọ̀_aṣínà_iye / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(Orúkọ, ọ̀nà_Àtòkọ, 접두):
        목적들 = []
        for ọ̀nà in ọ̀nà_Àtòkọ:
            èbúté_iye = 출력 / (접두 + ọ̀nà.stem + '.o')
            ṣiṣẹ́_àṣẹ([번역기] + 인수 + ['-c', ọ̀nà, '-o', èbúté_iye])
            목적들.append(èbúté_iye)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            Àjọṣe_iye = Path(임시) / Orúkọ
            ṣiṣẹ́_àṣẹ([Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́, 'rcs', Àjọṣe_iye] + 목적들)
            Àjọṣe_iye.replace(출력 / Orúkọ)
        return 출력 / Orúkọ
    묶기('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(ọ̀nà.relative_to(기준)) for ọ̀nà in 원본들],
        'flags': list(map(str, Àwọn_ààtò)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [ọ̀rọ̀_aṣínà_iye / 'src' / (Orúkọ + '.c') for Orúkọ in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((기준 / 'Ìjìnnà_iye').glob('*.c')), '')
