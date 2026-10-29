#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ


def सुरू_करा():
    वितरण_पथ = प्रोजेक्ट_मूळ / 'dist'
    वितरण_पथ.mkdir(exist_ok=True)
    पॉझिक्स = प्रोजेक्ट_मूळ.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(प्रोजेक्ट_मूळ / 'build')) as कार्यरत_पथ:
        विकास_संच = Path(कार्यरत_पथ) / 'jkoros-native-sdk'
        संचिका_यादी = {
            प्रोजेक्ट_मूळ.parents[1] / 'LICENSE': 'LICENSE',
            प्रोजेक्ट_मूळ.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            प्रोजेक्ट_मूळ / 'साधने/विकाससाधनसंच_बांधणी.py': 'compile.py',
            प्रोजेक्ट_मूळ / 'प्रयोक्ता/आवाहन.h': 'include/आवाहन.h',
            प्रोजेक्ट_मूळ / 'नामकरण/मशीन_लिंक_नावे.h': 'नामकरण/मशीन_लिंक_नावे.h',
            प्रोजेक्ट_मूळ / 'प्रयोक्ता/लिंक_लेआउट.ld': 'user.ld',
            पॉझिक्स / 'घोषणाशीर्षे/संचिका_द्विमानजोडणी.h': 'include/संचिका_द्विमानजोडणी.h',
            पॉझिक्स / 'घोषणाशीर्षे/संचारजाळे_द्विमानजोडणी.h': 'include/संचारजाळे_द्विमानजोडणी.h',
            प्रोजेक्ट_मूळ / 'build/user/start.o': 'lib/start.o',
            प्रोजेक्ट_मूळ / 'build/user/runtime.o': 'lib/runtime.o',
            प्रोजेक्ट_मूळ / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            प्रोजेक्ट_मूळ / 'प्रयोक्ता/संचिका_उदाहरण.cpp': 'examples/संचिका_उदाहरण.cpp',
            प्रोजेक्ट_मूळ / 'उदाहरणे/हांगुल_संकेतन/अभिवादन_ae353e94.c': 'examples/अभिवादन_ae353e94.c',
            प्रोजेक्ट_मूळ / 'उदाहरणे/हांगुल_संकेतन/प्रवाह_मूल्य.c': 'examples/प्रवाह_मूल्य.c',
            प्रोजेक्ट_मूळ / 'उदाहरणे/हांगुल_संकेतन/अभिवादन_ae353e94.cpp': 'examples/अभिवादन_ae353e94.cpp',
            प्रोजेक्ट_मूळ / 'प्रयोक्ता/संचार_उदाहरण.cpp': 'examples/संचार_उदाहरण.cpp',
            प्रोजेक्ट_मूळ / 'build/user/demo.elf': 'examples/demo.elf',
            प्रोजेक्ट_मूळ / 'build/user/network.elf': 'examples/network.elf',
        }
        बंडल_सूचीलेख = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for मूळ_डेटा, लक्ष्य in संचिका_यादी.items():
            गंतव्यस्थान_डेटा_पत्ता = विकास_संच / लक्ष्य
            गंतव्यस्थान_डेटा_पत्ता.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(मूळ_डेटा), str(गंतव्यस्थान_डेटा_पत्ता))
            बंडल_सूचीलेख['sha256'][लक्ष्य] = hashlib.sha256(गंतव्यस्थान_डेटा_पत्ता.read_bytes()).hexdigest()
        (विकास_संच / 'manifest.json').write_text(json.dumps(बंडल_सूचीलेख, indent=2) + '\n')
        (विकास_संच / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/संचिका_उदाहरण.cpp -o demo.elf\n'
            'python3 compile.py examples/अभिवादन_ae353e94.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int प्रारंभ_प्रयोक्ता_अनुप्रयोग(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: साधने/आज्ञा_कार्यवाही_करा.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 साधने/संचिका_कार्यवाही_करा.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: प्रयोक्ता_वितर्क_संख्या()/प्रयोक्ता_वितर्क() in आवाहन.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        संग्रह = Path(कार्यरत_पथ) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(संग्रह), 'w:gz') as मोजमाप_डेटा:
            मोजमाप_डेटा.add(str(विकास_संच), arcname=विकास_संच.name)
        संग्रह.replace(वितरण_पथ / संग्रह.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        संकलक_संग्रह = Path(कार्यरत_पथ) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(संकलक_संग्रह), 'w:gz') as मोजमाप_डेटा:
            for नाव in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                मोजमाप_डेटा.add(str(प्रोजेक्ट_मूळ.parents[1] / नाव), arcname='jkoros-native/' + नाव)
            for सापेक्ष_पथ in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'सी_संकलक', 'प्रयोक्ता', 'नामकरण',
                             'साधने/सी_संकलक_बांधणी.py', 'साधने/प्रयोक्ता_जागा_बांधणी.py', 'संचिका_स्थानांतर_आणि_संकलन.md'):
                मोजमाप_डेटा.add(str(प्रोजेक्ट_मूळ / सापेक्ष_पथ), arcname='jkoros-native/' + सापेक्ष_पथ)
            for नाव in ('crt.o', 'aot-runtime.o', 'सामान्य_भाषा_रनटाइम_समर्थन.o', 'सुरू_करा.o', 'आगाऊ_संबंधित_वेळ.o', 'परतकरा_ब्रिज.o'):
                गंतव्य_फाइल = प्रोजेक्ट_मूळ / 'build/ccompiler' / नाव
                मोजमाप_डेटा.add(str(गंतव्य_फाइल), arcname='jkoros-native/relink/' + नाव)
            for नाव in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                मोजमाप_डेटा.add(str(प्रोजेक्ट_मूळ / 'build/user' / नाव), arcname='jkoros-native/relink/user/' + नाव)
            मोजमाप_डेटा.add(str(प्रोजेक्ट_मूळ / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            मोजमाप_डेटा.add(str(पॉझिक्स), arcname='posix-kor/arm64-native')
        संकलक_संग्रह.replace(वितरण_पथ / संकलक_संग्रह.name)
    print('SDK:', वितरण_पथ / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    सुरू_करा()
