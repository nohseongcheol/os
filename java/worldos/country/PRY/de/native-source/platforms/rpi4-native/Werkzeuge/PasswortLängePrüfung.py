#!/usr/bin/env python3
"""개인 verbindung 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from entferntEinstellungen import vorbereiten
from COSLVerteilung import zielName, bibliothek

projektWurzel = Path(__file__).resolve().parents[1]


def ausführenVorgang():
    Ausgabe = projektWurzel / 'build/verification/password-length'
    Ausgabe.mkdir(parents=True, exist_ok=True)
    persönlichEinstellungen = projektWurzel / 'build/remote/access.json'
    ursprünglichEinstellungen = persönlichEinstellungen.read_bytes()
    berichtWert = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as vorläufigWert:
            arbeitsraumPrüfung = Path(vorläufigWert)
            einstellungenPfad = arbeitsraumPrüfung / 'build/remote'
            einstellungenPfad.mkdir(parents=True)
            einstellungenDatei = einstellungenPfad / 'access.json'
            def einstellungenSchreiben(Daten):
                einstellungenDatei.write_text(json.dumps(Daten, ensure_ascii=False) + '\n')
                einstellungenDatei.chmod(0o600)
            def einstellungenÜberprüfen(befehlshülle, Bildschirm):
                einstellungenSchreiben({'user': 'user', 'ssh_password': befehlshülle, 'vnc_password': Bildschirm})
                ursprünglich = einstellungenDatei.read_bytes()
                vorbereiten(arbeitsraumPrüfung)
                assert einstellungenDatei.read_bytes() == ursprünglich, 'Settings were rewritten'
                kopfWert = (einstellungenPfad / 'profil.h').read_text()
                istGleich = re.search(r'bildschirmPasswort\[\] = \{([^}]+)\}', kopfWert)
                assert istGleich and len(istGleich.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (einstellungenPfad / 'profil.h').stat().st_mode & 0o777 == 0o600
            for befehlshülle, Bildschirm in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                einstellungenÜberprüfen(befehlshülle, Bildschirm)
            berichtWert['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for wertÄndern, eintragWert in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                Daten = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                Daten.update(wertÄndern)
                einstellungenSchreiben(Daten)
                try:
                    vorbereiten(arbeitsraumPrüfung)
                except SystemExit as fehler:
                    assert eintragWert in str(fehler), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + eintragWert)
            berichtWert['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            einstellungen = json.loads((projektWurzel / 'build/remote/libassh-build.json').read_text())['flags']
            übersetzerWerkzeug = os.environ.get('ARM64_CC', 'clang')
            verbinder = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            archivWerkzeug = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def befehlAusführen(argumente, protokolldateiAufzeichnung):
                subprocess.run(list(map(str, argumente)), cwd=str(projektWurzel), stdout=protokolldateiAufzeichnung,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Name, befehlshülle, Bildschirm in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Name, flush=True)
                einstellungenÜberprüfen(befehlshülle, Bildschirm)
                ergebnis = Ausgabe / Name
                ergebnis.mkdir(exist_ok=True)
                with (ergebnis / 'build.log').open('wb') as protokolldateiAufzeichnung:
                    zielstellen = []
                    for ursprünglich in sorted((projektWurzel / 'entferntWert').glob('*.c')):
                        zielWert = arbeitsraumPrüfung / (ursprünglich.stem + '.o')
                        befehlAusführen([übersetzerWerkzeug] + einstellungen + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', einstellungenPfad, '-I', projektWurzel / 'entferntWert', '-I', projektWurzel / 'vendor/libassh/src',
                             '-I', projektWurzel / 'vendor/bearssl/inc', '-I', projektWurzel / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', ursprünglich, '-o', zielWert], protokolldateiAufzeichnung)
                        zielstellen.append(zielWert)
                    entferntBündel = arbeitsraumPrüfung / 'libremote.a'
                    befehlAusführen([archivWerkzeug, 'rcs', entferntBündel] + zielstellen, protokolldateiAufzeichnung)
                    befehlAusführen([verbinder, '--gc-sections', '-T', projektWurzel / 'Startvorgang/Bindungsanordnung.ld', '-o', arbeitsraumPrüfung / 'kernel.elf'] +
                         [projektWurzel / 'build' / (Name + '.o') for Name in zielName] + ['--start-group'] +
                         [entferntBündel if pfad == 'remote/libremote.a' else projektWurzel / 'build' / pfad for pfad in bibliothek] + ['--end-group'], protokolldateiAufzeichnung)
                    befehlAusführen([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         arbeitsraumPrüfung / 'kernel.elf', arbeitsraumPrüfung / 'kernel8.img'], protokolldateiAufzeichnung)
                with (ergebnis / 'remote-test.log').open('wb') as protokolldateiAufzeichnung:
                    befehlAusführen(['python3', projektWurzel / 'Werkzeuge/EntferntVerbindungPrüfung.py', '--kernel', arbeitsraumPrüfung / 'kernel8.img',
                         '--access', einstellungenDatei, '--output', ergebnis], protokolldateiAufzeichnung)
                validieren = json.loads((ergebnis / 'report.json').read_text())
                assert validieren['passed']
                berichtWert['checks'].append(Name + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        berichtWert['passed'] = True
    finally:
        berichtWert['personal_settings_unchanged'] = persönlichEinstellungen.read_bytes() == ursprünglichEinstellungen
        if not berichtWert['personal_settings_unchanged']:
            berichtWert['passed'] = False
        berichtWert['kernel_sha256'] = hashlib.sha256((projektWurzel / 'build/kernel8.img').read_bytes()).hexdigest()
        (Ausgabe / 'report.json').write_text(json.dumps(berichtWert, ensure_ascii=False, indent=2) + '\n')
    assert berichtWert['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(berichtWert, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ausführenVorgang()
