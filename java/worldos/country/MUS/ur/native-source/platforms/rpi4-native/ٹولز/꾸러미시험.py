#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 اپنا 커널에서 검사한다."""
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
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ


def 시험휠(نام, 파일들, جاب_قدر='Root-Is-Purelib: true\n', 의존성=''):
    کوائف = io.BytesIO()
    with zipfile.ZipFile(کوائف, 'w', zipfile.ZIP_DEFLATED) as بنڈل:
        بنڈل.writestr(نام + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + جاب_قدر)
        بنڈل.writestr(نام + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + نام + '\nVersion: 1.0\n' + 의존성)
        for راستہ_2, مشمول_قدر in 파일들.items():
            بنڈل.writestr(راستہ_2, مشمول_قدر)
    return کوائف.getvalue()


def پڑتال_کریں_میزبان():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'قدر=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'قدر=42\n'.encode()}
    for کوائف in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', کوائف, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel راستہ_2·حجم·C توسیع_قدر·의존성 رد_کریں_قدر')


def خالی_دہانہ_نمبر():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def چلائیں():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    دلائل = 해석기.parse_args()
    پڑتال_کریں_میزبان()
    if دلائل.host_only:
        return
    پیمائش_راہ = عکس_ڈالنا_روٹ/'build/verification/pip'
    پیمائش_راہ.mkdir(parents=True, exist_ok=True)
    ذخیرہ_راہ = پیمائش_راہ/'cache'
    ذخیرہ_راہ.mkdir(exist_ok=True)
    # اصل_کوائف PyPI 배포 فائل_کا_نام. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(عکس_ڈالنا_روٹ/'build/pip-cache').تیار_کریں('micropython-bisect==3.3.3')
    for دم_قدر in ('.archive', '.json'):
        shutil.copyfile(str(عکس_ڈالنا_روٹ/'build/pip-cache'/('micropython-bisect==3.3.3'+دم_قدر)), str(ذخیرہ_راہ/('micropython-bisect==3.3.3'+دم_قدر)))
    실물기록 = json.loads((ذخیرہ_راہ/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for نام, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'قدر=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        کوائف = 시험휠(نام, 파일들)
        (ذخیرہ_راہ/(نام+'==1.0.archive')).write_bytes(کوائف)
        (ذخیرہ_راہ/(نام+'==1.0.json')).write_text(json.dumps({'name': نام, 'version': '1.0',
            'filename': نام.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(کوائف).hexdigest()}))
    جواز_دہی_کریں = {'passed': False, 'kernel_sha256': hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    دہانہ_نمبر = خالی_دہانہ_نمبر()
    عمل_کاری = subprocess.Popen(['python3', str(عکس_ڈالنا_روٹ/'ٹولز/نفاذ_کریں_حکم.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(دہانہ_نمبر), '--pip-cache', str(ذخیرہ_راہ), '--ftp-port', str(خالی_دہانہ_نمبر())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    منتخب_کنندہ_a916db4e = selectors.DefaultSelector()
    منتخب_کنندہ_a916db4e.register(عمل_کاری.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(دکھانا_قدر=b'jkoros-native> '):
        مشمول_قدر = bytearray()
        끝 = time.monotonic()+120
        while دکھانا_قدر not in مشمول_قدر:
            if time.monotonic() > 끝 or عمل_کاری.poll() is not None:
                raise AssertionError('게스트 جواب_دیں 없음: '+مشمول_قدر.decode('utf-8','replace'))
            for اندراج_قدر, _ in منتخب_کنندہ_a916db4e.select(.1):
                조각 = اندراج_قدر.fileobj.read(4096)
                مشمول_قدر.extend(조각)
                대화기록.extend(조각)
        return مشمول_قدر.decode('utf-8', 'replace').replace('\r\n','\n')
    def شیل(حکم, دکھانا_قدر=b'jkoros-native> '):
        عمل_کاری.stdin.write(حکم.encode()+b'\n')
        عمل_کاری.stdin.flush()
        return 기다리기(دکھانا_قدر)
    def نفاذ_کریں_حکم(حکم, 예상, حالت_قدر=0):
        مشمول_قدر = شیل(حکم)
        assert 예상 in مشمول_قدر and '\nexit '+str(حالت_قدر)+'\n' in مشمول_قدر, مشمول_قدر
        جواز_دہی_کریں['checks'].append(حکم)
        return مشمول_قدر
    def اپ_لوڈ_کريں_فائلیں(نام, کوائف):
        شیل('load '+نام, b'hex> ')
        for پوزیشن_ٹھیک_کریں_اشاریہ in range(0, len(کوائف), 64):
            شیل(کوائف[پوزیشن_ٹھیک_کریں_اشاریہ:پوزیشن_ٹھیک_کریں_اشاریہ+64].hex(), b'hex> ')
        assert 'LOADED' in شیل('.')
    try:
        기다리기()
        نفاذ_کریں_حکم('pip --help', 'MicroPython ماخذ_شجر 설치기')
        اپ_لوڈ_کريں_فائلیں('오류시험.py', (عکس_ڈالنا_روٹ/'시험/파이썬/한국어오류시험.py').read_bytes())
        نفاذ_کریں_حکم('python 오류시험.py', 'اردو فائل_کا_نام استثنا تصدیق_کریں')
        نفاذ_کریں_حکم('pip install micropython-bisect==3.3.3 --port '+str(دہانہ_نمبر), 'نصب_کریں_قدر 완료: micropython-bisect 3.3.3')
        نفاذ_کریں_حکم('python -c \'from bisect import insort as 순서대로넣기; قدر=[1,5]; 순서대로넣기(قدر,3); print(قدر)\'', '[1, 3, 5]')
        نفاذ_کریں_حکم('python -m pip list', 'micropython-bisect 3.3.3')
        نفاذ_کریں_حکم('pip install micropython-bisect==3.3.3 --port '+str(دہانہ_نمبر), '이미 설치됨:')
        نفاذ_کریں_حکم('pip install jkoros-fixture==1.0 --port '+str(دہانہ_نمبر), 'نصب_کریں_قدر 완료: jkoros-fixture')
        نفاذ_کریں_حکم('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        نفاذ_کریں_حکم('pip install jkoros-syntax==1.0 --port '+str(دہانہ_نمبر), 'بنڈل غلطی:', 1)
        نفاذ_کریں_حکم('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 غلطی 보존")\'', '구문 غلطی 보존')
        اپ_لوڈ_کريں_فائلیں('공간시험.py', (عکس_ڈالنا_روٹ/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        نفاذ_کریں_حکم('python 공간시험.py '+str(دہانہ_نمبر), 'بنڈل 공간 부족 되돌림 تصدیق_کریں')
        نفاذ_کریں_حکم('pip uninstall jkoros-fixture', 'ہٹائیں_اندراج 완료: jkoros-fixture')
        نفاذ_کریں_حکم('pip uninstall micropython-bisect', 'ہٹائیں_اندراج 완료: micropython-bisect')
        نفاذ_کریں_حکم('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ہٹائیں_اندراج تصدیق_کریں")\'', 'ہٹائیں_اندراج تصدیق_کریں')
        جواز_دہی_کریں['passed'] = True
        print('PASS: PyPI 실물 نصب_کریں_قدر·import·نفاذ_کریں_حکم, اردو استثنا, 패키지 ڈائریکٹری_قدر, ناکامی_قدر 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 خروج_ایپ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            عمل_کاری.stdin.write(b'\x01x')
            عمل_کاری.stdin.flush()
            عمل_کاری.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            عمل_کاری.terminate()
            try:
                عمل_کاری.wait(timeout=8)
            except subprocess.TimeoutExpired:
                عمل_کاری.kill()
                عمل_کاری.wait()
        if عمل_کاری.poll() is None:
            عمل_کاری.kill()
            عمل_کاری.wait()
        منتخب_کنندہ_a916db4e.close()
        عمل_کاری.stdin.close()
        عمل_کاری.stdout.close()
        (پیمائش_راہ/'serial.log').write_bytes(대화기록)
        (پیمائش_راہ/'report.json').write_text(json.dumps(جواز_دہی_کریں, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    چلائیں()
