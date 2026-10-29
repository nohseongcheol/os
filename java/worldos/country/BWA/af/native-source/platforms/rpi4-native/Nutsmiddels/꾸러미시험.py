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
from 꾸러미중계 import bondel_bewaarplek, 압축풀기
from uitvoer_bevel import Project_wortel


def 시험휠(Naam, 파일들, saak_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as bondel:
        bondel.writestr(Naam + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + saak_VALUE)
        bondel.writestr(Naam + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Naam + '\nVersion: 1.0\n' + 의존성)
        for Pad, Inhoud_VALUE in 파일들.items():
            bondel.writestr(Pad, Inhoud_VALUE)
    return data.getvalue()


def tjek_hou():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
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
    print('PASS: wheel Pad·Grootte·C uitbreiding_VALUE·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Loop():
    ontleder_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ontleder_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = ontleder_48ee4b1b.parse_args()
    tjek_hou()
    if 인수.host_only:
        return
    maatreël_pad = Project_wortel/'build/verification/pip'
    maatreël_pad.mkdir(parents=True, exist_ok=True)
    Berging_pad = maatreël_pad/'cache'
    Berging_pad.mkdir(exist_ok=True)
    # werklik_data PyPI 배포 Lêer. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    bondel_bewaarplek(Project_wortel/'build/pip-cache').Maak_gereed('micropython-bisect==3.3.3')
    for stert_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(Project_wortel/'build/pip-cache'/('micropython-bisect==3.3.3'+stert_VALUE)), str(Berging_pad/('micropython-bisect==3.3.3'+stert_VALUE)))
    hardeware_LOG = json.loads((Berging_pad/'micropython-bisect==3.3.3.json').read_text())
    assert hardeware_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Naam, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = 시험휠(Naam, 파일들)
        (Berging_pad/(Naam+'==1.0.archive')).write_bytes(data)
        (Berging_pad/(Naam+'==1.0.json')).write_text(json.dumps({'name': Naam, 'version': '1.0',
            'filename': Naam.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    valideer = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': hardeware_LOG, 'checks': []}
    접속번호 = 빈접속번호()
    Proses = subprocess.Popen(['python3', str(Project_wortel/'Nutsmiddels/uitvoer_bevel.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Berging_pad), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selekteerder_a916db4e = selectors.DefaultSelector()
    selekteerder_a916db4e.register(Proses.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(wys_VALUE=b'jkoros-native> '):
        Inhoud_VALUE = bytearray()
        끝 = time.monotonic()+120
        while wys_VALUE not in Inhoud_VALUE:
            if time.monotonic() > 끝 or Proses.poll() is not None:
                raise AssertionError('게스트 antwoord 없음: '+Inhoud_VALUE.decode('utf-8','replace'))
            for inskrywing_VALUE, _ in selekteerder_a916db4e.select(.1):
                조각 = inskrywing_VALUE.fileobj.read(4096)
                Inhoud_VALUE.extend(조각)
                대화기록.extend(조각)
        return Inhoud_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def dop(Opdrag, wys_VALUE=b'jkoros-native> '):
        Proses.stdin.write(Opdrag.encode()+b'\n')
        Proses.stdin.flush()
        return 기다리기(wys_VALUE)
    def uitvoer_bevel(Opdrag, 예상, stand_VALUE=0):
        Inhoud_VALUE = dop(Opdrag)
        assert 예상 in Inhoud_VALUE and '\nexit '+str(stand_VALUE)+'\n' in Inhoud_VALUE, Inhoud_VALUE
        valideer['checks'].append(Opdrag)
        return Inhoud_VALUE
    def oplaai_Lêers(Naam, data):
        dop('load '+Naam, b'hex> ')
        for plaas_INDEX in range(0, len(data), 64):
            dop(data[plaas_INDEX:plaas_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in dop('.')
    try:
        기다리기()
        uitvoer_bevel('pip --help', 'MicroPython bron_boom 설치기')
        oplaai_Lêers('오류시험.py', (Project_wortel/'시험/PYTHON/한국어오류시험.py').read_bytes())
        uitvoer_bevel('python 오류시험.py', '한국어 Lêer uitsondering verifieer')
        uitvoer_bevel('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'installeer_VALUE 완료: micropython-bisect 3.3.3')
        uitvoer_bevel('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        uitvoer_bevel('python -m pip list', 'micropython-bisect 3.3.3')
        uitvoer_bevel('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        uitvoer_bevel('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'installeer_VALUE 완료: jkoros-fixture')
        uitvoer_bevel('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        uitvoer_bevel('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'bondel Fout:', 1)
        uitvoer_bevel('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Fout 보존")\'', '구문 Fout 보존')
        oplaai_Lêers('공간시험.py', (Project_wortel/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        uitvoer_bevel('python 공간시험.py '+str(접속번호), 'bondel 공간 부족 teruggee_brug verifieer')
        uitvoer_bevel('pip uninstall jkoros-fixture', 'verwyder_inskrywing 완료: jkoros-fixture')
        uitvoer_bevel('pip uninstall micropython-bisect', 'verwyder_inskrywing 완료: micropython-bisect')
        uitvoer_bevel('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("verwyder_inskrywing verifieer")\'', 'verwyder_inskrywing verifieer')
        valideer['passed'] = True
        print('PASS: PyPI 실물 installeer_VALUE·import·uitvoer_bevel, 한국어 uitsondering, 패키지 gids_VALUE, faling_VALUE teruggee_brug, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Verlaat_program 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
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
        selekteerder_a916db4e.close()
        Proses.stdin.close()
        Proses.stdout.close()
        (maatreël_pad/'serial.log').write_bytes(대화기록)
        (maatreël_pad/'report.json').write_text(json.dumps(valideer, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Loop()
