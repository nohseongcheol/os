#!/usr/bin/env python3
"""개인 കണക്ഷൻ_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from വിദൂര_ക്രമീകരണം import തയ്യാറാക്കുക
from COSL배포 import ഉദ്ദിഷ്ടസ്ഥാനം_നാ_മം, లైబ్రరీ

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]


def നടപ്പിലാക്കുക():
    ഫലം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/verification/password-length'
    ഫലം.mkdir(parents=True, exist_ok=True)
    സ്വകാര്യ_സജ്ജീകരണം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/remote/access.json'
    원래설정 = സ്വകാര്യ_സജ്ജീകരണം.read_bytes()
    నివేదిక_മൂല്യം = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            ക്രമീകരണം_പാത = 시험터 / 'build/remote'
            ക്രമീകരണം_പാത.mkdir(parents=True)
            ക്രമീകരണം_ഫയല് = ക്രമീകരണം_പാത / 'access.json'
            def റൈറ്റ്_ചെയ്യുക_ക്രമീകരണം(ഡാറ്റാ):
                ക്രമീകരണം_ഫയല്.write_text(json.dumps(ഡാറ്റാ, ensure_ascii=False) + '\n')
                ക്രമീകരണം_ഫയല്.chmod(0o600)
            def പരിശോധിക്കുക_ക്രമീകരണം(ഷെല്, 화면):
                റൈറ്റ്_ചെയ്യുക_ക്രമീകരണം({'user': 'user', 'ssh_password': ഷെല്, 'vnc_password': 화면})
                원본 = ക്രമീകരണം_ഫയല്.read_bytes()
                തയ്യാറാക്കുക(시험터)
                assert ക്രമീകരണം_ഫയല്.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (ക്രമീകരണം_പാത / 'പ്രൊഫൈൽ.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (ക്രമീകരണം_പാത / 'പ്രൊഫൈൽ.h').stat().st_mode & 0o777 == 0o600
            for ഷെല്, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                പരിശോധിക്കുക_ക്രമീകരണം(ഷെല്, 화면)
            నివేదిక_മൂല്യം['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for മാറ്റികൊടുക്കുക_മൂല്യം, എന്_ട്രി_മൂല്യം in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ഡാറ്റാ = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ഡാറ്റാ.update(മാറ്റികൊടുക്കുക_മൂല്യം)
                റൈറ്റ്_ചെയ്യുക_ക്രമീകരണം(ഡാറ്റാ)
                try:
                    തയ്യാറാക്കുക(시험터)
                except SystemExit as പിശക്:
                    assert എന്_ട്രി_മൂല്യം in str(പിശക്), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + എന്_ട്രി_മൂല്യം)
            నివేదిక_മൂല്യം['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            സജ്ജീകരണം = json.loads((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            കണക്ടര് = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ശേഖരം_ഉപകരണം = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def നടപ്പാക്കുക_കമാന്_ഡ്(인수, ലോഗ്_രേഖ):
                subprocess.run(list(map(str, 인수)), cwd=str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം), stdout=ലോഗ്_രേഖ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for പേരു്, ഷെല്, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + പേരു്, flush=True)
                പരിശോധിക്കുക_ക്രമീകരണം(ഷെല്, 화면)
                അളവ് = ഫലം / പേരു്
                അളവ്.mkdir(exist_ok=True)
                with (അളവ് / 'build.log').open('wb') as ലോഗ്_രേഖ:
                    목적들 = []
                    for 원본 in sorted((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'വിദൂര_മൂല്യം').glob('*.c')):
                        ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം = 시험터 / (원본.stem + '.o')
                        നടപ്പാക്കുക_കമാന്_ഡ്([번역기] + സജ്ജീകരണം + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', ക്രമീകരണം_പാത, '-I', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'വിദൂര_മൂല്യം', '-I', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor/libassh/src',
                             '-I', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor/bearssl/inc', '-I', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം], ലോഗ്_രേഖ)
                        목적들.append(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം)
                    വിദൂര_ബണ്ടിൽ = 시험터 / 'libremote.a'
                    നടപ്പാക്കുക_കമാന്_ഡ്([ശേഖരം_ഉപകരണം, 'rcs', വിദൂര_ബണ്ടിൽ] + 목적들, ലോഗ്_രേഖ)
                    നടപ്പാക്കുക_കമാന്_ഡ്([കണക്ടര്, '--gc-sections', '-T', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '부팅/ലിങ്ക്_ലേഔട്ട്.ld', '-o', 시험터 / 'kernel.elf'] +
                         [പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build' / (പേരു് + '.o') for പേരു് in ഉദ്ദിഷ്ടസ്ഥാനം_നാ_മം] + ['--start-group'] +
                         [വിദൂര_ബണ്ടിൽ if വഴി == 'remote/libremote.a' else പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build' / വഴി for വഴി in లైబ్రరీ] + ['--end-group'], ലോഗ്_രേഖ)
                    നടപ്പാക്കുക_കമാന്_ഡ്([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], ലോഗ്_രേഖ)
                with (അളവ് / 'remote-test.log').open('wb') as ലോഗ്_രേഖ:
                    നടപ്പാക്കുക_കമാന്_ഡ്(['python3', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉപകരണങ്ങൾ/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', ക്രമീകരണം_ഫയല്, '--output', അളവ്], ലോഗ്_രേഖ)
                സാധൂകരിക്കുക = json.loads((അളവ് / 'report.json').read_text())
                assert സാധൂകരിക്കുക['passed']
                నివేదిక_മൂല്യം['checks'].append(പേരു് + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        నివేదిక_മൂല്യം['passed'] = True
    finally:
        నివేదిక_മൂല്യം['personal_settings_unchanged'] = സ്വകാര്യ_സജ്ജീകരണം.read_bytes() == 원래설정
        if not నివేదిక_മൂല്യം['personal_settings_unchanged']:
            నివేదిక_മൂല്യം['passed'] = False
        నివేదిక_മൂല്യം['kernel_sha256'] = hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel8.img').read_bytes()).hexdigest()
        (ഫലം / 'report.json').write_text(json.dumps(నివేదిక_മൂല്യം, ensure_ascii=False, indent=2) + '\n')
    assert నివేదిక_മൂല്യം['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(నివేదిక_മൂല്യം, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    നടപ്പിലാക്കുക()
