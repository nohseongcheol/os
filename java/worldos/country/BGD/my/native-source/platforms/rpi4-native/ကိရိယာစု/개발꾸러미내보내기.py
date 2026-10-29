#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from စက်မောင်း import စီမံကိန်းအမြစ်


def လုပ်ဆောင်():
    ဖြန့်ချိမှုလမ်းကြောင်း = စီမံကိန်းအမြစ် / 'dist'
    ဖြန့်ချိမှုလမ်းကြောင်း.mkdir(exist_ok=True)
    POSIX = စီမံကိန်းအမြစ်.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(စီမံကိန်းအမြစ် / 'build')) as လုပ်ဆောင်လမ်း:
        개발꾸러미 = Path(လုပ်ဆောင်လမ်း) / 'jkoros-native-sdk'
        ဖိုင်စာရင်း = {
            စီမံကိန်းအမြစ်.parents[1] / 'LICENSE': 'LICENSE',
            စီမံကိန်းအမြစ်.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            စီမံကိန်းအမြစ် / 'ကိရိယာစု/개발꾸러미번역.py': 'compile.py',
            စီမံကိန်းအမြစ် / 'သုံးစွဲသူ/ခေါ်လုပ်.h': 'include/ခေါ်လုပ်.h',
            စီမံကိန်းအမြစ် / '명명/စက်ချိတ်အမည်များ.h': '명명/စက်ချိတ်အမည်များ.h',
            စီမံကိန်းအမြစ် / 'သုံးစွဲသူ/နေရာချထားပုံ.ld': 'user.ld',
            POSIX / 'ခေါင်းစီးဖိုင်/파일규약.h': 'include/파일규약.h',
            POSIX / 'ခေါင်းစီးဖိုင်/통신규약.h': 'include/통신규약.h',
            စီမံကိန်းအမြစ် / 'build/user/start.o': 'lib/start.o',
            စီမံကိန်းအမြစ် / 'build/user/runtime.o': 'lib/runtime.o',
            စီမံကိန်းအမြစ် / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            စီမံကိန်းအမြစ် / 'သုံးစွဲသူ/ဖိုင်ဥပမာ.cpp': 'examples/ဖိုင်ဥပမာ.cpp',
            စီမံကိန်းအမြစ် / 'ဥပမာ/ဟန်ဂုကုဒ်ရေး/နှုတ်ဆက်.c': 'examples/နှုတ်ဆက်.c',
            စီမံကိန်းအမြစ် / 'ဥပမာ/ဟန်ဂုကုဒ်ရေး/စီးကြောင်းတန်ဖိုး.c': 'examples/စီးကြောင်းတန်ဖိုး.c',
            စီမံကိန်းအမြစ် / 'ဥပမာ/ဟန်ဂုကုဒ်ရေး/နှုတ်ဆက်.cpp': 'examples/နှုတ်ဆက်.cpp',
            စီမံကိန်းအမြစ် / 'သုံးစွဲသူ/ဆက်သွယ်မှုဥပမာ.cpp': 'examples/ဆက်သွယ်မှုဥပမာ.cpp',
            စီမံကိန်းအမြစ် / 'build/user/demo.elf': 'examples/demo.elf',
            စီမံကိန်းအမြစ် / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for မူရင်းဒေတာ, ဦးတည်ချက်တန်ဖိုး in ဖိုင်စာရင်း.items():
            ဦးတည်ရာဒေတာလိပ်စာ = 개발꾸러미 / ဦးတည်ချက်တန်ဖိုး
            ဦးတည်ရာဒေတာလိပ်စာ.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(မူရင်းဒေတာ), str(ဦးတည်ရာဒေတာလိပ်စာ))
            꾸러미명세['sha256'][ဦးတည်ချက်တန်ဖိုး] = hashlib.sha256(ဦးတည်ရာဒေတာလိပ်စာ.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ဖိုင်ဥပမာ.cpp -o demo.elf\n'
            'python3 compile.py examples/နှုတ်ဆက်.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int သုံးစွဲသူပရိုဂရမ်စတင်(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ကိရိယာစု/စက်မောင်း.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ကိရိယာစု/ဖိုင်လုပ်ဆောင်.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: သုံးစွဲသူပေးအချက်အရေအတွက်()/သုံးစွဲသူပေးအချက်() in ခေါ်လုပ်.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        မော်ကွန်း = Path(လုပ်ဆောင်လမ်း) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(မော်ကွန်း), 'w:gz') as ရလဒ်ဒေတာ:
            ရလဒ်ဒေတာ.add(str(개발꾸러미), arcname=개발꾸러미.name)
        မော်ကွန်း.replace(ဖြန့်ချိမှုလမ်းကြောင်း / မော်ကွန်း.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        ဘာသာပြန်စက်မော်ကွန်း = Path(လုပ်ဆောင်လမ်း) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(ဘာသာပြန်စက်မော်ကွန်း), 'w:gz') as ရလဒ်ဒေတာ:
            for အမည် in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ရလဒ်ဒေတာ.add(str(စီမံကိန်းအမြစ်.parents[1] / အမည်), arcname='jkoros-native/' + အမည်)
            for နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'Cဘာသာပြန်စက်', 'သုံးစွဲသူ', '명명',
                             'ကိရိယာစု/Cဘာသာပြန်စက်တည်ဆောက်.py', 'ကိရိယာစု/သုံးစွဲသူနေရာလပ်တည်ဆောက်.py', 'ဖိုင်လွှဲပြောင်းနှင့်ဘာသာပြန်မှု.md'):
                ရလဒ်ဒေတာ.add(str(စီမံကိန်းအမြစ် / နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း), arcname='jkoros-native/' + နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း)
            for အမည် in ('crt.o', 'aot-runtime.o', 'လည်ပတ်ဝန်းကျင်ထောက်ပံ့မှု.o', 'လုပ်ဆောင်.o', '미리번역.o', 'ပြန်ပေးတံတား.o'):
                ဦးတည်ရာဖိုင် = စီမံကိန်းအမြစ် / 'build/ccompiler' / အမည်
                ရလဒ်ဒေတာ.add(str(ဦးတည်ရာဖိုင်), arcname='jkoros-native/relink/' + အမည်)
            for အမည် in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ရလဒ်ဒေတာ.add(str(စီမံကိန်းအမြစ် / 'build/user' / အမည်), arcname='jkoros-native/relink/user/' + အမည်)
            ရလဒ်ဒေတာ.add(str(စီမံကိန်းအမြစ် / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ရလဒ်ဒေတာ.add(str(POSIX), arcname='posix-kor/arm64-native')
        ဘာသာပြန်စက်မော်ကွန်း.replace(ဖြန့်ချိမှုလမ်းကြောင်း / ဘာသာပြန်စက်မော်ကွန်း.name)
    print('SDK:', ဖြန့်ချိမှုလမ်းကြောင်း / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    လုပ်ဆောင်()
