#!/usr/bin/env python3
"""مهمان javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from گڏ_ڪريو_صارف_جڳهه import ٺاھيو_صارف_جڳهه
from گڏ_ڪريو_نيٽ_ورڪ import ٺاھيو_نيٽ_ورڪ_48d29d6d
from 예제빌드 import 예제만들기
from گڏ_ڪريو_بعيد import ٺاھيو_بعيد

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
گڏ_ڪريو_راههه = 기준 / 'build'


def تعميل_ڪرڻ_حڪم(دليل_ترتيب):
    subprocess.check_call([str(첫째값) for 첫째값 in دليل_ترتيب], cwd=str(기준))


def هلائڻ():
    گڏ_ڪريو_راههه.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    عنصر_فائل_تبديل_ڪندڙ = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    محفوظ_ٽول = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for اوزار in ('javac', 시언어번역기, 시플플번역기, 연결편집기, عنصر_فائل_تبديل_ڪندڙ, محفوظ_ٽول):
        if not shutil.which(اوزار):
            raise SystemExit('필요한 گڏ_ڪريو_سسٽم اوزار 없음: ' + اوزار)
    فانٽ_معلومات = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    فانٽ_ڪوائف = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(فانٽ_ڪوائف) != 65616 * 32 or hashlib.sha256(فانٽ_ڪوائف).hexdigest() != فانٽ_معلومات['sha256']:
        raise SystemExit('터미널 فانٽ_قدر سائيز/SHA256 불일치')
    برآمد_جدول = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'ڪرنل.작업', 'jfs_path_start': 'ميموري_فائلون.راههه_شروع',
               'jfs_path_byte': 'ميموري_فائلون.راههه_بائٽ', 'jfs_open': 'ميموري_فائلون.ٺاھيو',
               'jfs_read': 'ميموري_فائلون.읽기', 'jfs_write': 'ميموري_فائلون.لکو',
               'jfs_seek': 'ميموري_فائلون.옮기기', 'jfs_close': 'ميموري_فائلون.بند_ڪرڻ',
               'jfs_size': 'ميموري_فائلون.سائيز', 'jfs_unlink': 'ميموري_فائلون.지우기',
               'jfs_truncate': 'ميموري_فائلون.سيٽ_لمبائي'}
    برآمد_جدول.update({'jfs_entry_count': 'ميموري_فائلون.파일한도', 'jfs_entry_length': 'ميموري_فائلون.공개이름길이', 'jfs_entry_byte': 'ميموري_فائلون.공개이름바이트', 'jfs_entry_size': 'ميموري_فائلون.공개파일크기'})
    برآمد_جدول.update({'jdraw_prepare': '화면합성.تياري_ڪريو', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.تراشه',
        'jdraw_clip_value': '화면합성.تراشه_قدر', 'jdraw_begin': '화면합성.هلائڻ',
        'jdraw_end': '화면합성.ختم_ڪريو', 'jdraw_pixel': '화면합성.پيل',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.پوائنٽر'})
    برآمد_جدول.update({'jfs_mkdir': 'ميموري_فائلون.ٺاھيو_ڊائريڪٽري', 'jfs_rmdir': 'ميموري_فائلون.هٽايو_ڊائريڪٽري', 'jfs_kind': 'ميموري_فائلون.항목종류'})
    برآمد_جدول.update({'jnet_socket': '되돌림망.ٺاھيو_داخلا', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.اي_ميل',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.بند_ڪرڻ'})
    برآمد_جدول.update({'jstream_create': 'اسٽريم_نيٽ_ورڪ.ٺاھيو_داخلا', 'jstream_bind': 'اسٽريم_نيٽ_ورڪ.묶기', 'jstream_listen': 'اسٽريم_نيٽ_ورڪ.듣기', 'jstream_connect': 'اسٽريم_نيٽ_ورڪ.ڪنيڪٽ', 'jstream_accept': 'اسٽريم_نيٽ_ورڪ.قبول_ڪريو_ڪنيڪشن', 'jstream_read': 'اسٽريم_نيٽ_ورڪ.읽기', 'jstream_write': 'اسٽريم_نيٽ_ورڪ.لکو', 'jstream_port': 'اسٽريم_نيٽ_ورڪ.창구읽기', 'jstream_peer': 'اسٽريم_نيٽ_ورڪ.상대창구읽기', 'jstream_close': 'اسٽريم_نيٽ_ورڪ.بند_ڪرڻ'})
    for نشاني_قدر in list(برآمد_جدول):
        if نشاني_قدر.startswith('jstream_') or نشاني_قدر.startswith('jnet_') and نشاني_قدر not in ('jnet_put', 'jnet_get'):
            برآمد_جدول[نشاني_قدر.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = برآمد_جدول.pop(نشاني_قدر)
    예제들 = ['public final class بنڊل { public static void تياري_ڪريو() {']
    for راههه in sorted((기준 / '예제').iterdir()):
        if راههه.is_file():
            예제들.append('명령해석기.ساقط_فائل(%s, %s);' %
                (json.dumps(راههه.name), json.dumps(راههه.read_text(encoding='utf-8'), ensure_ascii=True)))
    (گڏ_ڪريو_راههه / 'بنڊل.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, تعميل_ڪرڻ_حڪم)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(گڏ_ڪريو_راههه)) as 작업경로:
        درجو_راههه = Path(작업경로)
        تعميل_ڪرڻ_حڪم(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', درجو_راههه, '-sourcepath', درجو_راههه, '-d', درجو_راههه] + sorted((기준 / 'ماخذ').glob('*.java')) + [گڏ_ڪريو_راههه / 'بنڊل.java', گڏ_ڪريو_راههه / '예제꾸러미.java'])
        # فائل·شيل·دري 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        دليل_ترتيب = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'ڪرنل.هلائڻ', '--heap-words', '1048576', '-o', گڏ_ڪريو_راههه / 'kernel-java.c']
        for نشاني_قدر, طريقو_داخلا in sorted(برآمد_جدول.items()):
            دليل_ترتيب += ['--export', نشاني_قدر + '=' + طريقو_داخلا]
        تعميل_ڪرڻ_حڪم(دليل_ترتيب + sorted(درجو_راههه.glob('*.class')))
    (گڏ_ڪريو_راههه / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    ٺاھيو_صارف_جڳهه(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, محفوظ_ٽول, 설정비트, تعميل_ڪرڻ_حڪم)
    نيٽ_ورڪ = ٺاھيو_نيٽ_ورڪ_48d29d6d(기준, 시언어번역기, محفوظ_ٽول, 설정비트, تعميل_ڪرڻ_حڪم)
    원격사용 = ٺاھيو_بعيد(기준, 시언어번역기, محفوظ_ٽول, 설정비트, تعميل_ڪرڻ_حڪم)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', گڏ_ڪريو_راههه]
    빌드작업 = [(시언어번역기, [], گڏ_ڪريو_راههه / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'مشين/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'مشين/وجيٽ.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], گڏ_ڪريو_راههه / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'مشين/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'مشين/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'مشين/صارف.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/داخلا_هنڌ_قدر.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'ڪنيڪٽ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [فائل_داخلا for فائل_داخلا in 설정비트 if فائل_داخلا != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        تعميل_ڪرڻ_حڪم([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', گڏ_ڪريو_راههه / 출력결과])
    تعميل_ڪرڻ_حڪم([محفوظ_ٽول, 'rcs', گڏ_ڪريو_راههه / 'libposix-kor-arm64.a', گڏ_ڪريو_راههه / 'posix.o'])
    تعميل_ڪرڻ_حڪم([연결편집기, '--gc-sections', '-T', 기준 / '부팅/ڪڙي_لي_آئوٽ.ld', '-Map', گڏ_ڪريو_راههه / 'kernel.map', '-o', گڏ_ڪريو_راههه / 'kernel.elf'] +
        [گڏ_ڪريو_راههه / نالو for نالو in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', گڏ_ڪريو_راههه / 'libposix-kor-arm64.a', نيٽ_ورڪ, 원격사용, گڏ_ڪريو_راههه / 'remote/libassh.a', گڏ_ڪريو_راههه / 'remote/libbearssl.a', '--end-group'])
    تعميل_ڪرڻ_حڪم([عنصر_فائل_تبديل_ڪندڙ, '-O', 'binary', گڏ_ڪريو_راههه / 'kernel.elf', گڏ_ڪريو_راههه / 'kernel8.img'])
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
    for نالو in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][نالو] = hashlib.sha256((گڏ_ڪريو_راههه / نالو).read_bytes()).hexdigest()
    (گڏ_ڪريو_راههه / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', گڏ_ڪريو_راههه / 'kernel8.img')


if __name__ == '__main__':
    هلائڻ()
