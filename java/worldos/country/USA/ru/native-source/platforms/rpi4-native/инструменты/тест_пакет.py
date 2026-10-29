#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 входные_данные_ЗНАЧЕН·RAM 되돌림을 свой 커널에서 검사한다."""
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
from пакет_Ретрансляция import пакет_репозиторий, распаковать
from 실행 import задача_корень


def тест_манипулятор_колесико(Название, 파일들, сумма_контракта='Root-Is-Purelib: true\n', 의존성=''):
    данные = io.BytesIO()
    with zipfile.ZipFile(данные, 'w', zipfile.ZIP_DEFLATED) as пакет:
        пакет.writestr(Название + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + сумма_контракта)
        пакет.writestr(Название + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Название + '\nVersion: 1.0\n' + 의존성)
        for путь, контент_ЗНАЧЕН in 파일들.items():
            пакет.writestr(путь, контент_ЗНАЧЕН)
    return данные.getvalue()


def чек_узел():
    ИТ_службы_обычный = тест_манипулятор_колесико('jkoros-fixture', {'mod.py': 'ЗНАЧЕН=42\n'})
    assert распаковать('jkoros_fixture-1.0-py3-none-any.whl', ИТ_службы_обычный, 'jkoros-fixture', '1.0') == {'mod.py': 'ЗНАЧЕН=42\n'.encode()}
    for данные in (
            тест_манипулятор_колесико('jkoros-fixture', {'../escape.py': ''}),
            тест_манипулятор_колесико('jkoros-fixture', {'/abs.py': ''}),
            тест_манипулятор_колесико('jkoros-fixture', {'big.py': 'x' * 16385}),
            тест_манипулятор_колесико('jkoros-fixture', {'mod.so': ''}),
            тест_манипулятор_колесико('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            тест_манипулятор_колесико('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            распаковать('jkoros_fixture-1.0-py3-none-any.whl', данные, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel путь·Размер·C расширение_ЗНАЧЕН·의존성 отклонить_ЗНАЧЕН')


def пустой_номер_порта():
    with socket.socket() as сокет_ЗНАЧЕН:
        сокет_ЗНАЧЕН.bind(('127.0.0.1', 0))
        return сокет_ЗНАЧЕН.getsockname()[1]


def запустить():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--host-only', action='store_true')
    аргументы = анализатор_48ee4b1b.parse_args()
    чек_узел()
    if аргументы.host_only:
        return
    KR_путь = задача_корень/'build/verification/pip'
    KR_путь.mkdir(parents=True, exist_ok=True)
    Память_путь = KR_путь/'cache'
    Память_путь.mkdir(exist_ok=True)
    # фактический_данные PyPI распределение_ЗНАЧЕН файл. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    пакет_репозиторий(задача_корень/'build/pip-cache').Подготовить('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(задача_корень/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Память_путь/('micropython-bisect==3.3.3'+꼬리)))
    аппаратный_LOG = json.loads((Память_путь/'micropython-bisect==3.3.3.json').read_text())
    assert аппаратный_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Название, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,СЕКУНДЫ_операнд):\n return 가+СЕКУНДЫ_операнд\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'ЗНАЧЕН=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        данные = тест_манипулятор_колесико(Название, 파일들)
        (Память_путь/(Название+'==1.0.archive')).write_bytes(данные)
        (Память_путь/(Название+'==1.0.json')).write_text(json.dumps({'name': Название, 'version': '1.0',
            'filename': Название.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(данные).hexdigest()}))
    проверить = {'passed': False, 'kernel_sha256': hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': аппаратный_LOG, 'checks': []}
    номер_порта = пустой_номер_порта()
    Процесс = subprocess.Popen(['python3', str(задача_корень/'инструменты/실행.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(номер_порта), '--pip-cache', str(Память_путь), '--ftp-port', str(пустой_номер_порта())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор_a916db4e = selectors.DefaultSelector()
    селектор_a916db4e.register(Процесс.stdout, selectors.EVENT_READ)
    расшифровка = bytearray()
    def 기다리기(выпуск_ЗНАЧЕН=b'jkoros-native> '):
        контент_ЗНАЧЕН = bytearray()
        끝 = time.monotonic()+120
        while выпуск_ЗНАЧЕН not in контент_ЗНАЧЕН:
            if time.monotonic() > 끝 or Процесс.poll() is not None:
                raise AssertionError('게스트 ответ 없음: '+контент_ЗНАЧЕН.decode('utf-8','replace'))
            for ввод_ЗНАЧЕН, _ in селектор_a916db4e.select(.1):
                блок_ЗНАЧЕН_652d4b53 = ввод_ЗНАЧЕН.fileobj.read(4096)
                контент_ЗНАЧЕН.extend(блок_ЗНАЧЕН_652d4b53)
                расшифровка.extend(блок_ЗНАЧЕН_652d4b53)
        return контент_ЗНАЧЕН.decode('utf-8', 'replace').replace('\r\n','\n')
    def оболочка(команда, выпуск_ЗНАЧЕН=b'jkoros-native> '):
        Процесс.stdin.write(команда.encode()+b'\n')
        Процесс.stdin.flush()
        return 기다리기(выпуск_ЗНАЧЕН)
    def 실행(команда, 예상, Состояние_ЗНАЧЕН=0):
        контент_ЗНАЧЕН = оболочка(команда)
        assert 예상 in контент_ЗНАЧЕН and '\nexit '+str(Состояние_ЗНАЧЕН)+'\n' in контент_ЗНАЧЕН, контент_ЗНАЧЕН
        проверить['checks'].append(команда)
        return контент_ЗНАЧЕН
    def Upload_Файлы(Название, данные):
        оболочка('load '+Название, b'hex> ')
        for позиция_ИНДЕКС in range(0, len(данные), 64):
            оболочка(данные[позиция_ИНДЕКС:позиция_ИНДЕКС+64].hex(), b'hex> ')
        assert 'LOADED' in оболочка('.')
    try:
        기다리기()
        실행('pip --help', 'MicroPython источник_дерево 설치기')
        Upload_Файлы('오류시험.py', (задача_корень/'испытания/PYTHON/한국어오류시험.py').read_bytes())
        실행('python 오류시험.py', 'русский файл исключение проверять')
        실행('pip install micropython-bisect==3.3.3 --port '+str(номер_порта), 'установить_ЗНАЧЕН 완료: micropython-bisect 3.3.3')
        실행('python -c \'from bisect import insort as 순서대로넣기; ЗНАЧЕН=[1,5]; 순서대로넣기(ЗНАЧЕН,3); print(ЗНАЧЕН)\'', '[1, 3, 5]')
        실행('python -m pip list', 'micropython-bisect 3.3.3')
        실행('pip install micropython-bisect==3.3.3 --port '+str(номер_порта), '이미 설치됨:')
        실행('pip install jkoros-fixture==1.0 --port '+str(номер_порта), 'установить_ЗНАЧЕН 완료: jkoros-fixture')
        실행('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        실행('pip install jkoros-syntax==1.0 --port '+str(номер_порта), 'пакет ошибка:', 1)
        실행('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ошибка 보존")\'', '구문 ошибка 보존')
        Upload_Файлы('공간시험.py', (задача_корень/'испытания/PYTHON/пакет_корень_тест.py').read_bytes())
        실행('python 공간시험.py '+str(номер_порта), 'пакет АДРЕС_регион 부족 Возврат_мост проверять')
        실행('pip uninstall jkoros-fixture', 'удалить_ввод 완료: jkoros-fixture')
        실행('pip uninstall micropython-bisect', 'удалить_ввод 완료: micropython-bisect')
        실행('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("удалить_ввод проверять")\'', 'удалить_ввод проверять')
        проверить['passed'] = True
        print('PASS: PyPI 실물 установить_ЗНАЧЕН·import·실행, русский исключение, 패키지 Каталог_ЗНАЧЕН, сбой_ЗНАЧЕН Возврат_мост, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Выход_программа 키로 QEMU를 끝내면 실행기의 Ретрансляция_ЗНАЧЕН 문맥도 정리된다.
            Процесс.stdin.write(b'\x01x')
            Процесс.stdin.flush()
            Процесс.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Процесс.terminate()
            try:
                Процесс.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Процесс.kill()
                Процесс.wait()
        if Процесс.poll() is None:
            Процесс.kill()
            Процесс.wait()
        селектор_a916db4e.close()
        Процесс.stdin.close()
        Процесс.stdout.close()
        (KR_путь/'serial.log').write_bytes(расшифровка)
        (KR_путь/'report.json').write_text(json.dumps(проверить, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    запустить()
