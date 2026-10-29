"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 статикалык_маани 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from алыскы_Орнотуулар import Даярдоо


def түзүү_алыскы(기준, 번역기, Архив_курал, Орнотуулар, аткаруу_буйрук):
    Чыгыш = 기준 / 'build/remote'
    Чыгыш.mkdir(exist_ok=True)
    Даярдоо(기준)
    коопсуз_сырты = 기준 / 'vendor/libassh/src'
    жашыруун_сөз_маани = 기준 / 'vendor/bearssl'
    өзөк = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [коопсуз_сырты / ('assh_' + Аты + '.c') for Аты in өзөк]
    for үлгү_маани in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(коопсуз_сырты.glob(үлгү_маани))
    원본들 += [коопсуз_сырты / (Аты + '.c') for Аты in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Орнотуулар + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 기준 / 'алыскы_маани', '-I', Чыгыш, '-I', коопсуз_сырты,
                    '-I', жашыруун_сөз_маани / 'inc', '-I', жашыруун_сөз_маани / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(Аты, жол_Тизме, 접두):
        목적들 = []
        for ЖОЛ in жол_Тизме:
            көздөө_жайы_маани = Чыгыш / (접두 + ЖОЛ.stem + '.o')
            аткаруу_буйрук([번역기] + 인수 + ['-c', ЖОЛ, '-o', көздөө_жайы_маани])
            목적들.append(көздөө_жайы_маани)
        with tempfile.TemporaryDirectory(dir=str(Чыгыш)) as 임시:
            топ_маани = Path(임시) / Аты
            аткаруу_буйрук([Архив_курал, 'rcs', топ_маани] + 목적들)
            топ_маани.replace(Чыгыш / Аты)
        return Чыгыш / Аты
    묶기('libassh.a', 원본들, 'assh-')
    (Чыгыш / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(ЖОЛ.relative_to(기준)) for ЖОЛ in 원본들],
        'flags': list(map(str, Орнотуулар)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [жашыруун_сөз_маани / 'src' / (Аты + '.c') for Аты in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((기준 / 'алыскы_маани').glob('*.c')), '')
