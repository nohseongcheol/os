#!/usr/bin/env python3
"""개인 সংযোগ_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from দূৰবৰ্তী_ছেটিংছ import প্ৰস্তুত_কৰক
from COSL배포 import গন্তব্য_স্থান_নাম, লাইব্ৰেৰী

기준 = Path(__file__).resolve().parents[1]


def সঞ্চালন():
    নিৰ্গম = 기준 / 'build/verification/password-length'
    নিৰ্গম.mkdir(parents=True, exist_ok=True)
    ব্যক্তিগত_ছেটিংছ = 기준 / 'build/remote/access.json'
    원래설정 = ব্যক্তিগত_ছেটিংছ.read_bytes()
    ৰিপ_ৰ্ট_মান = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            ছেটিংছ_পথ = 시험터 / 'build/remote'
            ছেটিংছ_পথ.mkdir(parents=True)
            ছেটিংছ_ফাইল = ছেটিংছ_পথ / 'access.json'
            def লিখক_ছেটিংছ(ডাটা):
                ছেটিংছ_ফাইল.write_text(json.dumps(ডাটা, ensure_ascii=False) + '\n')
                ছেটিংছ_ফাইল.chmod(0o600)
            def প্ৰমাণিত_কৰক_ছেটিংছ(শ্বেল, 화면):
                লিখক_ছেটিংছ({'user': 'user', 'ssh_password': শ্বেল, 'vnc_password': 화면})
                원본 = ছেটিংছ_ফাইল.read_bytes()
                প্ৰস্তুত_কৰক(시험터)
                assert ছেটিংছ_ফাইল.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (ছেটিংছ_পথ / 'প্ৰ_ফাইল.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (ছেটিংছ_পথ / 'প্ৰ_ফাইল.h').stat().st_mode & 0o777 == 0o600
            for শ্বেল, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                প্ৰমাণিত_কৰক_ছেটিংছ(শ্বেল, 화면)
            ৰিপ_ৰ্ট_মান['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for পৰিবৰ্তন_কৰক_মান, প্রবিষ্ট_মান in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ডাটা = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ডাটা.update(পৰিবৰ্তন_কৰক_মান)
                লিখক_ছেটিংছ(ডাটা)
                try:
                    প্ৰস্তুত_কৰক(시험터)
                except SystemExit as ত্ৰুটি:
                    assert প্রবিষ্ট_মান in str(ত্ৰুটি), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + প্রবিষ্ট_মান)
            ৰিপ_ৰ্ট_মান['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            বৈশিষ্ট্য = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            সংযোজক = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            অভিলেখাগাৰ_সঁজুলি = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def নিষ্পাদন_আদেশ(인수, লগ_শাৰী):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=লগ_শাৰী,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for নাম, শ্বেল, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + নাম, flush=True)
                প্ৰমাণিত_কৰক_ছেটিংছ(শ্বেল, 화면)
                পৰিমাপ = নিৰ্গম / নাম
                পৰিমাপ.mkdir(exist_ok=True)
                with (পৰিমাপ / 'build.log').open('wb') as লগ_শাৰী:
                    목적들 = []
                    for 원본 in sorted((기준 / 'দূৰবৰ্তী_মান').glob('*.c')):
                        গন্তব্য_স্থান_মান = 시험터 / (원본.stem + '.o')
                        নিষ্পাদন_আদেশ([번역기] + বৈশিষ্ট্য + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', ছেটিংছ_পথ, '-I', 기준 / 'দূৰবৰ্তী_মান', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', গন্তব্য_স্থান_মান], লগ_শাৰী)
                        목적들.append(গন্তব্য_স্থান_মান)
                    দূৰবৰ্তী_বাণ্ডল = 시험터 / 'libremote.a'
                    নিষ্পাদন_আদেশ([অভিলেখাগাৰ_সঁজুলি, 'rcs', দূৰবৰ্তী_বাণ্ডল] + 목적들, লগ_শাৰী)
                    নিষ্পাদন_আদেশ([সংযোজক, '--gc-sections', '-T', 기준 / '부팅/লিংক_লেআউট.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (নাম + '.o') for নাম in গন্তব্য_স্থান_নাম] + ['--start-group'] +
                         [দূৰবৰ্তী_বাণ্ডল if পথ == 'remote/libremote.a' else 기준 / 'build' / পথ for পথ in লাইব্ৰেৰী] + ['--end-group'], লগ_শাৰী)
                    নিষ্পাদন_আদেশ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], লগ_শাৰী)
                with (পৰিমাপ / 'remote-test.log').open('wb') as লগ_শাৰী:
                    নিষ্পাদন_আদেশ(['python3', 기준 / 'সঁজুলিসমূহ/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', ছেটিংছ_ফাইল, '--output', পৰিমাপ], লগ_শাৰী)
                বৈধকৰণ_কৰক = json.loads((পৰিমাপ / 'report.json').read_text())
                assert বৈধকৰণ_কৰক['passed']
                ৰিপ_ৰ্ট_মান['checks'].append(নাম + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ৰিপ_ৰ্ট_মান['passed'] = True
    finally:
        ৰিপ_ৰ্ট_মান['personal_settings_unchanged'] = ব্যক্তিগত_ছেটিংছ.read_bytes() == 원래설정
        if not ৰিপ_ৰ্ট_মান['personal_settings_unchanged']:
            ৰিপ_ৰ্ট_মান['passed'] = False
        ৰিপ_ৰ্ট_মান['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (নিৰ্গম / 'report.json').write_text(json.dumps(ৰিপ_ৰ্ট_মান, ensure_ascii=False, indent=2) + '\n')
    assert ৰিপ_ৰ্ট_মান['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ৰিপ_ৰ্ট_মান, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    সঞ্চালন()
