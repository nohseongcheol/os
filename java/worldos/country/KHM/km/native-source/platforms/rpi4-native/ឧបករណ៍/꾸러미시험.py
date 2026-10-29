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
from 꾸러미중계 import បាច់_ឃ្លាំង_ផ្ទុក, 압축풀기
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស


def 시험휠(ឈ្មោះ, 파일들, ករណី_តំលៃ='Root-Is-Purelib: true\n', 의존성=''):
    ទិន្នន័យ = io.BytesIO()
    with zipfile.ZipFile(ទិន្នន័យ, 'w', zipfile.ZIP_DEFLATED) as បាច់:
        បាច់.writestr(ឈ្មោះ + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ករណី_តំលៃ)
        បាច់.writestr(ឈ្មោះ + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ឈ្មោះ + '\nVersion: 1.0\n' + 의존성)
        for ផ្លូវ, មាតិកា_តំលៃ in 파일들.items():
            បាច់.writestr(ផ្លូវ, មាតិកា_តំលៃ)
    return ទិន្នន័យ.getvalue()


def ត្រួតពិនិត្យ_ហូស():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'តំលៃ=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'តំលៃ=42\n'.encode()}
    for ទិន្នន័យ in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ទិន្នន័យ, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ផ្លូវ·ដាក់ទំហំ·C ម៉ូឌុល_តំលៃ·의존성 បដិសេធ_តំលៃ')


