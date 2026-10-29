#!/usr/bin/env python3
"""개인 haɗi_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from na_nesa_Saituna import Shirya
from COSL배포 import Zangon_ƙarshe_Suna, laburare

기준 = Path(__file__).resolve().parents[1]


def Tafiyar_da():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    Saitunan_kanka = 기준 / 'build/remote/access.json'
    원래설정 = Saitunan_kanka.read_bytes()
    Rahoto_Daraja = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Saituna_Hanyar_shiga = 시험터 / 'build/remote'
            Saituna_Hanyar_shiga.mkdir(parents=True)
            Saituna_Fayil = Saituna_Hanyar_shiga / 'access.json'
            def Rubuta_Saituna(Tarin_bayani):
                Saituna_Fayil.write_text(json.dumps(Tarin_bayani, ensure_ascii=False) + '\n')
                Saituna_Fayil.chmod(0o600)
            def Tabbatar_da_Saituna(Mai_fayyace_umani, 화면):
                Rubuta_Saituna({'user': 'user', 'ssh_password': Mai_fayyace_umani, 'vnc_password': 화면})
                원본 = Saituna_Fayil.read_bytes()
                Shirya(시험터)
                assert Saituna_Fayil.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Saituna_Hanyar_shiga / 'furofayil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Saituna_Hanyar_shiga / 'furofayil.h').stat().st_mode & 0o777 == 0o600
            for Mai_fayyace_umani, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                Tabbatar_da_Saituna(Mai_fayyace_umani, 화면)
            Rahoto_Daraja['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for Canza_Daraja, Mashigar_bayanai_Daraja in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                Tarin_bayani = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                Tarin_bayani.update(Canza_Daraja)
                Rubuta_Saituna(Tarin_bayani)
                try:
                    Shirya(시험터)
                except SystemExit as Kuskure:
                    assert Mashigar_bayanai_Daraja in str(Kuskure), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + Mashigar_bayanai_Daraja)
            Rahoto_Daraja['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Saituna = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            na_urar_haɗawa = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Rumbun_ajiya_kayan_aiki = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def gudanar_Umarni(인수, logu_naɗa):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=logu_naɗa,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Suna, Mai_fayyace_umani, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Suna, flush=True)
                Tabbatar_da_Saituna(Mai_fayyace_umani, 화면)
                결과 = 출력 / Suna
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as logu_naɗa:
                    목적들 = []
                    for 원본 in sorted((기준 / 'na_nesa_Daraja').glob('*.c')):
                        Zangon_ƙarshe_Daraja = 시험터 / (원본.stem + '.o')
                        gudanar_Umarni([번역기] + Saituna + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Saituna_Hanyar_shiga, '-I', 기준 / 'na_nesa_Daraja', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', Zangon_ƙarshe_Daraja], logu_naɗa)
                        목적들.append(Zangon_ƙarshe_Daraja)
                    na_nesa_dami = 시험터 / 'libremote.a'
                    gudanar_Umarni([Rumbun_ajiya_kayan_aiki, 'rcs', na_nesa_dami] + 목적들, logu_naɗa)
                    gudanar_Umarni([na_urar_haɗawa, '--gc-sections', '-T', 기준 / '부팅/Kafa_Zagaye.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Suna + '.o') for Suna in Zangon_ƙarshe_Suna] + ['--start-group'] +
                         [na_nesa_dami if Hanyar_shiga == 'remote/libremote.a' else 기준 / 'build' / Hanyar_shiga for Hanyar_shiga in laburare] + ['--end-group'], logu_naɗa)
                    gudanar_Umarni([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], logu_naɗa)
                with (결과 / 'remote-test.log').open('wb') as logu_naɗa:
                    gudanar_Umarni(['python3', 기준 / 'Kaya/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Saituna_Fayil, '--output', 결과], logu_naɗa)
                inganta = json.loads((결과 / 'report.json').read_text())
                assert inganta['passed']
                Rahoto_Daraja['checks'].append(Suna + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        Rahoto_Daraja['passed'] = True
    finally:
        Rahoto_Daraja['personal_settings_unchanged'] = Saitunan_kanka.read_bytes() == 원래설정
        if not Rahoto_Daraja['personal_settings_unchanged']:
            Rahoto_Daraja['passed'] = False
        Rahoto_Daraja['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(Rahoto_Daraja, ensure_ascii=False, indent=2) + '\n')
    assert Rahoto_Daraja['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(Rahoto_Daraja, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Tafiyar_da()
