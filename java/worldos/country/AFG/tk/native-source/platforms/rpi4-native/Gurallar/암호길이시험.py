#!/usr/bin/env python3
"""개인 birikme_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from uzakdan_Sazlamalar import Taýýarla
from COSL배포 import barylmaly_ýer_at, Kitaphana

기준 = Path(__file__).resolve().parents[1]


def Bitir():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    şahsy_gurma = 기준 / 'build/remote/access.json'
    원래설정 = şahsy_gurma.read_bytes()
    hasabat_baha = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Sazlamalar_ýol = 시험터 / 'build/remote'
            Sazlamalar_ýol.mkdir(parents=True)
            Sazlamalar_faýl = Sazlamalar_ýol / 'access.json'
            def ýaz_Sazlamalar(maglumat):
                Sazlamalar_faýl.write_text(json.dumps(maglumat, ensure_ascii=False) + '\n')
                Sazlamalar_faýl.chmod(0o600)
            def barla_Sazlamalar(gabyjak, 화면):
                ýaz_Sazlamalar({'user': 'user', 'ssh_password': gabyjak, 'vnc_password': 화면})
                원본 = Sazlamalar_faýl.read_bytes()
                Taýýarla(시험터)
                assert Sazlamalar_faýl.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Sazlamalar_ýol / 'profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Sazlamalar_ýol / 'profil.h').stat().st_mode & 0o777 == 0o600
            for gabyjak, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                barla_Sazlamalar(gabyjak, 화면)
            hasabat_baha['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for üýtget_baha, girizmeklik_baha in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                maglumat = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                maglumat.update(üýtget_baha)
                ýaz_Sazlamalar(maglumat)
                try:
                    Taýýarla(시험터)
                except SystemExit as Hata:
                    assert girizmeklik_baha in str(Hata), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + girizmeklik_baha)
            hasabat_baha['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Düzümler = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            birikdiriji = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arhiw_gural = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ýerine_ýetir_buýruk(인수, hasaba_alyş_setir):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=hasaba_alyş_setir,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Ad, gabyjak, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Ad, flush=True)
                barla_Sazlamalar(gabyjak, 화면)
                결과 = 출력 / Ad
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as hasaba_alyş_setir:
                    목적들 = []
                    for 원본 in sorted((기준 / 'uzakdan_baha').glob('*.c')):
                        barylmaly_ýer_baha = 시험터 / (원본.stem + '.o')
                        ýerine_ýetir_buýruk([번역기] + Düzümler + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Sazlamalar_ýol, '-I', 기준 / 'uzakdan_baha', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', barylmaly_ýer_baha], hasaba_alyş_setir)
                        목적들.append(barylmaly_ýer_baha)
                    uzakdan_toplum = 시험터 / 'libremote.a'
                    ýerine_ýetir_buýruk([Arhiw_gural, 'rcs', uzakdan_toplum] + 목적들, hasaba_alyş_setir)
                    ýerine_ýetir_buýruk([birikdiriji, '--gc-sections', '-T', 기준 / '부팅/Bag_Ýerleşiş.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Ad + '.o') for Ad in barylmaly_ýer_at] + ['--start-group'] +
                         [uzakdan_toplum if Ýol == 'remote/libremote.a' else 기준 / 'build' / Ýol for Ýol in Kitaphana] + ['--end-group'], hasaba_alyş_setir)
                    ýerine_ýetir_buýruk([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], hasaba_alyş_setir)
                with (결과 / 'remote-test.log').open('wb') as hasaba_alyş_setir:
                    ýerine_ýetir_buýruk(['python3', 기준 / 'Gurallar/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Sazlamalar_faýl, '--output', 결과], hasaba_alyş_setir)
                tassykla = json.loads((결과 / 'report.json').read_text())
                assert tassykla['passed']
                hasabat_baha['checks'].append(Ad + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        hasabat_baha['passed'] = True
    finally:
        hasabat_baha['personal_settings_unchanged'] = şahsy_gurma.read_bytes() == 원래설정
        if not hasabat_baha['personal_settings_unchanged']:
            hasabat_baha['passed'] = False
        hasabat_baha['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(hasabat_baha, ensure_ascii=False, indent=2) + '\n')
    assert hasabat_baha['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(hasabat_baha, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Bitir()
