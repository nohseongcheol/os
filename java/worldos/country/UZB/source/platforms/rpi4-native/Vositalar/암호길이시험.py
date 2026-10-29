#!/usr/bin/env python3
"""개인 aloqa_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from masofaviy_Sozlamalar import Tayyorlamoq
from COSL배포 import ko_chirish_joyi_nom, kutubxona

Project_ildiz = Path(__file__).resolve().parents[1]


def Bajarish():
    출력 = Project_ildiz / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    Shaxsiy_parametrlar = Project_ildiz / 'build/remote/access.json'
    원래설정 = Shaxsiy_parametrlar.read_bytes()
    hisobot_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Sozlamalar_yo_l = 시험터 / 'build/remote'
            Sozlamalar_yo_l.mkdir(parents=True)
            Sozlamalar_fayl = Sozlamalar_yo_l / 'access.json'
            def yozmoq_Sozlamalar(ma_lumotlar):
                Sozlamalar_fayl.write_text(json.dumps(ma_lumotlar, ensure_ascii=False) + '\n')
                Sozlamalar_fayl.chmod(0o600)
            def tasdiqlamoq_Sozlamalar(qobiq, 화면):
                yozmoq_Sozlamalar({'user': 'user', 'ssh_password': qobiq, 'vnc_password': 화면})
                원본 = Sozlamalar_fayl.read_bytes()
                Tayyorlamoq(시험터)
                assert Sozlamalar_fayl.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Sozlamalar_yo_l / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Sozlamalar_yo_l / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for qobiq, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                tasdiqlamoq_Sozlamalar(qobiq, 화면)
            hisobot_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for o_zgartirmoq_VALUE, kiritish_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ma_lumotlar = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ma_lumotlar.update(o_zgartirmoq_VALUE)
                yozmoq_Sozlamalar(ma_lumotlar)
                try:
                    Tayyorlamoq(시험터)
                except SystemExit as Xato:
                    assert kiritish_VALUE in str(Xato), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + kiritish_VALUE)
            hisobot_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Moslamalar = json.loads((Project_ildiz / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Ulagich = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arxiv_vosita = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def bajarmoq_buyruq(인수, LOG_satr):
                subprocess.run(list(map(str, 인수)), cwd=str(Project_ildiz), stdout=LOG_satr,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nomi, qobiq, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nomi, flush=True)
                tasdiqlamoq_Sozlamalar(qobiq, 화면)
                o_lchov = 출력 / Nomi
                o_lchov.mkdir(exist_ok=True)
                with (o_lchov / 'build.log').open('wb') as LOG_satr:
                    목적들 = []
                    for 원본 in sorted((Project_ildiz / 'masofaviy_VALUE').glob('*.c')):
                        ko_chirish_joyi_VALUE = 시험터 / (원본.stem + '.o')
                        bajarmoq_buyruq([번역기] + Moslamalar + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Sozlamalar_yo_l, '-I', Project_ildiz / 'masofaviy_VALUE', '-I', Project_ildiz / 'vendor/libassh/src',
                             '-I', Project_ildiz / 'vendor/bearssl/inc', '-I', Project_ildiz / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ko_chirish_joyi_VALUE], LOG_satr)
                        목적들.append(ko_chirish_joyi_VALUE)
                    masofaviy_to_plam = 시험터 / 'libremote.a'
                    bajarmoq_buyruq([Arxiv_vosita, 'rcs', masofaviy_to_plam] + 목적들, LOG_satr)
                    bajarmoq_buyruq([Ulagich, '--gc-sections', '-T', Project_ildiz / '부팅/ulash_Maket.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_ildiz / 'build' / (Nomi + '.o') for Nomi in ko_chirish_joyi_nom] + ['--start-group'] +
                         [masofaviy_to_plam if yo_l == 'remote/libremote.a' else Project_ildiz / 'build' / yo_l for yo_l in kutubxona] + ['--end-group'], LOG_satr)
                    bajarmoq_buyruq([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_satr)
                with (o_lchov / 'remote-test.log').open('wb') as LOG_satr:
                    bajarmoq_buyruq(['python3', Project_ildiz / 'Vositalar/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Sozlamalar_fayl, '--output', o_lchov], LOG_satr)
                tasdiqlash = json.loads((o_lchov / 'report.json').read_text())
                assert tasdiqlash['passed']
                hisobot_VALUE['checks'].append(Nomi + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        hisobot_VALUE['passed'] = True
    finally:
        hisobot_VALUE['personal_settings_unchanged'] = Shaxsiy_parametrlar.read_bytes() == 원래설정
        if not hisobot_VALUE['personal_settings_unchanged']:
            hisobot_VALUE['passed'] = False
        hisobot_VALUE['kernel_sha256'] = hashlib.sha256((Project_ildiz / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(hisobot_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert hisobot_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(hisobot_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Bajarish()
