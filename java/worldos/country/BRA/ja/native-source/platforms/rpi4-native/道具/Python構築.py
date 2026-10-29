"""고정한 공식 MicroPython 소스로 内蔵 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

言語版値 = '1.24.1'
妥当性ハッシュ = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Python作成(根経路, Cコンパイラ, 連結器道具要素):
    名前 = 'micropython-' + 言語版値
    書庫 = 根経路 / 'vendor' / (名前 + '.tar.gz')
    if not 書庫.is_file() or hashlib.sha256(書庫.read_bytes()).hexdigest() != 妥当性ハッシュ:
        raise SystemExit('MicroPython ソース木 未存在メソッド/ハッシュファイル 불일치: ' + str(書庫))
    原本データ = 根経路 / 'build' / 名前
    if not (原本データ / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(書庫)) as TAR束:
            for 成員 in TAR束.getmembers():
                経路 = Path(成員.name)
                if 経路.is_absolute() or '..' in 経路.parts or 経路.parts[0] != 名前:
                    raise SystemExit('안전하지 않은 ソース木 経路')
                if 成員.isfile() or 成員.isdir():
                    TAR束.extract(成員, str(根経路 / 'build'))
        (原本データ / '.jkoros-source-sha256').write_text(妥当性ハッシュ + '\n')
    Newlib包含経路 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(Newlib包含経路) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 必要値')
    subprocess.check_call(['make', '-j2', 'CC=' + Cコンパイラ, 'LD=' + 連結器道具要素, 'NEWLIB_INCLUDE=' + Newlib包含経路], cwd=str(根経路 / 'Python橋渡し'))
