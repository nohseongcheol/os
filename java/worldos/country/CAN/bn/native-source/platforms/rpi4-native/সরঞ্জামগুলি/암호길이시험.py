#!/usr/bin/env python3
"""개인 সংযোগ_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from দূরবর্তী_সেটিংস import প্রস্তুত_করুন
from COSL배포 import গন্তব্য_নাম, লাইব্রেরি

প্রকল্প_মূল = Path(__file__).resolve().parents[1]


def চালনা():
    নির্গম = প্রকল্প_মূল / 'build/verification/password-length'
    নির্গম.mkdir(parents=True, exist_ok=True)
    ব্যক্তিগত_সেটিংস = প্রকল্প_মূল / 'build/remote/access.json'
    원래설정 = ব্যক্তিগত_সেটিংস.read_bytes()
    রিপোর্ট_মান = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            সেটিংস_পথ = 시험터 / 'build/remote'
            সেটিংস_পথ.mkdir(parents=True)
            সেটিংস_ফাইল = সেটিংস_পথ / 'access.json'
            def লেখা_সেটিংস(ডাটা):
                সেটিংস_ফাইল.write_text(json.dumps(ডাটা, ensure_ascii=False) + '\n')
                সেটিংস_ফাইল.chmod(0o600)
            def যাচাই_করা_সেটিংস(শেল, 화면):
                লেখা_সেটিংস({'user': 'user', 'ssh_password': শেল, 'vnc_password': 화면})
                원본 = সেটিংস_ফাইল.read_bytes()
                প্রস্তুত_করুন(시험터)
                assert সেটিংস_ফাইল.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (সেটিংস_পথ / 'বিবরণী.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (সেটিংস_পথ / 'বিবরণী.h').stat().st_mode & 0o777 == 0o600
            for শেল, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                যাচাই_করা_সেটিংস(শেল, 화면)
            রিপোর্ট_মান['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for পরিবর্তন_করা_মান, ভুক্তি_মান in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ডাটা = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ডাটা.update(পরিবর্তন_করা_মান)
                লেখা_সেটিংস(ডাটা)
                try:
                    প্রস্তুত_করুন(시험터)
                except SystemExit as ত্রুটি:
                    assert ভুক্তি_মান in str(ত্রুটি), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ভুক্তি_মান)
            রিপোর্ট_মান['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            সেটিংস = json.loads((প্রকল্প_মূল / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            সংযোজক = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            সংগ্রহ_করা_টুল = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def কার্যকর_করুন_আদেশ(আর্গুমেন্ট_তালিকা, লগ_সারি):
                subprocess.run(list(map(str, আর্গুমেন্ট_তালিকা)), cwd=str(প্রকল্প_মূল), stdout=লগ_সারি,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for নাম, শেল, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + নাম, flush=True)
                যাচাই_করা_সেটিংস(শেল, 화면)
                পরিমাপ = নির্গম / নাম
                পরিমাপ.mkdir(exist_ok=True)
                with (পরিমাপ / 'build.log').open('wb') as লগ_সারি:
                    목적들 = []
                    for 원본 in sorted((প্রকল্প_মূল / 'দূরবর্তী_মান').glob('*.c')):
                        গন্তব্য_মান = 시험터 / (원본.stem + '.o')
                        কার্যকর_করুন_আদেশ([번역기] + সেটিংস + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', সেটিংস_পথ, '-I', প্রকল্প_মূল / 'দূরবর্তী_মান', '-I', প্রকল্প_মূল / 'vendor/libassh/src',
                             '-I', প্রকল্প_মূল / 'vendor/bearssl/inc', '-I', প্রকল্প_মূল / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', গন্তব্য_মান], লগ_সারি)
                        목적들.append(গন্তব্য_মান)
                    দূরবর্তী_পাঁজা = 시험터 / 'libremote.a'
                    কার্যকর_করুন_আদেশ([সংগ্রহ_করা_টুল, 'rcs', দূরবর্তী_পাঁজা] + 목적들, লগ_সারি)
                    কার্যকর_করুন_আদেশ([সংযোজক, '--gc-sections', '-T', প্রকল্প_মূল / '부팅/লিংক_লেআউট.ld', '-o', 시험터 / 'kernel.elf'] +
                         [প্রকল্প_মূল / 'build' / (নাম + '.o') for নাম in গন্তব্য_নাম] + ['--start-group'] +
                         [দূরবর্তী_পাঁজা if পথ_2 == 'remote/libremote.a' else প্রকল্প_মূল / 'build' / পথ_2 for পথ_2 in লাইব্রেরি] + ['--end-group'], লগ_সারি)
                    কার্যকর_করুন_আদেশ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], লগ_সারি)
                with (পরিমাপ / 'remote-test.log').open('wb') as লগ_সারি:
                    কার্যকর_করুন_আদেশ(['python3', প্রকল্প_মূল / 'সরঞ্জামগুলি/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', সেটিংস_ফাইল, '--output', পরিমাপ], লগ_সারি)
                বৈধ_করুন = json.loads((পরিমাপ / 'report.json').read_text())
                assert বৈধ_করুন['passed']
                রিপোর্ট_মান['checks'].append(নাম + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        রিপোর্ট_মান['passed'] = True
    finally:
        রিপোর্ট_মান['personal_settings_unchanged'] = ব্যক্তিগত_সেটিংস.read_bytes() == 원래설정
        if not রিপোর্ট_মান['personal_settings_unchanged']:
            রিপোর্ট_মান['passed'] = False
        রিপোর্ট_মান['kernel_sha256'] = hashlib.sha256((প্রকল্প_মূল / 'build/kernel8.img').read_bytes()).hexdigest()
        (নির্গম / 'report.json').write_text(json.dumps(রিপোর্ট_মান, ensure_ascii=False, indent=2) + '\n')
    assert রিপোর্ট_মান['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(রিপোর্ট_মান, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    চালনা()
