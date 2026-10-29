#!/usr/bin/env python3
"""개인 ការភ្ជាប់_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from ពីចម្ងាយ_ការកំណត់ import រៀបចំ
from COSL배포 import ទិសដៅ_ឈ្មោះ, បណ្ណាល័យ

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]


def រត់():
    លទ្ធផល = បញ្ចាំង_ឬស / 'build/verification/password-length'
    លទ្ធផល.mkdir(parents=True, exist_ok=True)
    ការកំណត់ផ្ទាល់ខ្លួន = បញ្ចាំង_ឬស / 'build/remote/access.json'
    원래설정 = ការកំណត់ផ្ទាល់ខ្លួន.read_bytes()
    រាយការណ៍_តំលៃ = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            ការកំណត់_ផ្លូវ = 시험터 / 'build/remote'
            ការកំណត់_ផ្លូវ.mkdir(parents=True)
            ការកំណត់_ឯកសារ = ការកំណត់_ផ្លូវ / 'access.json'
            def សរសេរ_ការកំណត់(ទិន្នន័យ):
                ការកំណត់_ឯកសារ.write_text(json.dumps(ទិន្នន័យ, ensure_ascii=False) + '\n')
                ការកំណត់_ឯកសារ.chmod(0o600)
            def ផ្ទៀងផ្ទាត់_ការកំណត់(셸, 화면):
                សរសេរ_ការកំណត់({'user': 'user', 'ssh_password': 셸, 'vnc_password': 화면})
                원본 = ការកំណត់_ឯកសារ.read_bytes()
                រៀបចំ(시험터)
                assert ការកំណត់_ឯកសារ.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (ការកំណត់_ផ្លូវ / 'ទម្រង់.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (ការកំណត់_ផ្លូវ / 'ទម្រង់.h').stat().st_mode & 0o777 == 0o600
            for 셸, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ផ្ទៀងផ្ទាត់_ការកំណត់(셸, 화면)
            រាយការណ៍_តំលៃ['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for កែប្រែ_តំលៃ, ការបញ្ចូល_តំលៃ in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ទិន្នន័យ = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ទិន្នន័យ.update(កែប្រែ_តំលៃ)
                សរសេរ_ការកំណត់(ទិន្នន័យ)
                try:
                    រៀបចំ(시험터)
                except SystemExit as កំហុស:
                    assert ការបញ្ចូល_តំលៃ in str(កំហុស), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ការបញ្ចូល_តំលៃ)
            រាយការណ៍_តំលៃ['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ការកំណត់ = json.loads((បញ្ចាំង_ឬស / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            អង្គភ្ជាប់ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ប័ណ្ណសារ_ឧបករណ៏ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def អនុវត្ត_ពាក្យបញ្ជា(អាគុយម៉ង់, កំណត់_ហេតុ_ថត):
                subprocess.run(list(map(str, អាគុយម៉ង់)), cwd=str(បញ្ចាំង_ឬស), stdout=កំណត់_ហេតុ_ថត,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ឈ្មោះ, 셸, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ឈ្មោះ, flush=True)
                ផ្ទៀងផ្ទាត់_ការកំណត់(셸, 화면)
                ការវាស់វែង = លទ្ធផល / ឈ្មោះ
                ការវាស់វែង.mkdir(exist_ok=True)
                with (ការវាស់វែង / 'build.log').open('wb') as កំណត់_ហេតុ_ថត:
                    목적들 = []
                    for 원본 in sorted((បញ្ចាំង_ឬស / 'ពីចម្ងាយ_តំលៃ').glob('*.c')):
                        ទិសដៅ_តំលៃ = 시험터 / (원본.stem + '.o')
                        អនុវត្ត_ពាក្យបញ្ជា([번역기] + ការកំណត់ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', ការកំណត់_ផ្លូវ, '-I', បញ្ចាំង_ឬស / 'ពីចម្ងាយ_តំលៃ', '-I', បញ្ចាំង_ឬស / 'vendor/libassh/src',
                             '-I', បញ្ចាំង_ឬស / 'vendor/bearssl/inc', '-I', បញ្ចាំង_ឬស / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ទិសដៅ_តំលៃ], កំណត់_ហេតុ_ថត)
                        목적들.append(ទិសដៅ_តំលៃ)
                    ពីចម្ងាយ_បាច់ = 시험터 / 'libremote.a'
                    អនុវត្ត_ពាក្យបញ្ជា([ប័ណ្ណសារ_ឧបករណ៏, 'rcs', ពីចម្ងាយ_បាច់] + 목적들, កំណត់_ហេតុ_ថត)
                    អនុវត្ត_ពាក្យបញ្ជា([អង្គភ្ជាប់, '--gc-sections', '-T', បញ្ចាំង_ឬស / '부팅/តំណ_ប្លង់.ld', '-o', 시험터 / 'kernel.elf'] +
                         [បញ្ចាំង_ឬស / 'build' / (ឈ្មោះ + '.o') for ឈ្មោះ in ទិសដៅ_ឈ្មោះ] + ['--start-group'] +
                         [ពីចម្ងាយ_បាច់ if ផ្លូវ == 'remote/libremote.a' else បញ្ចាំង_ឬស / 'build' / ផ្លូវ for ផ្លូវ in បណ្ណាល័យ] + ['--end-group'], កំណត់_ហេតុ_ថត)
                    អនុវត្ត_ពាក្យបញ្ជា([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], កំណត់_ហេតុ_ថត)
                with (ការវាស់វែង / 'remote-test.log').open('wb') as កំណត់_ហេតុ_ថត:
                    អនុវត្ត_ពាក្យបញ្ជា(['python3', បញ្ចាំង_ឬស / 'ឧបករណ៍/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', ការកំណត់_ឯកសារ, '--output', ការវាស់វែង], កំណត់_ហេតុ_ថត)
                ធ្វើអោយមានសុពលភាព = json.loads((ការវាស់វែង / 'report.json').read_text())
                assert ធ្វើអោយមានសុពលភាព['passed']
                រាយការណ៍_តំលៃ['checks'].append(ឈ្មោះ + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        រាយការណ៍_តំលៃ['passed'] = True
    finally:
        រាយការណ៍_តំលៃ['personal_settings_unchanged'] = ការកំណត់ផ្ទាល់ខ្លួន.read_bytes() == 원래설정
        if not រាយការណ៍_តំលៃ['personal_settings_unchanged']:
            រាយការណ៍_តំលៃ['passed'] = False
        រាយការណ៍_តំលៃ['kernel_sha256'] = hashlib.sha256((បញ្ចាំង_ឬស / 'build/kernel8.img').read_bytes()).hexdigest()
        (លទ្ធផល / 'report.json').write_text(json.dumps(រាយការណ៍_តំលៃ, ensure_ascii=False, indent=2) + '\n')
    assert រាយការណ៍_តំលៃ['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(រាយការណ៍_តំលៃ, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    រត់()
