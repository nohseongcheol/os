#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 bevitel_ÉRTÉK·RAM 되돌림을 saját 커널에서 검사한다."""
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
from 꾸러미중계 import köteg_adattár, kicsomagol
from végrehajt_parancs import teendő_gyök


def teszt_tárcsa(Név, 파일들, szerződés_értéke='Root-Is-Purelib: true\n', 의존성=''):
    adat = io.BytesIO()
    with zipfile.ZipFile(adat, 'w', zipfile.ZIP_DEFLATED) as köteg:
        köteg.writestr(Név + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + szerződés_értéke)
        köteg.writestr(Név + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Név + '\nVersion: 1.0\n' + 의존성)
        for ÚTVONAL, Tartalom_ÉRTÉK in 파일들.items():
            köteg.writestr(ÚTVONAL, Tartalom_ÉRTÉK)
    return adat.getvalue()


def csekk_gazda():
    informatikai_részleg_normál = teszt_tárcsa('jkoros-fixture', {'mod.py': 'ÉRTÉK=42\n'})
    assert kicsomagol('jkoros_fixture-1.0-py3-none-any.whl', informatikai_részleg_normál, 'jkoros-fixture', '1.0') == {'mod.py': 'ÉRTÉK=42\n'.encode()}
    for adat in (
            teszt_tárcsa('jkoros-fixture', {'../escape.py': ''}),
            teszt_tárcsa('jkoros-fixture', {'/abs.py': ''}),
            teszt_tárcsa('jkoros-fixture', {'big.py': 'x' * 16385}),
            teszt_tárcsa('jkoros-fixture', {'mod.so': ''}),
            teszt_tárcsa('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            teszt_tárcsa('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            kicsomagol('jkoros_fixture-1.0-py3-none-any.whl', adat, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ÚTVONAL·Méret·C bővítmény_ÉRTÉK·의존성 elutasít_ÉRTÉK')


def üres_portszám():
    with socket.socket() as szoftvercsatorna_ÉRTÉK:
        szoftvercsatorna_ÉRTÉK.bind(('127.0.0.1', 0))
        return szoftvercsatorna_ÉRTÉK.getsockname()[1]


def Futtatás():
    elemző_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    elemző_48ee4b1b.add_argument('--host-only', action='store_true')
    Argumentumok = elemző_48ee4b1b.parse_args()
    csekk_gazda()
    if Argumentumok.host_only:
        return
    KR_útvonal = teendő_gyök/'build/verification/pip'
    KR_útvonal.mkdir(parents=True, exist_ok=True)
    tár_útvonal = KR_útvonal/'cache'
    tár_útvonal.mkdir(exist_ok=True)
    # tényleges_adat PyPI elosztás_ÉRTÉK Fájl. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    köteg_adattár(teendő_gyök/'build/pip-cache').Előkészítés('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(teendő_gyök/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(tár_útvonal/('micropython-bisect==3.3.3'+꼬리)))
    hardver_LOG = json.loads((tár_útvonal/'micropython-bisect==3.3.3.json').read_text())
    assert hardver_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Név, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,MPERC_operandus):\n return 가+MPERC_operandus\n'}),
            ('jkoros-space', {'space%d.py' % szám: 'ÉRTÉK=1\n' for szám in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        adat = teszt_tárcsa(Név, 파일들)
        (tár_útvonal/(Név+'==1.0.archive')).write_bytes(adat)
        (tár_útvonal/(Név+'==1.0.json')).write_text(json.dumps({'name': Név, 'version': '1.0',
            'filename': Név.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(adat).hexdigest()}))
    ellenőriz = {'passed': False, 'kernel_sha256': hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': hardver_LOG, 'checks': []}
    portszám = üres_portszám()
    Folyamat = subprocess.Popen(['python3', str(teendő_gyök/'Eszközök/végrehajt_parancs.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(portszám), '--pip-cache', str(tár_útvonal), '--ftp-port', str(üres_portszám())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    szelektor_a916db4e = selectors.DefaultSelector()
    szelektor_a916db4e.register(Folyamat.stdout, selectors.EVENT_READ)
    átirat = bytearray()
    def 기다리기(bemutató_ÉRTÉK=b'jkoros-native> '):
        Tartalom_ÉRTÉK = bytearray()
        끝 = time.monotonic()+120
        while bemutató_ÉRTÉK not in Tartalom_ÉRTÉK:
            if time.monotonic() > 끝 or Folyamat.poll() is not None:
                raise AssertionError('게스트 válasz 없음: '+Tartalom_ÉRTÉK.decode('utf-8','replace'))
            for bejegyzés_ÉRTÉK, _ in szelektor_a916db4e.select(.1):
                조각 = bejegyzés_ÉRTÉK.fileobj.read(4096)
                Tartalom_ÉRTÉK.extend(조각)
                átirat.extend(조각)
        return Tartalom_ÉRTÉK.decode('utf-8', 'replace').replace('\r\n','\n')
    def felület(Parancs, bemutató_ÉRTÉK=b'jkoros-native> '):
        Folyamat.stdin.write(Parancs.encode()+b'\n')
        Folyamat.stdin.flush()
        return 기다리기(bemutató_ÉRTÉK)
    def végrehajt_parancs(Parancs, 예상, Állapot_ÉRTÉK=0):
        Tartalom_ÉRTÉK = felület(Parancs)
        assert 예상 in Tartalom_ÉRTÉK and '\nexit '+str(Állapot_ÉRTÉK)+'\n' in Tartalom_ÉRTÉK, Tartalom_ÉRTÉK
        ellenőriz['checks'].append(Parancs)
        return Tartalom_ÉRTÉK
    def feltölt_Files(Név, adat):
        felület('load '+Név, b'hex> ')
        for helyzetindex in range(0, len(adat), 64):
            felület(adat[helyzetindex:helyzetindex+64].hex(), b'hex> ')
        assert 'LOADED' in felület('.')
    try:
        기다리기()
        végrehajt_parancs('pip --help', 'MicroPython forrás_fa 설치기')
        feltölt_Files('오류시험.py', (teendő_gyök/'시험/PYTHON/한국어오류시험.py').read_bytes())
        végrehajt_parancs('python 오류시험.py', 'magyar Fájl kivétel igazol')
        végrehajt_parancs('pip install micropython-bisect==3.3.3 --port '+str(portszám), 'telepít_ÉRTÉK 완료: micropython-bisect 3.3.3')
        végrehajt_parancs('python -c \'from bisect import insort as 순서대로넣기; ÉRTÉK=[1,5]; 순서대로넣기(ÉRTÉK,3); print(ÉRTÉK)\'', '[1, 3, 5]')
        végrehajt_parancs('python -m pip list', 'micropython-bisect 3.3.3')
        végrehajt_parancs('pip install micropython-bisect==3.3.3 --port '+str(portszám), '이미 설치됨:')
        végrehajt_parancs('pip install jkoros-fixture==1.0 --port '+str(portszám), 'telepít_ÉRTÉK 완료: jkoros-fixture')
        végrehajt_parancs('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        végrehajt_parancs('pip install jkoros-syntax==1.0 --port '+str(portszám), 'köteg HIBA:', 1)
        végrehajt_parancs('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 HIBA 보존")\'', '구문 HIBA 보존')
        feltölt_Files('공간시험.py', (teendő_gyök/'시험/PYTHON/köteg_névtér_teszt.py').read_bytes())
        végrehajt_parancs('python 공간시험.py '+str(portszám), 'köteg CÍM_régió 부족 visszaküld_híd igazol')
        végrehajt_parancs('pip uninstall jkoros-fixture', 'eltávolít_bejegyzés 완료: jkoros-fixture')
        végrehajt_parancs('pip uninstall micropython-bisect', 'eltávolít_bejegyzés 완료: micropython-bisect')
        végrehajt_parancs('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("eltávolít_bejegyzés igazol")\'', 'eltávolít_bejegyzés igazol')
        ellenőriz['passed'] = True
        print('PASS: PyPI 실물 telepít_ÉRTÉK·import·végrehajt_parancs, magyar kivétel, 패키지 címtár_ÉRTÉK, hiba_ÉRTÉK visszaküld_híd, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 kilép_app 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Folyamat.stdin.write(b'\x01x')
            Folyamat.stdin.flush()
            Folyamat.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Folyamat.terminate()
            try:
                Folyamat.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Folyamat.kill()
                Folyamat.wait()
        if Folyamat.poll() is None:
            Folyamat.kill()
            Folyamat.wait()
        szelektor_a916db4e.close()
        Folyamat.stdin.close()
        Folyamat.stdout.close()
        (KR_útvonal/'serial.log').write_bytes(átirat)
        (KR_útvonal/'report.json').write_text(json.dumps(ellenőriz, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Futtatás()
