#!/usr/bin/env python3
"""хост javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from төзү_кулланучы_өлкә import Төзү_кулланучы_өлкә
from төзү_Челтәр import Төзү_Челтәр
from 예제빌드 import 예제만들기
from төзү_читтәге import Төзү_читтәге

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]
저장소 = экранга_җибәрү_тамыр.parents[1]
төзү_юл = экранга_җибәрү_тамыр / 'build'


def үтәргә_команда(аргумент_МАССИВ):
    subprocess.check_call([str(첫째값) for 첫째값 in аргумент_МАССИВ], cwd=str(экранга_җибәрү_тамыр))


def эшләтү():
    төзү_юл.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    объект_файл_конвертер = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Архив_чара = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Кораллар in ('javac', 시언어번역기, 시플플번역기, 연결편집기, объект_файл_конвертер, Архив_чара):
        if not shutil.which(Кораллар):
            raise SystemExit('필요한 төзү_система Кораллар 없음: ' + Кораллар)
    шрифт_мәгълүмат_c16c0f1c = json.loads((экранга_җибәрү_тамыр / 'vendor/terminal-font.json').read_text())
    шрифт_мәгълүмат = (экранга_җибәрү_тамыр / 'vendor/terminal-font.bin').read_bytes()
    if len(шрифт_мәгълүмат) != 65616 * 32 or hashlib.sha256(шрифт_мәгълүмат).hexdigest() != шрифт_мәгълүмат_c16c0f1c['sha256']:
        raise SystemExit('Терминал шрифт_VALUE үлчәмен_үзгәртү/SHA256 불일치')
    экспортлау_таблица = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'төш.작업', 'jfs_path_start': 'Хәтер_Файллар.юл_Start',
               'jfs_path_byte': 'Хәтер_Файллар.юл_байт', 'jfs_open': 'Хәтер_Файллар.ачу',
               'jfs_read': 'Хәтер_Файллар.읽기', 'jfs_write': 'Хәтер_Файллар.язу',
               'jfs_seek': 'Хәтер_Файллар.эзләү_урнаштыру', 'jfs_close': 'Хәтер_Файллар.Yap',
               'jfs_size': 'Хәтер_Файллар.үлчәмен_үзгәртү', 'jfs_unlink': 'Хәтер_Файллар.지우기',
               'jfs_truncate': 'Хәтер_Файллар.җыелма_озынлык'}
    экспортлау_таблица.update({'jfs_entry_count': 'Хәтер_Файллар.파일한도', 'jfs_entry_length': 'Хәтер_Файллар.공개이름길이', 'jfs_entry_byte': 'Хәтер_Файллар.공개이름바이트', 'jfs_entry_size': 'Хәтер_Файллар.공개파일크기'})
    экспортлау_таблица.update({'jdraw_prepare': '화면합성.Әзерләү', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.клип',
        'jdraw_clip_value': '화면합성.клип_VALUE', 'jdraw_begin': '화면합성.эшләтү',
        'jdraw_end': '화면합성.Әзер', 'jdraw_pixel': '화면합성.нокта',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.күрсәткеч'})
    экспортлау_таблица.update({'jfs_mkdir': 'Хәтер_Файллар.Төзү_каталог', 'jfs_rmdir': 'Хәтер_Файллар.бетерү_каталог', 'jfs_kind': 'Хәтер_Файллар.항목종류'})
    экспортлау_таблица.update({'jnet_socket': '되돌림망.Төзү_кертү', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.җибәрү',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Yap'})
    экспортлау_таблица.update({'jstream_create': 'агым_Челтәр.Төзү_кертү', 'jstream_bind': 'агым_Челтәр.묶기', 'jstream_listen': 'агым_Челтәр.듣기', 'jstream_connect': 'агым_Челтәр.ялгау', 'jstream_accept': 'агым_Челтәр.кабул_итү_тоташу', 'jstream_read': 'агым_Челтәр.읽기', 'jstream_write': 'агым_Челтәр.язу', 'jstream_port': 'агым_Челтәр.창구읽기', 'jstream_peer': 'агым_Челтәр.상대창구읽기', 'jstream_close': 'агым_Челтәр.Yap'})
    for символ_VALUE in list(экспортлау_таблица):
        if символ_VALUE.startswith('jstream_') or символ_VALUE.startswith('jnet_') and символ_VALUE not in ('jnet_put', 'jnet_get'):
            экспортлау_таблица[символ_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = экспортлау_таблица.pop(символ_VALUE)
    예제들 = ['public final class пакет { public static void Әзерләү() {']
    for Yul in sorted((экранга_җибәрү_тамыр / '예제').iterdir()):
        if Yul.is_file():
            예제들.append('명령해석기.статик_файл(%s, %s);' %
                (json.dumps(Yul.name), json.dumps(Yul.read_text(encoding='utf-8'), ensure_ascii=True)))
    (төзү_юл / 'пакет.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(экранга_җибәрү_тамыр, 저장소, үтәргә_команда)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(төзү_юл)) as 작업경로:
        класс_юл = Path(작업경로)
        үтәргә_команда(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', класс_юл, '-sourcepath', класс_юл, '-d', класс_юл] + sorted((экранга_җибәрү_тамыр / 'чыганак').glob('*.java')) + [төзү_юл / 'пакет.java', төзү_юл / '예제꾸러미.java'])
        # Birem·тышча·тәрәз 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        аргумент_МАССИВ = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'төш.эшләтү', '--heap-words', '1048576', '-o', төзү_юл / 'kernel-java.c']
        for символ_VALUE, ысул_кертү in sorted(экспортлау_таблица.items()):
            аргумент_МАССИВ += ['--export', символ_VALUE + '=' + ысул_кертү]
        үтәргә_команда(аргумент_МАССИВ + sorted(класс_юл.glob('*.class')))
    (төзү_юл / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    Төзү_кулланучы_өлкә(экранга_җибәрү_тамыр, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Архив_чара, 설정비트, үтәргә_команда)
    Челтәр = Төзү_Челтәр(экранга_җибәрү_тамыр, 시언어번역기, Архив_чара, 설정비트, үтәргә_команда)
    원격사용 = Төзү_читтәге(экранга_җибәрү_тамыр, 시언어번역기, Архив_чара, 설정비트, үтәргә_команда)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', төзү_юл]
    빌드작업 = [(시언어번역기, [], төзү_юл / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], экранга_җибәрү_тамыр / 'машина/Терминал.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], экранга_җибәрү_тамыр / 'машина/виджет.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], төзү_юл / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], экранга_җибәрү_тамыр / 'машина/такта.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], экранга_җибәрү_тамыр / 'машина/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], экранга_җибәрү_тамыр / 'машина/кулланучы.c', 'user.o'),
            (시언어번역기, [], экранга_җибәрү_тамыр / '부팅/кертү_балл_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'ялгау.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], экранга_җибәрү_тамыр / '시험/файл_Шалтыратулар.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [файл_кертү for файл_кертү in 설정비트 if файл_кертү != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        үтәргә_команда([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', төзү_юл / 출력결과])
    үтәргә_команда([Архив_чара, 'rcs', төзү_юл / 'libposix-kor-arm64.a', төзү_юл / 'posix.o'])
    үтәргә_команда([연결편집기, '--gc-sections', '-T', экранга_җибәрү_тамыр / '부팅/бәйләү_план.ld', '-Map', төзү_юл / 'kernel.map', '-o', төзү_юл / 'kernel.elf'] +
        [төзү_юл / исем for исем in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', төзү_юл / 'libposix-kor-arm64.a', Челтәр, 원격사용, төзү_юл / 'remote/libassh.a', төзү_юл / 'remote/libbearssl.a', '--end-group'])
    үтәргә_команда([объект_файл_конвертер, '-O', 'binary', төзү_юл / 'kernel.elf', төзү_юл / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Татарча.자체', 'korean_exceptions': 20,
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
    for исем in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][исем] = hashlib.sha256((төзү_юл / исем).read_bytes()).hexdigest()
    (төзү_юл / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', төзү_юл / 'kernel8.img')


if __name__ == '__main__':
    эшләтү()
