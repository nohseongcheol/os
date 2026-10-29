#!/usr/bin/env python3
"""개인 jokkalóo_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from lu_soree_Jekkal_yi import jël_matuwaay
from COSL배포 import jëmmukaay_tur, daaray_téere

기준 = Path(__file__).resolve().parents[1]


def daw():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    rañeefi_sa_bopp = 기준 / 'build/remote/access.json'
    원래설정 = rañeefi_sa_bopp.read_bytes()
    tënk_xëyma = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Jekkal_yi_Yoonu_jëmale = 시험터 / 'build/remote'
            Jekkal_yi_Yoonu_jëmale.mkdir(parents=True)
            Jekkal_yi_bara_denc = Jekkal_yi_Yoonu_jëmale / 'access.json'
            def biir_Jekkal_yi(mbir):
                Jekkal_yi_bara_denc.write_text(json.dumps(mbir, ensure_ascii=False) + '\n')
                Jekkal_yi_bara_denc.chmod(0o600)
            def luñutu_Jekkal_yi(Wëreef, 화면):
                biir_Jekkal_yi({'user': 'user', 'ssh_password': Wëreef, 'vnc_password': 화면})
                원본 = Jekkal_yi_bara_denc.read_bytes()
                jël_matuwaay(시험터)
                assert Jekkal_yi_bara_denc.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Jekkal_yi_Yoonu_jëmale / 'profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Jekkal_yi_Yoonu_jëmale / 'profil.h').stat().st_mode & 0o777 == 0o600
            for Wëreef, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                luñutu_Jekkal_yi(Wëreef, 화면)
            tënk_xëyma['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for soppi_xëyma_16f64fe4, dugal_xabaar_xëyma in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                mbir = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                mbir.update(soppi_xëyma_16f64fe4)
                biir_Jekkal_yi(mbir)
                try:
                    jël_matuwaay(시험터)
                except SystemExit as njumte:
                    assert dugal_xabaar_xëyma in str(njumte), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + dugal_xabaar_xëyma)
            tënk_xëyma['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Jekkal_yi = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Jokkalóo = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            denc_jumtukaay = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def def_ndigel(인수, làq_Dënk):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=làq_Dënk,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for tur_253d1510, Wëreef, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + tur_253d1510, flush=True)
                luñutu_Jekkal_yi(Wëreef, 화면)
                결과 = 출력 / tur_253d1510
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as làq_Dënk:
                    목적들 = []
                    for 원본 in sorted((기준 / 'lu_soree_xëyma').glob('*.c')):
                        jëmmukaay_xëyma = 시험터 / (원본.stem + '.o')
                        def_ndigel([번역기] + Jekkal_yi + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Jekkal_yi_Yoonu_jëmale, '-I', 기준 / 'lu_soree_xëyma', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', jëmmukaay_xëyma], làq_Dënk)
                        목적들.append(jëmmukaay_xëyma)
                    lu_soree_takku_xéewël = 시험터 / 'libremote.a'
                    def_ndigel([denc_jumtukaay, 'rcs', lu_soree_takku_xéewël] + 목적들, làq_Dënk)
                    def_ndigel([Jokkalóo, '--gc-sections', '-T', 기준 / '부팅/lëkkale_Tëralin.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (tur_253d1510 + '.o') for tur_253d1510 in jëmmukaay_tur] + ['--start-group'] +
                         [lu_soree_takku_xéewël if Yoonu_jëmale == 'remote/libremote.a' else 기준 / 'build' / Yoonu_jëmale for Yoonu_jëmale in daaray_téere] + ['--end-group'], làq_Dënk)
                    def_ndigel([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], làq_Dënk)
                with (결과 / 'remote-test.log').open('wb') as làq_Dënk:
                    def_ndigel(['python3', 기준 / 'Jumtukaay_yi/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Jekkal_yi_bara_denc, '--output', 결과], làq_Dënk)
                wéral = json.loads((결과 / 'report.json').read_text())
                assert wéral['passed']
                tënk_xëyma['checks'].append(tur_253d1510 + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        tënk_xëyma['passed'] = True
    finally:
        tënk_xëyma['personal_settings_unchanged'] = rañeefi_sa_bopp.read_bytes() == 원래설정
        if not tënk_xëyma['personal_settings_unchanged']:
            tënk_xëyma['passed'] = False
        tënk_xëyma['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(tënk_xëyma, ensure_ascii=False, indent=2) + '\n')
    assert tënk_xëyma['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(tënk_xëyma, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    daw()
