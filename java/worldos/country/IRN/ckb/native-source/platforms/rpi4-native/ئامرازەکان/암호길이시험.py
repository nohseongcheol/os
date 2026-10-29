#!/usr/bin/env python3
"""개인 گرێدان_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from دوورەدەس_ڕێكبەندەكان import ئامادە_کردن_9ce364fc
from COSL배포 import جێمەبەست_ناو, کتێبخانە

기준 = Path(__file__).resolve().parents[1]


def ڕادان():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    ڕێککردنە_شەخسییەکان = 기준 / 'build/remote/access.json'
    원래설정 = ڕێککردنە_شەخسییەکان.read_bytes()
    ڕاپۆرت_نرخ = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            ڕێكبەندەكان_گوزەر = 시험터 / 'build/remote'
            ڕێكبەندەكان_گوزەر.mkdir(parents=True)
            ڕێكبەندەكان_فایل = ڕێكبەندەكان_گوزەر / 'access.json'
            def ڕایت_کردن_ڕێكبەندەكان(دەیتا):
                ڕێكبەندەكان_فایل.write_text(json.dumps(دەیتا, ensure_ascii=False) + '\n')
                ڕێكبەندەكان_فایل.chmod(0o600)
            def سەلماندن_ڕێكبەندەكان(توێکڵ, 화면):
                ڕایت_کردن_ڕێكبەندەكان({'user': 'user', 'ssh_password': توێکڵ, 'vnc_password': 화면})
                원본 = ڕێكبەندەكان_فایل.read_bytes()
                ئامادە_کردن_9ce364fc(시험터)
                assert ڕێكبەندەكان_فایل.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (ڕێكبەندەكان_گوزەر / 'پرۆفایل.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (ڕێكبەندەكان_گوزەر / 'پرۆفایل.h').stat().st_mode & 0o777 == 0o600
            for توێکڵ, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                سەلماندن_ڕێكبەندەكان(توێکڵ, 화면)
            ڕاپۆرت_نرخ['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for گۆڕین_نرخ, تێنووسین_نرخ in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                دەیتا = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                دەیتا.update(گۆڕین_نرخ)
                ڕایت_کردن_ڕێكبەندەكان(دەیتا)
                try:
                    ئامادە_کردن_9ce364fc(시험터)
                except SystemExit as هەڵە:
                    assert تێنووسین_نرخ in str(هەڵە), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + تێنووسین_نرخ)
            ڕاپۆرت_نرخ['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ڕێكبەندەكان = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            لکێنەر = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ئەرشیف_ئامراز = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def جێبەجێکردن_فەرمان(인수, تۆمار_ڕزن):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=تۆمار_ڕزن,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ناو, توێکڵ, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ناو, flush=True)
                سەلماندن_ڕێكبەندەكان(توێکڵ, 화면)
                결과 = 출력 / ناو
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as تۆمار_ڕزن:
                    목적들 = []
                    for 원본 in sorted((기준 / 'دوورەدەس_نرخ').glob('*.c')):
                        جێمەبەست_نرخ = 시험터 / (원본.stem + '.o')
                        جێبەجێکردن_فەرمان([번역기] + ڕێكبەندەكان + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', ڕێكبەندەكان_گوزەر, '-I', 기준 / 'دوورەدەس_نرخ', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', جێمەبەست_نرخ], تۆمار_ڕزن)
                        목적들.append(جێمەبەست_نرخ)
                    دوورەدەس_گورزە = 시험터 / 'libremote.a'
                    جێبەجێکردن_فەرمان([ئەرشیف_ئامراز, 'rcs', دوورەدەس_گورزە] + 목적들, تۆمار_ڕزن)
                    جێبەجێکردن_فەرمان([لکێنەر, '--gc-sections', '-T', 기준 / '부팅/لینك_ڕیزبەست.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (ناو + '.o') for ناو in جێمەبەست_ناو] + ['--start-group'] +
                         [دوورەدەس_گورزە if گوزەر == 'remote/libremote.a' else 기준 / 'build' / گوزەر for گوزەر in کتێبخانە] + ['--end-group'], تۆمار_ڕزن)
                    جێبەجێکردن_فەرمان([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], تۆمار_ڕزن)
                with (결과 / 'remote-test.log').open('wb') as تۆمار_ڕزن:
                    جێبەجێکردن_فەرمان(['python3', 기준 / 'ئامرازەکان/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', ڕێكبەندەكان_فایل, '--output', 결과], تۆمار_ڕزن)
                ڕەوایی = json.loads((결과 / 'report.json').read_text())
                assert ڕەوایی['passed']
                ڕاپۆرت_نرخ['checks'].append(ناو + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ڕاپۆرت_نرخ['passed'] = True
    finally:
        ڕاپۆرت_نرخ['personal_settings_unchanged'] = ڕێککردنە_شەخسییەکان.read_bytes() == 원래설정
        if not ڕاپۆرت_نرخ['personal_settings_unchanged']:
            ڕاپۆرت_نرخ['passed'] = False
        ڕاپۆرت_نرخ['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(ڕاپۆرت_نرخ, ensure_ascii=False, indent=2) + '\n')
    assert ڕاپۆرت_نرخ['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ڕاپۆرت_نرخ, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ڕادان()
