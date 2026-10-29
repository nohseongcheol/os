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
from 꾸러미중계 import ಬಂಡಲ್_ಸಂಗ್ರಹಣೆ, 압축풀기
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ


def 시험휠(ಹೆಸರು, 파일들, ಕೆಲಸ_ಮೌಲ್ಯ='Root-Is-Purelib: true\n', 의존성=''):
    ಡೇಟಾ = io.BytesIO()
    with zipfile.ZipFile(ಡೇಟಾ, 'w', zipfile.ZIP_DEFLATED) as ಬಂಡಲ್:
        ಬಂಡಲ್.writestr(ಹೆಸರು + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ಕೆಲಸ_ಮೌಲ್ಯ)
        ಬಂಡಲ್.writestr(ಹೆಸರು + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ಹೆಸರು + '\nVersion: 1.0\n' + 의존성)
        for ಮಾರ್ಗ, ವಿಷಯ_ಮೌಲ್ಯ in 파일들.items():
            ಬಂಡಲ್.writestr(ಮಾರ್ಗ, ವಿಷಯ_ಮೌಲ್ಯ)
    return ಡೇಟಾ.getvalue()


def ಚೆಕ್_ಹೋಸ್ಟ್():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'ಮೌಲ್ಯ=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'ಮೌಲ್ಯ=42\n'.encode()}
    for ಡೇಟಾ in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ಡೇಟಾ, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ಮಾರ್ಗ·ಗಾತ್ರ·C ವಿಸ್ತರಣೆ_ಮೌಲ್ಯ·의존성 ನಿರಾಕರಿಸು_ಮೌಲ್ಯ')


