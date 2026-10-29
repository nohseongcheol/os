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
from Utfør_kommando import spegle_rot


def 시험휠(Namn, 파일들, sak_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as bunt:
        bunt.writestr(Namn + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + sak_VALUE)
        bunt.writestr(Namn + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Namn + '\nVersion: 1.0\n' + 의존성)
        for STIGE, Innhald_VALUE in 파일들.items():
            bunt.writestr(STIGE, Innhald_VALUE)
    return data.getvalue()


def sjekk_vert():
    informasjonsteknologi_normal = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', informasjonsteknologi_normal, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
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
    print('PASS: wheel STIGE·Storleik·C filtype_VALUE·의존성 avvise_VALUE')


def tom_portnummer():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Køyr_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    Argument = 해석기.parse_args()
    sjekk_vert()
    if Argument.host_only:
        return
    forretningsmål_bane = spegle_rot/'build/verification/pip'
    forretningsmål_bane.mkdir(parents=True, exist_ok=True)
    Lagring_bane = forretningsmål_bane/'cache'
    Lagring_bane.mkdir(exist_ok=True)
    # faktisk_data PyPI 배포 Fil. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(spegle_rot/'build/pip-cache').Klargjer('micropython-bisect==3.3.3')
    for side_VALUE_906127f7 in ('.archive', '.json'):
        shutil.copyfile(str(spegle_rot/'build/pip-cache'/('micropython-bisect==3.3.3'+side_VALUE_906127f7)), str(Lagring_bane/('micropython-bisect==3.3.3'+side_VALUE_906127f7)))
    실물기록 = json.loads((Lagring_bane/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Namn, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = 시험휠(Namn, 파일들)
        (Lagring_bane/(Namn+'==1.0.archive')).write_bytes(data)
        (Lagring_bane/(Namn+'==1.0.json')).write_text(json.dumps({'name': Namn, 'version': '1.0',
            'filename': Namn.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    bekrefte = {'passed': False, 'kernel_sha256': hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    portnummer = tom_portnummer()
    Prosess = subprocess.Popen(['python3', str(spegle_rot/'Verktøy/Utfør_kommando.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(portnummer), '--pip-cache', str(Lagring_bane), '--ftp-port', str(tom_portnummer())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    veljar_a916db4e = selectors.DefaultSelector()
    veljar_a916db4e.register(Prosess.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(vise_VALUE_487749b8=b'jkoros-native> '):
        Innhald_VALUE = bytearray()
        끝 = time.monotonic()+120
        while vise_VALUE_487749b8 not in Innhald_VALUE:
            if time.monotonic() > 끝 or Prosess.poll() is not None:
                raise AssertionError('게스트 svare 없음: '+Innhald_VALUE.decode('utf-8','replace'))
            for oppføring_VALUE, _ in veljar_a916db4e.select(.1):
                조각 = oppføring_VALUE.fileobj.read(4096)
                Innhald_VALUE.extend(조각)
                대화기록.extend(조각)
        return Innhald_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def grensesnitt(Kommando, vise_VALUE_487749b8=b'jkoros-native> '):
        Prosess.stdin.write(Kommando.encode()+b'\n')
        Prosess.stdin.flush()
        return 기다리기(vise_VALUE_487749b8)
    def Utfør_kommando(Kommando, 예상, status_VALUE=0):
        Innhald_VALUE = grensesnitt(Kommando)
        assert 예상 in Innhald_VALUE and '\nexit '+str(status_VALUE)+'\n' in Innhald_VALUE, Innhald_VALUE
        bekrefte['checks'].append(Kommando)
        return Innhald_VALUE
    def Upload_Filer(Namn, data):
        grensesnitt('load '+Namn, b'hex> ')
        for plassere_INDEX in range(0, len(data), 64):
            grensesnitt(data[plassere_INDEX:plassere_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in grensesnitt('.')
    try:
        기다리기()
        Utfør_kommando('pip --help', 'MicroPython kjelde_tre 설치기')
        Upload_Filer('오류시험.py', (spegle_rot/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Utfør_kommando('python 오류시험.py', '한국어 Fil unntak stadfeste')
        Utfør_kommando('pip install micropython-bisect==3.3.3 --port '+str(portnummer), 'installere_VALUE 완료: micropython-bisect 3.3.3')
        Utfør_kommando('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Utfør_kommando('python -m pip list', 'micropython-bisect 3.3.3')
        Utfør_kommando('pip install micropython-bisect==3.3.3 --port '+str(portnummer), '이미 설치됨:')
        Utfør_kommando('pip install jkoros-fixture==1.0 --port '+str(portnummer), 'installere_VALUE 완료: jkoros-fixture')
        Utfør_kommando('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Utfør_kommando('pip install jkoros-syntax==1.0 --port '+str(portnummer), 'bunt FEIL:', 1)
        Utfør_kommando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 FEIL 보존")\'', '구문 FEIL 보존')
        Upload_Filer('공간시험.py', (spegle_rot/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Utfør_kommando('python 공간시험.py '+str(portnummer), 'bunt 공간 부족 levere_tilbake_bru stadfeste')
        Utfør_kommando('pip uninstall jkoros-fixture', 'fjerne_oppføring 완료: jkoros-fixture')
        Utfør_kommando('pip uninstall micropython-bisect', 'fjerne_oppføring 완료: micropython-bisect')
        Utfør_kommando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("fjerne_oppføring stadfeste")\'', 'fjerne_oppføring stadfeste')
        bekrefte['passed'] = True
        print('PASS: PyPI 실물 installere_VALUE·import·Utfør_kommando, 한국어 unntak, 패키지 katalog_VALUE, feil_VALUE levere_tilbake_bru, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Utgang_app 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Prosess.stdin.write(b'\x01x')
            Prosess.stdin.flush()
            Prosess.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Prosess.terminate()
            try:
                Prosess.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Prosess.kill()
                Prosess.wait()
        if Prosess.poll() is None:
            Prosess.kill()
            Prosess.wait()
        veljar_a916db4e.close()
        Prosess.stdin.close()
        Prosess.stdout.close()
        (forretningsmål_bane/'serial.log').write_bytes(대화기록)
        (forretningsmål_bane/'report.json').write_text(json.dumps(bekrefte, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Køyr_2()
