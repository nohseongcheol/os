#!/usr/bin/env python3
"""PyPI fisico_hardware 배포와 부정 input_VALORE·RAM 되돌림을 nativo 커널에서 검사한다."""
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
from aggregare_Inoltro import aggregare_archivio, decomprimere
from Esegui_comando import azione_radice


def test_rotella(Nome, 파일들, valore_di_contratto='Root-Is-Purelib: true\n', 의존성=''):
    dati = io.BytesIO()
    with zipfile.ZipFile(dati, 'w', zipfile.ZIP_DEFLATED) as aggregare:
        aggregare.writestr(Nome + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + valore_di_contratto)
        aggregare.writestr(Nome + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nome + '\nVersion: 1.0\n' + 의존성)
        for percorso, Contenuto_VALORE in 파일들.items():
            aggregare.writestr(percorso, Contenuto_VALORE)
    return dati.getvalue()


def assegno_host():
    reparto_IT_normale = test_rotella('jkoros-fixture', {'mod.py': 'VALORE=42\n'})
    assert decomprimere('jkoros_fixture-1.0-py3-none-any.whl', reparto_IT_normale, 'jkoros-fixture', '1.0') == {'mod.py': 'VALORE=42\n'.encode()}
    for dati in (
            test_rotella('jkoros-fixture', {'../escape.py': ''}),
            test_rotella('jkoros-fixture', {'/abs.py': ''}),
            test_rotella('jkoros-fixture', {'big.py': 'x' * 16385}),
            test_rotella('jkoros-fixture', {'mod.so': ''}),
            test_rotella('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            test_rotella('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            decomprimere('jkoros_fixture-1.0-py3-none-any.whl', dati, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel percorso·Dimensione·C estensione_VALORE·의존성 rifiutare_VALORE')


def vuota_numero_di_porta():
    with socket.socket() as socket_VALORE:
        socket_VALORE.bind(('127.0.0.1', 0))
        return socket_VALORE.getsockname()[1]


def avvia():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--host-only', action='store_true')
    argomenti = parser_48ee4b1b.parse_args()
    assegno_host()
    if argomenti.host_only:
        return
    KR_percorso = azione_radice/'build/verification/pip'
    KR_percorso.mkdir(parents=True, exist_ok=True)
    Memoria_percorso = KR_percorso/'cache'
    Memoria_percorso.mkdir(exist_ok=True)
    # effettivo_dati PyPI distribuzione_VALORE file. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    aggregare_archivio(azione_radice/'build/pip-cache').Prepara('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(azione_radice/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Memoria_percorso/('micropython-bisect==3.3.3'+꼬리)))
    hardware_LOG = json.loads((Memoria_percorso/'micropython-bisect==3.3.3.json').read_text())
    assert hardware_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nome, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SECONDO_operando):\n return 가+SECONDO_operando\n'}),
            ('jkoros-space', {'space%d.py' % numero: 'VALORE=1\n' for numero in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        dati = test_rotella(Nome, 파일들)
        (Memoria_percorso/(Nome+'==1.0.archive')).write_bytes(dati)
        (Memoria_percorso/(Nome+'==1.0.json')).write_text(json.dumps({'name': Nome, 'version': '1.0',
            'filename': Nome.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(dati).hexdigest()}))
    convalidare = {'passed': False, 'kernel_sha256': hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': hardware_LOG, 'checks': []}
    numero_di_porta = vuota_numero_di_porta()
    Processi = subprocess.Popen(['python3', str(azione_radice/'strumenti/Esegui_comando.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(numero_di_porta), '--pip-cache', str(Memoria_percorso), '--ftp-port', str(vuota_numero_di_porta())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selettore_a916db4e = selectors.DefaultSelector()
    selettore_a916db4e.register(Processi.stdout, selectors.EVENT_READ)
    trascrizione = bytearray()
    def 기다리기(mostrare_VALORE=b'jkoros-native> '):
        Contenuto_VALORE = bytearray()
        끝 = time.monotonic()+120
        while mostrare_VALORE not in Contenuto_VALORE:
            if time.monotonic() > 끝 or Processi.poll() is not None:
                raise AssertionError('게스트 replica 없음: '+Contenuto_VALORE.decode('utf-8','replace'))
            for voce_VALORE, _ in selettore_a916db4e.select(.1):
                blocco_VALORE_652d4b53 = voce_VALORE.fileobj.read(4096)
                Contenuto_VALORE.extend(blocco_VALORE_652d4b53)
                trascrizione.extend(blocco_VALORE_652d4b53)
        return Contenuto_VALORE.decode('utf-8', 'replace').replace('\r\n','\n')
    def Shell(comando, mostrare_VALORE=b'jkoros-native> '):
        Processi.stdin.write(comando.encode()+b'\n')
        Processi.stdin.flush()
        return 기다리기(mostrare_VALORE)
    def Esegui_comando(comando, 예상, Stato_VALORE=0):
        Contenuto_VALORE = Shell(comando)
        assert 예상 in Contenuto_VALORE and '\nexit '+str(Stato_VALORE)+'\n' in Contenuto_VALORE, Contenuto_VALORE
        convalidare['checks'].append(comando)
        return Contenuto_VALORE
    def Upload_File(Nome, dati):
        Shell('load '+Nome, b'hex> ')
        for funzione_INDICE in range(0, len(dati), 64):
            Shell(dati[funzione_INDICE:funzione_INDICE+64].hex(), b'hex> ')
        assert 'LOADED' in Shell('.')
    try:
        기다리기()
        Esegui_comando('pip --help', 'MicroPython fonte_albero 설치기')
        Upload_File('오류시험.py', (azione_radice/'prove/PYTHON/한국어오류시험.py').read_bytes())
        Esegui_comando('python 오류시험.py', 'Italiano file eccezione verificare')
        Esegui_comando('pip install micropython-bisect==3.3.3 --port '+str(numero_di_porta), 'installare_VALORE 완료: micropython-bisect 3.3.3')
        Esegui_comando('python -c \'from bisect import insort as 순서대로넣기; VALORE=[1,5]; 순서대로넣기(VALORE,3); print(VALORE)\'', '[1, 3, 5]')
        Esegui_comando('python -m pip list', 'micropython-bisect 3.3.3')
        Esegui_comando('pip install micropython-bisect==3.3.3 --port '+str(numero_di_porta), '이미 설치됨:')
        Esegui_comando('pip install jkoros-fixture==1.0 --port '+str(numero_di_porta), 'installare_VALORE 완료: jkoros-fixture')
        Esegui_comando('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Esegui_comando('pip install jkoros-syntax==1.0 --port '+str(numero_di_porta), 'aggregare errore:', 1)
        Esegui_comando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 errore 보존")\'', '구문 errore 보존')
        Upload_File('공간시험.py', (azione_radice/'prove/PYTHON/aggregare_radice_test.py').read_bytes())
        Esegui_comando('python 공간시험.py '+str(numero_di_porta), 'aggregare e_mail_area 부족 Reso_bridge verificare')
        Esegui_comando('pip uninstall jkoros-fixture', 'rimuovere_voce 완료: jkoros-fixture')
        Esegui_comando('pip uninstall micropython-bisect', 'rimuovere_voce 완료: micropython-bisect')
        Esegui_comando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("rimuovere_voce verificare")\'', 'rimuovere_voce verificare')
        convalidare['passed'] = True
        print('PASS: PyPI fisico_hardware installare_VALORE·import·Esegui_comando, Italiano eccezione, 패키지 elenco_VALORE, errore_VALORE Reso_bridge, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Esci_app 키로 QEMU를 끝내면 실행기의 Inoltro_VALORE 문맥도 정리된다.
            Processi.stdin.write(b'\x01x')
            Processi.stdin.flush()
            Processi.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Processi.terminate()
            try:
                Processi.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Processi.kill()
                Processi.wait()
        if Processi.poll() is None:
            Processi.kill()
            Processi.wait()
        selettore_a916db4e.close()
        Processi.stdin.close()
        Processi.stdout.close()
        (KR_percorso/'serial.log').write_bytes(trascrizione)
        (KR_percorso/'report.json').write_text(json.dumps(convalidare, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    avvia()
