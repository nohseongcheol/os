#!/usr/bin/env python3
"""宿主 javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from 构建用户空间 import 创建用户空间
from 构建网络 import 创建网络
from 构建用例集 import 创建用例集
from 构建远程 import 创建远程

项目根 = Path(__file__).resolve().parents[1]
代码库根 = 项目根.parents[1]
构建路径 = 项目根 / 'build'


def 执行命令(参数数组):
    subprocess.check_call([str(首位值) for 首位值 in 参数数组], cwd=str(项目根))


def 运行():
    构建路径.mkdir(exist_ok=True)
    C编译器 = os.environ.get('ARM64_CC', 'clang')
    Cpp编译器 = os.environ.get('ARM64_CXX', 'clang++')
    链接器工具 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    对象文件转换器 = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    存档工具 = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for 工具集 in ('javac', C编译器, Cpp编译器, 链接器工具, 对象文件转换器, 存档工具):
        if not shutil.which(工具集):
            raise SystemExit('필요한 构建系统 工具集 缺失方法: ' + 工具集)
    字体信息 = json.loads((项目根 / 'vendor/terminal-font.json').read_text())
    字体数据 = (项目根 / 'vendor/terminal-font.bin').read_bytes()
    if len(字体数据) != 65616 * 32 or hashlib.sha256(字体数据).hexdigest() != 字体信息['sha256']:
        raise SystemExit('终端 字体值 大小/SHA256 불일치')
    导出表 = {'jshell_interactive': '命令壳输入输出.是否交互式', 'jshell_output': '命令壳输入输出.输出', 'jshell_input': '命令壳输入输出.输入值', 'java_task': '内核.任务', 'jfs_path_start': '内存文件集.路径开始',
               'jfs_path_byte': '内存文件集.路径字节', 'jfs_open': '内存文件集.打开',
               'jfs_read': '内存文件集.读取', 'jfs_write': '内存文件集.写入',
               'jfs_seek': '内存文件集.寻道位置', 'jfs_close': '内存文件集.关闭',
               'jfs_size': '内存文件集.大小', 'jfs_unlink': '内存文件集.擦除条目',
               'jfs_truncate': '内存文件集.设定长度'}
    导出表.update({'jfs_entry_count': '内存文件集.文件限制', 'jfs_entry_length': '内存文件集.已导出名称长度', 'jfs_entry_byte': '内存文件集.已导出名称字节', 'jfs_entry_size': '内存文件集.已导出文件大小'})
    导出表.update({'jdraw_prepare': '帧缓冲组合器.准备', 'jdraw_width': '帧缓冲组合器.获取宽度',
        'jdraw_height': '帧缓冲组合器.获取高度', 'jdraw_count_low': '帧缓冲组合器.获取计数器低位',
        'jdraw_count_high': '帧缓冲组合器.获取计数器高位', 'jdraw_clip': '帧缓冲组合器.裁剪',
        'jdraw_clip_value': '帧缓冲组合器.裁剪值', 'jdraw_begin': '帧缓冲组合器.运行',
        'jdraw_end': '帧缓冲组合器.结束操作', 'jdraw_pixel': '帧缓冲组合器.像素',
        'jdraw_rectangle': '帧缓冲组合器.矩形填充', 'jdraw_pointer': '帧缓冲组合器.指针'})
    导出表.update({'jfs_mkdir': '内存文件集.创建目录', 'jfs_rmdir': '内存文件集.移除目录', 'jfs_kind': '内存文件集.条目种类'})
    导出表.update({'jnet_socket': '环回网络.创建条目', 'jnet_bind': '环回网络.可执行束打包',
        'jnet_put': '环回网络.放入数据', 'jnet_get': '环回网络.读取数据', 'jnet_send': '环回网络.发送',
        'jnet_recv': '环回网络.接收', 'jnet_port': '环回网络.读取端点端口', 'jnet_address': '环回网络.读取地址',
        'jnet_peer': '环回网络.发送方端点', 'jnet_close': '环回网络.关闭'})
    导出表.update({'jstream_create': '流网络.创建条目', 'jstream_bind': '流网络.可执行束打包', 'jstream_listen': '流网络.侦听端点', 'jstream_connect': '流网络.连接', 'jstream_accept': '流网络.接受连接状态', 'jstream_read': '流网络.读取', 'jstream_write': '流网络.写入', 'jstream_port': '流网络.读取端点端口', 'jstream_peer': '流网络.读取对端端口', 'jstream_close': '流网络.关闭'})
    for 符号值 in list(导出表):
        if 符号值.startswith('jstream_') or 符号值.startswith('jnet_') and 符号值 not in ('jnet_put', 'jnet_get'):
            导出表[符号值.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = 导出表.pop(符号值)
    示例条目列 = ['public final class 软件包 { public static void 准备() {']
    for 路径 in sorted((项目根 / '用例').iterdir()):
        if 路径.is_file():
            示例条目列.append('命令解释器.静态文件(%s, %s);' %
                (json.dumps(路径.name), json.dumps(路径.read_text(encoding='utf-8'), ensure_ascii=True)))
    (构建路径 / '软件包.java').write_text('\n'.join(示例条目列 + ['}}']), encoding='utf-8')
    创建用例集(项目根, 代码库根, 执行命令)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(构建路径)) as 工作中路径:
        类路径 = Path(工作中路径)
        执行命令(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', 类路径, '-sourcepath', 类路径, '-d', 类路径] + sorted((项目根 / '源代码').glob('*.java')) + [构建路径 / '软件包.java', 构建路径 / '示例捆绑.java'])
        # 文件·命令壳·窗口 세션·통신과 Java 屏幕 합성 배열을 构建全部 수용한다.
        参数数组 = ['sh', 代码库根 / 'compiler/提前所属时间.sh', '--entry', '内核.运行', '--heap-words', '1048576', '-o', 构建路径 / 'kernel-java.c']
        for 符号值, 方法条目 in sorted(导出表.items()):
            参数数组 += ['--export', 符号值 + '=' + 方法条目]
        执行命令(参数数组 + sorted(类路径.glob('*.class')))
    (构建路径 / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    配置项位列 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    POSIX = 代码库根 / 'posix-kor/arm64-native'
    创建用户空间(项目根, 代码库根, C编译器, Cpp编译器, 链接器工具, 存档工具, 配置项位列, 执行命令)
    使用网络 = 创建网络(项目根, C编译器, 存档工具, 配置项位列, 执行命令)
    远程使用 = 创建远程(项目根, C编译器, 存档工具, 配置项位列, 执行命令)
    包含项 = ['-I', POSIX / '头文件', '-I', 构建路径]
    构建作业列 = [(C编译器, [], 构建路径 / 'terminal-font.S', 'font.o'),
            (C编译器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 项目根 / '计算机/终端.c', 'terminal.o'),
            (C编译器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 项目根 / '计算机/小组件.c', 'widgets.o'),
            (C编译器, ['-std=c11'], 构建路径 / 'kernel-java.c', 'java.o'),
            (C编译器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 项目根 / '计算机/板.c', 'board.o'),
            (C编译器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 项目根 / '计算机/屏幕绘图.c', 'drawing.o'),
            (C编译器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 项目根 / '计算机/用户.c', 'user.o'),
            (C编译器, [], 项目根 / '启动/条目分值.S', 'entry.o'),
            (C编译器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], POSIX / '连接.c', 'posix.o'),
            (Cpp编译器, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 项目根 / '测试/文件调用列.cpp', 'cpp.o')]
    for 编译器工具, 附加区域, 原始数据, 输出结果 in 构建作业列:
        原始配置项 = [文件条目 for 文件条目 in 配置项位列 if 文件条目 != '-mgeneral-regs-only'] if 原始数据.suffix == '.S' else 配置项位列
        执行命令([编译器工具] + 原始配置项 + 附加区域 + 包含项 + ['-c', 原始数据, '-o', 构建路径 / 输出结果])
    执行命令([存档工具, 'rcs', 构建路径 / 'libposix-kor-arm64.a', 构建路径 / 'posix.o'])
    执行命令([链接器工具, '--gc-sections', '-T', 项目根 / '启动/链接布局.ld', '-Map', 构建路径 / 'kernel.map', '-o', 构建路径 / 'kernel.elf'] +
        [构建路径 / 名称 for 名称 in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', 构建路径 / 'libposix-kor-arm64.a', 使用网络, 远程使用, 构建路径 / 'remote/libassh.a', 构建路径 / 'remote/libbearssl.a', '--end-group'])
    执行命令([对象文件转换器, '-O', 'binary', 构建路径 / 'kernel.elf', 构建路径 / 'kernel8.img'])
    捆绑构建清单 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': '中文.内置', 'korean_exceptions': 20,
                                 'full_awt_swing': False, 'swing_subset': ['JFrame','JPanel','JLabel','JButton','JTextField','ActionListener','SwingUtilities.invokeLater'], 'java_se_certified': False},
                'python': 'MicroPython 1.24.1 integer build', 'cpython': False,
                'pip': {'kind': 'source installer with host PyPI HTTPS relay', 'commands': ['install','list','uninstall'], 'cpython_pip': False, 'dependencies': False, 'persistent': False},
                'korean_c_api': 'independent structs, enum constants and real function symbols',
                'framebuffer': {'format': 'RGB32', 'default': [640,480], 'maximum': [1920,1080], 'boot_configurable': True, 'size_syscall': 22},
                'shell': 'UTF-8 editor/history, directories, variables, scripts, sequential pipes, redirects, ELF execution',
                'system_commands': ['ipconfig','ip','ifconfig','ping','route','netstat','ss','ps','top','free','df','uptime','poweroff'],
                'system_status': 'real lwIP interface/endpoints, native task/session PIDs, AOT heap pools, RAM filesystem slots',
                'ip_configuration': 'GENET DHCP on real Pi4; static IPv4/netmask/gateway; volatile; close active sockets before address changes',
                'ping': 'real ICMPv4 echo, numeric addresses, count/timeout/RTT; no DNS resolver',
                'poweroff': 'BCM2835 PM firmware-halt watchdog; QEMU guest shutdown; physical Pi untested',
                'pipe_capacity_bytes': 16384, 'posix_shell_complete': False,
                'ram_files': {'count': 64, 'bytes_each': 16384, 'directories': 16, 'persistent': False},
                'user_abi': 1, 'user_elf64': True, 'elf_extension_required': False,
                'linux_static_elf_subset': True, 'full_linux_binary_compatibility': False,
                'mmu': True, 'user_timeout_seconds': 2, 'cooperative_user_sessions': 4,
                'interactive_wait_renews_deadline': True, 'vi': 'native EL0 UTF-8 vi subset',
                'network': 'lwIP 2.2.0 IPv4 TCP/UDP/ARP/ICMP; GENET v5 Ethernet or UART1 SLIP', 'external_network': True,
                'external_network_transport': 'Pi4 GENET (hardware untested); QEMU auxiliary UART SLIP bridge',
                'ftp': 'guest service, passive binary transfers, anonymous root RAM workspace',
                'genet_ethernet': True, 'genet_driver_status': 'implemented; MMIO/MDIO model tests only', 'physical_network_tested': False,
                'ssh': {'implementation': 'guest libassh 1.1 / LGPL-2.1-or-later', 'port': 22, 'password_auth': True, 'console': 'shared kernel shell', 'independent_sessions': False, 'sftp': False, 'port_forwarding': False},
                'vnc': {'implementation': 'guest RFB 3.8 / VNC authentication / raw incremental tiles', 'port': 5900, 'encrypted_pixels': False, 'clients': 1, 'korean_input': 'native two-set F9/Shift+Space'},
                'rdp': False,
                'gui': 'four native terminal windows and Swing subset peers; guest VNC server with native input; optional QEMU VNC bridge',
                'native_usb_input': False, 'full_swing': False, 'swing_subset': True, 'sha256': {}}
    for 名称 in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        捆绑构建清单['sha256'][名称] = hashlib.sha256((构建路径 / 名称).read_bytes()).hexdigest()
    (构建路径 / 'build.json').write_text(json.dumps(捆绑构建清单, indent=2) + '\n')
    print('是否完成:', 构建路径 / 'kernel8.img')


if __name__ == '__main__':
    运行()
