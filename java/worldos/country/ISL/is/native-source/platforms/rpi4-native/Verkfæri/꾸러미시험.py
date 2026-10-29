#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 eigin 커널에서 검사한다."""
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
from 꾸러미중계 import búnt_gagnageymsla, 압축풀기
from keyra_skipun import verk_rót


def 시험휠(Heiti, 파일들, samningsvirði='Root-Is-Purelib: true\n', 의존성=''):
    gögn = io.BytesIO()
    with zipfile.ZipFile(gögn, 'w', zipfile.ZIP_DEFLATED) as búnt:
        búnt.writestr(Heiti + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + samningsvirði)
        búnt.writestr(Heiti + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Heiti + '\nVersion: 1.0\n' + 의존성)
        for SLÓÐ, Efni_VALUE in 파일들.items():
            búnt.writestr(SLÓÐ, Efni_VALUE)
    return gögn.getvalue()


def athuga_hýsa():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for gögn in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', gögn, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel SLÓÐ·Stærð·C viðbót_VALUE·의존성 hafna_VALUE')


def autt_tengisnúmer():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Keyra_2():
    þáttari_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    þáttari_48ee4b1b.add_argument('--host-only', action='store_true')
    Viðföng = þáttari_48ee4b1b.parse_args()
    athuga_hýsa()
    if Viðföng.host_only:
        return
    mæld_stærð_slóð = verk_rót/'build/verification/pip'
    mæld_stærð_slóð.mkdir(parents=True, exist_ok=True)
    geymsla_slóð_02e62bb7 = mæld_stærð_slóð/'cache'
    geymsla_slóð_02e62bb7.mkdir(exist_ok=True)
    # raun_gögn PyPI dreifing_VALUE Skrá. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    búnt_gagnageymsla(verk_rót/'build/pip-cache').Undirbúa('micropython-bisect==3.3.3')
    for hali_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(verk_rót/'build/pip-cache'/('micropython-bisect==3.3.3'+hali_VALUE)), str(geymsla_slóð_02e62bb7/('micropython-bisect==3.3.3'+hali_VALUE)))
    실물기록 = json.loads((geymsla_slóð_02e62bb7/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Heiti, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % númer: 'VALUE=1\n' for númer in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        gögn = 시험휠(Heiti, 파일들)
        (geymsla_slóð_02e62bb7/(Heiti+'==1.0.archive')).write_bytes(gögn)
        (geymsla_slóð_02e62bb7/(Heiti+'==1.0.json')).write_text(json.dumps({'name': Heiti, 'version': '1.0',
            'filename': Heiti.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(gögn).hexdigest()}))
    staðfesta = {'passed': False, 'kernel_sha256': hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    tengisnúmer = autt_tengisnúmer()
    Ferli = subprocess.Popen(['python3', str(verk_rót/'Verkfæri/keyra_skipun.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(tengisnúmer), '--pip-cache', str(geymsla_slóð_02e62bb7), '--ftp-port', str(autt_tengisnúmer())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    val_a916db4e = selectors.DefaultSelector()
    val_a916db4e.register(Ferli.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(sýna_VALUE=b'jkoros-native> '):
        Efni_VALUE = bytearray()
        끝 = time.monotonic()+120
        while sýna_VALUE not in Efni_VALUE:
            if time.monotonic() > 끝 or Ferli.poll() is not None:
                raise AssertionError('게스트 svara 없음: '+Efni_VALUE.decode('utf-8','replace'))
            for færsla_VALUE, _ in val_a916db4e.select(.1):
                조각 = færsla_VALUE.fileobj.read(4096)
                Efni_VALUE.extend(조각)
                대화기록.extend(조각)
        return Efni_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def skel(Skipun, sýna_VALUE=b'jkoros-native> '):
        Ferli.stdin.write(Skipun.encode()+b'\n')
        Ferli.stdin.flush()
        return 기다리기(sýna_VALUE)
    def keyra_skipun(Skipun, 예상, staða_VALUE_e10195a1=0):
        Efni_VALUE = skel(Skipun)
        assert 예상 in Efni_VALUE and '\nexit '+str(staða_VALUE_e10195a1)+'\n' in Efni_VALUE, Efni_VALUE
        staðfesta['checks'].append(Skipun)
        return Efni_VALUE
    def hlaða_upp_Skrár(Heiti, gögn):
        skel('load '+Heiti, b'hex> ')
        for staða_INDEX in range(0, len(gögn), 64):
            skel(gögn[staða_INDEX:staða_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in skel('.')
    try:
        기다리기()
        keyra_skipun('pip --help', 'MicroPython uppruni_tré 설치기')
        hlaða_upp_Skrár('오류시험.py', (verk_rót/'시험/PYTHON/한국어오류시험.py').read_bytes())
        keyra_skipun('python 오류시험.py', 'Íslenska Skrá undantekning sannprófa')
        keyra_skipun('pip install micropython-bisect==3.3.3 --port '+str(tengisnúmer), 'setja_upp_VALUE 완료: micropython-bisect 3.3.3')
        keyra_skipun('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        keyra_skipun('python -m pip list', 'micropython-bisect 3.3.3')
        keyra_skipun('pip install micropython-bisect==3.3.3 --port '+str(tengisnúmer), '이미 설치됨:')
        keyra_skipun('pip install jkoros-fixture==1.0 --port '+str(tengisnúmer), 'setja_upp_VALUE 완료: jkoros-fixture')
        keyra_skipun('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        keyra_skipun('pip install jkoros-syntax==1.0 --port '+str(tengisnúmer), 'búnt Villa:', 1)
        keyra_skipun('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Villa 보존")\'', '구문 Villa 보존')
        hlaða_upp_Skrár('공간시험.py', (verk_rót/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        keyra_skipun('python 공간시험.py '+str(tengisnúmer), 'búnt 공간 부족 skila_brú sannprófa')
        keyra_skipun('pip uninstall jkoros-fixture', 'fjarlægja_færsla 완료: jkoros-fixture')
        keyra_skipun('pip uninstall micropython-bisect', 'fjarlægja_færsla 완료: micropython-bisect')
        keyra_skipun('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("fjarlægja_færsla sannprófa")\'', 'fjarlægja_færsla sannprófa')
        staðfesta['passed'] = True
        print('PASS: PyPI 실물 setja_upp_VALUE·import·keyra_skipun, Íslenska undantekning, 패키지 skráasafn_VALUE, bilun_VALUE skila_brú, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 loka_forrit 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Ferli.stdin.write(b'\x01x')
            Ferli.stdin.flush()
            Ferli.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Ferli.terminate()
            try:
                Ferli.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Ferli.kill()
                Ferli.wait()
        if Ferli.poll() is None:
            Ferli.kill()
            Ferli.wait()
        val_a916db4e.close()
        Ferli.stdin.close()
        Ferli.stdout.close()
        (mæld_stærð_slóð/'serial.log').write_bytes(대화기록)
        (mæld_stærð_slóð/'report.json').write_text(json.dumps(staðfesta, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Keyra_2()
