#!/usr/bin/env python3
"""개인 пайваст_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from дурдаст_Танзимот import Омода_кардан
from COSL배포 import ҷои_таъинот_ном, китобхона

기준 = Path(__file__).resolve().parents[1]


def порча():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    танзимҳои_шахсӣ = 기준 / 'build/remote/access.json'
    원래설정 = танзимҳои_шахсӣ.read_bytes()
    гузориш_қимат = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Танзимот_масир = 시험터 / 'build/remote'
            Танзимот_масир.mkdir(parents=True)
            Танзимот_файл = Танзимот_масир / 'access.json'
            def навиштан_Танзимот(иттилоот):
                Танзимот_файл.write_text(json.dumps(иттилоот, ensure_ascii=False) + '\n')
                Танзимот_файл.chmod(0o600)
            def тасдиқ_кардан_Танзимот(восит, 화면):
                навиштан_Танзимот({'user': 'user', 'ssh_password': восит, 'vnc_password': 화면})
                원본 = Танзимот_файл.read_bytes()
                Омода_кардан(시험터)
                assert Танзимот_файл.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Танзимот_масир / 'Профил.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Танзимот_масир / 'Профил.h').stat().st_mode & 0o777 == 0o600
            for восит, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                тасдиқ_кардан_Танзимот(восит, 화면)
            гузориш_қимат['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for тағйир_додан_қимат, ворида_қимат in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                иттилоот = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                иттилоот.update(тағйир_додан_қимат)
                навиштан_Танзимот(иттилоот)
                try:
                    Омода_кардан(시험터)
                except SystemExit as Хато:
                    assert ворида_қимат in str(Хато), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ворида_қимат)
            гузориш_қимат['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Танзимот = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            васлгар = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Бойгонӣ_абзор = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def иҷро_кардан_фармон(인수, сабт_кардан_сабт):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=сабт_кардан_сабт,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Ном, восит, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Ном, flush=True)
                тасдиқ_кардан_Танзимот(восит, 화면)
                결과 = 출력 / Ном
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as сабт_кардан_сабт:
                    목적들 = []
                    for 원본 in sorted((기준 / 'дурдаст_қимат').glob('*.c')):
                        ҷои_таъинот_қимат = 시험터 / (원본.stem + '.o')
                        иҷро_кардан_фармон([번역기] + Танзимот + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Танзимот_масир, '-I', 기준 / 'дурдаст_қимат', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ҷои_таъинот_қимат], сабт_кардан_сабт)
                        목적들.append(ҷои_таъинот_қимат)
                    дурдаст_баста = 시험터 / 'libremote.a'
                    иҷро_кардан_фармон([Бойгонӣ_абзор, 'rcs', дурдаст_баста] + 목적들, сабт_кардан_сабт)
                    иҷро_кардан_фармон([васлгар, '--gc-sections', '-T', 기준 / '부팅/Пайванд_Тарҳбандӣ.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Ном + '.o') for Ном in ҷои_таъинот_ном] + ['--start-group'] +
                         [дурдаст_баста if масир == 'remote/libremote.a' else 기준 / 'build' / масир for масир in китобхона] + ['--end-group'], сабт_кардан_сабт)
                    иҷро_кардан_фармон([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], сабт_кардан_сабт)
                with (결과 / 'remote-test.log').open('wb') as сабт_кардан_сабт:
                    иҷро_кардан_фармон(['python3', 기준 / 'Абзорҳо/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Танзимот_файл, '--output', 결과], сабт_кардан_сабт)
                санҷидани_эътибор = json.loads((결과 / 'report.json').read_text())
                assert санҷидани_эътибор['passed']
                гузориш_қимат['checks'].append(Ном + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        гузориш_қимат['passed'] = True
    finally:
        гузориш_қимат['personal_settings_unchanged'] = танзимҳои_шахсӣ.read_bytes() == 원래설정
        if not гузориш_қимат['personal_settings_unchanged']:
            гузориш_қимат['passed'] = False
        гузориш_қимат['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(гузориш_қимат, ensure_ascii=False, indent=2) + '\n')
    assert гузориш_қимат['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(гузориш_қимат, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    порча()
