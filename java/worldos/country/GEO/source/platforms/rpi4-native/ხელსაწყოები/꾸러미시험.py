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
from შესრულება_ბრძანება import პროეცირება_ფესვი


def 시험휠(სახელი, 파일들, დავალება_მნიშვნელობა='Root-Is-Purelib: true\n', 의존성=''):
    მონაცემები = io.BytesIO()
    with zipfile.ZipFile(მონაცემები, 'w', zipfile.ZIP_DEFLATED) as შეკვრა:
        შეკვრა.writestr(სახელი + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + დავალება_მნიშვნელობა)
        შეკვრა.writestr(სახელი + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + სახელი + '\nVersion: 1.0\n' + 의존성)
        for გეზი, შიგთავსი_მნიშვნელობა in 파일들.items():
            შეკვრა.writestr(გეზი, შიგთავსი_მნიშვნელობა)
    return მონაცემები.getvalue()


def შემოწმება_მასპინძელი():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'მნიშვნელობა=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'მნიშვნელობა=42\n'.encode()}
    for მონაცემები in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', მონაცემები, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel გეზი·ზომა·C გაფართოება_მნიშვნელობა·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def გაშვება():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    შემოწმება_მასპინძელი()
    if 인수.host_only:
        return
    გაზომვა_მდებარეობა = პროეცირება_ფესვი/'build/verification/pip'
    გაზომვა_მდებარეობა.mkdir(parents=True, exist_ok=True)
    საცავი_მდებარეობა = გაზომვა_მდებარეობა/'cache'
    საცავი_მდებარეობა.mkdir(exist_ok=True)
    # რეალური_მონაცემები PyPI 배포 ფაილი. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(პროეცირება_ფესვი/'build/pip-cache').მომზადება('micropython-bisect==3.3.3')
    for დაბოლოება_მნიშვნელობა in ('.archive', '.json'):
        shutil.copyfile(str(პროეცირება_ფესვი/'build/pip-cache'/('micropython-bisect==3.3.3'+დაბოლოება_მნიშვნელობა)), str(საცავი_მდებარეობა/('micropython-bisect==3.3.3'+დაბოლოება_მნიშვნელობა)))
    실물기록 = json.loads((საცავი_მდებარეობა/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for სახელი, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'მნიშვნელობა=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        მონაცემები = 시험휠(სახელი, 파일들)
        (საცავი_მდებარეობა/(სახელი+'==1.0.archive')).write_bytes(მონაცემები)
        (საცავი_მდებარეობა/(სახელი+'==1.0.json')).write_text(json.dumps({'name': სახელი, 'version': '1.0',
            'filename': სახელი.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(მონაცემები).hexdigest()}))
    შემოწმება = {'passed': False, 'kernel_sha256': hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    პროცესი = subprocess.Popen(['python3', str(პროეცირება_ფესვი/'ხელსაწყოები/შესრულება_ბრძანება.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(საცავი_მდებარეობა), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    სელექტორი_a916db4e = selectors.DefaultSelector()
    სელექტორი_a916db4e.register(პროცესი.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(ჩვენება_მნიშვნელობა=b'jkoros-native> '):
        შიგთავსი_მნიშვნელობა = bytearray()
        끝 = time.monotonic()+120
        while ჩვენება_მნიშვნელობა not in შიგთავსი_მნიშვნელობა:
            if time.monotonic() > 끝 or პროცესი.poll() is not None:
                raise AssertionError('게스트 პასუხი 없음: '+შიგთავსი_მნიშვნელობა.decode('utf-8','replace'))
            for შენატანი_მნიშვნელობა, _ in სელექტორი_a916db4e.select(.1):
                조각 = შენატანი_მნიშვნელობა.fileobj.read(4096)
                შიგთავსი_მნიშვნელობა.extend(조각)
                대화기록.extend(조각)
        return შიგთავსი_მნიშვნელობა.decode('utf-8', 'replace').replace('\r\n','\n')
    def გარემო(ბრძანება, ჩვენება_მნიშვნელობა=b'jkoros-native> '):
        პროცესი.stdin.write(ბრძანება.encode()+b'\n')
        პროცესი.stdin.flush()
        return 기다리기(ჩვენება_მნიშვნელობა)
    def შესრულება_ბრძანება(ბრძანება, 예상, სტატუსი_მნიშვნელობა=0):
        შიგთავსი_მნიშვნელობა = გარემო(ბრძანება)
        assert 예상 in შიგთავსი_მნიშვნელობა and '\nexit '+str(სტატუსი_მნიშვნელობა)+'\n' in შიგთავსი_მნიშვნელობა, შიგთავსი_მნიშვნელობა
        შემოწმება['checks'].append(ბრძანება)
        return შიგთავსი_მნიშვნელობა
    def ატვირთვა_ფაილები(სახელი, მონაცემები):
        გარემო('load '+სახელი, b'hex> ')
        for პოზიცია_ინდექსი in range(0, len(მონაცემები), 64):
            გარემო(მონაცემები[პოზიცია_ინდექსი:პოზიცია_ინდექსი+64].hex(), b'hex> ')
        assert 'LOADED' in გარემო('.')
    try:
        기다리기()
        შესრულება_ბრძანება('pip --help', 'MicroPython წყარო_ხე 설치기')
        ატვირთვა_ფაილები('오류시험.py', (პროეცირება_ფესვი/'시험/파이썬/한국어오류시험.py').read_bytes())
        შესრულება_ბრძანება('python 오류시험.py', '한국어 ფაილი 예외 გადამოწმება')
        შესრულება_ბრძანება('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'ინსტალაცია_მნიშვნელობა 완료: micropython-bisect 3.3.3')
        შესრულება_ბრძანება('python -c \'from bisect import insort as 순서대로넣기; მნიშვნელობა=[1,5]; 순서대로넣기(მნიშვნელობა,3); print(მნიშვნელობა)\'', '[1, 3, 5]')
        შესრულება_ბრძანება('python -m pip list', 'micropython-bisect 3.3.3')
        შესრულება_ბრძანება('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        შესრულება_ბრძანება('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'ინსტალაცია_მნიშვნელობა 완료: jkoros-fixture')
        შესრულება_ბრძანება('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        შესრულება_ბრძანება('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'შეკვრა შეცდომა:', 1)
        შესრულება_ბრძანება('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 შეცდომა 보존")\'', '구문 შეცდომა 보존')
        ატვირთვა_ფაილები('공간시험.py', (პროეცირება_ფესვი/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        შესრულება_ბრძანება('python 공간시험.py '+str(접속번호), 'შეკვრა 공간 부족 დაბრუნება_ხიდი გადამოწმება')
        შესრულება_ბრძანება('pip uninstall jkoros-fixture', 'ამოშლა_შენატანი 완료: jkoros-fixture')
        შესრულება_ბრძანება('pip uninstall micropython-bisect', 'ამოშლა_შენატანი 완료: micropython-bisect')
        შესრულება_ბრძანება('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ამოშლა_შენატანი გადამოწმება")\'', 'ამოშლა_შენატანი გადამოწმება')
        შემოწმება['passed'] = True
        print('PASS: PyPI 실물 ინსტალაცია_მნიშვნელობა·import·შესრულება_ბრძანება, 한국어 예외, 패키지 საქაღალდე_მნიშვნელობა, მარცხი_მნიშვნელობა დაბრუნება_ხიდი, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 გასვლა_აპი 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            პროცესი.stdin.write(b'\x01x')
            პროცესი.stdin.flush()
            პროცესი.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            პროცესი.terminate()
            try:
                პროცესი.wait(timeout=8)
            except subprocess.TimeoutExpired:
                პროცესი.kill()
                პროცესი.wait()
        if პროცესი.poll() is None:
            პროცესი.kill()
            პროცესი.wait()
        სელექტორი_a916db4e.close()
        პროცესი.stdin.close()
        პროცესი.stdout.close()
        (გაზომვა_მდებარეობა/'serial.log').write_bytes(대화기록)
        (გაზომვა_მდებარეობა/'report.json').write_text(json.dumps(შემოწმება, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    გაშვება()
