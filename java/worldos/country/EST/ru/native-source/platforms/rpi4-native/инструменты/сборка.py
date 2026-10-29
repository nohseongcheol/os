#!/usr/bin/env python3
"""узел javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from BLD_пользователь_место import Create_пользователь_место
from BLD_сеть import Create_сеть
from 예제빌드 import 예제만들기
from BLD_удаленный import Create_удаленный

задача_корень = Path(__file__).resolve().parents[1]
корень_репозитория = задача_корень.parents[1]
BLD_путь = задача_корень / 'build'


def 실행(аргумент_МАССИВ):
    subprocess.check_call([str(첫째값) for 첫째값 in аргумент_МАССИВ], cwd=str(задача_корень))


def запустить():
    BLD_путь.mkdir(exist_ok=True)
    C_компилятор = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    компоновщик_средство = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    объектный_файл_преобразователь = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Архив_средство = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for инструменты in ('javac', C_компилятор, 시플플번역기, компоновщик_средство, объектный_файл_преобразователь, Архив_средство):
        if not shutil.which(инструменты):
            raise SystemExit('필요한 сборка инструменты 없음: ' + инструменты)
    шрифт_сведения = json.loads((задача_корень / 'vendor/terminal-font.json').read_text())
    шрифт_данные = (задача_корень / 'vendor/terminal-font.bin').read_bytes()
    if len(шрифт_данные) != 65616 * 32 or hashlib.sha256(шрифт_данные).hexdigest() != шрифт_сведения['sha256']:
        raise SystemExit('терминал шрифт_ЗНАЧЕН Размер/SHA256 불일치')
    экспортировать_таблица = {'jshell_interactive': '셸입출력.ИТ_службы_интерактивный', 'jshell_output': '셸입출력.текстовыйВывод', 'jshell_input': '셸입출력.входные_данные_ЗНАЧЕН', 'java_task': 'Ядро.작업', 'jfs_path_start': 'ФайлыПамяти.путь_Пуск',
               'jfs_path_byte': 'ФайлыПамяти.путь_байт', 'jfs_open': 'ФайлыПамяти.Открыть',
               'jfs_read': 'ФайлыПамяти.Чтение', 'jfs_write': 'ФайлыПамяти.Запись',
               'jfs_seek': 'ФайлыПамяти.поиск_позиция', 'jfs_close': 'ФайлыПамяти.Закрыть',
               'jfs_size': 'ФайлыПамяти.Размер', 'jfs_unlink': 'ФайлыПамяти.удалить_ввод_c8dbc399',
               'jfs_truncate': 'ФайлыПамяти.сет_длина'}
    экспортировать_таблица.update({'jfs_entry_count': 'ФайлыПамяти.파일한도', 'jfs_entry_length': 'ФайлыПамяти.공개이름길이', 'jfs_entry_byte': 'ФайлыПамяти.공개이름바이트', 'jfs_entry_size': 'ФайлыПамяти.공개파일크기'})
    экспортировать_таблица.update({'jdraw_prepare': 'КомпозицияЭкрана.Подготовить', 'jdraw_width': 'КомпозицияЭкрана.너비얻기',
        'jdraw_height': 'КомпозицияЭкрана.높이얻기', 'jdraw_count_low': 'КомпозицияЭкрана.기록아래얻기',
        'jdraw_count_high': 'КомпозицияЭкрана.기록위얻기', 'jdraw_clip': 'КомпозицияЭкрана.клип',
        'jdraw_clip_value': 'КомпозицияЭкрана.клип_ЗНАЧЕН', 'jdraw_begin': 'КомпозицияЭкрана.запустить',
        'jdraw_end': 'КомпозицияЭкрана.Готово', 'jdraw_pixel': 'КомпозицияЭкрана.пиксель',
        'jdraw_rectangle': 'КомпозицияЭкрана.прямоугольник_залить', 'jdraw_pointer': 'КомпозицияЭкрана.указатель'})
    экспортировать_таблица.update({'jfs_mkdir': 'ФайлыПамяти.Create_Каталог', 'jfs_rmdir': 'ФайлыПамяти.удалить_Каталог', 'jfs_kind': 'ФайлыПамяти.ввод_Вид'})
    экспортировать_таблица.update({'jnet_socket': 'замыкание_на_себя_сеть.Create_ввод', 'jnet_bind': 'замыкание_на_себя_сеть.BIND_участник',
        'jnet_put': 'замыкание_на_себя_сеть.자료넣기', 'jnet_get': 'замыкание_на_себя_сеть.чтение_данные', 'jnet_send': 'замыкание_на_себя_сеть.написать',
        'jnet_recv': 'замыкание_на_себя_сеть.получить', 'jnet_port': 'замыкание_на_себя_сеть.чтение_участник_порт', 'jnet_address': 'замыкание_на_себя_сеть.чтение_АДРЕС',
        'jnet_peer': 'замыкание_на_себя_сеть.отправитель_участник', 'jnet_close': 'замыкание_на_себя_сеть.Закрыть'})
    экспортировать_таблица.update({'jstream_create': 'поток_сеть.Create_ввод', 'jstream_bind': 'поток_сеть.BIND_участник', 'jstream_listen': 'поток_сеть.ожидать_передачи_данных_участник', 'jstream_connect': 'поток_сеть.Подключить', 'jstream_accept': 'поток_сеть.принять_контакт', 'jstream_read': 'поток_сеть.Чтение', 'jstream_write': 'поток_сеть.Запись', 'jstream_port': 'поток_сеть.чтение_участник_порт', 'jstream_peer': 'поток_сеть.чтение_одноранговый_порт', 'jstream_close': 'поток_сеть.Закрыть'})
    for символ_ЗНАЧЕН in list(экспортировать_таблица):
        if символ_ЗНАЧЕН.startswith('jstream_') or символ_ЗНАЧЕН.startswith('jnet_') and символ_ЗНАЧЕН not in ('jnet_put', 'jnet_get'):
            экспортировать_таблица[символ_ЗНАЧЕН.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = экспортировать_таблица.pop(символ_ЗНАЧЕН)
    예제들 = ['public final class пакет { public static void Подготовить() {']
    for путь in sorted((задача_корень / '예제').iterdir()):
        if путь.is_file():
            예제들.append('ИнтерпретаторКоманд.статический_файл(%s, %s);' %
                (json.dumps(путь.name), json.dumps(путь.read_text(encoding='utf-8'), ensure_ascii=True)))
    (BLD_путь / 'пакет.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(задача_корень, корень_репозитория, 실행)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(BLD_путь)) as 작업경로:
        Класс_путь = Path(작업경로)
        실행(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Класс_путь, '-sourcepath', Класс_путь, '-d', Класс_путь] + sorted((задача_корень / 'исходныйКод').glob('*.java')) + [BLD_путь / 'пакет.java', BLD_путь / '예제꾸러미.java'])
        # файл·оболочка·Окно 세션·통신과 Java экран 합성 배열을 모두 수용한다.
        аргумент_МАССИВ = ['sh', корень_репозитория / 'compiler/미리번역.sh', '--entry', 'Ядро.запустить', '--heap-words', '1048576', '-o', BLD_путь / 'kernel-java.c']
        for символ_ЗНАЧЕН, метод_ввод in sorted(экспортировать_таблица.items()):
            аргумент_МАССИВ += ['--export', символ_ЗНАЧЕН + '=' + метод_ввод]
        실행(аргумент_МАССИВ + sorted(Класс_путь.glob('*.class')))
    (BLD_путь / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    настройки_BITS = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = корень_репозитория / 'posix-kor/arm64-native'
    Create_пользователь_место(задача_корень, корень_репозитория, C_компилятор, 시플플번역기, компоновщик_средство, Архив_средство, настройки_BITS, 실행)
    сеть = Create_сеть(задача_корень, C_компилятор, Архив_средство, настройки_BITS, 실행)
    удаленный_использовать = Create_удаленный(задача_корень, C_компилятор, Архив_средство, настройки_BITS, 실행)
    포함인수 = ['-I', 포직스경로 / 'объявления', '-I', BLD_путь]
    빌드작업 = [(C_компилятор, [], BLD_путь / 'terminal-font.S', 'font.o'),
            (C_компилятор, ['-std=c11', '-Wall', '-Wextra', '-Werror'], задача_корень / 'компьютер_5eb260fa/терминал.c', 'terminal.o'),
            (C_компилятор, ['-std=c11', '-Wall', '-Wextra', '-Werror'], задача_корень / 'компьютер_5eb260fa/элемент_экрана.c', 'widgets.o'),
            (C_компилятор, ['-std=c11'], BLD_путь / 'kernel-java.c', 'java.o'),
            (C_компилятор, ['-std=c11', '-Wall', '-Wextra', '-Werror'], задача_корень / 'компьютер_5eb260fa/Доска.c', 'board.o'),
            (C_компилятор, ['-std=c11', '-Wall', '-Wextra', '-Werror'], задача_корень / 'компьютер_5eb260fa/экран_рисунок.c', 'drawing.o'),
            (C_компилятор, ['-std=c11', '-Wall', '-Wextra', '-Werror'], задача_корень / 'компьютер_5eb260fa/пространство_пользователя.c', 'user.o'),
            (C_компилятор, [], задача_корень / 'запуск_машины/точка_входа_ЗНАЧЕН.S', 'entry.o'),
            (C_компилятор, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Подключить.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], задача_корень / 'испытания/файл_Вызовы.cpp', 'cpp.o')]
    for компилятор_средство, 추가영역, 원본자료, выход in 빌드작업:
        원본설정 = [файл_ввод for файл_ввод in настройки_BITS if файл_ввод != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else настройки_BITS
        실행([компилятор_средство] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', BLD_путь / выход])
    실행([Архив_средство, 'rcs', BLD_путь / 'libposix-kor-arm64.a', BLD_путь / 'posix.o'])
    실행([компоновщик_средство, '--gc-sections', '-T', задача_корень / 'запуск_машины/схема_компоновки.ld', '-Map', BLD_путь / 'kernel.map', '-o', BLD_путь / 'kernel.elf'] +
        [BLD_путь / Название for Название in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', BLD_путь / 'libposix-kor-arm64.a', сеть, удаленный_использовать, BLD_путь / 'remote/libassh.a', BLD_путь / 'remote/libbearssl.a', '--end-group'])
    실행([объектный_файл_преобразователь, '-O', 'binary', BLD_путь / 'kernel.elf', BLD_путь / 'kernel8.img'])
    пакет_манифест = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'русский.свой', 'korean_exceptions': 20,
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
    for Название in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        пакет_манифест['sha256'][Название] = hashlib.sha256((BLD_путь / Название).read_bytes()).hexdigest()
    (BLD_путь / 'build.json').write_text(json.dumps(пакет_манифест, indent=2) + '\n')
    print('완료:', BLD_путь / 'kernel8.img')


if __name__ == '__main__':
    запустить()
