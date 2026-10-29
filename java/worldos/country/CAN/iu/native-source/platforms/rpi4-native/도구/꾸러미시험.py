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
from 실행 import 기준


def 시험휠(atiq, 파일들, pijatsaq_atuutilik='Root-Is-Purelib: true\n', 의존성=''):
    titiqqat = io.BytesIO()
    with zipfile.ZipFile(titiqqat, 'w', zipfile.ZIP_DEFLATED) as 꾸러미:
        꾸러미.writestr(atiq + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + pijatsaq_atuutilik)
        꾸러미.writestr(atiq + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + atiq + '\nVersion: 1.0\n' + 의존성)
        for aqqut, Ilulingit_atuutilik in 파일들.items():
            꾸러미.writestr(aqqut, Ilulingit_atuutilik)
    return titiqqat.getvalue()


def qaujigiarli_tuttarvik():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'atuutilik=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'atuutilik=42\n'.encode()}
    for titiqqat in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', titiqqat, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel aqqut·anininga·C uigu_atuutilik·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def 시작():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    qaujigiarli_tuttarvik()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    저장경로 = 결과경로/'cache'
    저장경로.mkdir(exist_ok=True)
    # taannallarik_titiqqat PyPI 배포 ini. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').Parnalli('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(저장경로/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((저장경로/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for atiq, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'atuutilik=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        titiqqat = 시험휠(atiq, 파일들)
        (저장경로/(atiq+'==1.0.archive')).write_bytes(titiqqat)
        (저장경로/(atiq+'==1.0.json')).write_text(json.dumps({'name': atiq, 'version': '1.0',
            'filename': atiq.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(titiqqat).hexdigest()}))
    naammannirarli = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Pivallianiq = subprocess.Popen(['python3', str(기준/'도구/실행.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(저장경로), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector()
    선택기.register(Pivallianiq.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(saqqilli_atuutilik=b'jkoros-native> '):
        Ilulingit_atuutilik = bytearray()
        끝 = time.monotonic()+120
        while saqqilli_atuutilik not in Ilulingit_atuutilik:
            if time.monotonic() > 끝 or Pivallianiq.poll() is not None:
                raise AssertionError('게스트 응답 없음: '+Ilulingit_atuutilik.decode('utf-8','replace'))
            for Iliniku_atuutilik, _ in 선택기.select(.1):
                조각 = Iliniku_atuutilik.fileobj.read(4096)
                Ilulingit_atuutilik.extend(조각)
                대화기록.extend(조각)
        return Ilulingit_atuutilik.decode('utf-8', 'replace').replace('\r\n','\n')
    def piqujijjutiliriji(piqujijjut, saqqilli_atuutilik=b'jkoros-native> '):
        Pivallianiq.stdin.write(piqujijjut.encode()+b'\n')
        Pivallianiq.stdin.flush()
        return 기다리기(saqqilli_atuutilik)
    def 실행(piqujijjut, 예상, qanuilinganiq_atuutilik=0):
        Ilulingit_atuutilik = piqujijjutiliriji(piqujijjut)
        assert 예상 in Ilulingit_atuutilik and '\nexit '+str(qanuilinganiq_atuutilik)+'\n' in Ilulingit_atuutilik, Ilulingit_atuutilik
        naammannirarli['checks'].append(piqujijjut)
        return Ilulingit_atuutilik
    def 올리기(atiq, titiqqat):
        piqujijjutiliriji('load '+atiq, b'hex> ')
        for 자리 in range(0, len(titiqqat), 64):
            piqujijjutiliriji(titiqqat[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in piqujijjutiliriji('.')
    try:
        기다리기()
        실행('pip --help', 'MicroPython pivviujuq_attavigiit 설치기')
        올리기('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        실행('python 오류시험.py', '한국어 ini 예외 nalunairli_1aacb54c')
        실행('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'ilili_atuutilik 완료: micropython-bisect 3.3.3')
        실행('python -c \'from bisect import insort as 순서대로넣기; atuutilik=[1,5]; 순서대로넣기(atuutilik,3); print(atuutilik)\'', '[1, 3, 5]')
        실행('python -m pip list', 'micropython-bisect 3.3.3')
        실행('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        실행('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'ilili_atuutilik 완료: jkoros-fixture')
        실행('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        실행('pip install jkoros-syntax==1.0 --port '+str(접속번호), '꾸러미 tammarniq:', 1)
        실행('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 tammarniq 보존")\'', '구문 tammarniq 보존')
        올리기('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        실행('python 공간시험.py '+str(접속번호), '꾸러미 공간 부족 되돌림 nalunairli_1aacb54c')
        실행('pip uninstall jkoros-fixture', 'sanirvalli_Iliniku 완료: jkoros-fixture')
        실행('pip uninstall micropython-bisect', 'sanirvalli_Iliniku 완료: micropython-bisect')
        실행('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("sanirvalli_Iliniku nalunairli_1aacb54c")\'', 'sanirvalli_Iliniku nalunairli_1aacb54c')
        naammannirarli['passed'] = True
        print('PASS: PyPI 실물 ilili_atuutilik·import·실행, 한국어 예외, 패키지 tukimuagutiit_atuutilik, itigaqtuq_atuutilik 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 taima_pilirijjut 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Pivallianiq.stdin.write(b'\x01x')
            Pivallianiq.stdin.flush()
            Pivallianiq.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Pivallianiq.terminate()
            try:
                Pivallianiq.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Pivallianiq.kill()
                Pivallianiq.wait()
        if Pivallianiq.poll() is None:
            Pivallianiq.kill()
            Pivallianiq.wait()
        선택기.close()
        Pivallianiq.stdin.close()
        Pivallianiq.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(naammannirarli, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    시작()
