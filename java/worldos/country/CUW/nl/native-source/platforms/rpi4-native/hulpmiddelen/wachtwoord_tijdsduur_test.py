#!/usr/bin/env python3
"""개인 verbinding_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from extern_Instellingen import Bereid_voor
from COSL배포 import doel_naam, bibliotheek

Taken_wortel = Path(__file__).resolve().parents[1]


def starten():
    tekstuitvoer = Taken_wortel / 'build/verification/password-length'
    tekstuitvoer.mkdir(parents=True, exist_ok=True)
    persoonlijke_instellingen = Taken_wortel / 'build/remote/access.json'
    원래설정 = persoonlijke_instellingen.read_bytes()
    Rapport_WAARDE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            test_werkgebied = Path(임시)
            Instellingen_pad = test_werkgebied / 'build/remote'
            Instellingen_pad.mkdir(parents=True)
            Instellingen_Bestand = Instellingen_pad / 'access.json'
            def schrijven_Instellingen(gegevens):
                Instellingen_Bestand.write_text(json.dumps(gegevens, ensure_ascii=False) + '\n')
                Instellingen_Bestand.chmod(0o600)
            def bevestigen_Instellingen(Shell, scherm):
                schrijven_Instellingen({'user': 'user', 'ssh_password': Shell, 'vnc_password': scherm})
                원본 = Instellingen_Bestand.read_bytes()
                Bereid_voor(test_werkgebied)
                assert Instellingen_Bestand.read_bytes() == 원본, 'Settings were rewritten'
                kop_WAARDE = (Instellingen_pad / 'Profiel.h').read_text()
                일치 = re.search(r'scherm_wachtwoord\[\] = \{([^}]+)\}', kop_WAARDE)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Instellingen_pad / 'Profiel.h').stat().st_mode & 0o777 == 0o600
            for Shell, scherm in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                bevestigen_Instellingen(Shell, scherm)
            Rapport_WAARDE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for wijzigen_WAARDE, invoer_WAARDE_962f286b in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                gegevens = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                gegevens.update(wijzigen_WAARDE)
                schrijven_Instellingen(gegevens)
                try:
                    Bereid_voor(test_werkgebied)
                except SystemExit as fout:
                    assert invoer_WAARDE_962f286b in str(fout), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + invoer_WAARDE_962f286b)
            Rapport_WAARDE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Instellingen = json.loads((Taken_wortel / 'build/remote/libassh-build.json').read_text())['flags']
            compiler_hulpmiddel = os.environ.get('ARM64_CC', 'clang')
            connector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Archief_hulpmiddel = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Uitvoeren_opdracht(argumenten, LOG_RECORD):
                subprocess.run(list(map(str, argumenten)), cwd=str(Taken_wortel), stdout=LOG_RECORD,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Naam, Shell, scherm in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Naam, flush=True)
                bevestigen_Instellingen(Shell, scherm)
                resultaat = tekstuitvoer / Naam
                resultaat.mkdir(exist_ok=True)
                with (resultaat / 'build.log').open('wb') as LOG_RECORD:
                    목적들 = []
                    for 원본 in sorted((Taken_wortel / 'extern_WAARDE_28edcfa1').glob('*.c')):
                        doel_WAARDE = test_werkgebied / (원본.stem + '.o')
                        Uitvoeren_opdracht([compiler_hulpmiddel] + Instellingen + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Instellingen_pad, '-I', Taken_wortel / 'extern_WAARDE_28edcfa1', '-I', Taken_wortel / 'vendor/libassh/src',
                             '-I', Taken_wortel / 'vendor/bearssl/inc', '-I', Taken_wortel / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', doel_WAARDE], LOG_RECORD)
                        목적들.append(doel_WAARDE)
                    extern_bundel = test_werkgebied / 'libremote.a'
                    Uitvoeren_opdracht([Archief_hulpmiddel, 'rcs', extern_bundel] + 목적들, LOG_RECORD)
                    Uitvoeren_opdracht([connector, '--gc-sections', '-T', Taken_wortel / 'machineopstart/koppelindeling.ld', '-o', test_werkgebied / 'kernel.elf'] +
                         [Taken_wortel / 'build' / (Naam + '.o') for Naam in doel_naam] + ['--start-group'] +
                         [extern_bundel if pad == 'remote/libremote.a' else Taken_wortel / 'build' / pad for pad in bibliotheek] + ['--end-group'], LOG_RECORD)
                    Uitvoeren_opdracht([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         test_werkgebied / 'kernel.elf', test_werkgebied / 'kernel8.img'], LOG_RECORD)
                with (resultaat / 'remote-test.log').open('wb') as LOG_RECORD:
                    Uitvoeren_opdracht(['python3', Taken_wortel / 'hulpmiddelen/externe_verbinding_test.py', '--kernel', test_werkgebied / 'kernel8.img',
                         '--access', Instellingen_Bestand, '--output', resultaat], LOG_RECORD)
                valideren = json.loads((resultaat / 'report.json').read_text())
                assert valideren['passed']
                Rapport_WAARDE['checks'].append(Naam + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        Rapport_WAARDE['passed'] = True
    finally:
        Rapport_WAARDE['personal_settings_unchanged'] = persoonlijke_instellingen.read_bytes() == 원래설정
        if not Rapport_WAARDE['personal_settings_unchanged']:
            Rapport_WAARDE['passed'] = False
        Rapport_WAARDE['kernel_sha256'] = hashlib.sha256((Taken_wortel / 'build/kernel8.img').read_bytes()).hexdigest()
        (tekstuitvoer / 'report.json').write_text(json.dumps(Rapport_WAARDE, ensure_ascii=False, indent=2) + '\n')
    assert Rapport_WAARDE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(Rapport_WAARDE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    starten()
