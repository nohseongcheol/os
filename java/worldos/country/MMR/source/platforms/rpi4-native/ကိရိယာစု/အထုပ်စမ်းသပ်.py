#!/usr/bin/env python3
"""PyPI ရုပ်ပိုင်းစက်ပစ္စည်း 배포와 부정 ဝင်ဒေတာ·RAM 되돌림을 ကိုယ်ပိုင် 커널에서 검사한다."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import shutil
import socket
import subprocess
import time
import zipfile
from 꾸러미중계 import 꾸러미저장소, 압축풀기
from စက်မောင်း import စီမံကိန်းအမြစ်


def 시험휠(အမည်, ဖိုင်အချက်များ, သဘောတူစည်းမျဉ်းတန်ဖိုး='Root-Is-Purelib: true\n', 의존성=''):
    ဒေတာ = io.BytesIO()
    with zipfile.ZipFile(ဒေတာ, 'w', zipfile.ZIP_DEFLATED) as အထုပ်:
        အထုပ်.writestr(အမည် + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + သဘောတူစည်းမျဉ်းတန်ဖိုး)
        အထုပ်.writestr(အမည် + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + အမည် + '\nVersion: 1.0\n' + 의존성)
        for လမ်း, အကြောင်းအရာတန်ဖိုး in ဖိုင်အချက်များ.items():
            အထုပ်.writestr(လမ်း, အကြောင်းအရာတန်ဖိုး)
    return ဒေတာ.getvalue()


def အိမ်ရှင်စစ်():
    ဖြစ်သောပုံမှန် = 시험휠('jkoros-fixture', {'mod.py': 'တန်ဖိုး=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ဖြစ်သောပုံမှန်, 'jkoros-fixture', '1.0') == {'mod.py': 'တန်ဖိုး=42\n'.encode()}
    for ဒေတာ in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ဒေတာ, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel လမ်း·အရွယ်·C တိုးချဲ့မှု·의존성 တန်ဖိုးငြင်းပယ်')


def အလွတ်ဆက်သွယ်ပေါက်ကိန်း():
    with socket.socket() as ကွန်ရက်ပေါက်တန်ဖိုး:
        ကွန်ရက်ပေါက်တန်ဖိုး.bind(('127.0.0.1', 0))
        return ကွန်ရက်ပေါက်တန်ဖိုး.getsockname()[1]


def လုပ်ဆောင်():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    အချက်များ = 해석기.parse_args()
    အိမ်ရှင်စစ်()
    if အချက်များ.host_only:
        return
    ရလဒ်လမ်းကြောင်း = စီမံကိန်းအမြစ်/'build/verification/pip'
    ရလဒ်လမ်းကြောင်း.mkdir(parents=True, exist_ok=True)
    သိုလှောင်ရာလမ်းကြောင်း = ရလဒ်လမ်းကြောင်း/'cache'
    သိုလှောင်ရာလမ်းကြောင်း.mkdir(exist_ok=True)
    # တကယ့်ဒေတာ PyPI ဖြန့်ချိမှုတန်ဖိုး ဖိုင်. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(စီမံကိန်းအမြစ်/'build/pip-cache').ပြင်ဆင်('micropython-bisect==3.3.3')
    for အမြီးတန်ဖိုး in ('.archive', '.json'):
        shutil.copyfile(str(စီမံကိန်းအမြစ်/'build/pip-cache'/('micropython-bisect==3.3.3'+အမြီးတန်ဖိုး)), str(သိုလှောင်ရာလမ်းကြောင်း/('micropython-bisect==3.3.3'+အမြီးတန်ဖိုး)))
    စက်ပစ္စည်းမှတ်တမ်း = json.loads((သိုလှောင်ရာလမ်းကြောင်း/'micropython-bisect==3.3.3.json').read_text())
    assert စက်ပစ္စည်းမှတ်တမ်း['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for အမည်, ဖိုင်အချက်များ in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .တွက်ချက်မှု import တန်ဖိုးများထည့်\n', '검증꾸러미/တွက်ချက်မှု.py': 'def တန်ဖိုးများထည့်(ပထမတွက်ချက်ခံ,ဒုတိယတွက်ချက်ခံ):\n return ပထမတွက်ချက်ခံ+ဒုတိယတွက်ချက်ခံ\n'}),
            ('jkoros-space', {'space%d.py' % ကိန်းတန်ဖိုး: 'တန်ဖိုး=1\n' for ကိန်းတန်ဖိုး in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ဒေတာ = 시험휠(အမည်, ဖိုင်အချက်များ)
        (သိုလှောင်ရာလမ်းကြောင်း/(အမည်+'==1.0.archive')).write_bytes(ဒေတာ)
        (သိုလှောင်ရာလမ်းကြောင်း/(အမည်+'==1.0.json')).write_text(json.dumps({'name': အမည်, 'version': '1.0',
            'filename': အမည်.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ဒေတာ).hexdigest()}))
    မှန်ကန်ကြောင်းစစ် = {'passed': False, 'kernel_sha256': hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': စက်ပစ္စည်းမှတ်တမ်း, 'checks': []}
    ဆက်သွယ်ပေါက်ကိန်း = အလွတ်ဆက်သွယ်ပေါက်ကိန်း()
    실행과정 = subprocess.Popen(['python3', str(စီမံကိန်းအမြစ်/'ကိရိယာစု/စက်မောင်း.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(ဆက်သွယ်ပေါက်ကိန်း), '--pip-cache', str(သိုလှောင်ရာလမ်းကြောင်း), '--ftp-port', str(အလွတ်ဆက်သွယ်ပေါက်ကိန်း())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector()
    선택기.register(실행과정.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def စောင့်(တန်ဖိုးပြသ=b'jkoros-native> '):
        အကြောင်းအရာတန်ဖိုး = bytearray()
        အဆုံး = time.monotonic()+120
        while တန်ဖိုးပြသ not in အကြောင်းအရာတန်ဖိုး:
            if time.monotonic() > အဆုံး or 실행과정.poll() is not None:
                raise AssertionError('게스트 အကြောင်းပြန်ချက် 없음: '+အကြောင်းအရာတန်ဖိုး.decode('utf-8','replace'))
            for အချက်တန်ဖိုး, _ in 선택기.select(.1):
                အစိတ်အပိုင်း = အချက်တန်ဖိုး.fileobj.read(4096)
                အကြောင်းအရာတန်ဖိုး.extend(အစိတ်အပိုင်း)
                대화기록.extend(အစိတ်အပိုင်း)
        return အကြောင်းအရာတန်ဖိုး.decode('utf-8', 'replace').replace('\r\n','\n')
    def အမိန့်ဝင်း(အမိန့်, တန်ဖိုးပြသ=b'jkoros-native> '):
        실행과정.stdin.write(အမိန့်.encode()+b'\n')
        실행과정.stdin.flush()
        return စောင့်(တန်ဖိုးပြသ)
    def စက်မောင်း(အမိန့်, မျှော်မှန်းတန်ဖိုးများ, အခြေအနေတန်ဖိုး=0):
        အကြောင်းအရာတန်ဖိုး = အမိန့်ဝင်း(အမိန့်)
        assert မျှော်မှန်းတန်ဖိုးများ in အကြောင်းအရာတန်ဖိုး and '\nexit '+str(အခြေအနေတန်ဖိုး)+'\n' in အကြောင်းအရာတန်ဖိုး, အကြောင်းအရာတန်ဖိုး
        မှန်ကန်ကြောင်းစစ်['checks'].append(အမိန့်)
        return အကြောင်းအရာတန်ဖိုး
    def ဖိုင်တင်(အမည်, ဒေတာ):
        အမိန့်ဝင်း('load '+အမည်, b'hex> ')
        for နေရာအညွှန်းကိန်း in range(0, len(ဒေတာ), 64):
            အမိန့်ဝင်း(ဒေတာ[နေရာအညွှန်းကိန်း:နေရာအညွှန်းကိန်း+64].hex(), b'hex> ')
        assert 'LOADED' in အမိန့်ဝင်း('.')
    try:
        စောင့်()
        စက်မောင်း('pip --help', 'MicroPython မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 설치기')
        ဖိုင်တင်('오류시험.py', (စီမံကိန်းအမြစ်/'စမ်းသပ်မှု/Python/한국어오류시험.py').read_bytes())
        စက်မောင်း('python 오류시험.py', 'မြန်မာ ဖိုင် ခြွင်းချက် အတည်ပြု')
        စက်မောင်း('pip install micropython-bisect==3.3.3 --port '+str(ဆက်သွယ်ပေါက်ကိန်း), 'တန်ဖိုးတပ်ဆင် ဖြစ်သောအပြည့်အစုံ: micropython-bisect 3.3.3')
        စက်မောင်း('python -c \'from bisect import insort as 순서대로넣기; တန်ဖိုး=[1,5]; 순서대로넣기(တန်ဖိုး,3); print(တန်ဖိုး)\'', '[1, 3, 5]')
        စက်မောင်း('python -m pip list', 'micropython-bisect 3.3.3')
        စက်မောင်း('pip install micropython-bisect==3.3.3 --port '+str(ဆက်သွယ်ပေါက်ကိန်း), '이미 설치됨:')
        စက်မောင်း('pip install jkoros-fixture==1.0 --port '+str(ဆက်သွယ်ပေါက်ကိန်း), 'တန်ဖိုးတပ်ဆင် ဖြစ်သောအပြည့်အစုံ: jkoros-fixture')
        စက်မောင်း('python -c \'from 검증꾸러미 import တန်ဖိုးများထည့်; print(တန်ဖိုးများထည့်(20,22))\'', '\n42\n')
        စက်မောင်း('pip install jkoros-syntax==1.0 --port '+str(ဆက်သွယ်ပေါက်ကိန်း), 'အထုပ် အမှား:', 1)
        စက်မောင်း('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 အမှား 보존")\'', '구문 အမှား 보존')
        ဖိုင်တင်('공간시험.py', (စီမံကိန်းအမြစ်/'စမ်းသပ်မှု/Python/အထုပ်အမည်နယ်ပယ်စမ်းသပ်.py').read_bytes())
        စက်မောင်း('python 공간시험.py '+str(ဆက်သွယ်ပေါက်ကိန်း), 'အထုပ် သတ်မှတ်လိပ်စာနယ် 부족 ပြန်ပေးတံတား အတည်ပြု')
        စက်မောင်း('pip uninstall jkoros-fixture', 'အချက်ဖယ်ရှား ဖြစ်သောအပြည့်အစုံ: jkoros-fixture')
        စက်မောင်း('pip uninstall micropython-bisect', 'အချက်ဖယ်ရှား ဖြစ်သောအပြည့်အစုံ: micropython-bisect')
        စက်မောင်း('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("အချက်ဖယ်ရှား အတည်ပြု")\'', 'အချက်ဖယ်ရှား အတည်ပြု')
        မှန်ကန်ကြောင်းစစ်['passed'] = True
        print('PASS: PyPI ရုပ်ပိုင်းစက်ပစ္စည်း တန်ဖိုးတပ်ဆင်·import·စက်မောင်း, မြန်မာ ခြွင်းချက်, 패키지 ဖိုင်တွဲတန်ဖိုး, မအောင်မြင်မှု ပြန်ပေးတံတား, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 ထွက်ပရိုဂရမ် 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            실행과정.stdin.write(b'\x01x')
            실행과정.stdin.flush()
            실행과정.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            실행과정.terminate()
            try:
                실행과정.wait(timeout=8)
            except subprocess.TimeoutExpired:
                실행과정.kill()
                실행과정.wait()
        if 실행과정.poll() is None:
            실행과정.kill()
            실행과정.wait()
        선택기.close()
        실행과정.stdin.close()
        실행과정.stdout.close()
        (ရလဒ်လမ်းကြောင်း/'serial.log').write_bytes(대화기록)
        (ရလဒ်လမ်းကြောင်း/'report.json').write_text(json.dumps(မှန်ကန်ကြောင်းစစ်, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    လုပ်ဆောင်()
