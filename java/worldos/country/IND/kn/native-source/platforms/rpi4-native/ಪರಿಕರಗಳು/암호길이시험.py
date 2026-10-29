#!/usr/bin/env python3
"""개인 ಸಂಪರ್ಕ_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from ರಿಮೋಟ್_ಸೆಟ್ಟಿಂಗ್ಸ್ import ಸಿದ್ಧಪಡಿಸು
from COSL배포 import ಗಮ್ಯಸ್ಥಾನ_ಹೆಸರು, ಲೈಬ್ರರಿ

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]


def ಚಲಾಯಿಸು_2():
    ಔಟ್_ಪುಟ್ = ಬಿಂಬಿಸು_ಮೂಲ / 'build/verification/password-length'
    ಔಟ್_ಪುಟ್.mkdir(parents=True, exist_ok=True)
    ವೈಯಕ್ತಿಕ_ಸೆಟ್ಟಿಂಗ್_ಗಳು = ಬಿಂಬಿಸು_ಮೂಲ / 'build/remote/access.json'
    원래설정 = ವೈಯಕ್ತಿಕ_ಸೆಟ್ಟಿಂಗ್_ಗಳು.read_bytes()
    ವರದಿ_ಮೌಲ್ಯ = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            ಸೆಟ್ಟಿಂಗ್ಸ್_ಹಾದಿ = 시험터 / 'build/remote'
            ಸೆಟ್ಟಿಂಗ್ಸ್_ಹಾದಿ.mkdir(parents=True)
            ಸೆಟ್ಟಿಂಗ್ಸ್_ಫೈಲ್ = ಸೆಟ್ಟಿಂಗ್ಸ್_ಹಾದಿ / 'access.json'
            def ಬರೆ_ಸೆಟ್ಟಿಂಗ್ಸ್(ಡೇಟಾ):
                ಸೆಟ್ಟಿಂಗ್ಸ್_ಫೈಲ್.write_text(json.dumps(ಡೇಟಾ, ensure_ascii=False) + '\n')
                ಸೆಟ್ಟಿಂಗ್ಸ್_ಫೈಲ್.chmod(0o600)
            def ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಸೆಟ್ಟಿಂಗ್ಸ್(ಶೆಲ್, 화면):
                ಬರೆ_ಸೆಟ್ಟಿಂಗ್ಸ್({'user': 'user', 'ssh_password': ಶೆಲ್, 'vnc_password': 화면})
                원본 = ಸೆಟ್ಟಿಂಗ್ಸ್_ಫೈಲ್.read_bytes()
                ಸಿದ್ಧಪಡಿಸು(시험터)
                assert ಸೆಟ್ಟಿಂಗ್ಸ್_ಫೈಲ್.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (ಸೆಟ್ಟಿಂಗ್ಸ್_ಹಾದಿ / 'ಪ್ರೊಫೈಲ್.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (ಸೆಟ್ಟಿಂಗ್ಸ್_ಹಾದಿ / 'ಪ್ರೊಫೈಲ್.h').stat().st_mode & 0o777 == 0o600
            for ಶೆಲ್, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಸೆಟ್ಟಿಂಗ್ಸ್(ಶೆಲ್, 화면)
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ಬದಲಿಸು_ಮೌಲ್ಯ, ನಮೂದು_ಮೌಲ್ಯ in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ಡೇಟಾ = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ಡೇಟಾ.update(ಬದಲಿಸು_ಮೌಲ್ಯ)
                ಬರೆ_ಸೆಟ್ಟಿಂಗ್ಸ್(ಡೇಟಾ)
                try:
                    ಸಿದ್ಧಪಡಿಸು(시험터)
                except SystemExit as ದೋಷ:
                    assert ನಮೂದು_ಮೌಲ್ಯ in str(ದೋಷ), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ನಮೂದು_ಮೌಲ್ಯ)
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ಸಿದ್ಧತೆಗಳು = json.loads((ಬಿಂಬಿಸು_ಮೂಲ / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            ಜೋಡಿಸುವವ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ಅರ್ಖೀವ್_ಪರಿಕರ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ಪೂರೈಸು_ಆದೇಶ(인수, ಲಾಗ್_ದಾಖಲೆ):
                subprocess.run(list(map(str, 인수)), cwd=str(ಬಿಂಬಿಸು_ಮೂಲ), stdout=ಲಾಗ್_ದಾಖಲೆ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ಹೆಸರು, ಶೆಲ್, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ಹೆಸರು, flush=True)
                ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಸೆಟ್ಟಿಂಗ್ಸ್(ಶೆಲ್, 화면)
                ಮಾಪನ = ಔಟ್_ಪುಟ್ / ಹೆಸರು
                ಮಾಪನ.mkdir(exist_ok=True)
                with (ಮಾಪನ / 'build.log').open('wb') as ಲಾಗ್_ದಾಖಲೆ:
                    목적들 = []
                    for 원본 in sorted((ಬಿಂಬಿಸು_ಮೂಲ / 'ರಿಮೋಟ್_ಮೌಲ್ಯ').glob('*.c')):
                        ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = 시험터 / (원본.stem + '.o')
                        ಪೂರೈಸು_ಆದೇಶ([번역기] + ಸಿದ್ಧತೆಗಳು + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', ಸೆಟ್ಟಿಂಗ್ಸ್_ಹಾದಿ, '-I', ಬಿಂಬಿಸು_ಮೂಲ / 'ರಿಮೋಟ್_ಮೌಲ್ಯ', '-I', ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/libassh/src',
                             '-I', ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/bearssl/inc', '-I', ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ], ಲಾಗ್_ದಾಖಲೆ)
                        목적들.append(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ)
                    ರಿಮೋಟ್_ಬಂಡಲ್ = 시험터 / 'libremote.a'
                    ಪೂರೈಸು_ಆದೇಶ([ಅರ್ಖೀವ್_ಪರಿಕರ, 'rcs', ರಿಮೋಟ್_ಬಂಡಲ್] + 목적들, ಲಾಗ್_ದಾಖಲೆ)
                    ಪೂರೈಸು_ಆದೇಶ([ಜೋಡಿಸುವವ, '--gc-sections', '-T', ಬಿಂಬಿಸು_ಮೂಲ / '부팅/ಜೋಡಣೆ_ಲೇಔಟ್.ld', '-o', 시험터 / 'kernel.elf'] +
                         [ಬಿಂಬಿಸು_ಮೂಲ / 'build' / (ಹೆಸರು + '.o') for ಹೆಸರು in ಗಮ್ಯಸ್ಥಾನ_ಹೆಸರು] + ['--start-group'] +
                         [ರಿಮೋಟ್_ಬಂಡಲ್ if ಮಾರ್ಗ == 'remote/libremote.a' else ಬಿಂಬಿಸು_ಮೂಲ / 'build' / ಮಾರ್ಗ for ಮಾರ್ಗ in ಲೈಬ್ರರಿ] + ['--end-group'], ಲಾಗ್_ದಾಖಲೆ)
                    ಪೂರೈಸು_ಆದೇಶ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], ಲಾಗ್_ದಾಖಲೆ)
                with (ಮಾಪನ / 'remote-test.log').open('wb') as ಲಾಗ್_ದಾಖಲೆ:
                    ಪೂರೈಸು_ಆದೇಶ(['python3', ಬಿಂಬಿಸು_ಮೂಲ / 'ಪರಿಕರಗಳು/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', ಸೆಟ್ಟಿಂಗ್ಸ್_ಫೈಲ್, '--output', ಮಾಪನ], ಲಾಗ್_ದಾಖಲೆ)
                ಸಕ್ರಮೀಕರಿಸು = json.loads((ಮಾಪನ / 'report.json').read_text())
                assert ಸಕ್ರಮೀಕರಿಸು['passed']
                ವರದಿ_ಮೌಲ್ಯ['checks'].append(ಹೆಸರು + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ವರದಿ_ಮೌಲ್ಯ['passed'] = True
    finally:
        ವರದಿ_ಮೌಲ್ಯ['personal_settings_unchanged'] = ವೈಯಕ್ತಿಕ_ಸೆಟ್ಟಿಂಗ್_ಗಳು.read_bytes() == 원래설정
        if not ವರದಿ_ಮೌಲ್ಯ['personal_settings_unchanged']:
            ವರದಿ_ಮೌಲ್ಯ['passed'] = False
        ವರದಿ_ಮೌಲ್ಯ['kernel_sha256'] = hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img').read_bytes()).hexdigest()
        (ಔಟ್_ಪುಟ್ / 'report.json').write_text(json.dumps(ವರದಿ_ಮೌಲ್ಯ, ensure_ascii=False, indent=2) + '\n')
    assert ವರದಿ_ಮೌಲ್ಯ['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ವರದಿ_ಮೌಲ್ಯ, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
