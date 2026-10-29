#!/usr/bin/env python3
"""개인 ርክብ_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from ርሑቕ_ኣቀማምጣታት import ኣዳልው
from COSL배포 import መዓልቦ_ሽም, ቤት_ንባብ

기준 = Path(__file__).resolve().parents[1]


def ኣኺድ():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    ግላዊ_ኣቀማምጣታት = 기준 / 'build/remote/access.json'
    원래설정 = ግላዊ_ኣቀማምጣታት.read_bytes()
    ጸብጻብ_ዋጋ = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            ኣቀማምጣታት_መገዲ = 시험터 / 'build/remote'
            ኣቀማምጣታት_መገዲ.mkdir(parents=True)
            ኣቀማምጣታት_ፋይል = ኣቀማምጣታት_መገዲ / 'access.json'
            def ጸሓፍ_ኣቀማምጣታት(ሓበሬታ):
                ኣቀማምጣታት_ፋይል.write_text(json.dumps(ሓበሬታ, ensure_ascii=False) + '\n')
                ኣቀማምጣታት_ፋይል.chmod(0o600)
            def ኣረጋግጽ_ኣቀማምጣታት(ሽፋን, 화면):
                ጸሓፍ_ኣቀማምጣታት({'user': 'user', 'ssh_password': ሽፋን, 'vnc_password': 화면})
                원본 = ኣቀማምጣታት_ፋይል.read_bytes()
                ኣዳልው(시험터)
                assert ኣቀማምጣታት_ፋይል.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (ኣቀማምጣታት_መገዲ / 'መግለጺ_መንነት.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (ኣቀማምጣታት_መገዲ / 'መግለጺ_መንነት.h').stat().st_mode & 0o777 == 0o600
            for ሽፋን, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ኣረጋግጽ_ኣቀማምጣታት(ሽፋን, 화면)
            ጸብጻብ_ዋጋ['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ለውጥ_ዋጋ, ምእታው_ዋጋ in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ሓበሬታ = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ሓበሬታ.update(ለውጥ_ዋጋ)
                ጸሓፍ_ኣቀማምጣታት(ሓበሬታ)
                try:
                    ኣዳልው(시험터)
                except SystemExit as ጌጋ:
                    assert ምእታው_ዋጋ in str(ጌጋ), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ምእታው_ዋጋ)
            ጸብጻብ_ዋጋ['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ኣቀማምጣታት = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            መላገቢ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ሰንድ_መሳርሒ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ተግብር_ትእዛዝ(인수, ምዝጉብ_ሪጋ):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=ምዝጉብ_ሪጋ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ሽም, ሽፋን, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ሽም, flush=True)
                ኣረጋግጽ_ኣቀማምጣታት(ሽፋን, 화면)
                결과 = 출력 / ሽም
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as ምዝጉብ_ሪጋ:
                    목적들 = []
                    for 원본 in sorted((기준 / 'ርሑቕ_ዋጋ').glob('*.c')):
                        መዓልቦ_ዋጋ = 시험터 / (원본.stem + '.o')
                        ተግብር_ትእዛዝ([번역기] + ኣቀማምጣታት + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', ኣቀማምጣታት_መገዲ, '-I', 기준 / 'ርሑቕ_ዋጋ', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', መዓልቦ_ዋጋ], ምዝጉብ_ሪጋ)
                        목적들.append(መዓልቦ_ዋጋ)
                    ርሑቕ_ጥማር = 시험터 / 'libremote.a'
                    ተግብር_ትእዛዝ([ሰንድ_መሳርሒ, 'rcs', ርሑቕ_ጥማር] + 목적들, ምዝጉብ_ሪጋ)
                    ተግብር_ትእዛዝ([መላገቢ, '--gc-sections', '-T', 기준 / '부팅/መጋጠሚ_ኣቀማምጣ.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (ሽም + '.o') for ሽም in መዓልቦ_ሽም] + ['--start-group'] +
                         [ርሑቕ_ጥማር if መገዲ == 'remote/libremote.a' else 기준 / 'build' / መገዲ for መገዲ in ቤት_ንባብ] + ['--end-group'], ምዝጉብ_ሪጋ)
                    ተግብር_ትእዛዝ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], ምዝጉብ_ሪጋ)
                with (결과 / 'remote-test.log').open('wb') as ምዝጉብ_ሪጋ:
                    ተግብር_ትእዛዝ(['python3', 기준 / 'መሳርሒታት/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', ኣቀማምጣታት_ፋይል, '--output', 결과], ምዝጉብ_ሪጋ)
                አረጋግፅ = json.loads((결과 / 'report.json').read_text())
                assert አረጋግፅ['passed']
                ጸብጻብ_ዋጋ['checks'].append(ሽም + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ጸብጻብ_ዋጋ['passed'] = True
    finally:
        ጸብጻብ_ዋጋ['personal_settings_unchanged'] = ግላዊ_ኣቀማምጣታት.read_bytes() == 원래설정
        if not ጸብጻብ_ዋጋ['personal_settings_unchanged']:
            ጸብጻብ_ዋጋ['passed'] = False
        ጸብጻብ_ዋጋ['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(ጸብጻብ_ዋጋ, ensure_ascii=False, indent=2) + '\n')
    assert ጸብጻብ_ዋጋ['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ጸብጻብ_ዋጋ, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ኣኺድ()
