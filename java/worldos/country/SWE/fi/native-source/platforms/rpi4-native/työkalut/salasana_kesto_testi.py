#!/usr/bin/env python3
"""개인 yhteys_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from etä_Asetukset import Valmistele
from COSL배포 import kohde_nimi, kirjasto

aloite_juuri = Path(__file__).resolve().parents[1]


def Suorita_2():
    tulostuspaikka = aloite_juuri / 'build/verification/password-length'
    tulostuspaikka.mkdir(parents=True, exist_ok=True)
    omat_asetukset = aloite_juuri / 'build/remote/access.json'
    원래설정 = omat_asetukset.read_bytes()
    raportti_ARVO = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            testi_työtila = Path(임시)
            Asetukset_polku = testi_työtila / 'build/remote'
            Asetukset_polku.mkdir(parents=True)
            Asetukset_Tiedosto = Asetukset_polku / 'access.json'
            def kirjoitus_Asetukset(data):
                Asetukset_Tiedosto.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Asetukset_Tiedosto.chmod(0o600)
            def tarkistaa_Asetukset(liittymä, 화면):
                kirjoitus_Asetukset({'user': 'user', 'ssh_password': liittymä, 'vnc_password': 화면})
                원본 = Asetukset_Tiedosto.read_bytes()
                Valmistele(testi_työtila)
                assert Asetukset_Tiedosto.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Asetukset_polku / 'Profiili.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Asetukset_polku / 'Profiili.h').stat().st_mode & 0o777 == 0o600
            for liittymä, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                tarkistaa_Asetukset(liittymä, 화면)
            raportti_ARVO['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for muuttaa_ARVO, merkintä_ARVO_962f286b in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(muuttaa_ARVO)
                kirjoitus_Asetukset(data)
                try:
                    Valmistele(testi_työtila)
                except SystemExit as VIRHE:
                    assert merkintä_ARVO_962f286b in str(VIRHE), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + merkintä_ARVO_962f286b)
            raportti_ARVO['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Asetukset = json.loads((aloite_juuri / 'build/remote/libassh-build.json').read_text())['flags']
            kääntäjä_työkalu = os.environ.get('ARM64_CC', 'clang')
            liitin = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arkisto_työkalu = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Suorita_komento(argumentit, LOG_TIETUE):
                subprocess.run(list(map(str, argumentit)), cwd=str(aloite_juuri), stdout=LOG_TIETUE,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nimi, liittymä, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nimi, flush=True)
                tarkistaa_Asetukset(liittymä, 화면)
                TULOS = tulostuspaikka / Nimi
                TULOS.mkdir(exist_ok=True)
                with (TULOS / 'build.log').open('wb') as LOG_TIETUE:
                    목적들 = []
                    for 원본 in sorted((aloite_juuri / 'etä_ARVO').glob('*.c')):
                        kohde_ARVO = testi_työtila / (원본.stem + '.o')
                        Suorita_komento([kääntäjä_työkalu] + Asetukset + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Asetukset_polku, '-I', aloite_juuri / 'etä_ARVO', '-I', aloite_juuri / 'vendor/libassh/src',
                             '-I', aloite_juuri / 'vendor/bearssl/inc', '-I', aloite_juuri / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', kohde_ARVO], LOG_TIETUE)
                        목적들.append(kohde_ARVO)
                    etä_nippu = testi_työtila / 'libremote.a'
                    Suorita_komento([Arkisto_työkalu, 'rcs', etä_nippu] + 목적들, LOG_TIETUE)
                    Suorita_komento([liitin, '--gc-sections', '-T', aloite_juuri / 'koneen_käynnistys/linkitysasettelu.ld', '-o', testi_työtila / 'kernel.elf'] +
                         [aloite_juuri / 'build' / (Nimi + '.o') for Nimi in kohde_nimi] + ['--start-group'] +
                         [etä_nippu if polku_2 == 'remote/libremote.a' else aloite_juuri / 'build' / polku_2 for polku_2 in kirjasto] + ['--end-group'], LOG_TIETUE)
                    Suorita_komento([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         testi_työtila / 'kernel.elf', testi_työtila / 'kernel8.img'], LOG_TIETUE)
                with (TULOS / 'remote-test.log').open('wb') as LOG_TIETUE:
                    Suorita_komento(['python3', aloite_juuri / 'työkalut/etäyhteys_testi.py', '--kernel', testi_työtila / 'kernel8.img',
                         '--access', Asetukset_Tiedosto, '--output', TULOS], LOG_TIETUE)
                vahvista = json.loads((TULOS / 'report.json').read_text())
                assert vahvista['passed']
                raportti_ARVO['checks'].append(Nimi + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        raportti_ARVO['passed'] = True
    finally:
        raportti_ARVO['personal_settings_unchanged'] = omat_asetukset.read_bytes() == 원래설정
        if not raportti_ARVO['personal_settings_unchanged']:
            raportti_ARVO['passed'] = False
        raportti_ARVO['kernel_sha256'] = hashlib.sha256((aloite_juuri / 'build/kernel8.img').read_bytes()).hexdigest()
        (tulostuspaikka / 'report.json').write_text(json.dumps(raportti_ARVO, ensure_ascii=False, indent=2) + '\n')
    assert raportti_ARVO['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(raportti_ARVO, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Suorita_2()
