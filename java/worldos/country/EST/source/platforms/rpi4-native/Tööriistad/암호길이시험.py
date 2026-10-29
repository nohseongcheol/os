#!/usr/bin/env python3
"""개인 ühendus_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from kauge_Sätted import Ettevalmistamine
from COSL배포 import sihtkoht_nimetus, teek

Project_juur = Path(__file__).resolve().parents[1]


def Käivita_2():
    Väljund = Project_juur / 'build/verification/password-length'
    Väljund.mkdir(parents=True, exist_ok=True)
    Isiklik_Sätted = Project_juur / 'build/remote/access.json'
    원래설정 = Isiklik_Sätted.read_bytes()
    aruanne_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Sätted_tee = 시험터 / 'build/remote'
            Sätted_tee.mkdir(parents=True)
            Sätted_Fail = Sätted_tee / 'access.json'
            def kirjutamine_Sätted(andmed):
                Sätted_Fail.write_text(json.dumps(andmed, ensure_ascii=False) + '\n')
                Sätted_Fail.chmod(0o600)
            def kinnitama_Sätted(kest, 화면):
                kirjutamine_Sätted({'user': 'user', 'ssh_password': kest, 'vnc_password': 화면})
                원본 = Sätted_Fail.read_bytes()
                Ettevalmistamine(시험터)
                assert Sätted_Fail.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Sätted_tee / 'Profiil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Sätted_tee / 'Profiil.h').stat().st_mode & 0o777 == 0o600
            for kest, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                kinnitama_Sätted(kest, 화면)
            aruanne_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for muutma_VALUE, kirje_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                andmed = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                andmed.update(muutma_VALUE)
                kirjutamine_Sätted(andmed)
                try:
                    Ettevalmistamine(시험터)
                except SystemExit as VIGA:
                    assert kirje_VALUE in str(VIGA), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + kirje_VALUE)
            aruanne_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Seaded = json.loads((Project_juur / 'build/remote/libassh-build.json').read_text())['flags']
            kompilaator_tööriist = os.environ.get('ARM64_CC', 'clang')
            liitmik = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arhiiv_tööriist = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Täida_käsk(Argumendid, LOG_kirje):
                subprocess.run(list(map(str, Argumendid)), cwd=str(Project_juur), stdout=LOG_kirje,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nimi_2, kest, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nimi_2, flush=True)
                kinnitama_Sätted(kest, 화면)
                TULEMUS = Väljund / Nimi_2
                TULEMUS.mkdir(exist_ok=True)
                with (TULEMUS / 'build.log').open('wb') as LOG_kirje:
                    목적들 = []
                    for 원본 in sorted((Project_juur / 'kauge_VALUE').glob('*.c')):
                        sihtkoht_VALUE = 시험터 / (원본.stem + '.o')
                        Täida_käsk([kompilaator_tööriist] + Seaded + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Sätted_tee, '-I', Project_juur / 'kauge_VALUE', '-I', Project_juur / 'vendor/libassh/src',
                             '-I', Project_juur / 'vendor/bearssl/inc', '-I', Project_juur / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', sihtkoht_VALUE], LOG_kirje)
                        목적들.append(sihtkoht_VALUE)
                    kauge_kogum = 시험터 / 'libremote.a'
                    Täida_käsk([Arhiiv_tööriist, 'rcs', kauge_kogum] + 목적들, LOG_kirje)
                    Täida_käsk([liitmik, '--gc-sections', '-T', Project_juur / '부팅/Link_küljend.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_juur / 'build' / (Nimi_2 + '.o') for Nimi_2 in sihtkoht_nimetus] + ['--start-group'] +
                         [kauge_kogum if RADA == 'remote/libremote.a' else Project_juur / 'build' / RADA for RADA in teek] + ['--end-group'], LOG_kirje)
                    Täida_käsk([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_kirje)
                with (TULEMUS / 'remote-test.log').open('wb') as LOG_kirje:
                    Täida_käsk(['python3', Project_juur / 'Tööriistad/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Sätted_Fail, '--output', TULEMUS], LOG_kirje)
                valideerima = json.loads((TULEMUS / 'report.json').read_text())
                assert valideerima['passed']
                aruanne_VALUE['checks'].append(Nimi_2 + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        aruanne_VALUE['passed'] = True
    finally:
        aruanne_VALUE['personal_settings_unchanged'] = Isiklik_Sätted.read_bytes() == 원래설정
        if not aruanne_VALUE['personal_settings_unchanged']:
            aruanne_VALUE['passed'] = False
        aruanne_VALUE['kernel_sha256'] = hashlib.sha256((Project_juur / 'build/kernel8.img').read_bytes()).hexdigest()
        (Väljund / 'report.json').write_text(json.dumps(aruanne_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert aruanne_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(aruanne_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Käivita_2()
