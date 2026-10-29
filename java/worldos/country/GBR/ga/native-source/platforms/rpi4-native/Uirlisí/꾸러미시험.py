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
from Rith_ordú import teilgean_fréamh


def 시험휠(Ainm, 파일들, cás_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    sonraí = io.BytesIO()
    with zipfile.ZipFile(sonraí, 'w', zipfile.ZIP_DEFLATED) as beart:
        beart.writestr(Ainm + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + cás_VALUE)
        beart.writestr(Ainm + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Ainm + '\nVersion: 1.0\n' + 의존성)
        for CONAIR, Inneachar_VALUE in 파일들.items():
            beart.writestr(CONAIR, Inneachar_VALUE)
    return sonraí.getvalue()


def seic_óstach():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for sonraí in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', sonraí, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel CONAIR·Méid·C breisiú_VALUE·의존성 diúltaigh_VALUE')


def folamh_uimhir_phoirt():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Rith_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    Argóintí = 해석기.parse_args()
    seic_óstach()
    if Argóintí.host_only:
        return
    tomhas_cosán = teilgean_fréamh/'build/verification/pip'
    tomhas_cosán.mkdir(parents=True, exist_ok=True)
    Stóras_cosán = tomhas_cosán/'cache'
    Stóras_cosán.mkdir(exist_ok=True)
    # iarbhír_sonraí PyPI 배포 Comhad. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(teilgean_fréamh/'build/pip-cache').Ullmhaigh('micropython-bisect==3.3.3')
    for earr_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(teilgean_fréamh/'build/pip-cache'/('micropython-bisect==3.3.3'+earr_VALUE)), str(Stóras_cosán/('micropython-bisect==3.3.3'+earr_VALUE)))
    실물기록 = json.loads((Stóras_cosán/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Ainm, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        sonraí = 시험휠(Ainm, 파일들)
        (Stóras_cosán/(Ainm+'==1.0.archive')).write_bytes(sonraí)
        (Stóras_cosán/(Ainm+'==1.0.json')).write_text(json.dumps({'name': Ainm, 'version': '1.0',
            'filename': Ainm.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(sonraí).hexdigest()}))
    bailíochtaigh = {'passed': False, 'kernel_sha256': hashlib.sha256((teilgean_fréamh/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    uimhir_phoirt = folamh_uimhir_phoirt()
    Próiseas = subprocess.Popen(['python3', str(teilgean_fréamh/'Uirlisí/Rith_ordú.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(uimhir_phoirt), '--pip-cache', str(Stóras_cosán), '--ftp-port', str(folamh_uimhir_phoirt())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    roghnóir_a916db4e = selectors.DefaultSelector()
    roghnóir_a916db4e.register(Próiseas.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(seó_VALUE=b'jkoros-native> '):
        Inneachar_VALUE = bytearray()
        끝 = time.monotonic()+120
        while seó_VALUE not in Inneachar_VALUE:
            if time.monotonic() > 끝 or Próiseas.poll() is not None:
                raise AssertionError('게스트 freagair 없음: '+Inneachar_VALUE.decode('utf-8','replace'))
            for iontráil_VALUE, _ in roghnóir_a916db4e.select(.1):
                조각 = iontráil_VALUE.fileobj.read(4096)
                Inneachar_VALUE.extend(조각)
                대화기록.extend(조각)
        return Inneachar_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def blaosc(Ordú, seó_VALUE=b'jkoros-native> '):
        Próiseas.stdin.write(Ordú.encode()+b'\n')
        Próiseas.stdin.flush()
        return 기다리기(seó_VALUE)
    def Rith_ordú(Ordú, 예상, staid_VALUE=0):
        Inneachar_VALUE = blaosc(Ordú)
        assert 예상 in Inneachar_VALUE and '\nexit '+str(staid_VALUE)+'\n' in Inneachar_VALUE, Inneachar_VALUE
        bailíochtaigh['checks'].append(Ordú)
        return Inneachar_VALUE
    def uaslódáil_Comhaid(Ainm, sonraí):
        blaosc('load '+Ainm, b'hex> ')
        for suíomh_INDEX in range(0, len(sonraí), 64):
            blaosc(sonraí[suíomh_INDEX:suíomh_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in blaosc('.')
    try:
        기다리기()
        Rith_ordú('pip --help', 'MicroPython foinse_crann 설치기')
        uaslódáil_Comhaid('오류시험.py', (teilgean_fréamh/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Rith_ordú('python 오류시험.py', 'Gaeilge Comhad eisceacht fíoraigh')
        Rith_ordú('pip install micropython-bisect==3.3.3 --port '+str(uimhir_phoirt), 'suiteáil_VALUE 완료: micropython-bisect 3.3.3')
        Rith_ordú('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Rith_ordú('python -m pip list', 'micropython-bisect 3.3.3')
        Rith_ordú('pip install micropython-bisect==3.3.3 --port '+str(uimhir_phoirt), '이미 설치됨:')
        Rith_ordú('pip install jkoros-fixture==1.0 --port '+str(uimhir_phoirt), 'suiteáil_VALUE 완료: jkoros-fixture')
        Rith_ordú('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Rith_ordú('pip install jkoros-syntax==1.0 --port '+str(uimhir_phoirt), 'beart ERREÁID:', 1)
        Rith_ordú('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ERREÁID 보존")\'', '구문 ERREÁID 보존')
        uaslódáil_Comhaid('공간시험.py', (teilgean_fréamh/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Rith_ordú('python 공간시험.py '+str(uimhir_phoirt), 'beart 공간 부족 return_traschóiritheoir fíoraigh')
        Rith_ordú('pip uninstall jkoros-fixture', 'bain_iontráil 완료: jkoros-fixture')
        Rith_ordú('pip uninstall micropython-bisect', 'bain_iontráil 완료: micropython-bisect')
        Rith_ordú('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("bain_iontráil fíoraigh")\'', 'bain_iontráil fíoraigh')
        bailíochtaigh['passed'] = True
        print('PASS: PyPI 실물 suiteáil_VALUE·import·Rith_ordú, Gaeilge eisceacht, 패키지 eolaire_VALUE, teip_VALUE return_traschóiritheoir, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 scoir_clár 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Próiseas.stdin.write(b'\x01x')
            Próiseas.stdin.flush()
            Próiseas.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Próiseas.terminate()
            try:
                Próiseas.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Próiseas.kill()
                Próiseas.wait()
        if Próiseas.poll() is None:
            Próiseas.kill()
            Próiseas.wait()
        roghnóir_a916db4e.close()
        Próiseas.stdin.close()
        Próiseas.stdout.close()
        (tomhas_cosán/'serial.log').write_bytes(대화기록)
        (tomhas_cosán/'report.json').write_text(json.dumps(bailíochtaigh, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Rith_2()
