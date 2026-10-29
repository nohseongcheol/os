"""고정한 공식 MicroPython 소스로 ကိုယ်ပိုင် SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

ဘာသာစကားထုတ်ဝေမှုတန်ဖိုး = '1.24.1'
검증해시 = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Pythonဖန်တီး(အမြစ်လမ်းကြောင်း, Cဘာသာပြန်စက်, ချိတ်ဆက်စက်ကိရိယာတစ်ခု):
    အမည် = 'micropython-' + ဘာသာစကားထုတ်ဝေမှုတန်ဖိုး
    မော်ကွန်း = အမြစ်လမ်းကြောင်း / 'vendor' / (အမည် + '.tar.gz')
    if not မော်ကွန်း.is_file() or hashlib.sha256(မော်ကွန်း.read_bytes()).hexdigest() != 검증해시:
        raise SystemExit('MicroPython မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 없음/ဖိုင်ဟက်ရှ်တွက် 불일치: ' + str(မော်ကွန်း))
    မူရင်းဒေတာ = အမြစ်လမ်းကြောင်း / 'build' / အမည်
    if not (မူရင်းဒေတာ / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(မော်ကွန်း)) as 타르꾸러미:
            for အဖွဲ့ဝင် in 타르꾸러미.getmembers():
                လမ်း = Path(အဖွဲ့ဝင်.name)
                if လမ်း.is_absolute() or '..' in လမ်း.parts or လမ်း.parts[0] != အမည်:
                    raise SystemExit('안전하지 않은 မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ လမ်း')
                if အဖွဲ့ဝင်.isfile() or အဖွဲ့ဝင်.isdir():
                    타르꾸러미.extract(အဖွဲ့ဝင်, str(အမြစ်လမ်းကြောင်း / 'build'))
        (မူရင်းဒေတာ / '.jkoros-source-sha256').write_text(검증해시 + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + Cဘာသာပြန်စက်, 'LD=' + ချိတ်ဆက်စက်ကိရိယာတစ်ခု, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(အမြစ်လမ်းကြောင်း / 'Pythonတံတား'))
