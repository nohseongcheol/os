#!/usr/bin/env python3
"""개인 कनेक्शन_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from दूरस्थ_सेटिंग import 준비
from COSL배포 import गंतव्य_नाम, लाइब्रेरी

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]


def चलाएँ():
    निर्गम = प्रोजेक्ट_करें_मूल / 'build/verification/password-length'
    निर्गम.mkdir(parents=True, exist_ok=True)
    निजी_सेटिंग = प्रोजेक्ट_करें_मूल / 'build/remote/access.json'
    원래설정 = निजी_सेटिंग.read_bytes()
    रिपोर्ट_मान = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            सेटिंग_पथ = 시험터 / 'build/remote'
            सेटिंग_पथ.mkdir(parents=True)
            सेटिंग_फ़ाइल = सेटिंग_पथ / 'access.json'
            def लिखना_सेटिंग(आँकड़े):
                सेटिंग_फ़ाइल.write_text(json.dumps(आँकड़े, ensure_ascii=False) + '\n')
                सेटिंग_फ़ाइल.chmod(0o600)
            def सत्यापित_करें_सेटिंग(शेल, 화면):
                लिखना_सेटिंग({'user': 'user', 'ssh_password': शेल, 'vnc_password': 화면})
                원본 = सेटिंग_फ़ाइल.read_bytes()
                준비(시험터)
                assert सेटिंग_फ़ाइल.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (सेटिंग_पथ / 'प्रोफ़ाइल.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (सेटिंग_पथ / 'प्रोफ़ाइल.h').stat().st_mode & 0o777 == 0o600
            for शेल, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                सत्यापित_करें_सेटिंग(शेल, 화면)
            रिपोर्ट_मान['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for परिवर्तित_करें_मान, एन्ट्री_मान in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                आँकड़े = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                आँकड़े.update(परिवर्तित_करें_मान)
                लिखना_सेटिंग(आँकड़े)
                try:
                    준비(시험터)
                except SystemExit as त्रुटि:
                    assert एन्ट्री_मान in str(त्रुटि), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + एन्ट्री_मान)
            रिपोर्ट_मान['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            विन्यास = json.loads((प्रोजेक्ट_करें_मूल / 'build/remote/libassh-build.json').read_text())['flags']
            कंपाइलर_उपकरण = os.environ.get('ARM64_CC', 'clang')
            कनेक्टर = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            संग्रह_उपकरण = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def निष्पादित_करें_आदेश(तर्क, लॉग_रिकॉर्ड):
                subprocess.run(list(map(str, तर्क)), cwd=str(प्रोजेक्ट_करें_मूल), stdout=लॉग_रिकॉर्ड,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for नाम, शेल, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + नाम, flush=True)
                सत्यापित_करें_सेटिंग(शेल, 화면)
                परिणाम = निर्गम / नाम
                परिणाम.mkdir(exist_ok=True)
                with (परिणाम / 'build.log').open('wb') as लॉग_रिकॉर्ड:
                    목적들 = []
                    for 원본 in sorted((प्रोजेक्ट_करें_मूल / 'दूरस्थ_मान').glob('*.c')):
                        गंतव्य_मान = 시험터 / (원본.stem + '.o')
                        निष्पादित_करें_आदेश([कंपाइलर_उपकरण] + विन्यास + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', सेटिंग_पथ, '-I', प्रोजेक्ट_करें_मूल / 'दूरस्थ_मान', '-I', प्रोजेक्ट_करें_मूल / 'vendor/libassh/src',
                             '-I', प्रोजेक्ट_करें_मूल / 'vendor/bearssl/inc', '-I', प्रोजेक्ट_करें_मूल / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', गंतव्य_मान], लॉग_रिकॉर्ड)
                        목적들.append(गंतव्य_मान)
                    दूरस्थ_बंडल = 시험터 / 'libremote.a'
                    निष्पादित_करें_आदेश([संग्रह_उपकरण, 'rcs', दूरस्थ_बंडल] + 목적들, लॉग_रिकॉर्ड)
                    निष्पादित_करें_आदेश([कनेक्टर, '--gc-sections', '-T', प्रोजेक्ट_करें_मूल / '부팅/लिंक_लेआउट.ld', '-o', 시험터 / 'kernel.elf'] +
                         [प्रोजेक्ट_करें_मूल / 'build' / (नाम + '.o') for नाम in गंतव्य_नाम] + ['--start-group'] +
                         [दूरस्थ_बंडल if पथ == 'remote/libremote.a' else प्रोजेक्ट_करें_मूल / 'build' / पथ for पथ in लाइब्रेरी] + ['--end-group'], लॉग_रिकॉर्ड)
                    निष्पादित_करें_आदेश([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], लॉग_रिकॉर्ड)
                with (परिणाम / 'remote-test.log').open('wb') as लॉग_रिकॉर्ड:
                    निष्पादित_करें_आदेश(['python3', प्रोजेक्ट_करें_मूल / 'उपकरण/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', सेटिंग_फ़ाइल, '--output', परिणाम], लॉग_रिकॉर्ड)
                मान्य_करें = json.loads((परिणाम / 'report.json').read_text())
                assert मान्य_करें['passed']
                रिपोर्ट_मान['checks'].append(नाम + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        रिपोर्ट_मान['passed'] = True
    finally:
        रिपोर्ट_मान['personal_settings_unchanged'] = निजी_सेटिंग.read_bytes() == 원래설정
        if not रिपोर्ट_मान['personal_settings_unchanged']:
            रिपोर्ट_मान['passed'] = False
        रिपोर्ट_मान['kernel_sha256'] = hashlib.sha256((प्रोजेक्ट_करें_मूल / 'build/kernel8.img').read_bytes()).hexdigest()
        (निर्गम / 'report.json').write_text(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2) + '\n')
    assert रिपोर्ट_मान['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    चलाएँ()
