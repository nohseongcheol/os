#!/usr/bin/env python3
"""개인 врска_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from далечинскo_Параметри import Подготви
from COSL배포 import одредиште_име, библиотека

Project_корен = Path(__file__).resolve().parents[1]


def Изврши_2():
    출력 = Project_корен / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    лични_параметри = Project_корен / 'build/remote/access.json'
    원래설정 = лични_параметри.read_bytes()
    извештај_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Параметри_патека = 시험터 / 'build/remote'
            Параметри_патека.mkdir(parents=True)
            Параметри_датотека = Параметри_патека / 'access.json'
            def запиши_Параметри(податоци):
                Параметри_датотека.write_text(json.dumps(податоци, ensure_ascii=False) + '\n')
                Параметри_датотека.chmod(0o600)
            def провери_Параметри(обвивка, 화면):
                запиши_Параметри({'user': 'user', 'ssh_password': обвивка, 'vnc_password': 화면})
                원본 = Параметри_датотека.read_bytes()
                Подготви(시험터)
                assert Параметри_датотека.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Параметри_патека / 'Профил.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Параметри_патека / 'Профил.h').stat().st_mode & 0o777 == 0o600
            for обвивка, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                провери_Параметри(обвивка, 화면)
            извештај_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for измени_VALUE, внес_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                податоци = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                податоци.update(измени_VALUE)
                запиши_Параметри(податоци)
                try:
                    Подготви(시험터)
                except SystemExit as ГРЕШКА:
                    assert внес_VALUE in str(ГРЕШКА), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + внес_VALUE)
            извештај_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Подесувања = json.loads((Project_корен / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            приклучок = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Архива_алатка = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Изврши_наредба(Аргументи, LOG_ред):
                subprocess.run(list(map(str, Аргументи)), cwd=str(Project_корен), stdout=LOG_ред,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Име, обвивка, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Име, flush=True)
                провери_Параметри(обвивка, 화면)
                мерка = 출력 / Име
                мерка.mkdir(exist_ok=True)
                with (мерка / 'build.log').open('wb') as LOG_ред:
                    목적들 = []
                    for 원본 in sorted((Project_корен / 'далечинскo_VALUE').glob('*.c')):
                        одредиште_VALUE = 시험터 / (원본.stem + '.o')
                        Изврши_наредба([번역기] + Подесувања + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Параметри_патека, '-I', Project_корен / 'далечинскo_VALUE', '-I', Project_корен / 'vendor/libassh/src',
                             '-I', Project_корен / 'vendor/bearssl/inc', '-I', Project_корен / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', одредиште_VALUE], LOG_ред)
                        목적들.append(одредиште_VALUE)
                    далечинскo_пакет = 시험터 / 'libremote.a'
                    Изврши_наредба([Архива_алатка, 'rcs', далечинскo_пакет] + 목적들, LOG_ред)
                    Изврши_наредба([приклучок, '--gc-sections', '-T', Project_корен / '부팅/Врска_Распоред.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_корен / 'build' / (Име + '.o') for Име in одредиште_име] + ['--start-group'] +
                         [далечинскo_пакет if ПАТЕКА == 'remote/libremote.a' else Project_корен / 'build' / ПАТЕКА for ПАТЕКА in библиотека] + ['--end-group'], LOG_ред)
                    Изврши_наредба([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_ред)
                with (мерка / 'remote-test.log').open('wb') as LOG_ред:
                    Изврши_наредба(['python3', Project_корен / 'Алатки/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Параметри_датотека, '--output', мерка], LOG_ред)
                потврди = json.loads((мерка / 'report.json').read_text())
                assert потврди['passed']
                извештај_VALUE['checks'].append(Име + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        извештај_VALUE['passed'] = True
    finally:
        извештај_VALUE['personal_settings_unchanged'] = лични_параметри.read_bytes() == 원래설정
        if not извештај_VALUE['personal_settings_unchanged']:
            извештај_VALUE['passed'] = False
        извештај_VALUE['kernel_sha256'] = hashlib.sha256((Project_корен / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(извештај_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert извештај_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(извештај_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Изврши_2()
