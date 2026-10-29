"""독립된 内置 ABI ELF64와 로더 拒绝值 测试 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 构建Python import 创建Python
from 构建Java库 import 创建Java库
from 构建C编译器 import 创建C编译器


def 创建用户空间(根路径, 代码库路径, C编译器, Cpp编译器, 链接器工具, 存档工具, 配置项位列, 执行命令):
    配置项位列 = [设置值 for 设置值 in 配置项位列 if 设置值 != '-mgeneral-regs-only']
    构建路径 = 根路径 / 'build'
    输出结果 = 构建路径 / 'user'
    输出结果.mkdir(exist_ok=True)
    原始数据 = 根路径 / '用户'
    POSIX = 代码库路径 / 'posix-kor/arm64-native'
    包含路径 = ['-I', 原始数据, '-I', POSIX / '头文件', '-I', 输出结果]
    for 编译器工具, 附加区域, 路径, 名称 in [
            (C编译器, [], 原始数据 / '运行.S', 'start.o'),
            (C编译器, ['-std=c11'], 原始数据 / '执行命令.c', 'runtime.o'),
            (C编译器, ['-std=c11'], POSIX / '用户桥接.c', 'posix.o'),
            (Cpp编译器, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 原始数据 / '文件例.cpp', 'demo.o'),
            (Cpp编译器, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 原始数据 / '通信示例.cpp', 'network.o'),
            (C编译器, ['-std=c11'], 原始数据 / '保护测试.c', 'fault.o'),
            (C编译器, ['-std=c11'], 原始数据 / '编辑器.c', 'vi.o')]:
        执行命令([编译器工具] + 配置项位列 + 附加区域 + 包含路径 + ['-Wall', '-Wextra', '-Werror', '-c', 路径, '-o', 输出结果 / 名称])
    执行命令([存档工具, 'rcs', 构建路径 / 'libposix-kor-user.a', 输出结果 / 'posix.o'])
    for 名称 in ('demo', 'fault', 'network', 'vi'):
        执行命令([链接器工具, '-T', 原始数据 / '链接布局.ld', '-z', 'max-page-size=4096', '-o', 输出结果 / (名称 + '.elf'),
             输出结果 / 'start.o', 输出结果 / 'runtime.o', 输出结果 / (名称 + '.o'), 构建路径 / 'libposix-kor-user.a'])
    创建Java库(根路径, 执行命令)
    # 기존 内置 Java 编译器/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(构建路径)) as 工作中路径:
        类路径 = Path(工作中路径)
        执行命令(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', 类路径, '-sourcepath', 类路径, '-d', 类路径] +
            [数据位置 for 数据位置 in sorted((代码库路径 / 'os/用户/Java').glob('*.java')) if 数据位置.name != 'Java虚拟机.java'] + sorted((原始数据 / 'Java').glob('*.java')))
        执行命令(['sh', 代码库路径 / 'compiler/提前所属时间.sh', '--entry', '工具条目.运行',
             '--profile', 'user', '--heap-words', '1048576', '-o', 输出结果 / 'java-tools.c'] + sorted(类路径.glob('*.class')))
    解压库 = 根路径 / 'vendor/uzlib'
    for 路径, 名称 in [(输出结果 / 'java-tools.c', 'java-tools.o'), (原始数据 / 'Java桥接.c', 'java-link.o'),
                       (原始数据 / '软件包.c', 'jar.o')] + [(解压库 / (名称 + '.c'), 名称 + '.o') for 名称 in ('tinflate', 'crc32', 'adler32')]:
        执行命令([C编译器] + 配置项位列 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 解压库] + 包含路径 + ['-c', 路径, '-o', 输出结果 / 名称])
    执行命令([链接器工具, '-T', 原始数据 / '链接布局.ld', '-z', 'max-page-size=4096', '-o', 输出结果 / 'java-tools.elf'] +
        [输出结果 / 名称 for 名称 in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    创建Python(根路径, C编译器, 链接器工具)
    创建C编译器(根路径, 代码库路径, C编译器, 链接器工具, 配置项位列, 执行命令)
    有效 = (输出结果 / 'demo.elf').read_bytes()
    程序头部偏移 = struct.unpack_from('<Q', 有效, 32)[0]
    头部列表 = [程序头部偏移 + 项目个数 * 56 for 项目个数 in range(struct.unpack_from('<H', 有效, 56)[0])]
    载入项 = [数据位置 for 数据位置 in 头部列表 if struct.unpack_from('<I', 有效, 数据位置)[0] == 1]
    文本, 数据 = 载入项[:2]
    命令地址 = struct.unpack_from('<Q', 有效, 文本 + 16)[0]
    数据地址 = struct.unpack_from('<Q', 有效, 数据 + 16)[0]
    调用ABI = 有效.index(b'JKOROS\0')
    测试情况 = [('empty', b''), ('short', 有效[:63])]
    修改列 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', 命令地址 + 1), ('data-entry', 24, 'Q', 数据地址),
               ('outside-file', 文本 + 32, 'Q', len(有效) + 1), ('short-memory', 文本 + 40, 'Q', 1),
               ('kernel-address', 文本 + 16, 'Q', 0x80000), ('memory-overflow', 文本 + 40, 'Q', 2**64 - 1),
               ('writable-code', 文本 + 4, 'I', 7), ('missing-abi', 调用ABI, 'B', ord('X')),
               ('wrong-abi', 调用ABI + 8, 'I', 2), ('dynamic', 文本, 'I', 2),
               ('unaligned-load', 文本 + 16, 'Q', 命令地址 + 8),
               ('overlap', 数据 + 16, 'Q', 命令地址)]
    for 名称, 偏移值, 数据格式, 值 in 修改列:
        已更改 = bytearray(有效); struct.pack_into('<' + 数据格式, 已更改, 偏移值, 值)
        测试情况.append((名称, bytes(已更改)))
    二进制块集 = [(名称.replace('-', '_'), 输出结果 / (名称 + '.elf')) for 名称 in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 查找索引, (名称, 载荷数据数据) in enumerate(测试情况):
        路径 = 输出结果 / ('invalid-{}.elf'.format(名称)); 路径.write_bytes(载荷数据数据)
        二进制块集.append(('invalid_{}'.format(查找索引), 路径))
    汇编, 头部值 = ['.section .rodata.user,"a"'], []
    大小列 = {}
    for 名称, 路径 in 二进制块集:
        符号值 = 'user_blob_' + 名称
        大小列[名称] = 路径.stat().st_size
        # 생성한 对端值 경로만 넣어 프로젝트 경로의 공백/引号 영향을 피한다.
        汇编 += ['.balign 16', '.global ' + 符号值, 符号值 + ':', '.incbin "{}"'.format(路径.relative_to(根路径))]
        头部值.append('extern const unsigned char {}[];'.format(符号值))
    汇编.append('.section .note.GNU-stack,"",%progbits')
    头部值 += ['static const 执行条目 可执行文件条目列[] = {', '{user_blob_demo, %d, 0},' % 大小列['demo']]
    头部值 += ['{user_blob_fault, %d, %d},' % (大小列['fault'], 已转发值) for 已转发值 in range(8)]
    头部值 += ['{user_blob_network, %d, 0},' % 大小列['network']]
    头部值 += ['{user_blob_java_tools, %d, %d},' % (大小列['java_tools'], 方法模式) for 方法模式 in (0, 1)]
    头部值 += ['{user_blob_python, %d, 0},' % 大小列['python'], '{user_blob_vi, %d, 0},' % 大小列['vi']]
    头部值 += ['{user_blob_java_tools, %d, 2},' % 大小列['java_tools']]
    头部值 += ['{user_blob_cc, %d, 0},' % 大小列['cc']]
    头部值 += ['{user_blob_cc, %d, 1},' % 大小列['cc']]
    头部值 += ['};', 'static const 执行条目 无效可执行项列[] = {']
    头部值 += ['{user_blob_invalid_%d, %d, 0},' % (序数索引, len(载荷数据数据)) for 序数索引, (_, 载荷数据数据) in enumerate(测试情况)]
    头部值 += ['};']
    (构建路径 / 'programs.S').write_text('\n'.join(汇编) + '\n')
    (构建路径 / 'programs.h').write_text('\n'.join(头部值) + '\n')
    (输出结果 / 'invalid-cases.txt').write_text('\n'.join(名称 for 名称, _ in 测试情况) + '\n')
    执行命令([C编译器] + 配置项位列 + ['-c', 构建路径 / 'programs.S', '-o', 构建路径 / 'programs.o'])
