#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ፈጽም_ትእዛዝ import አሳይ_ስር


def ማስኬጃ():
    배포경로 = አሳይ_ስር / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = አሳይ_ስር.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(አሳይ_ስር / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ፋይል_ዝርዝር = {
            አሳይ_ስር.parents[1] / 'LICENSE': 'LICENSE',
            አሳይ_ስር.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            አሳይ_ስር / 'መሳሪያዎች/개발꾸러미번역.py': 'compile.py',
            አሳይ_ስር / 'ተጠቃሚ/호출.h': 'include/호출.h',
            አሳይ_ስር / '명명/기계연결이름.h': '명명/기계연결이름.h',
            አሳይ_ስር / 'ተጠቃሚ/አገናኝ_አሰሳ.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            አሳይ_ስር / 'build/user/start.o': 'lib/start.o',
            አሳይ_ስር / 'build/user/runtime.o': 'lib/runtime.o',
            አሳይ_ስር / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            አሳይ_ስር / 'ተጠቃሚ/파일예제.cpp': 'examples/파일예제.cpp',
            አሳይ_ስር / '예제/한글코딩/인사.c': 'examples/인사.c',
            አሳይ_ስር / '예제/한글코딩/ልቀቅ_እሴት.c': 'examples/ልቀቅ_እሴት.c',
            አሳይ_ስር / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            አሳይ_ስር / 'ተጠቃሚ/통신예제.cpp': 'examples/통신예제.cpp',
            አሳይ_ስር / 'build/user/demo.elf': 'examples/demo.elf',
            አሳይ_ስር / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, ዓላማ in ፋይል_ዝርዝር.items():
            መድረሻ_ውሂብ_አድራሻ = 개발꾸러미 / ዓላማ
            መድረሻ_ውሂብ_አድራሻ.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(መድረሻ_ውሂብ_አድራሻ))
            꾸러미명세['sha256'][ዓላማ] = hashlib.sha256(መድረሻ_ውሂብ_አድራሻ.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ጀምር_ተጠቃሚ_ፕሮግራም(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: መሳሪያዎች/ፈጽም_ትእዛዝ.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 መሳሪያዎች/ፈጽም_ፋይል.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ተጠቃሚ_ነጋሪ_እሴት() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ከዝን = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ከዝን), 'w:gz') as ልኬት_ውሂብ:
            ልኬት_ውሂብ.add(str(개발꾸러미), arcname=개발꾸러미.name)
        ከዝን.replace(배포경로 / ከዝን.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as ልኬት_ውሂብ:
            for ስም in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ልኬት_ውሂብ.add(str(አሳይ_ስር.parents[1] / ስም), arcname='jkoros-native/' + ስም)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ተጠቃሚ', '명명',
                             'መሳሪያዎች/시언어번역기빌드.py', 'መሳሪያዎች/ግንብ_ተጠቃሚ_ቦታ.py', '파일전송과번역.md'):
                ልኬት_ውሂብ.add(str(አሳይ_ስር / 상대경로), arcname='jkoros-native/' + 상대경로)
            for ስም in ('crt.o', 'aot-runtime.o', 'የጋራ_ቋንቋ_ማስኬጃ_ጊዜ_ድገፍ.o', 'ማስኬጃ.o', '미리번역.o', '되돌림.o'):
                መድረሻ_ፋይል = አሳይ_ስር / 'build/ccompiler' / ስም
                ልኬት_ውሂብ.add(str(መድረሻ_ፋይል), arcname='jkoros-native/relink/' + ስም)
            for ስም in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ልኬት_ውሂብ.add(str(አሳይ_ስር / 'build/user' / ስም), arcname='jkoros-native/relink/user/' + ስም)
            ልኬት_ውሂብ.add(str(አሳይ_ስር / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ልኬት_ውሂብ.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ማስኬጃ()
