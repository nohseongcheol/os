#!/usr/bin/env python3
"""개인 ချိတ်ဆက်မှု 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from အဝေးသတ်မှတ်ချက် import ပြင်ဆင်
from COSL배포 import ဦးတည်ရာအမည်, စာကြည့်တိုက်

စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]


def လုပ်ဆောင်():
    အထွက် = စီမံကိန်းအမြစ် / 'build/verification/password-length'
    အထွက်.mkdir(parents=True, exist_ok=True)
    ကိုယ်ရေးသတ်မှတ်ချက် = စီမံကိန်းအမြစ် / 'build/remote/access.json'
    မူရင်းသတ်မှတ်ချက် = ကိုယ်ရေးသတ်မှတ်ချက်.read_bytes()
    အစီရင်ခံစာတန်ဖိုး = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as ယာယီတန်ဖိုး:
            အလုပ်နယ်ပယ်စမ်းသပ် = Path(ယာယီတန်ဖိုး)
            သတ်မှတ်ချက်လမ်းကြောင်း = အလုပ်နယ်ပယ်စမ်းသပ် / 'build/remote'
            သတ်မှတ်ချက်လမ်းကြောင်း.mkdir(parents=True)
            သတ်မှတ်ချက်ဖိုင် = သတ်မှတ်ချက်လမ်းကြောင်း / 'access.json'
            def သတ်မှတ်ချက်ရေး(ဒေတာ):
                သတ်မှတ်ချက်ဖိုင်.write_text(json.dumps(ဒေတာ, ensure_ascii=False) + '\n')
                သတ်မှတ်ချက်ဖိုင်.chmod(0o600)
            def သတ်မှတ်ချက်အတည်ပြု(အမိန့်ဝင်း, မျက်နှာပြင်):
                သတ်မှတ်ချက်ရေး({'user': 'user', 'ssh_password': အမိန့်ဝင်း, 'vnc_password': မျက်နှာပြင်})
                မူရင်း = သတ်မှတ်ချက်ဖိုင်.read_bytes()
                ပြင်ဆင်(အလုပ်နယ်ပယ်စမ်းသပ်)
                assert သတ်မှတ်ချက်ဖိုင်.read_bytes() == မူရင်း, 'Settings were rewritten'
                ဦးခေါင်းတန်ဖိုး = (သတ်မှတ်ချက်လမ်းကြောင်း / 'ချိတ်ဆက်ပုံစံ.h').read_text()
                ဖြစ်သောညီ = re.search(r'မျက်နှာပြင်စကားဝှက်\[\] = \{([^}]+)\}', ဦးခေါင်းတန်ဖိုး)
                assert ဖြစ်သောညီ and len(ဖြစ်သောညီ.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (သတ်မှတ်ချက်လမ်းကြောင်း / 'ချိတ်ဆက်ပုံစံ.h').stat().st_mode & 0o777 == 0o600
            for အမိန့်ဝင်း, မျက်နှာပြင် in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                သတ်မှတ်ချက်အတည်ပြု(အမိန့်ဝင်း, မျက်နှာပြင်)
            အစီရင်ခံစာတန်ဖိုး['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for တန်ဖိုးပြောင်း, အချက်တန်ဖိုး in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ဒေတာ = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ဒေတာ.update(တန်ဖိုးပြောင်း)
                သတ်မှတ်ချက်ရေး(ဒေတာ)
                try:
                    ပြင်ဆင်(အလုပ်နယ်ပယ်စမ်းသပ်)
                except SystemExit as အမှား:
                    assert အချက်တန်ဖိုး in str(အမှား), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + အချက်တန်ဖိုး)
            အစီရင်ခံစာတန်ဖိုး['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            သတ်မှတ်ချက် = json.loads((စီမံကိန်းအမြစ် / 'build/remote/libassh-build.json').read_text())['flags']
            ဘာသာပြန်စက်ကိရိယာတစ်ခု = os.environ.get('ARM64_CC', 'clang')
            연결기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            မော်ကွန်းကိရိယာတစ်ခု = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def စက်မောင်း(အချက်များ, မှတ်တမ်းမှတ်တမ်းတစ်ခု):
                subprocess.run(list(map(str, အချက်များ)), cwd=str(စီမံကိန်းအမြစ်), stdout=မှတ်တမ်းမှတ်တမ်းတစ်ခု,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for အမည်, အမိန့်ဝင်း, မျက်နှာပြင် in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + အမည်, flush=True)
                သတ်မှတ်ချက်အတည်ပြု(အမိန့်ဝင်း, မျက်နှာပြင်)
                ရလဒ် = အထွက် / အမည်
                ရလဒ်.mkdir(exist_ok=True)
                with (ရလဒ် / 'build.log').open('wb') as မှတ်တမ်းမှတ်တမ်းတစ်ခု:
                    목적들 = []
                    for မူရင်း in sorted((စီမံကိန်းအမြစ် / 'အဝေးတန်ဖိုး').glob('*.c')):
                        ဦးတည်ရာတန်ဖိုး = အလုပ်နယ်ပယ်စမ်းသပ် / (မူရင်း.stem + '.o')
                        စက်မောင်း([ဘာသာပြန်စက်ကိရိယာတစ်ခု] + သတ်မှတ်ချက် + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', သတ်မှတ်ချက်လမ်းကြောင်း, '-I', စီမံကိန်းအမြစ် / 'အဝေးတန်ဖိုး', '-I', စီမံကိန်းအမြစ် / 'vendor/libassh/src',
                             '-I', စီမံကိန်းအမြစ် / 'vendor/bearssl/inc', '-I', စီမံကိန်းအမြစ် / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', မူရင်း, '-o', ဦးတည်ရာတန်ဖိုး], မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                        목적들.append(ဦးတည်ရာတန်ဖိုး)
                    အဝေးအထုပ် = အလုပ်နယ်ပယ်စမ်းသပ် / 'libremote.a'
                    စက်မောင်း([မော်ကွန်းကိရိယာတစ်ခု, 'rcs', အဝေးအထုပ်] + 목적들, မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                    စက်မောင်း([연결기, '--gc-sections', '-T', စီမံကိန်းအမြစ် / 'စက်တင်/နေရာချထားပုံ.ld', '-o', အလုပ်နယ်ပယ်စမ်းသပ် / 'kernel.elf'] +
                         [စီမံကိန်းအမြစ် / 'build' / (အမည် + '.o') for အမည် in ဦးတည်ရာအမည်] + ['--start-group'] +
                         [အဝေးအထုပ် if လမ်း == 'remote/libremote.a' else စီမံကိန်းအမြစ် / 'build' / လမ်း for လမ်း in စာကြည့်တိုက်] + ['--end-group'], မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                    စက်မောင်း([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         အလုပ်နယ်ပယ်စမ်းသပ် / 'kernel.elf', အလုပ်နယ်ပယ်စမ်းသပ် / 'kernel8.img'], မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                with (ရလဒ် / 'remote-test.log').open('wb') as မှတ်တမ်းမှတ်တမ်းတစ်ခု:
                    စက်မောင်း(['python3', စီမံကိန်းအမြစ် / 'ကိရိယာစု/အဝေးချိတ်ဆက်မှုစမ်းသပ်.py', '--kernel', အလုပ်နယ်ပယ်စမ်းသပ် / 'kernel8.img',
                         '--access', သတ်မှတ်ချက်ဖိုင်, '--output', ရလဒ်], မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                မှန်ကန်ကြောင်းစစ် = json.loads((ရလဒ် / 'report.json').read_text())
                assert မှန်ကန်ကြောင်းစစ်['passed']
                အစီရင်ခံစာတန်ဖိုး['checks'].append(အမည် + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        အစီရင်ခံစာတန်ဖိုး['passed'] = True
    finally:
        အစီရင်ခံစာတန်ဖိုး['personal_settings_unchanged'] = ကိုယ်ရေးသတ်မှတ်ချက်.read_bytes() == မူရင်းသတ်မှတ်ချက်
        if not အစီရင်ခံစာတန်ဖိုး['personal_settings_unchanged']:
            အစီရင်ခံစာတန်ဖိုး['passed'] = False
        အစီရင်ခံစာတန်ဖိုး['kernel_sha256'] = hashlib.sha256((စီမံကိန်းအမြစ် / 'build/kernel8.img').read_bytes()).hexdigest()
        (အထွက် / 'report.json').write_text(json.dumps(အစီရင်ခံစာတန်ဖိုး, ensure_ascii=False, indent=2) + '\n')
    assert အစီရင်ခံစာတန်ဖိုး['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(အစီရင်ခံစာတန်ဖိုး, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    လုပ်ဆောင်()
