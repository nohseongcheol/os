#!/usr/bin/env python3
"""вузел javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from зборка_карыстальнік_ПРАБЕЛ import стварыць_карыстальнік_ПРАБЕЛ
from зборка_Сетка import стварыць_Сетка
from 예제빌드 import 예제만들기
from зборка_аддалены import стварыць_аддалены

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
зборка_шлях = 기준 / 'build'


def выканаць_каманда(аргумент_масіў):
    subprocess.check_call([str(첫째값) for 첫째값 in аргумент_масіў], cwd=str(기준))


def Выканаць():
    зборка_шлях.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    аб_ект_файл_канвертар = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Архіў_інструмент = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Інструменты in ('javac', 시언어번역기, 시플플번역기, 연결편집기, аб_ект_файл_канвертар, Архіў_інструмент):
        if not shutil.which(Інструменты):
            raise SystemExit('필요한 зборка_сістэма Інструменты 없음: ' + Інструменты)
    шрыфт_звесткі = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    шрыфт_дадзеныя = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(шрыфт_дадзеныя) != 65616 * 32 or hashlib.sha256(шрыфт_дадзеныя).hexdigest() != шрыфт_звесткі['sha256']:
        raise SystemExit('Тэрмінал шрыфт_значэнне Памер/SHA256 불일치')
    экспартаваць_табліца = {'jshell_interactive': '셸입출력.аддзел_інфармацыйных_тэхналогій_інтэрактыўны', 'jshell_output': '셸입출력.Выхад', 'jshell_input': '셸입출력.입력', 'java_task': 'ядро.작업', 'jfs_path_start': 'памяць_Файлы.шлях_Пуск',
               'jfs_path_byte': 'памяць_Файлы.шлях_байт', 'jfs_open': 'памяць_Файлы.Адкрыць',
               'jfs_read': 'памяць_Файлы.Чытанне', 'jfs_write': 'памяць_Файлы.Запіс',
               'jfs_seek': 'памяць_Файлы.옮기기', 'jfs_close': 'памяць_Файлы.Закрыць',
               'jfs_size': 'памяць_Файлы.Памер', 'jfs_unlink': 'памяць_Файлы.ачысціць_увядзенне',
               'jfs_truncate': 'памяць_Файлы.набор_даўжыня'}
    экспартаваць_табліца.update({'jfs_entry_count': 'памяць_Файлы.파일한도', 'jfs_entry_length': 'памяць_Файлы.공개이름길이', 'jfs_entry_byte': 'памяць_Файлы.공개이름바이트', 'jfs_entry_size': 'памяць_Файлы.공개파일크기'})
    экспартаваць_табліца.update({'jdraw_prepare': '화면합성.Падрыхтаваць', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.кліп',
        'jdraw_clip_value': '화면합성.кліп_значэнне', 'jdraw_begin': '화면합성.Выканаць',
        'jdraw_end': '화면합성.Гатова', 'jdraw_pixel': '화면합성.пэл',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.указальнік'})
    экспартаваць_табліца.update({'jfs_mkdir': 'памяць_Файлы.стварыць_каталог', 'jfs_rmdir': 'памяць_Файлы.выдаліць_каталог', 'jfs_kind': 'памяць_Файлы.항목종류'})
    экспартаваць_табліца.update({'jnet_socket': '되돌림망.стварыць_увядзенне', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.адправіць',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Закрыць'})
    экспартаваць_табліца.update({'jstream_create': 'паток_Сетка.стварыць_увядзенне', 'jstream_bind': 'паток_Сетка.묶기', 'jstream_listen': 'паток_Сетка.듣기', 'jstream_connect': 'паток_Сетка.Злучыцца', 'jstream_accept': 'паток_Сетка.прыняць_кантакт', 'jstream_read': 'паток_Сетка.Чытанне', 'jstream_write': 'паток_Сетка.Запіс', 'jstream_port': 'паток_Сетка.창구읽기', 'jstream_peer': 'паток_Сетка.상대창구읽기', 'jstream_close': 'паток_Сетка.Закрыць'})
    for сімвал_значэнне in list(экспартаваць_табліца):
        if сімвал_значэнне.startswith('jstream_') or сімвал_значэнне.startswith('jnet_') and сімвал_значэнне not in ('jnet_put', 'jnet_get'):
            экспартаваць_табліца[сімвал_значэнне.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = экспартаваць_табліца.pop(сімвал_значэнне)
    예제들 = ['public final class пакет { public static void Падрыхтаваць() {']
    for ШЛЯХ in sorted((기준 / '예제').iterdir()):
        if ШЛЯХ.is_file():
            예제들.append('명령해석기.статычны_файл(%s, %s);' %
                (json.dumps(ШЛЯХ.name), json.dumps(ШЛЯХ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (зборка_шлях / 'пакет.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, выканаць_каманда)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(зборка_шлях)) as 작업경로:
        клас_шлях = Path(작업경로)
        выканаць_каманда(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', клас_шлях, '-sourcepath', клас_шлях, '-d', клас_шлях] + sorted((기준 / 'КРЫНІЦА').glob('*.java')) + [зборка_шлях / 'пакет.java', зборка_шлях / '예제꾸러미.java'])
        # Файл·абалонка·акно 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        аргумент_масіў = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'ядро.Выканаць', '--heap-words', '1048576', '-o', зборка_шлях / 'kernel-java.c']
        for сімвал_значэнне, спосаб_увядзенне in sorted(экспартаваць_табліца.items()):
            аргумент_масіў += ['--export', сімвал_значэнне + '=' + спосаб_увядзенне]
        выканаць_каманда(аргумент_масіў + sorted(клас_шлях.glob('*.class')))
    (зборка_шлях / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    стварыць_карыстальнік_ПРАБЕЛ(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Архіў_інструмент, канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў, выканаць_каманда)
    Сетка = стварыць_Сетка(기준, 시언어번역기, Архіў_інструмент, канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў, выканаць_каманда)
    원격사용 = стварыць_аддалены(기준, 시언어번역기, Архіў_інструмент, канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў, выканаць_каманда)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', зборка_шлях]
    빌드작업 = [(시언어번역기, [], зборка_шлях / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'камп_ютар/Тэрмінал.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'камп_ютар/віджэт.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], зборка_шлях / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'камп_ютар/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'камп_ютар/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'камп_ютар/карыстальнік.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/увядзенне_бал_значэнне.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Злучыцца.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [файл_увядзенне for файл_увядзенне in канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў if файл_увядзенне != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў
        выканаць_каманда([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', зборка_шлях / 출력결과])
    выканаць_каманда([Архіў_інструмент, 'rcs', зборка_шлях / 'libposix-kor-arm64.a', зборка_шлях / 'posix.o'])
    выканаць_каманда([연결편집기, '--gc-sections', '-T', 기준 / '부팅/сувязь_Макет.ld', '-Map', зборка_шлях / 'kernel.map', '-o', зборка_шлях / 'kernel.elf'] +
        [зборка_шлях / Назва for Назва in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', зборка_шлях / 'libposix-kor-arm64.a', Сетка, 원격사용, зборка_шлях / 'remote/libassh.a', зборка_шлях / 'remote/libbearssl.a', '--end-group'])
    выканаць_каманда([аб_ект_файл_канвертар, '-O', 'binary', зборка_шлях / 'kernel.elf', зборка_шлях / 'kernel8.img'])
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
    for Назва in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Назва] = hashlib.sha256((зборка_шлях / Назва).read_bytes()).hexdigest()
    (зборка_шлях / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', зборка_шлях / 'kernel8.img')


if __name__ == '__main__':
    Выканаць()
