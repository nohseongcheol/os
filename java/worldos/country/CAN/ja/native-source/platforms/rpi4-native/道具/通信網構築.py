from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def 通信網作成(根経路, Cコンパイラ, 書庫道具要素, 構成設定ビット列, 命令実行):
    原本データ = 根経路 / 'vendor/lwip/src'
    ポート番号 = 根経路 / '通信網'
    出力結果 = 根経路 / 'build/network'
    出力結果.mkdir(exist_ok=True)
    write_header(根経路, 出力結果 / 'ip_config.h')
    ファイル一覧 = sorted((原本データ / 'core').glob('*.c')) + sorted((原本データ / 'core/ipv4').glob('*.c'))
    ファイル一覧 += [原本データ / 'netif/ethernet.c']
    ファイル一覧 += sorted(ポート番号.glob('*.c'))
    宛先ファイル群 = []
    for 経路 in ファイル一覧:
        宛先ファイル = 出力結果 / (経路.stem + '.o')
        命令実行([Cコンパイラ] + 構成設定ビット列 + ['-include', 出力結果 / 'ip_config.h', '-std=c11', '-I', ポート番号, '-I', 原本データ / 'include',
             '-I', 根経路.parents[1] / 'posix-kor/arm64-native/ヘッダー', '-c', 経路, '-o', 宛先ファイル])
        宛先ファイル群.append(宛先ファイル)
    ライブラリ = 出力結果 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(出力結果)) as 一時経路:
        新規ライブラリ=Path(一時経路)/'libnetwork.a'
        命令実行([書庫道具要素, 'rcs', 新規ライブラリ] + 宛先ファイル群)
        新規ライブラリ.replace(ライブラリ)
    return ライブラリ
