"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 ස්ථිතික_අගය 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from දුරස්ථ_පසුතල import පිළියෙල_කරන්න


def සාදන්න_දුරස්ථ(기준, 번역기, සංරක්ෂිතය_මෙවලම, සැකසුම්, ක්_රියාත්මක_කරන්න_විධානය):
    출력 = 기준 / 'build/remote'
    출력.mkdir(exist_ok=True)
    පිළියෙල_කරන්න(기준)
    සුරක්ෂිත_කවචය = 기준 / 'vendor/libassh/src'
    මුර_පදය_අගය = 기준 / 'vendor/bearssl'
    කර්නලය = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [සුරක්ෂිත_කවචය / ('assh_' + නම + '.c') for නම in කර්නලය]
    for රටාව_අගය in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(සුරක්ෂිත_කවචය.glob(රටාව_අගය))
    원본들 += [සුරක්ෂිත_කවචය / (නම + '.c') for නම in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    විස්තාරක = සැකසුම් + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 기준 / 'දුරස්ථ_අගය', '-I', 출력, '-I', සුරක්ෂිත_කවචය,
                    '-I', මුර_පදය_අගය / 'inc', '-I', මුර_පදය_අගය / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(නම, පෙත_ලැයිස්තුව, 접두):
        목적들 = []
        for මාර්_ගය in පෙත_ලැයිස්තුව:
            ගමනාන්තය_අගය = 출력 / (접두 + මාර්_ගය.stem + '.o')
            ක්_රියාත්මක_කරන්න_විධානය([번역기] + විස්තාරක + ['-c', මාර්_ගය, '-o', ගමනාන්තය_අගය])
            목적들.append(ගමනාන්තය_අගය)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            සමූහය_අගය = Path(임시) / නම
            ක්_රියාත්මක_කරන්න_විධානය([සංරක්ෂිතය_මෙවලම, 'rcs', සමූහය_අගය] + 목적들)
            සමූහය_අගය.replace(출력 / නම)
        return 출력 / නම
    묶기('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(මාර්_ගය.relative_to(기준)) for මාර්_ගය in 원본들],
        'flags': list(map(str, සැකසුම්)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [මුර_පදය_අගය / 'src' / (නම + '.c') for නම in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((기준 / 'දුරස්ථ_අගය').glob('*.c')), '')
