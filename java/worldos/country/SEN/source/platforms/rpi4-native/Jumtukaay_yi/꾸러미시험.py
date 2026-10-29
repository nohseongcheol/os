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
from def_ndigel import 기준


def 시험휠(tur_253d1510, 파일들, ay_xëyma='Root-Is-Purelib: true\n', 의존성=''):
    mbir = io.BytesIO()
    with zipfile.ZipFile(mbir, 'w', zipfile.ZIP_DEFLATED) as takku_xéewël:
        takku_xéewël.writestr(tur_253d1510 + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ay_xëyma)
        takku_xéewël.writestr(tur_253d1510 + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + tur_253d1510 + '\nVersion: 1.0\n' + 의존성)
        for Yoonu_jëmale, Këmb_xëyma in 파일들.items():
            takku_xéewël.writestr(Yoonu_jëmale, Këmb_xëyma)
    return mbir.getvalue()


def sek_dalal():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'xëyma=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'xëyma=42\n'.encode()}
    for mbir in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', mbir, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Yoonu_jëmale·tolluwaay·C ñàmbaas_xëyma·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def daw():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    sek_dalal()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Dencukaay_Yoonu_jëmale = 결과경로/'cache'
    Dencukaay_Yoonu_jëmale.mkdir(exist_ok=True)
    # liteew_mbir PyPI 배포 bara_denc. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').jël_matuwaay('micropython-bisect==3.3.3')
    for asaka_ji_xëyma in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+asaka_ji_xëyma)), str(Dencukaay_Yoonu_jëmale/('micropython-bisect==3.3.3'+asaka_ji_xëyma)))
    jumtukaay_làq = json.loads((Dencukaay_Yoonu_jëmale/'micropython-bisect==3.3.3.json').read_text())
    assert jumtukaay_làq['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for tur_253d1510, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'xëyma=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        mbir = 시험휠(tur_253d1510, 파일들)
        (Dencukaay_Yoonu_jëmale/(tur_253d1510+'==1.0.archive')).write_bytes(mbir)
        (Dencukaay_Yoonu_jëmale/(tur_253d1510+'==1.0.json')).write_text(json.dumps({'name': tur_253d1510, 'version': '1.0',
            'filename': tur_253d1510.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(mbir).hexdigest()}))
    wéral = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': jumtukaay_làq, 'checks': []}
    접속번호 = 빈접속번호()
    yokkute = subprocess.Popen(['python3', str(기준/'Jumtukaay_yi/def_ndigel.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Dencukaay_Yoonu_jëmale), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tànnkat_a916db4e = selectors.DefaultSelector()
    tànnkat_a916db4e.register(yokkute.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(féeñal_xëyma=b'jkoros-native> '):
        Këmb_xëyma = bytearray()
        끝 = time.monotonic()+120
        while féeñal_xëyma not in Këmb_xëyma:
            if time.monotonic() > 끝 or yokkute.poll() is not None:
                raise AssertionError('게스트 tontu 없음: '+Këmb_xëyma.decode('utf-8','replace'))
            for dugal_xabaar_xëyma, _ in tànnkat_a916db4e.select(.1):
                조각 = dugal_xabaar_xëyma.fileobj.read(4096)
                Këmb_xëyma.extend(조각)
                대화기록.extend(조각)
        return Këmb_xëyma.decode('utf-8', 'replace').replace('\r\n','\n')
    def Wëreef(ndigel, féeñal_xëyma=b'jkoros-native> '):
        yokkute.stdin.write(ndigel.encode()+b'\n')
        yokkute.stdin.flush()
        return 기다리기(féeñal_xëyma)
    def def_ndigel(ndigel, 예상, nekkin_xëyma=0):
        Këmb_xëyma = Wëreef(ndigel)
        assert 예상 in Këmb_xëyma and '\nexit '+str(nekkin_xëyma)+'\n' in Këmb_xëyma, Këmb_xëyma
        wéral['checks'].append(ndigel)
        return Këmb_xëyma
    def toxalsi_Fisiye_yi(tur_253d1510, mbir):
        Wëreef('load '+tur_253d1510, b'hex> ')
        for 자리 in range(0, len(mbir), 64):
            Wëreef(mbir[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in Wëreef('.')
    try:
        기다리기()
        def_ndigel('pip --help', 'MicroPython Cosaan_tëralinuy_pàcc 설치기')
        toxalsi_Fisiye_yi('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        def_ndigel('python 오류시험.py', '한국어 bara_denc 예외 luñutu')
        def_ndigel('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'samp_xëyma 완료: micropython-bisect 3.3.3')
        def_ndigel('python -c \'from bisect import insort as 순서대로넣기; xëyma=[1,5]; 순서대로넣기(xëyma,3); print(xëyma)\'', '[1, 3, 5]')
        def_ndigel('python -m pip list', 'micropython-bisect 3.3.3')
        def_ndigel('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        def_ndigel('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'samp_xëyma 완료: jkoros-fixture')
        def_ndigel('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        def_ndigel('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'takku_xéewël njumte:', 1)
        def_ndigel('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 njumte 보존")\'', '구문 njumte 보존')
        toxalsi_Fisiye_yi('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        def_ndigel('python 공간시험.py '+str(접속번호), 'takku_xéewël 공간 부족 되돌림 luñutu')
        def_ndigel('pip uninstall jkoros-fixture', 'dandal_dugal_xabaar 완료: jkoros-fixture')
        def_ndigel('pip uninstall micropython-bisect', 'dandal_dugal_xabaar 완료: micropython-bisect')
        def_ndigel('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("dandal_dugal_xabaar luñutu")\'', 'dandal_dugal_xabaar luñutu')
        wéral['passed'] = True
        print('PASS: PyPI 실물 samp_xëyma·import·def_ndigel, 한국어 예외, 패키지 dàmb_xëyma, foo_xëyma 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Génn_jëfekaay 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            yokkute.stdin.write(b'\x01x')
            yokkute.stdin.flush()
            yokkute.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            yokkute.terminate()
            try:
                yokkute.wait(timeout=8)
            except subprocess.TimeoutExpired:
                yokkute.kill()
                yokkute.wait()
        if yokkute.poll() is None:
            yokkute.kill()
            yokkute.wait()
        tànnkat_a916db4e.close()
        yokkute.stdin.close()
        yokkute.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(wéral, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    daw()
