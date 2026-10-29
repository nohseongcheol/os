#!/usr/bin/env python3
"""개인 இணைப்பு_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from தொலைநிலை_அமைப்புகள் import தயார்படுத்த
from COSL배포 import இலக்கு_பெயர், நூலகம்

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]


def செயல்படுத்துக():
    வெளியீட்டு_இடம் = திட்டப்பணி_மூலம் / 'build/verification/password-length'
    வெளியீட்டு_இடம்.mkdir(parents=True, exist_ok=True)
    தனித்த_அமைப்புகள் = திட்டப்பணி_மூலம் / 'build/remote/access.json'
    원래설정 = தனித்த_அமைப்புகள்.read_bytes()
    அறிக்கை_மதிப்பு = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            அமைப்புகள்_பாதை = 시험터 / 'build/remote'
            அமைப்புகள்_பாதை.mkdir(parents=True)
            அமைப்புகள்_கோப்பு = அமைப்புகள்_பாதை / 'access.json'
            def எழுது_அமைப்புகள்(தரவு):
                அமைப்புகள்_கோப்பு.write_text(json.dumps(தரவு, ensure_ascii=False) + '\n')
                அமைப்புகள்_கோப்பு.chmod(0o600)
            def சரிபார்_அமைப்புகள்(கூடு, 화면):
                எழுது_அமைப்புகள்({'user': 'user', 'ssh_password': கூடு, 'vnc_password': 화면})
                원본 = அமைப்புகள்_கோப்பு.read_bytes()
                தயார்படுத்த(시험터)
                assert அமைப்புகள்_கோப்பு.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (அமைப்புகள்_பாதை / 'குறிப்பு.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (அமைப்புகள்_பாதை / 'குறிப்பு.h').stat().st_mode & 0o777 == 0o600
            for கூடு, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                சரிபார்_அமைப்புகள்(கூடு, 화면)
            அறிக்கை_மதிப்பு['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for மாற்று_மதிப்பு_16f64fe4, உள்ளீடு_மதிப்பு in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                தரவு = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                தரவு.update(மாற்று_மதிப்பு_16f64fe4)
                எழுது_அமைப்புகள்(தரவு)
                try:
                    தயார்படுத்த(시험터)
                except SystemExit as பிழை:
                    assert உள்ளீடு_மதிப்பு in str(பிழை), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + உள்ளீடு_மதிப்பு)
            அறிக்கை_மதிப்பு['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            அமைப்புகள் = json.loads((திட்டப்பணி_மூலம் / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            இணைப்பான் = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            காப்பகம்_கருவி = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def இயக்கு_கட்டளை(செயலுருபுகள், பதிவு_பதிவு):
                subprocess.run(list(map(str, செயலுருபுகள்)), cwd=str(திட்டப்பணி_மூலம்), stdout=பதிவு_பதிவு,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for பெயர், கூடு, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + பெயர், flush=True)
                சரிபார்_அமைப்புகள்(கூடு, 화면)
                அளவிடக்கூடியது = வெளியீட்டு_இடம் / பெயர்
                அளவிடக்கூடியது.mkdir(exist_ok=True)
                with (அளவிடக்கூடியது / 'build.log').open('wb') as பதிவு_பதிவு:
                    목적들 = []
                    for 원본 in sorted((திட்டப்பணி_மூலம் / 'தொலைநிலை_மதிப்பு').glob('*.c')):
                        இலக்கு_மதிப்பு = 시험터 / (원본.stem + '.o')
                        இயக்கு_கட்டளை([번역기] + அமைப்புகள் + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', அமைப்புகள்_பாதை, '-I', திட்டப்பணி_மூலம் / 'தொலைநிலை_மதிப்பு', '-I', திட்டப்பணி_மூலம் / 'vendor/libassh/src',
                             '-I', திட்டப்பணி_மூலம் / 'vendor/bearssl/inc', '-I', திட்டப்பணி_மூலம் / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', இலக்கு_மதிப்பு], பதிவு_பதிவு)
                        목적들.append(இலக்கு_மதிப்பு)
                    தொலைநிலை_மூட்டை = 시험터 / 'libremote.a'
                    இயக்கு_கட்டளை([காப்பகம்_கருவி, 'rcs', தொலைநிலை_மூட்டை] + 목적들, பதிவு_பதிவு)
                    இயக்கு_கட்டளை([இணைப்பான், '--gc-sections', '-T', திட்டப்பணி_மூலம் / '부팅/இணை_லேஅவுட்.ld', '-o', 시험터 / 'kernel.elf'] +
                         [திட்டப்பணி_மூலம் / 'build' / (பெயர் + '.o') for பெயர் in இலக்கு_பெயர்] + ['--start-group'] +
                         [தொலைநிலை_மூட்டை if பாதை_2 == 'remote/libremote.a' else திட்டப்பணி_மூலம் / 'build' / பாதை_2 for பாதை_2 in நூலகம்] + ['--end-group'], பதிவு_பதிவு)
                    இயக்கு_கட்டளை([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], பதிவு_பதிவு)
                with (அளவிடக்கூடியது / 'remote-test.log').open('wb') as பதிவு_பதிவு:
                    இயக்கு_கட்டளை(['python3', திட்டப்பணி_மூலம் / 'கருவிகள்/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', அமைப்புகள்_கோப்பு, '--output', அளவிடக்கூடியது], பதிவு_பதிவு)
                சரிபார்_5fb2b747 = json.loads((அளவிடக்கூடியது / 'report.json').read_text())
                assert சரிபார்_5fb2b747['passed']
                அறிக்கை_மதிப்பு['checks'].append(பெயர் + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        அறிக்கை_மதிப்பு['passed'] = True
    finally:
        அறிக்கை_மதிப்பு['personal_settings_unchanged'] = தனித்த_அமைப்புகள்.read_bytes() == 원래설정
        if not அறிக்கை_மதிப்பு['personal_settings_unchanged']:
            அறிக்கை_மதிப்பு['passed'] = False
        அறிக்கை_மதிப்பு['kernel_sha256'] = hashlib.sha256((திட்டப்பணி_மூலம் / 'build/kernel8.img').read_bytes()).hexdigest()
        (வெளியீட்டு_இடம் / 'report.json').write_text(json.dumps(அறிக்கை_மதிப்பு, ensure_ascii=False, indent=2) + '\n')
    assert அறிக்கை_மதிப்பு['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(அறிக்கை_மதிப்பு, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    செயல்படுத்துக()
