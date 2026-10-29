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
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट


def 시험휠(नांव, 파일들, काम_मोल='Root-Is-Purelib: true\n', 의존성=''):
    डेटा = io.BytesIO()
    with zipfile.ZipFile(डेटा, 'w', zipfile.ZIP_DEFLATED) as रास:
        रास.writestr(नांव + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + काम_मोल)
        रास.writestr(नांव + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + नांव + '\nVersion: 1.0\n' + 의존성)
        for पाथ, अनुक्रमणिका_मोल in 파일들.items():
            रास.writestr(पाथ, अनुक्रमणिका_मोल)
    return डेटा.getvalue()


def तपासचें_येजमान():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'मोल=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'मोल=42\n'.encode()}
    for डेटा in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', डेटा, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel पाथ·आवाठ·C विस्तार_मोल·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def चलोवप():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    तपासचें_येजमान()
    if 인수.host_only:
        return
    मेजप_पाथ = प्रॉजॅक्ट_रूट/'build/verification/pip'
    मेजप_पाथ.mkdir(parents=True, exist_ok=True)
    सांठवण_पाथ = मेजप_पाथ/'cache'
    सांठवण_पाथ.mkdir(exist_ok=True)
    # प्रत्यक्ष_डेटा PyPI 배포 फायल. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(प्रॉजॅक्ट_रूट/'build/pip-cache').तयार_करचें_9ce364fc('micropython-bisect==3.3.3')
    for ट्रेल_मोल in ('.archive', '.json'):
        shutil.copyfile(str(प्रॉजॅक्ट_रूट/'build/pip-cache'/('micropython-bisect==3.3.3'+ट्रेल_मोल)), str(सांठवण_पाथ/('micropython-bisect==3.3.3'+ट्रेल_मोल)))
    हार्डवॅर_LOG = json.loads((सांठवण_पाथ/'micropython-bisect==3.3.3.json').read_text())
    assert हार्डवॅर_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for नांव, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'मोल=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        डेटा = 시험휠(नांव, 파일들)
        (सांठवण_पाथ/(नांव+'==1.0.archive')).write_bytes(डेटा)
        (सांठवण_पाथ/(नांव+'==1.0.json')).write_text(json.dumps({'name': नांव, 'version': '1.0',
            'filename': नांव.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(डेटा).hexdigest()}))
    पुनर्तपासणी_करची_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': हार्डवॅर_LOG, 'checks': []}
    접속번호 = 빈접속번호()
    प्रक्रिया = subprocess.Popen(['python3', str(प्रॉजॅक्ट_रूट/'साधनां/पाळो_दिवचो_आदेश.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(सांठवण_पाथ), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    वेंचक_a916db4e = selectors.DefaultSelector()
    वेंचक_a916db4e.register(प्रक्रिया.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(शो_मोल=b'jkoros-native> '):
        अनुक्रमणिका_मोल = bytearray()
        끝 = time.monotonic()+120
        while शो_मोल not in अनुक्रमणिका_मोल:
            if time.monotonic() > 끝 or प्रक्रिया.poll() is not None:
                raise AssertionError('게스트 जाप_दिवप 없음: '+अनुक्रमणिका_मोल.decode('utf-8','replace'))
            for प्रवेश_मोल, _ in वेंचक_a916db4e.select(.1):
                조각 = प्रवेश_मोल.fileobj.read(4096)
                अनुक्रमणिका_मोल.extend(조각)
                대화기록.extend(조각)
        return अनुक्रमणिका_मोल.decode('utf-8', 'replace').replace('\r\n','\n')
    def शॅल(आदेश, शो_मोल=b'jkoros-native> '):
        प्रक्रिया.stdin.write(आदेश.encode()+b'\n')
        प्रक्रिया.stdin.flush()
        return 기다리기(शो_मोल)
    def पाळो_दिवचो_आदेश(आदेश, 예상, स्थिती_मोल_e10195a1=0):
        अनुक्रमणिका_मोल = शॅल(आदेश)
        assert 예상 in अनुक्रमणिका_मोल and '\nexit '+str(स्थिती_मोल_e10195a1)+'\n' in अनुक्रमणिका_मोल, अनुक्रमणिका_मोल
        पुनर्तपासणी_करची_5fb2b747['checks'].append(आदेश)
        return अनुक्रमणिका_मोल
    def अपलोड_करचें_फायली(नांव, डेटा):
        शॅल('load '+नांव, b'hex> ')
        for स्थिती_INDEX in range(0, len(डेटा), 64):
            शॅल(डेटा[स्थिती_INDEX:स्थिती_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in शॅल('.')
    try:
        기다리기()
        पाळो_दिवचो_आदेश('pip --help', 'MicroPython स्त्रोत_ट्री 설치기')
        अपलोड_करचें_फायली('오류시험.py', (प्रॉजॅक्ट_रूट/'시험/PYTHON/한국어오류시험.py').read_bytes())
        पाळो_दिवचो_आदेश('python 오류시험.py', '한국어 फायल 예외 पुनर्तपासणी_करची')
        पाळो_दिवचो_आदेश('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'स्थापणूक_मोल 완료: micropython-bisect 3.3.3')
        पाळो_दिवचो_आदेश('python -c \'from bisect import insort as 순서대로넣기; मोल=[1,5]; 순서대로넣기(मोल,3); print(मोल)\'', '[1, 3, 5]')
        पाळो_दिवचो_आदेश('python -m pip list', 'micropython-bisect 3.3.3')
        पाळो_दिवचो_आदेश('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        पाळो_दिवचो_आदेश('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'स्थापणूक_मोल 완료: jkoros-fixture')
        पाळो_दिवचो_आदेश('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        पाळो_दिवचो_आदेश('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'रास चूक:', 1)
        पाळो_दिवचो_आदेश('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 चूक 보존")\'', '구문 चूक 보존')
        अपलोड_करचें_फायली('공간시험.py', (प्रॉजॅक्ट_रूट/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        पाळो_दिवचो_आदेश('python 공간시험.py '+str(접속번호), 'रास 공간 부족 return_ब्रिज पुनर्तपासणी_करची')
        पाळो_दिवचो_आदेश('pip uninstall jkoros-fixture', 'काडचें_प्रवेश 완료: jkoros-fixture')
        पाळो_दिवचो_आदेश('pip uninstall micropython-bisect', 'काडचें_प्रवेश 완료: micropython-bisect')
        पाळो_दिवचो_आदेश('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("काडचें_प्रवेश पुनर्तपासणी_करची")\'', 'काडचें_प्रवेश पुनर्तपासणी_करची')
        पुनर्तपासणी_करची_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 स्थापणूक_मोल·import·पाळो_दिवचो_आदेश, 한국어 예외, 패키지 नामावळ_मोल, अपेस_मोल return_ब्रिज, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 प्रस्थान_करचें_एप्लिकेशन 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
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
        वेंचक_a916db4e.close()
        प्रक्रिया.stdin.close()
        प्रक्रिया.stdout.close()
        (मेजप_पाथ/'serial.log').write_bytes(대화기록)
        (मेजप_पाथ/'report.json').write_text(json.dumps(पुनर्तपासणी_करची_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    चलोवप()
