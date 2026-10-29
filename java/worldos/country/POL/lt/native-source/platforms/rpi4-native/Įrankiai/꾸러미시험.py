#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 savas 커널에서 검사한다."""
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
from 꾸러미중계 import paketas_saugykla, išskleisti_794097ae
from Vykdyti_komanda import Project_šaknis


def 시험휠(Pavadinimas_2, 파일들, sutarties_vertė='Root-Is-Purelib: true\n', 의존성=''):
    duomenys = io.BytesIO()
    with zipfile.ZipFile(duomenys, 'w', zipfile.ZIP_DEFLATED) as paketas:
        paketas.writestr(Pavadinimas_2 + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + sutarties_vertė)
        paketas.writestr(Pavadinimas_2 + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Pavadinimas_2 + '\nVersion: 1.0\n' + 의존성)
        for KELIAS, Turinys_VALUE in 파일들.items():
            paketas.writestr(KELIAS, Turinys_VALUE)
    return duomenys.getvalue()


def čekis_organizuoti():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert išskleisti_794097ae('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for duomenys in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            išskleisti_794097ae('jkoros_fixture-1.0-py3-none-any.whl', duomenys, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel KELIAS·Dydis·C plėtinys_VALUE·의존성 atmesti_VALUE')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Paleisti():
    analizatorius_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatorius_48ee4b1b.add_argument('--host-only', action='store_true')
    Argumentai = analizatorius_48ee4b1b.parse_args()
    čekis_organizuoti()
    if Argumentai.host_only:
        return
    KR_kelias = Project_šaknis/'build/verification/pip'
    KR_kelias.mkdir(parents=True, exist_ok=True)
    Saugykla_kelias = KR_kelias/'cache'
    Saugykla_kelias.mkdir(exist_ok=True)
    # faktinis_duomenys PyPI paskirstymas_VALUE Failas. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    paketas_saugykla(Project_šaknis/'build/pip-cache').Parengti('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(Project_šaknis/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Saugykla_kelias/('micropython-bisect==3.3.3'+꼬리)))
    aparatūra_LOG = json.loads((Saugykla_kelias/'micropython-bisect==3.3.3.json').read_text())
    assert aparatūra_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Pavadinimas_2, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SECOND_operandas):\n return 가+SECOND_operandas\n'}),
            ('jkoros-space', {'space%d.py' % numeris: 'VALUE=1\n' for numeris in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        duomenys = 시험휠(Pavadinimas_2, 파일들)
        (Saugykla_kelias/(Pavadinimas_2+'==1.0.archive')).write_bytes(duomenys)
        (Saugykla_kelias/(Pavadinimas_2+'==1.0.json')).write_text(json.dumps({'name': Pavadinimas_2, 'version': '1.0',
            'filename': Pavadinimas_2.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(duomenys).hexdigest()}))
    tikrinti = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': aparatūra_LOG, 'checks': []}
    prievado_numeris = 빈접속번호()
    Procesas = subprocess.Popen(['python3', str(Project_šaknis/'Įrankiai/Vykdyti_komanda.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(prievado_numeris), '--pip-cache', str(Saugykla_kelias), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    išrinkiklis_a916db4e = selectors.DefaultSelector()
    išrinkiklis_a916db4e.register(Procesas.stdout, selectors.EVENT_READ)
    transkribavimas = bytearray()
    def 기다리기(laida_VALUE=b'jkoros-native> '):
        Turinys_VALUE = bytearray()
        끝 = time.monotonic()+120
        while laida_VALUE not in Turinys_VALUE:
            if time.monotonic() > 끝 or Procesas.poll() is not None:
                raise AssertionError('게스트 atsakyti 없음: '+Turinys_VALUE.decode('utf-8','replace'))
            for įrašas_VALUE, _ in išrinkiklis_a916db4e.select(.1):
                조각 = įrašas_VALUE.fileobj.read(4096)
                Turinys_VALUE.extend(조각)
                transkribavimas.extend(조각)
        return Turinys_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def apvalkalas(Komanda, laida_VALUE=b'jkoros-native> '):
        Procesas.stdin.write(Komanda.encode()+b'\n')
        Procesas.stdin.flush()
        return 기다리기(laida_VALUE)
    def Vykdyti_komanda(Komanda, 예상, Būsena_VALUE=0):
        Turinys_VALUE = apvalkalas(Komanda)
        assert 예상 in Turinys_VALUE and '\nexit '+str(Būsena_VALUE)+'\n' in Turinys_VALUE, Turinys_VALUE
        tikrinti['checks'].append(Komanda)
        return Turinys_VALUE
    def Upload_Failai(Pavadinimas_2, duomenys):
        apvalkalas('load '+Pavadinimas_2, b'hex> ')
        for vietos_rodyklė in range(0, len(duomenys), 64):
            apvalkalas(duomenys[vietos_rodyklė:vietos_rodyklė+64].hex(), b'hex> ')
        assert 'LOADED' in apvalkalas('.')
    try:
        기다리기()
        Vykdyti_komanda('pip --help', 'MicroPython šaltinis_medis 설치기')
        Upload_Failai('오류시험.py', (Project_šaknis/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Vykdyti_komanda('python 오류시험.py', 'Lietuvių Failas išimtis patvirtinti')
        Vykdyti_komanda('pip install micropython-bisect==3.3.3 --port '+str(prievado_numeris), 'diegti_VALUE 완료: micropython-bisect 3.3.3')
        Vykdyti_komanda('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Vykdyti_komanda('python -m pip list', 'micropython-bisect 3.3.3')
        Vykdyti_komanda('pip install micropython-bisect==3.3.3 --port '+str(prievado_numeris), '이미 설치됨:')
        Vykdyti_komanda('pip install jkoros-fixture==1.0 --port '+str(prievado_numeris), 'diegti_VALUE 완료: jkoros-fixture')
        Vykdyti_komanda('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Vykdyti_komanda('pip install jkoros-syntax==1.0 --port '+str(prievado_numeris), 'paketas KLAIDA:', 1)
        Vykdyti_komanda('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 KLAIDA 보존")\'', '구문 KLAIDA 보존')
        Upload_Failai('공간시험.py', (Project_šaknis/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Vykdyti_komanda('python 공간시험.py '+str(prievado_numeris), 'paketas ADDRESS_sritis 부족 grąžinti_tiltas patvirtinti')
        Vykdyti_komanda('pip uninstall jkoros-fixture', 'pašalinti_įrašas 완료: jkoros-fixture')
        Vykdyti_komanda('pip uninstall micropython-bisect', 'pašalinti_įrašas 완료: micropython-bisect')
        Vykdyti_komanda('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("pašalinti_įrašas patvirtinti")\'', 'pašalinti_įrašas patvirtinti')
        tikrinti['passed'] = True
        print('PASS: PyPI 실물 diegti_VALUE·import·Vykdyti_komanda, Lietuvių išimtis, 패키지 Katalogas_VALUE, triktis_VALUE grąžinti_tiltas, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Baigti_programa_086bb533 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Procesas.stdin.write(b'\x01x')
            Procesas.stdin.flush()
            Procesas.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Procesas.terminate()
            try:
                Procesas.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Procesas.kill()
                Procesas.wait()
        if Procesas.poll() is None:
            Procesas.kill()
            Procesas.wait()
        išrinkiklis_a916db4e.close()
        Procesas.stdin.close()
        Procesas.stdout.close()
        (KR_kelias/'serial.log').write_bytes(transkribavimas)
        (KR_kelias/'report.json').write_text(json.dumps(tikrinti, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Paleisti()
