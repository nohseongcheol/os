#!/usr/bin/env python3
"""개인 కనెక్షన్_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from రిమోట్_సెట్టింగ్_లు import సిద్ధం_చేయు
from COSL배포 import గమ్యం_పేరు, లైబ్రరీ

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]


def నడుపుము():
    అవుట్పుట్ = ప్రొజెక్ట్_మూలం / 'build/verification/password-length'
    అవుట్పుట్.mkdir(parents=True, exist_ok=True)
    వ్యక్తిగత_అమర్పులు = ప్రొజెక్ట్_మూలం / 'build/remote/access.json'
    원래설정 = వ్యక్తిగత_అమర్పులు.read_bytes()
    నివేదిక_మూల్యం = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            సెట్టింగ్_లు_పథం = 시험터 / 'build/remote'
            సెట్టింగ్_లు_పథం.mkdir(parents=True)
            సెట్టింగ్_లు_ఫైలు = సెట్టింగ్_లు_పథం / 'access.json'
            def వ్రాయి_సెట్టింగ్_లు(డేటా):
                సెట్టింగ్_లు_ఫైలు.write_text(json.dumps(డేటా, ensure_ascii=False) + '\n')
                సెట్టింగ్_లు_ఫైలు.chmod(0o600)
            def సరిచూడు_సెట్టింగ్_లు(షెల్, 화면):
                వ్రాయి_సెట్టింగ్_లు({'user': 'user', 'ssh_password': షెల్, 'vnc_password': 화면})
                원본 = సెట్టింగ్_లు_ఫైలు.read_bytes()
                సిద్ధం_చేయు(시험터)
                assert సెట్టింగ్_లు_ఫైలు.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (సెట్టింగ్_లు_పథం / 'ప్రొఫైల్.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (సెట్టింగ్_లు_పథం / 'ప్రొఫైల్.h').stat().st_mode & 0o777 == 0o600
            for షెల్, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                సరిచూడు_సెట్టింగ్_లు(షెల్, 화면)
            నివేదిక_మూల్యం['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for మార్చు_మూల్యం, ప్రవేశం_మూల్యం in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                డేటా = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                డేటా.update(మార్చు_మూల్యం)
                వ్రాయి_సెట్టింగ్_లు(డేటా)
                try:
                    సిద్ధం_చేయు(시험터)
                except SystemExit as దోషం:
                    assert ప్రవేశం_మూల్యం in str(దోషం), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ప్రవేశం_మూల్యం)
            నివేదిక_మూల్యం['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            అమరికలు = json.loads((ప్రొజెక్ట్_మూలం / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            అనుసంధకం = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ఆర్కైవ్_ఉపకరణం = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def అమలు_చేయి_ఆదేశం(인수, లాగ్_వరుస):
                subprocess.run(list(map(str, 인수)), cwd=str(ప్రొజెక్ట్_మూలం), stdout=లాగ్_వరుస,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for పేరు, షెల్, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + పేరు, flush=True)
                సరిచూడు_సెట్టింగ్_లు(షెల్, 화면)
                ప్రమాణం = అవుట్పుట్ / పేరు
                ప్రమాణం.mkdir(exist_ok=True)
                with (ప్రమాణం / 'build.log').open('wb') as లాగ్_వరుస:
                    목적들 = []
                    for 원본 in sorted((ప్రొజెక్ట్_మూలం / 'రిమోట్_మూల్యం').glob('*.c')):
                        గమ్యం_మూల్యం = 시험터 / (원본.stem + '.o')
                        అమలు_చేయి_ఆదేశం([번역기] + అమరికలు + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', సెట్టింగ్_లు_పథం, '-I', ప్రొజెక్ట్_మూలం / 'రిమోట్_మూల్యం', '-I', ప్రొజెక్ట్_మూలం / 'vendor/libassh/src',
                             '-I', ప్రొజెక్ట్_మూలం / 'vendor/bearssl/inc', '-I', ప్రొజెక్ట్_మూలం / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', గమ్యం_మూల్యం], లాగ్_వరుస)
                        목적들.append(గమ్యం_మూల్యం)
                    రిమోట్_బండిల్ = 시험터 / 'libremote.a'
                    అమలు_చేయి_ఆదేశం([ఆర్కైవ్_ఉపకరణం, 'rcs', రిమోట్_బండిల్] + 목적들, లాగ్_వరుస)
                    అమలు_చేయి_ఆదేశం([అనుసంధకం, '--gc-sections', '-T', ప్రొజెక్ట్_మూలం / '부팅/బంధం_లేవుట్.ld', '-o', 시험터 / 'kernel.elf'] +
                         [ప్రొజెక్ట్_మూలం / 'build' / (పేరు + '.o') for పేరు in గమ్యం_పేరు] + ['--start-group'] +
                         [రిమోట్_బండిల్ if పాత్ == 'remote/libremote.a' else ప్రొజెక్ట్_మూలం / 'build' / పాత్ for పాత్ in లైబ్రరీ] + ['--end-group'], లాగ్_వరుస)
                    అమలు_చేయి_ఆదేశం([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], లాగ్_వరుస)
                with (ప్రమాణం / 'remote-test.log').open('wb') as లాగ్_వరుస:
                    అమలు_చేయి_ఆదేశం(['python3', ప్రొజెక్ట్_మూలం / 'ఉపకరణాలు/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', సెట్టింగ్_లు_ఫైలు, '--output', ప్రమాణం], లాగ్_వరుస)
                నిర్థారీకరించు = json.loads((ప్రమాణం / 'report.json').read_text())
                assert నిర్థారీకరించు['passed']
                నివేదిక_మూల్యం['checks'].append(పేరు + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        నివేదిక_మూల్యం['passed'] = True
    finally:
        నివేదిక_మూల్యం['personal_settings_unchanged'] = వ్యక్తిగత_అమర్పులు.read_bytes() == 원래설정
        if not నివేదిక_మూల్యం['personal_settings_unchanged']:
            నివేదిక_మూల్యం['passed'] = False
        నివేదిక_మూల్యం['kernel_sha256'] = hashlib.sha256((ప్రొజెక్ట్_మూలం / 'build/kernel8.img').read_bytes()).hexdigest()
        (అవుట్పుట్ / 'report.json').write_text(json.dumps(నివేదిక_మూల్యం, ensure_ascii=False, indent=2) + '\n')
    assert నివేదిక_మూల్యం['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(నివేదిక_మూల్యం, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    నడుపుము()