def ទទេរ_លេខរន្ធ():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def រត់():
    មុខងារ_ញែក_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    មុខងារ_ញែក_48ee4b1b.add_argument('--host-only', action='store_true')
    អាគុយម៉ង់ = មុខងារ_ញែក_48ee4b1b.parse_args()
    ត្រួតពិនិត្យ_ហូស()
    if អាគុយម៉ង់.host_only:
        return
    ការវាស់វែង_ផ្លូវ = បញ្ចាំង_ឬស/'build/verification/pip'
    ការវាស់វែង_ផ្លូវ.mkdir(parents=True, exist_ok=True)
    ការផ្ទុក_ផ្លូវ = ការវាស់វែង_ផ្លូវ/'cache'
    ការផ្ទុក_ផ្លូវ.mkdir(exist_ok=True)
    # ដែលពិត_ទិន្នន័យ PyPI 배포 ឯកសារ. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    បាច់_ឃ្លាំង_ផ្ទុក(បញ្ចាំង_ឬស/'build/pip-cache').រៀបចំ('micropython-bisect==3.3.3')
    for កន្ទុយ_តំលៃ in ('.archive', '.json'):
        shutil.copyfile(str(បញ្ចាំង_ឬស/'build/pip-cache'/('micropython-bisect==3.3.3'+កន្ទុយ_តំលៃ)), str(ការផ្ទុក_ផ្លូវ/('micropython-bisect==3.3.3'+កន្ទុយ_តំលៃ)))
    실물기록 = json.loads((ការផ្ទុក_ផ្លូវ/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ឈ្មោះ, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'តំលៃ=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ទិន្នន័យ = 시험휠(ឈ្មោះ, 파일들)
        (ការផ្ទុក_ផ្លូវ/(ឈ្មោះ+'==1.0.archive')).write_bytes(ទិន្នន័យ)
        (ការផ្ទុក_ផ្លូវ/(ឈ្មោះ+'==1.0.json')).write_text(json.dumps({'name': ឈ្មោះ, 'version': '1.0',
            'filename': ឈ្មោះ.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ទិន្នន័យ).hexdigest()}))
    ធ្វើអោយមានសុពលភាព = {'passed': False, 'kernel_sha256': hashlib.sha256((បញ្ចាំង_ឬស/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    លេខរន្ធ = ទទេរ_លេខរន្ធ()
    ដំណើរការ = subprocess.Popen(['python3', str(បញ្ចាំង_ឬស/'ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(លេខរន្ធ), '--pip-cache', str(ការផ្ទុក_ផ្លូវ), '--ftp-port', str(ទទេរ_លេខរន្ធ())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    អ្នកជ្រើសរើស_a916db4e = selectors.DefaultSelector()
    អ្នកជ្រើសរើស_a916db4e.register(ដំណើរការ.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(បង្ហាញ_តំលៃ=b'jkoros-native> '):
        មាតិកា_តំលៃ = bytearray()
        끝 = time.monotonic()+120
        while បង្ហាញ_តំលៃ not in មាតិកា_តំលៃ:
            if time.monotonic() > 끝 or ដំណើរការ.poll() is not None:
                raise AssertionError('게스트 ឆ្លើយតប 없음: '+មាតិកា_តំលៃ.decode('utf-8','replace'))
            for ការបញ្ចូល_តំលៃ, _ in អ្នកជ្រើសរើស_a916db4e.select(.1):
                조각 = ការបញ្ចូល_តំលៃ.fileobj.read(4096)
                មាតិកា_តំលៃ.extend(조각)
                대화기록.extend(조각)
        return មាតិកា_តំលៃ.decode('utf-8', 'replace').replace('\r\n','\n')
    def 셸(ពាក្យ_បញ្ជា, បង្ហាញ_តំលៃ=b'jkoros-native> '):
        ដំណើរការ.stdin.write(ពាក្យ_បញ្ជា.encode()+b'\n')
        ដំណើរការ.stdin.flush()
        return 기다리기(បង្ហាញ_តំលៃ)
    def អនុវត្ត_ពាក្យបញ្ជា(ពាក្យ_បញ្ជា, 예상, ភាព_តំលៃ=0):
        មាតិកា_តំលៃ = 셸(ពាក្យ_បញ្ជា)
        assert 예상 in មាតិកា_តំលៃ and '\nexit '+str(ភាព_តំលៃ)+'\n' in មាតិកា_តំលៃ, មាតិកា_តំលៃ
        ធ្វើអោយមានសុពលភាព['checks'].append(ពាក្យ_បញ្ជា)
        return មាតិកា_តំលៃ
    def បង្ហោះ_ឯកសារ(ឈ្មោះ, ទិន្នន័យ):
        셸('load '+ឈ្មោះ, b'hex> ')
        for កំណត់ទីតាំង_សន្ទស្សន៏ in range(0, len(ទិន្នន័យ), 64):
            셸(ទិន្នន័យ[កំណត់ទីតាំង_សន្ទស្សន៏:កំណត់ទីតាំង_សន្ទស្សន៏+64].hex(), b'hex> ')
        assert 'LOADED' in 셸('.')
    try:
        기다리기()
        អនុវត្ត_ពាក្យបញ្ជា('pip --help', 'MicroPython ប្រភព_មែកធាង 설치기')
        បង្ហោះ_ឯកសារ('오류시험.py', (បញ្ចាំង_ឬស/'시험/파이썬/한국어오류시험.py').read_bytes())
        អនុវត្ត_ពាក្យបញ្ជា('python 오류시험.py', '한국어 ឯកសារ ការលើកលែង ផ្ទៀងផ្ទាត់')
        អនុវត្ត_ពាក្យបញ្ជា('pip install micropython-bisect==3.3.3 --port '+str(លេខរន្ធ), 'ដំឡើង_តំលៃ 완료: micropython-bisect 3.3.3')
        អនុវត្ត_ពាក្យបញ្ជា('python -c \'from bisect import insort as 순서대로넣기; តំលៃ=[1,5]; 순서대로넣기(តំលៃ,3); print(តំលៃ)\'', '[1, 3, 5]')
        អនុវត្ត_ពាក្យបញ្ជា('python -m pip list', 'micropython-bisect 3.3.3')
        អនុវត្ត_ពាក្យបញ្ជា('pip install micropython-bisect==3.3.3 --port '+str(លេខរន្ធ), '이미 설치됨:')
        អនុវត្ត_ពាក្យបញ្ជា('pip install jkoros-fixture==1.0 --port '+str(លេខរន្ធ), 'ដំឡើង_តំលៃ 완료: jkoros-fixture')
        អនុវត្ត_ពាក្យបញ្ជា('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        អនុវត្ត_ពាក្យបញ្ជា('pip install jkoros-syntax==1.0 --port '+str(លេខរន្ធ), 'បាច់ កំហុស:', 1)
        អនុវត្ត_ពាក្យបញ្ជា('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 កំហុស 보존")\'', '구문 កំហុស 보존')
        បង្ហោះ_ឯកសារ('공간시험.py', (បញ្ចាំង_ឬស/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        អនុវត្ត_ពាក្យបញ្ជា('python 공간시험.py '+str(លេខរន្ធ), 'បាច់ 공간 부족 되돌림 ផ្ទៀងផ្ទាត់')
        អនុវត្ត_ពាក្យបញ្ជា('pip uninstall jkoros-fixture', 'យកចេញ_ការបញ្ចូល 완료: jkoros-fixture')
        អនុវត្ត_ពាក្យបញ្ជា('pip uninstall micropython-bisect', 'យកចេញ_ការបញ្ចូល 완료: micropython-bisect')
        អនុវត្ត_ពាក្យបញ្ជា('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("យកចេញ_ការបញ្ចូល ផ្ទៀងផ្ទាត់")\'', 'យកចេញ_ការបញ្ចូល ផ្ទៀងផ្ទាត់')
        ធ្វើអោយមានសុពលភាព['passed'] = True
        print('PASS: PyPI 실물 ដំឡើង_តំលៃ·import·អនុវត្ត_ពាក្យបញ្ជា, 한국어 ការលើកលែង, 패키지 បញ្ជី_តំលៃ, បរាជ័យ_តំលៃ 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 ចេញ_កម្មវិធី 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            ដំណើរការ.stdin.write(b'\x01x')
            ដំណើរការ.stdin.flush()
            ដំណើរការ.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            ដំណើរការ.terminate()
            try:
                ដំណើរការ.wait(timeout=8)
            except subprocess.TimeoutExpired:
                ដំណើរការ.kill()
                ដំណើរការ.wait()
        if ដំណើរការ.poll() is None:
            ដំណើរការ.kill()
            ដំណើរការ.wait()
        អ្នកជ្រើសរើស_a916db4e.close()
        ដំណើរការ.stdin.close()
        ដំណើរការ.stdout.close()
        (ការវាស់វែង_ផ្លូវ/'serial.log').write_bytes(대화기록)
        (ការវាស់វែង_ផ្លូវ/'report.json').write_text(json.dumps(ធ្វើអោយមានសុពលភាព, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    រត់()
