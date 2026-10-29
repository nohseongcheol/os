#!/usr/bin/env python3
"""개인 ਸਬੰਧ_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from ਰਿਮੋਟ_ਸੈਟਿੰਗਾਂ import ਤਿਆਰ_ਕਰੋ
from COSL배포 import ਮੰਜਿਲ_ਨਾਮ, ਪੁਸਤਕਾਲਾ

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]


def ਚਲਾਓ_2():
    ਆਉਟਪੁੱਟ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/verification/password-length'
    ਆਉਟਪੁੱਟ.mkdir(parents=True, exist_ok=True)
    ਵਿਅਕਤੀਗਤ_ਸੈਟਿੰਗਜ਼ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/remote/access.json'
    원래설정 = ਵਿਅਕਤੀਗਤ_ਸੈਟਿੰਗਜ਼.read_bytes()
    ਵਿਵਰਨ_ਕੀਮਤ = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            ਸੈਟਿੰਗਾਂ_ਰਸਤਾ = 시험터 / 'build/remote'
            ਸੈਟਿੰਗਾਂ_ਰਸਤਾ.mkdir(parents=True)
            ਸੈਟਿੰਗਾਂ_ਲਿਖਤ_ਪੱਤਰ = ਸੈਟਿੰਗਾਂ_ਰਸਤਾ / 'access.json'
            def ਲਿੱਖੋ_ਸੈਟਿੰਗਾਂ(ਸਮੱਗਰੀ):
                ਸੈਟਿੰਗਾਂ_ਲਿਖਤ_ਪੱਤਰ.write_text(json.dumps(ਸਮੱਗਰੀ, ensure_ascii=False) + '\n')
                ਸੈਟਿੰਗਾਂ_ਲਿਖਤ_ਪੱਤਰ.chmod(0o600)
            def ਤਸਦੀਕ_ਸੈਟਿੰਗਾਂ(ਸ਼ੈਲ, 화면):
                ਲਿੱਖੋ_ਸੈਟਿੰਗਾਂ({'user': 'user', 'ssh_password': ਸ਼ੈਲ, 'vnc_password': 화면})
                원본 = ਸੈਟਿੰਗਾਂ_ਲਿਖਤ_ਪੱਤਰ.read_bytes()
                ਤਿਆਰ_ਕਰੋ(시험터)
                assert ਸੈਟਿੰਗਾਂ_ਲਿਖਤ_ਪੱਤਰ.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (ਸੈਟਿੰਗਾਂ_ਰਸਤਾ / 'ਪ੍ਰੋਫਾਈਲ.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (ਸੈਟਿੰਗਾਂ_ਰਸਤਾ / 'ਪ੍ਰੋਫਾਈਲ.h').stat().st_mode & 0o777 == 0o600
            for ਸ਼ੈਲ, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ਤਸਦੀਕ_ਸੈਟਿੰਗਾਂ(ਸ਼ੈਲ, 화면)
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ਬਦਲੋ_ਕੀਮਤ, ਦਾਖਲਾ_ਕੀਮਤ in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ਸਮੱਗਰੀ = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ਸਮੱਗਰੀ.update(ਬਦਲੋ_ਕੀਮਤ)
                ਲਿੱਖੋ_ਸੈਟਿੰਗਾਂ(ਸਮੱਗਰੀ)
                try:
                    ਤਿਆਰ_ਕਰੋ(시험터)
                except SystemExit as ਗਲਤੀ:
                    assert ਦਾਖਲਾ_ਕੀਮਤ in str(ਗਲਤੀ), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ਦਾਖਲਾ_ਕੀਮਤ)
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ਸੈਟਿੰਗ = json.loads((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            ਕਨੈਕਟਰ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ਸੰਗ੍ਰਹਿ_ਸਾਧਨ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਆਰਗੂਮੈਂਟ, ਲੌਗ_ਕਤਾਰ):
                subprocess.run(list(map(str, ਆਰਗੂਮੈਂਟ)), cwd=str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ), stdout=ਲੌਗ_ਕਤਾਰ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ਨਾਂ, ਸ਼ੈਲ, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ਨਾਂ, flush=True)
                ਤਸਦੀਕ_ਸੈਟਿੰਗਾਂ(ਸ਼ੈਲ, 화면)
                ਮਾਪ = ਆਉਟਪੁੱਟ / ਨਾਂ
                ਮਾਪ.mkdir(exist_ok=True)
                with (ਮਾਪ / 'build.log').open('wb') as ਲੌਗ_ਕਤਾਰ:
                    목적들 = []
                    for 원본 in sorted((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਰਿਮੋਟ_ਕੀਮਤ').glob('*.c')):
                        ਮੰਜਿਲ_ਕੀਮਤ = 시험터 / (원본.stem + '.o')
                        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([번역기] + ਸੈਟਿੰਗ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', ਸੈਟਿੰਗਾਂ_ਰਸਤਾ, '-I', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਰਿਮੋਟ_ਕੀਮਤ', '-I', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor/libassh/src',
                             '-I', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor/bearssl/inc', '-I', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ਮੰਜਿਲ_ਕੀਮਤ], ਲੌਗ_ਕਤਾਰ)
                        목적들.append(ਮੰਜਿਲ_ਕੀਮਤ)
                    ਰਿਮੋਟ_ਬੰਡਲ = 시험터 / 'libremote.a'
                    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([ਸੰਗ੍ਰਹਿ_ਸਾਧਨ, 'rcs', ਰਿਮੋਟ_ਬੰਡਲ] + 목적들, ਲੌਗ_ਕਤਾਰ)
                    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([ਕਨੈਕਟਰ, '--gc-sections', '-T', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '부팅/ਲਿੰਕ_ਖਾਕਾ.ld', '-o', 시험터 / 'kernel.elf'] +
                         [ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build' / (ਨਾਂ + '.o') for ਨਾਂ in ਮੰਜਿਲ_ਨਾਮ] + ['--start-group'] +
                         [ਰਿਮੋਟ_ਬੰਡਲ if ਮਾਰਗ == 'remote/libremote.a' else ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build' / ਮਾਰਗ for ਮਾਰਗ in ਪੁਸਤਕਾਲਾ] + ['--end-group'], ਲੌਗ_ਕਤਾਰ)
                    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], ਲੌਗ_ਕਤਾਰ)
                with (ਮਾਪ / 'remote-test.log').open('wb') as ਲੌਗ_ਕਤਾਰ:
                    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(['python3', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਸਾਧਨ/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', ਸੈਟਿੰਗਾਂ_ਲਿਖਤ_ਪੱਤਰ, '--output', ਮਾਪ], ਲੌਗ_ਕਤਾਰ)
                ਪ੍ਰਮਾਣਿਤ = json.loads((ਮਾਪ / 'report.json').read_text())
                assert ਪ੍ਰਮਾਣਿਤ['passed']
                ਵਿਵਰਨ_ਕੀਮਤ['checks'].append(ਨਾਂ + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ਵਿਵਰਨ_ਕੀਮਤ['passed'] = True
    finally:
        ਵਿਵਰਨ_ਕੀਮਤ['personal_settings_unchanged'] = ਵਿਅਕਤੀਗਤ_ਸੈਟਿੰਗਜ਼.read_bytes() == 원래설정
        if not ਵਿਵਰਨ_ਕੀਮਤ['personal_settings_unchanged']:
            ਵਿਵਰਨ_ਕੀਮਤ['passed'] = False
        ਵਿਵਰਨ_ਕੀਮਤ['kernel_sha256'] = hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel8.img').read_bytes()).hexdigest()
        (ਆਉਟਪੁੱਟ / 'report.json').write_text(json.dumps(ਵਿਵਰਨ_ਕੀਮਤ, ensure_ascii=False, indent=2) + '\n')
    assert ਵਿਵਰਨ_ਕੀਮਤ['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ਵਿਵਰਨ_ਕੀਮਤ, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ਚਲਾਓ_2()
