#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट


def चलाउनुहोस्():
    배포경로 = परियोजना_रूट / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = परियोजना_रूट.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(परियोजना_रूट / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        फाइल_सूची = {
            परियोजना_रूट.parents[1] / 'LICENSE': 'LICENSE',
            परियोजना_रूट.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            परियोजना_रूट / 'उपकरणहरू/개발꾸러미번역.py': 'compile.py',
            परियोजना_रूट / 'प्रयोगकर्ता/호출.h': 'include/호출.h',
            परियोजना_रूट / '명명/기계연결이름.h': '명명/기계연결이름.h',
            परियोजना_रूट / 'प्रयोगकर्ता/लिङ्क_लेआउट.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            परियोजना_रूट / 'build/user/start.o': 'lib/start.o',
            परियोजना_रूट / 'build/user/runtime.o': 'lib/runtime.o',
            परियोजना_रूट / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            परियोजना_रूट / 'प्रयोगकर्ता/फाइलउदाहरण.cpp': 'examples/फाइलउदाहरण.cpp',
            परियोजना_रूट / '예제/한글코딩/인사.c': 'examples/인사.c',
            परियोजना_रूट / '예제/한글코딩/प्रवाह_मान.c': 'examples/प्रवाह_मान.c',
            परियोजना_रूट / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            परियोजना_रूट / 'प्रयोगकर्ता/통신예제.cpp': 'examples/통신예제.cpp',
            परियोजना_रूट / 'build/user/demo.elf': 'examples/demo.elf',
            परियोजना_रूट / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, लक्ष्य in फाइल_सूची.items():
            गन्तव्य_लगत_ठेगाना = 개발꾸러미 / लक्ष्य
            गन्तव्य_लगत_ठेगाना.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(गन्तव्य_लगत_ठेगाना))
            꾸러미명세['sha256'][लक्ष्य] = hashlib.sha256(गन्तव्य_लगत_ठेगाना.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/फाइलउदाहरण.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int सुरु_प्रयोगकर्ता_अनुप्रयोग(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 उपकरणहरू/कार्यान्वयन_गर्नुहोस्_फाइल.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/प्रयोगकर्ता_तर्क() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        सङ्ग्रह = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(सङ्ग्रह), 'w:gz') as मापन_लगत:
            मापन_लगत.add(str(개발꾸러미), arcname=개발꾸러미.name)
        सङ्ग्रह.replace(배포경로 / सङ्ग्रह.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as मापन_लगत:
            for नाम in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                मापन_लगत.add(str(परियोजना_रूट.parents[1] / नाम), arcname='jkoros-native/' + नाम)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'प्रयोगकर्ता', '명명',
                             'उपकरणहरू/시언어번역기빌드.py', 'उपकरणहरू/बनाउनुहोस्_प्रयोगकर्ता_स्थान.py', '파일전송과번역.md'):
                मापन_लगत.add(str(परियोजना_रूट / 상대경로), arcname='jkoros-native/' + 상대경로)
            for नाम in ('crt.o', 'aot-runtime.o', 'सामान्य_भाषा_चालु_समय_समर्थन.o', 'चलाउनुहोस्.o', '미리번역.o', '되돌림.o'):
                गन्तव्य_फाइल = परियोजना_रूट / 'build/ccompiler' / नाम
                मापन_लगत.add(str(गन्तव्य_फाइल), arcname='jkoros-native/relink/' + नाम)
            for नाम in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                मापन_लगत.add(str(परियोजना_रूट / 'build/user' / नाम), arcname='jkoros-native/relink/user/' + नाम)
            मापन_लगत.add(str(परियोजना_रूट / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            मापन_लगत.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    चलाउनुहोस्()
