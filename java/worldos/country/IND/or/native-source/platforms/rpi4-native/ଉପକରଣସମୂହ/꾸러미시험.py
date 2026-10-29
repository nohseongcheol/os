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
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍


def 시험휠(ନାମ, 파일들, କର୍ମ_ମୂଲ୍ୟ='Root-Is-Purelib: true\n', 의존성=''):
    ଡାଟା = io.BytesIO()
    with zipfile.ZipFile(ଡାଟା, 'w', zipfile.ZIP_DEFLATED) as ବଣ୍ଡଲ୍:
        ବଣ୍ଡଲ୍.writestr(ନାମ + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + କର୍ମ_ମୂଲ୍ୟ)
        ବଣ୍ଡଲ୍.writestr(ନାମ + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ନାମ + '\nVersion: 1.0\n' + 의존성)
        for ପଥ, ବିଷୟ_ମୂଲ୍ୟ in 파일들.items():
            ବଣ୍ଡଲ୍.writestr(ପଥ, ବିଷୟ_ମୂଲ୍ୟ)
    return ଡାଟା.getvalue()


def ପରୀକ୍ଷିତ_ଆୟୋଜକ():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'ମୂଲ୍ୟ=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'ମୂଲ୍ୟ=42\n'.encode()}
    for ଡାଟା in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ଡାଟା, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ପଥ·ଆକାର·C ଏକ୍ସଟେନସନ୍_ମୂଲ୍ୟ·의존성 ପ୍ରତ୍ୟାକ୍ଷାନ_ମୂଲ୍ୟ')


