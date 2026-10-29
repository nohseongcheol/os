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
from 꾸러미중계 import dami_matattara, 압축풀기
from gudanar_Umarni import 기준


def 시험휠(Suna, 파일들, Kes_Daraja='Root-Is-Purelib: true\n', 의존성=''):
    Tarin_bayani = io.BytesIO()
    with zipfile.ZipFile(Tarin_bayani, 'w', zipfile.ZIP_DEFLATED) as dami:
        dami.writestr(Suna + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + Kes_Daraja)
        dami.writestr(Suna + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Suna + '\nVersion: 1.0\n' + 의존성)
        for Hanyar_shiga, kunshiya_Daraja in 파일들.items():
            dami.writestr(Hanyar_shiga, kunshiya_Daraja)
    return Tarin_bayani.getvalue()


def Bincika_sauka():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'Daraja=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'Daraja=42\n'.encode()}
    for Tarin_bayani in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', Tarin_bayani, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Hanyar_shiga·Girma·C faɗi_Daraja·의존성 kore_Daraja')


def holoko_lambar_kafa():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Tafiyar_da():
    tatsar_manhaja_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    tatsar_manhaja_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = tatsar_manhaja_48ee4b1b.parse_args()
    Bincika_sauka()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Wurin_adana_Hanyar_shiga = 결과경로/'cache'
    Wurin_adana_Hanyar_shiga.mkdir(exist_ok=True)
    # Na_hakika_Tarin_bayani PyPI 배포 Fayil. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    dami_matattara(기준/'build/pip-cache').Shirya('micropython-bisect==3.3.3')
    for na_karshe_Daraja in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+na_karshe_Daraja)), str(Wurin_adana_Hanyar_shiga/('micropython-bisect==3.3.3'+na_karshe_Daraja)))
    kayan_haɗi_na_kwamfuta_logu = json.loads((Wurin_adana_Hanyar_shiga/'micropython-bisect==3.3.3.json').read_text())
    assert kayan_haɗi_na_kwamfuta_logu['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Suna, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'Daraja=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        Tarin_bayani = 시험휠(Suna, 파일들)
        (Wurin_adana_Hanyar_shiga/(Suna+'==1.0.archive')).write_bytes(Tarin_bayani)
        (Wurin_adana_Hanyar_shiga/(Suna+'==1.0.json')).write_text(json.dumps({'name': Suna, 'version': '1.0',
            'filename': Suna.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(Tarin_bayani).hexdigest()}))
    inganta = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': kayan_haɗi_na_kwamfuta_logu, 'checks': []}
    lambar_kafa = holoko_lambar_kafa()
    haryar_aikin_na_ura = subprocess.Popen(['python3', str(기준/'Kaya/gudanar_Umarni.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(lambar_kafa), '--pip-cache', str(Wurin_adana_Hanyar_shiga), '--ftp-port', str(holoko_lambar_kafa())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    mai_zabe_a916db4e = selectors.DefaultSelector()
    mai_zabe_a916db4e.register(haryar_aikin_na_ura.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(Nuna_Daraja=b'jkoros-native> '):
        kunshiya_Daraja = bytearray()
        끝 = time.monotonic()+120
        while Nuna_Daraja not in kunshiya_Daraja:
            if time.monotonic() > 끝 or haryar_aikin_na_ura.poll() is not None:
                raise AssertionError('게스트 mayar_da_martani 없음: '+kunshiya_Daraja.decode('utf-8','replace'))
            for Mashigar_bayanai_Daraja, _ in mai_zabe_a916db4e.select(.1):
                조각 = Mashigar_bayanai_Daraja.fileobj.read(4096)
                kunshiya_Daraja.extend(조각)
                대화기록.extend(조각)
        return kunshiya_Daraja.decode('utf-8', 'replace').replace('\r\n','\n')
    def Mai_fayyace_umani(Umarni, Nuna_Daraja=b'jkoros-native> '):
        haryar_aikin_na_ura.stdin.write(Umarni.encode()+b'\n')
        haryar_aikin_na_ura.stdin.flush()
        return 기다리기(Nuna_Daraja)
    def gudanar_Umarni(Umarni, 예상, Matsayi_Daraja=0):
        kunshiya_Daraja = Mai_fayyace_umani(Umarni)
        assert 예상 in kunshiya_Daraja and '\nexit '+str(Matsayi_Daraja)+'\n' in kunshiya_Daraja, kunshiya_Daraja
        inganta['checks'].append(Umarni)
        return kunshiya_Daraja
    def lodawa_Fayiloli(Suna, Tarin_bayani):
        Mai_fayyace_umani('load '+Suna, b'hex> ')
        for 자리 in range(0, len(Tarin_bayani), 64):
            Mai_fayyace_umani(Tarin_bayani[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in Mai_fayyace_umani('.')
    try:
        기다리기()
        gudanar_Umarni('pip --help', 'MicroPython tushe_Li_irabin_tarin_bayanai 설치기')
        lodawa_Fayiloli('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        gudanar_Umarni('python 오류시험.py', '한국어 Fayil banbanchi Tabbatar_da')
        gudanar_Umarni('pip install micropython-bisect==3.3.3 --port '+str(lambar_kafa), 'Girka_Daraja 완료: micropython-bisect 3.3.3')
        gudanar_Umarni('python -c \'from bisect import insort as 순서대로넣기; Daraja=[1,5]; 순서대로넣기(Daraja,3); print(Daraja)\'', '[1, 3, 5]')
        gudanar_Umarni('python -m pip list', 'micropython-bisect 3.3.3')
        gudanar_Umarni('pip install micropython-bisect==3.3.3 --port '+str(lambar_kafa), '이미 설치됨:')
        gudanar_Umarni('pip install jkoros-fixture==1.0 --port '+str(lambar_kafa), 'Girka_Daraja 완료: jkoros-fixture')
        gudanar_Umarni('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        gudanar_Umarni('pip install jkoros-syntax==1.0 --port '+str(lambar_kafa), 'dami Kuskure:', 1)
        gudanar_Umarni('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Kuskure 보존")\'', '구문 Kuskure 보존')
        lodawa_Fayiloli('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        gudanar_Umarni('python 공간시험.py '+str(lambar_kafa), 'dami 공간 부족 되돌림 Tabbatar_da')
        gudanar_Umarni('pip uninstall jkoros-fixture', 'Cire_Mashigar_bayanai 완료: jkoros-fixture')
        gudanar_Umarni('pip uninstall micropython-bisect', 'Cire_Mashigar_bayanai 완료: micropython-bisect')
        gudanar_Umarni('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("Cire_Mashigar_bayanai Tabbatar_da")\'', 'Cire_Mashigar_bayanai Tabbatar_da')
        inganta['passed'] = True
        print('PASS: PyPI 실물 Girka_Daraja·import·gudanar_Umarni, 한국어 banbanchi, 패키지 ma_ajiya_Daraja, Kasa_aiki_Daraja 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Mafita_Shiri 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            haryar_aikin_na_ura.stdin.write(b'\x01x')
            haryar_aikin_na_ura.stdin.flush()
            haryar_aikin_na_ura.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            haryar_aikin_na_ura.terminate()
            try:
                haryar_aikin_na_ura.wait(timeout=8)
            except subprocess.TimeoutExpired:
                haryar_aikin_na_ura.kill()
                haryar_aikin_na_ura.wait()
        if haryar_aikin_na_ura.poll() is None:
            haryar_aikin_na_ura.kill()
            haryar_aikin_na_ura.wait()
        mai_zabe_a916db4e.close()
        haryar_aikin_na_ura.stdin.close()
        haryar_aikin_na_ura.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(inganta, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Tafiyar_da()
