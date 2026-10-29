#!/usr/bin/env python3
"""개인 կապ_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from հեռակա_Կարգավորումներ import Պատրաստել
from COSL배포 import նպատակակետ_անուն, դարան

արձակել_արմատ = Path(__file__).resolve().parents[1]


def Գործարկել():
    Ելք = արձակել_արմատ / 'build/verification/password-length'
    Ելք.mkdir(parents=True, exist_ok=True)
    անձնական_կարգավորումներ = արձակել_արմատ / 'build/remote/access.json'
    원래설정 = անձնական_կարգավորումներ.read_bytes()
    զեկույց_արժեք = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Կարգավորումներ_ուղի = 시험터 / 'build/remote'
            Կարգավորումներ_ուղի.mkdir(parents=True)
            Կարգավորումներ_նիշք = Կարգավորումներ_ուղի / 'access.json'
            def գրել_Կարգավորումներ(տվյալ):
                Կարգավորումներ_նիշք.write_text(json.dumps(տվյալ, ensure_ascii=False) + '\n')
                Կարգավորումներ_նիշք.chmod(0o600)
            def հաստատել_Կարգավորումներ(խեցի, 화면):
                գրել_Կարգավորումներ({'user': 'user', 'ssh_password': խեցի, 'vnc_password': 화면})
                원본 = Կարգավորումներ_նիշք.read_bytes()
                Պատրաստել(시험터)
                assert Կարգավորումներ_նիշք.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Կարգավորումներ_ուղի / 'Հատկագիր.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Կարգավորումներ_ուղի / 'Հատկագիր.h').stat().st_mode & 0o777 == 0o600
            for խեցի, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                հաստատել_Կարգավորումներ(խեցի, 화면)
            զեկույց_արժեք['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for փոխել_արժեք, մուտքագրում_արժեք in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                տվյալ = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                տվյալ.update(փոխել_արժեք)
                գրել_Կարգավորումներ(տվյալ)
                try:
                    Պատրաստել(시험터)
                except SystemExit as Սխալ:
                    assert մուտքագրում_արժեք in str(Սխալ), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + մուտքագրում_արժեք)
            զեկույց_արժեք['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Նախընտրանքներ = json.loads((արձակել_արմատ / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Կապակցիչ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Պահոց_գործիք = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def կատարել_հրաման(인수, մատյան_տող):
                subprocess.run(list(map(str, 인수)), cwd=str(արձակել_արմատ), stdout=մատյան_տող,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Անուն, խեցի, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Անուն, flush=True)
                հաստատել_Կարգավորումներ(խեցի, 화면)
                չափ = Ելք / Անուն
                չափ.mkdir(exist_ok=True)
                with (չափ / 'build.log').open('wb') as մատյան_տող:
                    목적들 = []
                    for 원본 in sorted((արձակել_արմատ / 'հեռակա_արժեք').glob('*.c')):
                        նպատակակետ_արժեք = 시험터 / (원본.stem + '.o')
                        կատարել_հրաման([번역기] + Նախընտրանքներ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Կարգավորումներ_ուղի, '-I', արձակել_արմատ / 'հեռակա_արժեք', '-I', արձակել_արմատ / 'vendor/libassh/src',
                             '-I', արձակել_արմատ / 'vendor/bearssl/inc', '-I', արձակել_արմատ / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', նպատակակետ_արժեք], մատյան_տող)
                        목적들.append(նպատակակետ_արժեք)
                    հեռակա_փաթեթ = 시험터 / 'libremote.a'
                    կատարել_հրաման([Պահոց_գործիք, 'rcs', հեռակա_փաթեթ] + 목적들, մատյան_տող)
                    կատարել_հրաման([Կապակցիչ, '--gc-sections', '-T', արձակել_արմատ / '부팅/կապ_Դասավորություն.ld', '-o', 시험터 / 'kernel.elf'] +
                         [արձակել_արմատ / 'build' / (Անուն + '.o') for Անուն in նպատակակետ_անուն] + ['--start-group'] +
                         [հեռակա_փաթեթ if Ճանապարհ == 'remote/libremote.a' else արձակել_արմատ / 'build' / Ճանապարհ for Ճանապարհ in դարան] + ['--end-group'], մատյան_տող)
                    կատարել_հրաման([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], մատյան_տող)
                with (չափ / 'remote-test.log').open('wb') as մատյան_տող:
                    կատարել_հրաման(['python3', արձակել_արմատ / 'Գործիքներ/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Կարգավորումներ_նիշք, '--output', չափ], մատյան_տող)
                վավերացնել = json.loads((չափ / 'report.json').read_text())
                assert վավերացնել['passed']
                զեկույց_արժեք['checks'].append(Անուն + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        զեկույց_արժեք['passed'] = True
    finally:
        զեկույց_արժեք['personal_settings_unchanged'] = անձնական_կարգավորումներ.read_bytes() == 원래설정
        if not զեկույց_արժեք['personal_settings_unchanged']:
            զեկույց_արժեք['passed'] = False
        զեկույց_արժեք['kernel_sha256'] = hashlib.sha256((արձակել_արմատ / 'build/kernel8.img').read_bytes()).hexdigest()
        (Ելք / 'report.json').write_text(json.dumps(զեկույց_արժեք, ensure_ascii=False, indent=2) + '\n')
    assert զեկույց_արժեք['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(զեկույց_արժեք, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Գործարկել()
