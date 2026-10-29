#!/usr/bin/env python3
"""개인 קשר_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from מרוחק_הגדרות import להכין
from COSL배포 import יעד_שם, ספריה

לשקף_בסיס = Path(__file__).resolve().parents[1]


def הפעלה():
    פלטטקסט = לשקף_בסיס / 'build/verification/password-length'
    פלטטקסט.mkdir(parents=True, exist_ok=True)
    אישי_הגדרות = לשקף_בסיס / 'build/remote/access.json'
    원래설정 = אישי_הגדרות.read_bytes()
    דוח_ערך_ddf2aaf3 = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            נסה_סביבת_עבודה = Path(임시)
            הגדרות_נתיב = נסה_סביבת_עבודה / 'build/remote'
            הגדרות_נתיב.mkdir(parents=True)
            הגדרות_קובץ = הגדרות_נתיב / 'access.json'
            def כתיבה_הגדרות(נתונים):
                הגדרות_קובץ.write_text(json.dumps(נתונים, ensure_ascii=False) + '\n')
                הגדרות_קובץ.chmod(0o600)
            def ודא_אמת_הגדרות(מעטפת, 화면):
                כתיבה_הגדרות({'user': 'user', 'ssh_password': מעטפת, 'vnc_password': 화면})
                원본 = הגדרות_קובץ.read_bytes()
                להכין(נסה_סביבת_עבודה)
                assert הגדרות_קובץ.read_bytes() == 원본, 'Settings were rewritten'
                ראש_ערך = (הגדרות_נתיב / 'פרופיל.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', ראש_ערך)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (הגדרות_נתיב / 'פרופיל.h').stat().st_mode & 0o777 == 0o600
            for מעטפת, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ודא_אמת_הגדרות(מעטפת, 화면)
            דוח_ערך_ddf2aaf3['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for שנה_ערך, ערך_ערך in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                נתונים = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                נתונים.update(שנה_ערך)
                כתיבה_הגדרות(נתונים)
                try:
                    להכין(נסה_סביבת_עבודה)
                except SystemExit as שגיאה:
                    assert ערך_ערך in str(שגיאה), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ערך_ערך)
            דוח_ערך_ddf2aaf3['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            הגדרות = json.loads((לשקף_בסיס / 'build/remote/libassh-build.json').read_text())['flags']
            מהדר_כלי = os.environ.get('ARM64_CC', 'clang')
            מחבר = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ארכיון_כלי = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def לבצע_פקודה(ארגומנטים, לרשום_שיא):
                subprocess.run(list(map(str, ארגומנטים)), cwd=str(לשקף_בסיס), stdout=לרשום_שיא,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for שם, מעטפת, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + שם, flush=True)
                ודא_אמת_הגדרות(מעטפת, 화면)
                תוצאה = פלטטקסט / שם
                תוצאה.mkdir(exist_ok=True)
                with (תוצאה / 'build.log').open('wb') as לרשום_שיא:
                    목적들 = []
                    for 원본 in sorted((לשקף_בסיס / 'מרוחק_ערך').glob('*.c')):
                        יעד_ערך = נסה_סביבת_עבודה / (원본.stem + '.o')
                        לבצע_פקודה([מהדר_כלי] + הגדרות + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', הגדרות_נתיב, '-I', לשקף_בסיס / 'מרוחק_ערך', '-I', לשקף_בסיס / 'vendor/libassh/src',
                             '-I', לשקף_בסיס / 'vendor/bearssl/inc', '-I', לשקף_בסיס / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', יעד_ערך], לרשום_שיא)
                        목적들.append(יעד_ערך)
                    מרוחק_חבילה = נסה_סביבת_עבודה / 'libremote.a'
                    לבצע_פקודה([ארכיון_כלי, 'rcs', מרוחק_חבילה] + 목적들, לרשום_שיא)
                    לבצע_פקודה([מחבר, '--gc-sections', '-T', לשקף_בסיס / '부팅/לקשר_ניווט.ld', '-o', נסה_סביבת_עבודה / 'kernel.elf'] +
                         [לשקף_בסיס / 'build' / (שם + '.o') for שם in יעד_שם] + ['--start-group'] +
                         [מרוחק_חבילה if נתיב == 'remote/libremote.a' else לשקף_בסיס / 'build' / נתיב for נתיב in ספריה] + ['--end-group'], לרשום_שיא)
                    לבצע_פקודה([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         נסה_סביבת_עבודה / 'kernel.elf', נסה_סביבת_עבודה / 'kernel8.img'], לרשום_שיא)
                with (תוצאה / 'remote-test.log').open('wb') as לרשום_שיא:
                    לבצע_פקודה(['python3', לשקף_בסיס / 'כלים/חיבור_מרוחק_נסה.py', '--kernel', נסה_סביבת_עבודה / 'kernel8.img',
                         '--access', הגדרות_קובץ, '--output', תוצאה], לרשום_שיא)
                לאמת = json.loads((תוצאה / 'report.json').read_text())
                assert לאמת['passed']
                דוח_ערך_ddf2aaf3['checks'].append(שם + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        דוח_ערך_ddf2aaf3['passed'] = True
    finally:
        דוח_ערך_ddf2aaf3['personal_settings_unchanged'] = אישי_הגדרות.read_bytes() == 원래설정
        if not דוח_ערך_ddf2aaf3['personal_settings_unchanged']:
            דוח_ערך_ddf2aaf3['passed'] = False
        דוח_ערך_ddf2aaf3['kernel_sha256'] = hashlib.sha256((לשקף_בסיס / 'build/kernel8.img').read_bytes()).hexdigest()
        (פלטטקסט / 'report.json').write_text(json.dumps(דוח_ערך_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    assert דוח_ערך_ddf2aaf3['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(דוח_ערך_ddf2aaf3, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    הפעלה()
