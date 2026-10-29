#!/usr/bin/env python3
"""개인 njikọ_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from ebe_dị̀anyā_Mwube import Kwado
from COSL배포 import ebemwèga_akara_ahà, ọbaakwụkwọ

기준 = Path(__file__).resolve().parents[1]


def Bido():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    mwube_kèonwē = 기준 / 'build/remote/access.json'
    원래설정 = mwube_kèonwē.read_bytes()
    akụkọ_valuu = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Mwube_ụzọ_ozi = 시험터 / 'build/remote'
            Mwube_ụzọ_ozi.mkdir(parents=True)
            Mwube_ọbọakwụkwọ = Mwube_ụzọ_ozi / 'access.json'
            def dee_Mwube(datà):
                Mwube_ọbọakwụkwọ.write_text(json.dumps(datà, ensure_ascii=False) + '\n')
                Mwube_ọbọakwụkwọ.chmod(0o600)
            def nkwàdo_eziokwū_Mwube(nkọwannyemiwu, 화면):
                dee_Mwube({'user': 'user', 'ssh_password': nkọwannyemiwu, 'vnc_password': 화면})
                원본 = Mwube_ọbọakwụkwọ.read_bytes()
                Kwado(시험터)
                assert Mwube_ọbọakwụkwọ.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Mwube_ụzọ_ozi / 'Profaịl.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Mwube_ụzọ_ozi / 'Profaịl.h').stat().st_mode & 0o777 == 0o600
            for nkọwannyemiwu, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                nkwàdo_eziokwū_Mwube(nkọwannyemiwu, 화면)
            akụkọ_valuu['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for gbanwèe_valuu, ndebà_valuu in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                datà = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                datà.update(gbanwèe_valuu)
                dee_Mwube(datà)
                try:
                    Kwado(시험터)
                except SystemExit as mmejọ:
                    assert ndebà_valuu in str(mmejọ), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ndebà_valuu)
            akụkọ_valuu['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Mwube = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            ṅjikọta = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ọkpụ_ngwaọrụ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def mee_nnyemiwu(인수, ndekọ_NDEKỌ):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=ndekọ_NDEKỌ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Aha, nkọwannyemiwu, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Aha, flush=True)
                nkwàdo_eziokwū_Mwube(nkọwannyemiwu, 화면)
                결과 = 출력 / Aha
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as ndekọ_NDEKỌ:
                    목적들 = []
                    for 원본 in sorted((기준 / 'ebe_dị̀anyā_valuu').glob('*.c')):
                        ebemwèga_valuu = 시험터 / (원본.stem + '.o')
                        mee_nnyemiwu([번역기] + Mwube + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Mwube_ụzọ_ozi, '-I', 기준 / 'ebe_dị̀anyā_valuu', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ebemwèga_valuu], ndekọ_NDEKỌ)
                        목적들.append(ebemwèga_valuu)
                    ebe_dị̀anyā_ngwungwu = 시험터 / 'libremote.a'
                    mee_nnyemiwu([ọkpụ_ngwaọrụ, 'rcs', ebe_dị̀anyā_ngwungwu] + 목적들, ndekọ_NDEKỌ)
                    mee_nnyemiwu([ṅjikọta, '--gc-sections', '-T', 기준 / '부팅/Njikọ_Nhàzi.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Aha + '.o') for Aha in ebemwèga_akara_ahà] + ['--start-group'] +
                         [ebe_dị̀anyā_ngwungwu if ụzọ_ozi == 'remote/libremote.a' else 기준 / 'build' / ụzọ_ozi for ụzọ_ozi in ọbaakwụkwọ] + ['--end-group'], ndekọ_NDEKỌ)
                    mee_nnyemiwu([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], ndekọ_NDEKỌ)
                with (결과 / 'remote-test.log').open('wb') as ndekọ_NDEKỌ:
                    mee_nnyemiwu(['python3', 기준 / 'Ngwaọrụ/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Mwube_ọbọakwụkwọ, '--output', 결과], ndekọ_NDEKỌ)
                mee_ịbanihe = json.loads((결과 / 'report.json').read_text())
                assert mee_ịbanihe['passed']
                akụkọ_valuu['checks'].append(Aha + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        akụkọ_valuu['passed'] = True
    finally:
        akụkọ_valuu['personal_settings_unchanged'] = mwube_kèonwē.read_bytes() == 원래설정
        if not akụkọ_valuu['personal_settings_unchanged']:
            akụkọ_valuu['passed'] = False
        akụkọ_valuu['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(akụkọ_valuu, ensure_ascii=False, indent=2) + '\n')
    assert akụkọ_valuu['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(akụkọ_valuu, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Bido()
