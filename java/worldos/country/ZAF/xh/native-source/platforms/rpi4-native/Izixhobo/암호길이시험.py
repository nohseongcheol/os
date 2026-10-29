#!/usr/bin/env python3
"""개인 uqhagamshelo_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from kude_Iisetingi import lungisa
from COSL배포 import indawo_ekuyiwa_kuyo_igama, ilayibhrari

기준 = Path(__file__).resolve().parents[1]


def Phumeza():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    useto_lomntu = 기준 / 'build/remote/access.json'
    원래설정 = useto_lomntu.read_bytes()
    ingxelo_ixabiso_ddf2aaf3 = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Iisetingi_indlela = 시험터 / 'build/remote'
            Iisetingi_indlela.mkdir(parents=True)
            Iisetingi_ifayile = Iisetingi_indlela / 'access.json'
            def bhala_Iisetingi(iingcombolo):
                Iisetingi_ifayile.write_text(json.dumps(iingcombolo, ensure_ascii=False) + '\n')
                Iisetingi_ifayile.chmod(0o600)
            def ngqinisisa_Iisetingi(isiniki_myalelo, 화면):
                bhala_Iisetingi({'user': 'user', 'ssh_password': isiniki_myalelo, 'vnc_password': 화면})
                원본 = Iisetingi_ifayile.read_bytes()
                lungisa(시험터)
                assert Iisetingi_ifayile.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Iisetingi_indlela / 'Iprofayile.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Iisetingi_indlela / 'Iprofayile.h').stat().st_mode & 0o777 == 0o600
            for isiniki_myalelo, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ngqinisisa_Iisetingi(isiniki_myalelo, 화면)
            ingxelo_ixabiso_ddf2aaf3['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for tshintsha_ixabiso, ufako_nkcukacha_ixabiso in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                iingcombolo = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                iingcombolo.update(tshintsha_ixabiso)
                bhala_Iisetingi(iingcombolo)
                try:
                    lungisa(시험터)
                except SystemExit as Impazamo:
                    assert ufako_nkcukacha_ixabiso in str(Impazamo), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ufako_nkcukacha_ixabiso)
            ingxelo_ixabiso_ddf2aaf3['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Imimiselo = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            isidibanisi = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Uvimba_isixhobo_sokutayipha = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ukwenza_umyalelo(인수, ilog_umqolo):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=ilog_umqolo,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Igama, isiniki_myalelo, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Igama, flush=True)
                ngqinisisa_Iisetingi(isiniki_myalelo, 화면)
                결과 = 출력 / Igama
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as ilog_umqolo:
                    목적들 = []
                    for 원본 in sorted((기준 / 'kude_ixabiso').glob('*.c')):
                        indawo_ekuyiwa_kuyo_ixabiso = 시험터 / (원본.stem + '.o')
                        ukwenza_umyalelo([번역기] + Imimiselo + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Iisetingi_indlela, '-I', 기준 / 'kude_ixabiso', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', indawo_ekuyiwa_kuyo_ixabiso], ilog_umqolo)
                        목적들.append(indawo_ekuyiwa_kuyo_ixabiso)
                    kude_umqulu = 시험터 / 'libremote.a'
                    ukwenza_umyalelo([Uvimba_isixhobo_sokutayipha, 'rcs', kude_umqulu] + 목적들, ilog_umqolo)
                    ukwenza_umyalelo([isidibanisi, '--gc-sections', '-T', 기준 / '부팅/Ilinki_ubume.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Igama + '.o') for Igama in indawo_ekuyiwa_kuyo_igama] + ['--start-group'] +
                         [kude_umqulu if INDLELA == 'remote/libremote.a' else 기준 / 'build' / INDLELA for INDLELA in ilayibhrari] + ['--end-group'], ilog_umqolo)
                    ukwenza_umyalelo([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], ilog_umqolo)
                with (결과 / 'remote-test.log').open('wb') as ilog_umqolo:
                    ukwenza_umyalelo(['python3', 기준 / 'Izixhobo/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Iisetingi_ifayile, '--output', 결과], ilog_umqolo)
                qinisekisa = json.loads((결과 / 'report.json').read_text())
                assert qinisekisa['passed']
                ingxelo_ixabiso_ddf2aaf3['checks'].append(Igama + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ingxelo_ixabiso_ddf2aaf3['passed'] = True
    finally:
        ingxelo_ixabiso_ddf2aaf3['personal_settings_unchanged'] = useto_lomntu.read_bytes() == 원래설정
        if not ingxelo_ixabiso_ddf2aaf3['personal_settings_unchanged']:
            ingxelo_ixabiso_ddf2aaf3['passed'] = False
        ingxelo_ixabiso_ddf2aaf3['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(ingxelo_ixabiso_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    assert ingxelo_ixabiso_ddf2aaf3['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ingxelo_ixabiso_ddf2aaf3, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Phumeza()
