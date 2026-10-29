#!/usr/bin/env python3
"""개인 веза_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from удаљено_Подешавања import Припремити
from COSL배포 import одредиште_назив, библиотека

기준 = Path(__file__).resolve().parents[1]


def 시작():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    корисничко_подешавање = 기준 / 'build/remote/access.json'
    원래설정 = корисничко_подешавање.read_bytes()
    извјештај_вриједност = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Подешавања_пут = 시험터 / 'build/remote'
            Подешавања_пут.mkdir(parents=True)
            Подешавања_фајл = Подешавања_пут / 'access.json'
            def писати_Подешавања(подаци):
                Подешавања_фајл.write_text(json.dumps(подаци, ensure_ascii=False) + '\n')
                Подешавања_фајл.chmod(0o600)
            def потврдити_Подешавања(љуска, 화면):
                писати_Подешавања({'user': 'user', 'ssh_password': љуска, 'vnc_password': 화면})
                원본 = Подешавања_фајл.read_bytes()
                Припремити(시험터)
                assert Подешавања_фајл.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Подешавања_пут / 'Профил.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Подешавања_пут / 'Профил.h').stat().st_mode & 0o777 == 0o600
            for љуска, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                потврдити_Подешавања(љуска, 화면)
            извјештај_вриједност['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for промијенити_вриједност, унос_вриједност in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                подаци = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                подаци.update(промијенити_вриједност)
                писати_Подешавања(подаци)
                try:
                    Припремити(시험터)
                except SystemExit as грешка:
                    assert унос_вриједност in str(грешка), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + унос_вриједност)
            извјештај_вриједност['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Подешавања = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            конектор = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            архива_алатка = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def 실행(인수, дневник_рада_ред):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=дневник_рада_ред,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for назив, љуска, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + назив, flush=True)
                потврдити_Подешавања(љуска, 화면)
                결과 = 출력 / назив
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as дневник_рада_ред:
                    목적들 = []
                    for 원본 in sorted((기준 / 'удаљено_вриједност').glob('*.c')):
                        одредиште_вриједност = 시험터 / (원본.stem + '.o')
                        실행([번역기] + Подешавања + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Подешавања_пут, '-I', 기준 / 'удаљено_вриједност', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', одредиште_вриједност], дневник_рада_ред)
                        목적들.append(одредиште_вриједност)
                    удаљено_пакет = 시험터 / 'libremote.a'
                    실행([архива_алатка, 'rcs', удаљено_пакет] + 목적들, дневник_рада_ред)
                    실행([конектор, '--gc-sections', '-T', 기준 / '부팅/веза_изглед.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (назив + '.o') for назив in одредиште_назив] + ['--start-group'] +
                         [удаљено_пакет if пут == 'remote/libremote.a' else 기준 / 'build' / пут for пут in библиотека] + ['--end-group'], дневник_рада_ред)
                    실행([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], дневник_рада_ред)
                with (결과 / 'remote-test.log').open('wb') as дневник_рада_ред:
                    실행(['python3', 기준 / '도구/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Подешавања_фајл, '--output', 결과], дневник_рада_ред)
                овјерити = json.loads((결과 / 'report.json').read_text())
                assert овјерити['passed']
                извјештај_вриједност['checks'].append(назив + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        извјештај_вриједност['passed'] = True
    finally:
        извјештај_вриједност['personal_settings_unchanged'] = корисничко_подешавање.read_bytes() == 원래설정
        if not извјештај_вриједност['personal_settings_unchanged']:
            извјештај_вриједност['passed'] = False
        извјештај_вриједност['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(извјештај_вриједност, ensure_ascii=False, indent=2) + '\n')
    assert извјештај_вриједност['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(извјештај_вриједност, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    시작()
