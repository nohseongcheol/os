#!/usr/bin/env python3
"""개인 connessione_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from remoto_Impostazioni import Prepara
from COSL배포 import meta_nome, Catalogo

azione_radice = Path(__file__).resolve().parents[1]


def avvia():
    uscitaTesto = azione_radice / 'build/verification/password-length'
    uscitaTesto.mkdir(parents=True, exist_ok=True)
    impostazioni_personali = azione_radice / 'build/remote/access.json'
    원래설정 = impostazioni_personali.read_bytes()
    Report_VALORE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            test_area_di_lavoro = Path(임시)
            Impostazioni_percorso = test_area_di_lavoro / 'build/remote'
            Impostazioni_percorso.mkdir(parents=True)
            Impostazioni_File = Impostazioni_percorso / 'access.json'
            def scrivere_Impostazioni(dati):
                Impostazioni_File.write_text(json.dumps(dati, ensure_ascii=False) + '\n')
                Impostazioni_File.chmod(0o600)
            def verificare_Impostazioni(Shell, schermata):
                scrivere_Impostazioni({'user': 'user', 'ssh_password': Shell, 'vnc_password': schermata})
                원본 = Impostazioni_File.read_bytes()
                Prepara(test_area_di_lavoro)
                assert Impostazioni_File.read_bytes() == 원본, 'Settings were rewritten'
                intestazione_VALORE = (Impostazioni_percorso / 'Profilo.h').read_text()
                일치 = re.search(r'schermata_password\[\] = \{([^}]+)\}', intestazione_VALORE)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Impostazioni_percorso / 'Profilo.h').stat().st_mode & 0o777 == 0o600
            for Shell, schermata in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verificare_Impostazioni(Shell, schermata)
            Report_VALORE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for cambiare_VALORE, voce_VALORE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                dati = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                dati.update(cambiare_VALORE)
                scrivere_Impostazioni(dati)
                try:
                    Prepara(test_area_di_lavoro)
                except SystemExit as errore:
                    assert voce_VALORE in str(errore), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + voce_VALORE)
            Report_VALORE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Impostazioni = json.loads((azione_radice / 'build/remote/libassh-build.json').read_text())['flags']
            compilatore_strumento = os.environ.get('ARM64_CC', 'clang')
            Connettore = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Archivio_strumento = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Esegui_comando(argomenti, LOG_riga):
                subprocess.run(list(map(str, argomenti)), cwd=str(azione_radice), stdout=LOG_riga,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nome, Shell, schermata in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nome, flush=True)
                verificare_Impostazioni(Shell, schermata)
                risultato = uscitaTesto / Nome
                risultato.mkdir(exist_ok=True)
                with (risultato / 'build.log').open('wb') as LOG_riga:
                    목적들 = []
                    for 원본 in sorted((azione_radice / 'remoto_VALORE').glob('*.c')):
                        meta_VALORE = test_area_di_lavoro / (원본.stem + '.o')
                        Esegui_comando([compilatore_strumento] + Impostazioni + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Impostazioni_percorso, '-I', azione_radice / 'remoto_VALORE', '-I', azione_radice / 'vendor/libassh/src',
                             '-I', azione_radice / 'vendor/bearssl/inc', '-I', azione_radice / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', meta_VALORE], LOG_riga)
                        목적들.append(meta_VALORE)
                    remoto_aggregare = test_area_di_lavoro / 'libremote.a'
                    Esegui_comando([Archivio_strumento, 'rcs', remoto_aggregare] + 목적들, LOG_riga)
                    Esegui_comando([Connettore, '--gc-sections', '-T', azione_radice / 'avvio_macchina/disposizione_di_collegamento.ld', '-o', test_area_di_lavoro / 'kernel.elf'] +
                         [azione_radice / 'build' / (Nome + '.o') for Nome in meta_nome] + ['--start-group'] +
                         [remoto_aggregare if percorso == 'remote/libremote.a' else azione_radice / 'build' / percorso for percorso in Catalogo] + ['--end-group'], LOG_riga)
                    Esegui_comando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         test_area_di_lavoro / 'kernel.elf', test_area_di_lavoro / 'kernel8.img'], LOG_riga)
                with (risultato / 'remote-test.log').open('wb') as LOG_riga:
                    Esegui_comando(['python3', azione_radice / 'strumenti/connessione_remota_test.py', '--kernel', test_area_di_lavoro / 'kernel8.img',
                         '--access', Impostazioni_File, '--output', risultato], LOG_riga)
                convalidare = json.loads((risultato / 'report.json').read_text())
                assert convalidare['passed']
                Report_VALORE['checks'].append(Nome + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        Report_VALORE['passed'] = True
    finally:
        Report_VALORE['personal_settings_unchanged'] = impostazioni_personali.read_bytes() == 원래설정
        if not Report_VALORE['personal_settings_unchanged']:
            Report_VALORE['passed'] = False
        Report_VALORE['kernel_sha256'] = hashlib.sha256((azione_radice / 'build/kernel8.img').read_bytes()).hexdigest()
        (uscitaTesto / 'report.json').write_text(json.dumps(Report_VALORE, ensure_ascii=False, indent=2) + '\n')
    assert Report_VALORE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(Report_VALORE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    avvia()
