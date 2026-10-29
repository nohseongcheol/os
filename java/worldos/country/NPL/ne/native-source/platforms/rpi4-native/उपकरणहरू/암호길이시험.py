#!/usr/bin/env python3
"""개인 जडान_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from दूर_सेटिङहरू import तयार_गर्नुहोस्
from COSL배포 import गन्तव्य_नाम, पुस्तकालय

परियोजना_रूट = Path(__file__).resolve().parents[1]


def चलाउनुहोस्():
    출력 = परियोजना_रूट / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    व्यक्तिगत_सेटिङ = परियोजना_रूट / 'build/remote/access.json'
    원래설정 = व्यक्तिगत_सेटिङ.read_bytes()
    रिपोर्ट_मान = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            सेटिङहरू_बाटो = 시험터 / 'build/remote'
            सेटिङहरू_बाटो.mkdir(parents=True)
            सेटिङहरू_फाइल = सेटिङहरू_बाटो / 'access.json'
            def लेख्नुहोस्_सेटिङहरू(लगत):
                सेटिङहरू_फाइल.write_text(json.dumps(लगत, ensure_ascii=False) + '\n')
                सेटिङहरू_फाइल.chmod(0o600)
            def रुजू_गर्नुहोस्_सेटिङहरू(शेल, 화면):
                लेख्नुहोस्_सेटिङहरू({'user': 'user', 'ssh_password': शेल, 'vnc_password': 화면})
                원본 = सेटिङहरू_फाइल.read_bytes()
                तयार_गर्नुहोस्(시험터)
                assert सेटिङहरू_फाइल.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (सेटिङहरू_बाटो / 'प्रोफाइल.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (सेटिङहरू_बाटो / 'प्रोफाइल.h').stat().st_mode & 0o777 == 0o600
            for शेल, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                रुजू_गर्नुहोस्_सेटिङहरू(शेल, 화면)
            रिपोर्ट_मान['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for परिवर्तन_मान, प्रविष्टि_मान in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                लगत = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                लगत.update(परिवर्तन_मान)
                लेख्नुहोस्_सेटिङहरू(लगत)
                try:
                    तयार_गर्नुहोस्(시험터)
                except SystemExit as त्रुटि:
                    assert प्रविष्टि_मान in str(त्रुटि), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + प्रविष्टि_मान)
            रिपोर्ट_मान['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            सेटिङ = json.loads((परियोजना_रूट / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            योजक = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            सङ्ग्रह_उपकरण = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def कार्यान्वयन_गर्नुहोस्_आदेश(तर्क, लग_रेकर्ड):
                subprocess.run(list(map(str, तर्क)), cwd=str(परियोजना_रूट), stdout=लग_रेकर्ड,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for नाम, शेल, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + नाम, flush=True)
                रुजू_गर्नुहोस्_सेटिङहरू(शेल, 화면)
                मापन = 출력 / नाम
                मापन.mkdir(exist_ok=True)
                with (मापन / 'build.log').open('wb') as लग_रेकर्ड:
                    목적들 = []
                    for 원본 in sorted((परियोजना_रूट / 'दूर_मान').glob('*.c')):
                        गन्तव्य_मान = 시험터 / (원본.stem + '.o')
                        कार्यान्वयन_गर्नुहोस्_आदेश([번역기] + सेटिङ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', सेटिङहरू_बाटो, '-I', परियोजना_रूट / 'दूर_मान', '-I', परियोजना_रूट / 'vendor/libassh/src',
                             '-I', परियोजना_रूट / 'vendor/bearssl/inc', '-I', परियोजना_रूट / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', गन्तव्य_मान], लग_रेकर्ड)
                        목적들.append(गन्तव्य_मान)
                    दूर_पोको = 시험터 / 'libremote.a'
                    कार्यान्वयन_गर्नुहोस्_आदेश([सङ्ग्रह_उपकरण, 'rcs', दूर_पोको] + 목적들, लग_रेकर्ड)
                    कार्यान्वयन_गर्नुहोस्_आदेश([योजक, '--gc-sections', '-T', परियोजना_रूट / '부팅/लिङ्क_लेआउट.ld', '-o', 시험터 / 'kernel.elf'] +
                         [परियोजना_रूट / 'build' / (नाम + '.o') for नाम in गन्तव्य_नाम] + ['--start-group'] +
                         [दूर_पोको if मार्ग == 'remote/libremote.a' else परियोजना_रूट / 'build' / मार्ग for मार्ग in पुस्तकालय] + ['--end-group'], लग_रेकर्ड)
                    कार्यान्वयन_गर्नुहोस्_आदेश([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], लग_रेकर्ड)
                with (मापन / 'remote-test.log').open('wb') as लग_रेकर्ड:
                    कार्यान्वयन_गर्नुहोस्_आदेश(['python3', परियोजना_रूट / 'उपकरणहरू/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', सेटिङहरू_फाइल, '--output', मापन], लग_रेकर्ड)
                वैध_गर्नुहोस् = json.loads((मापन / 'report.json').read_text())
                assert वैध_गर्नुहोस्['passed']
                रिपोर्ट_मान['checks'].append(नाम + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        रिपोर्ट_मान['passed'] = True
    finally:
        रिपोर्ट_मान['personal_settings_unchanged'] = व्यक्तिगत_सेटिङ.read_bytes() == 원래설정
        if not रिपोर्ट_मान['personal_settings_unchanged']:
            रिपोर्ट_मान['passed'] = False
        रिपोर्ट_मान['kernel_sha256'] = hashlib.sha256((परियोजना_रूट / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2) + '\n')
    assert रिपोर्ट_मान['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    चलाउनुहोस्()