def ଖାଲି_ପୋର୍ଟ୍_ନମ୍ଵର୍():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ଚଳାନ୍ତୁ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    ପରୀକ୍ଷିତ_ଆୟୋଜକ()
    if 인수.host_only:
        return
    ମାପ_ପଥ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/pip'
    ମାପ_ପଥ.mkdir(parents=True, exist_ok=True)
    ଷ୍ଟୋରେଜ୍_ପଥ = ମାପ_ପଥ/'cache'
    ଷ୍ଟୋରେଜ୍_ପଥ.mkdir(exist_ok=True)
    # ପ୍ରକୃତ_ଡାଟା PyPI 배포 ଫାଇଲ. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/pip-cache').ପ୍ରସ୍ତୁତ('micropython-bisect==3.3.3')
    for ପୁଚ୍ଛ_ମୂଲ୍ୟ in ('.archive', '.json'):
        shutil.copyfile(str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/pip-cache'/('micropython-bisect==3.3.3'+ପୁଚ୍ଛ_ମୂଲ୍ୟ)), str(ଷ୍ଟୋରେଜ୍_ପଥ/('micropython-bisect==3.3.3'+ପୁଚ୍ଛ_ମୂଲ୍ୟ)))
    ହାର୍ଡୱେର୍_ଲଗ୍ = json.loads((ଷ୍ଟୋରେଜ୍_ପଥ/'micropython-bisect==3.3.3.json').read_text())
    assert ହାର୍ଡୱେର୍_ଲଗ୍['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ନାମ, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'ମୂଲ୍ୟ=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ଡାଟା = 시험휠(ନାମ, 파일들)
        (ଷ୍ଟୋରେଜ୍_ପଥ/(ନାମ+'==1.0.archive')).write_bytes(ଡାଟା)
        (ଷ୍ଟୋରେଜ୍_ପଥ/(ନାମ+'==1.0.json')).write_text(json.dumps({'name': ନାମ, 'version': '1.0',
            'filename': ନାମ.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ଡାଟା).hexdigest()}))
    ବୈଧକରଣ = {'passed': False, 'kernel_sha256': hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': ହାର୍ଡୱେର୍_ଲଗ୍, 'checks': []}
    ପୋର୍ଟ୍_ନମ୍ଵର୍ = ଖାଲି_ପୋର୍ଟ୍_ନମ୍ଵର୍()
    ପ୍ରକ୍ରିୟା = subprocess.Popen(['python3', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(ପୋର୍ଟ୍_ନମ୍ଵର୍), '--pip-cache', str(ଷ୍ଟୋରେଜ୍_ପଥ), '--ftp-port', str(ଖାଲି_ପୋର୍ଟ୍_ନମ୍ଵର୍())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ଚୟନକାରୀ_a916db4e = selectors.DefaultSelector()
    ଚୟନକାରୀ_a916db4e.register(ପ୍ରକ୍ରିୟା.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ=b'jkoros-native> '):
        ବିଷୟ_ମୂଲ୍ୟ = bytearray()
        끝 = time.monotonic()+120
        while ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ not in ବିଷୟ_ମୂଲ୍ୟ:
            if time.monotonic() > 끝 or ପ୍ରକ୍ରିୟା.poll() is not None:
                raise AssertionError('게스트 ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ 없음: '+ବିଷୟ_ମୂଲ୍ୟ.decode('utf-8','replace'))
            for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, _ in ଚୟନକାରୀ_a916db4e.select(.1):
                조각 = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.fileobj.read(4096)
                ବିଷୟ_ମୂଲ୍ୟ.extend(조각)
                대화기록.extend(조각)
        return ବିଷୟ_ମୂଲ୍ୟ.decode('utf-8', 'replace').replace('\r\n','\n')
    def ଖୋଳ(ନିର୍ଦ୍ଦେଶ, ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ=b'jkoros-native> '):
        ପ୍ରକ୍ରିୟା.stdin.write(ନିର୍ଦ୍ଦେଶ.encode()+b'\n')
        ପ୍ରକ୍ରିୟା.stdin.flush()
        return 기다리기(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ)
    def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ନିର୍ଦ୍ଦେଶ, 예상, ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1=0):
        ବିଷୟ_ମୂଲ୍ୟ = ଖୋଳ(ନିର୍ଦ୍ଦେଶ)
        assert 예상 in ବିଷୟ_ମୂଲ୍ୟ and '\nexit '+str(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1)+'\n' in ବିଷୟ_ମୂଲ୍ୟ, ବିଷୟ_ମୂଲ୍ୟ
        ବୈଧକରଣ['checks'].append(ନିର୍ଦ୍ଦେଶ)
        return ବିଷୟ_ମୂଲ୍ୟ
    def ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ(ନାମ, ଡାଟା):
        ଖୋଳ('load '+ନାମ, b'hex> ')
        for ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା in range(0, len(ଡାଟା), 64):
            ଖୋଳ(ଡାଟା[ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା:ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା+64].hex(), b'hex> ')
        assert 'LOADED' in ଖୋଳ('.')
    try:
        기다리기()
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('pip --help', 'MicroPython ଉତ୍ସ_ବୃକ୍ଷ 설치기')
        ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('오류시험.py', (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'시험/파이썬/한국어오류시험.py').read_bytes())
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('python 오류시험.py', '한국어 ଫାଇଲ ବ୍ୟତିକ୍ରମ ଯାଞ୍ଚ୍_କରିବା')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('pip install micropython-bisect==3.3.3 --port '+str(ପୋର୍ଟ୍_ନମ୍ଵର୍), 'ସଂସ୍ଥାପନ_ମୂଲ୍ୟ 완료: micropython-bisect 3.3.3')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('python -c \'from bisect import insort as 순서대로넣기; ମୂଲ୍ୟ=[1,5]; 순서대로넣기(ମୂଲ୍ୟ,3); print(ମୂଲ୍ୟ)\'', '[1, 3, 5]')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('python -m pip list', 'micropython-bisect 3.3.3')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('pip install micropython-bisect==3.3.3 --port '+str(ପୋର୍ଟ୍_ନମ୍ଵର୍), '이미 설치됨:')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('pip install jkoros-fixture==1.0 --port '+str(ପୋର୍ଟ୍_ନମ୍ଵର୍), 'ସଂସ୍ଥାପନ_ମୂଲ୍ୟ 완료: jkoros-fixture')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('pip install jkoros-syntax==1.0 --port '+str(ପୋର୍ଟ୍_ନମ୍ଵର୍), 'ବଣ୍ଡଲ୍ ତ୍ରୁଟି:', 1)
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ତ୍ରୁଟି 보존")\'', '구문 ତ୍ରୁଟି 보존')
        ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('공간시험.py', (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('python 공간시험.py '+str(ପୋର୍ଟ୍_ନମ୍ଵର୍), 'ବଣ୍ଡଲ୍ 공간 부족 되돌림 ଯାଞ୍ଚ୍_କରିବା')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('pip uninstall jkoros-fixture', 'ଅପସାରଣ_କରିବା_ଏଣ୍ଟ୍ରି 완료: jkoros-fixture')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('pip uninstall micropython-bisect', 'ଅପସାରଣ_କରିବା_ଏଣ୍ଟ୍ରି 완료: micropython-bisect')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ଅପସାରଣ_କରିବା_ଏଣ୍ଟ୍ରି ଯାଞ୍ଚ୍_କରିବା")\'', 'ଅପସାରଣ_କରିବା_ଏଣ୍ଟ୍ରି ଯାଞ୍ଚ୍_କରିବା')
        ବୈଧକରଣ['passed'] = True
        print('PASS: PyPI 실물 ସଂସ୍ଥାପନ_ମୂଲ୍ୟ·import·ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ, 한국어 ବ୍ୟତିକ୍ରମ, 패키지 ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ, ବିଫଳତା_ମୂଲ୍ୟ 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            ପ୍ରକ୍ରିୟା.stdin.write(b'\x01x')
            ପ୍ରକ୍ରିୟା.stdin.flush()
            ପ୍ରକ୍ରିୟା.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            ପ୍ରକ୍ରିୟା.terminate()
            try:
                ପ୍ରକ୍ରିୟା.wait(timeout=8)
            except subprocess.TimeoutExpired:
                ପ୍ରକ୍ରିୟା.kill()
                ପ୍ରକ୍ରିୟା.wait()
        if ପ୍ରକ୍ରିୟା.poll() is None:
            ପ୍ରକ୍ରିୟା.kill()
            ପ୍ରକ୍ରିୟା.wait()
        ଚୟନକାରୀ_a916db4e.close()
        ପ୍ରକ୍ରିୟା.stdin.close()
        ପ୍ରକ୍ରିୟା.stdout.close()
        (ମାପ_ପଥ/'serial.log').write_bytes(대화기록)
        (ମାପ_ପଥ/'report.json').write_text(json.dumps(ବୈଧକରଣ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ଚଳାନ୍ତୁ()
