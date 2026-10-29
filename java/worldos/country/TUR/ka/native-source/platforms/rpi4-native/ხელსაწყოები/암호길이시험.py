#!/usr/bin/env python3
"""개인 კავშირი_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from დისტანციური_პარამეტრები import მომზადება
from COSL배포 import მიმართულება_სახელი, ბიბლიოთეკა

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]


def გაშვება():
    출력 = პროეცირება_ფესვი / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    პირადი_პარამეტრები = პროეცირება_ფესვი / 'build/remote/access.json'
    원래설정 = პირადი_პარამეტრები.read_bytes()
    ანგარიში_მნიშვნელობა = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            პარამეტრები_მდებარეობა = 시험터 / 'build/remote'
            პარამეტრები_მდებარეობა.mkdir(parents=True)
            პარამეტრები_ფაილი = პარამეტრები_მდებარეობა / 'access.json'
            def ჩაწერა_პარამეტრები(მონაცემები):
                პარამეტრები_ფაილი.write_text(json.dumps(მონაცემები, ensure_ascii=False) + '\n')
                პარამეტრები_ფაილი.chmod(0o600)
            def გადამოწმება_პარამეტრები(გარემო, 화면):
                ჩაწერა_პარამეტრები({'user': 'user', 'ssh_password': გარემო, 'vnc_password': 화면})
                원본 = პარამეტრები_ფაილი.read_bytes()
                მომზადება(시험터)
                assert პარამეტრები_ფაილი.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (პარამეტრები_მდებარეობა / 'პროფილი.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (პარამეტრები_მდებარეობა / 'პროფილი.h').stat().st_mode & 0o777 == 0o600
            for გარემო, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                გადამოწმება_პარამეტრები(გარემო, 화면)
            ანგარიში_მნიშვნელობა['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for შეცვლა_მნიშვნელობა, შენატანი_მნიშვნელობა in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                მონაცემები = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                მონაცემები.update(შეცვლა_მნიშვნელობა)
                ჩაწერა_პარამეტრები(მონაცემები)
                try:
                    მომზადება(시험터)
                except SystemExit as შეცდომა:
                    assert შენატანი_მნიშვნელობა in str(შეცდომა), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + შენატანი_მნიშვნელობა)
            ანგარიში_მნიშვნელობა['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            პარამეტრები = json.loads((პროეცირება_ფესვი / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            მაერთებელი = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            არქივი_ხელსაწყო = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def შესრულება_ბრძანება(인수, ჟურნალი_ჩაწერა):
                subprocess.run(list(map(str, 인수)), cwd=str(პროეცირება_ფესვი), stdout=ჟურნალი_ჩაწერა,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for სახელი, გარემო, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + სახელი, flush=True)
                გადამოწმება_პარამეტრები(გარემო, 화면)
                გაზომვა = 출력 / სახელი
                გაზომვა.mkdir(exist_ok=True)
                with (გაზომვა / 'build.log').open('wb') as ჟურნალი_ჩაწერა:
                    목적들 = []
                    for 원본 in sorted((პროეცირება_ფესვი / 'დისტანციური_მნიშვნელობა').glob('*.c')):
                        მიმართულება_მნიშვნელობა = 시험터 / (원본.stem + '.o')
                        შესრულება_ბრძანება([번역기] + პარამეტრები + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', პარამეტრები_მდებარეობა, '-I', პროეცირება_ფესვი / 'დისტანციური_მნიშვნელობა', '-I', პროეცირება_ფესვი / 'vendor/libassh/src',
                             '-I', პროეცირება_ფესვი / 'vendor/bearssl/inc', '-I', პროეცირება_ფესვი / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', მიმართულება_მნიშვნელობა], ჟურნალი_ჩაწერა)
                        목적들.append(მიმართულება_მნიშვნელობა)
                    დისტანციური_შეკვრა = 시험터 / 'libremote.a'
                    შესრულება_ბრძანება([არქივი_ხელსაწყო, 'rcs', დისტანციური_შეკვრა] + 목적들, ჟურნალი_ჩაწერა)
                    შესრულება_ბრძანება([მაერთებელი, '--gc-sections', '-T', პროეცირება_ფესვი / '부팅/ბმული_განლაგება.ld', '-o', 시험터 / 'kernel.elf'] +
                         [პროეცირება_ფესვი / 'build' / (სახელი + '.o') for სახელი in მიმართულება_სახელი] + ['--start-group'] +
                         [დისტანციური_შეკვრა if გეზი == 'remote/libremote.a' else პროეცირება_ფესვი / 'build' / გეზი for გეზი in ბიბლიოთეკა] + ['--end-group'], ჟურნალი_ჩაწერა)
                    შესრულება_ბრძანება([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], ჟურნალი_ჩაწერა)
                with (გაზომვა / 'remote-test.log').open('wb') as ჟურნალი_ჩაწერა:
                    შესრულება_ბრძანება(['python3', პროეცირება_ფესვი / 'ხელსაწყოები/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', პარამეტრები_ფაილი, '--output', გაზომვა], ჟურნალი_ჩაწერა)
                შემოწმება = json.loads((გაზომვა / 'report.json').read_text())
                assert შემოწმება['passed']
                ანგარიში_მნიშვნელობა['checks'].append(სახელი + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ანგარიში_მნიშვნელობა['passed'] = True
    finally:
        ანგარიში_მნიშვნელობა['personal_settings_unchanged'] = პირადი_პარამეტრები.read_bytes() == 원래설정
        if not ანგარიში_მნიშვნელობა['personal_settings_unchanged']:
            ანგარიში_მნიშვნელობა['passed'] = False
        ანგარიში_მნიშვნელობა['kernel_sha256'] = hashlib.sha256((პროეცირება_ფესვი / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(ანგარიში_მნიშვნელობა, ensure_ascii=False, indent=2) + '\n')
    assert ანგარიში_მნიშვნელობა['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ანგარიში_მნიშვნელობა, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    გაშვება()
