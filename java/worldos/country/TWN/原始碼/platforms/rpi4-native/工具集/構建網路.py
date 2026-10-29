from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def 創建網路(根路徑, C編譯器, 存檔工具, 配置項位元列, 執行命令):
    原始資料 = 根路徑 / 'vendor/lwip/src'
    埠編號 = 根路徑 / '通信網絡'
    輸出結果 = 根路徑 / 'build/network'
    輸出結果.mkdir(exist_ok=True)
    write_header(根路徑, 輸出結果 / 'ip_config.h')
    檔案列表 = sorted((原始資料 / 'core').glob('*.c')) + sorted((原始資料 / 'core/ipv4').glob('*.c'))
    檔案列表 += [原始資料 / 'netif/ethernet.c']
    檔案列表 += sorted(埠編號.glob('*.c'))
    目的地址檔案集 = []
    for 路徑 in 檔案列表:
        目的地址檔案 = 輸出結果 / (路徑.stem + '.o')
        執行命令([C編譯器] + 配置項位元列 + ['-include', 輸出結果 / 'ip_config.h', '-std=c11', '-I', 埠編號, '-I', 原始資料 / 'include',
             '-I', 根路徑.parents[1] / 'posix-kor/arm64-native/頭文件', '-c', 路徑, '-o', 目的地址檔案])
        目的地址檔案集.append(目的地址檔案)
    庫 = 輸出結果 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(輸出結果)) as 臨時路徑:
        新建庫=Path(臨時路徑)/'libnetwork.a'
        執行命令([存檔工具, 'rcs', 新建庫] + 目的地址檔案集)
        新建庫.replace(庫)
    return 庫
