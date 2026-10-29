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
from 꾸러미중계 import ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ_ຣີໂພຊິທໍຣີ, 압축풀기
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ


def 시험휠(ຊື່, 파일들, ສັນຍາ_ຄ່າ='Root-Is-Purelib: true\n', 의존성=''):
    ຂໍ້ມູນ = io.BytesIO()
    with zipfile.ZipFile(ຂໍ້ມູນ, 'w', zipfile.ZIP_DEFLATED) as ຊຸດ:
        ຊຸດ.writestr(ຊື່ + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ສັນຍາ_ຄ່າ)
        ຊຸດ.writestr(ຊື່ + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ຊື່ + '\nVersion: 1.0\n' + 의존성)
        for ທາງໂຄຈອນ, ເນື້ອໃນ_ຄ່າ_cb0f2404 in 파일들.items():
            ຊຸດ.writestr(ທາງໂຄຈອນ, ເນື້ອໃນ_ຄ່າ_cb0f2404)
    return ຂໍ້ມູນ.getvalue()


def ເຊັກເງິນ_ໂຮສ():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'ຄ່າ=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'ຄ່າ=42\n'.encode()}
    for ຂໍ້ມູນ in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ຂໍ້ມູນ, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ທາງໂຄຈອນ·ຂະ_ຫນາດ·C ສ່ວນຂະຫຍາຍ_ຄ່າ·의존성 ປະຕິເສດ_ຄ່າ')


