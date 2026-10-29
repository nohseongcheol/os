#!/usr/bin/env python3
"""PyPI 物理硬件 배포와 부정 輸入值·RAM 되돌림을 內建 커널에서 검사한다."""
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
from 捆綁中繼 import 捆綁代碼庫, 解壓縮
from 執行命令 import 項目根


def 測試滾輪(名稱, 檔案條目列, 契約值='Root-Is-Purelib: true\n', 依賴項列=''):
    資料 = io.BytesIO()
    with zipfile.ZipFile(資料, 'w', zipfile.ZIP_DEFLATED) as 軟件包:
        軟件包.writestr(名稱 + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + 契約值)
        軟件包.writestr(名稱 + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + 名稱 + '\nVersion: 1.0\n' + 依賴項列)
        for 路徑, 內容值 in 檔案條目列.items():
            軟件包.writestr(路徑, 內容值)
    return 資料.getvalue()


def 檢查宿主():
    是否常規 = 測試滾輪('jkoros-fixture', {'mod.py': '值=42\n'})
    assert 解壓縮('jkoros_fixture-1.0-py3-none-any.whl', 是否常規, 'jkoros-fixture', '1.0') == {'mod.py': '值=42\n'.encode()}
    for 資料 in (
            測試滾輪('jkoros-fixture', {'../escape.py': ''}),
            測試滾輪('jkoros-fixture', {'/abs.py': ''}),
            測試滾輪('jkoros-fixture', {'big.py': 'x' * 16385}),
            測試滾輪('jkoros-fixture', {'mod.so': ''}),
            測試滾輪('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            測試滾輪('jkoros-fixture', {'mod.py': ''}, 依賴項列='Requires-Dist: requests\n')):
        try:
            解壓縮('jkoros_fixture-1.0-py3-none-any.whl', 資料, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel 路徑·大小·C 擴展名值·依賴項列 拒絕值')


def 空埠編號():
    with socket.socket() as 通訊端值:
        通訊端值.bind(('127.0.0.1', 0))
        return 通訊端值.getsockname()[1]


def 運行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--host-only', action='store_true')
    實參 = 解析器.parse_args()
    檢查宿主()
    if 實參.host_only:
        return
    結果路徑 = 項目根/'build/verification/pip'
    結果路徑.mkdir(parents=True, exist_ok=True)
    存儲裝置路徑 = 結果路徑/'cache'
    存儲裝置路徑.mkdir(exist_ok=True)
    # 實際資料 PyPI 分發值 檔案. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    捆綁代碼庫(項目根/'build/pip-cache').準備('micropython-bisect==3.3.3')
    for 尾部值 in ('.archive', '.json'):
        shutil.copyfile(str(項目根/'build/pip-cache'/('micropython-bisect==3.3.3'+尾部值)), str(存儲裝置路徑/('micropython-bisect==3.3.3'+尾部值)))
    硬件日誌 = json.loads((存儲裝置路徑/'micropython-bisect==3.3.3.json').read_text())
    assert 硬件日誌['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for 名稱, 檔案條目列 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .計算結果 import 添加值列\n', '검증꾸러미/計算結果.py': 'def 添加值列(首位操作數,第二操作數):\n return 首位操作數+第二操作數\n'}),
            ('jkoros-space', {'space%d.py' % 數: '值=1\n' for 數 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        資料 = 測試滾輪(名稱, 檔案條目列)
        (存儲裝置路徑/(名稱+'==1.0.archive')).write_bytes(資料)
        (存儲裝置路徑/(名稱+'==1.0.json')).write_text(json.dumps({'name': 名稱, 'version': '1.0',
            'filename': 名稱.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(資料).hexdigest()}))
    有效性校驗 = {'passed': False, 'kernel_sha256': hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 硬件日誌, 'checks': []}
    埠編號 = 空埠編號()
    程序 = subprocess.Popen(['python3', str(項目根/'工具集/執行命令.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(埠編號), '--pip-cache', str(存儲裝置路徑), '--ftp-port', str(空埠編號())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    選擇器 = selectors.DefaultSelector()
    選擇器.register(程序.stdout, selectors.EVENT_READ)
    執行記錄 = bytearray()
    def 等待(顯示值=b'jkoros-native> '):
        內容值 = bytearray()
        結尾 = time.monotonic()+120
        while 顯示值 not in 內容值:
            if time.monotonic() > 結尾 or 程序.poll() is not None:
                raise AssertionError('게스트 回覆 缺失方法: '+內容值.decode('utf-8','replace'))
            for 條目值, _ in 選擇器.select(.1):
                片段值 = 條目值.fileobj.read(4096)
                內容值.extend(片段值)
                執行記錄.extend(片段值)
        return 內容值.decode('utf-8', 'replace').replace('\r\n','\n')
    def 命令殼(命令, 顯示值=b'jkoros-native> '):
        程序.stdin.write(命令.encode()+b'\n')
        程序.stdin.flush()
        return 等待(顯示值)
    def 執行命令(命令, 預期值列, 狀態值=0):
        內容值 = 命令殼(命令)
        assert 預期值列 in 內容值 and '\nexit '+str(狀態值)+'\n' in 內容值, 內容值
        有效性校驗['checks'].append(命令)
        return 內容值
    def 上傳檔案集(名稱, 資料):
        命令殼('load '+名稱, b'hex> ')
        for 位置索引 in range(0, len(資料), 64):
            命令殼(資料[位置索引:位置索引+64].hex(), b'hex> ')
        assert 'LOADED' in 命令殼('.')
    try:
        等待()
        執行命令('pip --help', 'MicroPython 原始碼樹 설치기')
        上傳檔案集('오류시험.py', (項目根/'測試/Python/韓語錯誤測試.py').read_bytes())
        執行命令('python 오류시험.py', '中文 檔案 異常 驗證')
        執行命令('pip install micropython-bisect==3.3.3 --port '+str(埠編號), '安裝值 是否完成: micropython-bisect 3.3.3')
        執行命令('python -c \'from bisect import insort as 순서대로넣기; 值=[1,5]; 순서대로넣기(值,3); print(值)\'', '[1, 3, 5]')
        執行命令('python -m pip list', 'micropython-bisect 3.3.3')
        執行命令('pip install micropython-bisect==3.3.3 --port '+str(埠編號), '이미 설치됨:')
        執行命令('pip install jkoros-fixture==1.0 --port '+str(埠編號), '安裝值 是否完成: jkoros-fixture')
        執行命令('python -c \'from 검증꾸러미 import 添加值列; print(添加值列(20,22))\'', '\n42\n')
        執行命令('pip install jkoros-syntax==1.0 --port '+str(埠編號), '軟件包 錯誤:', 1)
        執行命令('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 錯誤 보존")\'', '구문 錯誤 보존')
        上傳檔案集('공간시험.py', (項目根/'測試/Python/捆綁命名空間測試.py').read_bytes())
        執行命令('python 공간시험.py '+str(埠編號), '軟件包 地址區域 부족 發回橋接 驗證')
        執行命令('pip uninstall jkoros-fixture', '移除條目 是否完成: jkoros-fixture')
        執行命令('pip uninstall micropython-bisect', '移除條目 是否完成: micropython-bisect')
        執行命令('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("移除條目 驗證")\'', '移除條目 驗證')
        有效性校驗['passed'] = True
        print('PASS: PyPI 物理硬件 安裝值·import·執行命令, 中文 異常, 패키지 目錄值, 失敗值 發回橋接, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 退出程式 키로 QEMU를 끝내면 실행기의 中繼值 문맥도 정리된다.
            程序.stdin.write(b'\x01x')
            程序.stdin.flush()
            程序.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            程序.terminate()
            try:
                程序.wait(timeout=8)
            except subprocess.TimeoutExpired:
                程序.kill()
                程序.wait()
        if 程序.poll() is None:
            程序.kill()
            程序.wait()
        選擇器.close()
        程序.stdin.close()
        程序.stdout.close()
        (結果路徑/'serial.log').write_bytes(執行記錄)
        (結果路徑/'report.json').write_text(json.dumps(有效性校驗, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    運行()
