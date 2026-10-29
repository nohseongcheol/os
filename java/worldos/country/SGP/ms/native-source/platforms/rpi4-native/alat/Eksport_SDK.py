#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from laksanakan_perintah import projek_akar


def Jalan():
    배포경로 = projek_akar / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = projek_akar.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(projek_akar / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        fail_Senarai = {
            projek_akar.parents[1] / 'LICENSE': 'LICENSE',
            projek_akar.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            projek_akar / 'alat/SDK_bina.py': 'compile.py',
            projek_akar / 'ruang_pengguna/호출.h': 'include/호출.h',
            projek_akar / '명명/기계연결이름.h': '명명/기계연결이름.h',
            projek_akar / 'ruang_pengguna/susun_atur_pautan.ld': 'user.ld',
            포직스경로 / 'pengisytiharan/파일규약.h': 'include/파일규약.h',
            포직스경로 / 'pengisytiharan/통신규약.h': 'include/통신규약.h',
            projek_akar / 'build/user/start.o': 'lib/start.o',
            projek_akar / 'build/user/runtime.o': 'lib/runtime.o',
            projek_akar / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            projek_akar / 'ruang_pengguna/ContohFail.cpp': 'examples/ContohFail.cpp',
            projek_akar / '예제/한글코딩/인사.c': 'examples/인사.c',
            projek_akar / '예제/한글코딩/strim_VALUE.c': 'examples/strim_VALUE.c',
            projek_akar / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            projek_akar / 'ruang_pengguna/통신예제.cpp': 'examples/통신예제.cpp',
            projek_akar / 'build/user/demo.elf': 'examples/demo.elf',
            projek_akar / 'build/user/network.elf': 'examples/network.elf',
        }
        pakej_manifes_aplikasi = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, sasaran in fail_Senarai.items():
            destinasi_data_e_mel = 개발꾸러미 / sasaran
            destinasi_data_e_mel.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(destinasi_data_e_mel))
            pakej_manifes_aplikasi['sha256'][sasaran] = hashlib.sha256(destinasi_data_e_mel.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(pakej_manifes_aplikasi, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ContohFail.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Mula_pengguna_aplikasi(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: alat/laksanakan_perintah.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 alat/laksanakan_fail.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: pengguna_argumen_COUNT()/pengguna_argumen() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arkib = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arkib), 'w:gz') as ukuran_data:
            ukuran_data.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Arkib.replace(배포경로 / Arkib.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as ukuran_data:
            for Nama in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ukuran_data.add(str(projek_akar.parents[1] / Nama), arcname='jkoros-native/' + Nama)
            for laluan_relatif in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ruang_pengguna', '명명',
                             'alat/시언어번역기빌드.py', 'alat/bina_pengguna_SPACE.py', '파일전송과번역.md'):
                ukuran_data.add(str(projek_akar / laluan_relatif), arcname='jkoros-native/' + laluan_relatif)
            for Nama in ('crt.o', 'aot-runtime.o', 'masa_jalan_bahasa_biasa_Sokongan.o', 'Jalan.o', '미리번역.o', 'kembalikan_penghubung.o'):
                fail_destinasi = projek_akar / 'build/ccompiler' / Nama
                ukuran_data.add(str(fail_destinasi), arcname='jkoros-native/relink/' + Nama)
            for Nama in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ukuran_data.add(str(projek_akar / 'build/user' / Nama), arcname='jkoros-native/relink/user/' + Nama)
            ukuran_data.add(str(projek_akar / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ukuran_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Jalan()
