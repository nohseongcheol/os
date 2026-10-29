#!/usr/bin/env python3
"""개인 કનેક્શન_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from રિમોટ_સેટિંગ્સ import તૈયાર_કરો
from COSL배포 import ગંતવ્ય_નામ, લાઇબ્રેરી

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]


def ચલાવો_2():
    આઉટપુટ = પ્રોજેક્ટ_રૂટ / 'build/verification/password-length'
    આઉટપુટ.mkdir(parents=True, exist_ok=True)
    વ્યક્તિગત_સેટિંગ્સ = પ્રોજેક્ટ_રૂટ / 'build/remote/access.json'
    원래설정 = વ્યક્તિગત_સેટિંગ્સ.read_bytes()
    અહેવાલ_મૂલ્ય = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            સેટિંગ્સ_પાથ = 시험터 / 'build/remote'
            સેટિંગ્સ_પાથ.mkdir(parents=True)
            સેટિંગ્સ_ફાઇલ = સેટિંગ્સ_પાથ / 'access.json'
            def લખો_સેટિંગ્સ(ડેટા):
                સેટિંગ્સ_ફાઇલ.write_text(json.dumps(ડેટા, ensure_ascii=False) + '\n')
                સેટિંગ્સ_ફાઇલ.chmod(0o600)
            def ચકાસવું_સેટિંગ્સ(શેલ, 화면):
                લખો_સેટિંગ્સ({'user': 'user', 'ssh_password': શેલ, 'vnc_password': 화면})
                원본 = સેટિંગ્સ_ફાઇલ.read_bytes()
                તૈયાર_કરો(시험터)
                assert સેટિંગ્સ_ફાઇલ.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (સેટિંગ્સ_પાથ / 'પ્રોફાઇલ.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (સેટિંગ્સ_પાથ / 'પ્રોફાઇલ.h').stat().st_mode & 0o777 == 0o600
            for શેલ, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ચકાસવું_સેટિંગ્સ(શેલ, 화면)
            અહેવાલ_મૂલ્ય['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for પરિવર્તન_કરો_મૂલ્ય, પ્રવેશ_મૂલ્ય in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ડેટા = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ડેટા.update(પરિવર્તન_કરો_મૂલ્ય)
                લખો_સેટિંગ્સ(ડેટા)
                try:
                    તૈયાર_કરો(시험터)
                except SystemExit as ભૂલ:
                    assert પ્રવેશ_મૂલ્ય in str(ભૂલ), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + પ્રવેશ_મૂલ્ય)
            અહેવાલ_મૂલ્ય['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            સુયોજના = json.loads((પ્રોજેક્ટ_રૂટ / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            કનેક્ટર = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            સંગ્રહ_ઉપકરણ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def અમલ_કરો_આદેશ(દલીલો, લૉગ_પંક્તિ):
                subprocess.run(list(map(str, દલીલો)), cwd=str(પ્રોજેક્ટ_રૂટ), stdout=લૉગ_પંક્તિ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for નામ, શેલ, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + નામ, flush=True)
                ચકાસવું_સેટિંગ્સ(શેલ, 화면)
                પરિમાણ = આઉટપુટ / નામ
                પરિમાણ.mkdir(exist_ok=True)
                with (પરિમાણ / 'build.log').open('wb') as લૉગ_પંક્તિ:
                    목적들 = []
                    for 원본 in sorted((પ્રોજેક્ટ_રૂટ / 'રિમોટ_મૂલ્ય').glob('*.c')):
                        ગંતવ્ય_મૂલ્ય = 시험터 / (원본.stem + '.o')
                        અમલ_કરો_આદેશ([번역기] + સુયોજના + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', સેટિંગ્સ_પાથ, '-I', પ્રોજેક્ટ_રૂટ / 'રિમોટ_મૂલ્ય', '-I', પ્રોજેક્ટ_રૂટ / 'vendor/libassh/src',
                             '-I', પ્રોજેક્ટ_રૂટ / 'vendor/bearssl/inc', '-I', પ્રોજેક્ટ_રૂટ / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ગંતવ્ય_મૂલ્ય], લૉગ_પંક્તિ)
                        목적들.append(ગંતવ્ય_મૂલ્ય)
                    રિમોટ_બન્ડલ = 시험터 / 'libremote.a'
                    અમલ_કરો_આદેશ([સંગ્રહ_ઉપકરણ, 'rcs', રિમોટ_બન્ડલ] + 목적들, લૉગ_પંક્તિ)
                    અમલ_કરો_આદેશ([કનેક્ટર, '--gc-sections', '-T', પ્રોજેક્ટ_રૂટ / '부팅/લિંક_લેઆઉટ.ld', '-o', 시험터 / 'kernel.elf'] +
                         [પ્રોજેક્ટ_રૂટ / 'build' / (નામ + '.o') for નામ in ગંતવ્ય_નામ] + ['--start-group'] +
                         [રિમોટ_બન્ડલ if પથ == 'remote/libremote.a' else પ્રોજેક્ટ_રૂટ / 'build' / પથ for પથ in લાઇબ્રેરી] + ['--end-group'], લૉગ_પંક્તિ)
                    અમલ_કરો_આદેશ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], લૉગ_પંક્તિ)
                with (પરિમાણ / 'remote-test.log').open('wb') as લૉગ_પંક્તિ:
                    અમલ_કરો_આદેશ(['python3', પ્રોજેક્ટ_રૂટ / 'ઉપકરણો/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', સેટિંગ્સ_ફાઇલ, '--output', પરિમાણ], લૉગ_પંક્તિ)
                માન્ય_કરો = json.loads((પરિમાણ / 'report.json').read_text())
                assert માન્ય_કરો['passed']
                અહેવાલ_મૂલ્ય['checks'].append(નામ + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        અહેવાલ_મૂલ્ય['passed'] = True
    finally:
        અહેવાલ_મૂલ્ય['personal_settings_unchanged'] = વ્યક્તિગત_સેટિંગ્સ.read_bytes() == 원래설정
        if not અહેવાલ_મૂલ્ય['personal_settings_unchanged']:
            અહેવાલ_મૂલ્ય['passed'] = False
        અહેવાલ_મૂલ્ય['kernel_sha256'] = hashlib.sha256((પ્રોજેક્ટ_રૂટ / 'build/kernel8.img').read_bytes()).hexdigest()
        (આઉટપુટ / 'report.json').write_text(json.dumps(અહેવાલ_મૂલ્ય, ensure_ascii=False, indent=2) + '\n')
    assert અહેવાલ_મૂલ્ય['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(અહેવાલ_મૂલ્ય, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ચલાવો_2()
