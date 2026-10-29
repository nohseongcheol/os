#!/usr/bin/env python3
"""개인 hubungan_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from jauh_Seting import Sediakan
from COSL배포 import destinasi_nama, pustaka

projek_akar = Path(__file__).resolve().parents[1]


def Jalan():
    출력 = projek_akar / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    seting_peribadi = projek_akar / 'build/remote/access.json'
    원래설정 = seting_peribadi.read_bytes()
    lapor_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            ujian_ruang_kerja = Path(임시)
            Seting_laluan = ujian_ruang_kerja / 'build/remote'
            Seting_laluan.mkdir(parents=True)
            Seting_fail = Seting_laluan / 'access.json'
            def tulis_Seting(data):
                Seting_fail.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Seting_fail.chmod(0o600)
            def tentu_sahkan_Seting(cangkerang, 화면):
                tulis_Seting({'user': 'user', 'ssh_password': cangkerang, 'vnc_password': 화면})
                원본 = Seting_fail.read_bytes()
                Sediakan(ujian_ruang_kerja)
                assert Seting_fail.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Seting_laluan / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Seting_laluan / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for cangkerang, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                tentu_sahkan_Seting(cangkerang, 화면)
            lapor_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ubah_VALUE, pemasukan_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(ubah_VALUE)
                tulis_Seting(data)
                try:
                    Sediakan(ujian_ruang_kerja)
                except SystemExit as RALAT:
                    assert pemasukan_VALUE in str(RALAT), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + pemasukan_VALUE)
            lapor_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Tetapan = json.loads((projek_akar / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Penyambung = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arkib_alat = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def laksanakan_perintah(인수, LOG_baris):
                subprocess.run(list(map(str, 인수)), cwd=str(projek_akar), stdout=LOG_baris,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nama, cangkerang, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nama, flush=True)
                tentu_sahkan_Seting(cangkerang, 화면)
                ukuran = 출력 / Nama
                ukuran.mkdir(exist_ok=True)
                with (ukuran / 'build.log').open('wb') as LOG_baris:
                    목적들 = []
                    for 원본 in sorted((projek_akar / 'jauh_VALUE').glob('*.c')):
                        destinasi_VALUE = ujian_ruang_kerja / (원본.stem + '.o')
                        laksanakan_perintah([번역기] + Tetapan + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Seting_laluan, '-I', projek_akar / 'jauh_VALUE', '-I', projek_akar / 'vendor/libassh/src',
                             '-I', projek_akar / 'vendor/bearssl/inc', '-I', projek_akar / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', destinasi_VALUE], LOG_baris)
                        목적들.append(destinasi_VALUE)
                    jauh_pakej = ujian_ruang_kerja / 'libremote.a'
                    laksanakan_perintah([Arkib_alat, 'rcs', jauh_pakej] + 목적들, LOG_baris)
                    laksanakan_perintah([Penyambung, '--gc-sections', '-T', projek_akar / 'permulaan_mesin/susun_atur_pautan.ld', '-o', ujian_ruang_kerja / 'kernel.elf'] +
                         [projek_akar / 'build' / (Nama + '.o') for Nama in destinasi_nama] + ['--start-group'] +
                         [jauh_pakej if LALUAN == 'remote/libremote.a' else projek_akar / 'build' / LALUAN for LALUAN in pustaka] + ['--end-group'], LOG_baris)
                    laksanakan_perintah([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         ujian_ruang_kerja / 'kernel.elf', ujian_ruang_kerja / 'kernel8.img'], LOG_baris)
                with (ukuran / 'remote-test.log').open('wb') as LOG_baris:
                    laksanakan_perintah(['python3', projek_akar / 'alat/sambungan_jauh_ujian.py', '--kernel', ujian_ruang_kerja / 'kernel8.img',
                         '--access', Seting_fail, '--output', ukuran], LOG_baris)
                sahkan = json.loads((ukuran / 'report.json').read_text())
                assert sahkan['passed']
                lapor_VALUE['checks'].append(Nama + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        lapor_VALUE['passed'] = True
    finally:
        lapor_VALUE['personal_settings_unchanged'] = seting_peribadi.read_bytes() == 원래설정
        if not lapor_VALUE['personal_settings_unchanged']:
            lapor_VALUE['passed'] = False
        lapor_VALUE['kernel_sha256'] = hashlib.sha256((projek_akar / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert lapor_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Jalan()
