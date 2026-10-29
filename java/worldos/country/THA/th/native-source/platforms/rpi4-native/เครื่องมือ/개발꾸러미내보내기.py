#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ดําเนินการ_คําสั่ง import แสดง_ราก


def เรียกใช้งาน():
    การกระจาย_พาธ = แสดง_ราก / 'dist'
    การกระจาย_พาธ.mkdir(exist_ok=True)
    포직스경로 = แสดง_ราก.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(แสดง_ราก / 'build')) as 작업경로:
        ชุดเครื่องมือการพัฒนา = Path(작업경로) / 'jkoros-native-sdk'
        แฟ้ม_รายการ = {
            แสดง_ราก.parents[1] / 'LICENSE': 'LICENSE',
            แสดง_ราก.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            แสดง_ราก / 'เครื่องมือ/개발꾸러미번역.py': 'compile.py',
            แสดง_ราก / 'ผู้ใช้/호출.h': 'include/호출.h',
            แสดง_ราก / '명명/기계연결이름.h': '명명/기계연결이름.h',
            แสดง_ราก / 'ผู้ใช้/ลิงก์_การนําทาง.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            แสดง_ราก / 'build/user/start.o': 'lib/start.o',
            แสดง_ราก / 'build/user/runtime.o': 'lib/runtime.o',
            แสดง_ราก / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            แสดง_ราก / 'ผู้ใช้/파일예제.cpp': 'examples/파일예제.cpp',
            แสดง_ราก / '예제/한글코딩/인사.c': 'examples/인사.c',
            แสดง_ราก / '예제/한글코딩/สตรีม_ค่า.c': 'examples/สตรีม_ค่า.c',
            แสดง_ราก / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            แสดง_ราก / 'ผู้ใช้/통신예제.cpp': 'examples/통신예제.cpp',
            แสดง_ราก / 'build/user/demo.elf': 'examples/demo.elf',
            แสดง_ราก / 'build/user/network.elf': 'examples/network.elf',
        }
        รวม_ไฟล์กํากับ = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, เป้าหมาย in แฟ้ม_รายการ.items():
            ปลายทาง_ข้อมูล_อีเมล = ชุดเครื่องมือการพัฒนา / เป้าหมาย
            ปลายทาง_ข้อมูล_อีเมล.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ปลายทาง_ข้อมูล_อีเมล))
            รวม_ไฟล์กํากับ['sha256'][เป้าหมาย] = hashlib.sha256(ปลายทาง_ข้อมูล_อีเมล.read_bytes()).hexdigest()
        (ชุดเครื่องมือการพัฒนา / 'manifest.json').write_text(json.dumps(รวม_ไฟล์กํากับ, indent=2) + '\n')
        (ชุดเครื่องมือการพัฒนา / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int เริ่ม_ผู้ใช้_แอป(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: เครื่องมือ/ดําเนินการ_คําสั่ง.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 เครื่องมือ/ดําเนินการ_แฟ้ม.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ผู้ใช้_อาร์กิวเมนต์() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        เก็บถาวร = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(เก็บถาวร), 'w:gz') as เมตริก_ข้อมูล:
            เมตริก_ข้อมูล.add(str(ชุดเครื่องมือการพัฒนา), arcname=ชุดเครื่องมือการพัฒนา.name)
        เก็บถาวร.replace(การกระจาย_พาธ / เก็บถาวร.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        คอมไพเลอร์_เก็บถาวร = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(คอมไพเลอร์_เก็บถาวร), 'w:gz') as เมตริก_ข้อมูล:
            for ชื่อ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                เมตริก_ข้อมูล.add(str(แสดง_ราก.parents[1] / ชื่อ), arcname='jkoros-native/' + ชื่อ)
            for เส้นทางสัมพัทธ์ in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ผู้ใช้', '명명',
                             'เครื่องมือ/시언어번역기빌드.py', 'เครื่องมือ/รุ่น_ผู้ใช้_สเปซ.py', '파일전송과번역.md'):
                เมตริก_ข้อมูล.add(str(แสดง_ราก / เส้นทางสัมพัทธ์), arcname='jkoros-native/' + เส้นทางสัมพัทธ์)
            for ชื่อ in ('crt.o', 'aot-runtime.o', 'รันไทม์_สนับสนุน.o', 'เรียกใช้งาน.o', '미리번역.o', 'ส่งคืน_บริดจ์.o'):
                แฟ้มปลายทาง = แสดง_ราก / 'build/ccompiler' / ชื่อ
                เมตริก_ข้อมูล.add(str(แฟ้มปลายทาง), arcname='jkoros-native/relink/' + ชื่อ)
            for ชื่อ in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                เมตริก_ข้อมูล.add(str(แสดง_ราก / 'build/user' / ชื่อ), arcname='jkoros-native/relink/user/' + ชื่อ)
            เมตริก_ข้อมูล.add(str(แสดง_ราก / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            เมตริก_ข้อมูล.add(str(포직스경로), arcname='posix-kor/arm64-native')
        คอมไพเลอร์_เก็บถาวร.replace(การกระจาย_พาธ / คอมไพเลอร์_เก็บถาวร.name)
    print('SDK:', การกระจาย_พาธ / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    เรียกใช้งาน()
