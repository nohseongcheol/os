#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ


def ແລ່ນ():
    배포경로 = ໂຄງ_ການ_ເລກຮາກ / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = ໂຄງ_ການ_ເລກຮາກ.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(ໂຄງ_ການ_ເລກຮາກ / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ຟາຍ_ລາຍຊື່ = {
            ໂຄງ_ການ_ເລກຮາກ.parents[1] / 'LICENSE': 'LICENSE',
            ໂຄງ_ການ_ເລກຮາກ.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            ໂຄງ_ການ_ເລກຮາກ / 'ເຄື່ອງມື/개발꾸러미번역.py': 'compile.py',
            ໂຄງ_ການ_ເລກຮາກ / 'ຜູ້ໃຊ້/호출.h': 'include/호출.h',
            ໂຄງ_ການ_ເລກຮາກ / '명명/기계연결이름.h': '명명/기계연결이름.h',
            ໂຄງ_ການ_ເລກຮາກ / 'ຜູ້ໃຊ້/ລິ້ງ_ຮູບແບບ.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            ໂຄງ_ການ_ເລກຮາກ / 'build/user/start.o': 'lib/start.o',
            ໂຄງ_ການ_ເລກຮາກ / 'build/user/runtime.o': 'lib/runtime.o',
            ໂຄງ_ການ_ເລກຮາກ / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            ໂຄງ_ການ_ເລກຮາກ / 'ຜູ້ໃຊ້/파일예제.cpp': 'examples/파일예제.cpp',
            ໂຄງ_ການ_ເລກຮາກ / '예제/한글코딩/인사.c': 'examples/인사.c',
            ໂຄງ_ການ_ເລກຮາກ / '예제/한글코딩/ສະຕຣີມ_ຄ່າ.c': 'examples/ສະຕຣີມ_ຄ່າ.c',
            ໂຄງ_ການ_ເລກຮາກ / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            ໂຄງ_ການ_ເລກຮາກ / 'ຜູ້ໃຊ້/통신예제.cpp': 'examples/통신예제.cpp',
            ໂຄງ_ການ_ເລກຮາກ / 'build/user/demo.elf': 'examples/demo.elf',
            ໂຄງ_ການ_ເລກຮາກ / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, ເປົ້າ_ຫມາຍ in ຟາຍ_ລາຍຊື່.items():
            ປາຍທາງ_ຂໍ້ມູນ_ອີເມວ = 개발꾸러미 / ເປົ້າ_ຫມາຍ
            ປາຍທາງ_ຂໍ້ມູນ_ອີເມວ.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ປາຍທາງ_ຂໍ້ມູນ_ອີເມວ))
            꾸러미명세['sha256'][ເປົ້າ_ຫມາຍ] = hashlib.sha256(ປາຍທາງ_ຂໍ້ມູນ_ອີເມວ.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ເລີ່ມ_ຜູ້ໃຊ້_ແອັບ(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຟາຍ.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ຜູ້ໃຊ້_ຂໍ້ພິສູດ() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ການສໍາເນົາ = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ການສໍາເນົາ), 'w:gz') as ມາດຕະການ_ຂໍ້ມູນ:
            ມາດຕະການ_ຂໍ້ມູນ.add(str(개발꾸러미), arcname=개발꾸러미.name)
        ການສໍາເນົາ.replace(배포경로 / ການສໍາເນົາ.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as ມາດຕະການ_ຂໍ້ມູນ:
            for ຊື່ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ມາດຕະການ_ຂໍ້ມູນ.add(str(ໂຄງ_ການ_ເລກຮາກ.parents[1] / ຊື່), arcname='jkoros-native/' + ຊື່)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ຜູ້ໃຊ້', '명명',
                             'ເຄື່ອງມື/시언어번역기빌드.py', 'ເຄື່ອງມື/ສ້າງ_ຜູ້ໃຊ້_ພື້ນທີ່.py', '파일전송과번역.md'):
                ມາດຕະການ_ຂໍ້ມູນ.add(str(ໂຄງ_ການ_ເລກຮາກ / 상대경로), arcname='jkoros-native/' + 상대경로)
            for ຊື່ in ('crt.o', 'aot-runtime.o', '실행지원.o', 'ແລ່ນ.o', '미리번역.o', '되돌림.o'):
                ຟາຍປາຍທາງ = ໂຄງ_ການ_ເລກຮາກ / 'build/ccompiler' / ຊື່
                ມາດຕະການ_ຂໍ້ມູນ.add(str(ຟາຍປາຍທາງ), arcname='jkoros-native/relink/' + ຊື່)
            for ຊື່ in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ມາດຕະການ_ຂໍ້ມູນ.add(str(ໂຄງ_ການ_ເລກຮາກ / 'build/user' / ຊື່), arcname='jkoros-native/relink/user/' + ຊື່)
            ມາດຕະການ_ຂໍ້ມູນ.add(str(ໂຄງ_ການ_ເລກຮາກ / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ມາດຕະການ_ຂໍ້ມູນ.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ແລ່ນ()
