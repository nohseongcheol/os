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
from 꾸러미중계 import ബണ്ടിൽ_കലവറ, മര്_ദ്ദം_കുറയ്ക്കുക
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം


def 시험휠(പേരു്, 파일들, കേസ്_മൂല്യം='Root-Is-Purelib: true\n', 의존성=''):
    ഡാറ്റാ = io.BytesIO()
    with zipfile.ZipFile(ഡാറ്റാ, 'w', zipfile.ZIP_DEFLATED) as ബണ്ടിൽ:
        ബണ്ടിൽ.writestr(പേരു് + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + കേസ്_മൂല്യം)
        ബണ്ടിൽ.writestr(പേരു് + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + പേരു് + '\nVersion: 1.0\n' + 의존성)
        for വഴി, ഉള്ളടക്കം_മൂല്യം in 파일들.items():
            ബണ്ടിൽ.writestr(വഴി, ഉള്ളടക്കം_മൂല്യം)
    return ഡാറ്റാ.getvalue()


def ചെക്ക്_ഹോസ്റ്റ്():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'മൂല്യം=42\n'})
    assert മര്_ദ്ദം_കുറയ്ക്കുക('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'മൂല്യം=42\n'.encode()}
    for ഡാറ്റാ in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            മര്_ദ്ദം_കുറയ്ക്കുക('jkoros_fixture-1.0-py3-none-any.whl', ഡാറ്റാ, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel വഴി·വലിപ്പം·C വിപുലീകരണം_മൂല്യം·의존성 നിരസിക്കുക_മൂല്യം')


def ശൂന്യം_പോര്_ട്ട്_നമ്പര്():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def നടപ്പിലാക്കുക():
    പാഴ്_സർ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    പാഴ്_സർ_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = പാഴ്_സർ_48ee4b1b.parse_args()
    ചെക്ക്_ഹോസ്റ്റ്()
    if 인수.host_only:
        return
    അളവ്_പാത = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/pip'
    അളവ്_പാത.mkdir(parents=True, exist_ok=True)
    സംഭരണം_പാത = അളവ്_പാത/'cache'
    സംഭരണം_പാത.mkdir(exist_ok=True)
    # വാസ്തവമായ_ഡാറ്റാ PyPI 배포 ഫയല്. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    ബണ്ടിൽ_കലവറ(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/pip-cache').തയ്യാറാക്കുക('micropython-bisect==3.3.3')
    for ടെയ്_ല്_മൂല്യം in ('.archive', '.json'):
        shutil.copyfile(str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/pip-cache'/('micropython-bisect==3.3.3'+ടെയ്_ല്_മൂല്യം)), str(സംഭരണം_പാത/('micropython-bisect==3.3.3'+ടെയ്_ല്_മൂല്യം)))
    실물기록 = json.loads((സംഭരണം_പാത/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for പേരു്, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'മൂല്യം=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ഡാറ്റാ = 시험휠(പേരു്, 파일들)
        (സംഭരണം_പാത/(പേരു്+'==1.0.archive')).write_bytes(ഡാറ്റാ)
        (സംഭരണം_പാത/(പേരു്+'==1.0.json')).write_text(json.dumps({'name': പേരു്, 'version': '1.0',
            'filename': പേരു്.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ഡാറ്റാ).hexdigest()}))
    സാധൂകരിക്കുക = {'passed': False, 'kernel_sha256': hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    പോര്_ട്ട്_നമ്പര് = ശൂന്യം_പോര്_ട്ട്_നമ്പര്()
    പ്രക്രിയ = subprocess.Popen(['python3', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(പോര്_ട്ട്_നമ്പര്), '--pip-cache', str(സംഭരണം_പാത), '--ftp-port', str(ശൂന്യം_പോര്_ട്ട്_നമ്പര്())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    సెలక్టర్_a916db4e = selectors.DefaultSelector()
    సెలక్టర్_a916db4e.register(പ്രക്രിയ.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(പ്രദർശനം_മൂല്യം=b'jkoros-native> '):
        ഉള്ളടക്കം_മൂല്യം = bytearray()
        끝 = time.monotonic()+120
        while പ്രദർശനം_മൂല്യം not in ഉള്ളടക്കം_മൂല്യം:
            if time.monotonic() > 끝 or പ്രക്രിയ.poll() is not None:
                raise AssertionError('게스트 മറുപടി_നൽകുക 없음: '+ഉള്ളടക്കം_മൂല്യം.decode('utf-8','replace'))
            for എന്_ട്രി_മൂല്യം, _ in సెలక్టర్_a916db4e.select(.1):
                조각 = എന്_ട്രി_മൂല്യം.fileobj.read(4096)
                ഉള്ളടക്കം_മൂല്യം.extend(조각)
                대화기록.extend(조각)
        return ഉള്ളടക്കം_മൂല്യം.decode('utf-8', 'replace').replace('\r\n','\n')
    def ഷെല്(ആജ്ഞ, പ്രദർശനം_മൂല്യം=b'jkoros-native> '):
        പ്രക്രിയ.stdin.write(ആജ്ഞ.encode()+b'\n')
        പ്രക്രിയ.stdin.flush()
        return 기다리기(പ്രദർശനം_മൂല്യം)
    def നടപ്പാക്കുക_കമാന്_ഡ്(ആജ്ഞ, 예상, അവസ്ഥ_മൂല്യം=0):
        ഉള്ളടക്കം_മൂല്യം = ഷെല്(ആജ്ഞ)
        assert 예상 in ഉള്ളടക്കം_മൂല്യം and '\nexit '+str(അവസ്ഥ_മൂല്യം)+'\n' in ഉള്ളടക്കം_മൂല്യം, ഉള്ളടക്കം_മൂല്യം
        സാധൂകരിക്കുക['checks'].append(ആജ്ഞ)
        return ഉള്ളടക്കം_മൂല്യം
    def അപ്_ലോഡ്_ഫയലുകൾ(പേരു്, ഡാറ്റാ):
        ഷെല്('load '+പേരു്, b'hex> ')
        for പദവി_സൂചിക in range(0, len(ഡാറ്റാ), 64):
            ഷെല്(ഡാറ്റാ[പദവി_സൂചിക:പദവി_സൂചിക+64].hex(), b'hex> ')
        assert 'LOADED' in ഷെല്('.')
    try:
        기다리기()
        നടപ്പാക്കുക_കമാന്_ഡ്('pip --help', 'MicroPython ഉറവിടം_ശാഖി 설치기')
        അപ്_ലോഡ്_ഫയലുകൾ('오류시험.py', (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'시험/파이썬/한국어오류시험.py').read_bytes())
        നടപ്പാക്കുക_കമാന്_ഡ്('python 오류시험.py', '한국어 ഫയല് ഒഴിവാക്കൽ പരിശോധിക്കുക')
        നടപ്പാക്കുക_കമാന്_ഡ്('pip install micropython-bisect==3.3.3 --port '+str(പോര്_ട്ട്_നമ്പര്), 'ഇന്_സ്റ്റാള്_ചെയ്യുക_മൂല്യം 완료: micropython-bisect 3.3.3')
        നടപ്പാക്കുക_കമാന്_ഡ്('python -c \'from bisect import insort as 순서대로넣기; മൂല്യം=[1,5]; 순서대로넣기(മൂല്യം,3); print(മൂല്യം)\'', '[1, 3, 5]')
        നടപ്പാക്കുക_കമാന്_ഡ്('python -m pip list', 'micropython-bisect 3.3.3')
        നടപ്പാക്കുക_കമാന്_ഡ്('pip install micropython-bisect==3.3.3 --port '+str(പോര്_ട്ട്_നമ്പര്), '이미 설치됨:')
        നടപ്പാക്കുക_കമാന്_ഡ്('pip install jkoros-fixture==1.0 --port '+str(പോര്_ട്ട്_നമ്പര്), 'ഇന്_സ്റ്റാള്_ചെയ്യുക_മൂല്യം 완료: jkoros-fixture')
        നടപ്പാക്കുക_കമാന്_ഡ്('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        നടപ്പാക്കുക_കമാന്_ഡ്('pip install jkoros-syntax==1.0 --port '+str(പോര്_ട്ട്_നമ്പര്), 'ബണ്ടിൽ പിശക്:', 1)
        നടപ്പാക്കുക_കമാന്_ഡ്('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 പിശക് 보존")\'', '구문 പിശക് 보존')
        അപ്_ലോഡ്_ഫയലുകൾ('공간시험.py', (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        നടപ്പാക്കുക_കമാന്_ഡ്('python 공간시험.py '+str(പോര്_ട്ട്_നമ്പര്), 'ബണ്ടിൽ 공간 부족 되돌림 പരിശോധിക്കുക')
        നടപ്പാക്കുക_കമാന്_ഡ്('pip uninstall jkoros-fixture', 'നീക്കംചെയ്യുക_എന്_ട്രി 완료: jkoros-fixture')
        നടപ്പാക്കുക_കമാന്_ഡ്('pip uninstall micropython-bisect', 'നീക്കംചെയ്യുക_എന്_ട്രി 완료: micropython-bisect')
        നടപ്പാക്കുക_കമാന്_ഡ്('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("നീക്കംചെയ്യുക_എന്_ട്രി പരിശോധിക്കുക")\'', 'നീക്കംചെയ്യുക_എന്_ട്രി പരിശോധിക്കുക')
        സാധൂകരിക്കുക['passed'] = True
        print('PASS: PyPI 실물 ഇന്_സ്റ്റാള്_ചെയ്യുക_മൂല്യം·import·നടപ്പാക്കുക_കമാന്_ഡ്, 한국어 ഒഴിവാക്കൽ, 패키지 ഡയറക്ടറി_മൂല്യം, പരാജയം_മൂല്യം 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 പുറത്തുകടക്കൽ_പ്രോഗ്രാം 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            പ്രക്രിയ.stdin.write(b'\x01x')
            പ്രക്രിയ.stdin.flush()
            പ്രക്രിയ.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            പ്രക്രിയ.terminate()
            try:
                പ്രക്രിയ.wait(timeout=8)
            except subprocess.TimeoutExpired:
                പ്രക്രിയ.kill()
                പ്രക്രിയ.wait()
        if പ്രക്രിയ.poll() is None:
            പ്രക്രിയ.kill()
            പ്രക്രിയ.wait()
        సెలక్టర్_a916db4e.close()
        പ്രക്രിയ.stdin.close()
        പ്രക്രിയ.stdout.close()
        (അളവ്_പാത/'serial.log').write_bytes(대화기록)
        (അളവ്_പാത/'report.json').write_text(json.dumps(സാധൂകരിക്കുക, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    നടപ്പിലാക്കുക()
