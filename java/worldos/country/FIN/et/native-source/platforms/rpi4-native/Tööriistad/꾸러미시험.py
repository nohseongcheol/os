#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 oma 커널에서 검사한다."""
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
from 꾸러미중계 import kogum_hoidla, lahti_pakkima
from Täida_käsk import Project_juur


def 시험휠(Nimi_2, 파일들, lepingu_väärtus='Root-Is-Purelib: true\n', 의존성=''):
    andmed = io.BytesIO()
    with zipfile.ZipFile(andmed, 'w', zipfile.ZIP_DEFLATED) as kogum:
        kogum.writestr(Nimi_2 + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + lepingu_väärtus)
        kogum.writestr(Nimi_2 + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nimi_2 + '\nVersion: 1.0\n' + 의존성)
        for RADA, Sisu_VALUE in 파일들.items():
            kogum.writestr(RADA, Sisu_VALUE)
    return andmed.getvalue()


def tšekk_host():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert lahti_pakkima('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for andmed in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            lahti_pakkima('jkoros_fixture-1.0-py3-none-any.whl', andmed, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel RADA·Suurus·C laiendus_VALUE·의존성 keelduma_VALUE')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Käivita_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--host-only', action='store_true')
    Argumendid = parser_48ee4b1b.parse_args()
    tšekk_host()
    if Argumendid.host_only:
        return
    näitaja_tee = Project_juur/'build/verification/pip'
    näitaja_tee.mkdir(parents=True, exist_ok=True)
    salvesti_tee = näitaja_tee/'cache'
    salvesti_tee.mkdir(exist_ok=True)
    # tegelik_andmed PyPI turustus_VALUE Fail. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    kogum_hoidla(Project_juur/'build/pip-cache').Ettevalmistamine('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(Project_juur/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(salvesti_tee/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((salvesti_tee/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nimi_2, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SECOND_operand):\n return 가+SECOND_operand\n'}),
            ('jkoros-space', {'space%d.py' % number: 'VALUE=1\n' for number in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        andmed = 시험휠(Nimi_2, 파일들)
        (salvesti_tee/(Nimi_2+'==1.0.archive')).write_bytes(andmed)
        (salvesti_tee/(Nimi_2+'==1.0.json')).write_text(json.dumps({'name': Nimi_2, 'version': '1.0',
            'filename': Nimi_2.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(andmed).hexdigest()}))
    valideerima = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    pordinumber = 빈접속번호()
    Protsess = subprocess.Popen(['python3', str(Project_juur/'Tööriistad/Täida_käsk.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(pordinumber), '--pip-cache', str(salvesti_tee), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    valija_a916db4e = selectors.DefaultSelector()
    valija_a916db4e.register(Protsess.stdout, selectors.EVENT_READ)
    transkriptsioon = bytearray()
    def 기다리기(saade_VALUE=b'jkoros-native> '):
        Sisu_VALUE = bytearray()
        끝 = time.monotonic()+120
        while saade_VALUE not in Sisu_VALUE:
            if time.monotonic() > 끝 or Protsess.poll() is not None:
                raise AssertionError('게스트 vastus 없음: '+Sisu_VALUE.decode('utf-8','replace'))
            for kirje_VALUE, _ in valija_a916db4e.select(.1):
                조각 = kirje_VALUE.fileobj.read(4096)
                Sisu_VALUE.extend(조각)
                transkriptsioon.extend(조각)
        return Sisu_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def kest(Käsk, saade_VALUE=b'jkoros-native> '):
        Protsess.stdin.write(Käsk.encode()+b'\n')
        Protsess.stdin.flush()
        return 기다리기(saade_VALUE)
    def Täida_käsk(Käsk, 예상, Olek_VALUE=0):
        Sisu_VALUE = kest(Käsk)
        assert 예상 in Sisu_VALUE and '\nexit '+str(Olek_VALUE)+'\n' in Sisu_VALUE, Sisu_VALUE
        valideerima['checks'].append(Käsk)
        return Sisu_VALUE
    def Upload_Failid(Nimi_2, andmed):
        kest('load '+Nimi_2, b'hex> ')
        for asukohaindeks in range(0, len(andmed), 64):
            kest(andmed[asukohaindeks:asukohaindeks+64].hex(), b'hex> ')
        assert 'LOADED' in kest('.')
    try:
        기다리기()
        Täida_käsk('pip --help', 'MicroPython lähe_puu 설치기')
        Upload_Failid('오류시험.py', (Project_juur/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Täida_käsk('python 오류시험.py', 'Eesti Fail erand kinnitama')
        Täida_käsk('pip install micropython-bisect==3.3.3 --port '+str(pordinumber), 'installima_VALUE 완료: micropython-bisect 3.3.3')
        Täida_käsk('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Täida_käsk('python -m pip list', 'micropython-bisect 3.3.3')
        Täida_käsk('pip install micropython-bisect==3.3.3 --port '+str(pordinumber), '이미 설치됨:')
        Täida_käsk('pip install jkoros-fixture==1.0 --port '+str(pordinumber), 'installima_VALUE 완료: jkoros-fixture')
        Täida_käsk('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Täida_käsk('pip install jkoros-syntax==1.0 --port '+str(pordinumber), 'kogum VIGA:', 1)
        Täida_käsk('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 VIGA 보존")\'', '구문 VIGA 보존')
        Upload_Failid('공간시험.py', (Project_juur/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Täida_käsk('python 공간시험.py '+str(pordinumber), 'kogum ADDRESS_regioon 부족 tagasi_saatma_sild kinnitama')
        Täida_käsk('pip uninstall jkoros-fixture', 'eemaldama_kirje 완료: jkoros-fixture')
        Täida_käsk('pip uninstall micropython-bisect', 'eemaldama_kirje 완료: micropython-bisect')
        Täida_käsk('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("eemaldama_kirje kinnitama")\'', 'eemaldama_kirje kinnitama')
        valideerima['passed'] = True
        print('PASS: PyPI 실물 installima_VALUE·import·Täida_käsk, Eesti erand, 패키지 kaust_VALUE, tõrge_VALUE tagasi_saatma_sild, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Välju_programm 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Protsess.stdin.write(b'\x01x')
            Protsess.stdin.flush()
            Protsess.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Protsess.terminate()
            try:
                Protsess.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Protsess.kill()
                Protsess.wait()
        if Protsess.poll() is None:
            Protsess.kill()
            Protsess.wait()
        valija_a916db4e.close()
        Protsess.stdin.close()
        Protsess.stdout.close()
        (näitaja_tee/'serial.log').write_bytes(transkriptsioon)
        (näitaja_tee/'report.json').write_text(json.dumps(valideerima, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Käivita_2()
