#!/usr/bin/env python3
"""개인 веза_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from удаљен_Поставке import Припремити
from COSL배포 import одредиште_име, библиотека

пројектовати_корен = Path(__file__).resolve().parents[1]


def Покрени():
    Излаз = пројектовати_корен / 'build/verification/password-length'
    Излаз.mkdir(parents=True, exist_ok=True)
    корисничко_подешавање = пројектовати_корен / 'build/remote/access.json'
    원래설정 = корисничко_подешавање.read_bytes()
    извештај_вриједност = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Поставке_пут = 시험터 / 'build/remote'
            Поставке_пут.mkdir(parents=True)
            Поставке_фајл = Поставке_пут / 'access.json'
            def писати_Поставке(подаци):
                Поставке_фајл.write_text(json.dumps(подаци, ensure_ascii=False) + '\n')
                Поставке_фајл.chmod(0o600)
            def потврдити_Поставке(љуска, 화면):
                писати_Поставке({'user': 'user', 'ssh_password': љуска, 'vnc_password': 화면})
                원본 = Поставке_фајл.read_bytes()
                Припремити(시험터)
                assert Поставке_фајл.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Поставке_пут / 'Профил.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Поставке_пут / 'Профил.h').stat().st_mode & 0o777 == 0o600
            for љуска, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                потврдити_Поставке(љуска, 화면)
            извештај_вриједност['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for промијенити_вриједност, унос_вриједност in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                подаци = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                подаци.update(промијенити_вриједност)
                писати_Поставке(подаци)
                try:
                    Припремити(시험터)
                except SystemExit as ГРЕШКА:
                    assert унос_вриједност in str(ГРЕШКА), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + унос_вриједност)
            извештај_вриједност['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Поставке = json.loads((пројектовати_корен / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Конектор = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Архива_алат = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Изврши_команда(Аргументи, евиденција_ред):
                subprocess.run(list(map(str, Аргументи)), cwd=str(пројектовати_корен), stdout=евиденција_ред,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Назив, љуска, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Назив, flush=True)
                потврдити_Поставке(љуска, 화면)
                ИСХОД = Излаз / Назив
                ИСХОД.mkdir(exist_ok=True)
                with (ИСХОД / 'build.log').open('wb') as евиденција_ред:
                    목적들 = []
                    for 원본 in sorted((пројектовати_корен / 'удаљен_вриједност').glob('*.c')):
                        одредиште_вриједност = 시험터 / (원본.stem + '.o')
                        Изврши_команда([번역기] + Поставке + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Поставке_пут, '-I', пројектовати_корен / 'удаљен_вриједност', '-I', пројектовати_корен / 'vendor/libassh/src',
                             '-I', пројектовати_корен / 'vendor/bearssl/inc', '-I', пројектовати_корен / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', одредиште_вриједност], евиденција_ред)
                        목적들.append(одредиште_вриједност)
                    удаљен_пакет = 시험터 / 'libremote.a'
                    Изврши_команда([Архива_алат, 'rcs', удаљен_пакет] + 목적들, евиденција_ред)
                    Изврши_команда([Конектор, '--gc-sections', '-T', пројектовати_корен / '부팅/Веза_изглед.ld', '-o', 시험터 / 'kernel.elf'] +
                         [пројектовати_корен / 'build' / (Назив + '.o') for Назив in одредиште_име] + ['--start-group'] +
                         [удаљен_пакет if ПУТАЊА == 'remote/libremote.a' else пројектовати_корен / 'build' / ПУТАЊА for ПУТАЊА in библиотека] + ['--end-group'], евиденција_ред)
                    Изврши_команда([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], евиденција_ред)
                with (ИСХОД / 'remote-test.log').open('wb') as евиденција_ред:
                    Изврши_команда(['python3', пројектовати_корен / 'Алатке/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Поставке_фајл, '--output', ИСХОД], евиденција_ред)
                потврдити_5fb2b747 = json.loads((ИСХОД / 'report.json').read_text())
                assert потврдити_5fb2b747['passed']
                извештај_вриједност['checks'].append(Назив + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        извештај_вриједност['passed'] = True
    finally:
        извештај_вриједност['personal_settings_unchanged'] = корисничко_подешавање.read_bytes() == 원래설정
        if not извештај_вриједност['personal_settings_unchanged']:
            извештај_вриједност['passed'] = False
        извештај_вриједност['kernel_sha256'] = hashlib.sha256((пројектовати_корен / 'build/kernel8.img').read_bytes()).hexdigest()
        (Излаз / 'report.json').write_text(json.dumps(извештај_вриједност, ensure_ascii=False, indent=2) + '\n')
    assert извештај_вриједност['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(извештај_вриједност, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Покрени()
