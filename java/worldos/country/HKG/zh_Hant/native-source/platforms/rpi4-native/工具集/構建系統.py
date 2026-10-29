#!/usr/bin/env python3
"""宿主 javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from 構建用戶空間 import 創建用戶空間
from 構建網路 import 創建網路
from 構建範例集 import 創建範例集
from 構建遠程 import 創建遠程

項目根 = Path(__file__).resolve().parents[1]
代碼庫根 = 項目根.parents[1]
構建路徑 = 項目根 / 'build'


def 執行命令(實際參數陣列):
    subprocess.check_call([str(首位值) for 首位值 in 實際參數陣列], cwd=str(項目根))


def 運行():
    構建路徑.mkdir(exist_ok=True)
    C編譯器 = os.environ.get('ARM64_CC', 'clang')
    Cpp編譯器 = os.environ.get('ARM64_CXX', 'clang++')
    鏈接器工具 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    物件檔案轉換器 = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    存檔工具 = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for 工具集 in ('javac', C編譯器, Cpp編譯器, 鏈接器工具, 物件檔案轉換器, 存檔工具):
        if not shutil.which(工具集):
            raise SystemExit('필요한 構建系統 工具集 缺失方法: ' + 工具集)
    字體信息 = json.loads((項目根 / 'vendor/terminal-font.json').read_text())
    字體資料 = (項目根 / 'vendor/terminal-font.bin').read_bytes()
    if len(字體資料) != 65616 * 32 or hashlib.sha256(字體資料).hexdigest() != 字體信息['sha256']:
        raise SystemExit('終端 字體值 大小/SHA256 불일치')
    導出表 = {'jshell_interactive': '命令殼輸入輸出.是否交互式', 'jshell_output': '命令殼輸入輸出.輸出', 'jshell_input': '命令殼輸入輸出.輸入值', 'java_task': '內核.任務', 'jfs_path_start': '記憶體檔案集.路徑開始',
               'jfs_path_byte': '記憶體檔案集.路徑位元組', 'jfs_open': '記憶體檔案集.打開',
               'jfs_read': '記憶體檔案集.讀取', 'jfs_write': '記憶體檔案集.寫入',
               'jfs_seek': '記憶體檔案集.尋道位置', 'jfs_close': '記憶體檔案集.關閉',
               'jfs_size': '記憶體檔案集.大小', 'jfs_unlink': '記憶體檔案集.擦除條目',
               'jfs_truncate': '記憶體檔案集.設定長度'}
    導出表.update({'jfs_entry_count': '記憶體檔案集.檔案限制', 'jfs_entry_length': '記憶體檔案集.已導出名稱長度', 'jfs_entry_byte': '記憶體檔案集.已導出名稱位元組', 'jfs_entry_size': '記憶體檔案集.已導出檔案大小'})
    導出表.update({'jdraw_prepare': '幀緩衝組合器.準備', 'jdraw_width': '幀緩衝組合器.獲取寬度',
        'jdraw_height': '幀緩衝組合器.獲取高度', 'jdraw_count_low': '幀緩衝組合器.獲取計數器低位',
        'jdraw_count_high': '幀緩衝組合器.獲取計數器高位', 'jdraw_clip': '幀緩衝組合器.裁剪',
        'jdraw_clip_value': '幀緩衝組合器.裁剪值', 'jdraw_begin': '幀緩衝組合器.運行',
        'jdraw_end': '幀緩衝組合器.結束操作', 'jdraw_pixel': '幀緩衝組合器.像素',
        'jdraw_rectangle': '幀緩衝組合器.矩形填充', 'jdraw_pointer': '幀緩衝組合器.指針'})
    導出表.update({'jfs_mkdir': '記憶體檔案集.創建目錄', 'jfs_rmdir': '記憶體檔案集.移除目錄', 'jfs_kind': '記憶體檔案集.條目種類'})
    導出表.update({'jnet_socket': '環回網路.創建條目', 'jnet_bind': '環回網路.可執行束打包',
        'jnet_put': '環回網路.放入資料', 'jnet_get': '環回網路.讀取資料', 'jnet_send': '環回網路.發送',
        'jnet_recv': '環回網路.接收', 'jnet_port': '環回網路.讀取端點埠', 'jnet_address': '環回網路.讀取地址',
        'jnet_peer': '環回網路.發送方端點', 'jnet_close': '環回網路.關閉'})
    導出表.update({'jstream_create': '流網路.創建條目', 'jstream_bind': '流網路.可執行束打包', 'jstream_listen': '流網路.偵聽端點', 'jstream_connect': '流網路.連接', 'jstream_accept': '流網路.接受連接狀態', 'jstream_read': '流網路.讀取', 'jstream_write': '流網路.寫入', 'jstream_port': '流網路.讀取端點埠', 'jstream_peer': '流網路.讀取對端埠', 'jstream_close': '流網路.關閉'})
    for 符號值 in list(導出表):
        if 符號值.startswith('jstream_') or 符號值.startswith('jnet_') and 符號值 not in ('jnet_put', 'jnet_get'):
            導出表[符號值.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = 導出表.pop(符號值)
    範例條目列 = ['public final class 軟件包 { public static void 準備() {']
    for 路徑 in sorted((項目根 / '範例').iterdir()):
        if 路徑.is_file():
            範例條目列.append('命令解釋器.靜態檔案(%s, %s);' %
                (json.dumps(路徑.name), json.dumps(路徑.read_text(encoding='utf-8'), ensure_ascii=True)))
    (構建路徑 / '軟件包.java').write_text('\n'.join(範例條目列 + ['}}']), encoding='utf-8')
    創建範例集(項目根, 代碼庫根, 執行命令)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(構建路徑)) as 工作中路徑:
        類別路徑 = Path(工作中路徑)
        執行命令(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', 類別路徑, '-sourcepath', 類別路徑, '-d', 類別路徑] + sorted((項目根 / '原始碼').glob('*.java')) + [構建路徑 / '軟件包.java', 構建路徑 / '範例捆綁.java'])
        # 檔案·命令殼·窗口 세션·통신과 Java 屏幕 합성 배열을 構建全部 수용한다.
        實際參數陣列 = ['sh', 代碼庫根 / 'compiler/提前所屬時間.sh', '--entry', '內核.運行', '--heap-words', '1048576', '-o', 構建路徑 / 'kernel-java.c']
        for 符號值, 方法條目 in sorted(導出表.items()):
            實際參數陣列 += ['--export', 符號值 + '=' + 方法條目]
        執行命令(實際參數陣列 + sorted(類別路徑.glob('*.class')))
    (構建路徑 / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    配置項位元列 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    POSIX = 代碼庫根 / 'posix-kor/arm64-native'
    創建用戶空間(項目根, 代碼庫根, C編譯器, Cpp編譯器, 鏈接器工具, 存檔工具, 配置項位元列, 執行命令)
    使用網路 = 創建網路(項目根, C編譯器, 存檔工具, 配置項位元列, 執行命令)
    遠程使用 = 創建遠程(項目根, C編譯器, 存檔工具, 配置項位元列, 執行命令)
    包含項 = ['-I', POSIX / '頭文件', '-I', 構建路徑]
    構建作業列 = [(C編譯器, [], 構建路徑 / 'terminal-font.S', 'font.o'),
            (C編譯器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 項目根 / '計算機/終端.c', 'terminal.o'),
            (C編譯器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 項目根 / '計算機/小組件.c', 'widgets.o'),
            (C編譯器, ['-std=c11'], 構建路徑 / 'kernel-java.c', 'java.o'),
            (C編譯器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 項目根 / '計算機/板.c', 'board.o'),
            (C編譯器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 項目根 / '計算機/屏幕繪圖.c', 'drawing.o'),
            (C編譯器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 項目根 / '計算機/使用者.c', 'user.o'),
            (C編譯器, [], 項目根 / '啓動/條目分值.S', 'entry.o'),
            (C編譯器, ['-std=c11', '-Wall', '-Wextra', '-Werror'], POSIX / '連接.c', 'posix.o'),
            (Cpp編譯器, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 項目根 / '測試/檔案調用列.cpp', 'cpp.o')]
    for 編譯器工具, 附加區域, 原始資料, 輸出結果 in 構建作業列:
        原始配置項 = [檔案條目 for 檔案條目 in 配置項位元列 if 檔案條目 != '-mgeneral-regs-only'] if 原始資料.suffix == '.S' else 配置項位元列
        執行命令([編譯器工具] + 原始配置項 + 附加區域 + 包含項 + ['-c', 原始資料, '-o', 構建路徑 / 輸出結果])
    執行命令([存檔工具, 'rcs', 構建路徑 / 'libposix-kor-arm64.a', 構建路徑 / 'posix.o'])
    執行命令([鏈接器工具, '--gc-sections', '-T', 項目根 / '啓動/鏈接佈局.ld', '-Map', 構建路徑 / 'kernel.map', '-o', 構建路徑 / 'kernel.elf'] +
        [構建路徑 / 名稱 for 名稱 in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', 構建路徑 / 'libposix-kor-arm64.a', 使用網路, 遠程使用, 構建路徑 / 'remote/libassh.a', 構建路徑 / 'remote/libbearssl.a', '--end-group'])
    執行命令([物件檔案轉換器, '-O', 'binary', 構建路徑 / 'kernel.elf', 構建路徑 / 'kernel8.img'])
    捆綁構建清單 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': '中文.內建', 'korean_exceptions': 20,
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
    for 名稱 in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        捆綁構建清單['sha256'][名稱] = hashlib.sha256((構建路徑 / 名稱).read_bytes()).hexdigest()
    (構建路徑 / 'build.json').write_text(json.dumps(捆綁構建清單, indent=2) + '\n')
    print('是否完成:', 構建路徑 / 'kernel8.img')


if __name__ == '__main__':
    運行()
