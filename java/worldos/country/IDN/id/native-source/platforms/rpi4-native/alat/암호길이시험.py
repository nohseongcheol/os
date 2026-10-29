#!/usr/bin/env python3
"""개인 koneksi_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from jarak_jauh_Pengaturan import Siapkan
from COSL배포 import tujuan_nama, pustaka

Tugas_akar = Path(__file__).resolve().parents[1]


def jalankan():
    keluaranTeks = Tugas_akar / 'build/verification/password-length'
    keluaranTeks.mkdir(parents=True, exist_ok=True)
    penataan_pribadi = Tugas_akar / 'build/remote/access.json'
    원래설정 = penataan_pribadi.read_bytes()
    lapor_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Pengaturan_jalur = 시험터 / 'build/remote'
            Pengaturan_jalur.mkdir(parents=True)
            Pengaturan_file = Pengaturan_jalur / 'access.json'
            def tulis_Pengaturan(data):
                Pengaturan_file.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Pengaturan_file.chmod(0o600)
            def periksa_Pengaturan(shell, 화면):
                tulis_Pengaturan({'user': 'user', 'ssh_password': shell, 'vnc_password': 화면})
                원본 = Pengaturan_file.read_bytes()
                Siapkan(시험터)
                assert Pengaturan_file.read_bytes() == 원본, 'Settings were rewritten'
                kepala_VALUE = (Pengaturan_jalur / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', kepala_VALUE)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Pengaturan_jalur / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for shell, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                periksa_Pengaturan(shell, 화면)
            lapor_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ubah_VALUE, entri_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(ubah_VALUE)
                tulis_Pengaturan(data)
                try:
                    Siapkan(시험터)
                except SystemExit as galat:
                    assert entri_VALUE in str(galat), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + entri_VALUE)
            lapor_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Konfigurasi = json.loads((Tugas_akar / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Konektor = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arsip_alat = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Jalankan_perintah(argumen, LOG_baris):
                subprocess.run(list(map(str, argumen)), cwd=str(Tugas_akar), stdout=LOG_baris,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nama_2, shell, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nama_2, flush=True)
                periksa_Pengaturan(shell, 화면)
                hasil = keluaranTeks / Nama_2
                hasil.mkdir(exist_ok=True)
                with (hasil / 'build.log').open('wb') as LOG_baris:
                    목적들 = []
                    for 원본 in sorted((Tugas_akar / 'jarak_jauh_VALUE').glob('*.c')):
                        tujuan_VALUE = 시험터 / (원본.stem + '.o')
                        Jalankan_perintah([번역기] + Konfigurasi + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Pengaturan_jalur, '-I', Tugas_akar / 'jarak_jauh_VALUE', '-I', Tugas_akar / 'vendor/libassh/src',
                             '-I', Tugas_akar / 'vendor/bearssl/inc', '-I', Tugas_akar / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', tujuan_VALUE], LOG_baris)
                        목적들.append(tujuan_VALUE)
                    jarak_jauh_paket = 시험터 / 'libremote.a'
                    Jalankan_perintah([Arsip_alat, 'rcs', jarak_jauh_paket] + 목적들, LOG_baris)
                    Jalankan_perintah([Konektor, '--gc-sections', '-T', Tugas_akar / 'awal_mesin/tata_letak_penautan.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Tugas_akar / 'build' / (Nama_2 + '.o') for Nama_2 in tujuan_nama] + ['--start-group'] +
                         [jarak_jauh_paket if jalur == 'remote/libremote.a' else Tugas_akar / 'build' / jalur for jalur in pustaka] + ['--end-group'], LOG_baris)
                    Jalankan_perintah([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_baris)
                with (hasil / 'remote-test.log').open('wb') as LOG_baris:
                    Jalankan_perintah(['python3', Tugas_akar / 'alat/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Pengaturan_file, '--output', hasil], LOG_baris)
                validasi = json.loads((hasil / 'report.json').read_text())
                assert validasi['passed']
                lapor_VALUE['checks'].append(Nama_2 + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        lapor_VALUE['passed'] = True
    finally:
        lapor_VALUE['personal_settings_unchanged'] = penataan_pribadi.read_bytes() == 원래설정
        if not lapor_VALUE['personal_settings_unchanged']:
            lapor_VALUE['passed'] = False
        lapor_VALUE['kernel_sha256'] = hashlib.sha256((Tugas_akar / 'build/kernel8.img').read_bytes()).hexdigest()
        (keluaranTeks / 'report.json').write_text(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert lapor_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    jalankan()
