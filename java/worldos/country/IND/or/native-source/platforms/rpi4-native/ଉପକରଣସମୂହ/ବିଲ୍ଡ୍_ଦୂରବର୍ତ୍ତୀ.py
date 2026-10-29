"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 ସ୍ଥିର_ମୂଲ୍ୟ 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from ଦୂରବର୍ତ୍ତୀ_ସେଟିଂସ୍ import ପ୍ରସ୍ତୁତ


def ସୃଷ୍ଟି_ଦୂରବର୍ତ୍ତୀ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, 번역기, ଅଭିଲେଖାଗାର_ଉପକରଣ, ବିନ୍ଯାସ, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ):
    ନିର୍ଗମ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/remote'
    ନିର୍ଗମ.mkdir(exist_ok=True)
    ପ୍ରସ୍ତୁତ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍)
    ସୁରକ୍ଷିତ_ଖୋଳ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/libassh/src'
    ପାସ୍_ୱାର୍ଡ୍_ମୂଲ୍ୟ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/bearssl'
    କେନ୍ଦ୍ରିକ = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [ସୁରକ୍ଷିତ_ଖୋଳ / ('assh_' + ନାମ + '.c') for ନାମ in କେନ୍ଦ୍ରିକ]
    for ପାଟର୍ନ_ମୂଲ୍ୟ in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(ସୁରକ୍ଷିତ_ଖୋଳ.glob(ପାଟର୍ନ_ମୂଲ୍ୟ))
    원본들 += [ସୁରକ୍ଷିତ_ଖୋଳ / (ନାମ + '.c') for ନାମ in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    인수 = ବିନ୍ଯାସ + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ', '-I', ନିର୍ଗମ, '-I', ସୁରକ୍ଷିତ_ଖୋଳ,
                    '-I', ପାସ୍_ୱାର୍ଡ୍_ମୂଲ୍ୟ / 'inc', '-I', ପାସ୍_ୱାର୍ଡ୍_ମୂଲ୍ୟ / 'src', '-isystem', '/usr/include/newlib']
    def 묶기(ନାମ, ପଥ_ତାଲିକା, 접두):
        목적들 = []
        for ପଥ in ପଥ_ତାଲିକା:
            ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = ନିର୍ଗମ / (접두 + ପଥ.stem + '.o')
            ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([번역기] + 인수 + ['-c', ପଥ, '-o', ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ])
            목적들.append(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ)
        with tempfile.TemporaryDirectory(dir=str(ନିର୍ଗମ)) as 임시:
            ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ = Path(임시) / ନାମ
            ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([ଅଭିଲେଖାଗାର_ଉପକରଣ, 'rcs', ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ] + 목적들)
            ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ.replace(ନିର୍ଗମ / ନାମ)
        return ନିର୍ଗମ / ନାମ
    묶기('libassh.a', 원본들, 'assh-')
    (ନିର୍ଗମ / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(ପଥ.relative_to(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍)) for ପଥ in 원본들],
        'flags': list(map(str, ବିନ୍ଯାସ)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    베어원문 = [ପାସ୍_ୱାର୍ଡ୍_ମୂଲ୍ୟ / 'src' / (ନାମ + '.c') for ନାମ in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    묶기('libbearssl.a', 베어원문, 'bear-')
    return 묶기('libremote.a', sorted((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ').glob('*.c')), '')
