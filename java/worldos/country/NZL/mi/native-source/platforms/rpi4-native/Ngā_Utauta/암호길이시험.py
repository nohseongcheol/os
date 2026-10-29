#!/usr/bin/env python3
"""개인 hononga_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from mamao_Ngā_Tautuhinga import Whakarite
from COSL배포 import ūnga_ingoa, puna

whakaatu_pūtake = Path(__file__).resolve().parents[1]


def whakahaere():
    출력 = whakaatu_pūtake / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    tautuhinga_whaiaro = whakaatu_pūtake / 'build/remote/access.json'
    원래설정 = tautuhinga_whaiaro.read_bytes()
    pūrongo_uara = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Ngā_Tautuhinga_ara = 시험터 / 'build/remote'
            Ngā_Tautuhinga_ara.mkdir(parents=True)
            Ngā_Tautuhinga_kōnae = Ngā_Tautuhinga_ara / 'access.json'
            def tuhi_Ngā_Tautuhinga(raraunga):
                Ngā_Tautuhinga_kōnae.write_text(json.dumps(raraunga, ensure_ascii=False) + '\n')
                Ngā_Tautuhinga_kōnae.chmod(0o600)
            def manatoko_Ngā_Tautuhinga(anga, 화면):
                tuhi_Ngā_Tautuhinga({'user': 'user', 'ssh_password': anga, 'vnc_password': 화면})
                원본 = Ngā_Tautuhinga_kōnae.read_bytes()
                Whakarite(시험터)
                assert Ngā_Tautuhinga_kōnae.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Ngā_Tautuhinga_ara / 'Kōtaha.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Ngā_Tautuhinga_ara / 'Kōtaha.h').stat().st_mode & 0o777 == 0o600
            for anga, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                manatoko_Ngā_Tautuhinga(anga, 화면)
            pūrongo_uara['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for huri_uara, tāurunga_uara in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                raraunga = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                raraunga.update(huri_uara)
                tuhi_Ngā_Tautuhinga(raraunga)
                try:
                    Whakarite(시험터)
                except SystemExit as Pōhēhē:
                    assert tāurunga_uara in str(Pōhēhē), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + tāurunga_uara)
            pūrongo_uara['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Ngā_Tautuhinga = json.loads((whakaatu_pūtake / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            pūtūhono = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Pūranga_utauta = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def kawe_tono(인수, LOG_RECORD):
                subprocess.run(list(map(str, 인수)), cwd=str(whakaatu_pūtake), stdout=LOG_RECORD,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Ingoa, anga, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Ingoa, flush=True)
                manatoko_Ngā_Tautuhinga(anga, 화면)
                mēhua = 출력 / Ingoa
                mēhua.mkdir(exist_ok=True)
                with (mēhua / 'build.log').open('wb') as LOG_RECORD:
                    목적들 = []
                    for 원본 in sorted((whakaatu_pūtake / 'mamao_uara').glob('*.c')):
                        ūnga_uara = 시험터 / (원본.stem + '.o')
                        kawe_tono([번역기] + Ngā_Tautuhinga + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Ngā_Tautuhinga_ara, '-I', whakaatu_pūtake / 'mamao_uara', '-I', whakaatu_pūtake / 'vendor/libassh/src',
                             '-I', whakaatu_pūtake / 'vendor/bearssl/inc', '-I', whakaatu_pūtake / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ūnga_uara], LOG_RECORD)
                        목적들.append(ūnga_uara)
                    mamao_pūpū = 시험터 / 'libremote.a'
                    kawe_tono([Pūranga_utauta, 'rcs', mamao_pūpū] + 목적들, LOG_RECORD)
                    kawe_tono([pūtūhono, '--gc-sections', '-T', whakaatu_pūtake / '부팅/Hono_Tahora.ld', '-o', 시험터 / 'kernel.elf'] +
                         [whakaatu_pūtake / 'build' / (Ingoa + '.o') for Ingoa in ūnga_ingoa] + ['--start-group'] +
                         [mamao_pūpū if ara == 'remote/libremote.a' else whakaatu_pūtake / 'build' / ara for ara in puna] + ['--end-group'], LOG_RECORD)
                    kawe_tono([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_RECORD)
                with (mēhua / 'remote-test.log').open('wb') as LOG_RECORD:
                    kawe_tono(['python3', whakaatu_pūtake / 'Ngā_Utauta/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Ngā_Tautuhinga_kōnae, '--output', mēhua], LOG_RECORD)
                whakamana = json.loads((mēhua / 'report.json').read_text())
                assert whakamana['passed']
                pūrongo_uara['checks'].append(Ingoa + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        pūrongo_uara['passed'] = True
    finally:
        pūrongo_uara['personal_settings_unchanged'] = tautuhinga_whaiaro.read_bytes() == 원래설정
        if not pūrongo_uara['personal_settings_unchanged']:
            pūrongo_uara['passed'] = False
        pūrongo_uara['kernel_sha256'] = hashlib.sha256((whakaatu_pūtake / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(pūrongo_uara, ensure_ascii=False, indent=2) + '\n')
    assert pūrongo_uara['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(pūrongo_uara, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    whakahaere()
