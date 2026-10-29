#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Gweithredu_gorchymyn import prosiect_gwraidd


def Gweithredu_2():
    배포경로 = prosiect_gwraidd / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = prosiect_gwraidd.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(prosiect_gwraidd / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ffeil_Rhestr = {
            prosiect_gwraidd.parents[1] / 'LICENSE': 'LICENSE',
            prosiect_gwraidd.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            prosiect_gwraidd / 'Offer/SDK_llunio.py': 'compile.py',
            prosiect_gwraidd / 'defnyddiwr/호출.h': 'include/호출.h',
            prosiect_gwraidd / '명명/기계연결이름.h': '명명/기계연결이름.h',
            prosiect_gwraidd / 'defnyddiwr/Dolen_Llywio.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            prosiect_gwraidd / 'build/user/start.o': 'lib/start.o',
            prosiect_gwraidd / 'build/user/runtime.o': 'lib/runtime.o',
            prosiect_gwraidd / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            prosiect_gwraidd / 'defnyddiwr/파일예제.cpp': 'examples/파일예제.cpp',
            prosiect_gwraidd / '예제/한글코딩/인사.c': 'examples/인사.c',
            prosiect_gwraidd / '예제/한글코딩/ffrwd_VALUE.c': 'examples/ffrwd_VALUE.c',
            prosiect_gwraidd / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            prosiect_gwraidd / 'defnyddiwr/통신예제.cpp': 'examples/통신예제.cpp',
            prosiect_gwraidd / 'build/user/demo.elf': 'examples/demo.elf',
            prosiect_gwraidd / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, targed in ffeil_Rhestr.items():
            cyrchfan_data_ADDRESS = 개발꾸러미 / targed
            cyrchfan_data_ADDRESS.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(cyrchfan_data_ADDRESS))
            꾸러미명세['sha256'][targed] = hashlib.sha256(cyrchfan_data_ADDRESS.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_defnyddiwr_Rhaglen(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Offer/Gweithredu_gorchymyn.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Offer/Gweithredu_ffeil.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: defnyddiwr_arg_COUNT()/defnyddiwr_arg() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Archif = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Archif), 'w:gz') as mesur_data:
            mesur_data.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Archif.replace(배포경로 / Archif.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as mesur_data:
            for Enw in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                mesur_data.add(str(prosiect_gwraidd.parents[1] / Enw), arcname='jkoros-native/' + Enw)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'defnyddiwr', '명명',
                             'Offer/시언어번역기빌드.py', 'Offer/llunio_defnyddiwr_lle.py', '파일전송과번역.md'):
                mesur_data.add(str(prosiect_gwraidd / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Enw in ('crt.o', 'aot-runtime.o', 'amser_rhedeg_iaith_gyffredin_Cymorth.o', 'Gweithredu_2.o', '미리번역.o', 'return_pont.o'):
                ffeil_derbyn = prosiect_gwraidd / 'build/ccompiler' / Enw
                mesur_data.add(str(ffeil_derbyn), arcname='jkoros-native/relink/' + Enw)
            for Enw in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                mesur_data.add(str(prosiect_gwraidd / 'build/user' / Enw), arcname='jkoros-native/relink/user/' + Enw)
            mesur_data.add(str(prosiect_gwraidd / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            mesur_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Gweithredu_2()
