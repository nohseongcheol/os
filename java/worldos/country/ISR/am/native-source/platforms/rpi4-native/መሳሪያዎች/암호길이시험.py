#!/usr/bin/env python3
"""개인 ግንኙነት_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from የሩቅ_ቅንብሮች import አዘጋጅ_9ce364fc
from COSL배포 import መድረሻ_ስም, ማከማቻ_ስፍራ

አሳይ_ስር = Path(__file__).resolve().parents[1]


def ማስኬጃ():
    ውጤት = አሳይ_ስር / 'build/verification/password-length'
    ውጤት.mkdir(parents=True, exist_ok=True)
    የግል_ቅንብሮች = አሳይ_ስር / 'build/remote/access.json'
    원래설정 = የግል_ቅንብሮች.read_bytes()
    ዘገባ_እሴት = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            ቅንብሮች_ዱካ = 시험터 / 'build/remote'
            ቅንብሮች_ዱካ.mkdir(parents=True)
            ቅንብሮች_ፋይል = ቅንብሮች_ዱካ / 'access.json'
            def ጻፍ_ቅንብሮች(ውሂብ):
                ቅንብሮች_ፋይል.write_text(json.dumps(ውሂብ, ensure_ascii=False) + '\n')
                ቅንብሮች_ፋይል.chmod(0o600)
            def አረጋግጥ_ቅንብሮች(ሼል, 화면):
                ጻፍ_ቅንብሮች({'user': 'user', 'ssh_password': ሼል, 'vnc_password': 화면})
                원본 = ቅንብሮች_ፋይል.read_bytes()
                አዘጋጅ_9ce364fc(시험터)
                assert ቅንብሮች_ፋይል.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (ቅንብሮች_ዱካ / 'መገለጫ.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (ቅንብሮች_ዱካ / 'መገለጫ.h').stat().st_mode & 0o777 == 0o600
            for ሼል, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                አረጋግጥ_ቅንብሮች(ሼል, 화면)
            ዘገባ_እሴት['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ለውጥ_እሴት, ምዝግብ_እሴት in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ውሂብ = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ውሂብ.update(ለውጥ_እሴት)
                ጻፍ_ቅንብሮች(ውሂብ)
                try:
                    አዘጋጅ_9ce364fc(시험터)
                except SystemExit as ስህተት:
                    assert ምዝግብ_እሴት in str(ስህተት), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ምዝግብ_እሴት)
            ዘገባ_እሴት['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ማሰናጃዎች = json.loads((አሳይ_ስር / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            አገናኝ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ከዝን_መሳሪያ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ፈጽም_ትእዛዝ(인수, መዝግብ_ረድፍ):
                subprocess.run(list(map(str, 인수)), cwd=str(አሳይ_ስር), stdout=መዝግብ_ረድፍ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ስም, ሼል, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ስም, flush=True)
                አረጋግጥ_ቅንብሮች(ሼል, 화면)
                ልኬት = ውጤት / ስም
                ልኬት.mkdir(exist_ok=True)
                with (ልኬት / 'build.log').open('wb') as መዝግብ_ረድፍ:
                    목적들 = []
                    for 원본 in sorted((አሳይ_ስር / 'የሩቅ_እሴት').glob('*.c')):
                        መድረሻ_እሴት = 시험터 / (원본.stem + '.o')
                        ፈጽም_ትእዛዝ([번역기] + ማሰናጃዎች + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', ቅንብሮች_ዱካ, '-I', አሳይ_ስር / 'የሩቅ_እሴት', '-I', አሳይ_ስር / 'vendor/libassh/src',
                             '-I', አሳይ_ስር / 'vendor/bearssl/inc', '-I', አሳይ_ስር / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', መድረሻ_እሴት], መዝግብ_ረድፍ)
                        목적들.append(መድረሻ_እሴት)
                    የሩቅ_ቀርቅብ = 시험터 / 'libremote.a'
                    ፈጽም_ትእዛዝ([ከዝን_መሳሪያ, 'rcs', የሩቅ_ቀርቅብ] + 목적들, መዝግብ_ረድፍ)
                    ፈጽም_ትእዛዝ([አገናኝ, '--gc-sections', '-T', አሳይ_ስር / '부팅/አገናኝ_አሰሳ.ld', '-o', 시험터 / 'kernel.elf'] +
                         [አሳይ_ስር / 'build' / (ስም + '.o') for ስም in መድረሻ_ስም] + ['--start-group'] +
                         [የሩቅ_ቀርቅብ if መተላለፊያ == 'remote/libremote.a' else አሳይ_ስር / 'build' / መተላለፊያ for መተላለፊያ in ማከማቻ_ስፍራ] + ['--end-group'], መዝግብ_ረድፍ)
                    ፈጽም_ትእዛዝ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], መዝግብ_ረድፍ)
                with (ልኬት / 'remote-test.log').open('wb') as መዝግብ_ረድፍ:
                    ፈጽም_ትእዛዝ(['python3', አሳይ_ስር / 'መሳሪያዎች/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', ቅንብሮች_ፋይል, '--output', ልኬት], መዝግብ_ረድፍ)
                ትክክለኛነት_አረጋግጥ = json.loads((ልኬት / 'report.json').read_text())
                assert ትክክለኛነት_አረጋግጥ['passed']
                ዘገባ_እሴት['checks'].append(ስም + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ዘገባ_እሴት['passed'] = True
    finally:
        ዘገባ_እሴት['personal_settings_unchanged'] = የግል_ቅንብሮች.read_bytes() == 원래설정
        if not ዘገባ_እሴት['personal_settings_unchanged']:
            ዘገባ_እሴት['passed'] = False
        ዘገባ_እሴት['kernel_sha256'] = hashlib.sha256((አሳይ_ስር / 'build/kernel8.img').read_bytes()).hexdigest()
        (ውጤት / 'report.json').write_text(json.dumps(ዘገባ_እሴት, ensure_ascii=False, indent=2) + '\n')
    assert ዘገባ_እሴት['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ዘገባ_እሴት, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ማስኬጃ()
