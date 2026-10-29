#!/usr/bin/env python3
"""配布値 자료만으로 LGPL 재연결과 수정한 TinyCC의 実際データ 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from 命令実行 import 計画根, 命令


def 起動処理():
    構文解析器 = argparse.ArgumentParser(description=__doc__)
    構文解析器.add_argument('--sdk', type=Path, default=計画根.parent / 'rpi4/build/rootfs')
    引数 = 構文解析器.parse_args()
    出力 = 計画根 / 'build/verification/cosl-relink'
    出力.mkdir(parents=True, exist_ok=True)
    報告値 = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((計画根 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 一時値:
            経路 = Path(一時値)
            with tarfile.open(str(計画根 / 'dist/jkoros-native-relink.tar.gz')) as 集合値:
                for 入口値 in 集合値.getmembers():
                    if 経路 not in (経路 / 入口値.name).resolve().parents or 入口値.issym() or 入口値.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + 入口値.name)
                集合値.extractall(str(経路))
            ソース = 経路 / 'jkoros-native-relink'
            def 再接続通信端点(名前, 引数列一覧):
                with (出力 / 名前).open('wb') as 履歴記録記録:
                    subprocess.run(['python3', 'relink.py'] + 引数列一覧, cwd=str(ソース),
                                   stdout=履歴記録記録, stderr=subprocess.STDOUT, check=True, timeout=180)
            再接続通信端点('original.log', ['--verify'])
            報告値['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            コンパイラ道具要素 = ソース / 'vendor/tinycc/libtcc.c'
            本体本文 = コンパイラ道具要素.read_text()
            位置 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert 本体本文.count(位置) == 1
            コンパイラ道具要素.write_text(本体本文.replace(位置, 位置 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            再接続通信端点('modified-tinycc.log', ['--tinycc', '--sdk', str(引数.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            イメージ値 = ソース / 'build/relinked/kernel8.img'
            報告値['modified_kernel_sha256'] = hashlib.sha256(イメージ値.read_bytes()).hexdigest()
            assert 報告値['modified_kernel_sha256'] != 報告値['kernel_sha256']
            報告値['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            引数列一覧 = 命令()
            引数列一覧[引数列一覧.index('-kernel') + 1] = str(イメージ値)
            プロセス値 = subprocess.Popen(引数列一覧 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            履歴記録記録 = bytearray()
            選択状態値 = selectors.DefaultSelector()
            選択状態値.register(プロセス値.stdout, selectors.EVENT_READ)
            def 状況待合(値表示=b'jkoros-native> ', 初期項目=0):
                終端 = time.monotonic() + 40
                while 値表示 not in 履歴記録記録[初期項目:]:
                    if time.monotonic() > 終端 or プロセス値.poll() is not None:
                        raise AssertionError('Missing ' + repr(値表示) + '\n' + 履歴記録記録[初期項目:].decode('utf-8', 'replace'))
                    for 入口値, _ in 選択状態値.select(.1):
                        データ = 入口値.fileobj.read(65536)
                        if データ:
                            履歴記録記録.extend(データ)
                return bytes(履歴記録記録[初期項目:])
            def 送信(語本文, 値表示=b'jkoros-native> '):
                初期項目 = len(履歴記録記録)
                プロセス値.stdin.write(語本文.encode() + b'\n')
                プロセス値.stdin.flush()
                return 状況待合(値表示, 初期項目)
            try:
                状況待合()
                試験 = '#include <ファイルABI.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ファイルデータ書込(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                送信('load /relink.c', b'hex> ')
                for 位置添字 in range(0, len(試験), 64):
                    送信(試験[位置添字:位置添字+64].hex(), b'hex> ')
                assert b'LOADED' in 送信('.')
                結果 = 送信('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 結果, 結果
                結果 = 送信('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 結果 and b'exit 0' in 結果, 結果
                報告値['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                選択状態値.close()
                if プロセス値.poll() is None:
                    プロセス値.terminate()
                    try:
                        プロセス値.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        プロセス値.kill()
                        プロセス値.wait()
                (出力 / 'guest.log').write_bytes(履歴記録記録)
        報告値['passed'] = True
        print(json.dumps(報告値, ensure_ascii=False, indent=2))
    finally:
        (出力 / 'report.json').write_text(json.dumps(報告値, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    起動処理()
