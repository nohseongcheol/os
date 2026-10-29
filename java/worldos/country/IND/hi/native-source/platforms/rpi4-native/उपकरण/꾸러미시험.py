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
from 꾸러미중계 import बंडल_संग्रह, असंम्पिड्य
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल


def 시험휠(नाम, 파일들, मामला_मान='Root-Is-Purelib: true\n', 의존성=''):
    आँकड़े = io.BytesIO()
    with zipfile.ZipFile(आँकड़े, 'w', zipfile.ZIP_DEFLATED) as बंडल:
        बंडल.writestr(नाम + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + मामला_मान)
        बंडल.writestr(नाम + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + नाम + '\nVersion: 1.0\n' + 의존성)
        for पथ, सामग्री_मान in 파일들.items():
            बंडल.writestr(पथ, सामग्री_मान)
    return आँकड़े.getvalue()


def जाँचें_आयोजक():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'मान=42\n'})
    assert असंम्पिड्य('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'मान=42\n'.encode()}
    for आँकड़े in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            असंम्पिड्य('jkoros_fixture-1.0-py3-none-any.whl', आँकड़े, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel पथ·आकार·C एक्सटेंशन_मान·의존성 अस्वीकृत_करें_मान')


def 빈접속번호():
    with socket.socket() as सॉकेट_मान:
        सॉकेट_मान.bind(('127.0.0.1', 0))
        return सॉकेट_मान.getsockname()[1]


def चलाएँ():
    पार्सर_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    पार्सर_48ee4b1b.add_argument('--host-only', action='store_true')
    तर्क = पार्सर_48ee4b1b.parse_args()
    जाँचें_आयोजक()
    if तर्क.host_only:
        return
    परिणाम_पथ = प्रोजेक्ट_करें_मूल/'build/verification/pip'
    परिणाम_पथ.mkdir(parents=True, exist_ok=True)
    संग्रहण_पथ = परिणाम_पथ/'cache'
    संग्रहण_पथ.mkdir(exist_ok=True)
    # वास्तविक_डेटा PyPI 배포 संचिका. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    बंडल_संग्रह(प्रोजेक्ट_करें_मूल/'build/pip-cache').준비('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(प्रोजेक्ट_करें_मूल/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(संग्रहण_पथ/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((संग्रहण_पथ/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for नाम, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'मान=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        आँकड़े = 시험휠(नाम, 파일들)
        (संग्रहण_पथ/(नाम+'==1.0.archive')).write_bytes(आँकड़े)
        (संग्रहण_पथ/(नाम+'==1.0.json')).write_text(json.dumps({'name': नाम, 'version': '1.0',
            'filename': नाम.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(आँकड़े).hexdigest()}))
    मान्य_करें = {'passed': False, 'kernel_sha256': hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    पोर्ट_संख्या = 빈접속번호()
    प्रक्रिया = subprocess.Popen(['python3', str(प्रोजेक्ट_करें_मूल/'उपकरण/निष्पादित_करें_आदेश.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(पोर्ट_संख्या), '--pip-cache', str(संग्रहण_पथ), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    सिलेक्टर_a916db4e = selectors.DefaultSelector()
    सिलेक्टर_a916db4e.register(प्रक्रिया.stdout, selectors.EVENT_READ)
    बोला_गया_पाठ = bytearray()
    def 기다리기(शो_मान=b'jkoros-native> '):
        सामग्री_मान = bytearray()
        끝 = time.monotonic()+120
        while शो_मान not in सामग्री_मान:
            if time.monotonic() > 끝 or प्रक्रिया.poll() is not None:
                raise AssertionError('게스트 उत्तर 없음: '+सामग्री_मान.decode('utf-8','replace'))
            for एन्ट्री_मान, _ in सिलेक्टर_a916db4e.select(.1):
                조각 = एन्ट्री_मान.fileobj.read(4096)
                सामग्री_मान.extend(조각)
                बोला_गया_पाठ.extend(조각)
        return सामग्री_मान.decode('utf-8', 'replace').replace('\r\n','\n')
    def शेल(आदेश, शो_मान=b'jkoros-native> '):
        प्रक्रिया.stdin.write(आदेश.encode()+b'\n')
        प्रक्रिया.stdin.flush()
        return 기다리기(शो_मान)
    def निष्पादित_करें_आदेश(आदेश, 예상, अवस्था_मान=0):
        सामग्री_मान = शेल(आदेश)
        assert 예상 in सामग्री_मान and '\nexit '+str(अवस्था_मान)+'\n' in सामग्री_मान, सामग्री_मान
        मान्य_करें['checks'].append(आदेश)
        return सामग्री_मान
    def अपलोड_फ़ाइलें(नाम, आँकड़े):
        शेल('load '+नाम, b'hex> ')
        for पद_इंडेक्स in range(0, len(आँकड़े), 64):
            शेल(आँकड़े[पद_इंडेक्स:पद_इंडेक्स+64].hex(), b'hex> ')
        assert 'LOADED' in शेल('.')
    try:
        기다리기()
        निष्पादित_करें_आदेश('pip --help', 'MicroPython स्रोत_ट्री 설치기')
        अपलोड_फ़ाइलें('오류시험.py', (प्रोजेक्ट_करें_मूल/'시험/파이썬/한국어오류시험.py').read_bytes())
        निष्पादित_करें_आदेश('python 오류시험.py', 'हिंदी संचिका अपवाद सत्यापित_करें')
        निष्पादित_करें_आदेश('pip install micropython-bisect==3.3.3 --port '+str(पोर्ट_संख्या), 'इंस्टॉल_करें_मान 완료: micropython-bisect 3.3.3')
        निष्पादित_करें_आदेश('python -c \'from bisect import insort as 순서대로넣기; मान=[1,5]; 순서대로넣기(मान,3); print(मान)\'', '[1, 3, 5]')
        निष्पादित_करें_आदेश('python -m pip list', 'micropython-bisect 3.3.3')
        निष्पादित_करें_आदेश('pip install micropython-bisect==3.3.3 --port '+str(पोर्ट_संख्या), '이미 설치됨:')
        निष्पादित_करें_आदेश('pip install jkoros-fixture==1.0 --port '+str(पोर्ट_संख्या), 'इंस्टॉल_करें_मान 완료: jkoros-fixture')
        निष्पादित_करें_आदेश('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        निष्पादित_करें_आदेश('pip install jkoros-syntax==1.0 --port '+str(पोर्ट_संख्या), 'बंडल त्रुटि:', 1)
        निष्पादित_करें_आदेश('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 त्रुटि 보존")\'', '구문 त्रुटि 보존')
        अपलोड_फ़ाइलें('공간시험.py', (प्रोजेक्ट_करें_मूल/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        निष्पादित_करें_आदेश('python 공간시험.py '+str(पोर्ट_संख्या), 'बंडल पता_क्षेत्र 부족 वापस_करें_ब्रिज सत्यापित_करें')
        निष्पादित_करें_आदेश('pip uninstall jkoros-fixture', 'निकालें_एन्ट्री 완료: jkoros-fixture')
        निष्पादित_करें_आदेश('pip uninstall micropython-bisect', 'निकालें_एन्ट्री 완료: micropython-bisect')
        निष्पादित_करें_आदेश('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("निकालें_एन्ट्री सत्यापित_करें")\'', 'निकालें_एन्ट्री सत्यापित_करें')
        मान्य_करें['passed'] = True
        print('PASS: PyPI 실물 इंस्टॉल_करें_मान·import·निष्पादित_करें_आदेश, हिंदी अपवाद, 패키지 डायरेक्टरी_मान, विफलता_मान वापस_करें_ब्रिज, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 निर्गमन_ऐप 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
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
        सिलेक्टर_a916db4e.close()
        प्रक्रिया.stdin.close()
        प्रक्रिया.stdout.close()
        (परिणाम_पथ/'serial.log').write_bytes(बोला_गया_पाठ)
        (परिणाम_पथ/'report.json').write_text(json.dumps(मान्य_करें, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    चलाएँ()
