#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from εκτελώ_εντολή import έργο_ρίζα


def Εκτέλεση_2():
    배포경로 = έργο_ρίζα / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = έργο_ρίζα.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(έργο_ρίζα / 'build')) as 작업경로:
        κιτ_ανάπτυξης_λογισμικού = Path(작업경로) / 'jkoros-native-sdk'
        λίστα_αρχείων = {
            έργο_ρίζα.parents[1] / 'LICENSE': 'LICENSE',
            έργο_ρίζα.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            έργο_ρίζα / 'Εργαλεία/개발꾸러미번역.py': 'compile.py',
            έργο_ρίζα / 'χρήστης/호출.h': 'include/호출.h',
            έργο_ρίζα / '명명/기계연결이름.h': '명명/기계연결이름.h',
            έργο_ρίζα / 'χρήστης/συνδέω_Διάταξη.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            έργο_ρίζα / 'build/user/start.o': 'lib/start.o',
            έργο_ρίζα / 'build/user/runtime.o': 'lib/runtime.o',
            έργο_ρίζα / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            έργο_ρίζα / 'χρήστης/ΠαράδειγμαΑρχείου.cpp': 'examples/ΠαράδειγμαΑρχείου.cpp',
            έργο_ρίζα / '예제/한글코딩/인사.c': 'examples/인사.c',
            έργο_ρίζα / '예제/한글코딩/ροή_τιμή.c': 'examples/ροή_τιμή.c',
            έργο_ρίζα / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            έργο_ρίζα / 'χρήστης/통신예제.cpp': 'examples/통신예제.cpp',
            έργο_ρίζα / 'build/user/demo.elf': 'examples/demo.elf',
            έργο_ρίζα / 'build/user/network.elf': 'examples/network.elf',
        }
        πακέτο_διακήρυξη = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, τιμή_στόχος in λίστα_αρχείων.items():
            προορισμός_δεδομένα_διεύθυνση = κιτ_ανάπτυξης_λογισμικού / τιμή_στόχος
            προορισμός_δεδομένα_διεύθυνση.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(προορισμός_δεδομένα_διεύθυνση))
            πακέτο_διακήρυξη['sha256'][τιμή_στόχος] = hashlib.sha256(προορισμός_δεδομένα_διεύθυνση.read_bytes()).hexdigest()
        (κιτ_ανάπτυξης_λογισμικού / 'manifest.json').write_text(json.dumps(πακέτο_διακήρυξη, indent=2) + '\n')
        (κιτ_ανάπτυξης_λογισμικού / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ΠαράδειγμαΑρχείου.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int αρχή_χρήστης_εφαρμογή(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Εργαλεία/εκτελώ_εντολή.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Εργαλεία/εκτελώ_Αρχείο.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/χρήστης_όρισμα() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Αρχειοθήκη = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Αρχειοθήκη), 'w:gz') as μέτρηση_δεδομένα:
            μέτρηση_δεδομένα.add(str(κιτ_ανάπτυξης_λογισμικού), arcname=κιτ_ανάπτυξης_λογισμικού.name)
        Αρχειοθήκη.replace(배포경로 / Αρχειοθήκη.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        πρόγραμμα_μεταγλώττισης_Αρχειοθήκη = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(πρόγραμμα_μεταγλώττισης_Αρχειοθήκη), 'w:gz') as μέτρηση_δεδομένα:
            for Όνομα in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                μέτρηση_δεδομένα.add(str(έργο_ρίζα.parents[1] / Όνομα), arcname='jkoros-native/' + Όνομα)
            for σχετική_διαδρομή in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης', 'χρήστης', '명명',
                             'Εργαλεία/δομή_Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης.py', 'Εργαλεία/δομή_χρήστης_χώρος.py', '파일전송과번역.md'):
                μέτρηση_δεδομένα.add(str(έργο_ρίζα / σχετική_διαδρομή), arcname='jkoros-native/' + σχετική_διαδρομή)
            for Όνομα in ('crt.o', 'aot-runtime.o', 'περιβάλλον_εκτέλεσης_στήριγμα.o', 'Εκτέλεση_2.o', '미리번역.o', 'επιστρέφω_γέφυρα.o'):
                αρχείο_προορισμού = έργο_ρίζα / 'build/ccompiler' / Όνομα
                μέτρηση_δεδομένα.add(str(αρχείο_προορισμού), arcname='jkoros-native/relink/' + Όνομα)
            for Όνομα in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                μέτρηση_δεδομένα.add(str(έργο_ρίζα / 'build/user' / Όνομα), arcname='jkoros-native/relink/user/' + Όνομα)
            μέτρηση_δεδομένα.add(str(έργο_ρίζα / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            μέτρηση_δεδομένα.add(str(포직스경로), arcname='posix-kor/arm64-native')
        πρόγραμμα_μεταγλώττισης_Αρχειοθήκη.replace(배포경로 / πρόγραμμα_μεταγλώττισης_Αρχειοθήκη.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Εκτέλεση_2()
