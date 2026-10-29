#!/usr/bin/env python3
"""개인 සබැඳුම_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from දුරස්ථ_පසුතල import පිළියෙල_කරන්න
from COSL배포 import ගමනාන්තය_නම, ලේඛාගාරය

기준 = Path(__file__).resolve().parents[1]


def ක්_රියාත්මක_කරන්න_2():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    පෞද්ගලික_සිටුවම් = 기준 / 'build/remote/access.json'
    원래설정 = පෞද්ගලික_සිටුවම්.read_bytes()
    වාර්තාව_අගය = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            පසුතල_පෙත = 시험터 / 'build/remote'
            පසුතල_පෙත.mkdir(parents=True)
            පසුතල_ගොනුව = පසුතල_පෙත / 'access.json'
            def ලියන්න_පසුතල(දත්ත):
                පසුතල_ගොනුව.write_text(json.dumps(දත්ත, ensure_ascii=False) + '\n')
                පසුතල_ගොනුව.chmod(0o600)
            def තහවුරු_කරන්න_පසුතල(කවචය, 화면):
                ලියන්න_පසුතල({'user': 'user', 'ssh_password': කවචය, 'vnc_password': 화면})
                원본 = පසුතල_ගොනුව.read_bytes()
                පිළියෙල_කරන්න(시험터)
                assert පසුතල_ගොනුව.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (පසුතල_පෙත / 'පැතිකඩ.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (පසුතල_පෙත / 'පැතිකඩ.h').stat().st_mode & 0o777 == 0o600
            for කවචය, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                තහවුරු_කරන්න_පසුතල(කවචය, 화면)
            වාර්තාව_අගය['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for වෙනස්_කරන්න_අගය, පිවිසුම_අගය in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                දත්ත = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                දත්ත.update(වෙනස්_කරන්න_අගය)
                ලියන්න_පසුතල(දත්ත)
                try:
                    පිළියෙල_කරන්න(시험터)
                except SystemExit as දෝෂය:
                    assert පිවිසුම_අගය in str(දෝෂය), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + පිවිසුම_අගය)
            වාර්තාව_අගය['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            සැකසුම් = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            සම්බන්ධකය = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            සංරක්ෂිතය_මෙවලම = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ක්_රියාත්මක_කරන්න_විධානය(විස්තාරක, ලොගය_පේළිය):
                subprocess.run(list(map(str, විස්තාරක)), cwd=str(기준), stdout=ලොගය_පේළිය,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for නම, කවචය, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + නම, flush=True)
                තහවුරු_කරන්න_පසුතල(කවචය, 화면)
                결과 = 출력 / නම
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as ලොගය_පේළිය:
                    목적들 = []
                    for 원본 in sorted((기준 / 'දුරස්ථ_අගය').glob('*.c')):
                        ගමනාන්තය_අගය = 시험터 / (원본.stem + '.o')
                        ක්_රියාත්මක_කරන්න_විධානය([번역기] + සැකසුම් + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', පසුතල_පෙත, '-I', 기준 / 'දුරස්ථ_අගය', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ගමනාන්තය_අගය], ලොගය_පේළිය)
                        목적들.append(ගමනාන්තය_අගය)
                    දුරස්ථ_පොදිය = 시험터 / 'libremote.a'
                    ක්_රියාත්මක_කරන්න_විධානය([සංරක්ෂිතය_මෙවලම, 'rcs', දුරස්ථ_පොදිය] + 목적들, ලොගය_පේළිය)
                    ක්_රියාත්මක_කරන්න_විධානය([සම්බන්ධකය, '--gc-sections', '-T', 기준 / '부팅/සබැඳිය_සැකැස්ම.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (නම + '.o') for නම in ගමනාන්තය_නම] + ['--start-group'] +
                         [දුරස්ථ_පොදිය if මාර්_ගය == 'remote/libremote.a' else 기준 / 'build' / මාර්_ගය for මාර්_ගය in ලේඛාගාරය] + ['--end-group'], ලොගය_පේළිය)
                    ක්_රියාත්මක_කරන්න_විධානය([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], ලොගය_පේළිය)
                with (결과 / 'remote-test.log').open('wb') as ලොගය_පේළිය:
                    ක්_රියාත්මක_කරන්න_විධානය(['python3', 기준 / 'මෙවලම්/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', පසුතල_ගොනුව, '--output', 결과], ලොගය_පේළිය)
                වලංගු_කරන්න = json.loads((결과 / 'report.json').read_text())
                assert වලංගු_කරන්න['passed']
                වාර්තාව_අගය['checks'].append(නම + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        වාර්තාව_අගය['passed'] = True
    finally:
        වාර්තාව_අගය['personal_settings_unchanged'] = පෞද්ගලික_සිටුවම්.read_bytes() == 원래설정
        if not වාර්තාව_අගය['personal_settings_unchanged']:
            වාර්තාව_අගය['passed'] = False
        වාර්තාව_අගය['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(වාර්තාව_අගය, ensure_ascii=False, indent=2) + '\n')
    assert වාර්තාව_අගය['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(වාර්තාව_අගය, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_2()
