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
from ተግብር_ትእዛዝ import 기준


def 시험휠(ሽም, 파일들, ዕዮ_ዋጋ_102996da='Root-Is-Purelib: true\n', 의존성=''):
    ሓበሬታ = io.BytesIO()
    with zipfile.ZipFile(ሓበሬታ, 'w', zipfile.ZIP_DEFLATED) as ጥማር:
        ጥማር.writestr(ሽም + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ዕዮ_ዋጋ_102996da)
        ጥማር.writestr(ሽም + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ሽም + '\nVersion: 1.0\n' + 의존성)
        for መገዲ, ትሕዝቶ_ዋጋ in 파일들.items():
            ጥማር.writestr(መገዲ, ትሕዝቶ_ዋጋ)
    return ሓበሬታ.getvalue()


def ፈትሽ_አዐንግድ():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'ዋጋ=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'ዋጋ=42\n'.encode()}
    for ሓበሬታ in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ሓበሬታ, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel መገዲ·መጠን·C ቅጥያ_ዋጋ·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ኣኺድ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    ፈትሽ_አዐንግድ()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    መኽዘን_መገዲ = 결과경로/'cache'
    መኽዘን_መገዲ.mkdir(exist_ok=True)
    # ትኽክለኛ_ሓበሬታ PyPI 배포 ፋይል. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').ኣዳልው('micropython-bisect==3.3.3')
    for ጭራ_ዋጋ in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+ጭራ_ዋጋ)), str(መኽዘን_መገዲ/('micropython-bisect==3.3.3'+ጭራ_ዋጋ)))
    ሃርድዌር_ምዝጉብ = json.loads((መኽዘን_መገዲ/'micropython-bisect==3.3.3.json').read_text())
    assert ሃርድዌር_ምዝጉብ['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ሽም, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'ዋጋ=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ሓበሬታ = 시험휠(ሽም, 파일들)
        (መኽዘን_መገዲ/(ሽም+'==1.0.archive')).write_bytes(ሓበሬታ)
        (መኽዘን_መገዲ/(ሽም+'==1.0.json')).write_text(json.dumps({'name': ሽም, 'version': '1.0',
            'filename': ሽም.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ሓበሬታ).hexdigest()}))
    አረጋግፅ = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': ሃርድዌር_ምዝጉብ, 'checks': []}
    접속번호 = 빈접속번호()
    መስርሕ = subprocess.Popen(['python3', str(기준/'መሳርሒታት/ተግብር_ትእዛዝ.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(መኽዘን_መገዲ), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    መራፂ_a916db4e = selectors.DefaultSelector()
    መራፂ_a916db4e.register(መስርሕ.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(ኣርእይ_ዋጋ=b'jkoros-native> '):
        ትሕዝቶ_ዋጋ = bytearray()
        끝 = time.monotonic()+120
        while ኣርእይ_ዋጋ not in ትሕዝቶ_ዋጋ:
            if time.monotonic() > 끝 or መስርሕ.poll() is not None:
                raise AssertionError('게스트 መልስ 없음: '+ትሕዝቶ_ዋጋ.decode('utf-8','replace'))
            for ምእታው_ዋጋ, _ in መራፂ_a916db4e.select(.1):
                조각 = ምእታው_ዋጋ.fileobj.read(4096)
                ትሕዝቶ_ዋጋ.extend(조각)
                대화기록.extend(조각)
        return ትሕዝቶ_ዋጋ.decode('utf-8', 'replace').replace('\r\n','\n')
    def ሽፋን(ትእዛዝ, ኣርእይ_ዋጋ=b'jkoros-native> '):
        መስርሕ.stdin.write(ትእዛዝ.encode()+b'\n')
        መስርሕ.stdin.flush()
        return 기다리기(ኣርእይ_ዋጋ)
    def ተግብር_ትእዛዝ(ትእዛዝ, 예상, ደረጃ_ዋጋ=0):
        ትሕዝቶ_ዋጋ = ሽፋን(ትእዛዝ)
        assert 예상 in ትሕዝቶ_ዋጋ and '\nexit '+str(ደረጃ_ዋጋ)+'\n' in ትሕዝቶ_ዋጋ, ትሕዝቶ_ዋጋ
        አረጋግፅ['checks'].append(ትእዛዝ)
        return ትሕዝቶ_ዋጋ
    def ስቐል_ፋይላት(ሽም, ሓበሬታ):
        ሽፋን('load '+ሽም, b'hex> ')
        for 자리 in range(0, len(ሓበሬታ), 64):
            ሽፋን(ሓበሬታ[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in ሽፋን('.')
    try:
        기다리기()
        ተግብር_ትእዛዝ('pip --help', 'MicroPython ምንጪ_ገረብ 설치기')
        ስቐል_ፋይላት('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        ተግብር_ትእዛዝ('python 오류시험.py', 'ትግርኛ ፋይል 예외 ኣረጋግጽ')
        ተግብር_ትእዛዝ('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'ጸዓን_ዋጋ 완료: micropython-bisect 3.3.3')
        ተግብር_ትእዛዝ('python -c \'from bisect import insort as 순서대로넣기; ዋጋ=[1,5]; 순서대로넣기(ዋጋ,3); print(ዋጋ)\'', '[1, 3, 5]')
        ተግብር_ትእዛዝ('python -m pip list', 'micropython-bisect 3.3.3')
        ተግብር_ትእዛዝ('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        ተግብር_ትእዛዝ('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'ጸዓን_ዋጋ 완료: jkoros-fixture')
        ተግብር_ትእዛዝ('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ተግብር_ትእዛዝ('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'ጥማር ጌጋ:', 1)
        ተግብር_ትእዛዝ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ጌጋ 보존")\'', '구문 ጌጋ 보존')
        ስቐል_ፋይላት('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ተግብር_ትእዛዝ('python 공간시험.py '+str(접속번호), 'ጥማር 공간 부족 되돌림 ኣረጋግጽ')
        ተግብር_ትእዛዝ('pip uninstall jkoros-fixture', 'ኣልግስ_ምእታው 완료: jkoros-fixture')
        ተግብር_ትእዛዝ('pip uninstall micropython-bisect', 'ኣልግስ_ምእታው 완료: micropython-bisect')
        ተግብር_ትእዛዝ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ኣልግስ_ምእታው ኣረጋግጽ")\'', 'ኣልግስ_ምእታው ኣረጋግጽ')
        አረጋግፅ['passed'] = True
        print('PASS: PyPI 실물 ጸዓን_ዋጋ·import·ተግብር_ትእዛዝ, ትግርኛ 예외, 패키지 ሓባሪ_ማህደር_ዋጋ, ፍሽለት_ዋጋ 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 ውጻእ_መተግበሪ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            መስርሕ.stdin.write(b'\x01x')
            መስርሕ.stdin.flush()
            መስርሕ.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            መስርሕ.terminate()
            try:
                መስርሕ.wait(timeout=8)
            except subprocess.TimeoutExpired:
                መስርሕ.kill()
                መስርሕ.wait()
        if መስርሕ.poll() is None:
            መስርሕ.kill()
            መስርሕ.wait()
        መራፂ_a916db4e.close()
        መስርሕ.stdin.close()
        መስርሕ.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(አረጋግፅ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ኣኺድ()
