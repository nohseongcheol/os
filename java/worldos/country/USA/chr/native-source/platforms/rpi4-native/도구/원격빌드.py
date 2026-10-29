"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 ᎾᏓᏅᏍᎬᎾ_ᏧᎬᏩᎶᏗᏯ 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from 원격설정 import ᎭᏛᏅᎢᏍᏓ


def 원격만들기(기준, 번역기, ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, ᏕᎦᎧᎲᎢ, ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ):
    출력 = 기준 / 'build/remote'
    출력.mkdir(exist_ok=True)
    ᎭᏛᏅᎢᏍᏓ(기준)
    보안셸 = 기준 / 'vendor/libassh/src'
    ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ = 기준 / 'vendor/bearssl'
    kernel = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [보안셸 / ('assh_' + ᏚᏙᎥᎢ + '.c') for ᏚᏙᎥᎢ in kernel]
    for ᎤᎾᎶᎢᏓ_ᏧᎬᏩᎶᏗᏯ in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(보안셸.glob(ᎤᎾᎶᎢᏓ_ᏧᎬᏩᎶᏗᏯ))
    원본들 += [보안셸 / (ᏚᏙᎥᎢ + '.c') for ᏚᏙᎥᎢ in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = ᏕᎦᎧᎲᎢ + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', 기준 / '원격', '-I', 출력, '-I', 보안셸,
                    '-I', ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ / 'inc', '-I', ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(ᏚᏙᎥᎢ, ᎠᏍᏓᏩᏛᏍᏗ_ᏕᎦᏅᏅᏛ, 접두):
        목적들 = []
        for ᎠᏍᏓᏩᏛᏍᏗ in ᎠᏍᏓᏩᏛᏍᏗ_ᏕᎦᏅᏅᏛ:
            ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ = 출력 / (접두 + ᎠᏍᏓᏩᏛᏍᏗ.stem + '.o')
            ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([번역기] + 인수 + ['-c', ᎠᏍᏓᏩᏛᏍᏗ, '-o', ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ])
            목적들.append(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ)
        with tempfile.TemporaryDirectory(dir=str(출력)) as 임시:
            ᎤᎾᏓᏡᎬᎢ_ᏧᎬᏩᎶᏗᏯ = Path(임시) / ᏚᏙᎥᎢ
            ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, 'rcs', ᎤᎾᏓᏡᎬᎢ_ᏧᎬᏩᎶᏗᏯ] + 목적들)
            ᎤᎾᏓᏡᎬᎢ_ᏧᎬᏩᎶᏗᏯ.replace(출력 / ᏚᏙᎥᎢ)
        return 출력 / ᏚᏙᎥᎢ
    묶기('libassh.a', 원본들, 'assh-')
    (출력 / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(ᎠᏍᏓᏩᏛᏍᏗ.relative_to(기준)) for ᎠᏍᏓᏩᏛᏍᏗ in 원본들],
        'flags': list(map(str, ᏕᎦᎧᎲᎢ)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ / 'src' / (ᏚᏙᎥᎢ + '.c') for ᏚᏙᎥᎢ in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((기준 / '원격').glob('*.c')), '')
