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
from diragatsa_Taelo import 기준


def 시험휠(leina, 파일들, konteraka_Boleng='Root-Is-Purelib: true\n', 의존성=''):
    tshedimosetso = io.BytesIO()
    with zipfile.ZipFile(tshedimosetso, 'w', zipfile.ZIP_DEFLATED) as ngatanngwe:
        ngatanngwe.writestr(leina + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + konteraka_Boleng)
        ngatanngwe.writestr(leina + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + leina + '\nVersion: 1.0\n' + 의존성)
        for tsela, Diteng_Boleng in 파일들.items():
            ngatanngwe.writestr(tsela, Diteng_Boleng)
    return tshedimosetso.getvalue()


def tlhola_pinagare():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'Boleng=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'Boleng=42\n'.encode()}
    for tshedimosetso in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', tshedimosetso, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel tsela·lekanya·C katoloso_Boleng·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def dirisa():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    tlhola_pinagare()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Polokelo_tsela = 결과경로/'cache'
    Polokelo_tsela.mkdir(exist_ok=True)
    # tota_tshedimosetso PyPI 배포 faele. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').Baakanya('micropython-bisect==3.3.3')
    for mogatla_Boleng in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+mogatla_Boleng)), str(Polokelo_tsela/('micropython-bisect==3.3.3'+mogatla_Boleng)))
    실물기록 = json.loads((Polokelo_tsela/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for leina, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'Boleng=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        tshedimosetso = 시험휠(leina, 파일들)
        (Polokelo_tsela/(leina+'==1.0.archive')).write_bytes(tshedimosetso)
        (Polokelo_tsela/(leina+'==1.0.json')).write_text(json.dumps({'name': leina, 'version': '1.0',
            'filename': leina.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(tshedimosetso).hexdigest()}))
    netefatsa_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Thulaganyo = subprocess.Popen(['python3', str(기준/'Thuluse/diragatsa_Taelo.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Polokelo_tsela), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    setlhophi_a916db4e = selectors.DefaultSelector()
    setlhophi_a916db4e.register(Thulaganyo.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(bontsha_Boleng=b'jkoros-native> '):
        Diteng_Boleng = bytearray()
        끝 = time.monotonic()+120
        while bontsha_Boleng not in Diteng_Boleng:
            if time.monotonic() > 끝 or Thulaganyo.poll() is not None:
                raise AssertionError('게스트 araba 없음: '+Diteng_Boleng.decode('utf-8','replace'))
            for tsenyo_Boleng, _ in setlhophi_a916db4e.select(.1):
                조각 = tsenyo_Boleng.fileobj.read(4096)
                Diteng_Boleng.extend(조각)
                대화기록.extend(조각)
        return Diteng_Boleng.decode('utf-8', 'replace').replace('\r\n','\n')
    def setlhalosataelo(Taelo, bontsha_Boleng=b'jkoros-native> '):
        Thulaganyo.stdin.write(Taelo.encode()+b'\n')
        Thulaganyo.stdin.flush()
        return 기다리기(bontsha_Boleng)
    def diragatsa_Taelo(Taelo, 예상, kemo_Boleng=0):
        Diteng_Boleng = setlhalosataelo(Taelo)
        assert 예상 in Diteng_Boleng and '\nexit '+str(kemo_Boleng)+'\n' in Diteng_Boleng, Diteng_Boleng
        netefatsa_5fb2b747['checks'].append(Taelo)
        return Diteng_Boleng
    def laisa_Difaele(leina, tshedimosetso):
        setlhalosataelo('load '+leina, b'hex> ')
        for 자리 in range(0, len(tshedimosetso), 64):
            setlhalosataelo(tshedimosetso[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in setlhalosataelo('.')
    try:
        기다리기()
        diragatsa_Taelo('pip --help', 'MicroPython Motswedi_sebopego_sa_tshedimosetso 설치기')
        laisa_Difaele('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        diragatsa_Taelo('python 오류시험.py', '한국어 faele 예외 netefatsa')
        diragatsa_Taelo('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'tsenya_Boleng 완료: micropython-bisect 3.3.3')
        diragatsa_Taelo('python -c \'from bisect import insort as 순서대로넣기; Boleng=[1,5]; 순서대로넣기(Boleng,3); print(Boleng)\'', '[1, 3, 5]')
        diragatsa_Taelo('python -m pip list', 'micropython-bisect 3.3.3')
        diragatsa_Taelo('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        diragatsa_Taelo('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'tsenya_Boleng 완료: jkoros-fixture')
        diragatsa_Taelo('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        diragatsa_Taelo('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'ngatanngwe phoso:', 1)
        diragatsa_Taelo('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 phoso 보존")\'', '구문 phoso 보존')
        laisa_Difaele('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        diragatsa_Taelo('python 공간시험.py '+str(접속번호), 'ngatanngwe 공간 부족 되돌림 netefatsa')
        diragatsa_Taelo('pip uninstall jkoros-fixture', 'tlosa_tsenyo 완료: jkoros-fixture')
        diragatsa_Taelo('pip uninstall micropython-bisect', 'tlosa_tsenyo 완료: micropython-bisect')
        diragatsa_Taelo('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("tlosa_tsenyo netefatsa")\'', 'tlosa_tsenyo netefatsa')
        netefatsa_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 tsenya_Boleng·import·diragatsa_Taelo, 한국어 예외, 패키지 Lenaneofaele_Boleng, palelo_Boleng 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 tswaya_Tiriso 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Thulaganyo.stdin.write(b'\x01x')
            Thulaganyo.stdin.flush()
            Thulaganyo.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Thulaganyo.terminate()
            try:
                Thulaganyo.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Thulaganyo.kill()
                Thulaganyo.wait()
        if Thulaganyo.poll() is None:
            Thulaganyo.kill()
            Thulaganyo.wait()
        setlhophi_a916db4e.close()
        Thulaganyo.stdin.close()
        Thulaganyo.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(netefatsa_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    dirisa()
