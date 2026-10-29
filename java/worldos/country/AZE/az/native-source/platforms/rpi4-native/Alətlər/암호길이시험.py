#!/usr/bin/env python3
"""개인 qoşulma_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from uzaq_Parametrlər import Hazırla
from COSL배포 import təyinat_ad, kitabxana

Project_kök = Path(__file__).resolve().parents[1]


def İcra_Et():
    출력 = Project_kök / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    fərdi_parametrlər = Project_kök / 'build/remote/access.json'
    원래설정 = fərdi_parametrlər.read_bytes()
    hesabat_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Parametrlər_yol = 시험터 / 'build/remote'
            Parametrlər_yol.mkdir(parents=True)
            Parametrlər_fayl = Parametrlər_yol / 'access.json'
            def yazmaq_Parametrlər(verilənlər):
                Parametrlər_fayl.write_text(json.dumps(verilənlər, ensure_ascii=False) + '\n')
                Parametrlər_fayl.chmod(0o600)
            def yoxlamaq_Parametrlər(örtük, 화면):
                yazmaq_Parametrlər({'user': 'user', 'ssh_password': örtük, 'vnc_password': 화면})
                원본 = Parametrlər_fayl.read_bytes()
                Hazırla(시험터)
                assert Parametrlər_fayl.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Parametrlər_yol / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Parametrlər_yol / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for örtük, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                yoxlamaq_Parametrlər(örtük, 화면)
            hesabat_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for dəyişdirmək_VALUE, daxiletmə_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                verilənlər = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                verilənlər.update(dəyişdirmək_VALUE)
                yazmaq_Parametrlər(verilənlər)
                try:
                    Hazırla(시험터)
                except SystemExit as XƏTA:
                    assert daxiletmə_VALUE in str(XƏTA), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + daxiletmə_VALUE)
            hesabat_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Sazlama = json.loads((Project_kök / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Birləşdirici = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arxiv_alət = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def icra_etmək_əmr(인수, LOG_yaz):
                subprocess.run(list(map(str, 인수)), cwd=str(Project_kök), stdout=LOG_yaz,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Ad, örtük, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Ad, flush=True)
                yoxlamaq_Parametrlər(örtük, 화면)
                ölçü = 출력 / Ad
                ölçü.mkdir(exist_ok=True)
                with (ölçü / 'build.log').open('wb') as LOG_yaz:
                    목적들 = []
                    for 원본 in sorted((Project_kök / 'uzaq_VALUE').glob('*.c')):
                        təyinat_VALUE_a0fbc067 = 시험터 / (원본.stem + '.o')
                        icra_etmək_əmr([번역기] + Sazlama + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Parametrlər_yol, '-I', Project_kök / 'uzaq_VALUE', '-I', Project_kök / 'vendor/libassh/src',
                             '-I', Project_kök / 'vendor/bearssl/inc', '-I', Project_kök / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', təyinat_VALUE_a0fbc067], LOG_yaz)
                        목적들.append(təyinat_VALUE_a0fbc067)
                    uzaq_paket = 시험터 / 'libremote.a'
                    icra_etmək_əmr([Arxiv_alət, 'rcs', uzaq_paket] + 목적들, LOG_yaz)
                    icra_etmək_əmr([Birləşdirici, '--gc-sections', '-T', Project_kök / '부팅/keçid_Düzüm.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_kök / 'build' / (Ad + '.o') for Ad in təyinat_ad] + ['--start-group'] +
                         [uzaq_paket if Cığır == 'remote/libremote.a' else Project_kök / 'build' / Cığır for Cığır in kitabxana] + ['--end-group'], LOG_yaz)
                    icra_etmək_əmr([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_yaz)
                with (ölçü / 'remote-test.log').open('wb') as LOG_yaz:
                    icra_etmək_əmr(['python3', Project_kök / 'Alətlər/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Parametrlər_fayl, '--output', ölçü], LOG_yaz)
                təsdiqlə = json.loads((ölçü / 'report.json').read_text())
                assert təsdiqlə['passed']
                hesabat_VALUE['checks'].append(Ad + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        hesabat_VALUE['passed'] = True
    finally:
        hesabat_VALUE['personal_settings_unchanged'] = fərdi_parametrlər.read_bytes() == 원래설정
        if not hesabat_VALUE['personal_settings_unchanged']:
            hesabat_VALUE['passed'] = False
        hesabat_VALUE['kernel_sha256'] = hashlib.sha256((Project_kök / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(hesabat_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert hesabat_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(hesabat_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    İcra_Et()
