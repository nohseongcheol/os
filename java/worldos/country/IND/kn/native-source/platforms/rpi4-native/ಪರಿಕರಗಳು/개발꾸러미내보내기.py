#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ


def ಚಲಾಯಿಸು_2():
    배포경로 = ಬಿಂಬಿಸು_ಮೂಲ / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = ಬಿಂಬಿಸು_ಮೂಲ.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(ಬಿಂಬಿಸು_ಮೂಲ / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ಫೈಲ್_ಪಟ್ಟಿ = {
            ಬಿಂಬಿಸು_ಮೂಲ.parents[1] / 'LICENSE': 'LICENSE',
            ಬಿಂಬಿಸು_ಮೂಲ.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            ಬಿಂಬಿಸು_ಮೂಲ / 'ಪರಿಕರಗಳು/개발꾸러미번역.py': 'compile.py',
            ಬಿಂಬಿಸು_ಮೂಲ / 'ಬಳಕೆದಾರ/호출.h': 'include/호출.h',
            ಬಿಂಬಿಸು_ಮೂಲ / '명명/기계연결이름.h': '명명/기계연결이름.h',
            ಬಿಂಬಿಸು_ಮೂಲ / 'ಬಳಕೆದಾರ/ಜೋಡಣೆ_ಲೇಔಟ್.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            ಬಿಂಬಿಸು_ಮೂಲ / 'build/user/start.o': 'lib/start.o',
            ಬಿಂಬಿಸು_ಮೂಲ / 'build/user/runtime.o': 'lib/runtime.o',
            ಬಿಂಬಿಸು_ಮೂಲ / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            ಬಿಂಬಿಸು_ಮೂಲ / 'ಬಳಕೆದಾರ/파일예제.cpp': 'examples/파일예제.cpp',
            ಬಿಂಬಿಸು_ಮೂಲ / '예제/한글코딩/인사.c': 'examples/인사.c',
            ಬಿಂಬಿಸು_ಮೂಲ / '예제/한글코딩/ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.c': 'examples/ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.c',
            ಬಿಂಬಿಸು_ಮೂಲ / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            ಬಿಂಬಿಸು_ಮೂಲ / 'ಬಳಕೆದಾರ/통신예제.cpp': 'examples/통신예제.cpp',
            ಬಿಂಬಿಸು_ಮೂಲ / 'build/user/demo.elf': 'examples/demo.elf',
            ಬಿಂಬಿಸು_ಮೂಲ / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, ಲಕ್ಷ್ಯ in ಫೈಲ್_ಪಟ್ಟಿ.items():
            ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ_ಇಮೇಲ್ = 개발꾸러미 / ಲಕ್ಷ್ಯ
            ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ_ಇಮೇಲ್.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ_ಇಮೇಲ್))
            꾸러미명세['sha256'][ಲಕ್ಷ್ಯ] = hashlib.sha256(ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ_ಇಮೇಲ್.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ಆರಂಭಿಸು_ಬಳಕೆದಾರ_ಅಪ್ಲಿ(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ಪರಿಕರಗಳು/ಪೂರೈಸು_ಫೈಲ್.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ಬಳಕೆದಾರ_ವಾದ() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ಅರ್ಖೀವ್ = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ಅರ್ಖೀವ್), 'w:gz') as ಮಾಪನ_ಡೇಟಾ:
            ಮಾಪನ_ಡೇಟಾ.add(str(개발꾸러미), arcname=개발꾸러미.name)
        ಅರ್ಖೀವ್.replace(배포경로 / ಅರ್ಖೀವ್.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as ಮಾಪನ_ಡೇಟಾ:
            for ಹೆಸರು in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ಮಾಪನ_ಡೇಟಾ.add(str(ಬಿಂಬಿಸು_ಮೂಲ.parents[1] / ಹೆಸರು), arcname='jkoros-native/' + ಹೆಸರು)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ಬಳಕೆದಾರ', '명명',
                             'ಪರಿಕರಗಳು/시언어번역기빌드.py', 'ಪರಿಕರಗಳು/ಬಿಲ್ಡ್_ಬಳಕೆದಾರ_ಸ್ಪೇಸ್.py', '파일전송과번역.md'):
                ಮಾಪನ_ಡೇಟಾ.add(str(ಬಿಂಬಿಸು_ಮೂಲ / 상대경로), arcname='jkoros-native/' + 상대경로)
            for ಹೆಸರು in ('crt.o', 'aot-runtime.o', 'ಸಾಮಾನ್ಯ_ಭಾಷೆಯ_ಚಾಲ್ತಿ_ಸಮಯ_ಬೆಂಬಲ.o', 'ಚಲಾಯಿಸು_2.o', '미리번역.o', '되돌림.o'):
                ತಲುಪುವ_ಫೈಲ್ = ಬಿಂಬಿಸು_ಮೂಲ / 'build/ccompiler' / ಹೆಸರು
                ಮಾಪನ_ಡೇಟಾ.add(str(ತಲುಪುವ_ಫೈಲ್), arcname='jkoros-native/relink/' + ಹೆಸರು)
            for ಹೆಸರು in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ಮಾಪನ_ಡೇಟಾ.add(str(ಬಿಂಬಿಸು_ಮೂಲ / 'build/user' / ಹೆಸರು), arcname='jkoros-native/relink/user/' + ಹೆಸರು)
            ಮಾಪನ_ಡೇಟಾ.add(str(ಬಿಂಬಿಸು_ಮೂಲ / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ಮಾಪನ_ಡೇಟಾ.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
