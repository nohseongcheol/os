#!/usr/bin/env python3
"""개인 туташуу_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from алыскы_Орнотуулар import Даярдоо
from COSL배포 import көздөө_жайы_аты, жыйнак

기준 = Path(__file__).resolve().parents[1]


def Жүргүзүү():
    Чыгыш = 기준 / 'build/verification/password-length'
    Чыгыш.mkdir(parents=True, exist_ok=True)
    жеке_параметрлер = 기준 / 'build/remote/access.json'
    원래설정 = жеке_параметрлер.read_bytes()
    отчет_маани_ddf2aaf3 = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Орнотуулар_жол = 시험터 / 'build/remote'
            Орнотуулар_жол.mkdir(parents=True)
            Орнотуулар_файл = Орнотуулар_жол / 'access.json'
            def жазуу_Орнотуулар(берилмелер):
                Орнотуулар_файл.write_text(json.dumps(берилмелер, ensure_ascii=False) + '\n')
                Орнотуулар_файл.chmod(0o600)
            def тууралыгын_аныктоо_Орнотуулар(сырты, 화면):
                жазуу_Орнотуулар({'user': 'user', 'ssh_password': сырты, 'vnc_password': 화면})
                원본 = Орнотуулар_файл.read_bytes()
                Даярдоо(시험터)
                assert Орнотуулар_файл.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Орнотуулар_жол / 'Профиль.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Орнотуулар_жол / 'Профиль.h').stat().st_mode & 0o777 == 0o600
            for сырты, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                тууралыгын_аныктоо_Орнотуулар(сырты, 화면)
            отчет_маани_ddf2aaf3['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for өзгөртүү_маани, киргизме_жазуу_маани in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                берилмелер = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                берилмелер.update(өзгөртүү_маани)
                жазуу_Орнотуулар(берилмелер)
                try:
                    Даярдоо(시험터)
                except SystemExit as Ката:
                    assert киргизме_жазуу_маани in str(Ката), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + киргизме_жазуу_маани)
            отчет_маани_ddf2aaf3['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Орнотуулар = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            туташтыргыч = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Архив_курал = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def аткаруу_буйрук(인수, жазуу_катар):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=жазуу_катар,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Аты, сырты, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Аты, flush=True)
                тууралыгын_аныктоо_Орнотуулар(сырты, 화면)
                결과 = Чыгыш / Аты
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as жазуу_катар:
                    목적들 = []
                    for 원본 in sorted((기준 / 'алыскы_маани').glob('*.c')):
                        көздөө_жайы_маани = 시험터 / (원본.stem + '.o')
                        аткаруу_буйрук([번역기] + Орнотуулар + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Орнотуулар_жол, '-I', 기준 / 'алыскы_маани', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', көздөө_жайы_маани], жазуу_катар)
                        목적들.append(көздөө_жайы_маани)
                    алыскы_пакет = 시험터 / 'libremote.a'
                    аткаруу_буйрук([Архив_курал, 'rcs', алыскы_пакет] + 목적들, жазуу_катар)
                    аткаруу_буйрук([туташтыргыч, '--gc-sections', '-T', 기준 / '부팅/Шилтеме_түзүлүш.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Аты + '.o') for Аты in көздөө_жайы_аты] + ['--start-group'] +
                         [алыскы_пакет if ЖОЛ == 'remote/libremote.a' else 기준 / 'build' / ЖОЛ for ЖОЛ in жыйнак] + ['--end-group'], жазуу_катар)
                    аткаруу_буйрук([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], жазуу_катар)
                with (결과 / 'remote-test.log').open('wb') as жазуу_катар:
                    аткаруу_буйрук(['python3', 기준 / 'Куралдар/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Орнотуулар_файл, '--output', 결과], жазуу_катар)
                жарактуулугун_текшерүү = json.loads((결과 / 'report.json').read_text())
                assert жарактуулугун_текшерүү['passed']
                отчет_маани_ddf2aaf3['checks'].append(Аты + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        отчет_маани_ddf2aaf3['passed'] = True
    finally:
        отчет_маани_ddf2aaf3['personal_settings_unchanged'] = жеке_параметрлер.read_bytes() == 원래설정
        if not отчет_маани_ddf2aaf3['personal_settings_unchanged']:
            отчет_маани_ddf2aaf3['passed'] = False
        отчет_маани_ddf2aaf3['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (Чыгыш / 'report.json').write_text(json.dumps(отчет_маани_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    assert отчет_маани_ddf2aaf3['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(отчет_маани_ddf2aaf3, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Жүргүзүү()
