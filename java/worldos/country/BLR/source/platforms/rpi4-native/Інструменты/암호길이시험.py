#!/usr/bin/env python3
"""개인 кантакт_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from аддалены_Налады import Падрыхтаваць
from COSL배포 import прызначэнне_імя, бібліятэка

기준 = Path(__file__).resolve().parents[1]


def Выканаць():
    Выхад = 기준 / 'build/verification/password-length'
    Выхад.mkdir(parents=True, exist_ok=True)
    асабістыя_налады = 기준 / 'build/remote/access.json'
    원래설정 = асабістыя_налады.read_bytes()
    справаздача_значэнне = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Налады_шлях = 시험터 / 'build/remote'
            Налады_шлях.mkdir(parents=True)
            Налады_файл = Налады_шлях / 'access.json'
            def напісаць_Налады(дадзеныя):
                Налады_файл.write_text(json.dumps(дадзеныя, ensure_ascii=False) + '\n')
                Налады_файл.chmod(0o600)
            def праверыць_Налады(абалонка, 화면):
                напісаць_Налады({'user': 'user', 'ssh_password': абалонка, 'vnc_password': 화면})
                원본 = Налады_файл.read_bytes()
                Падрыхтаваць(시험터)
                assert Налады_файл.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Налады_шлях / 'Профіль.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Налады_шлях / 'Профіль.h').stat().st_mode & 0o777 == 0o600
            for абалонка, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                праверыць_Налады(абалонка, 화면)
            справаздача_значэнне['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for змяніць_значэнне, увядзенне_значэнне in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                дадзеныя = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                дадзеныя.update(змяніць_значэнне)
                напісаць_Налады(дадзеныя)
                try:
                    Падрыхтаваць(시험터)
                except SystemExit as ПАМЫЛКА:
                    assert увядзенне_значэнне in str(ПАМЫЛКА), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + увядзенне_значэнне)
            справаздача_значэнне['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Усталёўкі = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            злучальнік = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Архіў_інструмент = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def выканаць_каманда(인수, журнал_запіс):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=журнал_запіс,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Назва, абалонка, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Назва, flush=True)
                праверыць_Налады(абалонка, 화면)
                결과 = Выхад / Назва
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as журнал_запіс:
                    목적들 = []
                    for 원본 in sorted((기준 / 'аддалены_значэнне').glob('*.c')):
                        прызначэнне_значэнне_a0fbc067 = 시험터 / (원본.stem + '.o')
                        выканаць_каманда([번역기] + Усталёўкі + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Налады_шлях, '-I', 기준 / 'аддалены_значэнне', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', прызначэнне_значэнне_a0fbc067], журнал_запіс)
                        목적들.append(прызначэнне_значэнне_a0fbc067)
                    аддалены_пакет = 시험터 / 'libremote.a'
                    выканаць_каманда([Архіў_інструмент, 'rcs', аддалены_пакет] + 목적들, журнал_запіс)
                    выканаць_каманда([злучальнік, '--gc-sections', '-T', 기준 / '부팅/сувязь_Макет.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Назва + '.o') for Назва in прызначэнне_імя] + ['--start-group'] +
                         [аддалены_пакет if ШЛЯХ == 'remote/libremote.a' else 기준 / 'build' / ШЛЯХ for ШЛЯХ in бібліятэка] + ['--end-group'], журнал_запіс)
                    выканаць_каманда([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], журнал_запіс)
                with (결과 / 'remote-test.log').open('wb') as журнал_запіс:
                    выканаць_каманда(['python3', 기준 / 'Інструменты/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Налады_файл, '--output', 결과], журнал_запіс)
                праверыць_5fb2b747 = json.loads((결과 / 'report.json').read_text())
                assert праверыць_5fb2b747['passed']
                справаздача_значэнне['checks'].append(Назва + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        справаздача_значэнне['passed'] = True
    finally:
        справаздача_значэнне['personal_settings_unchanged'] = асабістыя_налады.read_bytes() == 원래설정
        if not справаздача_значэнне['personal_settings_unchanged']:
            справаздача_значэнне['passed'] = False
        справаздача_значэнне['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (Выхад / 'report.json').write_text(json.dumps(справаздача_значэнне, ensure_ascii=False, indent=2) + '\n')
    assert справаздача_значэнне['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(справаздача_значэнне, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Выканаць()
