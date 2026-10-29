"""고정한 공식 MicroPython 소스로 内置 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

版本版次值 = '1.24.1'
有效性验证哈希 = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 创建Python(根路径, C编译器, 链接器工具):
    名称 = 'micropython-' + 版本版次值
    存档 = 根路径 / 'vendor' / (名称 + '.tar.gz')
    if not 存档.is_file() or hashlib.sha256(存档.read_bytes()).hexdigest() != 有效性验证哈希:
        raise SystemExit('MicroPython 源代码树 缺失方法/哈希文件 불일치: ' + str(存档))
    原始数据 = 根路径 / 'build' / 名称
    if not (原始数据 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(存档)) as TAR捆绑:
            for 成员 in TAR捆绑.getmembers():
                路径 = Path(成员.name)
                if 路径.is_absolute() or '..' in 路径.parts or 路径.parts[0] != 名称:
                    raise SystemExit('안전하지 않은 源代码树 路径')
                if 成员.isfile() or 成员.isdir():
                    TAR捆绑.extract(成员, str(根路径 / 'build'))
        (原始数据 / '.jkoros-source-sha256').write_text(有效性验证哈希 + '\n')
    Newlib包含路径 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(Newlib包含路径) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 所需条件值')
    subprocess.check_call(['make', '-j2', 'CC=' + C编译器, 'LD=' + 链接器工具, 'NEWLIB_INCLUDE=' + Newlib包含路径], cwd=str(根路径 / 'Python桥接'))
