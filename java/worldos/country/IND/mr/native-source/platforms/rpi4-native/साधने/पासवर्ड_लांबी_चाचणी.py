#!/usr/bin/env python3
"""개인 कनेक्शन_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from दूरस्_थ_सेटिंग्ज import तयार_करणे
from सीओएसएल_वितरण import गंतव्यस्थान_नाव, लायब्ररी

प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]


def सुरू_करा():
    आउटपुट = प्रोजेक्ट_मूळ / 'build/verification/password-length'
    आउटपुट.mkdir(parents=True, exist_ok=True)
    व्यक्तिगत_सेटिंग्ज = प्रोजेक्ट_मूळ / 'build/remote/access.json'
    मूळ_सेटिंग्ज = व्यक्तिगत_सेटिंग्ज.read_bytes()
    अहवाल_मूल्य = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as तात्पुरते_मूल्य:
            वर्कस्पेस_चाचणी = Path(तात्पुरते_मूल्य)
            सेटिंग्ज_पथ = वर्कस्पेस_चाचणी / 'build/remote'
            सेटिंग्ज_पथ.mkdir(parents=True)
            सेटिंग्ज_संचिका = सेटिंग्ज_पथ / 'access.json'
            def सेटिंग्ज_लिहा(डेटा):
                सेटिंग्ज_संचिका.write_text(json.dumps(डेटा, ensure_ascii=False) + '\n')
                सेटिंग्ज_संचिका.chmod(0o600)
            def सेटिंग्ज_पडताळा(शेल, पडदा):
                सेटिंग्ज_लिहा({'user': 'user', 'ssh_password': शेल, 'vnc_password': पडदा})
                मूळ = सेटिंग्ज_संचिका.read_bytes()
                तयार_करणे(वर्कस्पेस_चाचणी)
                assert सेटिंग्ज_संचिका.read_bytes() == मूळ, 'Settings were rewritten'
                शीर्ष_मूल्य = (सेटिंग्ज_पथ / 'प्रोफाइल.h').read_text()
                आहे_समान = re.search(r'पडदा_पासवर्ड\[\] = \{([^}]+)\}', शीर्ष_मूल्य)
                assert आहे_समान and len(आहे_समान.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (सेटिंग्ज_पथ / 'प्रोफाइल.h').stat().st_mode & 0o777 == 0o600
            for शेल, पडदा in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                सेटिंग्ज_पडताळा(शेल, पडदा)
            अहवाल_मूल्य['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for बदल_करा_मूल्य, प्रविष्टी_मूल्य in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                डेटा = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                डेटा.update(बदल_करा_मूल्य)
                सेटिंग्ज_लिहा(डेटा)
                try:
                    तयार_करणे(वर्कस्पेस_चाचणी)
                except SystemExit as त्रुटी:
                    assert प्रविष्टी_मूल्य in str(त्रुटी), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + प्रविष्टी_मूल्य)
            अहवाल_मूल्य['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            संयोजना = json.loads((प्रोजेक्ट_मूळ / 'build/remote/libassh-build.json').read_text())['flags']
            संकलक_साधन = os.environ.get('ARM64_CC', 'clang')
            कनेक्टर = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            संग्रह_साधन = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def आज्ञा_कार्यवाही_करा(बाबी, लॉग_नोंद):
                subprocess.run(list(map(str, बाबी)), cwd=str(प्रोजेक्ट_मूळ), stdout=लॉग_नोंद,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for नाव, शेल, पडदा in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + नाव, flush=True)
                सेटिंग्ज_पडताळा(शेल, पडदा)
                मोजमाप = आउटपुट / नाव
                मोजमाप.mkdir(exist_ok=True)
                with (मोजमाप / 'build.log').open('wb') as लॉग_नोंद:
                    गंतव्ये = []
                    for मूळ in sorted((प्रोजेक्ट_मूळ / 'दूरस्_थ_मूल्य').glob('*.c')):
                        गंतव्यस्थान_मूल्य = वर्कस्पेस_चाचणी / (मूळ.stem + '.o')
                        आज्ञा_कार्यवाही_करा([संकलक_साधन] + संयोजना + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', सेटिंग्ज_पथ, '-I', प्रोजेक्ट_मूळ / 'दूरस्_थ_मूल्य', '-I', प्रोजेक्ट_मूळ / 'vendor/libassh/src',
                             '-I', प्रोजेक्ट_मूळ / 'vendor/bearssl/inc', '-I', प्रोजेक्ट_मूळ / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', मूळ, '-o', गंतव्यस्थान_मूल्य], लॉग_नोंद)
                        गंतव्ये.append(गंतव्यस्थान_मूल्य)
                    दूरस्_थ_बंडल = वर्कस्पेस_चाचणी / 'libremote.a'
                    आज्ञा_कार्यवाही_करा([संग्रह_साधन, 'rcs', दूरस्_थ_बंडल] + गंतव्ये, लॉग_नोंद)
                    आज्ञा_कार्यवाही_करा([कनेक्टर, '--gc-sections', '-T', प्रोजेक्ट_मूळ / 'प्रणालीप्रारंभ/लिंक_लेआउट.ld', '-o', वर्कस्पेस_चाचणी / 'kernel.elf'] +
                         [प्रोजेक्ट_मूळ / 'build' / (नाव + '.o') for नाव in गंतव्यस्थान_नाव] + ['--start-group'] +
                         [दूरस्_थ_बंडल if मार्ग == 'remote/libremote.a' else प्रोजेक्ट_मूळ / 'build' / मार्ग for मार्ग in लायब्ररी] + ['--end-group'], लॉग_नोंद)
                    आज्ञा_कार्यवाही_करा([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         वर्कस्पेस_चाचणी / 'kernel.elf', वर्कस्पेस_चाचणी / 'kernel8.img'], लॉग_नोंद)
                with (मोजमाप / 'remote-test.log').open('wb') as लॉग_नोंद:
                    आज्ञा_कार्यवाही_करा(['python3', प्रोजेक्ट_मूळ / 'साधने/दूरस्_थ_कनेक्शन_चाचणी.py', '--kernel', वर्कस्पेस_चाचणी / 'kernel8.img',
                         '--access', सेटिंग्ज_संचिका, '--output', मोजमाप], लॉग_नोंद)
                प्रमाणित = json.loads((मोजमाप / 'report.json').read_text())
                assert प्रमाणित['passed']
                अहवाल_मूल्य['checks'].append(नाव + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        अहवाल_मूल्य['passed'] = True
    finally:
        अहवाल_मूल्य['personal_settings_unchanged'] = व्यक्तिगत_सेटिंग्ज.read_bytes() == मूळ_सेटिंग्ज
        if not अहवाल_मूल्य['personal_settings_unchanged']:
            अहवाल_मूल्य['passed'] = False
        अहवाल_मूल्य['kernel_sha256'] = hashlib.sha256((प्रोजेक्ट_मूळ / 'build/kernel8.img').read_bytes()).hexdigest()
        (आउटपुट / 'report.json').write_text(json.dumps(अहवाल_मूल्य, ensure_ascii=False, indent=2) + '\n')
    assert अहवाल_मूल्य['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(अहवाल_मूल्य, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    सुरू_करा()