def ຫວ່າງ_ເປົ່າ_ຫມາຍເລກພອດ():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ແລ່ນ():
    ຕົວແຍກວິເຄາະ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = ຕົວແຍກວິເຄາະ_48ee4b1b.parse_args()
    ເຊັກເງິນ_ໂຮສ()
    if 인수.host_only:
        return
    ມາດຕະການ_ທາງໂຄຈອນ = ໂຄງ_ການ_ເລກຮາກ/'build/verification/pip'
    ມາດຕະການ_ທາງໂຄຈອນ.mkdir(parents=True, exist_ok=True)
    ບ່ອນເກັບຂໍ້ມູນ_ທາງໂຄຈອນ = ມາດຕະການ_ທາງໂຄຈອນ/'cache'
    ບ່ອນເກັບຂໍ້ມູນ_ທາງໂຄຈອນ.mkdir(exist_ok=True)
    # ຕົວ_ຈິງ_ຂໍ້ມູນ PyPI 배포 ຟາຍ. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ_ຣີໂພຊິທໍຣີ(ໂຄງ_ການ_ເລກຮາກ/'build/pip-cache').ກະ_ກຽມ('micropython-bisect==3.3.3')
    for ຫາງ_ຄ່າ in ('.archive', '.json'):
        shutil.copyfile(str(ໂຄງ_ການ_ເລກຮາກ/'build/pip-cache'/('micropython-bisect==3.3.3'+ຫາງ_ຄ່າ)), str(ບ່ອນເກັບຂໍ້ມູນ_ທາງໂຄຈອນ/('micropython-bisect==3.3.3'+ຫາງ_ຄ່າ)))
    실물기록 = json.loads((ບ່ອນເກັບຂໍ້ມູນ_ທາງໂຄຈອນ/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ຊື່, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'ຄ່າ=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ຂໍ້ມູນ = 시험휠(ຊື່, 파일들)
        (ບ່ອນເກັບຂໍ້ມູນ_ທາງໂຄຈອນ/(ຊື່+'==1.0.archive')).write_bytes(ຂໍ້ມູນ)
        (ບ່ອນເກັບຂໍ້ມູນ_ທາງໂຄຈອນ/(ຊື່+'==1.0.json')).write_text(json.dumps({'name': ຊື່, 'version': '1.0',
            'filename': ຊື່.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ຂໍ້ມູນ).hexdigest()}))
    ຮັບ_ຮອງ = {'passed': False, 'kernel_sha256': hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    ຫມາຍເລກພອດ = ຫວ່າງ_ເປົ່າ_ຫມາຍເລກພອດ()
    ຂະ_ບວນ_ການ = subprocess.Popen(['python3', str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(ຫມາຍເລກພອດ), '--pip-cache', str(ບ່ອນເກັບຂໍ້ມູນ_ທາງໂຄຈອນ), '--ftp-port', str(ຫວ່າງ_ເປົ່າ_ຫມາຍເລກພອດ())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ຕົວ_ໃຊ້_ເລືອກ_a916db4e = selectors.DefaultSelector()
    ຕົວ_ໃຊ້_ເລືອກ_a916db4e.register(ຂະ_ບວນ_ການ.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(ລາຍການ_ຄ່າ=b'jkoros-native> '):
        ເນື້ອໃນ_ຄ່າ_cb0f2404 = bytearray()
        끝 = time.monotonic()+120
        while ລາຍການ_ຄ່າ not in ເນື້ອໃນ_ຄ່າ_cb0f2404:
            if time.monotonic() > 끝 or ຂະ_ບວນ_ການ.poll() is not None:
                raise AssertionError('게스트 ຕອບກັບ 없음: '+ເນື້ອໃນ_ຄ່າ_cb0f2404.decode('utf-8','replace'))
            for ເຂົ້າໃນ_ຄ່າ, _ in ຕົວ_ໃຊ້_ເລືອກ_a916db4e.select(.1):
                조각 = ເຂົ້າໃນ_ຄ່າ.fileobj.read(4096)
                ເນື້ອໃນ_ຄ່າ_cb0f2404.extend(조각)
                대화기록.extend(조각)
        return ເນື້ອໃນ_ຄ່າ_cb0f2404.decode('utf-8', 'replace').replace('\r\n','\n')
    def ເຊລ(ຄໍາສັ່ງ_1f12b8e2, ລາຍການ_ຄ່າ=b'jkoros-native> '):
        ຂະ_ບວນ_ການ.stdin.write(ຄໍາສັ່ງ_1f12b8e2.encode()+b'\n')
        ຂະ_ບວນ_ການ.stdin.flush()
        return 기다리기(ລາຍການ_ຄ່າ)
    def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຄໍາສັ່ງ_1f12b8e2, 예상, ສະຖານະ_ຄ່າ=0):
        ເນື້ອໃນ_ຄ່າ_cb0f2404 = ເຊລ(ຄໍາສັ່ງ_1f12b8e2)
        assert 예상 in ເນື້ອໃນ_ຄ່າ_cb0f2404 and '\nexit '+str(ສະຖານະ_ຄ່າ)+'\n' in ເນື້ອໃນ_ຄ່າ_cb0f2404, ເນື້ອໃນ_ຄ່າ_cb0f2404
        ຮັບ_ຮອງ['checks'].append(ຄໍາສັ່ງ_1f12b8e2)
        return ເນື້ອໃນ_ຄ່າ_cb0f2404
    def ໂອນອອກ_ໄຟລ໌(ຊື່, ຂໍ້ມູນ):
        ເຊລ('load '+ຊື່, b'hex> ')
        for ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ in range(0, len(ຂໍ້ມູນ), 64):
            ເຊລ(ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ:ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ+64].hex(), b'hex> ')
        assert 'LOADED' in ເຊລ('.')
    try:
        기다리기()
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('pip --help', 'MicroPython ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 설치기')
        ໂອນອອກ_ໄຟລ໌('오류시험.py', (ໂຄງ_ການ_ເລກຮາກ/'시험/파이썬/한국어오류시험.py').read_bytes())
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('python 오류시험.py', '한국어 ຟາຍ ຂໍ້ຍົກເວັ້ນ 확인')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('pip install micropython-bisect==3.3.3 --port '+str(ຫມາຍເລກພອດ), 'ຕິດຕັ້ງ_ຄ່າ 완료: micropython-bisect 3.3.3')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('python -c \'from bisect import insort as 순서대로넣기; ຄ່າ=[1,5]; 순서대로넣기(ຄ່າ,3); print(ຄ່າ)\'', '[1, 3, 5]')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('python -m pip list', 'micropython-bisect 3.3.3')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('pip install micropython-bisect==3.3.3 --port '+str(ຫມາຍເລກພອດ), '이미 설치됨:')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('pip install jkoros-fixture==1.0 --port '+str(ຫມາຍເລກພອດ), 'ຕິດຕັ້ງ_ຄ່າ 완료: jkoros-fixture')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('pip install jkoros-syntax==1.0 --port '+str(ຫມາຍເລກພອດ), 'ຊຸດ ຂໍ້ຜິດພາດ:', 1)
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ຂໍ້ຜິດພາດ 보존")\'', '구문 ຂໍ້ຜິດພາດ 보존')
        ໂອນອອກ_ໄຟລ໌('공간시험.py', (ໂຄງ_ການ_ເລກຮາກ/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('python 공간시험.py '+str(ຫມາຍເລກພອດ), 'ຊຸດ 공간 부족 되돌림 확인')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('pip uninstall jkoros-fixture', '제거 완료: jkoros-fixture')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('pip uninstall micropython-bisect', '제거 완료: micropython-bisect')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("제거 확인")\'', '제거 확인')
        ຮັບ_ຮອງ['passed'] = True
        print('PASS: PyPI 실물 ຕິດຕັ້ງ_ຄ່າ·import·ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ, 한국어 ຂໍ້ຍົກເວັ້ນ, 패키지 ກຸ່ມຂໍ້ມູນ_ຄ່າ, ຫຼົ້ມເຫຼວ_ຄ່າ 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 ອອກ_ແອັບ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            ຂະ_ບວນ_ການ.stdin.write(b'\x01x')
            ຂະ_ບວນ_ການ.stdin.flush()
            ຂະ_ບວນ_ການ.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            ຂະ_ບວນ_ການ.terminate()
            try:
                ຂະ_ບວນ_ການ.wait(timeout=8)
            except subprocess.TimeoutExpired:
                ຂະ_ບວນ_ການ.kill()
                ຂະ_ບວນ_ການ.wait()
        if ຂະ_ບວນ_ການ.poll() is None:
            ຂະ_ບວນ_ການ.kill()
            ຂະ_ບວນ_ການ.wait()
        ຕົວ_ໃຊ້_ເລືອກ_a916db4e.close()
        ຂະ_ບວນ_ການ.stdin.close()
        ຂະ_ບວນ_ການ.stdout.close()
        (ມາດຕະການ_ທາງໂຄຈອນ/'serial.log').write_bytes(대화기록)
        (ມາດຕະການ_ທາງໂຄຈອນ/'report.json').write_text(json.dumps(ຮັບ_ຮອງ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ແລ່ນ()
