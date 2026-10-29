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
from 꾸러미중계 import மூட்டை_தொகுபதிவகம், சுருக்க_நீக்கம்
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்


def 시험휠(பெயர், 파일들, வேலை_மதிப்பு_102996da='Root-Is-Purelib: true\n', 의존성=''):
    தரவு = io.BytesIO()
    with zipfile.ZipFile(தரவு, 'w', zipfile.ZIP_DEFLATED) as மூட்டை:
        மூட்டை.writestr(பெயர் + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + வேலை_மதிப்பு_102996da)
        மூட்டை.writestr(பெயர் + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + பெயர் + '\nVersion: 1.0\n' + 의존성)
        for பாதை_2, உள்ளடக்கம்_மதிப்பு in 파일들.items():
            மூட்டை.writestr(பாதை_2, உள்ளடக்கம்_மதிப்பு)
    return தரவு.getvalue()


def காசோலை_ஓம்பு():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'மதிப்பு=42\n'})
    assert சுருக்க_நீக்கம்('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'மதிப்பு=42\n'.encode()}
    for தரவு in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            சுருக்க_நீக்கம்('jkoros_fixture-1.0-py3-none-any.whl', தரவு, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel பாதை_2·அளவு·C நீட்டிப்பு_மதிப்பு·의존성 புறக்கணி_மதிப்பு')


def வெறுமை_முனைய_எண்():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def செயல்படுத்துக():
    பார்சர்_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    பார்சர்_48ee4b1b.add_argument('--host-only', action='store_true')
    செயலுருபுகள் = பார்சர்_48ee4b1b.parse_args()
    காசோலை_ஓம்பு()
    if செயலுருபுகள்.host_only:
        return
    அளவிடக்கூடியது_பாதை = திட்டப்பணி_மூலம்/'build/verification/pip'
    அளவிடக்கூடியது_பாதை.mkdir(parents=True, exist_ok=True)
    சேமிப்பகம்_பாதை = அளவிடக்கூடியது_பாதை/'cache'
    சேமிப்பகம்_பாதை.mkdir(exist_ok=True)
    # அசல்_தரவு PyPI 배포 கோப்பின்_பெயர். 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    மூட்டை_தொகுபதிவகம்(திட்டப்பணி_மூலம்/'build/pip-cache').தயார்படுத்த('micropython-bisect==3.3.3')
    for இறுதிப்பகுதி_மதிப்பு in ('.archive', '.json'):
        shutil.copyfile(str(திட்டப்பணி_மூலம்/'build/pip-cache'/('micropython-bisect==3.3.3'+இறுதிப்பகுதி_மதிப்பு)), str(சேமிப்பகம்_பாதை/('micropython-bisect==3.3.3'+இறுதிப்பகுதி_மதிப்பு)))
    실물기록 = json.loads((சேமிப்பகம்_பாதை/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for பெயர், 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'மதிப்பு=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        தரவு = 시험휠(பெயர், 파일들)
        (சேமிப்பகம்_பாதை/(பெயர்+'==1.0.archive')).write_bytes(தரவு)
        (சேமிப்பகம்_பாதை/(பெயர்+'==1.0.json')).write_text(json.dumps({'name': பெயர், 'version': '1.0',
            'filename': பெயர்.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(தரவு).hexdigest()}))
    சரிபார்_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    முனைய_எண் = வெறுமை_முனைய_எண்()
    செயல்பாடு = subprocess.Popen(['python3', str(திட்டப்பணி_மூலம்/'கருவிகள்/இயக்கு_கட்டளை.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(முனைய_எண்), '--pip-cache', str(சேமிப்பகம்_பாதை), '--ftp-port', str(வெறுமை_முனைய_எண்())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    தேர்வி_a916db4e = selectors.DefaultSelector()
    தேர்வி_a916db4e.register(செயல்பாடு.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(காட்சி_மதிப்பு_487749b8=b'jkoros-native> '):
        உள்ளடக்கம்_மதிப்பு = bytearray()
        끝 = time.monotonic()+120
        while காட்சி_மதிப்பு_487749b8 not in உள்ளடக்கம்_மதிப்பு:
            if time.monotonic() > 끝 or செயல்பாடு.poll() is not None:
                raise AssertionError('게스트 பதிலளி 없음: '+உள்ளடக்கம்_மதிப்பு.decode('utf-8','replace'))
            for உள்ளீடு_மதிப்பு, _ in தேர்வி_a916db4e.select(.1):
                조각 = உள்ளீடு_மதிப்பு.fileobj.read(4096)
                உள்ளடக்கம்_மதிப்பு.extend(조각)
                대화기록.extend(조각)
        return உள்ளடக்கம்_மதிப்பு.decode('utf-8', 'replace').replace('\r\n','\n')
    def கூடு(கட்டளை, காட்சி_மதிப்பு_487749b8=b'jkoros-native> '):
        செயல்பாடு.stdin.write(கட்டளை.encode()+b'\n')
        செயல்பாடு.stdin.flush()
        return 기다리기(காட்சி_மதிப்பு_487749b8)
    def இயக்கு_கட்டளை(கட்டளை, 예상, நிலை_மதிப்பு_e10195a1=0):
        உள்ளடக்கம்_மதிப்பு = கூடு(கட்டளை)
        assert 예상 in உள்ளடக்கம்_மதிப்பு and '\nexit '+str(நிலை_மதிப்பு_e10195a1)+'\n' in உள்ளடக்கம்_மதிப்பு, உள்ளடக்கம்_மதிப்பு
        சரிபார்_5fb2b747['checks'].append(கட்டளை)
        return உள்ளடக்கம்_மதிப்பு
    def பதிவேற்று_கோப்புகள்(பெயர், தரவு):
        கூடு('load '+பெயர், b'hex> ')
        for நிலை_அடைவு in range(0, len(தரவு), 64):
            கூடு(தரவு[நிலை_அடைவு:நிலை_அடைவு+64].hex(), b'hex> ')
        assert 'LOADED' in கூடு('.')
    try:
        기다리기()
        இயக்கு_கட்டளை('pip --help', 'MicroPython மூலம்_மரம் 설치기')
        பதிவேற்று_கோப்புகள்('오류시험.py', (திட்டப்பணி_மூலம்/'시험/파이썬/한국어오류시험.py').read_bytes())
        இயக்கு_கட்டளை('python 오류시험.py', 'தமிழ் கோப்பின்_பெயர் விதிவிலக்கு சரிபார்')
        இயக்கு_கட்டளை('pip install micropython-bisect==3.3.3 --port '+str(முனைய_எண்), 'நிறுவு_மதிப்பு 완료: micropython-bisect 3.3.3')
        இயக்கு_கட்டளை('python -c \'from bisect import insort as 순서대로넣기; மதிப்பு=[1,5]; 순서대로넣기(மதிப்பு,3); print(மதிப்பு)\'', '[1, 3, 5]')
        இயக்கு_கட்டளை('python -m pip list', 'micropython-bisect 3.3.3')
        இயக்கு_கட்டளை('pip install micropython-bisect==3.3.3 --port '+str(முனைய_எண்), '이미 설치됨:')
        இயக்கு_கட்டளை('pip install jkoros-fixture==1.0 --port '+str(முனைய_எண்), 'நிறுவு_மதிப்பு 완료: jkoros-fixture')
        இயக்கு_கட்டளை('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        இயக்கு_கட்டளை('pip install jkoros-syntax==1.0 --port '+str(முனைய_எண்), 'மூட்டை பிழை:', 1)
        இயக்கு_கட்டளை('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 பிழை 보존")\'', '구문 பிழை 보존')
        பதிவேற்று_கோப்புகள்('공간시험.py', (திட்டப்பணி_மூலம்/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        இயக்கு_கட்டளை('python 공간시험.py '+str(முனைய_எண்), 'மூட்டை 공간 부족 되돌림 சரிபார்')
        இயக்கு_கட்டளை('pip uninstall jkoros-fixture', 'அகற்று_உள்ளீடு 완료: jkoros-fixture')
        இயக்கு_கட்டளை('pip uninstall micropython-bisect', 'அகற்று_உள்ளீடு 완료: micropython-bisect')
        இயக்கு_கட்டளை('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("அகற்று_உள்ளீடு சரிபார்")\'', 'அகற்று_உள்ளீடு சரிபார்')
        சரிபார்_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 நிறுவு_மதிப்பு·import·இயக்கு_கட்டளை, தமிழ் விதிவிலக்கு, 패키지 கோப்பகம்_மதிப்பு, செயலிழப்பு_மதிப்பு 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 முடிவு_நிரல் 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            செயல்பாடு.stdin.write(b'\x01x')
            செயல்பாடு.stdin.flush()
            செயல்பாடு.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            செயல்பாடு.terminate()
            try:
                செயல்பாடு.wait(timeout=8)
            except subprocess.TimeoutExpired:
                செயல்பாடு.kill()
                செயல்பாடு.wait()
        if செயல்பாடு.poll() is None:
            செயல்பாடு.kill()
            செயல்பாடு.wait()
        தேர்வி_a916db4e.close()
        செயல்பாடு.stdin.close()
        செயல்பாடு.stdout.close()
        (அளவிடக்கூடியது_பாதை/'serial.log').write_bytes(대화기록)
        (அளவிடக்கூடியது_பாதை/'report.json').write_text(json.dumps(சரிபார்_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    செயல்படுத்துக()
