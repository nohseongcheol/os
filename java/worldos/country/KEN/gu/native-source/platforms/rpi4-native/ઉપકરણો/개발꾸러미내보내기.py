#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ


def ચલાવો_2():
    배포경로 = પ્રોજેક્ટ_રૂટ / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = પ્રોજેક્ટ_રૂટ.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(પ્રોજેક્ટ_રૂટ / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ફાઇલ_સૂચી = {
            પ્રોજેક્ટ_રૂટ.parents[1] / 'LICENSE': 'LICENSE',
            પ્રોજેક્ટ_રૂટ.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            પ્રોજેક્ટ_રૂટ / 'ઉપકરણો/개발꾸러미번역.py': 'compile.py',
            પ્રોજેક્ટ_રૂટ / 'ઉપયોગકર્તા/호출.h': 'include/호출.h',
            પ્રોજેક્ટ_રૂટ / '명명/기계연결이름.h': '명명/기계연결이름.h',
            પ્રોજેક્ટ_રૂટ / 'ઉપયોગકર્તા/લિંક_લેઆઉટ.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            પ્રોજેક્ટ_રૂટ / 'build/user/start.o': 'lib/start.o',
            પ્રોજેક્ટ_રૂટ / 'build/user/runtime.o': 'lib/runtime.o',
            પ્રોજેક્ટ_રૂટ / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            પ્રોજેક્ટ_રૂટ / 'ઉપયોગકર્તા/파일예제.cpp': 'examples/파일예제.cpp',
            પ્રોજેક્ટ_રૂટ / '예제/한글코딩/인사.c': 'examples/인사.c',
            પ્રોજેક્ટ_રૂટ / '예제/한글코딩/સ્ટ્રીમ_મૂલ્ય.c': 'examples/સ્ટ્રીમ_મૂલ્ય.c',
            પ્રોજેક્ટ_રૂટ / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            પ્રોજેક્ટ_રૂટ / 'ઉપયોગકર્તા/통신예제.cpp': 'examples/통신예제.cpp',
            પ્રોજેક્ટ_રૂટ / 'build/user/demo.elf': 'examples/demo.elf',
            પ્રોજેક્ટ_રૂટ / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, લક્ષ્ય in ફાઇલ_સૂચી.items():
            ગંતવ્ય_ડેટા_સરનામું = 개발꾸러미 / લક્ષ્ય
            ગંતવ્ય_ડેટા_સરનામું.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ગંતવ્ય_ડેટા_સરનામું))
            꾸러미명세['sha256'][લક્ષ્ય] = hashlib.sha256(ગંતવ્ય_ડેટા_સરનામું.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int પ્રારંભ_ઉપયોગકર્તા_એપ્લિકેશન(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ઉપકરણો/અમલ_કરો_આદેશ.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ઉપકરણો/અમલ_કરો_ફાઇલ.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ઉપયોગકર્તા_દલીલ() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        સંગ્રહ = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(સંગ્રહ), 'w:gz') as પરિમાણ_ડેટા:
            પરિમાણ_ડેટા.add(str(개발꾸러미), arcname=개발꾸러미.name)
        સંગ્રહ.replace(배포경로 / સંગ્રહ.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as પરિમાણ_ડેટા:
            for નામ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                પરિમાણ_ડેટા.add(str(પ્રોજેક્ટ_રૂટ.parents[1] / નામ), arcname='jkoros-native/' + નામ)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ઉપયોગકર્તા', '명명',
                             'ઉપકરણો/시언어번역기빌드.py', 'ઉપકરણો/બિલ્ડ_ઉપયોગકર્તા_જગ્યા.py', '파일전송과번역.md'):
                પરિમાણ_ડેટા.add(str(પ્રોજેક્ટ_રૂટ / 상대경로), arcname='jkoros-native/' + 상대경로)
            for નામ in ('crt.o', 'aot-runtime.o', 'સામાન્ય_ભાષા_રનટાઇમ_સપોર્ટ.o', 'ચલાવો_2.o', '미리번역.o', '되돌림.o'):
                ગંતવ્ય_ફાઇલ = પ્રોજેક્ટ_રૂટ / 'build/ccompiler' / નામ
                પરિમાણ_ડેટા.add(str(ગંતવ્ય_ફાઇલ), arcname='jkoros-native/relink/' + નામ)
            for નામ in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                પરિમાણ_ડેટા.add(str(પ્રોજેક્ટ_રૂટ / 'build/user' / નામ), arcname='jkoros-native/relink/user/' + નામ)
            પરિમાણ_ડેટા.add(str(પ્રોજેક્ટ_રૂટ / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            પરિમાણ_ડેટા.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ચલાવો_2()
