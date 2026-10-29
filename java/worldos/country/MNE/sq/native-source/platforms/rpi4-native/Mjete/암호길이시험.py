#!/usr/bin/env python3
"""개인 lidhje_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from në_largësi_cilësimet import Përgatit
from COSL배포 import vendmbërritje_emër, bibliotekë

Project_rrënjë = Path(__file__).resolve().parents[1]


def Ekzekuto():
    출력 = Project_rrënjë / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    Parametrim_personal = Project_rrënjë / 'build/remote/access.json'
    원래설정 = Parametrim_personal.read_bytes()
    raport_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            cilësimet_shteg = 시험터 / 'build/remote'
            cilësimet_shteg.mkdir(parents=True)
            cilësimet_skedar = cilësimet_shteg / 'access.json'
            def shkruaj_cilësimet(të_dhëna):
                cilësimet_skedar.write_text(json.dumps(të_dhëna, ensure_ascii=False) + '\n')
                cilësimet_skedar.chmod(0o600)
            def verifikoj_cilësimet(pasues, 화면):
                shkruaj_cilësimet({'user': 'user', 'ssh_password': pasues, 'vnc_password': 화면})
                원본 = cilësimet_skedar.read_bytes()
                Përgatit(시험터)
                assert cilësimet_skedar.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (cilësimet_shteg / 'profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (cilësimet_shteg / 'profil.h').stat().st_mode & 0o777 == 0o600
            for pasues, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verifikoj_cilësimet(pasues, 화면)
            raport_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ndryshoj_VALUE, futje_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                të_dhëna = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                të_dhëna.update(ndryshoj_VALUE)
                shkruaj_cilësimet(të_dhëna)
                try:
                    Përgatit(시험터)
                except SystemExit as GABIM:
                    assert futje_VALUE in str(GABIM), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + futje_VALUE)
            raport_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Rregullime = json.loads((Project_rrënjë / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            bashkues = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            arkiv_vegël = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def zbatoj_komandë(Argumente, LOG_RECORD):
                subprocess.run(list(map(str, Argumente)), cwd=str(Project_rrënjë), stdout=LOG_RECORD,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Emër, pasues, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Emër, flush=True)
                verifikoj_cilësimet(pasues, 화면)
                llogaritje = 출력 / Emër
                llogaritje.mkdir(exist_ok=True)
                with (llogaritje / 'build.log').open('wb') as LOG_RECORD:
                    목적들 = []
                    for 원본 in sorted((Project_rrënjë / 'në_largësi_VALUE').glob('*.c')):
                        vendmbërritje_VALUE = 시험터 / (원본.stem + '.o')
                        zbatoj_komandë([번역기] + Rregullime + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', cilësimet_shteg, '-I', Project_rrënjë / 'në_largësi_VALUE', '-I', Project_rrënjë / 'vendor/libassh/src',
                             '-I', Project_rrënjë / 'vendor/bearssl/inc', '-I', Project_rrënjë / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', vendmbërritje_VALUE], LOG_RECORD)
                        목적들.append(vendmbërritje_VALUE)
                    në_largësi_grupoj = 시험터 / 'libremote.a'
                    zbatoj_komandë([arkiv_vegël, 'rcs', në_largësi_grupoj] + 목적들, LOG_RECORD)
                    zbatoj_komandë([bashkues, '--gc-sections', '-T', Project_rrënjë / '부팅/lidh_Navigimi.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_rrënjë / 'build' / (Emër + '.o') for Emër in vendmbërritje_emër] + ['--start-group'] +
                         [në_largësi_grupoj if POZICIONI == 'remote/libremote.a' else Project_rrënjë / 'build' / POZICIONI for POZICIONI in bibliotekë] + ['--end-group'], LOG_RECORD)
                    zbatoj_komandë([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_RECORD)
                with (llogaritje / 'remote-test.log').open('wb') as LOG_RECORD:
                    zbatoj_komandë(['python3', Project_rrënjë / 'Mjete/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', cilësimet_skedar, '--output', llogaritje], LOG_RECORD)
                vlerësoj = json.loads((llogaritje / 'report.json').read_text())
                assert vlerësoj['passed']
                raport_VALUE['checks'].append(Emër + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        raport_VALUE['passed'] = True
    finally:
        raport_VALUE['personal_settings_unchanged'] = Parametrim_personal.read_bytes() == 원래설정
        if not raport_VALUE['personal_settings_unchanged']:
            raport_VALUE['passed'] = False
        raport_VALUE['kernel_sha256'] = hashlib.sha256((Project_rrënjë / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(raport_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert raport_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(raport_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Ekzekuto()
