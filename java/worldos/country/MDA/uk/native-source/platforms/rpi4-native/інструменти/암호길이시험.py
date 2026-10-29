#!/usr/bin/env python3
"""개인 зв_язок_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from віддалений_Настройки import Готувати
from COSL배포 import місце_ім_я, бібліотека

Дії_корінь = Path(__file__).resolve().parents[1]


def запустити():
    Вивід = Дії_корінь / 'build/verification/password-length'
    Вивід.mkdir(parents=True, exist_ok=True)
    особисте_Настройки = Дії_корінь / 'build/remote/access.json'
    원래설정 = особисте_Настройки.read_bytes()
    звіт_значення = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Настройки_шлях = 시험터 / 'build/remote'
            Настройки_шлях.mkdir(parents=True)
            Настройки_Файл = Настройки_шлях / 'access.json'
            def записування_Настройки(дані):
                Настройки_Файл.write_text(json.dumps(дані, ensure_ascii=False) + '\n')
                Настройки_Файл.chmod(0o600)
            def перевіряти_Настройки(оболонка, 화면):
                записування_Настройки({'user': 'user', 'ssh_password': оболонка, 'vnc_password': 화면})
                원본 = Настройки_Файл.read_bytes()
                Готувати(시험터)
                assert Настройки_Файл.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Настройки_шлях / 'Профіль.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Настройки_шлях / 'Профіль.h').stat().st_mode & 0o777 == 0o600
            for оболонка, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                перевіряти_Настройки(оболонка, 화면)
            звіт_значення['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for змінювати_значення, запис_значення_962f286b in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                дані = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                дані.update(змінювати_значення)
                записування_Настройки(дані)
                try:
                    Готувати(시험터)
                except SystemExit as ПОМИЛКА:
                    assert запис_значення_962f286b in str(ПОМИЛКА), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + запис_значення_962f286b)
            звіт_значення['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Налаштування = json.loads((Дії_корінь / 'build/remote/libassh-build.json').read_text())['flags']
            компілятор_інструмент = os.environ.get('ARM64_CC', 'clang')
            Конектор = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Архів_інструмент = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Виконати_команда(аргументи, журнал_запис):
                subprocess.run(list(map(str, аргументи)), cwd=str(Дії_корінь), stdout=журнал_запис,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Назва, оболонка, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Назва, flush=True)
                перевіряти_Настройки(оболонка, 화면)
                результат = Вивід / Назва
                результат.mkdir(exist_ok=True)
                with (результат / 'build.log').open('wb') as журнал_запис:
                    목적들 = []
                    for 원본 in sorted((Дії_корінь / 'віддалений_значення').glob('*.c')):
                        місце_значення = 시험터 / (원본.stem + '.o')
                        Виконати_команда([компілятор_інструмент] + Налаштування + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Настройки_шлях, '-I', Дії_корінь / 'віддалений_значення', '-I', Дії_корінь / 'vendor/libassh/src',
                             '-I', Дії_корінь / 'vendor/bearssl/inc', '-I', Дії_корінь / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', місце_значення], журнал_запис)
                        목적들.append(місце_значення)
                    віддалений_набір = 시험터 / 'libremote.a'
                    Виконати_команда([Архів_інструмент, 'rcs', віддалений_набір] + 목적들, журнал_запис)
                    Виконати_команда([Конектор, '--gc-sections', '-T', Дії_корінь / 'запуск_машини/схема_компонування.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Дії_корінь / 'build' / (Назва + '.o') for Назва in місце_ім_я] + ['--start-group'] +
                         [віддалений_набір if шлях == 'remote/libremote.a' else Дії_корінь / 'build' / шлях for шлях in бібліотека] + ['--end-group'], журнал_запис)
                    Виконати_команда([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], журнал_запис)
                with (результат / 'remote-test.log').open('wb') as журнал_запис:
                    Виконати_команда(['python3', Дії_корінь / 'інструменти/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Настройки_Файл, '--output', результат], журнал_запис)
                затвердити = json.loads((результат / 'report.json').read_text())
                assert затвердити['passed']
                звіт_значення['checks'].append(Назва + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        звіт_значення['passed'] = True
    finally:
        звіт_значення['personal_settings_unchanged'] = особисте_Настройки.read_bytes() == 원래설정
        if not звіт_значення['personal_settings_unchanged']:
            звіт_значення['passed'] = False
        звіт_значення['kernel_sha256'] = hashlib.sha256((Дії_корінь / 'build/kernel8.img').read_bytes()).hexdigest()
        (Вивід / 'report.json').write_text(json.dumps(звіт_значення, ensure_ascii=False, indent=2) + '\n')
    assert звіт_значення['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(звіт_значення, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    запустити()
