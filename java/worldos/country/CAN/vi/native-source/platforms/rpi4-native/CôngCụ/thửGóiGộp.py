#!/usr/bin/env python3
"""PyPI phầnCứngVậtLý 배포와 부정 giáTrịVào·RAM 되돌림을 tựThân 커널에서 검사한다."""
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
from chuyểnTiếpGóiGộp import khoNguồnGóiGộp, giảiNén
from thựcThiLệnh import gốcCâyDựÁn


def thửBánhCuộn(tên, cácMụcTệp, giáTrịQuyƯớc='Root-Is-Purelib: true\n', cácPhụThuộc=''):
    DữLiệu = io.BytesIO()
    with zipfile.ZipFile(DữLiệu, 'w', zipfile.ZIP_DEFLATED) as GóiGộp:
        GóiGộp.writestr(tên + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + giáTrịQuyƯớc)
        GóiGộp.writestr(tên + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + tên + '\nVersion: 1.0\n' + cácPhụThuộc)
        for đườngDẫn, giáTrịNộiDung in cácMụcTệp.items():
            GóiGộp.writestr(đườngDẫn, giáTrịNộiDung)
    return DữLiệu.getvalue()


def kiểmTraChủ():
    làBìnhThường = thửBánhCuộn('jkoros-fixture', {'mod.py': 'giáTrị=42\n'})
    assert giảiNén('jkoros_fixture-1.0-py3-none-any.whl', làBìnhThường, 'jkoros-fixture', '1.0') == {'mod.py': 'giáTrị=42\n'.encode()}
    for DữLiệu in (
            thửBánhCuộn('jkoros-fixture', {'../escape.py': ''}),
            thửBánhCuộn('jkoros-fixture', {'/abs.py': ''}),
            thửBánhCuộn('jkoros-fixture', {'big.py': 'x' * 16385}),
            thửBánhCuộn('jkoros-fixture', {'mod.so': ''}),
            thửBánhCuộn('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            thửBánhCuộn('jkoros-fixture', {'mod.py': ''}, cácPhụThuộc='Requires-Dist: requests\n')):
        try:
            giảiNén('jkoros_fixture-1.0-py3-none-any.whl', DữLiệu, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel đườngDẫn·cỡ·C giáTrịPhầnMởRộng·cácPhụThuộc từChốiGiáTrị')


def sốCổngRỗng():
    with socket.socket() as giáTrịỔCắmMạng:
        giáTrịỔCắmMạng.bind(('127.0.0.1', 0))
        return giáTrịỔCắmMạng.getsockname()[1]


def chạy():
    BộPhânTích = argparse.ArgumentParser(description=__doc__)
    BộPhânTích.add_argument('--host-only', action='store_true')
    cácĐốiSố = BộPhânTích.parse_args()
    kiểmTraChủ()
    if cácĐốiSố.host_only:
        return
    đườngDẫnKếtQuả = gốcCâyDựÁn/'build/verification/pip'
    đườngDẫnKếtQuả.mkdir(parents=True, exist_ok=True)
    đườngDẫnLưuTrữ = đườngDẫnKếtQuả/'cache'
    đườngDẫnLưuTrữ.mkdir(exist_ok=True)
    # dữLiệuThựcTế PyPI giáTrịBảnPhânPhối Tệp. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    khoNguồnGóiGộp(gốcCâyDựÁn/'build/pip-cache').chuẩnBị('micropython-bisect==3.3.3')
    for giáTrịĐuôi in ('.archive', '.json'):
        shutil.copyfile(str(gốcCâyDựÁn/'build/pip-cache'/('micropython-bisect==3.3.3'+giáTrịĐuôi)), str(đườngDẫnLưuTrữ/('micropython-bisect==3.3.3'+giáTrịĐuôi)))
    nhậtKýPhầnCứng = json.loads((đườngDẫnLưuTrữ/'micropython-bisect==3.3.3.json').read_text())
    assert nhậtKýPhầnCứng['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for tên, cácMụcTệp in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .phépTính import thêmCácGiáTrị\n', '검증꾸러미/phépTính.py': 'def thêmCácGiáTrị(toánHạngĐầuTiên,toánHạngThứHai):\n return toánHạngĐầuTiên+toánHạngThứHai\n'}),
            ('jkoros-space', {'space%d.py' % trịSố: 'giáTrị=1\n' for trịSố in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        DữLiệu = thửBánhCuộn(tên, cácMụcTệp)
        (đườngDẫnLưuTrữ/(tên+'==1.0.archive')).write_bytes(DữLiệu)
        (đườngDẫnLưuTrữ/(tên+'==1.0.json')).write_text(json.dumps({'name': tên, 'version': '1.0',
            'filename': tên.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(DữLiệu).hexdigest()}))
    thẩmĐịnh = {'passed': False, 'kernel_sha256': hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': nhậtKýPhầnCứng, 'checks': []}
    sốCổng = sốCổngRỗng()
    tiếnTrình = subprocess.Popen(['python3', str(gốcCâyDựÁn/'CôngCụ/thựcThiLệnh.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(sốCổng), '--pip-cache', str(đườngDẫnLưuTrữ), '--ftp-port', str(sốCổngRỗng())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    BộChọn = selectors.DefaultSelector()
    BộChọn.register(tiếnTrình.stdout, selectors.EVENT_READ)
    bảnGhiDiễnTiến = bytearray()
    def đợi(hiệnGiáTrị=b'jkoros-native> '):
        giáTrịNộiDung = bytearray()
        phầnKết = time.monotonic()+120
        while hiệnGiáTrị not in giáTrịNộiDung:
            if time.monotonic() > phầnKết or tiếnTrình.poll() is not None:
                raise AssertionError('게스트 lờiĐáp phươngThứcThiếu: '+giáTrịNộiDung.decode('utf-8','replace'))
            for giáTrịMục, _ in BộChọn.select(.1):
                giáTrịĐoạn = giáTrịMục.fileobj.read(4096)
                giáTrịNộiDung.extend(giáTrịĐoạn)
                bảnGhiDiễnTiến.extend(giáTrịĐoạn)
        return giáTrịNộiDung.decode('utf-8', 'replace').replace('\r\n','\n')
    def vỏLệnh(lệnh, hiệnGiáTrị=b'jkoros-native> '):
        tiếnTrình.stdin.write(lệnh.encode()+b'\n')
        tiếnTrình.stdin.flush()
        return đợi(hiệnGiáTrị)
    def thựcThiLệnh(lệnh, cácGiáTrịDựKiến, giáTrịTrạngThái=0):
        giáTrịNộiDung = vỏLệnh(lệnh)
        assert cácGiáTrịDựKiến in giáTrịNộiDung and '\nexit '+str(giáTrịTrạngThái)+'\n' in giáTrịNộiDung, giáTrịNộiDung
        thẩmĐịnh['checks'].append(lệnh)
        return giáTrịNộiDung
    def cácTệpTảiLên(tên, DữLiệu):
        vỏLệnh('load '+tên, b'hex> ')
        for chỉSốVịTrí in range(0, len(DữLiệu), 64):
            vỏLệnh(DữLiệu[chỉSốVịTrí:chỉSốVịTrí+64].hex(), b'hex> ')
        assert 'LOADED' in vỏLệnh('.')
    try:
        đợi()
        thựcThiLệnh('pip --help', 'MicroPython câyNguồn 설치기')
        cácTệpTảiLên('오류시험.py', (gốcCâyDựÁn/'KiểmThử/Python/ThửLỗiTiếngHàn.py').read_bytes())
        thựcThiLệnh('python 오류시험.py', 'tiếngViệt Tệp ngoạiLệ xácMinh')
        thựcThiLệnh('pip install micropython-bisect==3.3.3 --port '+str(sốCổng), 'càiĐặtGiáTrị làĐầyĐủ: micropython-bisect 3.3.3')
        thựcThiLệnh('python -c \'from bisect import insort as 순서대로넣기; giáTrị=[1,5]; 순서대로넣기(giáTrị,3); print(giáTrị)\'', '[1, 3, 5]')
        thựcThiLệnh('python -m pip list', 'micropython-bisect 3.3.3')
        thựcThiLệnh('pip install micropython-bisect==3.3.3 --port '+str(sốCổng), '이미 설치됨:')
        thựcThiLệnh('pip install jkoros-fixture==1.0 --port '+str(sốCổng), 'càiĐặtGiáTrị làĐầyĐủ: jkoros-fixture')
        thựcThiLệnh('python -c \'from 검증꾸러미 import thêmCácGiáTrị; print(thêmCácGiáTrị(20,22))\'', '\n42\n')
        thựcThiLệnh('pip install jkoros-syntax==1.0 --port '+str(sốCổng), 'GóiGộp lỗi:', 1)
        thựcThiLệnh('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 lỗi 보존")\'', '구문 lỗi 보존')
        cácTệpTảiLên('공간시험.py', (gốcCâyDựÁn/'KiểmThử/Python/ThửKhôngGianTênGóiGộp.py').read_bytes())
        thựcThiLệnh('python 공간시험.py '+str(sốCổng), 'GóiGộp miềnĐịaChỉ 부족 cầuNốiTrảVề xácMinh')
        thựcThiLệnh('pip uninstall jkoros-fixture', 'gỡMục làĐầyĐủ: jkoros-fixture')
        thựcThiLệnh('pip uninstall micropython-bisect', 'gỡMục làĐầyĐủ: micropython-bisect')
        thựcThiLệnh('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("gỡMục xácMinh")\'', 'gỡMục xácMinh')
        thẩmĐịnh['passed'] = True
        print('PASS: PyPI phầnCứngVậtLý càiĐặtGiáTrị·import·thựcThiLệnh, tiếngViệt ngoạiLệ, 패키지 giáTrịThưMục, giáTrịSựThấtBại cầuNốiTrảVề, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 chươngTrìnhRa 키로 QEMU를 끝내면 실행기의 chuyểnTiếpGiáTrị 문맥도 정리된다.
            tiếnTrình.stdin.write(b'\x01x')
            tiếnTrình.stdin.flush()
            tiếnTrình.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            tiếnTrình.terminate()
            try:
                tiếnTrình.wait(timeout=8)
            except subprocess.TimeoutExpired:
                tiếnTrình.kill()
                tiếnTrình.wait()
        if tiếnTrình.poll() is None:
            tiếnTrình.kill()
            tiếnTrình.wait()
        BộChọn.close()
        tiếnTrình.stdin.close()
        tiếnTrình.stdout.close()
        (đườngDẫnKếtQuả/'serial.log').write_bytes(bảnGhiDiễnTiến)
        (đườngDẫnKếtQuả/'report.json').write_text(json.dumps(thẩmĐịnh, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    chạy()
