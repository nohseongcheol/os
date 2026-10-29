#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from thựcThiLệnh import gốcCâyDựÁn


def chạy():
    đườngDẫnBảnPhânPhối = gốcCâyDựÁn / 'dist'
    đườngDẫnBảnPhânPhối.mkdir(exist_ok=True)
    pOSIX = gốcCâyDựÁn.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(gốcCâyDựÁn / 'build')) as đườngDẫnĐangLàmViệc:
        bộCôngCụPhátTriển = Path(đườngDẫnĐangLàmViệc) / 'jkoros-native-sdk'
        danhSáchTệp = {
            gốcCâyDựÁn.parents[1] / 'LICENSE': 'LICENSE',
            gốcCâyDựÁn.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            gốcCâyDựÁn / 'CôngCụ/biênDịchSDK.py': 'compile.py',
            gốcCâyDựÁn / 'NgườiDùng/gọiThựcHiện.h': 'include/gọiThựcHiện.h',
            gốcCâyDựÁn / 'cáchĐặtTên/cácTênLiênKếtMáy.h': 'cáchĐặtTên/cácTênLiênKếtMáy.h',
            gốcCâyDựÁn / 'NgườiDùng/BốTríLiênKết.ld': 'user.ld',
            pOSIX / 'TệpĐầuMục/ABITệp.h': 'include/ABITệp.h',
            pOSIX / 'TệpĐầuMục/ABIMạng.h': 'include/ABIMạng.h',
            gốcCâyDựÁn / 'build/user/start.o': 'lib/start.o',
            gốcCâyDựÁn / 'build/user/runtime.o': 'lib/runtime.o',
            gốcCâyDựÁn / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            gốcCâyDựÁn / 'NgườiDùng/VíDụTệp.cpp': 'examples/VíDụTệp.cpp',
            gốcCâyDựÁn / 'VíDụ/LậpTrìnhHangul/LờiChào.c': 'examples/LờiChào.c',
            gốcCâyDựÁn / 'VíDụ/LậpTrìnhHangul/giáTrịLuồng.c': 'examples/giáTrịLuồng.c',
            gốcCâyDựÁn / 'VíDụ/LậpTrìnhHangul/LờiChào.cpp': 'examples/LờiChào.cpp',
            gốcCâyDựÁn / 'NgườiDùng/VíDụTruyềnThông.cpp': 'examples/VíDụTruyềnThông.cpp',
            gốcCâyDựÁn / 'build/user/demo.elf': 'examples/demo.elf',
            gốcCâyDựÁn / 'build/user/network.elf': 'examples/network.elf',
        }
        bảnKêGóiGộp = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for dữLiệuNguyênBản, giáTrịĐốiĐích in danhSáchTệp.items():
            địaChỉDữLiệuĐích = bộCôngCụPhátTriển / giáTrịĐốiĐích
            địaChỉDữLiệuĐích.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(dữLiệuNguyênBản), str(địaChỉDữLiệuĐích))
            bảnKêGóiGộp['sha256'][giáTrịĐốiĐích] = hashlib.sha256(địaChỉDữLiệuĐích.read_bytes()).hexdigest()
        (bộCôngCụPhátTriển / 'manifest.json').write_text(json.dumps(bảnKêGóiGộp, indent=2) + '\n')
        (bộCôngCụPhátTriển / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/VíDụTệp.cpp -o demo.elf\n'
            'python3 compile.py examples/LờiChào.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int bắtChạyChươngTrìnhNgườiDùng(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: CôngCụ/thựcThiLệnh.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 CôngCụ/thựcThiTệp.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: sốLượngĐốiSốNgườiDùng()/đốiSốNgườiDùng() in gọiThựcHiện.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        khoLưuTrữ = Path(đườngDẫnĐangLàmViệc) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(khoLưuTrữ), 'w:gz') as dữLiệuKếtQuả:
            dữLiệuKếtQuả.add(str(bộCôngCụPhátTriển), arcname=bộCôngCụPhátTriển.name)
        khoLưuTrữ.replace(đườngDẫnBảnPhânPhối / khoLưuTrữ.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        khoLưuTrữTrìnhBiênDịch = Path(đườngDẫnĐangLàmViệc) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(khoLưuTrữTrìnhBiênDịch), 'w:gz') as dữLiệuKếtQuả:
            for tên in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                dữLiệuKếtQuả.add(str(gốcCâyDựÁn.parents[1] / tên), arcname='jkoros-native/' + tên)
            for đườngDẫnTươngĐối in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'TrìnhBiênDịchC', 'NgườiDùng', 'cáchĐặtTên',
                             'CôngCụ/xâyDựngTrìnhBiênDịchC.py', 'CôngCụ/xâyDựngKhôngGianNgườiDùng.py', 'ViệcBiênDịchVàChuyểnGiaoTệp.md'):
                dữLiệuKếtQuả.add(str(gốcCâyDựÁn / đườngDẫnTươngĐối), arcname='jkoros-native/' + đườngDẫnTươngĐối)
            for tên in ('crt.o', 'aot-runtime.o', 'HỗTrợMôiTrườngChạy.o', 'chạy.o', 'thờiGianCủaTrước.o', 'cầuNốiTrảVề.o'):
                tệpĐích = gốcCâyDựÁn / 'build/ccompiler' / tên
                dữLiệuKếtQuả.add(str(tệpĐích), arcname='jkoros-native/relink/' + tên)
            for tên in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                dữLiệuKếtQuả.add(str(gốcCâyDựÁn / 'build/user' / tên), arcname='jkoros-native/relink/user/' + tên)
            dữLiệuKếtQuả.add(str(gốcCâyDựÁn / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            dữLiệuKếtQuả.add(str(pOSIX), arcname='posix-kor/arm64-native')
        khoLưuTrữTrìnhBiênDịch.replace(đườngDẫnBảnPhânPhối / khoLưuTrữTrìnhBiênDịch.name)
    print('SDK:', đườngDẫnBảnPhânPhối / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    chạy()
