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
from 실행 import 기준


def 시험휠(نوم, 파일들, کیس_ارزښت='Root-Is-Purelib: true\n', 의존성=''):
    اومتوک = io.BytesIO()
    with zipfile.ZipFile(اومتوک, 'w', zipfile.ZIP_DEFLATED) as 꾸러미:
        꾸러미.writestr(نوم + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + کیس_ارزښت)
        꾸러미.writestr(نوم + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + نوم + '\nVersion: 1.0\n' + 의존성)
        for يونلور, منځپانګه_ارزښت in 파일들.items():
            꾸러미.writestr(يونلور, منځپانګه_ارزښت)
    return اومتوک.getvalue()


def کتل_کوربه():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'ارزښت=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'ارزښت=42\n'.encode()}
    for اومتوک in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', اومتوک, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel يونلور·کچ·C شاتاړى_ارزښت·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ځغلول():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    کتل_کوربه()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    저장경로 = 결과경로/'cache'
    저장경로.mkdir(exist_ok=True)
    # 실제 PyPI 배포 دوتنه. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').준비('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(저장경로/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((저장경로/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for نوم, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'ارزښت=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        اومتوک = 시험휠(نوم, 파일들)
        (저장경로/(نوم+'==1.0.archive')).write_bytes(اومتوک)
        (저장경로/(نوم+'==1.0.json')).write_text(json.dumps({'name': نوم, 'version': '1.0',
            'filename': نوم.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(اومتوک).hexdigest()}))
    검증 = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    بهير = subprocess.Popen(['python3', str(기준/'도구/실행.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(저장경로), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector()
    선택기.register(بهير.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(표시=b'jkoros-native> '):
        منځپانګه_ارزښت = bytearray()
        끝 = time.monotonic()+120
        while 표시 not in منځپانګه_ارزښت:
            if time.monotonic() > 끝 or بهير.poll() is not None:
                raise AssertionError('게스트 응답 없음: '+منځپانګه_ارزښت.decode('utf-8','replace'))
            for ننوت_ارزښت, _ in 선택기.select(.1):
                조각 = ننوت_ارزښت.fileobj.read(4096)
                منځپانګه_ارزښت.extend(조각)
                대화기록.extend(조각)
        return منځپانګه_ارزښت.decode('utf-8', 'replace').replace('\r\n','\n')
    def سیپۍ(بولۍ, 표시=b'jkoros-native> '):
        بهير.stdin.write(بولۍ.encode()+b'\n')
        بهير.stdin.flush()
        return 기다리기(표시)
    def 실행(بولۍ, 예상, انکړ_ارزښت=0):
        منځپانګه_ارزښت = سیپۍ(بولۍ)
        assert 예상 in منځپانګه_ارزښت and '\nexit '+str(انکړ_ارزښت)+'\n' in منځپانګه_ارزښت, منځپانګه_ارزښت
        검증['checks'].append(بولۍ)
        return منځپانګه_ارزښت
    def 올리기(نوم, اومتوک):
        سیپۍ('load '+نوم, b'hex> ')
        for 자리 in range(0, len(اومتوک), 64):
            سیپۍ(اومتوک[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in سیپۍ('.')
    try:
        기다리기()
        실행('pip --help', 'MicroPython سرچینه_ونه 설치기')
        올리기('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        실행('python 오류시험.py', '한국어 دوتنه 예외 확인')
        실행('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'لګول_ارزښت 완료: micropython-bisect 3.3.3')
        실행('python -c \'from bisect import insort as 순서대로넣기; ارزښت=[1,5]; 순서대로넣기(ارزښت,3); print(ارزښت)\'', '[1, 3, 5]')
        실행('python -m pip list', 'micropython-bisect 3.3.3')
        실행('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        실행('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'لګول_ارزښت 완료: jkoros-fixture')
        실행('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        실행('pip install jkoros-syntax==1.0 --port '+str(접속번호), '꾸러미 تېروتنه:', 1)
        실행('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 تېروتنه 보존")\'', '구문 تېروتنه 보존')
        올리기('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        실행('python 공간시험.py '+str(접속번호), '꾸러미 공간 부족 되돌림 확인')
        실행('pip uninstall jkoros-fixture', '제거 완료: jkoros-fixture')
        실행('pip uninstall micropython-bisect', '제거 완료: micropython-bisect')
        실행('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("제거 확인")\'', '제거 확인')
        검증['passed'] = True
        print('PASS: PyPI 실물 لګول_ارزښت·import·실행, 한국어 예외, 패키지 نوملړ_ارزښت, پاتېينه_ارزښت 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 وتون_کاريال 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            بهير.stdin.write(b'\x01x')
            بهير.stdin.flush()
            بهير.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            بهير.terminate()
            try:
                بهير.wait(timeout=8)
            except subprocess.TimeoutExpired:
                بهير.kill()
                بهير.wait()
        if بهير.poll() is None:
            بهير.kill()
            بهير.wait()
        선택기.close()
        بهير.stdin.close()
        بهير.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(검증, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ځغلول()
