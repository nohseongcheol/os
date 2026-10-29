#!/usr/bin/env python3
"""хост javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from градити_корисник_простор import Направи_корисник_простор
from градити_Мрежа import Направи_Мрежа
from 예제빌드 import 예제만들기
from градити_удаљен import Направи_удаљен

пројектовати_корен = Path(__file__).resolve().parents[1]
депо_корен = пројектовати_корен.parents[1]
градити_пут = пројектовати_корен / 'build'


def Изврши_команда(аргумент_низ):
    subprocess.check_call([str(첫째값) for 첫째값 in аргумент_низ], cwd=str(пројектовати_корен))


def Покрени():
    градити_пут.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    објекат_фајл_претварач = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Архива_алат = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Алатке in ('javac', 시언어번역기, 시플플번역기, 연결편집기, објекат_фајл_претварач, Архива_алат):
        if not shutil.which(Алатке):
            raise SystemExit('필요한 градити_систем Алатке 없음: ' + Алатке)
    фонт_информација = json.loads((пројектовати_корен / 'vendor/terminal-font.json').read_text())
    фонт_подаци = (пројектовати_корен / 'vendor/terminal-font.bin').read_bytes()
    if len(фонт_подаци) != 65616 * 32 or hashlib.sha256(фонт_подаци).hexdigest() != фонт_информација['sha256']:
        raise SystemExit('Терминал фонт_вриједност Величина/SHA256 불일치')
    Извоз_табела = {'jshell_interactive': '셸입출력.информатичко_одељење_интерактивно', 'jshell_output': '셸입출력.Излаз', 'jshell_input': '셸입출력.입력', 'java_task': 'језгро.작업', 'jfs_path_start': 'Меморија_Фајлови.пут_Старт',
               'jfs_path_byte': 'Меморија_Фајлови.пут_бајт', 'jfs_open': 'Меморија_Фајлови.Отвори',
               'jfs_read': 'Меморија_Фајлови.Чита', 'jfs_write': 'Меморија_Фајлови.Пише',
               'jfs_seek': 'Меморија_Фајлови.тражити_позиција', 'jfs_close': 'Меморија_Фајлови.Затворен',
               'jfs_size': 'Меморија_Фајлови.Величина', 'jfs_unlink': 'Меморија_Фајлови.지우기',
               'jfs_truncate': 'Меморија_Фајлови.скуп_дужина'}
    Извоз_табела.update({'jfs_entry_count': 'Меморија_Фајлови.파일한도', 'jfs_entry_length': 'Меморија_Фајлови.공개이름길이', 'jfs_entry_byte': 'Меморија_Фајлови.공개이름바이트', 'jfs_entry_size': 'Меморија_Фајлови.공개파일크기'})
    Извоз_табела.update({'jdraw_prepare': '화면합성.Припремити', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.клип',
        'jdraw_clip_value': '화면합성.клип_вриједност', 'jdraw_begin': '화면합성.Покрени',
        'jdraw_end': '화면합성.Крај', 'jdraw_pixel': '화면합성.пиксел',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.показивач'})
    Извоз_табела.update({'jfs_mkdir': 'Меморија_Фајлови.Направи_именик', 'jfs_rmdir': 'Меморија_Фајлови.уклонити_именик', 'jfs_kind': 'Меморија_Фајлови.항목종류'})
    Извоз_табела.update({'jnet_socket': '되돌림망.Направи_унос', 'jnet_bind': '되돌림망.повезати_крајња_тачка',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.послати',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.пошиљалац_крајња_тачка', 'jnet_close': '되돌림망.Затворен'})
    Извоз_табела.update({'jstream_create': 'ток_Мрежа.Направи_унос', 'jstream_bind': 'ток_Мрежа.повезати_крајња_тачка', 'jstream_listen': 'ток_Мрежа.слушати_крајња_тачка', 'jstream_connect': 'ток_Мрежа.Повежи_се', 'jstream_accept': 'ток_Мрежа.прихвати_веза', 'jstream_read': 'ток_Мрежа.Чита', 'jstream_write': 'ток_Мрежа.Пише', 'jstream_port': 'ток_Мрежа.창구읽기', 'jstream_peer': 'ток_Мрежа.상대창구읽기', 'jstream_close': 'ток_Мрежа.Затворен'})
    for симбол_вриједност in list(Извоз_табела):
        if симбол_вриједност.startswith('jstream_') or симбол_вриједност.startswith('jnet_') and симбол_вриједност not in ('jnet_put', 'jnet_get'):
            Извоз_табела[симбол_вриједност.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = Извоз_табела.pop(симбол_вриједност)
    예제들 = ['public final class пакет { public static void Припремити() {']
    for ПУТАЊА in sorted((пројектовати_корен / '예제').iterdir()):
        if ПУТАЊА.is_file():
            예제들.append('명령해석기.статични_фајл(%s, %s);' %
                (json.dumps(ПУТАЊА.name), json.dumps(ПУТАЊА.read_text(encoding='utf-8'), ensure_ascii=True)))
    (градити_пут / 'пакет.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(пројектовати_корен, депо_корен, Изврши_команда)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(градити_пут)) as 작업경로:
        класа_пут = Path(작업경로)
        Изврши_команда(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', класа_пут, '-sourcepath', класа_пут, '-d', класа_пут] + sorted((пројектовати_корен / 'ИЗВОР').glob('*.java')) + [градити_пут / 'пакет.java', градити_пут / '예제꾸러미.java'])
        # Датотека·љуска·Прозор 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        аргумент_низ = ['sh', депо_корен / 'compiler/미리번역.sh', '--entry', 'језгро.Покрени', '--heap-words', '1048576', '-o', градити_пут / 'kernel-java.c']
        for симбол_вриједност, метода_унос in sorted(Извоз_табела.items()):
            аргумент_низ += ['--export', симбол_вриједност + '=' + метода_унос]
        Изврши_команда(аргумент_низ + sorted(класа_пут.glob('*.class')))
    (градити_пут / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    конфигурација_Услуга_интелигентног_преноса_у_позадини = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = депо_корен / 'posix-kor/arm64-native'
    Направи_корисник_простор(пројектовати_корен, депо_корен, 시언어번역기, 시플플번역기, 연결편집기, Архива_алат, конфигурација_Услуга_интелигентног_преноса_у_позадини, Изврши_команда)
    Мрежа = Направи_Мрежа(пројектовати_корен, 시언어번역기, Архива_алат, конфигурација_Услуга_интелигентног_преноса_у_позадини, Изврши_команда)
    원격사용 = Направи_удаљен(пројектовати_корен, 시언어번역기, Архива_алат, конфигурација_Услуга_интелигентног_преноса_у_позадини, Изврши_команда)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', градити_пут]
    빌드작업 = [(시언어번역기, [], градити_пут / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], пројектовати_корен / 'рачунар/Терминал.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], пројектовати_корен / 'рачунар/виџет.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], градити_пут / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], пројектовати_корен / 'рачунар/Табла.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], пројектовати_корен / 'рачунар/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], пројектовати_корен / 'рачунар/корисник.c', 'user.o'),
            (시언어번역기, [], пројектовати_корен / '부팅/унос_поен_вриједност.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Повежи_се.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], пројектовати_корен / '시험/фајл_Позиви.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [фајл_унос for фајл_унос in конфигурација_Услуга_интелигентног_преноса_у_позадини if фајл_унос != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else конфигурација_Услуга_интелигентног_преноса_у_позадини
        Изврши_команда([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', градити_пут / 출력결과])
    Изврши_команда([Архива_алат, 'rcs', градити_пут / 'libposix-kor-arm64.a', градити_пут / 'posix.o'])
    Изврши_команда([연결편집기, '--gc-sections', '-T', пројектовати_корен / '부팅/Веза_изглед.ld', '-Map', градити_пут / 'kernel.map', '-o', градити_пут / 'kernel.elf'] +
        [градити_пут / Назив for Назив in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', градити_пут / 'libposix-kor-arm64.a', Мрежа, 원격사용, градити_пут / 'remote/libassh.a', градити_пут / 'remote/libbearssl.a', '--end-group'])
    Изврши_команда([објекат_фајл_претварач, '-O', 'binary', градити_пут / 'kernel.elf', градити_пут / 'kernel8.img'])
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
    for Назив in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Назив] = hashlib.sha256((градити_пут / Назив).read_bytes()).hexdigest()
    (градити_пут / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', градити_пут / 'kernel8.img')


if __name__ == '__main__':
    Покрени()
