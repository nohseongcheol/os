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
from تعميل_ڪرڻ_حڪم import 기준


def 시험휠(نالو, 파일들, حالت_قدر_102996da='Root-Is-Purelib: true\n', 의존성=''):
    ڪوائف = io.BytesIO()
    with zipfile.ZipFile(ڪوائف, 'w', zipfile.ZIP_DEFLATED) as بنڊل:
        بنڊل.writestr(نالو + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + حالت_قدر_102996da)
        بنڊل.writestr(نالو + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + نالو + '\nVersion: 1.0\n' + 의존성)
        for راههه, مواد_قدر in 파일들.items():
            بنڊل.writestr(راههه, مواد_قدر)
    return ڪوائف.getvalue()


def پڙتال_ڪريو_مهمان():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'قدر=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'قدر=42\n'.encode()}
    for ڪوائف in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ڪوائف, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel راههه·سائيز·C واڌ_قدر·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def هلائڻ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    پڙتال_ڪريو_مهمان()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    ذخيرو_راههه = 결과경로/'cache'
    ذخيرو_راههه.mkdir(exist_ok=True)
    # اصلي_ڪوائف PyPI 배포 فائل. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').تياري_ڪريو('micropython-bisect==3.3.3')
    for پڇڙ_قدر in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+پڇڙ_قدر)), str(ذخيرو_راههه/('micropython-bisect==3.3.3'+پڇڙ_قدر)))
    실물기록 = json.loads((ذخيرو_راههه/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for نالو, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'قدر=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ڪوائف = 시험휠(نالو, 파일들)
        (ذخيرو_راههه/(نالو+'==1.0.archive')).write_bytes(ڪوائف)
        (ذخيرو_راههه/(نالو+'==1.0.json')).write_text(json.dumps({'name': نالو, 'version': '1.0',
            'filename': نالو.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ڪوائف).hexdigest()}))
    ڪارگر_ڪريو = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    عمل_a7054519 = subprocess.Popen(['python3', str(기준/'اوزار/تعميل_ڪرڻ_حڪم.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(ذخيرو_راههه), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    چونڊيندڙ_a916db4e = selectors.DefaultSelector()
    چونڊيندڙ_a916db4e.register(عمل_a7054519.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(نمائش_ڪريو_قدر=b'jkoros-native> '):
        مواد_قدر = bytearray()
        끝 = time.monotonic()+120
        while نمائش_ڪريو_قدر not in مواد_قدر:
            if time.monotonic() > 끝 or عمل_a7054519.poll() is not None:
                raise AssertionError('게스트 جواب_ڏيو 없음: '+مواد_قدر.decode('utf-8','replace'))
            for داخلا_قدر, _ in چونڊيندڙ_a916db4e.select(.1):
                조각 = داخلا_قدر.fileobj.read(4096)
                مواد_قدر.extend(조각)
                대화기록.extend(조각)
        return مواد_قدر.decode('utf-8', 'replace').replace('\r\n','\n')
    def شيل(حڪم, نمائش_ڪريو_قدر=b'jkoros-native> '):
        عمل_a7054519.stdin.write(حڪم.encode()+b'\n')
        عمل_a7054519.stdin.flush()
        return 기다리기(نمائش_ڪريو_قدر)
    def تعميل_ڪرڻ_حڪم(حڪم, 예상, حالت_قدر=0):
        مواد_قدر = شيل(حڪم)
        assert 예상 in مواد_قدر and '\nexit '+str(حالت_قدر)+'\n' in مواد_قدر, مواد_قدر
        ڪارگر_ڪريو['checks'].append(حڪم)
        return مواد_قدر
    def اپ_لوڊ_ڪريو_فائلون(نالو, ڪوائف):
        شيل('load '+نالو, b'hex> ')
        for 자리 in range(0, len(ڪوائف), 64):
            شيل(ڪوائف[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in شيل('.')
    try:
        기다리기()
        تعميل_ڪرڻ_حڪم('pip --help', 'MicroPython ماخذ_شجرو 설치기')
        اپ_لوڊ_ڪريو_فائلون('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        تعميل_ڪرڻ_حڪم('python 오류시험.py', '한국어 فائل 예외 تصديق_ڪريو')
        تعميل_ڪرڻ_حڪم('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'نصب_ڪريو_قدر 완료: micropython-bisect 3.3.3')
        تعميل_ڪرڻ_حڪم('python -c \'from bisect import insort as 순서대로넣기; قدر=[1,5]; 순서대로넣기(قدر,3); print(قدر)\'', '[1, 3, 5]')
        تعميل_ڪرڻ_حڪم('python -m pip list', 'micropython-bisect 3.3.3')
        تعميل_ڪرڻ_حڪم('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        تعميل_ڪرڻ_حڪم('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'نصب_ڪريو_قدر 완료: jkoros-fixture')
        تعميل_ڪرڻ_حڪم('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        تعميل_ڪرڻ_حڪم('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'بنڊل نقص:', 1)
        تعميل_ڪرڻ_حڪم('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 نقص 보존")\'', '구문 نقص 보존')
        اپ_لوڊ_ڪريو_فائلون('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        تعميل_ڪرڻ_حڪم('python 공간시험.py '+str(접속번호), 'بنڊل 공간 부족 되돌림 تصديق_ڪريو')
        تعميل_ڪرڻ_حڪم('pip uninstall jkoros-fixture', 'هٽايو_داخلا 완료: jkoros-fixture')
        تعميل_ڪرڻ_حڪم('pip uninstall micropython-bisect', 'هٽايو_داخلا 완료: micropython-bisect')
        تعميل_ڪرڻ_حڪم('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("هٽايو_داخلا تصديق_ڪريو")\'', 'هٽايو_داخلا تصديق_ڪريو')
        ڪارگر_ڪريو['passed'] = True
        print('PASS: PyPI 실물 نصب_ڪريو_قدر·import·تعميل_ڪرڻ_حڪم, 한국어 예외, 패키지 ڊائريڪٽري_قدر, ناڪامي_قدر 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 خارج_ڪريو_ائپ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            عمل_a7054519.stdin.write(b'\x01x')
            عمل_a7054519.stdin.flush()
            عمل_a7054519.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            عمل_a7054519.terminate()
            try:
                عمل_a7054519.wait(timeout=8)
            except subprocess.TimeoutExpired:
                عمل_a7054519.kill()
                عمل_a7054519.wait()
        if عمل_a7054519.poll() is None:
            عمل_a7054519.kill()
            عمل_a7054519.wait()
        چونڊيندڙ_a916db4e.close()
        عمل_a7054519.stdin.close()
        عمل_a7054519.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(ڪارگر_ڪريو, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    هلائڻ()
