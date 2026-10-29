#!/usr/bin/env python3
"""개인 Ìsomọ́_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from Ìjìnnà_Àwọn_ààtò import gbaradì
from COSL배포 import èbúté_orúkọ, ibi_ìpamọ́

기준 = Path(__file__).resolve().parents[1]


def Rọ́ọ̀nù():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    ààtò_aládàáni = 기준 / 'build/remote/access.json'
    원래설정 = ààtò_aládàáni.read_bytes()
    ìjábọ̀_iye = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Àwọn_ààtò_ọ̀nà = 시험터 / 'build/remote'
            Àwọn_ààtò_ọ̀nà.mkdir(parents=True)
            Àwọn_ààtò_fáìlì = Àwọn_ààtò_ọ̀nà / 'access.json'
            def kọ_Àwọn_ààtò(détà):
                Àwọn_ààtò_fáìlì.write_text(json.dumps(détà, ensure_ascii=False) + '\n')
                Àwọn_ààtò_fáìlì.chmod(0o600)
            def ridájú_Àwọn_ààtò(ṣẹ́ẹ̀lì, 화면):
                kọ_Àwọn_ààtò({'user': 'user', 'ssh_password': ṣẹ́ẹ̀lì, 'vnc_password': 화면})
                원본 = Àwọn_ààtò_fáìlì.read_bytes()
                gbaradì(시험터)
                assert Àwọn_ààtò_fáìlì.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Àwọn_ààtò_ọ̀nà / 'Ìrísí_Olùlò.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Àwọn_ààtò_ọ̀nà / 'Ìrísí_Olùlò.h').stat().st_mode & 0o777 == 0o600
            for ṣẹ́ẹ̀lì, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ridájú_Àwọn_ààtò(ṣẹ́ẹ̀lì, 화면)
            ìjábọ̀_iye['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ṣàyípadà_iye, ìgbéwọlé_iye in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                détà = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                détà.update(ṣàyípadà_iye)
                kọ_Àwọn_ààtò(détà)
                try:
                    gbaradì(시험터)
                except SystemExit as àṣìṣe:
                    assert ìgbéwọlé_iye in str(àṣìṣe), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ìgbéwọlé_iye)
            ìjábọ̀_iye['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Àwọn_ààtò = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            olùsopọ̀ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ṣiṣẹ́_àṣẹ(인수, àkọsílẹ̀_ìṣe_ìlà_ìbú):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=àkọsílẹ̀_ìṣe_ìlà_ìbú,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Orúkọ, ṣẹ́ẹ̀lì, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Orúkọ, flush=True)
                ridájú_Àwọn_ààtò(ṣẹ́ẹ̀lì, 화면)
                결과 = 출력 / Orúkọ
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as àkọsílẹ̀_ìṣe_ìlà_ìbú:
                    목적들 = []
                    for 원본 in sorted((기준 / 'Ìjìnnà_iye').glob('*.c')):
                        èbúté_iye = 시험터 / (원본.stem + '.o')
                        ṣiṣẹ́_àṣẹ([번역기] + Àwọn_ààtò + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Àwọn_ààtò_ọ̀nà, '-I', 기준 / 'Ìjìnnà_iye', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', èbúté_iye], àkọsílẹ̀_ìṣe_ìlà_ìbú)
                        목적들.append(èbúté_iye)
                    Ìjìnnà_àkópọ̀ = 시험터 / 'libremote.a'
                    ṣiṣẹ́_àṣẹ([Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́, 'rcs', Ìjìnnà_àkópọ̀] + 목적들, àkọsílẹ̀_ìṣe_ìlà_ìbú)
                    ṣiṣẹ́_àṣẹ([olùsopọ̀, '--gc-sections', '-T', 기준 / '부팅/ṣàsopọ̀_ètò_ìrísí.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Orúkọ + '.o') for Orúkọ in èbúté_orúkọ] + ['--start-group'] +
                         [Ìjìnnà_àkópọ̀ if ọ̀nà == 'remote/libremote.a' else 기준 / 'build' / ọ̀nà for ọ̀nà in ibi_ìpamọ́] + ['--end-group'], àkọsílẹ̀_ìṣe_ìlà_ìbú)
                    ṣiṣẹ́_àṣẹ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], àkọsílẹ̀_ìṣe_ìlà_ìbú)
                with (결과 / 'remote-test.log').open('wb') as àkọsílẹ̀_ìṣe_ìlà_ìbú:
                    ṣiṣẹ́_àṣẹ(['python3', 기준 / 'Àwọn_irinṣẹ́/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Àwọn_ààtò_fáìlì, '--output', 결과], àkọsílẹ̀_ìṣe_ìlà_ìbú)
                ìfọwọ́síìwé = json.loads((결과 / 'report.json').read_text())
                assert ìfọwọ́síìwé['passed']
                ìjábọ̀_iye['checks'].append(Orúkọ + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ìjábọ̀_iye['passed'] = True
    finally:
        ìjábọ̀_iye['personal_settings_unchanged'] = ààtò_aládàáni.read_bytes() == 원래설정
        if not ìjábọ̀_iye['personal_settings_unchanged']:
            ìjábọ̀_iye['passed'] = False
        ìjábọ̀_iye['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(ìjábọ̀_iye, ensure_ascii=False, indent=2) + '\n')
    assert ìjábọ̀_iye['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ìjábọ̀_iye, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Rọ́ọ̀nù()
