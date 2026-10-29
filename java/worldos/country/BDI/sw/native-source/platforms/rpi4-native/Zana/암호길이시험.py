#!/usr/bin/env python3
"""개인 muunganisho_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from kwa_mbali_Mipangilio import Andaa
from COSL배포 import fikio_jina, maktaba

기준 = Path(__file__).resolve().parents[1]


def endesha():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    mipangizo_binafsi = 기준 / 'build/remote/access.json'
    원래설정 = mipangizo_binafsi.read_bytes()
    ripoti_thamani = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Mipangilio_njia = 시험터 / 'build/remote'
            Mipangilio_njia.mkdir(parents=True)
            Mipangilio_faili = Mipangilio_njia / 'access.json'
            def andika_Mipangilio(data):
                Mipangilio_faili.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Mipangilio_faili.chmod(0o600)
            def thibitisha_Mipangilio(sheli, 화면):
                andika_Mipangilio({'user': 'user', 'ssh_password': sheli, 'vnc_password': 화면})
                원본 = Mipangilio_faili.read_bytes()
                Andaa(시험터)
                assert Mipangilio_faili.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Mipangilio_njia / 'Maelezo_mafupi.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Mipangilio_njia / 'Maelezo_mafupi.h').stat().st_mode & 0o777 == 0o600
            for sheli, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                thibitisha_Mipangilio(sheli, 화면)
            ripoti_thamani['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for badilisha_thamani_16f64fe4, ingizo_thamani in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(badilisha_thamani_16f64fe4)
                andika_Mipangilio(data)
                try:
                    Andaa(시험터)
                except SystemExit as kosa:
                    assert ingizo_thamani in str(kosa), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ingizo_thamani)
            ripoti_thamani['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Mipangilio = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            kiunganisho = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Hifadhi_zana = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def tekeleza_amri(인수, batli_REKODI):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=batli_REKODI,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Jina, sheli, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Jina, flush=True)
                thibitisha_Mipangilio(sheli, 화면)
                결과 = 출력 / Jina
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as batli_REKODI:
                    목적들 = []
                    for 원본 in sorted((기준 / 'kwa_mbali_thamani').glob('*.c')):
                        fikio_thamani = 시험터 / (원본.stem + '.o')
                        tekeleza_amri([번역기] + Mipangilio + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Mipangilio_njia, '-I', 기준 / 'kwa_mbali_thamani', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', fikio_thamani], batli_REKODI)
                        목적들.append(fikio_thamani)
                    kwa_mbali_fungasha = 시험터 / 'libremote.a'
                    tekeleza_amri([Hifadhi_zana, 'rcs', kwa_mbali_fungasha] + 목적들, batli_REKODI)
                    tekeleza_amri([kiunganisho, '--gc-sections', '-T', 기준 / '부팅/Kiungo_Muundo.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Jina + '.o') for Jina in fikio_jina] + ['--start-group'] +
                         [kwa_mbali_fungasha if njia == 'remote/libremote.a' else 기준 / 'build' / njia for njia in maktaba] + ['--end-group'], batli_REKODI)
                    tekeleza_amri([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], batli_REKODI)
                with (결과 / 'remote-test.log').open('wb') as batli_REKODI:
                    tekeleza_amri(['python3', 기준 / 'Zana/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Mipangilio_faili, '--output', 결과], batli_REKODI)
                hakikisha = json.loads((결과 / 'report.json').read_text())
                assert hakikisha['passed']
                ripoti_thamani['checks'].append(Jina + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ripoti_thamani['passed'] = True
    finally:
        ripoti_thamani['personal_settings_unchanged'] = mipangizo_binafsi.read_bytes() == 원래설정
        if not ripoti_thamani['personal_settings_unchanged']:
            ripoti_thamani['passed'] = False
        ripoti_thamani['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(ripoti_thamani, ensure_ascii=False, indent=2) + '\n')
    assert ripoti_thamani['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ripoti_thamani, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    endesha()
