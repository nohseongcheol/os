#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 자체 커널에서 검사한다."""
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
from نفاذ_کرو_حکم import 기준


def 시험휠(ناں, 파일들, حالت_قدر_102996da='Root-Is-Purelib: true\n', 의존성=''):
    کوائف = io.BytesIO()
    with zipfile.ZipFile(کوائف, 'w', zipfile.ZIP_DEFLATED) as گٹھ:
        گٹھ.writestr(ناں + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + حالت_قدر_102996da)
        گٹھ.writestr(ناں + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ناں + '\nVersion: 1.0\n' + 의존성)
        for راہ, اجزاء_قدر in 파일들.items():
            گٹھ.writestr(راہ, اجزاء_قدر)
    return کوائف.getvalue()


def پڑتال_مہمان():
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
    print('PASS: wheel راہ·سائز·C توسیع_قدر·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def چلاؤ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    پڑتال_مہمان()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    ذخیرہ_راہ = 결과경로/'cache'
    ذخیرہ_راہ.mkdir(exist_ok=True)
    # اصلی_کوائف PyPI 배포 فائل. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').تیاری_کرو('micropython-bisect==3.3.3')
    for اخیرلا_حصہ_قدر in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+اخیرلا_حصہ_قدر)), str(ذخیرہ_راہ/('micropython-bisect==3.3.3'+اخیرلا_حصہ_قدر)))
    실물기록 = json.loads((ذخیرہ_راہ/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ناں, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'قدر=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        کوائف = 시험휠(ناں, 파일들)
        (ذخیرہ_راہ/(ناں+'==1.0.archive')).write_bytes(کوائف)
        (ذخیرہ_راہ/(ناں+'==1.0.json')).write_text(json.dumps({'name': ناں, 'version': '1.0',
            'filename': ناں.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(کوائف).hexdigest()}))
    تریخ_دے_مطابق_کرو = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    عمل = subprocess.Popen(['python3', str(기준/'اوزار/نفاذ_کرو_حکم.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(ذخیرہ_راہ), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    منتخب_کرنڑ_آلا_a916db4e = selectors.DefaultSelector()
    منتخب_کرنڑ_آلا_a916db4e.register(عمل.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(نمایش_کرو_قدر=b'jkoros-native> '):
        اجزاء_قدر = bytearray()
        끝 = time.monotonic()+120
        while نمایش_کرو_قدر not in اجزاء_قدر:
            if time.monotonic() > 끝 or عمل.poll() is not None:
                raise AssertionError('게스트 جواب_دیوؤ 없음: '+اجزاء_قدر.decode('utf-8','replace'))
            for داخلہ_قدر, _ in منتخب_کرنڑ_آلا_a916db4e.select(.1):
                조각 = داخلہ_قدر.fileobj.read(4096)
                اجزاء_قدر.extend(조각)
                대화기록.extend(조각)
        return اجزاء_قدر.decode('utf-8', 'replace').replace('\r\n','\n')
    def شیل(حکم, نمایش_کرو_قدر=b'jkoros-native> '):
        عمل.stdin.write(حکم.encode()+b'\n')
        عمل.stdin.flush()
        return 기다리기(نمایش_کرو_قدر)
    def نفاذ_کرو_حکم(حکم, 예상, حالت_قدر=0):
        اجزاء_قدر = شیل(حکم)
        assert 예상 in اجزاء_قدر and '\nexit '+str(حالت_قدر)+'\n' in اجزاء_قدر, اجزاء_قدر
        تریخ_دے_مطابق_کرو['checks'].append(حکم)
        return اجزاء_قدر
    def اپ_لوڈ_کرو_فائلاں(ناں, کوائف):
        شیل('load '+ناں, b'hex> ')
        for 자리 in range(0, len(کوائف), 64):
            شیل(کوائف[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in شیل('.')
    try:
        기다리기()
        نفاذ_کرو_حکم('pip --help', 'MicroPython ماخذ_شجرہ 설치기')
        اپ_لوڈ_کرو_فائلاں('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        نفاذ_کرو_حکم('python 오류시험.py', '한국어 فائل 예외 تصدیق_کرو')
        نفاذ_کرو_حکم('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'تنصیب_کرو_قدر 완료: micropython-bisect 3.3.3')
        نفاذ_کرو_حکم('python -c \'from bisect import insort as 순서대로넣기; قدر=[1,5]; 순서대로넣기(قدر,3); print(قدر)\'', '[1, 3, 5]')
        نفاذ_کرو_حکم('python -m pip list', 'micropython-bisect 3.3.3')
        نفاذ_کرو_حکم('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        نفاذ_کرو_حکم('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'تنصیب_کرو_قدر 완료: jkoros-fixture')
        نفاذ_کرو_حکم('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        نفاذ_کرو_حکم('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'گٹھ نقص:', 1)
        نفاذ_کرو_حکم('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 نقص 보존")\'', '구문 نقص 보존')
        اپ_لوڈ_کرو_فائلاں('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        نفاذ_کرو_حکم('python 공간시험.py '+str(접속번호), 'گٹھ 공간 부족 되돌림 تصدیق_کرو')
        نفاذ_کرو_حکم('pip uninstall jkoros-fixture', 'ہٹاؤ_داخلہ 완료: jkoros-fixture')
        نفاذ_کرو_حکم('pip uninstall micropython-bisect', 'ہٹاؤ_داخلہ 완료: micropython-bisect')
        نفاذ_کرو_حکم('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ہٹاؤ_داخلہ تصدیق_کرو")\'', 'ہٹاؤ_داخلہ تصدیق_کرو')
        تریخ_دے_مطابق_کرو['passed'] = True
        print('PASS: PyPI 실물 تنصیب_کرو_قدر·import·نفاذ_کرو_حکم, 한국어 예외, 패키지 ڈائریکٹری_قدر, ناکامی_قدر 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 خارج_کرو_ایپ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            عمل.stdin.write(b'\x01x')
            عمل.stdin.flush()
            عمل.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            عمل.terminate()
            try:
                عمل.wait(timeout=8)
            except subprocess.TimeoutExpired:
                عمل.kill()
                عمل.wait()
        if عمل.poll() is None:
            عمل.kill()
            عمل.wait()
        منتخب_کرنڑ_آلا_a916db4e.close()
        عمل.stdin.close()
        عمل.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(تریخ_دے_مطابق_کرو, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    چلاؤ()
