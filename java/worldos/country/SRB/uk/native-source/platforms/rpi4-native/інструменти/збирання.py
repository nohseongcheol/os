#!/usr/bin/env python3
"""хост javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from збірка_користувач_ПРОБІЛ import Створення_користувач_ПРОБІЛ
from збірка_мережа import Створення_мережа
from 예제빌드 import 예제만들기
from збірка_віддалений import Створення_віддалений

Дії_корінь = Path(__file__).resolve().parents[1]
репозиторій_корінь = Дії_корінь.parents[1]
збірка_шлях = Дії_корінь / 'build'


def Виконати_команда(аргумент_масив):
    subprocess.check_call([str(첫째값) for 첫째값 in аргумент_масив], cwd=str(Дії_корінь))


def запустити():
    збірка_шлях.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    об_єкт_Файл_перетворювач = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Архів_інструмент = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for інструменти in ('javac', 시언어번역기, 시플플번역기, 연결편집기, об_єкт_Файл_перетворювач, Архів_інструмент):
        if not shutil.which(інструменти):
            raise SystemExit('필요한 збирання інструменти 없음: ' + інструменти)
    шрифт_відомості = json.loads((Дії_корінь / 'vendor/terminal-font.json').read_text())
    шрифт_дані = (Дії_корінь / 'vendor/terminal-font.bin').read_bytes()
    if len(шрифт_дані) != 65616 * 32 or hashlib.sha256(шрифт_дані).hexdigest() != шрифт_відомості['sha256']:
        raise SystemExit('термінал шрифт_значення Розмір/SHA256 불일치')
    експортувати_таблиця = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.Вивід', 'jshell_input': '셸입출력.입력', 'java_task': 'Ядро.작업', 'jfs_path_start': 'ФайлиПамʼяті.шлях_ПУСК',
               'jfs_path_byte': 'ФайлиПамʼяті.шлях_байт', 'jfs_open': 'ФайлиПамʼяті.Відкрити',
               'jfs_read': 'ФайлиПамʼяті.Читання', 'jfs_write': 'ФайлиПамʼяті.Запис',
               'jfs_seek': 'ФайлиПамʼяті.шукати_посада', 'jfs_close': 'ФайлиПамʼяті.Закрити',
               'jfs_size': 'ФайлиПамʼяті.Розмір', 'jfs_unlink': 'ФайлиПамʼяті.видаляти_запис',
               'jfs_truncate': 'ФайлиПамʼяті.길이정하기'}
    експортувати_таблиця.update({'jfs_entry_count': 'ФайлиПамʼяті.파일한도', 'jfs_entry_length': 'ФайлиПамʼяті.공개이름길이', 'jfs_entry_byte': 'ФайлиПамʼяті.공개이름바이트', 'jfs_entry_size': 'ФайлиПамʼяті.공개파일크기'})
    експортувати_таблиця.update({'jdraw_prepare': '화면합성.Готувати', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.кліп',
        'jdraw_clip_value': '화면합성.кліп_значення', 'jdraw_begin': '화면합성.запустити',
        'jdraw_end': '화면합성.Готово', 'jdraw_pixel': '화면합성.елемент_зображення',
        'jdraw_rectangle': '화면합성.прямокутник_заливка', 'jdraw_pointer': '화면합성.курсор'})
    експортувати_таблиця.update({'jfs_mkdir': 'ФайлиПамʼяті.Створення_Каталог', 'jfs_rmdir': 'ФайлиПамʼяті.вилучати_Каталог', 'jfs_kind': 'ФайлиПамʼяті.항목종류'})
    експортувати_таблиця.update({'jnet_socket': 'замикання_на_себе_мережа.Створення_запис', 'jnet_bind': 'замикання_на_себе_мережа.зв_язувати_учасник',
        'jnet_put': 'замикання_на_себе_мережа.자료넣기', 'jnet_get': 'замикання_на_себе_мережа.자료읽기', 'jnet_send': 'замикання_на_себе_мережа.надсилати',
        'jnet_recv': 'замикання_на_себе_мережа.отримувати', 'jnet_port': 'замикання_на_себе_мережа.창구읽기', 'jnet_address': 'замикання_на_себе_мережа.주소읽기',
        'jnet_peer': 'замикання_на_себе_мережа.відправник_учасник', 'jnet_close': 'замикання_на_себе_мережа.Закрити'})
    експортувати_таблиця.update({'jstream_create': 'потік_мережа.Створення_запис', 'jstream_bind': 'потік_мережа.зв_язувати_учасник', 'jstream_listen': 'потік_мережа.прослуховувати_учасник', 'jstream_connect': 'потік_мережа.З_єднання', 'jstream_accept': 'потік_мережа.приймати_зв_язок', 'jstream_read': 'потік_мережа.Читання', 'jstream_write': 'потік_мережа.Запис', 'jstream_port': 'потік_мережа.창구읽기', 'jstream_peer': 'потік_мережа.상대창구읽기', 'jstream_close': 'потік_мережа.Закрити'})
    for символ_значення in list(експортувати_таблиця):
        if символ_значення.startswith('jstream_') or символ_значення.startswith('jnet_') and символ_значення not in ('jnet_put', 'jnet_get'):
            експортувати_таблиця[символ_значення.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = експортувати_таблиця.pop(символ_значення)
    예제들 = ['public final class набір { public static void Готувати() {']
    for шлях in sorted((Дії_корінь / '예제').iterdir()):
        if шлях.is_file():
            예제들.append('ІнтерпретаторКоманд.정적파일(%s, %s);' %
                (json.dumps(шлях.name), json.dumps(шлях.read_text(encoding='utf-8'), ensure_ascii=True)))
    (збірка_шлях / 'набір.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Дії_корінь, репозиторій_корінь, Виконати_команда)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(збірка_шлях)) as 작업경로:
        Клас_шлях = Path(작업경로)
        Виконати_команда(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Клас_шлях, '-sourcepath', Клас_шлях, '-d', Клас_шлях] + sorted((Дії_корінь / 'вихіднийКод').glob('*.java')) + [збірка_шлях / 'набір.java', збірка_шлях / '예제꾸러미.java'])
        # файл·оболонка·Вікно 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        аргумент_масив = ['sh', репозиторій_корінь / 'compiler/미리번역.sh', '--entry', 'Ядро.запустити', '--heap-words', '1048576', '-o', збірка_шлях / 'kernel-java.c']
        for символ_значення, метод_запис in sorted(експортувати_таблиця.items()):
            аргумент_масив += ['--export', символ_значення + '=' + метод_запис]
        Виконати_команда(аргумент_масив + sorted(Клас_шлях.glob('*.class')))
    (збірка_шлях / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    конфігурація_служба_фонового_передавання_файлів = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = репозиторій_корінь / 'posix-kor/arm64-native'
    Створення_користувач_ПРОБІЛ(Дії_корінь, репозиторій_корінь, 시언어번역기, 시플플번역기, 연결편집기, Архів_інструмент, конфігурація_служба_фонового_передавання_файлів, Виконати_команда)
    мережа = Створення_мережа(Дії_корінь, 시언어번역기, Архів_інструмент, конфігурація_служба_фонового_передавання_файлів, Виконати_команда)
    віддалений_використання = Створення_віддалений(Дії_корінь, 시언어번역기, Архів_інструмент, конфігурація_служба_фонового_передавання_файлів, Виконати_команда)
    포함인수 = ['-I', 포직스경로 / 'оголошення', '-I', збірка_шлях]
    빌드작업 = [(시언어번역기, [], збірка_шлях / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Дії_корінь / 'комп_ютер/термінал.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Дії_корінь / 'комп_ютер/елемент_екрана.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], збірка_шлях / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Дії_корінь / 'комп_ютер/Дошка.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Дії_корінь / 'комп_ютер/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Дії_корінь / 'комп_ютер/простір_користувача.c', 'user.o'),
            (시언어번역기, [], Дії_корінь / 'запуск_машини/запис_бал_значення.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'З_єднання.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Дії_корінь / 'випробування/Файл_Виклики.cpp', 'cpp.o')]
    for компілятор_інструмент, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [Файл_запис for Файл_запис in конфігурація_служба_фонового_передавання_файлів if Файл_запис != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else конфігурація_служба_фонового_передавання_файлів
        Виконати_команда([компілятор_інструмент] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', збірка_шлях / 출력결과])
    Виконати_команда([Архів_інструмент, 'rcs', збірка_шлях / 'libposix-kor-arm64.a', збірка_шлях / 'posix.o'])
    Виконати_команда([연결편집기, '--gc-sections', '-T', Дії_корінь / 'запуск_машини/схема_компонування.ld', '-Map', збірка_шлях / 'kernel.map', '-o', збірка_шлях / 'kernel.elf'] +
        [збірка_шлях / Назва for Назва in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', збірка_шлях / 'libposix-kor-arm64.a', мережа, віддалений_використання, збірка_шлях / 'remote/libassh.a', збірка_шлях / 'remote/libbearssl.a', '--end-group'])
    Виконати_команда([об_єкт_Файл_перетворювач, '-O', 'binary', збірка_шлях / 'kernel.elf', збірка_шлях / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'українська.своє', 'korean_exceptions': 20,
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
        꾸러미명세['sha256'][Назва] = hashlib.sha256((збірка_шлях / Назва).read_bytes()).hexdigest()
    (збірка_шлях / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', збірка_шлях / 'kernel8.img')


if __name__ == '__main__':
    запустити()
