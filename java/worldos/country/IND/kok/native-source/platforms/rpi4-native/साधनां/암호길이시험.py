#!/usr/bin/env python3
"""개인 कनॅक्शन_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from दुर्मीळ_मांडावळी import तयार_करचें_9ce364fc
from COSL배포 import नियुक्त_स्थान_नांव, लायब्ररी

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]


def चलोवप():
    출력 = प्रॉजॅक्ट_रूट / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    व्याक्तिगत_मांडावळी = प्रॉजॅक्ट_रूट / 'build/remote/access.json'
    원래설정 = व्याक्तिगत_मांडावळी.read_bytes()
    अहवाल_मोल = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            मांडावळी_पाथ = 시험터 / 'build/remote'
            मांडावळी_पाथ.mkdir(parents=True)
            मांडावळी_फायल = मांडावळी_पाथ / 'access.json'
            def बरोवचें_मांडावळी(डेटा):
                मांडावळी_फायल.write_text(json.dumps(डेटा, ensure_ascii=False) + '\n')
                मांडावळी_फायल.chmod(0o600)
            def पुनर्तपासणी_करची_मांडावळी(शॅल, 화면):
                बरोवचें_मांडावळी({'user': 'user', 'ssh_password': शॅल, 'vnc_password': 화면})
                원본 = मांडावळी_फायल.read_bytes()
                तयार_करचें_9ce364fc(시험터)
                assert मांडावळी_फायल.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (मांडावळी_पाथ / 'प्रोफायल.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (मांडावळी_पाथ / 'प्रोफायल.h').stat().st_mode & 0o777 == 0o600
            for शॅल, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                पुनर्तपासणी_करची_मांडावळी(शॅल, 화면)
            अहवाल_मोल['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for बदलचें_मोल, प्रवेश_मोल in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                डेटा = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                डेटा.update(बदलचें_मोल)
                बरोवचें_मांडावळी(डेटा)
                try:
                    तयार_करचें_9ce364fc(시험터)
                except SystemExit as चूक:
                    assert प्रवेश_मोल in str(चूक), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + प्रवेश_मोल)
            अहवाल_मोल['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            मांडावळी = json.loads((प्रॉजॅक्ट_रूट / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            कनॅक्टर = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            संग्रह_साधन = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def पाळो_दिवचो_आदेश(인수, LOG_नोंद):
                subprocess.run(list(map(str, 인수)), cwd=str(प्रॉजॅक्ट_रूट), stdout=LOG_नोंद,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for नांव, शॅल, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + नांव, flush=True)
                पुनर्तपासणी_करची_मांडावळी(शॅल, 화면)
                मेजप = 출력 / नांव
                मेजप.mkdir(exist_ok=True)
                with (मेजप / 'build.log').open('wb') as LOG_नोंद:
                    목적들 = []
                    for 원본 in sorted((प्रॉजॅक्ट_रूट / 'दुर्मीळ_मोल').glob('*.c')):
                        नियुक्त_स्थान_मोल = 시험터 / (원본.stem + '.o')
                        पाळो_दिवचो_आदेश([번역기] + मांडावळी + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', मांडावळी_पाथ, '-I', प्रॉजॅक्ट_रूट / 'दुर्मीळ_मोल', '-I', प्रॉजॅक्ट_रूट / 'vendor/libassh/src',
                             '-I', प्रॉजॅक्ट_रूट / 'vendor/bearssl/inc', '-I', प्रॉजॅक्ट_रूट / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', नियुक्त_स्थान_मोल], LOG_नोंद)
                        목적들.append(नियुक्त_स्थान_मोल)
                    दुर्मीळ_रास = 시험터 / 'libremote.a'
                    पाळो_दिवचो_आदेश([संग्रह_साधन, 'rcs', दुर्मीळ_रास] + 목적들, LOG_नोंद)
                    पाळो_दिवचो_आदेश([कनॅक्टर, '--gc-sections', '-T', प्रॉजॅक्ट_रूट / '부팅/लिंक_रचणाय.ld', '-o', 시험터 / 'kernel.elf'] +
                         [प्रॉजॅक्ट_रूट / 'build' / (नांव + '.o') for नांव in नियुक्त_स्थान_नांव] + ['--start-group'] +
                         [दुर्मीळ_रास if पाथ == 'remote/libremote.a' else प्रॉजॅक्ट_रूट / 'build' / पाथ for पाथ in लायब्ररी] + ['--end-group'], LOG_नोंद)
                    पाळो_दिवचो_आदेश([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_नोंद)
                with (मेजप / 'remote-test.log').open('wb') as LOG_नोंद:
                    पाळो_दिवचो_आदेश(['python3', प्रॉजॅक्ट_रूट / 'साधनां/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', मांडावळी_फायल, '--output', मेजप], LOG_नोंद)
                पुनर्तपासणी_करची_5fb2b747 = json.loads((मेजप / 'report.json').read_text())
                assert पुनर्तपासणी_करची_5fb2b747['passed']
                अहवाल_मोल['checks'].append(नांव + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        अहवाल_मोल['passed'] = True
    finally:
        अहवाल_मोल['personal_settings_unchanged'] = व्याक्तिगत_मांडावळी.read_bytes() == 원래설정
        if not अहवाल_मोल['personal_settings_unchanged']:
            अहवाल_मोल['passed'] = False
        अहवाल_मोल['kernel_sha256'] = hashlib.sha256((प्रॉजॅक्ट_रूट / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(अहवाल_मोल, ensure_ascii=False, indent=2) + '\n')
    assert अहवाल_मोल['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(अहवाल_मोल, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    चलोवप()
