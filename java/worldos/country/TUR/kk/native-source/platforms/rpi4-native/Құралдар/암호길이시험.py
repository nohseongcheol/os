#!/usr/bin/env python3
"""개인 қосылым_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from 원격설정 import Дайындау
from COSL배포 import тағайындау_аты, кітапхана

жоба_түбір = Path(__file__).resolve().parents[1]


def Орындау_2():
    Шығысы = жоба_түбір / 'build/verification/password-length'
    Шығысы.mkdir(parents=True, exist_ok=True)
    жеке_параметрлер = жоба_түбір / 'build/remote/access.json'
    원래설정 = жеке_параметрлер.read_bytes()
    есеп_мән = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Параметрлер_жол = 시험터 / 'build/remote'
            Параметрлер_жол.mkdir(parents=True)
            Параметрлер_файл = Параметрлер_жол / 'access.json'
            def жазу_Параметрлер(деректер):
                Параметрлер_файл.write_text(json.dumps(деректер, ensure_ascii=False) + '\n')
                Параметрлер_файл.chmod(0o600)
            def тексеру_Параметрлер(қоршам, 화면):
                жазу_Параметрлер({'user': 'user', 'ssh_password': қоршам, 'vnc_password': 화면})
                원본 = Параметрлер_файл.read_bytes()
                Дайындау(시험터)
                assert Параметрлер_файл.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Параметрлер_жол / 'Профиль.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Параметрлер_жол / 'Профиль.h').stat().st_mode & 0o777 == 0o600
            for қоршам, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                тексеру_Параметрлер(қоршам, 화면)
            есеп_мән['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for өзгерту_мән, енгізу_мән in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                деректер = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                деректер.update(өзгерту_мән)
                жазу_Параметрлер(деректер)
                try:
                    Дайындау(시험터)
                except SystemExit as Қате:
                    assert енгізу_мән in str(Қате), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + енгізу_мән)
            есеп_мән['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Баптаулар = json.loads((жоба_түбір / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Қосқыш = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Мұрағат_құрал = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def орындау_пәрмен(Аргументтер, журнал_жол):
                subprocess.run(list(map(str, Аргументтер)), cwd=str(жоба_түбір), stdout=журнал_жол,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Аты, қоршам, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Аты, flush=True)
                тексеру_Параметрлер(қоршам, 화면)
                НӘТИЖЕ = Шығысы / Аты
                НӘТИЖЕ.mkdir(exist_ok=True)
                with (НӘТИЖЕ / 'build.log').open('wb') as журнал_жол:
                    목적들 = []
                    for 원본 in sorted((жоба_түбір / '원격').glob('*.c')):
                        тағайындау_мән = 시험터 / (원본.stem + '.o')
                        орындау_пәрмен([번역기] + Баптаулар + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Параметрлер_жол, '-I', жоба_түбір / '원격', '-I', жоба_түбір / 'vendor/libassh/src',
                             '-I', жоба_түбір / 'vendor/bearssl/inc', '-I', жоба_түбір / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', тағайындау_мән], журнал_жол)
                        목적들.append(тағайындау_мән)
                    원격묶음 = 시험터 / 'libremote.a'
                    орындау_пәрмен([Мұрағат_құрал, 'rcs', 원격묶음] + 목적들, журнал_жол)
                    орындау_пәрмен([Қосқыш, '--gc-sections', '-T', жоба_түбір / '부팅/Cілтеме_макет.ld', '-o', 시험터 / 'kernel.elf'] +
                         [жоба_түбір / 'build' / (Аты + '.o') for Аты in тағайындау_аты] + ['--start-group'] +
                         [원격묶음 if Жол_2 == 'remote/libremote.a' else жоба_түбір / 'build' / Жол_2 for Жол_2 in кітапхана] + ['--end-group'], журнал_жол)
                    орындау_пәрмен([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], журнал_жол)
                with (НӘТИЖЕ / 'remote-test.log').open('wb') as журнал_жол:
                    орындау_пәрмен(['python3', жоба_түбір / 'Құралдар/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Параметрлер_файл, '--output', НӘТИЖЕ], журнал_жол)
                тексеру_5fb2b747 = json.loads((НӘТИЖЕ / 'report.json').read_text())
                assert тексеру_5fb2b747['passed']
                есеп_мән['checks'].append(Аты + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        есеп_мән['passed'] = True
    finally:
        есеп_мән['personal_settings_unchanged'] = жеке_параметрлер.read_bytes() == 원래설정
        if not есеп_мән['personal_settings_unchanged']:
            есеп_мән['passed'] = False
        есеп_мән['kernel_sha256'] = hashlib.sha256((жоба_түбір / 'build/kernel8.img').read_bytes()).hexdigest()
        (Шығысы / 'report.json').write_text(json.dumps(есеп_мән, ensure_ascii=False, indent=2) + '\n')
    assert есеп_мән['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(есеп_мән, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Орындау_2()
