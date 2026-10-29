"""고정한 공식 MicroPython 소스로 內建 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

版本版次值 = '1.24.1'
有效性驗證哈希 = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 創建Python(根路徑, C編譯器, 鏈接器工具):
    名稱 = 'micropython-' + 版本版次值
    存檔 = 根路徑 / 'vendor' / (名稱 + '.tar.gz')
    if not 存檔.is_file() or hashlib.sha256(存檔.read_bytes()).hexdigest() != 有效性驗證哈希:
        raise SystemExit('MicroPython 原始碼樹 缺失方法/哈希檔案 불일치: ' + str(存檔))
    原始資料 = 根路徑 / 'build' / 名稱
    if not (原始資料 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(存檔)) as TAR捆綁:
            for 成員 in TAR捆綁.getmembers():
                路徑 = Path(成員.name)
                if 路徑.is_absolute() or '..' in 路徑.parts or 路徑.parts[0] != 名稱:
                    raise SystemExit('안전하지 않은 原始碼樹 路徑')
                if 成員.isfile() or 成員.isdir():
                    TAR捆綁.extract(成員, str(根路徑 / 'build'))
        (原始資料 / '.jkoros-source-sha256').write_text(有效性驗證哈希 + '\n')
    Newlib包含路徑 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(Newlib包含路徑) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 所需條件值')
    subprocess.check_call(['make', '-j2', 'CC=' + C編譯器, 'LD=' + 鏈接器工具, 'NEWLIB_INCLUDE=' + Newlib包含路徑], cwd=str(根路徑 / 'Python橋接'))
