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
from 꾸러미중계 import пакет_склад, 압축풀기
from Изврши_наредба import Project_корен


def 시험휠(Име, 파일들, задача_VALUE_102996da='Root-Is-Purelib: true\n', 의존성=''):
    податоци = io.BytesIO()
    with zipfile.ZipFile(податоци, 'w', zipfile.ZIP_DEFLATED) as пакет:
        пакет.writestr(Име + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + задача_VALUE_102996da)
        пакет.writestr(Име + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Име + '\nVersion: 1.0\n' + 의존성)
        for ПАТЕКА, Содржина_VALUE in 파일들.items():
            пакет.writestr(ПАТЕКА, Содржина_VALUE)
    return податоци.getvalue()


def провери_вдоми():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for податоци in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', податоци, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ПАТЕКА·Големина·C наставка_VALUE·의존성 одбива_VALUE')


def празно_број_на_порта():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Изврши_2():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--host-only', action='store_true')
    Аргументи = анализатор_48ee4b1b.parse_args()
    провери_вдоми()
    if Аргументи.host_only:
        return
    мерка_патека = Project_корен/'build/verification/pip'
    мерка_патека.mkdir(parents=True, exist_ok=True)
    Склад_патека = мерка_патека/'cache'
    Склад_патека.mkdir(exist_ok=True)
    # реален_податоци PyPI 배포 Датотека. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    пакет_склад(Project_корен/'build/pip-cache').Подготви('micropython-bisect==3.3.3')
    for крак_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(Project_корен/'build/pip-cache'/('micropython-bisect==3.3.3'+крак_VALUE)), str(Склад_патека/('micropython-bisect==3.3.3'+крак_VALUE)))
    실물기록 = json.loads((Склад_патека/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Име, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        податоци = 시험휠(Име, 파일들)
        (Склад_патека/(Име+'==1.0.archive')).write_bytes(податоци)
        (Склад_патека/(Име+'==1.0.json')).write_text(json.dumps({'name': Име, 'version': '1.0',
            'filename': Име.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(податоци).hexdigest()}))
    потврди = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    број_на_порта = празно_број_на_порта()
    Процес = subprocess.Popen(['python3', str(Project_корен/'Алатки/Изврши_наредба.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(број_на_порта), '--pip-cache', str(Склад_патека), '--ftp-port', str(празно_број_на_порта())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    избирач_a916db4e = selectors.DefaultSelector()
    избирач_a916db4e.register(Процес.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(прикажи_VALUE=b'jkoros-native> '):
        Содржина_VALUE = bytearray()
        끝 = time.monotonic()+120
        while прикажи_VALUE not in Содржина_VALUE:
            if time.monotonic() > 끝 or Процес.poll() is not None:
                raise AssertionError('게스트 одговори 없음: '+Содржина_VALUE.decode('utf-8','replace'))
            for внес_VALUE, _ in избирач_a916db4e.select(.1):
                조각 = внес_VALUE.fileobj.read(4096)
                Содржина_VALUE.extend(조각)
                대화기록.extend(조각)
        return Содржина_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def обвивка(Команда, прикажи_VALUE=b'jkoros-native> '):
        Процес.stdin.write(Команда.encode()+b'\n')
        Процес.stdin.flush()
        return 기다리기(прикажи_VALUE)
    def Изврши_наредба(Команда, 예상, статус_VALUE=0):
        Содржина_VALUE = обвивка(Команда)
        assert 예상 in Содржина_VALUE and '\nexit '+str(статус_VALUE)+'\n' in Содржина_VALUE, Содржина_VALUE
        потврди['checks'].append(Команда)
        return Содржина_VALUE
    def постави_Датотеки(Име, податоци):
        обвивка('load '+Име, b'hex> ')
        for позиционирање_INDEX in range(0, len(податоци), 64):
            обвивка(податоци[позиционирање_INDEX:позиционирање_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in обвивка('.')
    try:
        기다리기()
        Изврши_наредба('pip --help', 'MicroPython извор_дрво 설치기')
        постави_Датотеки('오류시험.py', (Project_корен/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Изврши_наредба('python 오류시험.py', 'Македонски Датотека исклучок провери')
        Изврши_наредба('pip install micropython-bisect==3.3.3 --port '+str(број_на_порта), 'инсталирај_VALUE 완료: micropython-bisect 3.3.3')
        Изврши_наредба('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Изврши_наредба('python -m pip list', 'micropython-bisect 3.3.3')
        Изврши_наредба('pip install micropython-bisect==3.3.3 --port '+str(број_на_порта), '이미 설치됨:')
        Изврши_наредба('pip install jkoros-fixture==1.0 --port '+str(број_на_порта), 'инсталирај_VALUE 완료: jkoros-fixture')
        Изврши_наредба('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Изврши_наредба('pip install jkoros-syntax==1.0 --port '+str(број_на_порта), 'пакет ГРЕШКА:', 1)
        Изврши_наредба('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ГРЕШКА 보존")\'', '구문 ГРЕШКА 보존')
        постави_Датотеки('공간시험.py', (Project_корен/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Изврши_наредба('python 공간시험.py '+str(број_на_порта), 'пакет 공간 부족 되돌림 провери')
        Изврши_наредба('pip uninstall jkoros-fixture', 'отстрани_внес 완료: jkoros-fixture')
        Изврши_наредба('pip uninstall micropython-bisect', 'отстрани_внес 완료: micropython-bisect')
        Изврши_наредба('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("отстрани_внес провери")\'', 'отстрани_внес провери')
        потврди['passed'] = True
        print('PASS: PyPI 실물 инсталирај_VALUE·import·Изврши_наредба, Македонски исклучок, 패키지 Именик_VALUE, неуспех_VALUE 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Излез_програма 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Процес.stdin.write(b'\x01x')
            Процес.stdin.flush()
            Процес.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Процес.terminate()
            try:
                Процес.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Процес.kill()
                Процес.wait()
        if Процес.poll() is None:
            Процес.kill()
            Процес.wait()
        избирач_a916db4e.close()
        Процес.stdin.close()
        Процес.stdout.close()
        (мерка_патека/'serial.log').write_bytes(대화기록)
        (мерка_патека/'report.json').write_text(json.dumps(потврди, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Изврши_2()