def ಖಾಲಿ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ಚಲಾಯಿಸು_2():
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = ಪಾರ್ಸರ್_48ee4b1b.parse_args()
    ಚೆಕ್_ಹೋಸ್ಟ್()
    if 인수.host_only:
        return
    ಮಾಪನ_ಹಾದಿ = ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/pip'
    ಮಾಪನ_ಹಾದಿ.mkdir(parents=True, exist_ok=True)
    ಸಂಗ್ರಹ_ಹಾದಿ = ಮಾಪನ_ಹಾದಿ/'cache'
    ಸಂಗ್ರಹ_ಹಾದಿ.mkdir(exist_ok=True)
    # ನಿಜವಾದ_ಡೇಟಾ PyPI 배포 ಕಡತ. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    ಬಂಡಲ್_ಸಂಗ್ರಹಣೆ(ಬಿಂಬಿಸು_ಮೂಲ/'build/pip-cache').ಸಿದ್ಧಪಡಿಸು('micropython-bisect==3.3.3')
    for ಟೇಲ್_ಮೌಲ್ಯ in ('.archive', '.json'):
        shutil.copyfile(str(ಬಿಂಬಿಸು_ಮೂಲ/'build/pip-cache'/('micropython-bisect==3.3.3'+ಟೇಲ್_ಮೌಲ್ಯ)), str(ಸಂಗ್ರಹ_ಹಾದಿ/('micropython-bisect==3.3.3'+ಟೇಲ್_ಮೌಲ್ಯ)))
    실물기록 = json.loads((ಸಂಗ್ರಹ_ಹಾದಿ/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ಹೆಸರು, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'ಮೌಲ್ಯ=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ಡೇಟಾ = 시험휠(ಹೆಸರು, 파일들)
        (ಸಂಗ್ರಹ_ಹಾದಿ/(ಹೆಸರು+'==1.0.archive')).write_bytes(ಡೇಟಾ)
        (ಸಂಗ್ರಹ_ಹಾದಿ/(ಹೆಸರು+'==1.0.json')).write_text(json.dumps({'name': ಹೆಸರು, 'version': '1.0',
            'filename': ಹೆಸರು.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ಡೇಟಾ).hexdigest()}))
    ಸಕ್ರಮೀಕರಿಸು = {'passed': False, 'kernel_sha256': hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    ಪೋರ್ಟ್_ಸಂಖ್ಯೆ = ಖಾಲಿ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ()
    ಪ್ರಕ್ರಿಯೆ = subprocess.Popen(['python3', str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ), '--pip-cache', str(ಸಂಗ್ರಹ_ಹಾದಿ), '--ftp-port', str(ಖಾಲಿ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ಸೆಲೆಕ್ಟರ್_a916db4e = selectors.DefaultSelector()
    ಸೆಲೆಕ್ಟರ್_a916db4e.register(ಪ್ರಕ್ರಿಯೆ.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(ಶೋ_ಮೌಲ್ಯ=b'jkoros-native> '):
        ವಿಷಯ_ಮೌಲ್ಯ = bytearray()
        끝 = time.monotonic()+120
        while ಶೋ_ಮೌಲ್ಯ not in ವಿಷಯ_ಮೌಲ್ಯ:
            if time.monotonic() > 끝 or ಪ್ರಕ್ರಿಯೆ.poll() is not None:
                raise AssertionError('게스트 ಪ್ರತ್ಯುತ್ತರ 없음: '+ವಿಷಯ_ಮೌಲ್ಯ.decode('utf-8','replace'))
            for ನಮೂದು_ಮೌಲ್ಯ, _ in ಸೆಲೆಕ್ಟರ್_a916db4e.select(.1):
                조각 = ನಮೂದು_ಮೌಲ್ಯ.fileobj.read(4096)
                ವಿಷಯ_ಮೌಲ್ಯ.extend(조각)
                대화기록.extend(조각)
        return ವಿಷಯ_ಮೌಲ್ಯ.decode('utf-8', 'replace').replace('\r\n','\n')
    def ಶೆಲ್(ಆಜ್ಞೆ, ಶೋ_ಮೌಲ್ಯ=b'jkoros-native> '):
        ಪ್ರಕ್ರಿಯೆ.stdin.write(ಆಜ್ಞೆ.encode()+b'\n')
        ಪ್ರಕ್ರಿಯೆ.stdin.flush()
        return 기다리기(ಶೋ_ಮೌಲ್ಯ)
    def ಪೂರೈಸು_ಆದೇಶ(ಆಜ್ಞೆ, 예상, ಸ್ಥಿತಿ_ಮೌಲ್ಯ=0):
        ವಿಷಯ_ಮೌಲ್ಯ = ಶೆಲ್(ಆಜ್ಞೆ)
        assert 예상 in ವಿಷಯ_ಮೌಲ್ಯ and '\nexit '+str(ಸ್ಥಿತಿ_ಮೌಲ್ಯ)+'\n' in ವಿಷಯ_ಮೌಲ್ಯ, ವಿಷಯ_ಮೌಲ್ಯ
        ಸಕ್ರಮೀಕರಿಸು['checks'].append(ಆಜ್ಞೆ)
        return ವಿಷಯ_ಮೌಲ್ಯ
    def ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು(ಹೆಸರು, ಡೇಟಾ):
        ಶೆಲ್('load '+ಹೆಸರು, b'hex> ')
        for ಹುದ್ದೆ_ಪದಸೂಚಿ in range(0, len(ಡೇಟಾ), 64):
            ಶೆಲ್(ಡೇಟಾ[ಹುದ್ದೆ_ಪದಸೂಚಿ:ಹುದ್ದೆ_ಪದಸೂಚಿ+64].hex(), b'hex> ')
        assert 'LOADED' in ಶೆಲ್('.')
    try:
        기다리기()
        ಪೂರೈಸು_ಆದೇಶ('pip --help', 'MicroPython ಮೂಲ_ವೃಕ್ಷ 설치기')
        ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('오류시험.py', (ಬಿಂಬಿಸು_ಮೂಲ/'시험/파이썬/한국어오류시험.py').read_bytes())
        ಪೂರೈಸು_ಆದೇಶ('python 오류시험.py', 'ಕನ್ನಡ ಕಡತ ವಿನಾಯಿತಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು')
        ಪೂರೈಸು_ಆದೇಶ('pip install micropython-bisect==3.3.3 --port '+str(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ), 'ಸ್ಥಾಪಿಸು_ಮೌಲ್ಯ 완료: micropython-bisect 3.3.3')
        ಪೂರೈಸು_ಆದೇಶ('python -c \'from bisect import insort as 순서대로넣기; ಮೌಲ್ಯ=[1,5]; 순서대로넣기(ಮೌಲ್ಯ,3); print(ಮೌಲ್ಯ)\'', '[1, 3, 5]')
        ಪೂರೈಸು_ಆದೇಶ('python -m pip list', 'micropython-bisect 3.3.3')
        ಪೂರೈಸು_ಆದೇಶ('pip install micropython-bisect==3.3.3 --port '+str(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ), '이미 설치됨:')
        ಪೂರೈಸು_ಆದೇಶ('pip install jkoros-fixture==1.0 --port '+str(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ), 'ಸ್ಥಾಪಿಸು_ಮೌಲ್ಯ 완료: jkoros-fixture')
        ಪೂರೈಸು_ಆದೇಶ('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ಪೂರೈಸು_ಆದೇಶ('pip install jkoros-syntax==1.0 --port '+str(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ), 'ಬಂಡಲ್ ದೋಷ:', 1)
        ಪೂರೈಸು_ಆದೇಶ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ದೋಷ 보존")\'', '구문 ದೋಷ 보존')
        ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('공간시험.py', (ಬಿಂಬಿಸು_ಮೂಲ/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ಪೂರೈಸು_ಆದೇಶ('python 공간시험.py '+str(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ), 'ಬಂಡಲ್ 공간 부족 되돌림 ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು')
        ಪೂರೈಸು_ಆದೇಶ('pip uninstall jkoros-fixture', 'ತೆಗೆ_ನಮೂದು 완료: jkoros-fixture')
        ಪೂರೈಸು_ಆದೇಶ('pip uninstall micropython-bisect', 'ತೆಗೆ_ನಮೂದು 완료: micropython-bisect')
        ಪೂರೈಸು_ಆದೇಶ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ತೆಗೆ_ನಮೂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು")\'', 'ತೆಗೆ_ನಮೂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು')
        ಸಕ್ರಮೀಕರಿಸು['passed'] = True
        print('PASS: PyPI 실물 ಸ್ಥಾಪಿಸು_ಮೌಲ್ಯ·import·ಪೂರೈಸು_ಆದೇಶ, ಕನ್ನಡ ವಿನಾಯಿತಿ, 패키지 ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ, ವೈಫಲ್ಯ_ಮೌಲ್ಯ 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 ನಿರ್ಗಮನ_ಅಪ್ಲಿ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            ಪ್ರಕ್ರಿಯೆ.stdin.write(b'\x01x')
            ಪ್ರಕ್ರಿಯೆ.stdin.flush()
            ಪ್ರಕ್ರಿಯೆ.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            ಪ್ರಕ್ರಿಯೆ.terminate()
            try:
                ಪ್ರಕ್ರಿಯೆ.wait(timeout=8)
            except subprocess.TimeoutExpired:
                ಪ್ರಕ್ರಿಯೆ.kill()
                ಪ್ರಕ್ರಿಯೆ.wait()
        if ಪ್ರಕ್ರಿಯೆ.poll() is None:
            ಪ್ರಕ್ರಿಯೆ.kill()
            ಪ್ರಕ್ರಿಯೆ.wait()
        ಸೆಲೆಕ್ಟರ್_a916db4e.close()
        ಪ್ರಕ್ರಿಯೆ.stdin.close()
        ಪ್ರಕ್ರಿಯೆ.stdout.close()
        (ಮಾಪನ_ಹಾದಿ/'serial.log').write_bytes(대화기록)
        (ಮಾಪನ_ಹಾದಿ/'report.json').write_text(json.dumps(ಸಕ್ರಮೀಕರಿಸು, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
