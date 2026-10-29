#!/usr/bin/env python3
"""вдоми javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from верзија_корисник_простор import Create_корисник_простор
from верзија_Мрежа import Create_Мрежа
from 예제빌드 import 예제만들기
from верзија_далечинскo import Create_далечинскo

Project_корен = Path(__file__).resolve().parents[1]
склад_корен = Project_корен.parents[1]
верзија_патека = Project_корен / 'build'


def Изврши_наредба(аргумент_низа):
    subprocess.check_call([str(첫째값) for 첫째값 in аргумент_низа], cwd=str(Project_корен))


def Изврши_2():
    верзија_патека.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    објект_датотека_конвертор = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Архива_алатка = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Алатки in ('javac', 시언어번역기, 시플플번역기, 연결편집기, објект_датотека_конвертор, Архива_алатка):
        if not shutil.which(Алатки):
            raise SystemExit('필요한 верзија_систем Алатки 없음: ' + Алатки)
    фонт_информации = json.loads((Project_корен / 'vendor/terminal-font.json').read_text())
    фонт_податоци = (Project_корен / 'vendor/terminal-font.bin').read_bytes()
    if len(фонт_податоци) != 65616 * 32 or hashlib.sha256(фонт_податоци).hexdigest() != фонт_информации['sha256']:
        raise SystemExit('Терминал фонт_VALUE Големина/SHA256 불일치')
    извези_табела = {'jshell_interactive': '셸입출력.информатичка_технологија_интерактивен', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'јадро.작업', 'jfs_path_start': 'Меморија_Датотеки.патека_Start',
               'jfs_path_byte': 'Меморија_Датотеки.патека_бајт', 'jfs_open': 'Меморија_Датотеки.Отвори',
               'jfs_read': 'Меморија_Датотеки.Читај', 'jfs_write': 'Меморија_Датотеки.Запиши',
               'jfs_seek': 'Меморија_Датотеки.пребарај_позиционирање', 'jfs_close': 'Меморија_Датотеки.Затвори',
               'jfs_size': 'Меморија_Датотеки.Големина', 'jfs_unlink': 'Меморија_Датотеки.избриши_внес',
               'jfs_truncate': 'Меморија_Датотеки.збир_должина'}
    извези_табела.update({'jfs_entry_count': 'Меморија_Датотеки.파일한도', 'jfs_entry_length': 'Меморија_Датотеки.공개이름길이', 'jfs_entry_byte': 'Меморија_Датотеки.공개이름바이트', 'jfs_entry_size': 'Меморија_Датотеки.공개파일크기'})
    извези_табела.update({'jdraw_prepare': '화면합성.Подготви', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.клип',
        'jdraw_clip_value': '화면합성.клип_VALUE', 'jdraw_begin': '화면합성.Изврши_2',
        'jdraw_end': '화면합성.Крај', 'jdraw_pixel': '화면합성.пиксел',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.покажувач'})
    извези_табела.update({'jfs_mkdir': 'Меморија_Датотеки.Create_Именик', 'jfs_rmdir': 'Меморија_Датотеки.отстрани_Именик', 'jfs_kind': 'Меморија_Датотеки.항목종류'})
    извези_табела.update({'jnet_socket': '되돌림망.Create_внес', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.испрати',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Затвори'})
    извези_табела.update({'jstream_create': 'Stream_Мрежа.Create_внес', 'jstream_bind': 'Stream_Мрежа.묶기', 'jstream_listen': 'Stream_Мрежа.듣기', 'jstream_connect': 'Stream_Мрежа.Врзи_се', 'jstream_accept': 'Stream_Мрежа.прифати_врска', 'jstream_read': 'Stream_Мрежа.Читај', 'jstream_write': 'Stream_Мрежа.Запиши', 'jstream_port': 'Stream_Мрежа.창구읽기', 'jstream_peer': 'Stream_Мрежа.상대창구읽기', 'jstream_close': 'Stream_Мрежа.Затвори'})
    for симбол_VALUE in list(извези_табела):
        if симбол_VALUE.startswith('jstream_') or симбол_VALUE.startswith('jnet_') and симбол_VALUE not in ('jnet_put', 'jnet_get'):
            извези_табела[симбол_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = извези_табела.pop(симбол_VALUE)
    예제들 = ['public final class пакет { public static void Подготви() {']
    for ПАТЕКА in sorted((Project_корен / '예제').iterdir()):
        if ПАТЕКА.is_file():
            예제들.append('명령해석기.статичен_датотека(%s, %s);' %
                (json.dumps(ПАТЕКА.name), json.dumps(ПАТЕКА.read_text(encoding='utf-8'), ensure_ascii=True)))
    (верзија_патека / 'пакет.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_корен, склад_корен, Изврши_наредба)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(верзија_патека)) as 작업경로:
        класа_патека = Path(작업경로)
        Изврши_наредба(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', класа_патека, '-sourcepath', класа_патека, '-d', класа_патека] + sorted((Project_корен / 'ИЗВОР').glob('*.java')) + [верзија_патека / 'пакет.java', верзија_патека / '예제꾸러미.java'])
        # Датотека·обвивка·прозорец 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        аргумент_низа = ['sh', склад_корен / 'compiler/미리번역.sh', '--entry', 'јадро.Изврши_2', '--heap-words', '1048576', '-o', верзија_патека / 'kernel-java.c']
        for симбол_VALUE, метод_внес in sorted(извези_табела.items()):
            аргумент_низа += ['--export', симбол_VALUE + '=' + метод_внес]
        Изврши_наредба(аргумент_низа + sorted(класа_патека.glob('*.class')))
    (верзија_патека / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    конфигурација_Услуга_за_интелигентен_пренос_во_заднина = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = склад_корен / 'posix-kor/arm64-native'
    Create_корисник_простор(Project_корен, склад_корен, 시언어번역기, 시플플번역기, 연결편집기, Архива_алатка, конфигурација_Услуга_за_интелигентен_пренос_во_заднина, Изврши_наредба)
    Мрежа = Create_Мрежа(Project_корен, 시언어번역기, Архива_алатка, конфигурација_Услуга_за_интелигентен_пренос_во_заднина, Изврши_наредба)
    원격사용 = Create_далечинскo(Project_корен, 시언어번역기, Архива_алатка, конфигурација_Услуга_за_интелигентен_пренос_во_заднина, Изврши_наредба)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', верзија_патека]
    빌드작업 = [(시언어번역기, [], верзија_патека / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_корен / 'машина/Терминал.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_корен / 'машина/графичка_контрола.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], верзија_патека / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_корен / 'машина/табла.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_корен / 'машина/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_корен / 'машина/корисник.c', 'user.o'),
            (시언어번역기, [], Project_корен / '부팅/внес_поен_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Врзи_се.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_корен / '시험/датотека_Повици.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [датотека_внес for датотека_внес in конфигурација_Услуга_за_интелигентен_пренос_во_заднина if датотека_внес != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else конфигурација_Услуга_за_интелигентен_пренос_во_заднина
        Изврши_наредба([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', верзија_патека / 출력결과])
    Изврши_наредба([Архива_алатка, 'rcs', верзија_патека / 'libposix-kor-arm64.a', верзија_патека / 'posix.o'])
    Изврши_наредба([연결편집기, '--gc-sections', '-T', Project_корен / '부팅/Врска_Распоред.ld', '-Map', верзија_патека / 'kernel.map', '-o', верзија_патека / 'kernel.elf'] +
        [верзија_патека / Име for Име in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', верзија_патека / 'libposix-kor-arm64.a', Мрежа, 원격사용, верзија_патека / 'remote/libassh.a', верзија_патека / 'remote/libbearssl.a', '--end-group'])
    Изврши_наредба([објект_датотека_конвертор, '-O', 'binary', верзија_патека / 'kernel.elf', верзија_патека / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Македонски.자체', 'korean_exceptions': 20,
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
        꾸러미명세['sha256'][Име] = hashlib.sha256((верзија_патека / Име).read_bytes()).hexdigest()
    (верзија_патека / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', верзија_патека / 'kernel8.img')


if __name__ == '__main__':
    Изврши_2()
