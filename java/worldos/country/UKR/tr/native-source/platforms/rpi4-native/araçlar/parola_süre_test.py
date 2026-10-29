#!/usr/bin/env python3
"""개인 cxn_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from uzak_Ayarlar import Hazırlan
from COSL배포 import hedef_ad, kitaplık

işlem_kök = Path(__file__).resolve().parents[1]


def çalıştır():
    metinÇıktısı = işlem_kök / 'build/verification/password-length'
    metinÇıktısı.mkdir(parents=True, exist_ok=True)
    Kişisel_Ayarlar = işlem_kök / 'build/remote/access.json'
    원래설정 = Kişisel_Ayarlar.read_bytes()
    Rapor_değer = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            test_çalışma_alanı = Path(임시)
            Ayarlar_yol = test_çalışma_alanı / 'build/remote'
            Ayarlar_yol.mkdir(parents=True)
            Ayarlar_Dosya = Ayarlar_yol / 'access.json'
            def yazma_Ayarlar(veri):
                Ayarlar_Dosya.write_text(json.dumps(veri, ensure_ascii=False) + '\n')
                Ayarlar_Dosya.chmod(0o600)
            def doğrulamak_Ayarlar(kabuk, 화면):
                yazma_Ayarlar({'user': 'user', 'ssh_password': kabuk, 'vnc_password': 화면})
                원본 = Ayarlar_Dosya.read_bytes()
                Hazırlan(test_çalışma_alanı)
                assert Ayarlar_Dosya.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Ayarlar_yol / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Ayarlar_yol / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for kabuk, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                doğrulamak_Ayarlar(kabuk, 화면)
            Rapor_değer['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for değiştirmek_değer, girdi_değer in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                veri = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                veri.update(değiştirmek_değer)
                yazma_Ayarlar(veri)
                try:
                    Hazırlan(test_çalışma_alanı)
                except SystemExit as hata:
                    assert girdi_değer in str(hata), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + girdi_değer)
            Rapor_değer['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Ayarlar = json.loads((işlem_kök / 'build/remote/libassh-build.json').read_text())['flags']
            derleyici_araç = os.environ.get('ARM64_CC', 'clang')
            Bağlayıcı = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arşiv_araç = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def yürütmek_komut(bağımsız_değişkenler, LOG_KAYIT):
                subprocess.run(list(map(str, bağımsız_değişkenler)), cwd=str(işlem_kök), stdout=LOG_KAYIT,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for İsim, kabuk, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + İsim, flush=True)
                doğrulamak_Ayarlar(kabuk, 화면)
                sonuç = metinÇıktısı / İsim
                sonuç.mkdir(exist_ok=True)
                with (sonuç / 'build.log').open('wb') as LOG_KAYIT:
                    목적들 = []
                    for 원본 in sorted((işlem_kök / 'uzak_değer').glob('*.c')):
                        hedef_değer = test_çalışma_alanı / (원본.stem + '.o')
                        yürütmek_komut([derleyici_araç] + Ayarlar + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Ayarlar_yol, '-I', işlem_kök / 'uzak_değer', '-I', işlem_kök / 'vendor/libassh/src',
                             '-I', işlem_kök / 'vendor/bearssl/inc', '-I', işlem_kök / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', hedef_değer], LOG_KAYIT)
                        목적들.append(hedef_değer)
                    uzak_paket_iş = test_çalışma_alanı / 'libremote.a'
                    yürütmek_komut([Arşiv_araç, 'rcs', uzak_paket_iş] + 목적들, LOG_KAYIT)
                    yürütmek_komut([Bağlayıcı, '--gc-sections', '-T', işlem_kök / 'makine_başlatma/bağlama_düzeni.ld', '-o', test_çalışma_alanı / 'kernel.elf'] +
                         [işlem_kök / 'build' / (İsim + '.o') for İsim in hedef_ad] + ['--start-group'] +
                         [uzak_paket_iş if yol == 'remote/libremote.a' else işlem_kök / 'build' / yol for yol in kitaplık] + ['--end-group'], LOG_KAYIT)
                    yürütmek_komut([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         test_çalışma_alanı / 'kernel.elf', test_çalışma_alanı / 'kernel8.img'], LOG_KAYIT)
                with (sonuç / 'remote-test.log').open('wb') as LOG_KAYIT:
                    yürütmek_komut(['python3', işlem_kök / 'araçlar/uzak_bağlantı_test.py', '--kernel', test_çalışma_alanı / 'kernel8.img',
                         '--access', Ayarlar_Dosya, '--output', sonuç], LOG_KAYIT)
                doğrulamak_5fb2b747 = json.loads((sonuç / 'report.json').read_text())
                assert doğrulamak_5fb2b747['passed']
                Rapor_değer['checks'].append(İsim + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        Rapor_değer['passed'] = True
    finally:
        Rapor_değer['personal_settings_unchanged'] = Kişisel_Ayarlar.read_bytes() == 원래설정
        if not Rapor_değer['personal_settings_unchanged']:
            Rapor_değer['passed'] = False
        Rapor_değer['kernel_sha256'] = hashlib.sha256((işlem_kök / 'build/kernel8.img').read_bytes()).hexdigest()
        (metinÇıktısı / 'report.json').write_text(json.dumps(Rapor_değer, ensure_ascii=False, indent=2) + '\n')
    assert Rapor_değer['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(Rapor_değer, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    çalıştır()
