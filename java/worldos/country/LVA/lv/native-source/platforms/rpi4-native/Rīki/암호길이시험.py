#!/usr/bin/env python3
"""개인 paziņa_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from attāls_Iestatījumi import Sagatavot
from COSL배포 import mērķis_nosaukums, bibliotēka

Project_sakne = Path(__file__).resolve().parents[1]


def Palaist():
    Izvade = Project_sakne / 'build/verification/password-length'
    Izvade.mkdir(parents=True, exist_ok=True)
    Personisks_Iestatījumi = Project_sakne / 'build/remote/access.json'
    원래설정 = Personisks_Iestatījumi.read_bytes()
    ziņot_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Iestatījumi_ceļš = 시험터 / 'build/remote'
            Iestatījumi_ceļš.mkdir(parents=True)
            Iestatījumi_Fails = Iestatījumi_ceļš / 'access.json'
            def rakstīšana_Iestatījumi(dati):
                Iestatījumi_Fails.write_text(json.dumps(dati, ensure_ascii=False) + '\n')
                Iestatījumi_Fails.chmod(0o600)
            def verificēt_Iestatījumi(čaula, 화면):
                rakstīšana_Iestatījumi({'user': 'user', 'ssh_password': čaula, 'vnc_password': 화면})
                원본 = Iestatījumi_Fails.read_bytes()
                Sagatavot(시험터)
                assert Iestatījumi_Fails.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Iestatījumi_ceļš / 'Profils.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Iestatījumi_ceļš / 'Profils.h').stat().st_mode & 0o777 == 0o600
            for čaula, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verificēt_Iestatījumi(čaula, 화면)
            ziņot_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for mainīt_VALUE, ievade_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                dati = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                dati.update(mainīt_VALUE)
                rakstīšana_Iestatījumi(dati)
                try:
                    Sagatavot(시험터)
                except SystemExit as Kļūda:
                    assert ievade_VALUE in str(Kļūda), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ievade_VALUE)
            ziņot_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Uzstādījumi = json.loads((Project_sakne / 'build/remote/libassh-build.json').read_text())['flags']
            kompilators_rīks = os.environ.get('ARM64_CC', 'clang')
            Savienotājs = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arhīvs_rīks = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Izpildīt_komanda(Parametri, LOG_RECORD):
                subprocess.run(list(map(str, Parametri)), cwd=str(Project_sakne), stdout=LOG_RECORD,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nosaukums, čaula, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nosaukums, flush=True)
                verificēt_Iestatījumi(čaula, 화면)
                mērs = Izvade / Nosaukums
                mērs.mkdir(exist_ok=True)
                with (mērs / 'build.log').open('wb') as LOG_RECORD:
                    목적들 = []
                    for 원본 in sorted((Project_sakne / 'attāls_VALUE').glob('*.c')):
                        mērķis_VALUE = 시험터 / (원본.stem + '.o')
                        Izpildīt_komanda([kompilators_rīks] + Uzstādījumi + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Iestatījumi_ceļš, '-I', Project_sakne / 'attāls_VALUE', '-I', Project_sakne / 'vendor/libassh/src',
                             '-I', Project_sakne / 'vendor/bearssl/inc', '-I', Project_sakne / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', mērķis_VALUE], LOG_RECORD)
                        목적들.append(mērķis_VALUE)
                    attāls_saistīt = 시험터 / 'libremote.a'
                    Izpildīt_komanda([Arhīvs_rīks, 'rcs', attāls_saistīt] + 목적들, LOG_RECORD)
                    Izpildīt_komanda([Savienotājs, '--gc-sections', '-T', Project_sakne / '부팅/Saite_shēma.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_sakne / 'build' / (Nosaukums + '.o') for Nosaukums in mērķis_nosaukums] + ['--start-group'] +
                         [attāls_saistīt if CEĻŠ == 'remote/libremote.a' else Project_sakne / 'build' / CEĻŠ for CEĻŠ in bibliotēka] + ['--end-group'], LOG_RECORD)
                    Izpildīt_komanda([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_RECORD)
                with (mērs / 'remote-test.log').open('wb') as LOG_RECORD:
                    Izpildīt_komanda(['python3', Project_sakne / 'Rīki/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Iestatījumi_Fails, '--output', mērs], LOG_RECORD)
                validēt = json.loads((mērs / 'report.json').read_text())
                assert validēt['passed']
                ziņot_VALUE['checks'].append(Nosaukums + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ziņot_VALUE['passed'] = True
    finally:
        ziņot_VALUE['personal_settings_unchanged'] = Personisks_Iestatījumi.read_bytes() == 원래설정
        if not ziņot_VALUE['personal_settings_unchanged']:
            ziņot_VALUE['passed'] = False
        ziņot_VALUE['kernel_sha256'] = hashlib.sha256((Project_sakne / 'build/kernel8.img').read_bytes()).hexdigest()
        (Izvade / 'report.json').write_text(json.dumps(ziņot_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert ziņot_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ziņot_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Palaist()
