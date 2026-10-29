#!/usr/bin/env python3
"""개인 ସଂଯୋଗ_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from ଦୂରବର୍ତ୍ତୀ_ସେଟିଂସ୍ import ପ୍ରସ୍ତୁତ
from COSL배포 import ଲକ୍ଷସ୍ଥଳ_ନାମ, ଲାଇବ୍ରେରୀ

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]


def ଚଳାନ୍ତୁ():
    ନିର୍ଗମ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/verification/password-length'
    ନିର୍ଗମ.mkdir(parents=True, exist_ok=True)
    ବ୍ୟକ୍ତିଗତ_ସେଟିଙ୍ଗସ୍ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/remote/access.json'
    원래설정 = ବ୍ୟକ୍ତିଗତ_ସେଟିଙ୍ଗସ୍.read_bytes()
    ରିପୋର୍ଟ_ମୂଲ୍ୟ = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            ସେଟିଂସ୍_ପଥ = 시험터 / 'build/remote'
            ସେଟିଂସ୍_ପଥ.mkdir(parents=True)
            ସେଟିଂସ୍_ଫାଇଲ୍ = ସେଟିଂସ୍_ପଥ / 'access.json'
            def ଲିଖନ_ସେଟିଂସ୍(ଡାଟା):
                ସେଟିଂସ୍_ଫାଇଲ୍.write_text(json.dumps(ଡାଟା, ensure_ascii=False) + '\n')
                ସେଟିଂସ୍_ଫାଇଲ୍.chmod(0o600)
            def ଯାଞ୍ଚ୍_କରିବା_ସେଟିଂସ୍(ଖୋଳ, 화면):
                ଲିଖନ_ସେଟିଂସ୍({'user': 'user', 'ssh_password': ଖୋଳ, 'vnc_password': 화면})
                원본 = ସେଟିଂସ୍_ଫାଇଲ୍.read_bytes()
                ପ୍ରସ୍ତୁତ(시험터)
                assert ସେଟିଂସ୍_ଫାଇଲ୍.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (ସେଟିଂସ୍_ପଥ / 'ପ୍ରୋଫାଇଲ୍.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (ସେଟିଂସ୍_ପଥ / 'ପ୍ରୋଫାଇଲ୍.h').stat().st_mode & 0o777 == 0o600
            for ଖୋଳ, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ଯାଞ୍ଚ୍_କରିବା_ସେଟିଂସ୍(ଖୋଳ, 화면)
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ପରିବର୍ତ୍ତନ_ମୂଲ୍ୟ, ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ଡାଟା = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ଡାଟା.update(ପରିବର୍ତ୍ତନ_ମୂଲ୍ୟ)
                ଲିଖନ_ସେଟିଂସ୍(ଡାଟା)
                try:
                    ପ୍ରସ୍ତୁତ(시험터)
                except SystemExit as ତ୍ରୁଟି:
                    assert ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in str(ତ୍ରୁଟି), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ)
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ବିନ୍ଯାସ = json.loads((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            ସଂଲଗ୍ନକ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ଅଭିଲେଖାଗାର_ଉପକରଣ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(인수, ଲଗ୍_ଧାଡ଼ି):
                subprocess.run(list(map(str, 인수)), cwd=str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍), stdout=ଲଗ୍_ଧାଡ଼ି,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ନାମ, ଖୋଳ, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ନାମ, flush=True)
                ଯାଞ୍ଚ୍_କରିବା_ସେଟିଂସ୍(ଖୋଳ, 화면)
                ମାପ = ନିର୍ଗମ / ନାମ
                ମାପ.mkdir(exist_ok=True)
                with (ମାପ / 'build.log').open('wb') as ଲଗ୍_ଧାଡ଼ି:
                    목적들 = []
                    for 원본 in sorted((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ').glob('*.c')):
                        ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = 시험터 / (원본.stem + '.o')
                        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([번역기] + ବିନ୍ଯାସ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', ସେଟିଂସ୍_ପଥ, '-I', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ', '-I', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/libassh/src',
                             '-I', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/bearssl/inc', '-I', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ], ଲଗ୍_ଧାଡ଼ି)
                        목적들.append(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ)
                    ଦୂରବର୍ତ୍ତୀ_ବଣ୍ଡଲ୍ = 시험터 / 'libremote.a'
                    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([ଅଭିଲେଖାଗାର_ଉପକରଣ, 'rcs', ଦୂରବର୍ତ୍ତୀ_ବଣ୍ଡଲ୍] + 목적들, ଲଗ୍_ଧାଡ଼ି)
                    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([ସଂଲଗ୍ନକ, '--gc-sections', '-T', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '부팅/ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld', '-o', 시험터 / 'kernel.elf'] +
                         [ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build' / (ନାମ + '.o') for ନାମ in ଲକ୍ଷସ୍ଥଳ_ନାମ] + ['--start-group'] +
                         [ଦୂରବର୍ତ୍ତୀ_ବଣ୍ଡଲ୍ if ପଥ == 'remote/libremote.a' else ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build' / ପଥ for ପଥ in ଲାଇବ୍ରେରୀ] + ['--end-group'], ଲଗ୍_ଧାଡ଼ି)
                    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], ଲଗ୍_ଧାଡ଼ି)
                with (ମାପ / 'remote-test.log').open('wb') as ଲଗ୍_ଧାଡ଼ି:
                    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(['python3', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉପକରଣସମୂହ/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', ସେଟିଂସ୍_ଫାଇଲ୍, '--output', ମାପ], ଲଗ୍_ଧାଡ଼ି)
                ବୈଧକରଣ = json.loads((ମାପ / 'report.json').read_text())
                assert ବୈଧକରଣ['passed']
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append(ନାମ + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ରିପୋର୍ଟ_ମୂଲ୍ୟ['passed'] = True
    finally:
        ରିପୋର୍ଟ_ମୂଲ୍ୟ['personal_settings_unchanged'] = ବ୍ୟକ୍ତିଗତ_ସେଟିଙ୍ଗସ୍.read_bytes() == 원래설정
        if not ରିପୋର୍ଟ_ମୂଲ୍ୟ['personal_settings_unchanged']:
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['passed'] = False
        ରିପୋର୍ଟ_ମୂଲ୍ୟ['kernel_sha256'] = hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel8.img').read_bytes()).hexdigest()
        (ନିର୍ଗମ / 'report.json').write_text(json.dumps(ରିପୋର୍ଟ_ମୂଲ୍ୟ, ensure_ascii=False, indent=2) + '\n')
    assert ରିପୋର୍ଟ_ମୂଲ୍ୟ['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ରିପୋର୍ଟ_ମୂଲ୍ୟ, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ଚଳାନ୍ତୁ()
