#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 своє 커널에서 검사한다."""
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
from 꾸러미중계 import набір_репозиторій, розпакувати
from Виконати_команда import Дії_корінь


def 시험휠(Назва, 파일들, контракт_значення='Root-Is-Purelib: true\n', 의존성=''):
    дані = io.BytesIO()
    with zipfile.ZipFile(дані, 'w', zipfile.ZIP_DEFLATED) as набір:
        набір.writestr(Назва + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + контракт_значення)
        набір.writestr(Назва + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Назва + '\nVersion: 1.0\n' + 의존성)
        for шлях, Вміст_значення in 파일들.items():
            набір.writestr(шлях, Вміст_значення)
    return дані.getvalue()


def перевіряти_хост():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'значення=42\n'})
    assert розпакувати('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'значення=42\n'.encode()}
    for дані in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            розпакувати('jkoros_fixture-1.0-py3-none-any.whl', дані, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel шлях·Розмір·C розширення_значення·의존성 відхилити_значення')


def 빈접속번호():
    with socket.socket() as сокет_значення:
        сокет_значення.bind(('127.0.0.1', 0))
        return сокет_значення.getsockname()[1]


def запустити():
    аналізатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатор_48ee4b1b.add_argument('--host-only', action='store_true')
    аргументи = аналізатор_48ee4b1b.parse_args()
    перевіряти_хост()
    if аргументи.host_only:
        return
    КР_шлях = Дії_корінь/'build/verification/pip'
    КР_шлях.mkdir(parents=True, exist_ok=True)
    місце_шлях_02e62bb7 = КР_шлях/'cache'
    місце_шлях_02e62bb7.mkdir(exist_ok=True)
    # фактично_дані PyPI 배포 файл. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    набір_репозиторій(Дії_корінь/'build/pip-cache').Готувати('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(Дії_корінь/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(місце_шлях_02e62bb7/('micropython-bisect==3.3.3'+꼬리)))
    обладнання_журнал = json.loads((місце_шлях_02e62bb7/'micropython-bisect==3.3.3.json').read_text())
    assert обладнання_журнал['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Назва, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'значення=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        дані = 시험휠(Назва, 파일들)
        (місце_шлях_02e62bb7/(Назва+'==1.0.archive')).write_bytes(дані)
        (місце_шлях_02e62bb7/(Назва+'==1.0.json')).write_text(json.dumps({'name': Назва, 'version': '1.0',
            'filename': Назва.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(дані).hexdigest()}))
    затвердити = {'passed': False, 'kernel_sha256': hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': обладнання_журнал, 'checks': []}
    номер_порту = 빈접속번호()
    Процеси = subprocess.Popen(['python3', str(Дії_корінь/'інструменти/Виконати_команда.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(номер_порту), '--pip-cache', str(місце_шлях_02e62bb7), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор_a916db4e = selectors.DefaultSelector()
    селектор_a916db4e.register(Процеси.stdout, selectors.EVENT_READ)
    транскрипт = bytearray()
    def 기다리기(показувати_значення=b'jkoros-native> '):
        Вміст_значення = bytearray()
        끝 = time.monotonic()+120
        while показувати_значення not in Вміст_значення:
            if time.monotonic() > 끝 or Процеси.poll() is not None:
                raise AssertionError('게스트 відповідь 없음: '+Вміст_значення.decode('utf-8','replace'))
            for запис_значення_962f286b, _ in селектор_a916db4e.select(.1):
                조각 = запис_значення_962f286b.fileobj.read(4096)
                Вміст_значення.extend(조각)
                транскрипт.extend(조각)
        return Вміст_значення.decode('utf-8', 'replace').replace('\r\n','\n')
    def оболонка(команда, показувати_значення=b'jkoros-native> '):
        Процеси.stdin.write(команда.encode()+b'\n')
        Процеси.stdin.flush()
        return 기다리기(показувати_значення)
    def Виконати_команда(команда, 예상, Стан_значення=0):
        Вміст_значення = оболонка(команда)
        assert 예상 in Вміст_значення and '\nexit '+str(Стан_значення)+'\n' in Вміст_значення, Вміст_значення
        затвердити['checks'].append(команда)
        return Вміст_значення
    def передавати_Файли(Назва, дані):
        оболонка('load '+Назва, b'hex> ')
        for індекс_розташування in range(0, len(дані), 64):
            оболонка(дані[індекс_розташування:індекс_розташування+64].hex(), b'hex> ')
        assert 'LOADED' in оболонка('.')
    try:
        기다리기()
        Виконати_команда('pip --help', 'MicroPython джерело_дерево 설치기')
        передавати_Файли('오류시험.py', (Дії_корінь/'випробування/파이썬/한국어오류시험.py').read_bytes())
        Виконати_команда('python 오류시험.py', 'українська файл виняток перевіряти')
        Виконати_команда('pip install micropython-bisect==3.3.3 --port '+str(номер_порту), 'інсталювати_значення 완료: micropython-bisect 3.3.3')
        Виконати_команда('python -c \'from bisect import insort as 순서대로넣기; значення=[1,5]; 순서대로넣기(значення,3); print(значення)\'', '[1, 3, 5]')
        Виконати_команда('python -m pip list', 'micropython-bisect 3.3.3')
        Виконати_команда('pip install micropython-bisect==3.3.3 --port '+str(номер_порту), '이미 설치됨:')
        Виконати_команда('pip install jkoros-fixture==1.0 --port '+str(номер_порту), 'інсталювати_значення 완료: jkoros-fixture')
        Виконати_команда('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Виконати_команда('pip install jkoros-syntax==1.0 --port '+str(номер_порту), 'набір ПОМИЛКА:', 1)
        Виконати_команда('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ПОМИЛКА 보존")\'', '구문 ПОМИЛКА 보존')
        передавати_Файли('공간시험.py', (Дії_корінь/'випробування/파이썬/꾸러미공간시험.py').read_bytes())
        Виконати_команда('python 공간시험.py '+str(номер_порту), 'набір адреса_область 부족 повернути_міст перевіряти')
        Виконати_команда('pip uninstall jkoros-fixture', 'вилучати_запис 완료: jkoros-fixture')
        Виконати_команда('pip uninstall micropython-bisect', 'вилучати_запис 완료: micropython-bisect')
        Виконати_команда('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("вилучати_запис перевіряти")\'', 'вилучати_запис перевіряти')
        затвердити['passed'] = True
        print('PASS: PyPI 실물 інсталювати_значення·import·Виконати_команда, українська виняток, 패키지 Каталог_значення, неполадка_значення повернути_міст, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Вийти_програма 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Процеси.stdin.write(b'\x01x')
            Процеси.stdin.flush()
            Процеси.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Процеси.terminate()
            try:
                Процеси.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Процеси.kill()
                Процеси.wait()
        if Процеси.poll() is None:
            Процеси.kill()
            Процеси.wait()
        селектор_a916db4e.close()
        Процеси.stdin.close()
        Процеси.stdout.close()
        (КР_шлях/'serial.log').write_bytes(транскрипт)
        (КР_шлях/'report.json').write_text(json.dumps(затвердити, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    запустити()
