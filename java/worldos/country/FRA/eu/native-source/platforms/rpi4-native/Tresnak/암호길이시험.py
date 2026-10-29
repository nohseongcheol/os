#!/usr/bin/env python3
"""개인 konexio_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urruneko_Ezarpenak import 준비
from COSL배포 import helburu_izen, liburutegi

Project_erro = Path(__file__).resolve().parents[1]


def Exekutatu_2():
    Irteera = Project_erro / 'build/verification/password-length'
    Irteera.mkdir(parents=True, exist_ok=True)
    ezarpen_pertsonalak = Project_erro / 'build/remote/access.json'
    원래설정 = ezarpen_pertsonalak.read_bytes()
    txosten_balio = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Ezarpenak_bide_izen = 시험터 / 'build/remote'
            Ezarpenak_bide_izen.mkdir(parents=True)
            Ezarpenak_fitxategi = Ezarpenak_bide_izen / 'access.json'
            def idatzi_Ezarpenak(datuak):
                Ezarpenak_fitxategi.write_text(json.dumps(datuak, ensure_ascii=False) + '\n')
                Ezarpenak_fitxategi.chmod(0o600)
            def egiaztatu_Ezarpenak(shell, 화면):
                idatzi_Ezarpenak({'user': 'user', 'ssh_password': shell, 'vnc_password': 화면})
                원본 = Ezarpenak_fitxategi.read_bytes()
                준비(시험터)
                assert Ezarpenak_fitxategi.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Ezarpenak_bide_izen / 'profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Ezarpenak_bide_izen / 'profil.h').stat().st_mode & 0o777 == 0o600
            for shell, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                egiaztatu_Ezarpenak(shell, 화면)
            txosten_balio['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for aldatu_balio, sarrera_balio in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                datuak = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                datuak.update(aldatu_balio)
                idatzi_Ezarpenak(datuak)
                try:
                    준비(시험터)
                except SystemExit as errorea:
                    assert sarrera_balio in str(errorea), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + sarrera_balio)
            txosten_balio['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Ezarpenak = json.loads((Project_erro / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            konektore = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            artxibo_tresna = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def exekutatu_komando(Argumentuak, LOG_marka):
                subprocess.run(list(map(str, Argumentuak)), cwd=str(Project_erro), stdout=LOG_marka,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Izena, shell, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Izena, flush=True)
                egiaztatu_Ezarpenak(shell, 화면)
                EMAITZA = Irteera / Izena
                EMAITZA.mkdir(exist_ok=True)
                with (EMAITZA / 'build.log').open('wb') as LOG_marka:
                    목적들 = []
                    for 원본 in sorted((Project_erro / 'urruneko_balio').glob('*.c')):
                        helburu_balio_a0fbc067 = 시험터 / (원본.stem + '.o')
                        exekutatu_komando([번역기] + Ezarpenak + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Ezarpenak_bide_izen, '-I', Project_erro / 'urruneko_balio', '-I', Project_erro / 'vendor/libassh/src',
                             '-I', Project_erro / 'vendor/bearssl/inc', '-I', Project_erro / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', helburu_balio_a0fbc067], LOG_marka)
                        목적들.append(helburu_balio_a0fbc067)
                    urruneko_multzo = 시험터 / 'libremote.a'
                    exekutatu_komando([artxibo_tresna, 'rcs', urruneko_multzo] + 목적들, LOG_marka)
                    exekutatu_komando([konektore, '--gc-sections', '-T', Project_erro / '부팅/lotu_diseinu.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_erro / 'build' / (Izena + '.o') for Izena in helburu_izen] + ['--start-group'] +
                         [urruneko_multzo if Bide_izena == 'remote/libremote.a' else Project_erro / 'build' / Bide_izena for Bide_izena in liburutegi] + ['--end-group'], LOG_marka)
                    exekutatu_komando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_marka)
                with (EMAITZA / 'remote-test.log').open('wb') as LOG_marka:
                    exekutatu_komando(['python3', Project_erro / 'Tresnak/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Ezarpenak_fitxategi, '--output', EMAITZA], LOG_marka)
                baliozkotu = json.loads((EMAITZA / 'report.json').read_text())
                assert baliozkotu['passed']
                txosten_balio['checks'].append(Izena + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        txosten_balio['passed'] = True
    finally:
        txosten_balio['personal_settings_unchanged'] = ezarpen_pertsonalak.read_bytes() == 원래설정
        if not txosten_balio['personal_settings_unchanged']:
            txosten_balio['passed'] = False
        txosten_balio['kernel_sha256'] = hashlib.sha256((Project_erro / 'build/kernel8.img').read_bytes()).hexdigest()
        (Irteera / 'report.json').write_text(json.dumps(txosten_balio, ensure_ascii=False, indent=2) + '\n')
    assert txosten_balio['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(txosten_balio, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Exekutatu_2()
