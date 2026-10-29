#!/usr/bin/env python3
"""개인 контакт_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from удаленный_Настройки import Подготовить
from COSL배포 import цель_имя, библиотека

задача_корень = Path(__file__).resolve().parents[1]


def запустить():
    текстовыйВывод = задача_корень / 'build/verification/password-length'
    текстовыйВывод.mkdir(parents=True, exist_ok=True)
    личные_настройки = задача_корень / 'build/remote/access.json'
    원래설정 = личные_настройки.read_bytes()
    Отчет_ЗНАЧЕН = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            тест_рабочая_область = Path(임시)
            Настройки_путь = тест_рабочая_область / 'build/remote'
            Настройки_путь.mkdir(parents=True)
            Настройки_файл = Настройки_путь / 'access.json'
            def запись_Настройки(данные):
                Настройки_файл.write_text(json.dumps(данные, ensure_ascii=False) + '\n')
                Настройки_файл.chmod(0o600)
            def проверять_Настройки(оболочка, экран):
                запись_Настройки({'user': 'user', 'ssh_password': оболочка, 'vnc_password': экран})
                원본 = Настройки_файл.read_bytes()
                Подготовить(тест_рабочая_область)
                assert Настройки_файл.read_bytes() == 원본, 'Settings were rewritten'
                HEAD_ЗНАЧЕН = (Настройки_путь / 'Profile.h').read_text()
                일치 = re.search(r'экран_пароль\[\] = \{([^}]+)\}', HEAD_ЗНАЧЕН)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Настройки_путь / 'Profile.h').stat().st_mode & 0o777 == 0o600
            for оболочка, экран in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                проверять_Настройки(оболочка, экран)
            Отчет_ЗНАЧЕН['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for изменить_ЗНАЧЕН, ввод_ЗНАЧЕН in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                данные = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                данные.update(изменить_ЗНАЧЕН)
                запись_Настройки(данные)
                try:
                    Подготовить(тест_рабочая_область)
                except SystemExit as ошибка:
                    assert ввод_ЗНАЧЕН in str(ошибка), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ввод_ЗНАЧЕН)
            Отчет_ЗНАЧЕН['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Настройки = json.loads((задача_корень / 'build/remote/libassh-build.json').read_text())['flags']
            компилятор_средство = os.environ.get('ARM64_CC', 'clang')
            разъем = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Архив_средство = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def 실행(аргументы, LOG_ЗАПИСЬ):
                subprocess.run(list(map(str, аргументы)), cwd=str(задача_корень), stdout=LOG_ЗАПИСЬ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Название, оболочка, экран in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Название, flush=True)
                проверять_Настройки(оболочка, экран)
                результат = текстовыйВывод / Название
                результат.mkdir(exist_ok=True)
                with (результат / 'build.log').open('wb') as LOG_ЗАПИСЬ:
                    목적들 = []
                    for 원본 in sorted((задача_корень / 'удаленный_ЗНАЧЕН').glob('*.c')):
                        цель_ЗНАЧЕН = тест_рабочая_область / (원본.stem + '.o')
                        실행([компилятор_средство] + Настройки + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Настройки_путь, '-I', задача_корень / 'удаленный_ЗНАЧЕН', '-I', задача_корень / 'vendor/libassh/src',
                             '-I', задача_корень / 'vendor/bearssl/inc', '-I', задача_корень / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', цель_ЗНАЧЕН], LOG_ЗАПИСЬ)
                        목적들.append(цель_ЗНАЧЕН)
                    удаленный_пакет = тест_рабочая_область / 'libremote.a'
                    실행([Архив_средство, 'rcs', удаленный_пакет] + 목적들, LOG_ЗАПИСЬ)
                    실행([разъем, '--gc-sections', '-T', задача_корень / 'запуск_машины/схема_компоновки.ld', '-o', тест_рабочая_область / 'kernel.elf'] +
                         [задача_корень / 'build' / (Название + '.o') for Название in цель_имя] + ['--start-group'] +
                         [удаленный_пакет if путь == 'remote/libremote.a' else задача_корень / 'build' / путь for путь in библиотека] + ['--end-group'], LOG_ЗАПИСЬ)
                    실행([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         тест_рабочая_область / 'kernel.elf', тест_рабочая_область / 'kernel8.img'], LOG_ЗАПИСЬ)
                with (результат / 'remote-test.log').open('wb') as LOG_ЗАПИСЬ:
                    실행(['python3', задача_корень / 'инструменты/удаленное_подключение_тест.py', '--kernel', тест_рабочая_область / 'kernel8.img',
                         '--access', Настройки_файл, '--output', результат], LOG_ЗАПИСЬ)
                проверить = json.loads((результат / 'report.json').read_text())
                assert проверить['passed']
                Отчет_ЗНАЧЕН['checks'].append(Название + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        Отчет_ЗНАЧЕН['passed'] = True
    finally:
        Отчет_ЗНАЧЕН['personal_settings_unchanged'] = личные_настройки.read_bytes() == 원래설정
        if not Отчет_ЗНАЧЕН['personal_settings_unchanged']:
            Отчет_ЗНАЧЕН['passed'] = False
        Отчет_ЗНАЧЕН['kernel_sha256'] = hashlib.sha256((задача_корень / 'build/kernel8.img').read_bytes()).hexdigest()
        (текстовыйВывод / 'report.json').write_text(json.dumps(Отчет_ЗНАЧЕН, ensure_ascii=False, indent=2) + '\n')
    assert Отчет_ЗНАЧЕН['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(Отчет_ЗНАЧЕН, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    запустить()
