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
from kawe_tono import whakaatu_pūtake


def 시험휠(Ingoa, 파일들, kēhi_uara='Root-Is-Purelib: true\n', 의존성=''):
    raraunga = io.BytesIO()
    with zipfile.ZipFile(raraunga, 'w', zipfile.ZIP_DEFLATED) as pūpū:
        pūpū.writestr(Ingoa + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + kēhi_uara)
        pūpū.writestr(Ingoa + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Ingoa + '\nVersion: 1.0\n' + 의존성)
        for ara, Ihirangi_uara in 파일들.items():
            pūpū.writestr(ara, Ihirangi_uara)
    return raraunga.getvalue()


def taki_taurima():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'uara=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'uara=42\n'.encode()}
    for raraunga in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', raraunga, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ara·rahi·C toronga_uara·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def whakahaere():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    taki_taurima()
    if 인수.host_only:
        return
    mēhua_ara = whakaatu_pūtake/'build/verification/pip'
    mēhua_ara.mkdir(parents=True, exist_ok=True)
    Rokiroki_ara = mēhua_ara/'cache'
    Rokiroki_ara.mkdir(exist_ok=True)
    # tūturu_raraunga PyPI 배포 Kōnae. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(whakaatu_pūtake/'build/pip-cache').Whakarite('micropython-bisect==3.3.3')
    for whiore_uara in ('.archive', '.json'):
        shutil.copyfile(str(whakaatu_pūtake/'build/pip-cache'/('micropython-bisect==3.3.3'+whiore_uara)), str(Rokiroki_ara/('micropython-bisect==3.3.3'+whiore_uara)))
    실물기록 = json.loads((Rokiroki_ara/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Ingoa, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'uara=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        raraunga = 시험휠(Ingoa, 파일들)
        (Rokiroki_ara/(Ingoa+'==1.0.archive')).write_bytes(raraunga)
        (Rokiroki_ara/(Ingoa+'==1.0.json')).write_text(json.dumps({'name': Ingoa, 'version': '1.0',
            'filename': Ingoa.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(raraunga).hexdigest()}))
    whakamana = {'passed': False, 'kernel_sha256': hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Hātepe = subprocess.Popen(['python3', str(whakaatu_pūtake/'Ngā_Utauta/kawe_tono.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Rokiroki_ara), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    pūtīpako_a916db4e = selectors.DefaultSelector()
    pūtīpako_a916db4e.register(Hātepe.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(whakaatu_uara=b'jkoros-native> '):
        Ihirangi_uara = bytearray()
        끝 = time.monotonic()+120
        while whakaatu_uara not in Ihirangi_uara:
            if time.monotonic() > 끝 or Hātepe.poll() is not None:
                raise AssertionError('게스트 whakautu 없음: '+Ihirangi_uara.decode('utf-8','replace'))
            for tāurunga_uara, _ in pūtīpako_a916db4e.select(.1):
                조각 = tāurunga_uara.fileobj.read(4096)
                Ihirangi_uara.extend(조각)
                대화기록.extend(조각)
        return Ihirangi_uara.decode('utf-8', 'replace').replace('\r\n','\n')
    def anga(tono, whakaatu_uara=b'jkoros-native> '):
        Hātepe.stdin.write(tono.encode()+b'\n')
        Hātepe.stdin.flush()
        return 기다리기(whakaatu_uara)
    def kawe_tono(tono, 예상, tūnga_uara=0):
        Ihirangi_uara = anga(tono)
        assert 예상 in Ihirangi_uara and '\nexit '+str(tūnga_uara)+'\n' in Ihirangi_uara, Ihirangi_uara
        whakamana['checks'].append(tono)
        return Ihirangi_uara
    def tukuatu_Ngā_Kōnae(Ingoa, raraunga):
        anga('load '+Ingoa, b'hex> ')
        for tūranga_INDEX in range(0, len(raraunga), 64):
            anga(raraunga[tūranga_INDEX:tūranga_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in anga('.')
    try:
        기다리기()
        kawe_tono('pip --help', 'MicroPython pūtake_rākau 설치기')
        tukuatu_Ngā_Kōnae('오류시험.py', (whakaatu_pūtake/'시험/PYTHON/한국어오류시험.py').read_bytes())
        kawe_tono('python 오류시험.py', 'Reo_Māori Kōnae 예외 manatoko')
        kawe_tono('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'tāuta_uara 완료: micropython-bisect 3.3.3')
        kawe_tono('python -c \'from bisect import insort as 순서대로넣기; uara=[1,5]; 순서대로넣기(uara,3); print(uara)\'', '[1, 3, 5]')
        kawe_tono('python -m pip list', 'micropython-bisect 3.3.3')
        kawe_tono('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        kawe_tono('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'tāuta_uara 완료: jkoros-fixture')
        kawe_tono('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        kawe_tono('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'pūpū Pōhēhē:', 1)
        kawe_tono('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Pōhēhē 보존")\'', '구문 Pōhēhē 보존')
        tukuatu_Ngā_Kōnae('공간시험.py', (whakaatu_pūtake/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        kawe_tono('python 공간시험.py '+str(접속번호), 'pūpū 공간 부족 되돌림 manatoko')
        kawe_tono('pip uninstall jkoros-fixture', 'tango_tāurunga 완료: jkoros-fixture')
        kawe_tono('pip uninstall micropython-bisect', 'tango_tāurunga 완료: micropython-bisect')
        kawe_tono('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("tango_tāurunga manatoko")\'', 'tango_tāurunga manatoko')
        whakamana['passed'] = True
        print('PASS: PyPI 실물 tāuta_uara·import·kawe_tono, Reo_Māori 예외, 패키지 whaiaronga_uara, rahunga_uara 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Putaatu_kaupapa 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Hātepe.stdin.write(b'\x01x')
            Hātepe.stdin.flush()
            Hātepe.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Hātepe.terminate()
            try:
                Hātepe.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Hātepe.kill()
                Hātepe.wait()
        if Hātepe.poll() is None:
            Hātepe.kill()
            Hātepe.wait()
        pūtīpako_a916db4e.close()
        Hātepe.stdin.close()
        Hātepe.stdout.close()
        (mēhua_ara/'serial.log').write_bytes(대화기록)
        (mēhua_ara/'report.json').write_text(json.dumps(whakamana, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    whakahaere()
