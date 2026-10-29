#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Rith_ordú import teilgean_fréamh


def Rith_2():
    배포경로 = teilgean_fréamh / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = teilgean_fréamh.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(teilgean_fréamh / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        comhad_Liosta = {
            teilgean_fréamh.parents[1] / 'LICENSE': 'LICENSE',
            teilgean_fréamh.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            teilgean_fréamh / 'Uirlisí/SDK_tóg.py': 'compile.py',
            teilgean_fréamh / 'úsáideoir/호출.h': 'include/호출.h',
            teilgean_fréamh / '명명/기계연결이름.h': '명명/기계연결이름.h',
            teilgean_fréamh / 'úsáideoir/Nasc_dáileadh.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            teilgean_fréamh / 'build/user/start.o': 'lib/start.o',
            teilgean_fréamh / 'build/user/runtime.o': 'lib/runtime.o',
            teilgean_fréamh / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            teilgean_fréamh / 'úsáideoir/파일예제.cpp': 'examples/파일예제.cpp',
            teilgean_fréamh / '예제/한글코딩/인사.c': 'examples/인사.c',
            teilgean_fréamh / '예제/한글코딩/sruth_VALUE.c': 'examples/sruth_VALUE.c',
            teilgean_fréamh / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            teilgean_fréamh / 'úsáideoir/통신예제.cpp': 'examples/통신예제.cpp',
            teilgean_fréamh / 'build/user/demo.elf': 'examples/demo.elf',
            teilgean_fréamh / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, sprioc in comhad_Liosta.items():
            sprioc_sonraí_ADDRESS = 개발꾸러미 / sprioc
            sprioc_sonraí_ADDRESS.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(sprioc_sonraí_ADDRESS))
            꾸러미명세['sha256'][sprioc] = hashlib.sha256(sprioc_sonraí_ADDRESS.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_úsáideoir_clár(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Uirlisí/Rith_ordú.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Uirlisí/Rith_comhad.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: úsáideoir_argóint_COUNT()/úsáideoir_argóint() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Cartlann = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Cartlann), 'w:gz') as tomhas_sonraí:
            tomhas_sonraí.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Cartlann.replace(배포경로 / Cartlann.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as tomhas_sonraí:
            for Ainm in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                tomhas_sonraí.add(str(teilgean_fréamh.parents[1] / Ainm), arcname='jkoros-native/' + Ainm)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'úsáideoir', '명명',
                             'Uirlisí/시언어번역기빌드.py', 'Uirlisí/tóg_úsáideoir_spás.py', '파일전송과번역.md'):
                tomhas_sonraí.add(str(teilgean_fréamh / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Ainm in ('crt.o', 'aot-runtime.o', 'am_rite_teanga_coiteann_Tacaíocht.o', 'Rith_2.o', '미리번역.o', 'return_traschóiritheoir.o'):
                comhad_sprice = teilgean_fréamh / 'build/ccompiler' / Ainm
                tomhas_sonraí.add(str(comhad_sprice), arcname='jkoros-native/relink/' + Ainm)
            for Ainm in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                tomhas_sonraí.add(str(teilgean_fréamh / 'build/user' / Ainm), arcname='jkoros-native/relink/user/' + Ainm)
            tomhas_sonraí.add(str(teilgean_fréamh / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            tomhas_sonraí.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Rith_2()
