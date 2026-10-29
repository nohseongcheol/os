#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from gnìomhaich_àithne import tilg_freumh


def ruith():
    배포경로 = tilg_freumh / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = tilg_freumh.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(tilg_freumh / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        faidhle_Liosta = {
            tilg_freumh.parents[1] / 'LICENSE': 'LICENSE',
            tilg_freumh.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            tilg_freumh / 'innealan/개발꾸러미번역.py': 'compile.py',
            tilg_freumh / 'cleachdaiche/호출.h': 'include/호출.h',
            tilg_freumh / '명명/기계연결이름.h': '명명/기계연결이름.h',
            tilg_freumh / 'cleachdaiche/ceangal_co_dhealbhachd.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            tilg_freumh / 'build/user/start.o': 'lib/start.o',
            tilg_freumh / 'build/user/runtime.o': 'lib/runtime.o',
            tilg_freumh / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            tilg_freumh / 'cleachdaiche/파일예제.cpp': 'examples/파일예제.cpp',
            tilg_freumh / '예제/한글코딩/인사.c': 'examples/인사.c',
            tilg_freumh / '예제/한글코딩/sruth_VALUE.c': 'examples/sruth_VALUE.c',
            tilg_freumh / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            tilg_freumh / 'cleachdaiche/통신예제.cpp': 'examples/통신예제.cpp',
            tilg_freumh / 'build/user/demo.elf': 'examples/demo.elf',
            tilg_freumh / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, targaid in faidhle_Liosta.items():
            ceann_uidhe_dàta_ADDRESS = 개발꾸러미 / targaid
            ceann_uidhe_dàta_ADDRESS.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ceann_uidhe_dàta_ADDRESS))
            꾸러미명세['sha256'][targaid] = hashlib.sha256(ceann_uidhe_dàta_ADDRESS.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_cleachdaiche_ap(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: innealan/gnìomhaich_àithne.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 innealan/gnìomhaich_faidhle.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: cleachdaiche_argamaid_COUNT()/cleachdaiche_argamaid() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        taisg = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(taisg), 'w:gz') as tomhas_dàta:
            tomhas_dàta.add(str(개발꾸러미), arcname=개발꾸러미.name)
        taisg.replace(배포경로 / taisg.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as tomhas_dàta:
            for Ainm in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                tomhas_dàta.add(str(tilg_freumh.parents[1] / Ainm), arcname='jkoros-native/' + Ainm)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'cleachdaiche', '명명',
                             'innealan/시언어번역기빌드.py', 'innealan/tog_cleachdaiche_spàs.py', '파일전송과번역.md'):
                tomhas_dàta.add(str(tilg_freumh / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Ainm in ('crt.o', 'aot-runtime.o', 'Common_Language_Runtime_taic.o', 'ruith.o', '미리번역.o', 'return_drochaid.o'):
                faidhle_uidhe = tilg_freumh / 'build/ccompiler' / Ainm
                tomhas_dàta.add(str(faidhle_uidhe), arcname='jkoros-native/relink/' + Ainm)
            for Ainm in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                tomhas_dàta.add(str(tilg_freumh / 'build/user' / Ainm), arcname='jkoros-native/relink/user/' + Ainm)
            tomhas_dàta.add(str(tilg_freumh / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            tomhas_dàta.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ruith()
