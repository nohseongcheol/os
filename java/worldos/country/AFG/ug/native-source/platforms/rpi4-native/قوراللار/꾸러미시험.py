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
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز


def 시험휠(ئاتى, 파일들, خىزمەت_قىممىتى='Root-Is-Purelib: true\n', 의존성=''):
    مەلۇمات = io.BytesIO()
    with zipfile.ZipFile(مەلۇمات, 'w', zipfile.ZIP_DEFLATED) as توپلام:
        توپلام.writestr(ئاتى + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + خىزمەت_قىممىتى)
        توپلام.writestr(ئاتى + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ئاتى + '\nVersion: 1.0\n' + 의존성)
        for يول, مەزمۇن_قىممىتى in 파일들.items():
            توپلام.writestr(يول, مەزمۇن_قىممىتى)
    return مەلۇمات.getvalue()


def تەكشۈرۈش_باقار():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'قىممىتى=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'قىممىتى=42\n'.encode()}
    for مەلۇمات in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', مەلۇمات, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel يول·چوڭلۇقى·C كېڭەيتمە_قىممىتى·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ئىجرا_قىل_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    ئۆزگەرگۈچىلەر = 해석기.parse_args()
    تەكشۈرۈش_باقار()
    if ئۆزگەرگۈچىلەر.host_only:
        return
    ئۆلچەم_يول = كۆرسىتىش_يىلتىز/'build/verification/pip'
    ئۆلچەم_يول.mkdir(parents=True, exist_ok=True)
    بوشلۇق_يول = ئۆلچەم_يول/'cache'
    بوشلۇق_يول.mkdir(exist_ok=True)
    # ھەقىقىي_مەلۇمات PyPI 배포 ھۆججەت. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(كۆرسىتىش_يىلتىز/'build/pip-cache').تەييارلىماق('micropython-bisect==3.3.3')
    for قۇيرۇق_قىممىتى in ('.archive', '.json'):
        shutil.copyfile(str(كۆرسىتىش_يىلتىز/'build/pip-cache'/('micropython-bisect==3.3.3'+قۇيرۇق_قىممىتى)), str(بوشلۇق_يول/('micropython-bisect==3.3.3'+قۇيرۇق_قىممىتى)))
    قاتتىق_دېتال_خاتىرە = json.loads((بوشلۇق_يول/'micropython-bisect==3.3.3.json').read_text())
    assert قاتتىق_دېتال_خاتىرە['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ئاتى, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'قىممىتى=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        مەلۇمات = 시험휠(ئاتى, 파일들)
        (بوشلۇق_يول/(ئاتى+'==1.0.archive')).write_bytes(مەلۇمات)
        (بوشلۇق_يول/(ئاتى+'==1.0.json')).write_text(json.dumps({'name': ئاتى, 'version': '1.0',
            'filename': ئاتى.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(مەلۇمات).hexdigest()}))
    دەلىللەش = {'passed': False, 'kernel_sha256': hashlib.sha256((كۆرسىتىش_يىلتىز/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': قاتتىق_دېتال_خاتىرە, 'checks': []}
    접속번호 = 빈접속번호()
    جەريان = subprocess.Popen(['python3', str(كۆرسىتىش_يىلتىز/'قوراللار/ئىجرا_قىلىش_بۇيرۇق.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(بوشلۇق_يول), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    تاللىغۇچ_a916db4e = selectors.DefaultSelector()
    تاللىغۇچ_a916db4e.register(جەريان.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(كۆرسەتمەك_قىممىتى=b'jkoros-native> '):
        مەزمۇن_قىممىتى = bytearray()
        끝 = time.monotonic()+120
        while كۆرسەتمەك_قىممىتى not in مەزمۇن_قىممىتى:
            if time.monotonic() > 끝 or جەريان.poll() is not None:
                raise AssertionError('게스트 جاۋابلاش 없음: '+مەزمۇن_قىممىتى.decode('utf-8','replace'))
            for كىرگۈزۈش_قىممىتى, _ in تاللىغۇچ_a916db4e.select(.1):
                조각 = كىرگۈزۈش_قىممىتى.fileobj.read(4096)
                مەزمۇن_قىممىتى.extend(조각)
                대화기록.extend(조각)
        return مەزمۇن_قىممىتى.decode('utf-8', 'replace').replace('\r\n','\n')
    def قاپ(بۇيرۇق, كۆرسەتمەك_قىممىتى=b'jkoros-native> '):
        جەريان.stdin.write(بۇيرۇق.encode()+b'\n')
        جەريان.stdin.flush()
        return 기다리기(كۆرسەتمەك_قىممىتى)
    def ئىجرا_قىلىش_بۇيرۇق(بۇيرۇق, 예상, ھالەت_قىممىتى=0):
        مەزمۇن_قىممىتى = قاپ(بۇيرۇق)
        assert 예상 in مەزمۇن_قىممىتى and '\nexit '+str(ھالەت_قىممىتى)+'\n' in مەزمۇن_قىممىتى, مەزمۇن_قىممىتى
        دەلىللەش['checks'].append(بۇيرۇق)
        return مەزمۇن_قىممىتى
    def يۈكلىمەك_ھۆججەت(ئاتى, مەلۇمات):
        قاپ('load '+ئاتى, b'hex> ')
        for ئورۇنلاشتۇرۇش_ئىندېكس in range(0, len(مەلۇمات), 64):
            قاپ(مەلۇمات[ئورۇنلاشتۇرۇش_ئىندېكس:ئورۇنلاشتۇرۇش_ئىندېكس+64].hex(), b'hex> ')
        assert 'LOADED' in قاپ('.')
    try:
        기다리기()
        ئىجرا_قىلىش_بۇيرۇق('pip --help', 'MicroPython مەنبە_دەرەخ 설치기')
        يۈكلىمەك_ھۆججەت('오류시험.py', (كۆرسىتىش_يىلتىز/'시험/파이썬/한국어오류시험.py').read_bytes())
        ئىجرا_قىلىش_بۇيرۇق('python 오류시험.py', '한국어 ھۆججەت 예외 دەلىللىمەك')
        ئىجرا_قىلىش_بۇيرۇق('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'قاچىلاش_قىممىتى 완료: micropython-bisect 3.3.3')
        ئىجرا_قىلىش_بۇيرۇق('python -c \'from bisect import insort as 순서대로넣기; قىممىتى=[1,5]; 순서대로넣기(قىممىتى,3); print(قىممىتى)\'', '[1, 3, 5]')
        ئىجرا_قىلىش_بۇيرۇق('python -m pip list', 'micropython-bisect 3.3.3')
        ئىجرا_قىلىش_بۇيرۇق('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        ئىجرا_قىلىش_بۇيرۇق('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'قاچىلاش_قىممىتى 완료: jkoros-fixture')
        ئىجرا_قىلىش_بۇيرۇق('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ئىجرا_قىلىش_بۇيرۇق('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'توپلام خاتالىق:', 1)
        ئىجرا_قىلىش_بۇيرۇق('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 خاتالىق 보존")\'', '구문 خاتالىق 보존')
        يۈكلىمەك_ھۆججەت('공간시험.py', (كۆرسىتىش_يىلتىز/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ئىجرا_قىلىش_بۇيرۇق('python 공간시험.py '+str(접속번호), 'توپلام 공간 부족 قايتۇرۇپ_بېرىش_كۆۋرۈك دەلىللىمەك')
        ئىجرا_قىلىش_بۇيرۇق('pip uninstall jkoros-fixture', 'چىقىرىۋەتمەك_كىرگۈزۈش 완료: jkoros-fixture')
        ئىجرا_قىلىش_بۇيرۇق('pip uninstall micropython-bisect', 'چىقىرىۋەتمەك_كىرگۈزۈش 완료: micropython-bisect')
        ئىجرا_قىلىش_بۇيرۇق('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("چىقىرىۋەتمەك_كىرگۈزۈش دەلىللىمەك")\'', 'چىقىرىۋەتمەك_كىرگۈزۈش دەلىللىمەك')
        دەلىللەش['passed'] = True
        print('PASS: PyPI 실물 قاچىلاش_قىممىتى·import·ئىجرا_قىلىش_بۇيرۇق, 한국어 예외, 패키지 مۇندەرىجە_قىممىتى, مەغلۇپ_بولۇش_قىممىتى قايتۇرۇپ_بېرىش_كۆۋرۈك, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 چىقىش_ئەپ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            جەريان.stdin.write(b'\x01x')
            جەريان.stdin.flush()
            جەريان.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            جەريان.terminate()
            try:
                جەريان.wait(timeout=8)
            except subprocess.TimeoutExpired:
                جەريان.kill()
                جەريان.wait()
        if جەريان.poll() is None:
            جەريان.kill()
            جەريان.wait()
        تاللىغۇچ_a916db4e.close()
        جەريان.stdin.close()
        جەريان.stdout.close()
        (ئۆلچەم_يول/'serial.log').write_bytes(대화기록)
        (ئۆلچەم_يول/'report.json').write_text(json.dumps(دەلىللەش, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ئىجرا_قىل_2()
