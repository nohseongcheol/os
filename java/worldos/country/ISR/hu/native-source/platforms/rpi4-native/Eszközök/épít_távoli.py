"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 statikus_ÉRTÉK 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from távoli_Gépház import Előkészítés


def készít_távoli(teendő_gyök, fordítóprogram_eszköz, archív_eszköz, Beállítások, végrehajt_parancs):
    Kimenet = teendő_gyök / 'build/remote'
    Kimenet.mkdir(exist_ok=True)
    Előkészítés(teendő_gyök)
    biztonságos_felület = teendő_gyök / 'vendor/libassh/src'
    jelszó_ÉRTÉK = teendő_gyök / 'vendor/bearssl'
    kernel = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [biztonságos_felület / ('assh_' + Név + '.c') for Név in kernel]
    for minta_ÉRTÉK in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(biztonságos_felület.glob(minta_ÉRTÉK))
    원본들 += [biztonságos_felület / (Név + '.c') for Név in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    Argumentumok = Beállítások + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', teendő_gyök / 'távoli_ÉRTÉK', '-I', Kimenet, '-I', biztonságos_felület,
                    '-I', jelszó_ÉRTÉK / 'inc', '-I', jelszó_ÉRTÉK / 'src', '-isystem', '/usr/include/newlib']
    def BIND_végpont(Név, útvonal_Lista, 접두):
        목적들 = []
        for ÚTVONAL in útvonal_Lista:
            cél_ÉRTÉK = Kimenet / (접두 + ÚTVONAL.stem + '.o')
            végrehajt_parancs([fordítóprogram_eszköz] + Argumentumok + ['-c', ÚTVONAL, '-o', cél_ÉRTÉK])
            목적들.append(cél_ÉRTÉK)
        with tempfile.TemporaryDirectory(dir=str(Kimenet)) as 임시:
            Csoport_ÉRTÉK = Path(임시) / Név
            végrehajt_parancs([archív_eszköz, 'rcs', Csoport_ÉRTÉK] + 목적들)
            Csoport_ÉRTÉK.replace(Kimenet / Név)
        return Kimenet / Név
    BIND_végpont('libassh.a', 원본들, 'assh-')
    (Kimenet / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(ÚTVONAL.relative_to(teendő_gyök)) for ÚTVONAL in 원본들],
        'flags': list(map(str, Beállítások)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    operációs_rendszer_nélküli_számítógép_forrás = [jelszó_ÉRTÉK / 'src' / (Név + '.c') for Név in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    BIND_végpont('libbearssl.a', operációs_rendszer_nélküli_számítógép_forrás, 'bear-')
    return BIND_végpont('libremote.a', sorted((teendő_gyök / 'távoli_ÉRTÉK').glob('*.c')), '')
