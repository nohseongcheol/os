"""LGPL libassh와 MIT BearSSL을 각각 보존하여 재연결 가능한 정적 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from दूरस्थ_सेटिंग import 준비


def बनाएँ_दूरस्थ(प्रोजेक्ट_करें_मूल, कंपाइलर_उपकरण, संग्रह_उपकरण, विन्यास, निष्पादित_करें_आदेश):
    निर्गम = प्रोजेक्ट_करें_मूल / 'build/remote'
    निर्गम.mkdir(exist_ok=True)
    준비(प्रोजेक्ट_करें_मूल)
    सुरक्षित_शेल = प्रोजेक्ट_करें_मूल / 'vendor/libassh/src'
    पासवर्ड_मान = प्रोजेक्ट_करें_मूल / 'vendor/bearssl'
    कर्नेल = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    원본들 = [सुरक्षित_शेल / ('assh_' + नाम + '.c') for नाम in कर्नेल]
    for पैटर्न_मान in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        원본들 += sorted(सुरक्षित_शेल.glob(पैटर्न_मान))
    원본들 += [सुरक्षित_शेल / (नाम + '.c') for नाम in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    तर्क = विन्यास + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', प्रोजेक्ट_करें_मूल / 'दूरस्थ_मान', '-I', निर्गम, '-I', सुरक्षित_शेल,
                    '-I', पासवर्ड_मान / 'inc', '-I', पासवर्ड_मान / 'src', '-isystem', '/usr/include/newlib']
    def बाइंड_करें_एंडपॉइंट(नाम, पथ_सूची, 접두):
        목적들 = []
        for पथ in पथ_सूची:
            गंतव्य_मान = निर्गम / (접두 + पथ.stem + '.o')
            निष्पादित_करें_आदेश([कंपाइलर_उपकरण] + तर्क + ['-c', पथ, '-o', गंतव्य_मान])
            목적들.append(गंतव्य_मान)
        with tempfile.TemporaryDirectory(dir=str(निर्गम)) as 임시:
            समूह_मान = Path(임시) / नाम
            निष्पादित_करें_आदेश([संग्रह_उपकरण, 'rcs', समूह_मान] + 목적들)
            समूह_मान.replace(निर्गम / नाम)
        return निर्गम / नाम
    बाइंड_करें_एंडपॉइंट('libassh.a', 원본들, 'assh-')
    (निर्गम / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(पथ.relative_to(प्रोजेक्ट_करें_मूल)) for पथ in 원본들],
        'flags': list(map(str, विन्यास)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    ऑपरेटिंग_सिस्टम_रहित_कंप्यूटर_स्रोत = [पासवर्ड_मान / 'src' / (नाम + '.c') for नाम in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    बाइंड_करें_एंडपॉइंट('libbearssl.a', ऑपरेटिंग_सिस्टम_रहित_कंप्यूटर_स्रोत, 'bear-')
    return बाइंड_करें_एंडपॉइंट('libremote.a', sorted((प्रोजेक्ट_करें_मूल / 'दूरस्थ_मान').glob('*.c')), '')
