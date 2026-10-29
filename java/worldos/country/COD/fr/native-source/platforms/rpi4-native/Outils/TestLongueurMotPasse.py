#!/usr/bin/env python3
"""개인 connexion 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from réglagesDistant import préparer
from DistributionCOSL import nomDestination, bibliothèque

racineProjet = Path(__file__).resolve().parents[1]


def lancer():
    Sortie = racineProjet / 'build/verification/password-length'
    Sortie.mkdir(parents=True, exist_ok=True)
    réglagesPersonnel = racineProjet / 'build/remote/access.json'
    réglagesOriginal = réglagesPersonnel.read_bytes()
    valeurRapport = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as valeurTemporaire:
            testEspaceTravail = Path(valeurTemporaire)
            cheminRéglages = testEspaceTravail / 'build/remote'
            cheminRéglages.mkdir(parents=True)
            fichierRéglages = cheminRéglages / 'access.json'
            def écrireRéglages(Données):
                fichierRéglages.write_text(json.dumps(Données, ensure_ascii=False) + '\n')
                fichierRéglages.chmod(0o600)
            def vérifierRéglages(interpréteurCommandes, Écran):
                écrireRéglages({'user': 'user', 'ssh_password': interpréteurCommandes, 'vnc_password': Écran})
                original = fichierRéglages.read_bytes()
                préparer(testEspaceTravail)
                assert fichierRéglages.read_bytes() == original, 'Settings were rewritten'
                valeurTête = (cheminRéglages / 'profil.h').read_text()
                estÉgal = re.search(r'motPasseÉcran\[\] = \{([^}]+)\}', valeurTête)
                assert estÉgal and len(estÉgal.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (cheminRéglages / 'profil.h').stat().st_mode & 0o777 == 0o600
            for interpréteurCommandes, Écran in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                vérifierRéglages(interpréteurCommandes, Écran)
            valeurRapport['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for changerValeur, valeurEntréeÉlément in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                Données = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                Données.update(changerValeur)
                écrireRéglages(Données)
                try:
                    préparer(testEspaceTravail)
                except SystemExit as erreur:
                    assert valeurEntréeÉlément in str(erreur), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + valeurEntréeÉlément)
            valeurRapport['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            réglages = json.loads((racineProjet / 'build/remote/libassh-build.json').read_text())['flags']
            outilCompilateur = os.environ.get('ARM64_CC', 'clang')
            connecteur = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            outilArchive = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def exécuterCommande(arguments, enregistrementJournal):
                subprocess.run(list(map(str, arguments)), cwd=str(racineProjet), stdout=enregistrementJournal,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for nom, interpréteurCommandes, Écran in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + nom, flush=True)
                vérifierRéglages(interpréteurCommandes, Écran)
                résultat = Sortie / nom
                résultat.mkdir(exist_ok=True)
                with (résultat / 'build.log').open('wb') as enregistrementJournal:
                    destinations = []
                    for original in sorted((racineProjet / 'valeurDistant').glob('*.c')):
                        valeurDestination = testEspaceTravail / (original.stem + '.o')
                        exécuterCommande([outilCompilateur] + réglages + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', cheminRéglages, '-I', racineProjet / 'valeurDistant', '-I', racineProjet / 'vendor/libassh/src',
                             '-I', racineProjet / 'vendor/bearssl/inc', '-I', racineProjet / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', original, '-o', valeurDestination], enregistrementJournal)
                        destinations.append(valeurDestination)
                    lotDistant = testEspaceTravail / 'libremote.a'
                    exécuterCommande([outilArchive, 'rcs', lotDistant] + destinations, enregistrementJournal)
                    exécuterCommande([connecteur, '--gc-sections', '-T', racineProjet / 'Amorçage/DispositionLiens.ld', '-o', testEspaceTravail / 'kernel.elf'] +
                         [racineProjet / 'build' / (nom + '.o') for nom in nomDestination] + ['--start-group'] +
                         [lotDistant if chemin == 'remote/libremote.a' else racineProjet / 'build' / chemin for chemin in bibliothèque] + ['--end-group'], enregistrementJournal)
                    exécuterCommande([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         testEspaceTravail / 'kernel.elf', testEspaceTravail / 'kernel8.img'], enregistrementJournal)
                with (résultat / 'remote-test.log').open('wb') as enregistrementJournal:
                    exécuterCommande(['python3', racineProjet / 'Outils/TestConnexionDistant.py', '--kernel', testEspaceTravail / 'kernel8.img',
                         '--access', fichierRéglages, '--output', résultat], enregistrementJournal)
                valider = json.loads((résultat / 'report.json').read_text())
                assert valider['passed']
                valeurRapport['checks'].append(nom + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        valeurRapport['passed'] = True
    finally:
        valeurRapport['personal_settings_unchanged'] = réglagesPersonnel.read_bytes() == réglagesOriginal
        if not valeurRapport['personal_settings_unchanged']:
            valeurRapport['passed'] = False
        valeurRapport['kernel_sha256'] = hashlib.sha256((racineProjet / 'build/kernel8.img').read_bytes()).hexdigest()
        (Sortie / 'report.json').write_text(json.dumps(valeurRapport, ensure_ascii=False, indent=2) + '\n')
    assert valeurRapport['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(valeurRapport, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    lancer()
