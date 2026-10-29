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
from Gweithredu_gorchymyn import prosiect_gwraidd


def 시험휠(Enw, 파일들, tasg_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as bwndel:
        bwndel.writestr(Enw + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + tasg_VALUE)
        bwndel.writestr(Enw + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Enw + '\nVersion: 1.0\n' + 의존성)
        for LLWYBR, Cynnwys_VALUE in 파일들.items():
            bwndel.writestr(LLWYBR, Cynnwys_VALUE)
    return data.getvalue()


def gwirio_lletya():
    technoleg_gwybodaeth_normal = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', technoleg_gwybodaeth_normal, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
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
    print('PASS: wheel LLWYBR·Maint·C estyniad_VALUE·의존성 gwrthod_VALUE')


def gwag_rhif_porth():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Gweithredu_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    gwirio_lletya()
    if 인수.host_only:
        return
    mesur_llwybr = prosiect_gwraidd/'build/verification/pip'
    mesur_llwybr.mkdir(parents=True, exist_ok=True)
    Storio_llwybr = mesur_llwybr/'cache'
    Storio_llwybr.mkdir(exist_ok=True)
    # go_iawn_data PyPI 배포 Ffeil. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(prosiect_gwraidd/'build/pip-cache').Paratoi('micropython-bisect==3.3.3')
    for cynffon_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(prosiect_gwraidd/'build/pip-cache'/('micropython-bisect==3.3.3'+cynffon_VALUE)), str(Storio_llwybr/('micropython-bisect==3.3.3'+cynffon_VALUE)))
    실물기록 = json.loads((Storio_llwybr/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Enw, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = 시험휠(Enw, 파일들)
        (Storio_llwybr/(Enw+'==1.0.archive')).write_bytes(data)
        (Storio_llwybr/(Enw+'==1.0.json')).write_text(json.dumps({'name': Enw, 'version': '1.0',
            'filename': Enw.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    dilysu_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((prosiect_gwraidd/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    rhif_porth = gwag_rhif_porth()
    Proses = subprocess.Popen(['python3', str(prosiect_gwraidd/'Offer/Gweithredu_gorchymyn.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(rhif_porth), '--pip-cache', str(Storio_llwybr), '--ftp-port', str(gwag_rhif_porth())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    dewisydd_a916db4e = selectors.DefaultSelector()
    dewisydd_a916db4e.register(Proses.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(sioe_VALUE=b'jkoros-native> '):
        Cynnwys_VALUE = bytearray()
        끝 = time.monotonic()+120
        while sioe_VALUE not in Cynnwys_VALUE:
            if time.monotonic() > 끝 or Proses.poll() is not None:
                raise AssertionError('게스트 ateb 없음: '+Cynnwys_VALUE.decode('utf-8','replace'))
            for cofnod_VALUE, _ in dewisydd_a916db4e.select(.1):
                조각 = cofnod_VALUE.fileobj.read(4096)
                Cynnwys_VALUE.extend(조각)
                대화기록.extend(조각)
        return Cynnwys_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def cragen(Gorchymyn, sioe_VALUE=b'jkoros-native> '):
        Proses.stdin.write(Gorchymyn.encode()+b'\n')
        Proses.stdin.flush()
        return 기다리기(sioe_VALUE)
    def Gweithredu_gorchymyn(Gorchymyn, 예상, cyflwr_VALUE=0):
        Cynnwys_VALUE = cragen(Gorchymyn)
        assert 예상 in Cynnwys_VALUE and '\nexit '+str(cyflwr_VALUE)+'\n' in Cynnwys_VALUE, Cynnwys_VALUE
        dilysu_5fb2b747['checks'].append(Gorchymyn)
        return Cynnwys_VALUE
    def Upload_Ffeil(Enw, data):
        cragen('load '+Enw, b'hex> ')
        for safle_INDEX in range(0, len(data), 64):
            cragen(data[safle_INDEX:safle_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in cragen('.')
    try:
        기다리기()
        Gweithredu_gorchymyn('pip --help', 'MicroPython ffynhonnell_coeden 설치기')
        Upload_Ffeil('오류시험.py', (prosiect_gwraidd/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Gweithredu_gorchymyn('python 오류시험.py', 'Cymraeg Ffeil eithriad dilysu')
        Gweithredu_gorchymyn('pip install micropython-bisect==3.3.3 --port '+str(rhif_porth), 'gosod_VALUE 완료: micropython-bisect 3.3.3')
        Gweithredu_gorchymyn('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Gweithredu_gorchymyn('python -m pip list', 'micropython-bisect 3.3.3')
        Gweithredu_gorchymyn('pip install micropython-bisect==3.3.3 --port '+str(rhif_porth), '이미 설치됨:')
        Gweithredu_gorchymyn('pip install jkoros-fixture==1.0 --port '+str(rhif_porth), 'gosod_VALUE 완료: jkoros-fixture')
        Gweithredu_gorchymyn('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Gweithredu_gorchymyn('pip install jkoros-syntax==1.0 --port '+str(rhif_porth), 'bwndel Gwall:', 1)
        Gweithredu_gorchymyn('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Gwall 보존")\'', '구문 Gwall 보존')
        Upload_Ffeil('공간시험.py', (prosiect_gwraidd/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Gweithredu_gorchymyn('python 공간시험.py '+str(rhif_porth), 'bwndel 공간 부족 return_pont dilysu')
        Gweithredu_gorchymyn('pip uninstall jkoros-fixture', 'tynnu_cofnod 완료: jkoros-fixture')
        Gweithredu_gorchymyn('pip uninstall micropython-bisect', 'tynnu_cofnod 완료: micropython-bisect')
        Gweithredu_gorchymyn('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("tynnu_cofnod dilysu")\'', 'tynnu_cofnod dilysu')
        dilysu_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 gosod_VALUE·import·Gweithredu_gorchymyn, Cymraeg eithriad, 패키지 cyfeiriadur_VALUE, methiant_VALUE return_pont, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 gadael_Rhaglen 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Proses.stdin.write(b'\x01x')
            Proses.stdin.flush()
            Proses.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Proses.terminate()
            try:
                Proses.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Proses.kill()
                Proses.wait()
        if Proses.poll() is None:
            Proses.kill()
            Proses.wait()
        dewisydd_a916db4e.close()
        Proses.stdin.close()
        Proses.stdout.close()
        (mesur_llwybr/'serial.log').write_bytes(대화기록)
        (mesur_llwybr/'report.json').write_text(json.dumps(dilysu_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Gweithredu_2()
