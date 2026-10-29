#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from zbatoj_komandë import Project_rrënjë


def Ekzekuto():
    배포경로 = Project_rrënjë / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Project_rrënjë.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_rrënjë / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        skedar_Listë = {
            Project_rrënjë.parents[1] / 'LICENSE': 'LICENSE',
            Project_rrënjë.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_rrënjë / 'Mjete/개발꾸러미번역.py': 'compile.py',
            Project_rrënjë / 'përdorues/호출.h': 'include/호출.h',
            Project_rrënjë / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_rrënjë / 'përdorues/lidh_Navigimi.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_rrënjë / 'build/user/start.o': 'lib/start.o',
            Project_rrënjë / 'build/user/runtime.o': 'lib/runtime.o',
            Project_rrënjë / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_rrënjë / 'përdorues/파일예제.cpp': 'examples/파일예제.cpp',
            Project_rrënjë / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_rrënjë / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            Project_rrënjë / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_rrënjë / 'përdorues/통신예제.cpp': 'examples/통신예제.cpp',
            Project_rrënjë / 'build/user/demo.elf': 'examples/demo.elf',
            Project_rrënjë / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, objektiv in skedar_Listë.items():
            vendmbërritje_të_dhëna_email = 개발꾸러미 / objektiv
            vendmbërritje_të_dhëna_email.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(vendmbërritje_të_dhëna_email))
            꾸러미명세['sha256'][objektiv] = hashlib.sha256(vendmbërritje_të_dhëna_email.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int nis_përdorues_program(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Mjete/zbatoj_komandë.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Mjete/zbatoj_skedar.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: përdorues_argument_COUNT()/përdorues_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        arkiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(arkiv), 'w:gz') as llogaritje_të_dhëna:
            llogaritje_të_dhëna.add(str(개발꾸러미), arcname=개발꾸러미.name)
        arkiv.replace(배포경로 / arkiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as llogaritje_të_dhëna:
            for Emër in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                llogaritje_të_dhëna.add(str(Project_rrënjë.parents[1] / Emër), arcname='jkoros-native/' + Emër)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'përdorues', '명명',
                             'Mjete/시언어번역기빌드.py', 'Mjete/ndërtoj_përdorues_HAPËSIRË.py', '파일전송과번역.md'):
                llogaritje_të_dhëna.add(str(Project_rrënjë / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Emër in ('crt.o', 'aot-runtime.o', 'koha_e_ekzekutimit_të_gjuhës_së_zakonshme_Mbështetje.o', 'Ekzekuto.o', '미리번역.o', 'Kthe_urë.o'):
                skedari_i_vendmbërritjes = Project_rrënjë / 'build/ccompiler' / Emër
                llogaritje_të_dhëna.add(str(skedari_i_vendmbërritjes), arcname='jkoros-native/relink/' + Emër)
            for Emër in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                llogaritje_të_dhëna.add(str(Project_rrënjë / 'build/user' / Emër), arcname='jkoros-native/relink/user/' + Emër)
            llogaritje_të_dhëna.add(str(Project_rrënjë / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            llogaritje_të_dhëna.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Ekzekuto()
