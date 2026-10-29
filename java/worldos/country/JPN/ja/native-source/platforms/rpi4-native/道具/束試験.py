#!/usr/bin/env python3
"""PyPI 物理機器 배포와 부정 入力値·RAM 되돌림을 内蔵 커널에서 검사한다."""
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
from 束中継 import 束保管庫, 展開
from 命令実行 import 計画根


def 車輪試験(名前, ファイル登録項目一覧, 契約値='Root-Is-Purelib: true\n', 依存項目=''):
    データ = io.BytesIO()
    with zipfile.ZipFile(データ, 'w', zipfile.ZIP_DEFLATED) as パッケージ:
        パッケージ.writestr(名前 + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + 契約値)
        パッケージ.writestr(名前 + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + 名前 + '\nVersion: 1.0\n' + 依存項目)
        for 経路, 内容物値 in ファイル登録項目一覧.items():
            パッケージ.writestr(経路, 内容物値)
    return データ.getvalue()


def ホスト検査():
    判定通常 = 車輪試験('jkoros-fixture', {'mod.py': '値=42\n'})
    assert 展開('jkoros_fixture-1.0-py3-none-any.whl', 判定通常, 'jkoros-fixture', '1.0') == {'mod.py': '値=42\n'.encode()}
    for データ in (
            車輪試験('jkoros-fixture', {'../escape.py': ''}),
            車輪試験('jkoros-fixture', {'/abs.py': ''}),
            車輪試験('jkoros-fixture', {'big.py': 'x' * 16385}),
            車輪試験('jkoros-fixture', {'mod.so': ''}),
            車輪試験('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            車輪試験('jkoros-fixture', {'mod.py': ''}, 依存項目='Requires-Dist: requests\n')):
        try:
            展開('jkoros_fixture-1.0-py3-none-any.whl', データ, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel 経路·容量·C 拡張子値·依存項目 値却下')


def 空ポート番号():
    with socket.socket() as ソケット値:
        ソケット値.bind(('127.0.0.1', 0))
        return ソケット値.getsockname()[1]


def 起動処理():
    構文解析器 = argparse.ArgumentParser(description=__doc__)
    構文解析器.add_argument('--host-only', action='store_true')
    引数 = 構文解析器.parse_args()
    ホスト検査()
    if 引数.host_only:
        return
    結果経路 = 計画根/'build/verification/pip'
    結果経路.mkdir(parents=True, exist_ok=True)
    記憶装置経路 = 結果経路/'cache'
    記憶装置経路.mkdir(exist_ok=True)
    # 実際データ PyPI 配布値 ファイル. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    束保管庫(計画根/'build/pip-cache').用意('micropython-bisect==3.3.3')
    for 尾部値 in ('.archive', '.json'):
        shutil.copyfile(str(計画根/'build/pip-cache'/('micropython-bisect==3.3.3'+尾部値)), str(記憶装置経路/('micropython-bisect==3.3.3'+尾部値)))
    機器履歴記録 = json.loads((記憶装置経路/'micropython-bisect==3.3.3.json').read_text())
    assert 機器履歴記録['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for 名前, ファイル登録項目一覧 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .計算結果 import 値一覧追加\n', '검증꾸러미/計算結果.py': 'def 値一覧追加(先頭位置被演算子,第二被演算子):\n return 先頭位置被演算子+第二被演算子\n'}),
            ('jkoros-space', {'space%d.py' % 数: '値=1\n' for 数 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        データ = 車輪試験(名前, ファイル登録項目一覧)
        (記憶装置経路/(名前+'==1.0.archive')).write_bytes(データ)
        (記憶装置経路/(名前+'==1.0.json')).write_text(json.dumps({'name': 名前, 'version': '1.0',
            'filename': 名前.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(データ).hexdigest()}))
    妥当性検査 = {'passed': False, 'kernel_sha256': hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 機器履歴記録, 'checks': []}
    ポート番号 = 空ポート番号()
    プロセス = subprocess.Popen(['python3', str(計画根/'道具/命令実行.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(ポート番号), '--pip-cache', str(記憶装置経路), '--ftp-port', str(空ポート番号())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    選択器 = selectors.DefaultSelector()
    選択器.register(プロセス.stdout, selectors.EVENT_READ)
    実行記録 = bytearray()
    def 待機(値表示=b'jkoros-native> '):
        内容物値 = bytearray()
        終端 = time.monotonic()+120
        while 値表示 not in 内容物値:
            if time.monotonic() > 終端 or プロセス.poll() is not None:
                raise AssertionError('게스트 返答 未存在メソッド: '+内容物値.decode('utf-8','replace'))
            for 入口値, _ in 選択器.select(.1):
                断片値 = 入口値.fileobj.read(4096)
                内容物値.extend(断片値)
                実行記録.extend(断片値)
        return 内容物値.decode('utf-8', 'replace').replace('\r\n','\n')
    def シェル(命令, 値表示=b'jkoros-native> '):
        プロセス.stdin.write(命令.encode()+b'\n')
        プロセス.stdin.flush()
        return 待機(値表示)
    def 命令実行(命令, 期待値一覧, 状況値=0):
        内容物値 = シェル(命令)
        assert 期待値一覧 in 内容物値 and '\nexit '+str(状況値)+'\n' in 内容物値, 内容物値
        妥当性検査['checks'].append(命令)
        return 内容物値
    def 送出転送ファイル群(名前, データ):
        シェル('load '+名前, b'hex> ')
        for 位置添字 in range(0, len(データ), 64):
            シェル(データ[位置添字:位置添字+64].hex(), b'hex> ')
        assert 'LOADED' in シェル('.')
    try:
        待機()
        命令実行('pip --help', 'MicroPython ソース木 설치기')
        送出転送ファイル群('오류시험.py', (計画根/'試験/Python/韓国語エラー試験.py').read_bytes())
        命令実行('python 오류시험.py', '日本語 ファイル 例外 検証')
        命令実行('pip install micropython-bisect==3.3.3 --port '+str(ポート番号), '値導入 判定完了: micropython-bisect 3.3.3')
        命令実行('python -c \'from bisect import insort as 순서대로넣기; 値=[1,5]; 순서대로넣기(値,3); print(値)\'', '[1, 3, 5]')
        命令実行('python -m pip list', 'micropython-bisect 3.3.3')
        命令実行('pip install micropython-bisect==3.3.3 --port '+str(ポート番号), '이미 설치됨:')
        命令実行('pip install jkoros-fixture==1.0 --port '+str(ポート番号), '値導入 判定完了: jkoros-fixture')
        命令実行('python -c \'from 검증꾸러미 import 値一覧追加; print(値一覧追加(20,22))\'', '\n42\n')
        命令実行('pip install jkoros-syntax==1.0 --port '+str(ポート番号), 'パッケージ エラー:', 1)
        命令実行('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 エラー 보존")\'', '구문 エラー 보존')
        送出転送ファイル群('공간시험.py', (計画根/'試験/Python/束名前空間試験.py').read_bytes())
        命令実行('python 공간시험.py '+str(ポート番号), 'パッケージ 番地領域 부족 復帰橋渡し 検証')
        命令実行('pip uninstall jkoros-fixture', '入口除去 判定完了: jkoros-fixture')
        命令実行('pip uninstall micropython-bisect', '入口除去 判定完了: micropython-bisect')
        命令実行('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("入口除去 検証")\'', '入口除去 検証')
        妥当性検査['passed'] = True
        print('PASS: PyPI 物理機器 値導入·import·命令実行, 日本語 例外, 패키지 ディレクトリ値, 失敗値 復帰橋渡し, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 終了点プログラム 키로 QEMU를 끝내면 실행기의 値中継 문맥도 정리된다.
            プロセス.stdin.write(b'\x01x')
            プロセス.stdin.flush()
            プロセス.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            プロセス.terminate()
            try:
                プロセス.wait(timeout=8)
            except subprocess.TimeoutExpired:
                プロセス.kill()
                プロセス.wait()
        if プロセス.poll() is None:
            プロセス.kill()
            プロセス.wait()
        選択器.close()
        プロセス.stdin.close()
        プロセス.stdout.close()
        (結果経路/'serial.log').write_bytes(実行記録)
        (結果経路/'report.json').write_text(json.dumps(妥当性検査, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    起動処理()
