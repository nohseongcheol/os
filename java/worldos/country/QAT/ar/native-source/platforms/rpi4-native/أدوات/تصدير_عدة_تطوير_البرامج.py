#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ينفذ_أمر import يعرض_جذر


def تشغيل():
    توزيع_مسار = يعرض_جذر / 'dist'
    توزيع_مسار.mkdir(exist_ok=True)
    포직스경로 = يعرض_جذر.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(يعرض_جذر / 'build')) as 작업경로:
        أداة_التطوير = Path(작업경로) / 'jkoros-native-sdk'
        ملف_قائمة = {
            يعرض_جذر.parents[1] / 'LICENSE': 'LICENSE',
            يعرض_جذر.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            يعرض_جذر / 'أدوات/عدة_تطوير_البرامج_يحول_برمجياً.py': 'compile.py',
            يعرض_جذر / 'فضاء_المستخدم/호출.h': 'include/호출.h',
            يعرض_جذر / '명명/기계연결이름.h': '명명/기계연결이름.h',
            يعرض_جذر / 'فضاء_المستخدم/تخطيط_الربط.ld': 'user.ld',
            포직스경로 / 'تصريحات/파일규약.h': 'include/파일규약.h',
            포직스경로 / 'تصريحات/통신규약.h': 'include/통신규약.h',
            يعرض_جذر / 'build/user/start.o': 'lib/start.o',
            يعرض_جذر / 'build/user/runtime.o': 'lib/runtime.o',
            يعرض_جذر / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            يعرض_جذر / 'فضاء_المستخدم/مثالملف.cpp': 'examples/مثالملف.cpp',
            يعرض_جذر / '예제/한글코딩/인사.c': 'examples/인사.c',
            يعرض_جذر / '예제/한글코딩/بث_قيمة.c': 'examples/بث_قيمة.c',
            يعرض_جذر / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            يعرض_جذر / 'فضاء_المستخدم/통신예제.cpp': 'examples/통신예제.cpp',
            يعرض_جذر / 'build/user/demo.elf': 'examples/demo.elf',
            يعرض_جذر / 'build/user/network.elf': 'examples/network.elf',
        }
        يُجمع_بيان = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, الهدف in ملف_قائمة.items():
            وجهة_بيانات_عنوان = أداة_التطوير / الهدف
            وجهة_بيانات_عنوان.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(وجهة_بيانات_عنوان))
            يُجمع_بيان['sha256'][الهدف] = hashlib.sha256(وجهة_بيانات_عنوان.read_bytes()).hexdigest()
        (أداة_التطوير / 'manifest.json').write_text(json.dumps(يُجمع_بيان, indent=2) + '\n')
        (أداة_التطوير / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/مثالملف.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int بدء_مستخدم_تطبيق(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: أدوات/ينفذ_أمر.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 أدوات/ينفذ_ملف.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/مستخدم_وسيطة() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        أرشيف = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(أرشيف), 'w:gz') as مقياس_بيانات:
            مقياس_بيانات.add(str(أداة_التطوير), arcname=أداة_التطوير.name)
        أرشيف.replace(توزيع_مسار / أرشيف.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        محول_برمجي_أرشيف = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(محول_برمجي_أرشيف), 'w:gz') as مقياس_بيانات:
            for اسم in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                مقياس_بيانات.add(str(يعرض_جذر.parents[1] / اسم), arcname='jkoros-native/' + اسم)
            for مسار_نسبي in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'الرمز_البريدي_محول_برمجي', 'فضاء_المستخدم', '명명',
                             'أدوات/بنية_الرمز_البريدي_محول_برمجي.py', 'أدوات/بنية_مستخدم_مساحة.py', '파일전송과번역.md'):
                مقياس_بيانات.add(str(يعرض_جذر / مسار_نسبي), arcname='jkoros-native/' + مسار_نسبي)
            for اسم in ('crt.o', 'aot-runtime.o', 'دعمتشغيل.o', 'تشغيل.o', '미리번역.o', 'إرجاع_جسر.o'):
                الملف_الوجهة = يعرض_جذر / 'build/ccompiler' / اسم
                مقياس_بيانات.add(str(الملف_الوجهة), arcname='jkoros-native/relink/' + اسم)
            for اسم in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                مقياس_بيانات.add(str(يعرض_جذر / 'build/user' / اسم), arcname='jkoros-native/relink/user/' + اسم)
            مقياس_بيانات.add(str(يعرض_جذر / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            مقياس_بيانات.add(str(포직스경로), arcname='posix-kor/arm64-native')
        محول_برمجي_أرشيف.replace(توزيع_مسار / محول_برمجي_أرشيف.name)
    print('SDK:', توزيع_مسار / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    تشغيل()
