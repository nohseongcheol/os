#!/usr/bin/env python3
"""хост javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from компилация_потребител_ИНТЕРВАЛ import Създаване_потребител_ИНТЕРВАЛ
from компилация_мрежа import Създаване_мрежа
from 예제빌드 import 예제만들기
from компилация_отдалечен import Създаване_отдалечен

проект_корен = Path(__file__).resolve().parents[1]
хранилище_корен = проект_корен.parents[1]
компилация_път = проект_корен / 'build'


def изпълнявам_команда(аргумент_масив):
    subprocess.check_call([str(첫째값) for 첫째값 in аргумент_масив], cwd=str(проект_корен))


def Стартиране():
    компилация_път.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    обект_Файл_конвертор = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Архив_инструмент = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Инструменти in ('javac', 시언어번역기, 시플플번역기, 연결편집기, обект_Файл_конвертор, Архив_инструмент):
        if not shutil.which(Инструменти):
            raise SystemExit('필요한 компилация_система Инструменти 없음: ' + Инструменти)
    шрифт_инфо = json.loads((проект_корен / 'vendor/terminal-font.json').read_text())
    шрифт_данни = (проект_корен / 'vendor/terminal-font.bin').read_bytes()
    if len(шрифт_данни) != 65616 * 32 or hashlib.sha256(шрифт_данни).hexdigest() != шрифт_инфо['sha256']:
        raise SystemExit('Терминал шрифт_стойност Размер/SHA256 불일치')
    експортирам_таблица = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.Изход', 'jshell_input': '셸입출력.입력', 'java_task': 'ядро.작업', 'jfs_path_start': 'Памет_Файлове.път_Старт',
               'jfs_path_byte': 'Памет_Файлове.път_байт', 'jfs_open': 'Памет_Файлове.Отваряне',
               'jfs_read': 'Памет_Файлове.Четене', 'jfs_write': 'Памет_Файлове.Писане',
               'jfs_seek': 'Памет_Файлове.търся_позиция', 'jfs_close': 'Памет_Файлове.Затворен',
               'jfs_size': 'Памет_Файлове.Размер', 'jfs_unlink': 'Памет_Файлове.изтривам_запис',
               'jfs_truncate': 'Памет_Файлове.길이정하기'}
    експортирам_таблица.update({'jfs_entry_count': 'Памет_Файлове.파일한도', 'jfs_entry_length': 'Памет_Файлове.공개이름길이', 'jfs_entry_byte': 'Памет_Файлове.공개이름바이트', 'jfs_entry_size': 'Памет_Файлове.공개파일크기'})
    експортирам_таблица.update({'jdraw_prepare': '화면합성.Подготвяне', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.клип',
        'jdraw_clip_value': '화면합성.клип_стойност', 'jdraw_begin': '화면합성.Стартиране',
        'jdraw_end': '화면합성.Готово', 'jdraw_pixel': '화면합성.пиксел',
        'jdraw_rectangle': '화면합성.правоъгълник_запълване', 'jdraw_pointer': '화면합성.показалец'})
    експортирам_таблица.update({'jfs_mkdir': 'Памет_Файлове.Създаване_указател', 'jfs_rmdir': 'Памет_Файлове.премахвам_указател', 'jfs_kind': 'Памет_Файлове.항목종류'})
    експортирам_таблица.update({'jnet_socket': 'обръщане_към_себе_си_за_компютър_в_мрежа_мрежа.Създаване_запис', 'jnet_bind': 'обръщане_към_себе_си_за_компютър_в_мрежа_мрежа.обвързвам_участник',
        'jnet_put': 'обръщане_към_себе_си_за_компютър_в_мрежа_мрежа.자료넣기', 'jnet_get': 'обръщане_към_себе_си_за_компютър_в_мрежа_мрежа.자료읽기', 'jnet_send': 'обръщане_към_себе_си_за_компютър_в_мрежа_мрежа.изпращам',
        'jnet_recv': 'обръщане_към_себе_си_за_компютър_в_мрежа_мрежа.получавам', 'jnet_port': 'обръщане_към_себе_си_за_компютър_в_мрежа_мрежа.창구읽기', 'jnet_address': 'обръщане_към_себе_си_за_компютър_в_мрежа_мрежа.주소읽기',
        'jnet_peer': 'обръщане_към_себе_си_за_компютър_в_мрежа_мрежа.подател_участник', 'jnet_close': 'обръщане_към_себе_си_за_компютър_в_мрежа_мрежа.Затворен'})
    експортирам_таблица.update({'jstream_create': 'поток_мрежа.Създаване_запис', 'jstream_bind': 'поток_мрежа.обвързвам_участник', 'jstream_listen': 'поток_мрежа.чакам_участник', 'jstream_connect': 'поток_мрежа.Свързване', 'jstream_accept': 'поток_мрежа.приемам_връзка', 'jstream_read': 'поток_мрежа.Четене', 'jstream_write': 'поток_мрежа.Писане', 'jstream_port': 'поток_мрежа.창구읽기', 'jstream_peer': 'поток_мрежа.상대창구읽기', 'jstream_close': 'поток_мрежа.Затворен'})
    for символ_стойност in list(експортирам_таблица):
        if символ_стойност.startswith('jstream_') or символ_стойност.startswith('jnet_') and символ_стойност not in ('jnet_put', 'jnet_get'):
            експортирам_таблица[символ_стойност.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = експортирам_таблица.pop(символ_стойност)
    예제들 = ['public final class пакет { public static void Подготвяне() {']
    for ПЪТ in sorted((проект_корен / '예제').iterdir()):
        if ПЪТ.is_file():
            예제들.append('명령해석기.정적파일(%s, %s);' %
                (json.dumps(ПЪТ.name), json.dumps(ПЪТ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (компилация_път / 'пакет.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(проект_корен, хранилище_корен, изпълнявам_команда)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(компилация_път)) as 작업경로:
        Клас_път = Path(작업경로)
        изпълнявам_команда(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Клас_път, '-sourcepath', Клас_път, '-d', Клас_път] + sorted((проект_корен / 'ИЗТОЧНИК').glob('*.java')) + [компилация_път / 'пакет.java', компилация_път / '예제꾸러미.java'])
        # Файл·обвивка·Прозорец 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        аргумент_масив = ['sh', хранилище_корен / 'compiler/미리번역.sh', '--entry', 'ядро.Стартиране', '--heap-words', '1048576', '-o', компилация_път / 'kernel-java.c']
        for символ_стойност, метод_запис in sorted(експортирам_таблица.items()):
            аргумент_масив += ['--export', символ_стойност + '=' + метод_запис]
        изпълнявам_команда(аргумент_масив + sorted(Клас_път.glob('*.class')))
    (компилация_път / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = хранилище_корен / 'posix-kor/arm64-native'
    Създаване_потребител_ИНТЕРВАЛ(проект_корен, хранилище_корен, 시언어번역기, 시플플번역기, 연결편집기, Архив_инструмент, конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим, изпълнявам_команда)
    мрежа = Създаване_мрежа(проект_корен, 시언어번역기, Архив_инструмент, конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим, изпълнявам_команда)
    отдалечен_използвам = Създаване_отдалечен(проект_корен, 시언어번역기, Архив_инструмент, конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим, изпълнявам_команда)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', компилация_път]
    빌드작업 = [(시언어번역기, [], компилация_път / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], проект_корен / 'машина/Терминал.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], проект_корен / 'машина/изпълним_модул.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], компилация_път / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], проект_корен / 'машина/Табло.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], проект_корен / 'машина/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], проект_корен / 'машина/потребител.c', 'user.o'),
            (시언어번역기, [], проект_корен / '부팅/запис_пункт_стойност.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Свързване.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], проект_корен / '시험/Файл_Обаждания.cpp', 'cpp.o')]
    for компилатор_инструмент, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [Файл_запис for Файл_запис in конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим if Файл_запис != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим
        изпълнявам_команда([компилатор_инструмент] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', компилация_път / 출력결과])
    изпълнявам_команда([Архив_инструмент, 'rcs', компилация_път / 'libposix-kor-arm64.a', компилация_път / 'posix.o'])
    изпълнявам_команда([연결편집기, '--gc-sections', '-T', проект_корен / '부팅/Връзка_схема.ld', '-Map', компилация_път / 'kernel.map', '-o', компилация_път / 'kernel.elf'] +
        [компилация_път / Име for Име in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', компилация_път / 'libposix-kor-arm64.a', мрежа, отдалечен_използвам, компилация_път / 'remote/libassh.a', компилация_път / 'remote/libbearssl.a', '--end-group'])
    изпълнявам_команда([обект_Файл_конвертор, '-O', 'binary', компилация_път / 'kernel.elf', компилация_път / 'kernel8.img'])
    пакет_манифест = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Български.자체', 'korean_exceptions': 20,
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
    for Име in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        пакет_манифест['sha256'][Име] = hashlib.sha256((компилация_път / Име).read_bytes()).hexdigest()
    (компилация_път / 'build.json').write_text(json.dumps(пакет_манифест, indent=2) + '\n')
    print('완료:', компилация_път / 'kernel8.img')


if __name__ == '__main__':
    Стартиране()
