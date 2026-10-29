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
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ


def 시험휠(ਨਾਂ, 파일들, ਕੰਮ_ਕੀਮਤ='Root-Is-Purelib: true\n', 의존성=''):
    ਸਮੱਗਰੀ = io.BytesIO()
    with zipfile.ZipFile(ਸਮੱਗਰੀ, 'w', zipfile.ZIP_DEFLATED) as ਬੰਡਲ:
        ਬੰਡਲ.writestr(ਨਾਂ + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ਕੰਮ_ਕੀਮਤ)
        ਬੰਡਲ.writestr(ਨਾਂ + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ਨਾਂ + '\nVersion: 1.0\n' + 의존성)
        for ਮਾਰਗ, ਤਤਕਰਾ_ਕੀਮਤ in 파일들.items():
            ਬੰਡਲ.writestr(ਮਾਰਗ, ਤਤਕਰਾ_ਕੀਮਤ)
    return ਸਮੱਗਰੀ.getvalue()


def ਚੈਕ_ਕਰੋ_ਹੋਸਟ():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'ਕੀਮਤ=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'ਕੀਮਤ=42\n'.encode()}
    for ਸਮੱਗਰੀ in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ਸਮੱਗਰੀ, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ਮਾਰਗ·ਆਕਾਰ·C ਪ੍ਰਸਾਰ_ਕੀਮਤ·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ਚਲਾਓ_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    ਆਰਗੂਮੈਂਟ = 해석기.parse_args()
    ਚੈਕ_ਕਰੋ_ਹੋਸਟ()
    if ਆਰਗੂਮੈਂਟ.host_only:
        return
    ਮਾਪ_ਰਸਤਾ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/pip'
    ਮਾਪ_ਰਸਤਾ.mkdir(parents=True, exist_ok=True)
    ਸਟੋਰੇਜ_ਰਸਤਾ = ਮਾਪ_ਰਸਤਾ/'cache'
    ਸਟੋਰੇਜ_ਰਸਤਾ.mkdir(exist_ok=True)
    # ਅਸਲ_ਸਮੱਗਰੀ PyPI 배포 ਫਾਇਲ. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/pip-cache').ਤਿਆਰ_ਕਰੋ('micropython-bisect==3.3.3')
    for ਟੇਲ_ਕੀਮਤ in ('.archive', '.json'):
        shutil.copyfile(str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/pip-cache'/('micropython-bisect==3.3.3'+ਟੇਲ_ਕੀਮਤ)), str(ਸਟੋਰੇਜ_ਰਸਤਾ/('micropython-bisect==3.3.3'+ਟੇਲ_ਕੀਮਤ)))
    실물기록 = json.loads((ਸਟੋਰੇਜ_ਰਸਤਾ/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ਨਾਂ, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'ਕੀਮਤ=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ਸਮੱਗਰੀ = 시험휠(ਨਾਂ, 파일들)
        (ਸਟੋਰੇਜ_ਰਸਤਾ/(ਨਾਂ+'==1.0.archive')).write_bytes(ਸਮੱਗਰੀ)
        (ਸਟੋਰੇਜ_ਰਸਤਾ/(ਨਾਂ+'==1.0.json')).write_text(json.dumps({'name': ਨਾਂ, 'version': '1.0',
            'filename': ਨਾਂ.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ਸਮੱਗਰੀ).hexdigest()}))
    ਪ੍ਰਮਾਣਿਤ = {'passed': False, 'kernel_sha256': hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    ਪਰੋਸੈੱਸ = subprocess.Popen(['python3', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(ਸਟੋਰੇਜ_ਰਸਤਾ), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ਚੋਣਕਰਤਾ_a916db4e = selectors.DefaultSelector()
    ਚੋਣਕਰਤਾ_a916db4e.register(ਪਰੋਸੈੱਸ.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(ਸ਼ੋਅ_ਕੀਮਤ=b'jkoros-native> '):
        ਤਤਕਰਾ_ਕੀਮਤ = bytearray()
        끝 = time.monotonic()+120
        while ਸ਼ੋਅ_ਕੀਮਤ not in ਤਤਕਰਾ_ਕੀਮਤ:
            if time.monotonic() > 끝 or ਪਰੋਸੈੱਸ.poll() is not None:
                raise AssertionError('게스트 ਜਵਾਬ_ਦਿਓ 없음: '+ਤਤਕਰਾ_ਕੀਮਤ.decode('utf-8','replace'))
            for ਦਾਖਲਾ_ਕੀਮਤ, _ in ਚੋਣਕਰਤਾ_a916db4e.select(.1):
                조각 = ਦਾਖਲਾ_ਕੀਮਤ.fileobj.read(4096)
                ਤਤਕਰਾ_ਕੀਮਤ.extend(조각)
                대화기록.extend(조각)
        return ਤਤਕਰਾ_ਕੀਮਤ.decode('utf-8', 'replace').replace('\r\n','\n')
    def ਸ਼ੈਲ(ਕਮਾਂਡ, ਸ਼ੋਅ_ਕੀਮਤ=b'jkoros-native> '):
        ਪਰੋਸੈੱਸ.stdin.write(ਕਮਾਂਡ.encode()+b'\n')
        ਪਰੋਸੈੱਸ.stdin.flush()
        return 기다리기(ਸ਼ੋਅ_ਕੀਮਤ)
    def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਕਮਾਂਡ, 예상, ਸਥਿਤੀ_ਕੀਮਤ=0):
        ਤਤਕਰਾ_ਕੀਮਤ = ਸ਼ੈਲ(ਕਮਾਂਡ)
        assert 예상 in ਤਤਕਰਾ_ਕੀਮਤ and '\nexit '+str(ਸਥਿਤੀ_ਕੀਮਤ)+'\n' in ਤਤਕਰਾ_ਕੀਮਤ, ਤਤਕਰਾ_ਕੀਮਤ
        ਪ੍ਰਮਾਣਿਤ['checks'].append(ਕਮਾਂਡ)
        return ਤਤਕਰਾ_ਕੀਮਤ
    def ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ(ਨਾਂ, ਸਮੱਗਰੀ):
        ਸ਼ੈਲ('load '+ਨਾਂ, b'hex> ')
        for ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ in range(0, len(ਸਮੱਗਰੀ), 64):
            ਸ਼ੈਲ(ਸਮੱਗਰੀ[ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ:ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ+64].hex(), b'hex> ')
        assert 'LOADED' in ਸ਼ੈਲ('.')
    try:
        기다리기()
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('pip --help', 'MicroPython ਸਰੋਤ_ਟ੍ਰੀ 설치기')
        ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('오류시험.py', (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'시험/파이썬/한국어오류시험.py').read_bytes())
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('python 오류시험.py', 'ਪੰਜਾਬੀ ਫਾਇਲ 예외 ਤਸਦੀਕ')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'ਸਥਾਪਿਤ_ਕਰੋ_ਕੀਮਤ 완료: micropython-bisect 3.3.3')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('python -c \'from bisect import insort as 순서대로넣기; ਕੀਮਤ=[1,5]; 순서대로넣기(ਕੀਮਤ,3); print(ਕੀਮਤ)\'', '[1, 3, 5]')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('python -m pip list', 'micropython-bisect 3.3.3')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'ਸਥਾਪਿਤ_ਕਰੋ_ਕੀਮਤ 완료: jkoros-fixture')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'ਬੰਡਲ ਗਲਤੀ:', 1)
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ਗਲਤੀ 보존")\'', '구문 ਗਲਤੀ 보존')
        ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('공간시험.py', (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('python 공간시험.py '+str(접속번호), 'ਬੰਡਲ 공간 부족 되돌림 ਤਸਦੀਕ')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('pip uninstall jkoros-fixture', 'ਹਟਾਉਣਾ_ਦਾਖਲਾ 완료: jkoros-fixture')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('pip uninstall micropython-bisect', 'ਹਟਾਉਣਾ_ਦਾਖਲਾ 완료: micropython-bisect')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ਹਟਾਉਣਾ_ਦਾਖਲਾ ਤਸਦੀਕ")\'', 'ਹਟਾਉਣਾ_ਦਾਖਲਾ ਤਸਦੀਕ')
        ਪ੍ਰਮਾਣਿਤ['passed'] = True
        print('PASS: PyPI 실물 ਸਥਾਪਿਤ_ਕਰੋ_ਕੀਮਤ·import·ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼, ਪੰਜਾਬੀ 예외, 패키지 ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ, ਅਸਫਲ_ਕੀਮਤ 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            ਪਰੋਸੈੱਸ.stdin.write(b'\x01x')
            ਪਰੋਸੈੱਸ.stdin.flush()
            ਪਰੋਸੈੱਸ.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            ਪਰੋਸੈੱਸ.terminate()
            try:
                ਪਰੋਸੈੱਸ.wait(timeout=8)
            except subprocess.TimeoutExpired:
                ਪਰੋਸੈੱਸ.kill()
                ਪਰੋਸੈੱਸ.wait()
        if ਪਰੋਸੈੱਸ.poll() is None:
            ਪਰੋਸੈੱਸ.kill()
            ਪਰੋਸੈੱਸ.wait()
        ਚੋਣਕਰਤਾ_a916db4e.close()
        ਪਰੋਸੈੱਸ.stdin.close()
        ਪਰੋਸੈੱਸ.stdout.close()
        (ਮਾਪ_ਰਸਤਾ/'serial.log').write_bytes(대화기록)
        (ਮਾਪ_ਰਸਤਾ/'report.json').write_text(json.dumps(ਪ੍ਰਮਾਣਿਤ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ਚਲਾਓ_2()
