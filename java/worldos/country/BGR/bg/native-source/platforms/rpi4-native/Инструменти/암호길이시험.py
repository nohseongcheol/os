#!/usr/bin/env python3
"""개인 връзка_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from отдалечен_Настройки import Подготвяне
from COSL배포 import местоназначение_препратка_към_клетка, библиотека

проект_корен = Path(__file__).resolve().parents[1]


def Стартиране():
    Изход = проект_корен / 'build/verification/password-length'
    Изход.mkdir(parents=True, exist_ok=True)
    лични_Настройки = проект_корен / 'build/remote/access.json'
    원래설정 = лични_Настройки.read_bytes()
    отчет_стойност = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Настройки_път = 시험터 / 'build/remote'
            Настройки_път.mkdir(parents=True)
            Настройки_Файл = Настройки_път / 'access.json'
            def записване_Настройки(данни):
                Настройки_Файл.write_text(json.dumps(данни, ensure_ascii=False) + '\n')
                Настройки_Файл.chmod(0o600)
            def проверявам_Настройки(обвивка, 화면):
                записване_Настройки({'user': 'user', 'ssh_password': обвивка, 'vnc_password': 화면})
                원본 = Настройки_Файл.read_bytes()
                Подготвяне(시험터)
                assert Настройки_Файл.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Настройки_път / 'Профил.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Настройки_път / 'Профил.h').stat().st_mode & 0o777 == 0o600
            for обвивка, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                проверявам_Настройки(обвивка, 화면)
            отчет_стойност['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for променям_стойност, запис_стойност in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                данни = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                данни.update(променям_стойност)
                записване_Настройки(данни)
                try:
                    Подготвяне(시험터)
                except SystemExit as ГРЕШКА:
                    assert запис_стойност in str(ГРЕШКА), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + запис_стойност)
            отчет_стойност['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Настройки = json.loads((проект_корен / 'build/remote/libassh-build.json').read_text())['flags']
            компилатор_инструмент = os.environ.get('ARM64_CC', 'clang')
            Конектор = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Архив_инструмент = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def изпълнявам_команда(Параметри, регистрирам_запис):
                subprocess.run(list(map(str, Параметри)), cwd=str(проект_корен), stdout=регистрирам_запис,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Име, обвивка, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Име, flush=True)
                проверявам_Настройки(обвивка, 화면)
                РЕЗУЛТАТ = Изход / Име
                РЕЗУЛТАТ.mkdir(exist_ok=True)
                with (РЕЗУЛТАТ / 'build.log').open('wb') as регистрирам_запис:
                    목적들 = []
                    for 원본 in sorted((проект_корен / 'отдалечен_стойност').glob('*.c')):
                        местоназначение_стойност = 시험터 / (원본.stem + '.o')
                        изпълнявам_команда([компилатор_инструмент] + Настройки + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Настройки_път, '-I', проект_корен / 'отдалечен_стойност', '-I', проект_корен / 'vendor/libassh/src',
                             '-I', проект_корен / 'vendor/bearssl/inc', '-I', проект_корен / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', местоназначение_стойност], регистрирам_запис)
                        목적들.append(местоназначение_стойност)
                    отдалечен_пакет = 시험터 / 'libremote.a'
                    изпълнявам_команда([Архив_инструмент, 'rcs', отдалечен_пакет] + 목적들, регистрирам_запис)
                    изпълнявам_команда([Конектор, '--gc-sections', '-T', проект_корен / '부팅/Връзка_схема.ld', '-o', 시험터 / 'kernel.elf'] +
                         [проект_корен / 'build' / (Име + '.o') for Име in местоназначение_препратка_към_клетка] + ['--start-group'] +
                         [отдалечен_пакет if ПЪТ == 'remote/libremote.a' else проект_корен / 'build' / ПЪТ for ПЪТ in библиотека] + ['--end-group'], регистрирам_запис)
                    изпълнявам_команда([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], регистрирам_запис)
                with (РЕЗУЛТАТ / 'remote-test.log').open('wb') as регистрирам_запис:
                    изпълнявам_команда(['python3', проект_корен / 'Инструменти/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Настройки_Файл, '--output', РЕЗУЛТАТ], регистрирам_запис)
                проверка = json.loads((РЕЗУЛТАТ / 'report.json').read_text())
                assert проверка['passed']
                отчет_стойност['checks'].append(Име + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        отчет_стойност['passed'] = True
    finally:
        отчет_стойност['personal_settings_unchanged'] = лични_Настройки.read_bytes() == 원래설정
        if not отчет_стойност['personal_settings_unchanged']:
            отчет_стойност['passed'] = False
        отчет_стойност['kernel_sha256'] = hashlib.sha256((проект_корен / 'build/kernel8.img').read_bytes()).hexdigest()
        (Изход / 'report.json').write_text(json.dumps(отчет_стойност, ensure_ascii=False, indent=2) + '\n')
    assert отчет_стойност['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(отчет_стойност, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Стартиране()
