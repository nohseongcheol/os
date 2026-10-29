"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 statik_değer 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from uzak_Ayarlar import Hazırlan


def açmak_uzak(işlem_kök, derleyici_araç, Arşiv_araç, Ayarlar, yürütmek_komut):
    metinÇıktısı = işlem_kök / 'build/remote'
    metinÇıktısı.mkdir(exist_ok=True)
    Hazırlan(işlem_kök)
    SSH = işlem_kök / 'vendor/libassh/src'
    parola_değer = işlem_kök / 'vendor/bearssl'
    Çekirdek = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [SSH / ('assh_' + İsim + '.c') for İsim in Çekirdek]
    for desen_değer in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(SSH.glob(desen_değer))
    원본들 += [SSH / (İsim + '.c') for İsim in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    bağımsız_değişkenler = Ayarlar + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', işlem_kök / 'uzak_değer', '-I', metinÇıktısı, '-I', SSH,
                    '-I', parola_değer / 'inc', '-I', parola_değer / 'src', '-isystem', '/usr/include/newlib']
    def BIND_uç_nokta(İsim, yol_Liste, 접두):
        목적들 = []
        for yol in yol_Liste:
            hedef_değer = metinÇıktısı / (접두 + yol.stem + '.o')
            yürütmek_komut([derleyici_araç] + bağımsız_değişkenler + ['-c', yol, '-o', hedef_değer])
            목적들.append(hedef_değer)
        with tempfile.TemporaryDirectory(dir=str(metinÇıktısı)) as 임시:
            Grup_değer = Path(임시) / İsim
            yürütmek_komut([Arşiv_araç, 'rcs', Grup_değer] + 목적들)
            Grup_değer.replace(metinÇıktısı / İsim)
        return metinÇıktısı / İsim
    BIND_uç_nokta('libassh.a', 원본들, 'assh-')
    (metinÇıktısı / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(yol.relative_to(işlem_kök)) for yol in 원본들],
        'flags': list(map(str, Ayarlar)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    çıplak_bilgisayar_kaynak = [parola_değer / 'src' / (İsim + '.c') for İsim in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_uç_nokta('libbearssl.a', çıplak_bilgisayar_kaynak, 'bear-')
    return BIND_uç_nokta('libremote.a', sorted((işlem_kök / 'uzak_değer').glob('*.c')), '')
