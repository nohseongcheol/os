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
from ýerine_ýetir_buýruk import 기준


def 시험휠(Ad, 파일들, ýumuş_baha_102996da='Root-Is-Purelib: true\n', 의존성=''):
    maglumat = io.BytesIO()
    with zipfile.ZipFile(maglumat, 'w', zipfile.ZIP_DEFLATED) as toplum:
        toplum.writestr(Ad + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ýumuş_baha_102996da)
        toplum.writestr(Ad + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Ad + '\nVersion: 1.0\n' + 의존성)
        for Ýol, Mazmun_baha in 파일들.items():
            toplum.writestr(Ýol, Mazmun_baha)
    return maglumat.getvalue()


def derňe_esasy():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'baha=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'baha=42\n'.encode()}
    for maglumat in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', maglumat, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Ýol·Ululyk·C giňelme_baha·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Bitir():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    derňe_esasy()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Ammar_ýol = 결과경로/'cache'
    Ammar_ýol.mkdir(exist_ok=True)
    # hakyky_maglumat PyPI 배포 Faýl. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').Taýýarla('micropython-bisect==3.3.3')
    for guýruk_baha in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+guýruk_baha)), str(Ammar_ýol/('micropython-bisect==3.3.3'+guýruk_baha)))
    실물기록 = json.loads((Ammar_ýol/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Ad, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'baha=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        maglumat = 시험휠(Ad, 파일들)
        (Ammar_ýol/(Ad+'==1.0.archive')).write_bytes(maglumat)
        (Ammar_ýol/(Ad+'==1.0.json')).write_text(json.dumps({'name': Ad, 'version': '1.0',
            'filename': Ad.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(maglumat).hexdigest()}))
    tassykla = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Proses = subprocess.Popen(['python3', str(기준/'Gurallar/ýerine_ýetir_buýruk.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Ammar_ýol), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    saýlaýjy_a916db4e = selectors.DefaultSelector()
    saýlaýjy_a916db4e.register(Proses.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(görkez_baha_487749b8=b'jkoros-native> '):
        Mazmun_baha = bytearray()
        끝 = time.monotonic()+120
        while görkez_baha_487749b8 not in Mazmun_baha:
            if time.monotonic() > 끝 or Proses.poll() is not None:
                raise AssertionError('게스트 jogap_bermek 없음: '+Mazmun_baha.decode('utf-8','replace'))
            for girizmeklik_baha, _ in saýlaýjy_a916db4e.select(.1):
                조각 = girizmeklik_baha.fileobj.read(4096)
                Mazmun_baha.extend(조각)
                대화기록.extend(조각)
        return Mazmun_baha.decode('utf-8', 'replace').replace('\r\n','\n')
    def gabyjak(buýruk, görkez_baha_487749b8=b'jkoros-native> '):
        Proses.stdin.write(buýruk.encode()+b'\n')
        Proses.stdin.flush()
        return 기다리기(görkez_baha_487749b8)
    def ýerine_ýetir_buýruk(buýruk, 예상, ýagdaý_baha=0):
        Mazmun_baha = gabyjak(buýruk)
        assert 예상 in Mazmun_baha and '\nexit '+str(ýagdaý_baha)+'\n' in Mazmun_baha, Mazmun_baha
        tassykla['checks'].append(buýruk)
        return Mazmun_baha
    def ýükle_Faýllar(Ad, maglumat):
        gabyjak('load '+Ad, b'hex> ')
        for 자리 in range(0, len(maglumat), 64):
            gabyjak(maglumat[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in gabyjak('.')
    try:
        기다리기()
        ýerine_ýetir_buýruk('pip --help', 'MicroPython gor_agaç 설치기')
        ýükle_Faýllar('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        ýerine_ýetir_buýruk('python 오류시험.py', '한국어 Faýl 예외 barla')
        ýerine_ýetir_buýruk('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'gurna_baha 완료: micropython-bisect 3.3.3')
        ýerine_ýetir_buýruk('python -c \'from bisect import insort as 순서대로넣기; baha=[1,5]; 순서대로넣기(baha,3); print(baha)\'', '[1, 3, 5]')
        ýerine_ýetir_buýruk('python -m pip list', 'micropython-bisect 3.3.3')
        ýerine_ýetir_buýruk('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        ýerine_ýetir_buýruk('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'gurna_baha 완료: jkoros-fixture')
        ýerine_ýetir_buýruk('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ýerine_ýetir_buýruk('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'toplum Hata:', 1)
        ýerine_ýetir_buýruk('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Hata 보존")\'', '구문 Hata 보존')
        ýükle_Faýllar('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ýerine_ýetir_buýruk('python 공간시험.py '+str(접속번호), 'toplum 공간 부족 되돌림 barla')
        ýerine_ýetir_buýruk('pip uninstall jkoros-fixture', 'aýyr_girizmeklik 완료: jkoros-fixture')
        ýerine_ýetir_buýruk('pip uninstall micropython-bisect', 'aýyr_girizmeklik 완료: micropython-bisect')
        ýerine_ýetir_buýruk('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("aýyr_girizmeklik barla")\'', 'aýyr_girizmeklik barla')
        tassykla['passed'] = True
        print('PASS: PyPI 실물 gurna_baha·import·ýerine_ýetir_buýruk, 한국어 예외, 패키지 katalog_baha, näsazlyk_baha 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 çyk_programma 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
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
        saýlaýjy_a916db4e.close()
        Proses.stdin.close()
        Proses.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(tassykla, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Bitir()
