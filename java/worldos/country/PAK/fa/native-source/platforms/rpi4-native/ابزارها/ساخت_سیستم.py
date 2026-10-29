#!/usr/bin/env python3
"""میزبان javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from ساخت_کاربر_فضا import ایجاد_کاربر_فضا
from ساخت_شبکه import ایجاد_شبکه_48d29d6d
from 예제빌드 import 예제만들기
from ساخت_راه_دور import ایجاد_راه_دور

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]
مخزن_جذر = نمایش_دادن_جذر.parents[1]
ساخت_مسیر = نمایش_دادن_جذر / 'build'


def اجرا_فرمان(آرگومان_آرايه):
    subprocess.check_call([str(첫째값) for 첫째값 in آرگومان_آرايه], cwd=str(نمایش_دادن_جذر))


def اجرا_2():
    ساخت_مسیر.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    شئ_فایل_مبدل = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    آرشیو_ابزار = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ابزارها in ('javac', 시언어번역기, 시플플번역기, 연결편집기, شئ_فایل_مبدل, آرشیو_ابزار):
        if not shutil.which(ابزارها):
            raise SystemExit('필요한 ساخت_سیستم ابزارها 없음: ' + ابزارها)
    قلم_اطلاعات = json.loads((نمایش_دادن_جذر / 'vendor/terminal-font.json').read_text())
    قلم_داده_ها = (نمایش_دادن_جذر / 'vendor/terminal-font.bin').read_bytes()
    if len(قلم_داده_ها) != 65616 * 32 or hashlib.sha256(قلم_داده_ها).hexdigest() != قلم_اطلاعات['sha256']:
        raise SystemExit('پایانه قلم_مقدار اندازه/SHA256 불일치')
    صادرکردن_جدول = {'jshell_interactive': '셸입출력.فناوری_اطلاعات_محاوره_ای', 'jshell_output': '셸입출력.خروجی', 'jshell_input': '셸입출력.입력', 'java_task': 'هسته.작업', 'jfs_path_start': 'حافظه_فایل.مسیر_شروع',
               'jfs_path_byte': 'حافظه_فایل.مسیر_بایت', 'jfs_open': 'حافظه_فایل.باز_کردن',
               'jfs_read': 'حافظه_فایل.خواندن', 'jfs_write': 'حافظه_فایل.نوشتن',
               'jfs_seek': 'حافظه_فایل.جستجو_کردن_مرتب_کردن', 'jfs_close': 'حافظه_فایل.بستن',
               'jfs_size': 'حافظه_فایل.اندازه', 'jfs_unlink': 'حافظه_فایل.پاک_کردن_ورودی',
               'jfs_truncate': 'حافظه_فایل.مجموعه_طول'}
    صادرکردن_جدول.update({'jfs_entry_count': 'حافظه_فایل.파일한도', 'jfs_entry_length': 'حافظه_فایل.공개이름길이', 'jfs_entry_byte': 'حافظه_فایل.공개이름바이트', 'jfs_entry_size': 'حافظه_فایل.공개파일크기'})
    صادرکردن_جدول.update({'jdraw_prepare': '화면합성.آماده_کردن', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.کلیپ',
        'jdraw_clip_value': '화면합성.کلیپ_مقدار', 'jdraw_begin': '화면합성.اجرا_2',
        'jdraw_end': '화면합성.خاتمه', 'jdraw_pixel': '화면합성.پیکسل',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.اشاره_گر'})
    صادرکردن_جدول.update({'jfs_mkdir': 'حافظه_فایل.ایجاد_فهرست', 'jfs_rmdir': 'حافظه_فایل.حذف_فهرست', 'jfs_kind': 'حافظه_فایل.항목종류'})
    صادرکردن_جدول.update({'jnet_socket': '되돌림망.ایجاد_ورودی', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ارسال',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.بستن'})
    صادرکردن_جدول.update({'jstream_create': 'جریان_شبکه.ایجاد_ورودی', 'jstream_bind': 'جریان_شبکه.묶기', 'jstream_listen': 'جریان_شبکه.듣기', 'jstream_connect': 'جریان_شبکه.اتصال', 'jstream_accept': 'جریان_شبکه.پذیرش_اتصال', 'jstream_read': 'جریان_شبکه.خواندن', 'jstream_write': 'جریان_شبکه.نوشتن', 'jstream_port': 'جریان_شبکه.창구읽기', 'jstream_peer': 'جریان_شبکه.상대창구읽기', 'jstream_close': 'جریان_شبکه.بستن'})
    for نماد_مقدار in list(صادرکردن_جدول):
        if نماد_مقدار.startswith('jstream_') or نماد_مقدار.startswith('jnet_') and نماد_مقدار not in ('jnet_put', 'jnet_get'):
            صادرکردن_جدول[نماد_مقدار.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = صادرکردن_جدول.pop(نماد_مقدار)
    예제들 = ['public final class دسته_کردن { public static void آماده_کردن() {']
    for مسیر in sorted((نمایش_دادن_جذر / '예제').iterdir()):
        if مسیر.is_file():
            예제들.append('명령해석기.ایستا_فایل(%s, %s);' %
                (json.dumps(مسیر.name), json.dumps(مسیر.read_text(encoding='utf-8'), ensure_ascii=True)))
    (ساخت_مسیر / 'دسته_کردن.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(نمایش_دادن_جذر, مخزن_جذر, اجرا_فرمان)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(ساخت_مسیر)) as 작업경로:
        کلاس_مسیر = Path(작업경로)
        اجرا_فرمان(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', کلاس_مسیر, '-sourcepath', کلاس_مسیر, '-d', کلاس_مسیر] + sorted((نمایش_دادن_جذر / 'مبداء').glob('*.java')) + [ساخت_مسیر / 'دسته_کردن.java', ساخت_مسیر / '예제꾸러미.java'])
        # پرونده·واسط·پنجره 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        آرگومان_آرايه = ['sh', مخزن_جذر / 'compiler/미리번역.sh', '--entry', 'هسته.اجرا_2', '--heap-words', '1048576', '-o', ساخت_مسیر / 'kernel-java.c']
        for نماد_مقدار, روش_ورودی in sorted(صادرکردن_جدول.items()):
            آرگومان_آرايه += ['--export', نماد_مقدار + '=' + روش_ورودی]
        اجرا_فرمان(آرگومان_آرايه + sorted(کلاس_مسیر.glob('*.class')))
    (ساخت_مسیر / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = مخزن_جذر / 'posix-kor/arm64-native'
    ایجاد_کاربر_فضا(نمایش_دادن_جذر, مخزن_جذر, 시언어번역기, 시플플번역기, 연결편집기, آرشیو_ابزار, 설정비트, اجرا_فرمان)
    شبکه = ایجاد_شبکه_48d29d6d(نمایش_دادن_جذر, 시언어번역기, آرشیو_ابزار, 설정비트, اجرا_فرمان)
    원격사용 = ایجاد_راه_دور(نمایش_دادن_جذر, 시언어번역기, آرشیو_ابزار, 설정비트, اجرا_فرمان)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', ساخت_مسیر]
    빌드작업 = [(시언어번역기, [], ساخت_مسیر / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], نمایش_دادن_جذر / 'دستگاه/پایانه.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], نمایش_دادن_جذر / 'دستگاه/ویجت.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], ساخت_مسیر / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], نمایش_دادن_جذر / 'دستگاه/تخته_ای.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], نمایش_دادن_جذر / 'دستگاه/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], نمایش_دادن_جذر / 'دستگاه/کاربر.c', 'user.o'),
            (시언어번역기, [], نمایش_دادن_جذر / '부팅/ورودی_نقطه_مقدار.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'اتصال.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], نمایش_دادن_جذر / '시험/فایل_تماس_ها.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [فایل_ورودی for فایل_ورودی in 설정비트 if فایل_ورودی != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        اجرا_فرمان([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', ساخت_مسیر / 출력결과])
    اجرا_فرمان([آرشیو_ابزار, 'rcs', ساخت_مسیر / 'libposix-kor-arm64.a', ساخت_مسیر / 'posix.o'])
    اجرا_فرمان([연결편집기, '--gc-sections', '-T', نمایش_دادن_جذر / '부팅/پیوند_پیمایش.ld', '-Map', ساخت_مسیر / 'kernel.map', '-o', ساخت_مسیر / 'kernel.elf'] +
        [ساخت_مسیر / نام for نام in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', ساخت_مسیر / 'libposix-kor-arm64.a', شبکه, 원격사용, ساخت_مسیر / 'remote/libassh.a', ساخت_مسیر / 'remote/libbearssl.a', '--end-group'])
    اجرا_فرمان([شئ_فایل_مبدل, '-O', 'binary', ساخت_مسیر / 'kernel.elf', ساخت_مسیر / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'فارسی.بومی', 'korean_exceptions': 20,
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
    for نام in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][نام] = hashlib.sha256((ساخت_مسیر / نام).read_bytes()).hexdigest()
    (ساخت_مسیر / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', ساخت_مسیر / 'kernel8.img')


if __name__ == '__main__':
    اجرا_2()
