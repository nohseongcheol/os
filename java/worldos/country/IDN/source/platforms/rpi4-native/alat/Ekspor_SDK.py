#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Jalankan_perintah import Tugas_akar


def jalankan():
    배포경로 = Tugas_akar / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Tugas_akar.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Tugas_akar / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        file_Daftar = {
            Tugas_akar.parents[1] / 'LICENSE': 'LICENSE',
            Tugas_akar.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Tugas_akar / 'alat/SDK_bangun.py': 'compile.py',
            Tugas_akar / 'ruang_pengguna/호출.h': 'include/호출.h',
            Tugas_akar / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Tugas_akar / 'ruang_pengguna/tata_letak_penautan.ld': 'user.ld',
            포직스경로 / 'deklarasi/파일규약.h': 'include/파일규약.h',
            포직스경로 / 'deklarasi/통신규약.h': 'include/통신규약.h',
            Tugas_akar / 'build/user/start.o': 'lib/start.o',
            Tugas_akar / 'build/user/runtime.o': 'lib/runtime.o',
            Tugas_akar / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Tugas_akar / 'ruang_pengguna/ContohBerkas.cpp': 'examples/ContohBerkas.cpp',
            Tugas_akar / '예제/한글코딩/인사.c': 'examples/인사.c',
            Tugas_akar / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            Tugas_akar / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Tugas_akar / 'ruang_pengguna/통신예제.cpp': 'examples/통신예제.cpp',
            Tugas_akar / 'build/user/demo.elf': 'examples/demo.elf',
            Tugas_akar / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, target in file_Daftar.items():
            tujuan_data_surel = 개발꾸러미 / target
            tujuan_data_surel.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(tujuan_data_surel))
            꾸러미명세['sha256'][target] = hashlib.sha256(tujuan_data_surel.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ContohBerkas.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Mulai_pengguna_apl(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: alat/Jalankan_perintah.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 alat/Jalankan_file.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: pengguna_argumen_COUNT()/pengguna_argumen() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arsip = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arsip), 'w:gz') as KR_data:
            KR_data.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Arsip.replace(배포경로 / Arsip.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as KR_data:
            for Nama_2 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_data.add(str(Tugas_akar.parents[1] / Nama_2), arcname='jkoros-native/' + Nama_2)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ruang_pengguna', '명명',
                             'alat/시언어번역기빌드.py', 'alat/build_pengguna_SPACE.py', '파일전송과번역.md'):
                KR_data.add(str(Tugas_akar / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Nama_2 in ('crt.o', 'aot-runtime.o', 'runtime_bahasa_umum_dukung.o', 'jalankan.o', '미리번역.o', 'kembalikan_bridge.o'):
                file_tujuan = Tugas_akar / 'build/ccompiler' / Nama_2
                KR_data.add(str(file_tujuan), arcname='jkoros-native/relink/' + Nama_2)
            for Nama_2 in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_data.add(str(Tugas_akar / 'build/user' / Nama_2), arcname='jkoros-native/relink/user/' + Nama_2)
            KR_data.add(str(Tugas_akar / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    jalankan()
