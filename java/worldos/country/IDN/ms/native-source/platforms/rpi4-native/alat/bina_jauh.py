"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 statik_VALUE 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from jauh_Seting import Sediakan


def cipta_jauh(projek_akar, 번역기, Arkib_alat, Tetapan, laksanakan_perintah):
    출력 = projek_akar / 'build/remote'
    출력.mkdir(exist_ok=True)
    Sediakan(projek_akar)
    selamat_cangkerang = projek_akar / 'vendor/libassh/src'
    kata_laluan_VALUE = projek_akar / 'vendor/bearssl'
    kernel = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [selamat_cangkerang / ('assh_' + Nama + '.c') for Nama in kernel]
    for corak_VALUE in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(selamat_cangkerang.glob(corak_VALUE))
    원본들 += [selamat_cangkerang / (Nama + '.c') for Nama in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = Tetapan + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', projek_akar / 'jauh_VALUE', '-I', 출력, '-I', selamat_cangkerang,
                    '-I', kata_laluan_VALUE / 'inc', '-I', kata_laluan_VALUE / 'src', '-isystem', '/usr/include/newlib']
    def ikat_peserta(Nama, laluan_Senarai, 접두):
        목적들 = []
        for LALUAN in laluan_Senarai:
            destinasi_VALUE = 출력 / (접두 + LALUAN.stem + '.o')
            laksanakan_perintah([번역기] + 인수 + ['-c', LALUAN, '-o', destinasi_VALUE])
            목적들.append(destinasi_VALUE)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            Kumpulan_VALUE = Path(임시) / Nama
            laksanakan_perintah([Arkib_alat, 'rcs', Kumpulan_VALUE] + 목적들)
            Kumpulan_VALUE.replace(출력 / Nama)
        return 출력 / Nama
    ikat_peserta('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(LALUAN.relative_to(projek_akar)) for LALUAN in 원본들],
        'flags': list(map(str, Tetapan)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [kata_laluan_VALUE / 'src' / (Nama + '.c') for Nama in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    ikat_peserta('libbearssl.a', 베어원문, 'bear-')
    return ikat_peserta('libremote.a', sorted((projek_akar / 'jauh_VALUE').glob('*.c')), '')
