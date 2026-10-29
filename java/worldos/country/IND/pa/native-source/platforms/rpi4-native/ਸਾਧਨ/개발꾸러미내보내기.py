#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ


def ਚਲਾਓ_2():
    배포경로 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ = {
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1] / 'LICENSE': 'LICENSE',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਸਾਧਨ/개발꾸러미번역.py': 'compile.py',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਉਪਭੋਗਤਾ/호출.h': 'include/호출.h',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '명명/기계연결이름.h': '명명/기계연결이름.h',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਉਪਭੋਗਤਾ/ਲਿੰਕ_ਖਾਕਾ.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/user/start.o': 'lib/start.o',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/user/runtime.o': 'lib/runtime.o',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਉਪਭੋਗਤਾ/파일예제.cpp': 'examples/파일예제.cpp',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '예제/한글코딩/인사.c': 'examples/인사.c',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '예제/한글코딩/ਸਟ੍ਰੀਮ_ਕੀਮਤ.c': 'examples/ਸਟ੍ਰੀਮ_ਕੀਮਤ.c',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਉਪਭੋਗਤਾ/통신예제.cpp': 'examples/통신예제.cpp',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/user/demo.elf': 'examples/demo.elf',
            ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, ਟੀਚਾ in ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ.items():
            ਮੰਜਿਲ_ਸਮੱਗਰੀ_ਪਤਾ = 개발꾸러미 / ਟੀਚਾ
            ਮੰਜਿਲ_ਸਮੱਗਰੀ_ਪਤਾ.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ਮੰਜਿਲ_ਸਮੱਗਰੀ_ਪਤਾ))
            꾸러미명세['sha256'][ਟੀਚਾ] = hashlib.sha256(ਮੰਜਿਲ_ਸਮੱਗਰੀ_ਪਤਾ.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ਸੁਰੂ_ਉਪਭੋਗਤਾ_ਐਪਲੀਕੇਸ਼(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ਉਪਭੋਗਤਾ_ਦਲੀਲ() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ਸੰਗ੍ਰਹਿ = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ਸੰਗ੍ਰਹਿ), 'w:gz') as ਮਾਪ_ਸਮੱਗਰੀ:
            ਮਾਪ_ਸਮੱਗਰੀ.add(str(개발꾸러미), arcname=개발꾸러미.name)
        ਸੰਗ੍ਰਹਿ.replace(배포경로 / ਸੰਗ੍ਰਹਿ.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as ਮਾਪ_ਸਮੱਗਰੀ:
            for ਨਾਂ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ਮਾਪ_ਸਮੱਗਰੀ.add(str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1] / ਨਾਂ), arcname='jkoros-native/' + ਨਾਂ)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ਉਪਭੋਗਤਾ', '명명',
                             'ਸਾਧਨ/시언어번역기빌드.py', 'ਸਾਧਨ/ਬਿਲਡ_ਉਪਭੋਗਤਾ_ਥਾਂ.py', '파일전송과번역.md'):
                ਮਾਪ_ਸਮੱਗਰੀ.add(str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 상대경로), arcname='jkoros-native/' + 상대경로)
            for ਨਾਂ in ('crt.o', 'aot-runtime.o', 'ਸਾਧਾਰਨ_ਭਾਸ਼ਾ_ਰਨਟਾਈਮ_ਸਮਰਥਨ.o', 'ਚਲਾਓ_2.o', '미리번역.o', '되돌림.o'):
                ਮੰਜਿਲ_ਪਤਾ_ffac9b48 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/ccompiler' / ਨਾਂ
                ਮਾਪ_ਸਮੱਗਰੀ.add(str(ਮੰਜਿਲ_ਪਤਾ_ffac9b48), arcname='jkoros-native/relink/' + ਨਾਂ)
            for ਨਾਂ in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ਮਾਪ_ਸਮੱਗਰੀ.add(str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/user' / ਨਾਂ), arcname='jkoros-native/relink/user/' + ਨਾਂ)
            ਮਾਪ_ਸਮੱਗਰੀ.add(str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ਮਾਪ_ਸਮੱਗਰੀ.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ਚਲਾਓ_2()
