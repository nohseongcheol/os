#!/usr/bin/env python3
"""分发值 자료만으로 LGPL 재연결과 수정한 TinyCC의 实际数据 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from 执行命令 import 项目根, 命令


def 运行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--sdk', type=Path, default=项目根.parent / 'rpi4/build/rootfs')
    实参 = 解析器.parse_args()
    输出 = 项目根 / 'build/verification/cosl-relink'
    输出.mkdir(parents=True, exist_ok=True)
    报告值 = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((项目根 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 临时值:
            路径 = Path(临时值)
            with tarfile.open(str(项目根 / 'dist/jkoros-native-relink.tar.gz')) as 组值:
                for 条目值 in 组值.getmembers():
                    if 路径 not in (路径 / 条目值.name).resolve().parents or 条目值.issym() or 条目值.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + 条目值.name)
                组值.extractall(str(路径))
            源代码 = 路径 / 'jkoros-native-relink'
            def 重新连接端点(名称, 参数列列表):
                with (输出 / 名称).open('wb') as 日志记录:
                    subprocess.run(['python3', 'relink.py'] + 参数列列表, cwd=str(源代码),
                                   stdout=日志记录, stderr=subprocess.STDOUT, check=True, timeout=180)
            重新连接端点('original.log', ['--verify'])
            报告值['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            编译器工具 = 源代码 / 'vendor/tinycc/libtcc.c'
            主体文本 = 编译器工具.read_text()
            位置 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert 主体文本.count(位置) == 1
            编译器工具.write_text(主体文本.replace(位置, 位置 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            重新连接端点('modified-tinycc.log', ['--tinycc', '--sdk', str(实参.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            映像值 = 源代码 / 'build/relinked/kernel8.img'
            报告值['modified_kernel_sha256'] = hashlib.sha256(映像值.read_bytes()).hexdigest()
            assert 报告值['modified_kernel_sha256'] != 报告值['kernel_sha256']
            报告值['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            参数列列表 = 命令()
            参数列列表[参数列列表.index('-kernel') + 1] = str(映像值)
            进程值 = subprocess.Popen(参数列列表 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            日志记录 = bytearray()
            选中状态值 = selectors.DefaultSelector()
            选中状态值.register(进程值.stdout, selectors.EVENT_READ)
            def 等待状态状态(显示值=b'jkoros-native> ', 初始项目=0):
                结尾 = time.monotonic() + 40
                while 显示值 not in 日志记录[初始项目:]:
                    if time.monotonic() > 结尾 or 进程值.poll() is not None:
                        raise AssertionError('Missing ' + repr(显示值) + '\n' + 日志记录[初始项目:].decode('utf-8', 'replace'))
                    for 条目值, _ in 选中状态值.select(.1):
                        数据 = 条目值.fileobj.read(65536)
                        if 数据:
                            日志记录.extend(数据)
                return bytes(日志记录[初始项目:])
            def 发送(机器字文本, 显示值=b'jkoros-native> '):
                初始项目 = len(日志记录)
                进程值.stdin.write(机器字文本.encode() + b'\n')
                进程值.stdin.flush()
                return 等待状态状态(显示值, 初始项目)
            try:
                等待状态状态()
                测试 = '#include <文件ABI.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return 写入文件数据(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                发送('load /relink.c', b'hex> ')
                for 位置索引 in range(0, len(测试), 64):
                    发送(测试[位置索引:位置索引+64].hex(), b'hex> ')
                assert b'LOADED' in 发送('.')
                结果 = 发送('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 结果, 结果
                结果 = 发送('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 结果 and b'exit 0' in 结果, 结果
                报告值['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                选中状态值.close()
                if 进程值.poll() is None:
                    进程值.terminate()
                    try:
                        进程值.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        进程值.kill()
                        进程值.wait()
                (输出 / 'guest.log').write_bytes(日志记录)
        报告值['passed'] = True
        print(json.dumps(报告值, ensure_ascii=False, indent=2))
    finally:
        (输出 / 'report.json').write_text(json.dumps(报告值, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    运行()
