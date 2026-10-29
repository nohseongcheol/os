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
from 꾸러미중계 import пакет_рэпазіторый, 압축풀기
from выканаць_каманда import 기준


def 시험휠(Назва, 파일들, зварот_значэнне='Root-Is-Purelib: true\n', 의존성=''):
    дадзеныя = io.BytesIO()
    with zipfile.ZipFile(дадзеныя, 'w', zipfile.ZIP_DEFLATED) as пакет:
        пакет.writestr(Назва + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + зварот_значэнне)
        пакет.writestr(Назва + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Назва + '\nVersion: 1.0\n' + 의존성)
        for ШЛЯХ, кантэнт_значэнне in 파일들.items():
            пакет.writestr(ШЛЯХ, кантэнт_значэнне)
    return дадзеныя.getvalue()


def чэк_вузел():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'значэнне=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'значэнне=42\n'.encode()}
    for дадзеныя in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', дадзеныя, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ШЛЯХ·Памер·C пашырэнне_значэнне·의존성 адхіліць_значэнне')


def нулявая_нумар_порта():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Выканаць():
    аналізатар_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатар_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = аналізатар_48ee4b1b.parse_args()
    чэк_вузел()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Сховішча_шлях = 결과경로/'cache'
    Сховішча_шлях.mkdir(exist_ok=True)
    # фактычны_дадзеныя PyPI 배포 Файл. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    пакет_рэпазіторый(기준/'build/pip-cache').Падрыхтаваць('micropython-bisect==3.3.3')
    for канцавы_вузел_значэнне in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+канцавы_вузел_значэнне)), str(Сховішча_шлях/('micropython-bisect==3.3.3'+канцавы_вузел_значэнне)))
    실물기록 = json.loads((Сховішча_шлях/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Назва, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'значэнне=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        дадзеныя = 시험휠(Назва, 파일들)
        (Сховішча_шлях/(Назва+'==1.0.archive')).write_bytes(дадзеныя)
        (Сховішча_шлях/(Назва+'==1.0.json')).write_text(json.dumps({'name': Назва, 'version': '1.0',
            'filename': Назва.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(дадзеныя).hexdigest()}))
    праверыць_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    нумар_порта = нулявая_нумар_порта()
    Працэс = subprocess.Popen(['python3', str(기준/'Інструменты/выканаць_каманда.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(нумар_порта), '--pip-cache', str(Сховішча_шлях), '--ftp-port', str(нулявая_нумар_порта())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектар_a916db4e = selectors.DefaultSelector()
    селектар_a916db4e.register(Працэс.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(паказаць_значэнне=b'jkoros-native> '):
        кантэнт_значэнне = bytearray()
        끝 = time.monotonic()+120
        while паказаць_значэнне not in кантэнт_значэнне:
            if time.monotonic() > 끝 or Працэс.poll() is not None:
                raise AssertionError('게스트 адказаць 없음: '+кантэнт_значэнне.decode('utf-8','replace'))
            for увядзенне_значэнне, _ in селектар_a916db4e.select(.1):
                조각 = увядзенне_значэнне.fileobj.read(4096)
                кантэнт_значэнне.extend(조각)
                대화기록.extend(조각)
        return кантэнт_значэнне.decode('utf-8', 'replace').replace('\r\n','\n')
    def абалонка(Загад, паказаць_значэнне=b'jkoros-native> '):
        Працэс.stdin.write(Загад.encode()+b'\n')
        Працэс.stdin.flush()
        return 기다리기(паказаць_значэнне)
    def выканаць_каманда(Загад, 예상, стан_значэнне=0):
        кантэнт_значэнне = абалонка(Загад)
        assert 예상 in кантэнт_значэнне and '\nexit '+str(стан_значэнне)+'\n' in кантэнт_значэнне, кантэнт_значэнне
        праверыць_5fb2b747['checks'].append(Загад)
        return кантэнт_значэнне
    def запампоўка_Файлы(Назва, дадзеныя):
        абалонка('load '+Назва, b'hex> ')
        for 자리 in range(0, len(дадзеныя), 64):
            абалонка(дадзеныя[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in абалонка('.')
    try:
        기다리기()
        выканаць_каманда('pip --help', 'MicroPython крыніца_дрэва 설치기')
        запампоўка_Файлы('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        выканаць_каманда('python 오류시험.py', '한국어 Файл выключэнне праверыць')
        выканаць_каманда('pip install micropython-bisect==3.3.3 --port '+str(нумар_порта), 'усталяваць_значэнне 완료: micropython-bisect 3.3.3')
        выканаць_каманда('python -c \'from bisect import insort as 순서대로넣기; значэнне=[1,5]; 순서대로넣기(значэнне,3); print(значэнне)\'', '[1, 3, 5]')
        выканаць_каманда('python -m pip list', 'micropython-bisect 3.3.3')
        выканаць_каманда('pip install micropython-bisect==3.3.3 --port '+str(нумар_порта), '이미 설치됨:')
        выканаць_каманда('pip install jkoros-fixture==1.0 --port '+str(нумар_порта), 'усталяваць_значэнне 완료: jkoros-fixture')
        выканаць_каманда('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        выканаць_каманда('pip install jkoros-syntax==1.0 --port '+str(нумар_порта), 'пакет ПАМЫЛКА:', 1)
        выканаць_каманда('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ПАМЫЛКА 보존")\'', '구문 ПАМЫЛКА 보존')
        запампоўка_Файлы('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        выканаць_каманда('python 공간시험.py '+str(нумар_порта), 'пакет 공간 부족 되돌림 праверыць')
        выканаць_каманда('pip uninstall jkoros-fixture', 'выдаліць_увядзенне 완료: jkoros-fixture')
        выканаць_каманда('pip uninstall micropython-bisect', 'выдаліць_увядзенне 완료: micropython-bisect')
        выканаць_каманда('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("выдаліць_увядзенне праверыць")\'', 'выдаліць_увядзенне праверыць')
        праверыць_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 усталяваць_значэнне·import·выканаць_каманда, 한국어 выключэнне, 패키지 каталог_значэнне, няўдача_значэнне 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Выхад_праграма 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Працэс.stdin.write(b'\x01x')
            Працэс.stdin.flush()
            Працэс.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Працэс.terminate()
            try:
                Працэс.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Працэс.kill()
                Працэс.wait()
        if Працэс.poll() is None:
            Працэс.kill()
            Працэс.wait()
        селектар_a916db4e.close()
        Працэс.stdin.close()
        Працэс.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(праверыць_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Выканаць()
