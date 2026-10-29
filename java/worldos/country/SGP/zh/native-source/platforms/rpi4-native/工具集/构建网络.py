from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def 创建网络(根路径, C编译器, 存档工具, 配置项位列, 执行命令):
    原始数据 = 根路径 / 'vendor/lwip/src'
    端口编号 = 根路径 / '通信网络'
    输出结果 = 根路径 / 'build/network'
    输出结果.mkdir(exist_ok=True)
    write_header(根路径, 输出结果 / 'ip_config.h')
    文件列表 = sorted((原始数据 / 'core').glob('*.c')) + sorted((原始数据 / 'core/ipv4').glob('*.c'))
    文件列表 += [原始数据 / 'netif/ethernet.c']
    文件列表 += sorted(端口编号.glob('*.c'))
    目的地址文件集 = []
    for 路径 in 文件列表:
        目的地址文件 = 输出结果 / (路径.stem + '.o')
        执行命令([C编译器] + 配置项位列 + ['-include', 输出结果 / 'ip_config.h', '-std=c11', '-I', 端口编号, '-I', 原始数据 / 'include',
             '-I', 根路径.parents[1] / 'posix-kor/arm64-native/头文件', '-c', 路径, '-o', 目的地址文件])
        目的地址文件集.append(目的地址文件)
    库 = 输出结果 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(输出结果)) as 临时路径:
        新建库=Path(临时路径)/'libnetwork.a'
        执行命令([存档工具, 'rcs', 新建库] + 目的地址文件集)
        新建库.replace(库)
    return 库
