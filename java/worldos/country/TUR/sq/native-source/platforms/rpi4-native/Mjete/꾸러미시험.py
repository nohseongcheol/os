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
from 꾸러미중계 import grupoj_depo, 압축풀기
from zbatoj_komandë import Project_rrënjë


def 시험휠(Emër, 파일들, punë_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    të_dhëna = io.BytesIO()
    with zipfile.ZipFile(të_dhëna, 'w', zipfile.ZIP_DEFLATED) as grupoj:
        grupoj.writestr(Emër + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + punë_VALUE)
        grupoj.writestr(Emër + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Emër + '\nVersion: 1.0\n' + 의존성)
        for POZICIONI, Përmbajtje_VALUE in 파일들.items():
            grupoj.writestr(POZICIONI, Përmbajtje_VALUE)
    return të_dhëna.getvalue()


def çek_pritës():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for të_dhëna in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', të_dhëna, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel POZICIONI·Madhësi·C shtesë_VALUE·의존성 refuzo_VALUE')


def bosh_numri_i_portës():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Ekzekuto():
    analizues_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizues_48ee4b1b.add_argument('--host-only', action='store_true')
    Argumente = analizues_48ee4b1b.parse_args()
    çek_pritës()
    if Argumente.host_only:
        return
    llogaritje_shteg = Project_rrënjë/'build/verification/pip'
    llogaritje_shteg.mkdir(parents=True, exist_ok=True)
    hapësira_ruajtëse_shteg = llogaritje_shteg/'cache'
    hapësira_ruajtëse_shteg.mkdir(exist_ok=True)
    # aktual_të_dhëna PyPI 배포 Kartelë. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    grupoj_depo(Project_rrënjë/'build/pip-cache').Përgatit('micropython-bisect==3.3.3')
    for bishti_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(Project_rrënjë/'build/pip-cache'/('micropython-bisect==3.3.3'+bishti_VALUE)), str(hapësira_ruajtëse_shteg/('micropython-bisect==3.3.3'+bishti_VALUE)))
    실물기록 = json.loads((hapësira_ruajtëse_shteg/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Emër, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        të_dhëna = 시험휠(Emër, 파일들)
        (hapësira_ruajtëse_shteg/(Emër+'==1.0.archive')).write_bytes(të_dhëna)
        (hapësira_ruajtëse_shteg/(Emër+'==1.0.json')).write_text(json.dumps({'name': Emër, 'version': '1.0',
            'filename': Emër.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(të_dhëna).hexdigest()}))
    vlerësoj = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    numri_i_portës = bosh_numri_i_portës()
    Proçes = subprocess.Popen(['python3', str(Project_rrënjë/'Mjete/zbatoj_komandë.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(numri_i_portës), '--pip-cache', str(hapësira_ruajtëse_shteg), '--ftp-port', str(bosh_numri_i_portës())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    përzgjedhësi_a916db4e = selectors.DefaultSelector()
    përzgjedhësi_a916db4e.register(Proçes.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(shfaq_VALUE=b'jkoros-native> '):
        Përmbajtje_VALUE = bytearray()
        끝 = time.monotonic()+120
        while shfaq_VALUE not in Përmbajtje_VALUE:
            if time.monotonic() > 끝 or Proçes.poll() is not None:
                raise AssertionError('게스트 replikë 없음: '+Përmbajtje_VALUE.decode('utf-8','replace'))
            for futje_VALUE, _ in përzgjedhësi_a916db4e.select(.1):
                조각 = futje_VALUE.fileobj.read(4096)
                Përmbajtje_VALUE.extend(조각)
                대화기록.extend(조각)
        return Përmbajtje_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def pasues(Komanda, shfaq_VALUE=b'jkoros-native> '):
        Proçes.stdin.write(Komanda.encode()+b'\n')
        Proçes.stdin.flush()
        return 기다리기(shfaq_VALUE)
    def zbatoj_komandë(Komanda, 예상, status_VALUE=0):
        Përmbajtje_VALUE = pasues(Komanda)
        assert 예상 in Përmbajtje_VALUE and '\nexit '+str(status_VALUE)+'\n' in Përmbajtje_VALUE, Përmbajtje_VALUE
        vlerësoj['checks'].append(Komanda)
        return Përmbajtje_VALUE
    def Ngarkim_Skedarët(Emër, të_dhëna):
        pasues('load '+Emër, b'hex> ')
        for pozicioni_INDEX in range(0, len(të_dhëna), 64):
            pasues(të_dhëna[pozicioni_INDEX:pozicioni_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in pasues('.')
    try:
        기다리기()
        zbatoj_komandë('pip --help', 'MicroPython burim_degëzim 설치기')
        Ngarkim_Skedarët('오류시험.py', (Project_rrënjë/'시험/PYTHON/한국어오류시험.py').read_bytes())
        zbatoj_komandë('python 오류시험.py', '한국어 Kartelë përjashtim verifikoj')
        zbatoj_komandë('pip install micropython-bisect==3.3.3 --port '+str(numri_i_portës), 'instaloj_VALUE 완료: micropython-bisect 3.3.3')
        zbatoj_komandë('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        zbatoj_komandë('python -m pip list', 'micropython-bisect 3.3.3')
        zbatoj_komandë('pip install micropython-bisect==3.3.3 --port '+str(numri_i_portës), '이미 설치됨:')
        zbatoj_komandë('pip install jkoros-fixture==1.0 --port '+str(numri_i_portës), 'instaloj_VALUE 완료: jkoros-fixture')
        zbatoj_komandë('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        zbatoj_komandë('pip install jkoros-syntax==1.0 --port '+str(numri_i_portës), 'grupoj GABIM:', 1)
        zbatoj_komandë('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 GABIM 보존")\'', '구문 GABIM 보존')
        Ngarkim_Skedarët('공간시험.py', (Project_rrënjë/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        zbatoj_komandë('python 공간시험.py '+str(numri_i_portës), 'grupoj 공간 부족 Kthe_urë verifikoj')
        zbatoj_komandë('pip uninstall jkoros-fixture', 'heq_futje 완료: jkoros-fixture')
        zbatoj_komandë('pip uninstall micropython-bisect', 'heq_futje 완료: micropython-bisect')
        zbatoj_komandë('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("heq_futje verifikoj")\'', 'heq_futje verifikoj')
        vlerësoj['passed'] = True
        print('PASS: PyPI 실물 instaloj_VALUE·import·zbatoj_komandë, 한국어 përjashtim, 패키지 direktori_VALUE, dështim_VALUE Kthe_urë, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 dal_program 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Proçes.stdin.write(b'\x01x')
            Proçes.stdin.flush()
            Proçes.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Proçes.terminate()
            try:
                Proçes.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Proçes.kill()
                Proçes.wait()
        if Proçes.poll() is None:
            Proçes.kill()
            Proçes.wait()
        përzgjedhësi_a916db4e.close()
        Proçes.stdin.close()
        Proçes.stdout.close()
        (llogaritje_shteg/'serial.log').write_bytes(대화기록)
        (llogaritje_shteg/'report.json').write_text(json.dumps(vlerësoj, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Ekzekuto()
