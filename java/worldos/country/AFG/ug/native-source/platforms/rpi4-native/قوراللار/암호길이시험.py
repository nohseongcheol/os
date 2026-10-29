#!/usr/bin/env python3
"""개인 ئۇلىنىش_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from يىراق_تەڭشەك import تەييارلىماق
from COSL배포 import نىشان_نامى, ئامبار

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]


def ئىجرا_قىل_2():
    چىقار = كۆرسىتىش_يىلتىز / 'build/verification/password-length'
    چىقار.mkdir(parents=True, exist_ok=True)
    خۇسۇسىي_تەڭشەكلەر = كۆرسىتىش_يىلتىز / 'build/remote/access.json'
    원래설정 = خۇسۇسىي_تەڭشەكلەر.read_bytes()
    خەۋەر_قىممىتى = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            تەڭشەك_يول = 시험터 / 'build/remote'
            تەڭشەك_يول.mkdir(parents=True)
            تەڭشەك_ھۆججەت = تەڭشەك_يول / 'access.json'
            def يازماق_تەڭشەك(مەلۇمات):
                تەڭشەك_ھۆججەت.write_text(json.dumps(مەلۇمات, ensure_ascii=False) + '\n')
                تەڭشەك_ھۆججەت.chmod(0o600)
            def دەلىللىمەك_تەڭشەك(قاپ, 화면):
                يازماق_تەڭشەك({'user': 'user', 'ssh_password': قاپ, 'vnc_password': 화면})
                원본 = تەڭشەك_ھۆججەت.read_bytes()
                تەييارلىماق(시험터)
                assert تەڭشەك_ھۆججەت.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (تەڭشەك_يول / 'ئارخىپ_1c9b560a.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (تەڭشەك_يول / 'ئارخىپ_1c9b560a.h').stat().st_mode & 0o777 == 0o600
            for قاپ, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                دەلىللىمەك_تەڭشەك(قاپ, 화면)
            خەۋەر_قىممىتى['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ئۆزگەرتمەك_قىممىتى, كىرگۈزۈش_قىممىتى in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                مەلۇمات = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                مەلۇمات.update(ئۆزگەرتمەك_قىممىتى)
                يازماق_تەڭشەك(مەلۇمات)
                try:
                    تەييارلىماق(시험터)
                except SystemExit as خاتالىق:
                    assert كىرگۈزۈش_قىممىتى in str(خاتالىق), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + كىرگۈزۈش_قىممىتى)
            خەۋەر_قىممىتى['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            تەڭشەكلەر = json.loads((كۆرسىتىش_يىلتىز / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            ئۇلىغۇچ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ئارخىپ_قورال = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ئىجرا_قىلىش_بۇيرۇق(ئۆزگەرگۈچىلەر, خاتىرە_قۇر):
                subprocess.run(list(map(str, ئۆزگەرگۈچىلەر)), cwd=str(كۆرسىتىش_يىلتىز), stdout=خاتىرە_قۇر,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ئاتى, قاپ, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ئاتى, flush=True)
                دەلىللىمەك_تەڭشەك(قاپ, 화면)
                ئۆلچەم = چىقار / ئاتى
                ئۆلچەم.mkdir(exist_ok=True)
                with (ئۆلچەم / 'build.log').open('wb') as خاتىرە_قۇر:
                    목적들 = []
                    for 원본 in sorted((كۆرسىتىش_يىلتىز / 'يىراق_قىممىتى').glob('*.c')):
                        نىشان_قىممىتى = 시험터 / (원본.stem + '.o')
                        ئىجرا_قىلىش_بۇيرۇق([번역기] + تەڭشەكلەر + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', تەڭشەك_يول, '-I', كۆرسىتىش_يىلتىز / 'يىراق_قىممىتى', '-I', كۆرسىتىش_يىلتىز / 'vendor/libassh/src',
                             '-I', كۆرسىتىش_يىلتىز / 'vendor/bearssl/inc', '-I', كۆرسىتىش_يىلتىز / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', نىشان_قىممىتى], خاتىرە_قۇر)
                        목적들.append(نىشان_قىممىتى)
                    يىراق_توپلام = 시험터 / 'libremote.a'
                    ئىجرا_قىلىش_بۇيرۇق([ئارخىپ_قورال, 'rcs', يىراق_توپلام] + 목적들, خاتىرە_قۇر)
                    ئىجرا_قىلىش_بۇيرۇق([ئۇلىغۇچ, '--gc-sections', '-T', كۆرسىتىش_يىلتىز / '부팅/ئۇلانما_لايىھە.ld', '-o', 시험터 / 'kernel.elf'] +
                         [كۆرسىتىش_يىلتىز / 'build' / (ئاتى + '.o') for ئاتى in نىشان_نامى] + ['--start-group'] +
                         [يىراق_توپلام if يول == 'remote/libremote.a' else كۆرسىتىش_يىلتىز / 'build' / يول for يول in ئامبار] + ['--end-group'], خاتىرە_قۇر)
                    ئىجرا_قىلىش_بۇيرۇق([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], خاتىرە_قۇر)
                with (ئۆلچەم / 'remote-test.log').open('wb') as خاتىرە_قۇر:
                    ئىجرا_قىلىش_بۇيرۇق(['python3', كۆرسىتىش_يىلتىز / 'قوراللار/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', تەڭشەك_ھۆججەت, '--output', ئۆلچەم], خاتىرە_قۇر)
                دەلىللەش = json.loads((ئۆلچەم / 'report.json').read_text())
                assert دەلىللەش['passed']
                خەۋەر_قىممىتى['checks'].append(ئاتى + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        خەۋەر_قىممىتى['passed'] = True
    finally:
        خەۋەر_قىممىتى['personal_settings_unchanged'] = خۇسۇسىي_تەڭشەكلەر.read_bytes() == 원래설정
        if not خەۋەر_قىممىتى['personal_settings_unchanged']:
            خەۋەر_قىممىتى['passed'] = False
        خەۋەر_قىممىتى['kernel_sha256'] = hashlib.sha256((كۆرسىتىش_يىلتىز / 'build/kernel8.img').read_bytes()).hexdigest()
        (چىقار / 'report.json').write_text(json.dumps(خەۋەر_قىممىتى, ensure_ascii=False, indent=2) + '\n')
    assert خەۋەر_قىممىتى['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(خەۋەر_قىممىتى, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ئىجرا_قىل_2()
