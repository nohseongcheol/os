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
from phethagatša_taelo import 기준


def 시험휠(Leina, 파일들, taba_boleng='Root-Is-Purelib: true\n', 의존성=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as sehlopha:
        sehlopha.writestr(Leina + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + taba_boleng)
        sehlopha.writestr(Leina + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Leina + '\nVersion: 1.0\n' + 의존성)
        for Tsejana, Diteng_boleng in 파일들.items():
            sehlopha.writestr(Tsejana, Diteng_boleng)
    return data.getvalue()


def lekola_go_nea_ditirelo():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'boleng=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'boleng=42\n'.encode()}
    for data in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', data, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Tsejana·Bogolo·C koketšo_boleng·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Diriša():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    lekola_go_nea_ditirelo()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Bobolokelo_tsela = 결과경로/'cache'
    Bobolokelo_tsela.mkdir(exist_ok=True)
    # kgonthe_data PyPI 배포 Faele. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').Lokišetša('micropython-bisect==3.3.3')
    for theile_boleng in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+theile_boleng)), str(Bobolokelo_tsela/('micropython-bisect==3.3.3'+theile_boleng)))
    실물기록 = json.loads((Bobolokelo_tsela/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Leina, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'boleng=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = 시험휠(Leina, 파일들)
        (Bobolokelo_tsela/(Leina+'==1.0.archive')).write_bytes(data)
        (Bobolokelo_tsela/(Leina+'==1.0.json')).write_text(json.dumps({'name': Leina, 'version': '1.0',
            'filename': Leina.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    kgonthiša_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    tiragalo_a7054519 = subprocess.Popen(['python3', str(기준/'Ditholosi/phethagatša_taelo.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Bobolokelo_tsela), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    sekgethi_a916db4e = selectors.DefaultSelector()
    sekgethi_a916db4e.register(tiragalo_a7054519.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(bontšha_boleng=b'jkoros-native> '):
        Diteng_boleng = bytearray()
        끝 = time.monotonic()+120
        while bontšha_boleng not in Diteng_boleng:
            if time.monotonic() > 끝 or tiragalo_a7054519.poll() is not None:
                raise AssertionError('게스트 fetola 없음: '+Diteng_boleng.decode('utf-8','replace'))
            for go_tsenya_tshedimošo_boleng, _ in sekgethi_a916db4e.select(.1):
                조각 = go_tsenya_tshedimošo_boleng.fileobj.read(4096)
                Diteng_boleng.extend(조각)
                대화기록.extend(조각)
        return Diteng_boleng.decode('utf-8', 'replace').replace('\r\n','\n')
    def šele(Taelo, bontšha_boleng=b'jkoros-native> '):
        tiragalo_a7054519.stdin.write(Taelo.encode()+b'\n')
        tiragalo_a7054519.stdin.flush()
        return 기다리기(bontšha_boleng)
    def phethagatša_taelo(Taelo, 예상, boemo_boleng=0):
        Diteng_boleng = šele(Taelo)
        assert 예상 in Diteng_boleng and '\nexit '+str(boemo_boleng)+'\n' in Diteng_boleng, Diteng_boleng
        kgonthiša_5fb2b747['checks'].append(Taelo)
        return Diteng_boleng
    def apolouto_Difaele(Leina, data):
        šele('load '+Leina, b'hex> ')
        for 자리 in range(0, len(data), 64):
            šele(data[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in šele('.')
    try:
        기다리기()
        phethagatša_taelo('pip --help', 'MicroPython mohlodi_mohlare 설치기')
        apolouto_Difaele('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        phethagatša_taelo('python 오류시험.py', '한국어 Faele 예외 kgonthiša')
        phethagatša_taelo('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'hloma_boleng 완료: micropython-bisect 3.3.3')
        phethagatša_taelo('python -c \'from bisect import insort as 순서대로넣기; boleng=[1,5]; 순서대로넣기(boleng,3); print(boleng)\'', '[1, 3, 5]')
        phethagatša_taelo('python -m pip list', 'micropython-bisect 3.3.3')
        phethagatša_taelo('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        phethagatša_taelo('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'hloma_boleng 완료: jkoros-fixture')
        phethagatša_taelo('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        phethagatša_taelo('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'sehlopha Phošo:', 1)
        phethagatša_taelo('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Phošo 보존")\'', '구문 Phošo 보존')
        apolouto_Difaele('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        phethagatša_taelo('python 공간시험.py '+str(접속번호), 'sehlopha 공간 부족 되돌림 kgonthiša')
        phethagatša_taelo('pip uninstall jkoros-fixture', 'tloša_go_tsenya_tshedimošo 완료: jkoros-fixture')
        phethagatša_taelo('pip uninstall micropython-bisect', 'tloša_go_tsenya_tshedimošo 완료: micropython-bisect')
        phethagatša_taelo('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("tloša_go_tsenya_tshedimošo kgonthiša")\'', 'tloša_go_tsenya_tshedimošo kgonthiša')
        kgonthiša_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 hloma_boleng·import·phethagatša_taelo, 한국어 예외, 패키지 lelokelelo_boleng, go_palelwa_boleng 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Etšwa_tirišo 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            tiragalo_a7054519.stdin.write(b'\x01x')
            tiragalo_a7054519.stdin.flush()
            tiragalo_a7054519.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            tiragalo_a7054519.terminate()
            try:
                tiragalo_a7054519.wait(timeout=8)
            except subprocess.TimeoutExpired:
                tiragalo_a7054519.kill()
                tiragalo_a7054519.wait()
        if tiragalo_a7054519.poll() is None:
            tiragalo_a7054519.kill()
            tiragalo_a7054519.wait()
        sekgethi_a916db4e.close()
        tiragalo_a7054519.stdin.close()
        tiragalo_a7054519.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(kgonthiša_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Diriša()
