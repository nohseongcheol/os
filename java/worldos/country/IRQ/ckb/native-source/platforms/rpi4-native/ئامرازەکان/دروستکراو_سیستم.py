#!/usr/bin/env python3
"""جێدەر javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from دروستکراو_بەکارهێنەر_مەودا import دروستکردن_بەکارهێنەر_مەودا
from دروستکراو_تۆڕ import دروستکردن_تۆڕ
from 예제빌드 import 예제만들기
from دروستکراو_دوورەدەس import دروستکردن_دوورەدەس

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
دروستکراو_گوزەر = 기준 / 'build'


def جێبەجێکردن_فەرمان(ئارگیومێنت_ڕیزی_داتا):
    subprocess.check_call([str(첫째값) for 첫째값 in ئارگیومێنت_ڕیزی_داتا], cwd=str(기준))


def ڕادان():
    دروستکراو_گوزەر.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    شت_فایل_بگۆڕ = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ئەرشیف_ئامراز = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ئامرازەکان in ('javac', 시언어번역기, 시플플번역기, 연결편집기, شت_فایل_بگۆڕ, ئەرشیف_ئامراز):
        if not shutil.which(ئامرازەکان):
            raise SystemExit('필요한 دروستکراو_سیستم ئامرازەکان 없음: ' + ئامرازەکان)
    جۆرەپیت_زانیاری = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    جۆرەپیت_دەیتا = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(جۆرەپیت_دەیتا) != 65616 * 32 or hashlib.sha256(جۆرەپیت_دەیتا).hexdigest() != جۆرەپیت_زانیاری['sha256']:
        raise SystemExit('터미널 جۆرەپیت_نرخ گۆڕینی_ئەندازە/SHA256 불일치')
    دەرهێنان_خشتە = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'کوورەک.작업', 'jfs_path_start': 'بیرگە_فایله_کان.گوزەر_دەستپێك',
               'jfs_path_byte': 'بیرگە_فایله_کان.گوزەر_بایت', 'jfs_open': 'بیرگە_فایله_کان.کردنەوە',
               'jfs_read': 'بیرگە_فایله_کان.읽기', 'jfs_write': 'بیرگە_فایله_کان.ڕایت_کردن',
               'jfs_seek': 'بیرگە_فایله_کان.옮기기', 'jfs_close': 'بیرگە_فایله_کان.داخستن',
               'jfs_size': 'بیرگە_فایله_کان.گۆڕینی_ئەندازە', 'jfs_unlink': 'بیرگە_فایله_کان.지우기',
               'jfs_truncate': 'بیرگە_فایله_کان.سێت_درێژی'}
    دەرهێنان_خشتە.update({'jfs_entry_count': 'بیرگە_فایله_کان.파일한도', 'jfs_entry_length': 'بیرگە_فایله_کان.공개이름길이', 'jfs_entry_byte': 'بیرگە_فایله_کان.공개이름바이트', 'jfs_entry_size': 'بیرگە_فایله_کان.공개파일크기'})
    دەرهێنان_خشتە.update({'jdraw_prepare': '화면합성.ئامادە_کردن_9ce364fc', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.کلیپ',
        'jdraw_clip_value': '화면합성.کلیپ_نرخ', 'jdraw_begin': '화면합성.ڕادان',
        'jdraw_end': '화면합성.تەواو', 'jdraw_pixel': '화면합성.پێڵ',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.نیشاندەر'})
    دەرهێنان_خشتە.update({'jfs_mkdir': 'بیرگە_فایله_کان.دروستکردن_ڕێبەرنامە', 'jfs_rmdir': 'بیرگە_فایله_کان.لابردن_ڕێبەرنامە', 'jfs_kind': 'بیرگە_فایله_کان.항목종류'})
    دەرهێنان_خشتە.update({'jnet_socket': '되돌림망.دروستکردن_تێنووسین', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ناردن',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.داخستن'})
    دەرهێنان_خشتە.update({'jstream_create': 'Stream_تۆڕ.دروستکردن_تێنووسین', 'jstream_bind': 'Stream_تۆڕ.묶기', 'jstream_listen': 'Stream_تۆڕ.듣기', 'jstream_connect': 'Stream_تۆڕ.لكاندن', 'jstream_accept': 'Stream_تۆڕ.قەبووڵکردن_گرێدان', 'jstream_read': 'Stream_تۆڕ.읽기', 'jstream_write': 'Stream_تۆڕ.ڕایت_کردن', 'jstream_port': 'Stream_تۆڕ.창구읽기', 'jstream_peer': 'Stream_تۆڕ.상대창구읽기', 'jstream_close': 'Stream_تۆڕ.داخستن'})
    for سیمبۆل_نرخ in list(دەرهێنان_خشتە):
        if سیمبۆل_نرخ.startswith('jstream_') or سیمبۆل_نرخ.startswith('jnet_') and سیمبۆل_نرخ not in ('jnet_put', 'jnet_get'):
            دەرهێنان_خشتە[سیمبۆل_نرخ.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = دەرهێنان_خشتە.pop(سیمبۆل_نرخ)
    예제들 = ['public final class گورزە { public static void ئامادە_کردن_9ce364fc() {']
    for گوزەر in sorted((기준 / '예제').iterdir()):
        if گوزەر.is_file():
            예제들.append('명령해석기.ستاتیک_فایل(%s, %s);' %
                (json.dumps(گوزەر.name), json.dumps(گوزەر.read_text(encoding='utf-8'), ensure_ascii=True)))
    (دروستکراو_گوزەر / 'گورزە.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, جێبەجێکردن_فەرمان)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(دروستکراو_گوزەر)) as 작업경로:
        کلاس_گوزەر = Path(작업경로)
        جێبەجێکردن_فەرمان(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', کلاس_گوزەر, '-sourcepath', کلاس_گوزەر, '-d', کلاس_گوزەر] + sorted((기준 / 'ژێدەر').glob('*.java')) + [دروستکراو_گوزەر / 'گورزە.java', دروستکراو_گوزەر / '예제꾸러미.java'])
        # فایل·توێکڵ·پەنجەرە 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ئارگیومێنت_ڕیزی_داتا = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'کوورەک.ڕادان', '--heap-words', '1048576', '-o', دروستکراو_گوزەر / 'kernel-java.c']
        for سیمبۆل_نرخ, ڕێگا_تێنووسین in sorted(دەرهێنان_خشتە.items()):
            ئارگیومێنت_ڕیزی_داتا += ['--export', سیمبۆل_نرخ + '=' + ڕێگا_تێنووسین]
        جێبەجێکردن_فەرمان(ئارگیومێنت_ڕیزی_داتا + sorted(کلاس_گوزەر.glob('*.class')))
    (دروستکراو_گوزەر / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    دروستکردن_بەکارهێنەر_مەودا(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, ئەرشیف_ئامراز, 설정비트, جێبەجێکردن_فەرمان)
    تۆڕ = دروستکردن_تۆڕ(기준, 시언어번역기, ئەرشیف_ئامراز, 설정비트, جێبەجێکردن_فەرمان)
    원격사용 = دروستکردن_دوورەدەس(기준, 시언어번역기, ئەرشیف_ئامراز, 설정비트, جێبەجێکردن_فەرمان)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', دروستکراو_گوزەر]
    빌드작업 = [(시언어번역기, [], دروستکراو_گوزەر / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'مەکینه/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'مەکینه/ویدجێت.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], دروستکراو_گوزەر / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'مەکینه/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'مەکینه/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'مەکینه/بەکارهێنەر.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/تێنووسین_خاڵ_نرخ.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'لكاندن.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [فایل_تێنووسین for فایل_تێنووسین in 설정비트 if فایل_تێنووسین != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        جێبەجێکردن_فەرمان([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', دروستکراو_گوزەر / 출력결과])
    جێبەجێکردن_فەرمان([ئەرشیف_ئامراز, 'rcs', دروستکراو_گوزەر / 'libposix-kor-arm64.a', دروستکراو_گوزەر / 'posix.o'])
    جێبەجێکردن_فەرمان([연결편집기, '--gc-sections', '-T', 기준 / '부팅/لینك_ڕیزبەست.ld', '-Map', دروستکراو_گوزەر / 'kernel.map', '-o', دروستکراو_گوزەر / 'kernel.elf'] +
        [دروستکراو_گوزەر / ناو for ناو in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', دروستکراو_گوزەر / 'libposix-kor-arm64.a', تۆڕ, 원격사용, دروستکراو_گوزەر / 'remote/libassh.a', دروستکراو_گوزەر / 'remote/libbearssl.a', '--end-group'])
    جێبەجێکردن_فەرمان([شت_فایل_بگۆڕ, '-O', 'binary', دروستکراو_گوزەر / 'kernel.elf', دروستکراو_گوزەر / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': '한국어.자체', 'korean_exceptions': 20,
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
    for ناو in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][ناو] = hashlib.sha256((دروستکراو_گوزەر / ناو).read_bytes()).hexdigest()
    (دروستکراو_گوزەر / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', دروستکراو_گوزەر / 'kernel8.img')


if __name__ == '__main__':
    ڕادان()
