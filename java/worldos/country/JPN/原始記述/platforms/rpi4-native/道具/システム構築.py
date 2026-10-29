#!/usr/bin/env python3
"""ホスト javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from 利用者空間構築 import 利用者空間作成
from 通信網構築 import 通信網作成
from 用例集構築 import 用例集作成
from 遠隔構築 import 遠隔作成

計画根 = Path(__file__).resolve().parents[1]
保管庫根 = 計画根.parents[1]
経路構築 = 計画根 / 'build'


def 命令実行(引数配列):
    subprocess.check_call([str(先頭位置値) for 先頭位置値 in 引数配列], cwd=str(計画根))


def 起動処理():
    経路構築.mkdir(exist_ok=True)
    Cコンパイラ = os.environ.get('ARM64_CC', 'clang')
    Cppコンパイラ = os.environ.get('ARM64_CXX', 'clang++')
    連結器道具要素 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    オブジェクトファイル変換器 = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    書庫道具要素 = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for 道具 in ('javac', Cコンパイラ, Cppコンパイラ, 連結器道具要素, オブジェクトファイル変換器, 書庫道具要素):
        if not shutil.which(道具):
            raise SystemExit('필요한 システム構築 道具 未存在メソッド: ' + 道具)
    書体情報 = json.loads((計画根 / 'vendor/terminal-font.json').read_text())
    書体データ = (計画根 / 'vendor/terminal-font.bin').read_bytes()
    if len(書体データ) != 65616 * 32 or hashlib.sha256(書体データ).hexdigest() != 書体情報['sha256']:
        raise SystemExit('端末 書体値 容量/SHA256 불일치')
    公開表 = {'jshell_interactive': 'シェル入出力.判定対話式', 'jshell_output': 'シェル入出力.出力', 'jshell_input': 'シェル入出力.入力値', 'java_task': '中核.作業', 'jfs_path_start': '記憶ファイル群.経路開始処理',
               'jfs_path_byte': '記憶ファイル群.経路バイト', 'jfs_open': '記憶ファイル群.開放',
               'jfs_read': '記憶ファイル群.読取', 'jfs_write': '記憶ファイル群.書込',
               'jfs_seek': '記憶ファイル群.位置位置移動', 'jfs_close': '記憶ファイル群.閉鎖',
               'jfs_size': '記憶ファイル群.容量', 'jfs_unlink': '記憶ファイル群.入口消去処理',
               'jfs_truncate': '記憶ファイル群.長さ設定'}
    公開表.update({'jfs_entry_count': '記憶ファイル群.ファイル上限', 'jfs_entry_length': '記憶ファイル群.公開済み名前長さ', 'jfs_entry_byte': '記憶ファイル群.公開済み名前バイト', 'jfs_entry_size': '記憶ファイル群.公開済みファイル容量'})
    公開表.update({'jdraw_prepare': '描画領域組立器.用意', 'jdraw_width': '描画領域組立器.幅取得',
        'jdraw_height': '描画領域組立器.高さ取得', 'jdraw_count_low': '描画領域組立器.計数器下位取得',
        'jdraw_count_high': '描画領域組立器.計数器上位取得', 'jdraw_clip': '描画領域組立器.切抜き',
        'jdraw_clip_value': '描画領域組立器.切抜き値', 'jdraw_begin': '描画領域組立器.起動処理',
        'jdraw_end': '描画領域組立器.終了処理', 'jdraw_pixel': '描画領域組立器.画素',
        'jdraw_rectangle': '描画領域組立器.矩形塗潰し', 'jdraw_pointer': '描画領域組立器.ポインタ'})
    公開表.update({'jfs_mkdir': '記憶ファイル群.ディレクトリ作成', 'jfs_rmdir': '記憶ファイル群.ディレクトリ除去', 'jfs_kind': '記憶ファイル群.入口種別'})
    公開表.update({'jnet_socket': '折返し通信網.入口作成', 'jnet_bind': '折返し通信網.実行束梱包',
        'jnet_put': '折返し通信網.データ格納', 'jnet_get': '折返し通信網.データ読取', 'jnet_send': '折返し通信網.送信',
        'jnet_recv': '折返し通信網.受取', 'jnet_port': '折返し通信網.通信端点ポート読取', 'jnet_address': '折返し通信網.番地読取',
        'jnet_peer': '折返し通信網.送信者通信端点', 'jnet_close': '折返し通信網.閉鎖'})
    公開表.update({'jstream_create': 'ストリーム通信網.入口作成', 'jstream_bind': 'ストリーム通信網.実行束梱包', 'jstream_listen': 'ストリーム通信網.通信端点接続待機', 'jstream_connect': 'ストリーム通信網.接続', 'jstream_accept': 'ストリーム通信網.接続状態受理', 'jstream_read': 'ストリーム通信網.読取', 'jstream_write': 'ストリーム通信網.書込', 'jstream_port': 'ストリーム通信網.通信端点ポート読取', 'jstream_peer': 'ストリーム通信網.通信相手ポート読取', 'jstream_close': 'ストリーム通信網.閉鎖'})
    for 記号値 in list(公開表):
        if 記号値.startswith('jstream_') or 記号値.startswith('jnet_') and 記号値 not in ('jnet_put', 'jnet_get'):
            公開表[記号値.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = 公開表.pop(記号値)
    例登録項目一覧 = ['public final class パッケージ { public static void 用意() {']
    for 経路 in sorted((計画根 / '用例').iterdir()):
        if 経路.is_file():
            例登録項目一覧.append('命令解釈器.静的ファイル(%s, %s);' %
                (json.dumps(経路.name), json.dumps(経路.read_text(encoding='utf-8'), ensure_ascii=True)))
    (経路構築 / 'パッケージ.java').write_text('\n'.join(例登録項目一覧 + ['}}']), encoding='utf-8')
    用例集作成(計画根, 保管庫根, 命令実行)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(経路構築)) as 作業中経路:
        クラス経路 = Path(作業中経路)
        命令実行(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', クラス経路, '-sourcepath', クラス経路, '-d', クラス経路] + sorted((計画根 / 'ソース').glob('*.java')) + [経路構築 / 'パッケージ.java', 経路構築 / '例束.java'])
        # ファイル·シェル·窓 세션·통신과 Java 画面 합성 배열을 全体構築 수용한다.
        引数配列 = ['sh', 保管庫根 / 'compiler/事前用時間.sh', '--entry', '中核.起動処理', '--heap-words', '1048576', '-o', 経路構築 / 'kernel-java.c']
        for 記号値, メソッド入口 in sorted(公開表.items()):
            引数配列 += ['--export', 記号値 + '=' + メソッド入口]
        命令実行(引数配列 + sorted(クラス経路.glob('*.class')))
    (経路構築 / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    構成設定ビット列 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    POSIX = 保管庫根 / 'posix-kor/arm64-native'
    利用者空間作成(計画根, 保管庫根, Cコンパイラ, Cppコンパイラ, 連結器道具要素, 書庫道具要素, 構成設定ビット列, 命令実行)
    通信使用 = 通信網作成(計画根, Cコンパイラ, 書庫道具要素, 構成設定ビット列, 命令実行)
    遠隔使用 = 遠隔作成(計画根, Cコンパイラ, 書庫道具要素, 構成設定ビット列, 命令実行)
    包含引数 = ['-I', POSIX / 'ヘッダー', '-I', 経路構築]
    仕事一覧構築 = [(Cコンパイラ, [], 経路構築 / 'terminal-font.S', 'font.o'),
            (Cコンパイラ, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 計画根 / '機械/端末.c', 'terminal.o'),
            (Cコンパイラ, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 計画根 / '機械/操作部品.c', 'widgets.o'),
            (Cコンパイラ, ['-std=c11'], 経路構築 / 'kernel-java.c', 'java.o'),
            (Cコンパイラ, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 計画根 / '機械/基板.c', 'board.o'),
            (Cコンパイラ, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 計画根 / '機械/画面描画中.c', 'drawing.o'),
            (Cコンパイラ, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 計画根 / '機械/利用者.c', 'user.o'),
            (Cコンパイラ, [], 計画根 / '起動/入口点値.S', 'entry.o'),
            (Cコンパイラ, ['-std=c11', '-Wall', '-Wextra', '-Werror'], POSIX / '接続.c', 'posix.o'),
            (Cppコンパイラ, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 計画根 / '試験/ファイル呼出し一覧.cpp', 'cpp.o')]
    for コンパイラ道具要素, 追加分領域, 原本データ, 出力結果 in 仕事一覧構築:
        原本構成設定 = [ファイル入口 for ファイル入口 in 構成設定ビット列 if ファイル入口 != '-mgeneral-regs-only'] if 原本データ.suffix == '.S' else 構成設定ビット列
        命令実行([コンパイラ道具要素] + 原本構成設定 + 追加分領域 + 包含引数 + ['-c', 原本データ, '-o', 経路構築 / 出力結果])
    命令実行([書庫道具要素, 'rcs', 経路構築 / 'libposix-kor-arm64.a', 経路構築 / 'posix.o'])
    命令実行([連結器道具要素, '--gc-sections', '-T', 計画根 / '起動/連結配置.ld', '-Map', 経路構築 / 'kernel.map', '-o', 経路構築 / 'kernel.elf'] +
        [経路構築 / 名前 for 名前 in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', 経路構築 / 'libposix-kor-arm64.a', 通信使用, 遠隔使用, 経路構築 / 'remote/libassh.a', 経路構築 / 'remote/libbearssl.a', '--end-group'])
    命令実行([オブジェクトファイル変換器, '-O', 'binary', 経路構築 / 'kernel.elf', 経路構築 / 'kernel8.img'])
    束管理目録 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': '日本語.内蔵', 'korean_exceptions': 20,
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
    for 名前 in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        束管理目録['sha256'][名前] = hashlib.sha256((経路構築 / 名前).read_bytes()).hexdigest()
    (経路構築 / 'build.json').write_text(json.dumps(束管理目録, indent=2) + '\n')
    print('判定完了:', 経路構築 / 'kernel8.img')


if __name__ == '__main__':
    起動処理()
