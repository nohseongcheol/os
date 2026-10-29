"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 statiki_baha 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from uzakdan_Sazlamalar import Taýýarla


def döretmek_uzakdan(기준, 번역기, Arhiw_gural, Düzümler, ýerine_ýetir_buýruk):
    출력 = 기준 / 'build/remote'
    출력.mkdir(exist_ok=True)
    Taýýarla(기준)
    goragly_gabyjak = 기준 / 'vendor/libassh/src'
    parol_baha = 기준 / 'vendor/bearssl'
    ýadro = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [goragly_gabyjak / ('assh_' + Ad + '.c') for Ad in ýadro]
    for nagyş_baha in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(goragly_gabyjak.glob(nagyş_baha))
    원본들 += [goragly_gabyjak / (Ad + '.c') for Ad in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Düzümler + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 기준 / 'uzakdan_baha', '-I', 출력, '-I', goragly_gabyjak,
                    '-I', parol_baha / 'inc', '-I', parol_baha / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(Ad, ýol_Sanaw, 접두):
        목적들 = []
        for Ýol in ýol_Sanaw:
            barylmaly_ýer_baha = 출력 / (접두 + Ýol.stem + '.o')
            ýerine_ýetir_buýruk([번역기] + 인수 + ['-c', Ýol, '-o', barylmaly_ýer_baha])
            목적들.append(barylmaly_ýer_baha)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            topar_baha = Path(임시) / Ad
            ýerine_ýetir_buýruk([Arhiw_gural, 'rcs', topar_baha] + 목적들)
            topar_baha.replace(출력 / Ad)
        return 출력 / Ad
    묶기('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(Ýol.relative_to(기준)) for Ýol in 원본들],
        'flags': list(map(str, Düzümler)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [parol_baha / 'src' / (Ad + '.c') for Ad in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((기준 / 'uzakdan_baha').glob('*.c')), '')
