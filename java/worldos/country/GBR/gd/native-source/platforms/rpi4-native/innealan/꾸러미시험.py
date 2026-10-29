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
from gnìomhaich_àithne import tilg_freumh


def 시험휠(Ainm, 파일들, cùis_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    dàta = io.BytesIO()
    with zipfile.ZipFile(dàta, 'w', zipfile.ZIP_DEFLATED) as trusgan:
        trusgan.writestr(Ainm + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + cùis_VALUE)
        trusgan.writestr(Ainm + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Ainm + '\nVersion: 1.0\n' + 의존성)
        for Slighe, susbaint_VALUE in 파일들.items():
            trusgan.writestr(Slighe, susbaint_VALUE)
    return dàta.getvalue()


def seic_òstair():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for dàta in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', dàta, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Slighe·atharraich_am_meud·C leudachan_VALUE·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ruith():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    seic_òstair()
    if 인수.host_only:
        return
    tomhas_slighe = tilg_freumh/'build/verification/pip'
    tomhas_slighe.mkdir(parents=True, exist_ok=True)
    stòras_slighe = tomhas_slighe/'cache'
    stòras_slighe.mkdir(exist_ok=True)
    # dearbh_dàta PyPI 배포 faidhle. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(tilg_freumh/'build/pip-cache').Ullaich('micropython-bisect==3.3.3')
    for earball_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(tilg_freumh/'build/pip-cache'/('micropython-bisect==3.3.3'+earball_VALUE)), str(stòras_slighe/('micropython-bisect==3.3.3'+earball_VALUE)))
    실물기록 = json.loads((stòras_slighe/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Ainm, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        dàta = 시험휠(Ainm, 파일들)
        (stòras_slighe/(Ainm+'==1.0.archive')).write_bytes(dàta)
        (stòras_slighe/(Ainm+'==1.0.json')).write_text(json.dumps({'name': Ainm, 'version': '1.0',
            'filename': Ainm.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(dàta).hexdigest()}))
    dearbh_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Pròiseas = subprocess.Popen(['python3', str(tilg_freumh/'innealan/gnìomhaich_àithne.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(stòras_slighe), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    roghnaichear_a916db4e = selectors.DefaultSelector()
    roghnaichear_a916db4e.register(Pròiseas.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(show_VALUE=b'jkoros-native> '):
        susbaint_VALUE = bytearray()
        끝 = time.monotonic()+120
        while show_VALUE not in susbaint_VALUE:
            if time.monotonic() > 끝 or Pròiseas.poll() is not None:
                raise AssertionError('게스트 freagair 없음: '+susbaint_VALUE.decode('utf-8','replace'))
            for cur_a_steach_VALUE, _ in roghnaichear_a916db4e.select(.1):
                조각 = cur_a_steach_VALUE.fileobj.read(4096)
                susbaint_VALUE.extend(조각)
                대화기록.extend(조각)
        return susbaint_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def slige(àithne, show_VALUE=b'jkoros-native> '):
        Pròiseas.stdin.write(àithne.encode()+b'\n')
        Pròiseas.stdin.flush()
        return 기다리기(show_VALUE)
    def gnìomhaich_àithne(àithne, 예상, cor_VALUE=0):
        susbaint_VALUE = slige(àithne)
        assert 예상 in susbaint_VALUE and '\nexit '+str(cor_VALUE)+'\n' in susbaint_VALUE, susbaint_VALUE
        dearbh_5fb2b747['checks'].append(àithne)
        return susbaint_VALUE
    def luchdaich_suas_faidhlichean(Ainm, dàta):
        slige('load '+Ainm, b'hex> ')
        for suidhich_INDEX in range(0, len(dàta), 64):
            slige(dàta[suidhich_INDEX:suidhich_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in slige('.')
    try:
        기다리기()
        gnìomhaich_àithne('pip --help', 'MicroPython tùs_craobh 설치기')
        luchdaich_suas_faidhlichean('오류시험.py', (tilg_freumh/'시험/PYTHON/한국어오류시험.py').read_bytes())
        gnìomhaich_àithne('python 오류시험.py', '한국어 faidhle 예외 dearbh')
        gnìomhaich_àithne('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'stàlaich_VALUE 완료: micropython-bisect 3.3.3')
        gnìomhaich_àithne('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        gnìomhaich_àithne('python -m pip list', 'micropython-bisect 3.3.3')
        gnìomhaich_àithne('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        gnìomhaich_àithne('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'stàlaich_VALUE 완료: jkoros-fixture')
        gnìomhaich_àithne('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        gnìomhaich_àithne('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'trusgan Mearachd:', 1)
        gnìomhaich_àithne('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Mearachd 보존")\'', '구문 Mearachd 보존')
        luchdaich_suas_faidhlichean('공간시험.py', (tilg_freumh/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        gnìomhaich_àithne('python 공간시험.py '+str(접속번호), 'trusgan 공간 부족 return_drochaid dearbh')
        gnìomhaich_àithne('pip uninstall jkoros-fixture', 'thoir_air_falbh_cur_a_steach 완료: jkoros-fixture')
        gnìomhaich_àithne('pip uninstall micropython-bisect', 'thoir_air_falbh_cur_a_steach 완료: micropython-bisect')
        gnìomhaich_àithne('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("thoir_air_falbh_cur_a_steach dearbh")\'', 'thoir_air_falbh_cur_a_steach dearbh')
        dearbh_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 stàlaich_VALUE·import·gnìomhaich_àithne, 한국어 예외, 패키지 eòlaire_VALUE, fàilligeadh_VALUE return_drochaid, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 fàg_ap 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Pròiseas.stdin.write(b'\x01x')
            Pròiseas.stdin.flush()
            Pròiseas.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Pròiseas.terminate()
            try:
                Pròiseas.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Pròiseas.kill()
                Pròiseas.wait()
        if Pròiseas.poll() is None:
            Pròiseas.kill()
            Pròiseas.wait()
        roghnaichear_a916db4e.close()
        Pròiseas.stdin.close()
        Pròiseas.stdout.close()
        (tomhas_slighe/'serial.log').write_bytes(대화기록)
        (tomhas_slighe/'report.json').write_text(json.dumps(dearbh_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ruith()
