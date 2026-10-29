#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 निज 커널에서 검사한다."""
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
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट


def 시험휠(नाम, 파일들, केस_मान='Root-Is-Purelib: true\n', 의존성=''):
    लगत = io.BytesIO()
    with zipfile.ZipFile(लगत, 'w', zipfile.ZIP_DEFLATED) as पोको:
        पोको.writestr(नाम + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + केस_मान)
        पोको.writestr(नाम + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + नाम + '\nVersion: 1.0\n' + 의존성)
        for मार्ग, सामग्री_मान in 파일들.items():
            पोको.writestr(मार्ग, सामग्री_मान)
    return लगत.getvalue()


def चेक_होस्ट():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'मान=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'मान=42\n'.encode()}
    for लगत in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', लगत, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel मार्ग·आकार·C विस्तार_मान·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def चलाउनुहोस्():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    तर्क = 해석기.parse_args()
    चेक_होस्ट()
    if तर्क.host_only:
        return
    मापन_बाटो = परियोजना_रूट/'build/verification/pip'
    मापन_बाटो.mkdir(parents=True, exist_ok=True)
    भण्डारण_बाटो = मापन_बाटो/'cache'
    भण्डारण_बाटो.mkdir(exist_ok=True)
    # वास्तविक_लगत PyPI 배포 फाइल. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(परियोजना_रूट/'build/pip-cache').तयार_गर्नुहोस्('micropython-bisect==3.3.3')
    for पुच्छर_मान in ('.archive', '.json'):
        shutil.copyfile(str(परियोजना_रूट/'build/pip-cache'/('micropython-bisect==3.3.3'+पुच्छर_मान)), str(भण्डारण_बाटो/('micropython-bisect==3.3.3'+पुच्छर_मान)))
    हार्डवेयर_लग = json.loads((भण्डारण_बाटो/'micropython-bisect==3.3.3.json').read_text())
    assert हार्डवेयर_लग['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for नाम, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'मान=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        लगत = 시험휠(नाम, 파일들)
        (भण्डारण_बाटो/(नाम+'==1.0.archive')).write_bytes(लगत)
        (भण्डारण_बाटो/(नाम+'==1.0.json')).write_text(json.dumps({'name': नाम, 'version': '1.0',
            'filename': नाम.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(लगत).hexdigest()}))
    वैध_गर्नुहोस् = {'passed': False, 'kernel_sha256': hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': हार्डवेयर_लग, 'checks': []}
    접속번호 = 빈접속번호()
    प्रक्रिया = subprocess.Popen(['python3', str(परियोजना_रूट/'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(भण्डारण_बाटो), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    चयनकर्ता_a916db4e = selectors.DefaultSelector()
    चयनकर्ता_a916db4e.register(प्रक्रिया.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(शो_मान=b'jkoros-native> '):
        सामग्री_मान = bytearray()
        끝 = time.monotonic()+120
        while शो_मान not in सामग्री_मान:
            if time.monotonic() > 끝 or प्रक्रिया.poll() is not None:
                raise AssertionError('게스트 जवाफ_दिनुहोस् 없음: '+सामग्री_मान.decode('utf-8','replace'))
            for प्रविष्टि_मान, _ in चयनकर्ता_a916db4e.select(.1):
                조각 = प्रविष्टि_मान.fileobj.read(4096)
                सामग्री_मान.extend(조각)
                대화기록.extend(조각)
        return सामग्री_मान.decode('utf-8', 'replace').replace('\r\n','\n')
    def शेल(आदेश, शो_मान=b'jkoros-native> '):
        प्रक्रिया.stdin.write(आदेश.encode()+b'\n')
        प्रक्रिया.stdin.flush()
        return 기다리기(शो_मान)
    def कार्यान्वयन_गर्नुहोस्_आदेश(आदेश, 예상, स्थिति_मान=0):
        सामग्री_मान = शेल(आदेश)
        assert 예상 in सामग्री_मान and '\nexit '+str(स्थिति_मान)+'\n' in सामग्री_मान, सामग्री_मान
        वैध_गर्नुहोस्['checks'].append(आदेश)
        return सामग्री_मान
    def अपलोड_गर्नुहोस्_फाइलहरू(नाम, लगत):
        शेल('load '+नाम, b'hex> ')
        for राख्नुहोस्_अनुक्रमणिका in range(0, len(लगत), 64):
            शेल(लगत[राख्नुहोस्_अनुक्रमणिका:राख्नुहोस्_अनुक्रमणिका+64].hex(), b'hex> ')
        assert 'LOADED' in शेल('.')
    try:
        기다리기()
        कार्यान्वयन_गर्नुहोस्_आदेश('pip --help', 'MicroPython स्रोत_वृक्ष 설치기')
        अपलोड_गर्नुहोस्_फाइलहरू('오류시험.py', (परियोजना_रूट/'시험/파이썬/한국어오류시험.py').read_bytes())
        कार्यान्वयन_गर्नुहोस्_आदेश('python 오류시험.py', 'नेपाली फाइल 예외 रुजू_गर्नुहोस्')
        कार्यान्वयन_गर्नुहोस्_आदेश('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'स्थापना_गर्नुहोस्_मान 완료: micropython-bisect 3.3.3')
        कार्यान्वयन_गर्नुहोस्_आदेश('python -c \'from bisect import insort as 순서대로넣기; मान=[1,5]; 순서대로넣기(मान,3); print(मान)\'', '[1, 3, 5]')
        कार्यान्वयन_गर्नुहोस्_आदेश('python -m pip list', 'micropython-bisect 3.3.3')
        कार्यान्वयन_गर्नुहोस्_आदेश('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        कार्यान्वयन_गर्नुहोस्_आदेश('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'स्थापना_गर्नुहोस्_मान 완료: jkoros-fixture')
        कार्यान्वयन_गर्नुहोस्_आदेश('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        कार्यान्वयन_गर्नुहोस्_आदेश('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'पोको त्रुटि:', 1)
        कार्यान्वयन_गर्नुहोस्_आदेश('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 त्रुटि 보존")\'', '구문 त्रुटि 보존')
        अपलोड_गर्नुहोस्_फाइलहरू('공간시험.py', (परियोजना_रूट/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        कार्यान्वयन_गर्नुहोस्_आदेश('python 공간시험.py '+str(접속번호), 'पोको 공간 부족 되돌림 रुजू_गर्नुहोस्')
        कार्यान्वयन_गर्नुहोस्_आदेश('pip uninstall jkoros-fixture', 'हटाउनुहोस्_प्रविष्टि 완료: jkoros-fixture')
        कार्यान्वयन_गर्नुहोस्_आदेश('pip uninstall micropython-bisect', 'हटाउनुहोस्_प्रविष्टि 완료: micropython-bisect')
        कार्यान्वयन_गर्नुहोस्_आदेश('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("हटाउनुहोस्_प्रविष्टि रुजू_गर्नुहोस्")\'', 'हटाउनुहोस्_प्रविष्टि रुजू_गर्नुहोस्')
        वैध_गर्नुहोस्['passed'] = True
        print('PASS: PyPI 실물 स्थापना_गर्नुहोस्_मान·import·कार्यान्वयन_गर्नुहोस्_आदेश, नेपाली 예외, 패키지 डाइरेक्टरी_मान, विफल_मान 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 बाहिर_जानुहोस्_अनुप्रयोग 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            प्रक्रिया.stdin.write(b'\x01x')
            प्रक्रिया.stdin.flush()
            प्रक्रिया.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            प्रक्रिया.terminate()
            try:
                प्रक्रिया.wait(timeout=8)
            except subprocess.TimeoutExpired:
                प्रक्रिया.kill()
                प्रक्रिया.wait()
        if प्रक्रिया.poll() is None:
            प्रक्रिया.kill()
            प्रक्रिया.wait()
        चयनकर्ता_a916db4e.close()
        प्रक्रिया.stdin.close()
        प्रक्रिया.stdout.close()
        (मापन_बाटो/'serial.log').write_bytes(대화기록)
        (मापन_बाटो/'report.json').write_text(json.dumps(वैध_गर्नुहोस्, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    चलाउनुहोस्()
