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
from mee_nnyemiwu import 기준


def 시험휠(Aha, 파일들, ngō_valuu='Root-Is-Purelib: true\n', 의존성=''):
    datà = io.BytesIO()
    with zipfile.ZipFile(datà, 'w', zipfile.ZIP_DEFLATED) as ngwungwu:
        ngwungwu.writestr(Aha + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ngō_valuu)
        ngwungwu.writestr(Aha + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Aha + '\nVersion: 1.0\n' + 의존성)
        for ụzọ_ozi, ndịnà_valuu in 파일들.items():
            ngwungwu.writestr(ụzọ_ozi, ndịnà_valuu)
    return datà.getvalue()


def cheèk_usu():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'valuu=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'valuu=42\n'.encode()}
    for datà in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', datà, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ụzọ_ozi·Ụhara·C mgbatị_valuu·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Bido():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    cheèk_usu()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Nchekwa_ụzọ_ozi = 결과경로/'cache'
    Nchekwa_ụzọ_ozi.mkdir(exist_ok=True)
    # ǹdịnezie_datà PyPI 배포 Faịlụ. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').Kwado('micropython-bisect==3.3.3')
    for ngwụcha_valuu in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+ngwụcha_valuu)), str(Nchekwa_ụzọ_ozi/('micropython-bisect==3.3.3'+ngwụcha_valuu)))
    ngwaike_ndekọ = json.loads((Nchekwa_ụzọ_ozi/'micropython-bisect==3.3.3.json').read_text())
    assert ngwaike_ndekọ['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Aha, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'valuu=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        datà = 시험휠(Aha, 파일들)
        (Nchekwa_ụzọ_ozi/(Aha+'==1.0.archive')).write_bytes(datà)
        (Nchekwa_ụzọ_ozi/(Aha+'==1.0.json')).write_text(json.dumps({'name': Aha, 'version': '1.0',
            'filename': Aha.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(datà).hexdigest()}))
    mee_ịbanihe = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': ngwaike_ndekọ, 'checks': []}
    접속번호 = 빈접속번호()
    ùsòrò = subprocess.Popen(['python3', str(기준/'Ngwaọrụ/mee_nnyemiwu.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Nchekwa_ụzọ_ozi), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ihe_nhọpụta_a916db4e = selectors.DefaultSelector()
    ihe_nhọpụta_a916db4e.register(ùsòrò.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(gòsi_valuu=b'jkoros-native> '):
        ndịnà_valuu = bytearray()
        끝 = time.monotonic()+120
        while gòsi_valuu not in ndịnà_valuu:
            if time.monotonic() > 끝 or ùsòrò.poll() is not None:
                raise AssertionError('게스트 nzaghachi 없음: '+ndịnà_valuu.decode('utf-8','replace'))
            for ndebà_valuu, _ in ihe_nhọpụta_a916db4e.select(.1):
                조각 = ndebà_valuu.fileobj.read(4096)
                ndịnà_valuu.extend(조각)
                대화기록.extend(조각)
        return ndịnà_valuu.decode('utf-8', 'replace').replace('\r\n','\n')
    def nkọwannyemiwu(Ntiiwu, gòsi_valuu=b'jkoros-native> '):
        ùsòrò.stdin.write(Ntiiwu.encode()+b'\n')
        ùsòrò.stdin.flush()
        return 기다리기(gòsi_valuu)
    def mee_nnyemiwu(Ntiiwu, 예상, ọnọdụ_valuu=0):
        ndịnà_valuu = nkọwannyemiwu(Ntiiwu)
        assert 예상 in ndịnà_valuu and '\nexit '+str(ọnọdụ_valuu)+'\n' in ndịnà_valuu, ndịnà_valuu
        mee_ịbanihe['checks'].append(Ntiiwu)
        return ndịnà_valuu
    def bùlie_Ndi_ọbọakwụkwọ(Aha, datà):
        nkọwannyemiwu('load '+Aha, b'hex> ')
        for 자리 in range(0, len(datà), 64):
            nkọwannyemiwu(datà[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in nkọwannyemiwu('.')
    try:
        기다리기()
        mee_nnyemiwu('pip --help', 'MicroPython ebensìbịa_èsèrèsè_osisi 설치기')
        bùlie_Ndi_ọbọakwụkwọ('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        mee_nnyemiwu('python 오류시험.py', '한국어 Faịlụ 예외 nkwàdo_eziokwū')
        mee_nnyemiwu('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'wùbe_valuu 완료: micropython-bisect 3.3.3')
        mee_nnyemiwu('python -c \'from bisect import insort as 순서대로넣기; valuu=[1,5]; 순서대로넣기(valuu,3); print(valuu)\'', '[1, 3, 5]')
        mee_nnyemiwu('python -m pip list', 'micropython-bisect 3.3.3')
        mee_nnyemiwu('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        mee_nnyemiwu('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'wùbe_valuu 완료: jkoros-fixture')
        mee_nnyemiwu('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        mee_nnyemiwu('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'ngwungwu mmejọ:', 1)
        mee_nnyemiwu('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 mmejọ 보존")\'', '구문 mmejọ 보존')
        bùlie_Ndi_ọbọakwụkwọ('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        mee_nnyemiwu('python 공간시험.py '+str(접속번호), 'ngwungwu 공간 부족 되돌림 nkwàdo_eziokwū')
        mee_nnyemiwu('pip uninstall jkoros-fixture', 'wepụ_ndebà 완료: jkoros-fixture')
        mee_nnyemiwu('pip uninstall micropython-bisect', 'wepụ_ndebà 완료: micropython-bisect')
        mee_nnyemiwu('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("wepụ_ndebà nkwàdo_eziokwū")\'', 'wepụ_ndebà nkwàdo_eziokwū')
        mee_ịbanihe['passed'] = True
        print('PASS: PyPI 실물 wùbe_valuu·import·mee_nnyemiwu, 한국어 예외, 패키지 dàịrektrị_valuu, ọdịdà_valuu 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 pụọ_app 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            ùsòrò.stdin.write(b'\x01x')
            ùsòrò.stdin.flush()
            ùsòrò.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            ùsòrò.terminate()
            try:
                ùsòrò.wait(timeout=8)
            except subprocess.TimeoutExpired:
                ùsòrò.kill()
                ùsòrò.wait()
        if ùsòrò.poll() is None:
            ùsòrò.kill()
            ùsòrò.wait()
        ihe_nhọpụta_a916db4e.close()
        ùsòrò.stdin.close()
        ùsòrò.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(mee_ịbanihe, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Bido()
