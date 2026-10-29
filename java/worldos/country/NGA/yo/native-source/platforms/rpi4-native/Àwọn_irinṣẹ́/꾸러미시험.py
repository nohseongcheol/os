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
from ṣiṣẹ́_àṣẹ import 기준


def 시험휠(Orúkọ, 파일들, iṣẹ́_iye='Root-Is-Purelib: true\n', 의존성=''):
    détà = io.BytesIO()
    with zipfile.ZipFile(détà, 'w', zipfile.ZIP_DEFLATED) as àkópọ̀:
        àkópọ̀.writestr(Orúkọ + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + iṣẹ́_iye)
        àkópọ̀.writestr(Orúkọ + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Orúkọ + '\nVersion: 1.0\n' + 의존성)
        for ọ̀nà, Àkóónú_iye in 파일들.items():
            àkópọ̀.writestr(ọ̀nà, Àkóónú_iye)
    return détà.getvalue()


def ṣàyẹ̀wò_olùpèsè():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'iye=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'iye=42\n'.encode()}
    for détà in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', détà, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ọ̀nà·Ìwọ̀n·C Àfikún_iye·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Rọ́ọ̀nù():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    ṣàyẹ̀wò_olùpèsè()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Ibi_ìpamọ́_ọ̀nà = 결과경로/'cache'
    Ibi_ìpamọ́_ọ̀nà.mkdir(exist_ok=True)
    # gangan_détà PyPI 배포 Fáìlì. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').gbaradì('micropython-bisect==3.3.3')
    for ìrù_iye in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+ìrù_iye)), str(Ibi_ìpamọ́_ọ̀nà/('micropython-bisect==3.3.3'+ìrù_iye)))
    ohun_èlò_alárídìmú_àkọsílẹ̀_ìṣe = json.loads((Ibi_ìpamọ́_ọ̀nà/'micropython-bisect==3.3.3.json').read_text())
    assert ohun_èlò_alárídìmú_àkọsílẹ̀_ìṣe['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Orúkọ, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'iye=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        détà = 시험휠(Orúkọ, 파일들)
        (Ibi_ìpamọ́_ọ̀nà/(Orúkọ+'==1.0.archive')).write_bytes(détà)
        (Ibi_ìpamọ́_ọ̀nà/(Orúkọ+'==1.0.json')).write_text(json.dumps({'name': Orúkọ, 'version': '1.0',
            'filename': Orúkọ.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(détà).hexdigest()}))
    ìfọwọ́síìwé = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': ohun_èlò_alárídìmú_àkọsílẹ̀_ìṣe, 'checks': []}
    접속번호 = 빈접속번호()
    Ìlànà = subprocess.Popen(['python3', str(기준/'Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Ibi_ìpamọ́_ọ̀nà), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    olùyàn_a916db4e = selectors.DefaultSelector()
    olùyàn_a916db4e.register(Ìlànà.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(ṣàfihàn_iye=b'jkoros-native> '):
        Àkóónú_iye = bytearray()
        끝 = time.monotonic()+120
        while ṣàfihàn_iye not in Àkóónú_iye:
            if time.monotonic() > 끝 or Ìlànà.poll() is not None:
                raise AssertionError('게스트 Fèsì 없음: '+Àkóónú_iye.decode('utf-8','replace'))
            for ìgbéwọlé_iye, _ in olùyàn_a916db4e.select(.1):
                조각 = ìgbéwọlé_iye.fileobj.read(4096)
                Àkóónú_iye.extend(조각)
                대화기록.extend(조각)
        return Àkóónú_iye.decode('utf-8', 'replace').replace('\r\n','\n')
    def ṣẹ́ẹ̀lì(Àṣẹ, ṣàfihàn_iye=b'jkoros-native> '):
        Ìlànà.stdin.write(Àṣẹ.encode()+b'\n')
        Ìlànà.stdin.flush()
        return 기다리기(ṣàfihàn_iye)
    def ṣiṣẹ́_àṣẹ(Àṣẹ, 예상, ipò_iye=0):
        Àkóónú_iye = ṣẹ́ẹ̀lì(Àṣẹ)
        assert 예상 in Àkóónú_iye and '\nexit '+str(ipò_iye)+'\n' in Àkóónú_iye, Àkóónú_iye
        ìfọwọ́síìwé['checks'].append(Àṣẹ)
        return Àkóónú_iye
    def fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì(Orúkọ, détà):
        ṣẹ́ẹ̀lì('load '+Orúkọ, b'hex> ')
        for 자리 in range(0, len(détà), 64):
            ṣẹ́ẹ̀lì(détà[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in ṣẹ́ẹ̀lì('.')
    try:
        기다리기()
        ṣiṣẹ́_àṣẹ('pip --help', 'MicroPython orísun_ètò_afigijúwe 설치기')
        fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        ṣiṣẹ́_àṣẹ('python 오류시험.py', '한국어 Fáìlì 예외 ridájú')
        ṣiṣẹ́_àṣẹ('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'ṣàgbékalẹ̀_iye 완료: micropython-bisect 3.3.3')
        ṣiṣẹ́_àṣẹ('python -c \'from bisect import insort as 순서대로넣기; iye=[1,5]; 순서대로넣기(iye,3); print(iye)\'', '[1, 3, 5]')
        ṣiṣẹ́_àṣẹ('python -m pip list', 'micropython-bisect 3.3.3')
        ṣiṣẹ́_àṣẹ('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        ṣiṣẹ́_àṣẹ('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'ṣàgbékalẹ̀_iye 완료: jkoros-fixture')
        ṣiṣẹ́_àṣẹ('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ṣiṣẹ́_àṣẹ('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'àkópọ̀ àṣìṣe:', 1)
        ṣiṣẹ́_àṣẹ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 àṣìṣe 보존")\'', '구문 àṣìṣe 보존')
        fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ṣiṣẹ́_àṣẹ('python 공간시험.py '+str(접속번호), 'àkópọ̀ 공간 부족 되돌림 ridájú')
        ṣiṣẹ́_àṣẹ('pip uninstall jkoros-fixture', 'ṣèmúkúro_ìgbéwọlé 완료: jkoros-fixture')
        ṣiṣẹ́_àṣẹ('pip uninstall micropython-bisect', 'ṣèmúkúro_ìgbéwọlé 완료: micropython-bisect')
        ṣiṣẹ́_àṣẹ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ṣèmúkúro_ìgbéwọlé ridájú")\'', 'ṣèmúkúro_ìgbéwọlé ridájú')
        ìfọwọ́síìwé['passed'] = True
        print('PASS: PyPI 실물 ṣàgbékalẹ̀_iye·import·ṣiṣẹ́_àṣẹ, 한국어 예외, 패키지 àkójọpọ̀_fáìlì_iye, ìkùnà_iye 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 jáde_àtòjọ_ètò 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Ìlànà.stdin.write(b'\x01x')
            Ìlànà.stdin.flush()
            Ìlànà.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Ìlànà.terminate()
            try:
                Ìlànà.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Ìlànà.kill()
                Ìlànà.wait()
        if Ìlànà.poll() is None:
            Ìlànà.kill()
            Ìlànà.wait()
        olùyàn_a916db4e.close()
        Ìlànà.stdin.close()
        Ìlànà.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(ìfọwọ́síìwé, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Rọ́ọ̀nù()
