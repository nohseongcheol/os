#!/usr/bin/env python3
"""개인 тоташу_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from читтәге_Параметрлар import Әзерләү
from COSL배포 import күчерү_урыны_исем, библиотека

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]


def эшләтү():
    출력 = экранга_җибәрү_тамыр / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    шәхси_көйләнмәләр = экранга_җибәрү_тамыр / 'build/remote/access.json'
    원래설정 = шәхси_көйләнмәләр.read_bytes()
    отчет_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Параметрлар_юл = 시험터 / 'build/remote'
            Параметрлар_юл.mkdir(parents=True)
            Параметрлар_файл = Параметрлар_юл / 'access.json'
            def язу_Параметрлар(мәгълүмат):
                Параметрлар_файл.write_text(json.dumps(мәгълүмат, ensure_ascii=False) + '\n')
                Параметрлар_файл.chmod(0o600)
            def раслау_Параметрлар(тышча, 화면):
                язу_Параметрлар({'user': 'user', 'ssh_password': тышча, 'vnc_password': 화면})
                원본 = Параметрлар_файл.read_bytes()
                Әзерләү(시험터)
                assert Параметрлар_файл.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Параметрлар_юл / 'Профиль.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Параметрлар_юл / 'Профиль.h').stat().st_mode & 0o777 == 0o600
            for тышча, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                раслау_Параметрлар(тышча, 화면)
            отчет_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for үзгәртү_VALUE, кертү_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                мәгълүмат = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                мәгълүмат.update(үзгәртү_VALUE)
                язу_Параметрлар(мәгълүмат)
                try:
                    Әзерләү(시험터)
                except SystemExit as Хата:
                    assert кертү_VALUE in str(Хата), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + кертү_VALUE)
            отчет_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Caylaw = json.loads((экранга_җибәрү_тамыр / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            бәйләүче = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Архив_чара = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def үтәргә_команда(인수, LOG_юл):
                subprocess.run(list(map(str, 인수)), cwd=str(экранга_җибәрү_тамыр), stdout=LOG_юл,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for исем, тышча, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + исем, flush=True)
                раслау_Параметрлар(тышча, 화면)
                үлчәм = 출력 / исем
                үлчәм.mkdir(exist_ok=True)
                with (үлчәм / 'build.log').open('wb') as LOG_юл:
                    목적들 = []
                    for 원본 in sorted((экранга_җибәрү_тамыр / 'читтәге_VALUE').glob('*.c')):
                        күчерү_урыны_VALUE = 시험터 / (원본.stem + '.o')
                        үтәргә_команда([번역기] + Caylaw + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Параметрлар_юл, '-I', экранга_җибәрү_тамыр / 'читтәге_VALUE', '-I', экранга_җибәрү_тамыр / 'vendor/libassh/src',
                             '-I', экранга_җибәрү_тамыр / 'vendor/bearssl/inc', '-I', экранга_җибәрү_тамыр / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', күчерү_урыны_VALUE], LOG_юл)
                        목적들.append(күчерү_урыны_VALUE)
                    читтәге_пакет = 시험터 / 'libremote.a'
                    үтәргә_команда([Архив_чара, 'rcs', читтәге_пакет] + 목적들, LOG_юл)
                    үтәргә_команда([бәйләүче, '--gc-sections', '-T', экранга_җибәрү_тамыр / '부팅/бәйләү_план.ld', '-o', 시험터 / 'kernel.elf'] +
                         [экранга_җибәрү_тамыр / 'build' / (исем + '.o') for исем in күчерү_урыны_исем] + ['--start-group'] +
                         [читтәге_пакет if Yul == 'remote/libremote.a' else экранга_җибәрү_тамыр / 'build' / Yul for Yul in библиотека] + ['--end-group'], LOG_юл)
                    үтәргә_команда([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_юл)
                with (үлчәм / 'remote-test.log').open('wb') as LOG_юл:
                    үтәргә_команда(['python3', экранга_җибәрү_тамыр / 'Кораллар/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Параметрлар_файл, '--output', үлчәм], LOG_юл)
                тикшерү = json.loads((үлчәм / 'report.json').read_text())
                assert тикшерү['passed']
                отчет_VALUE['checks'].append(исем + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        отчет_VALUE['passed'] = True
    finally:
        отчет_VALUE['personal_settings_unchanged'] = шәхси_көйләнмәләр.read_bytes() == 원래설정
        if not отчет_VALUE['personal_settings_unchanged']:
            отчет_VALUE['passed'] = False
        отчет_VALUE['kernel_sha256'] = hashlib.sha256((экранга_җибәрү_тамыр / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(отчет_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert отчет_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(отчет_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    эшләтү()
