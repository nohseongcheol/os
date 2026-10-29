#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट


def चलोवप():
    배포경로 = प्रॉजॅक्ट_रूट / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = प्रॉजॅक्ट_रूट.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(प्रॉजॅक्ट_रूट / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        फायल_सुची = {
            प्रॉजॅक्ट_रूट.parents[1] / 'LICENSE': 'LICENSE',
            प्रॉजॅक्ट_रूट.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            प्रॉजॅक्ट_रूट / 'साधनां/개발꾸러미번역.py': 'compile.py',
            प्रॉजॅक्ट_रूट / 'उपेगकर्तो/호출.h': 'include/호출.h',
            प्रॉजॅक्ट_रूट / '명명/기계연결이름.h': '명명/기계연결이름.h',
            प्रॉजॅक्ट_रूट / 'उपेगकर्तो/लिंक_रचणाय.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            प्रॉजॅक्ट_रूट / 'build/user/start.o': 'lib/start.o',
            प्रॉजॅक्ट_रूट / 'build/user/runtime.o': 'lib/runtime.o',
            प्रॉजॅक्ट_रूट / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            प्रॉजॅक्ट_रूट / 'उपेगकर्तो/파일예제.cpp': 'examples/파일예제.cpp',
            प्रॉजॅक्ट_रूट / '예제/한글코딩/인사.c': 'examples/인사.c',
            प्रॉजॅक्ट_रूट / '예제/한글코딩/Stream_मोल.c': 'examples/Stream_मोल.c',
            प्रॉजॅक्ट_रूट / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            प्रॉजॅक्ट_रूट / 'उपेगकर्तो/통신예제.cpp': 'examples/통신예제.cpp',
            प्रॉजॅक्ट_रूट / 'build/user/demo.elf': 'examples/demo.elf',
            प्रॉजॅक्ट_रूट / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, लक्ष्य in फायल_सुची.items():
            नियुक्त_स्थान_डेटा_नामो = 개발꾸러미 / लक्ष्य
            नियुक्त_स्थान_डेटा_नामो.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(नियुक्त_स्थान_डेटा_नामो))
            꾸러미명세['sha256'][लक्ष्य] = hashlib.sha256(नियुक्त_स्थान_डेटा_नामो.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_उपेगकर्तो_एप्लिकेशन(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: साधनां/पाळो_दिवचो_आदेश.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 साधनां/पाळो_दिवचो_फायल.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: उपेगकर्तो_युक्तीवाद_COUNT()/उपेगकर्तो_युक्तीवाद() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        संग्रह = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(संग्रह), 'w:gz') as मेजप_डेटा:
            मेजप_डेटा.add(str(개발꾸러미), arcname=개발꾸러미.name)
        संग्रह.replace(배포경로 / संग्रह.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as मेजप_डेटा:
            for नांव in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                मेजप_डेटा.add(str(प्रॉजॅक्ट_रूट.parents[1] / नांव), arcname='jkoros-native/' + नांव)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'उपेगकर्तो', '명명',
                             'साधनां/시언어번역기빌드.py', 'साधनां/दाळचे_उपेगकर्तो_SPACE.py', '파일전송과번역.md'):
                मेजप_डेटा.add(str(प्रॉजॅक्ट_रूट / 상대경로), arcname='jkoros-native/' + 상대경로)
            for नांव in ('crt.o', 'aot-runtime.o', 'सामान्य_भास_रनटायम_तेंको.o', 'चलोवप.o', '미리번역.o', 'return_ब्रिज.o'):
                नियुक्त_स्थानाची_फायल = प्रॉजॅक्ट_रूट / 'build/ccompiler' / नांव
                मेजप_डेटा.add(str(नियुक्त_स्थानाची_फायल), arcname='jkoros-native/relink/' + नांव)
            for नांव in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                मेजप_डेटा.add(str(प्रॉजॅक्ट_रूट / 'build/user' / नांव), arcname='jkoros-native/relink/user/' + नांव)
            मेजप_डेटा.add(str(प्रॉजॅक्ट_रूट / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            मेजप_डेटा.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    चलोवप()
