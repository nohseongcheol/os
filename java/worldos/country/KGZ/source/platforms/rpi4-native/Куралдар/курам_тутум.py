#!/usr/bin/env python3
"""кабылдоо javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from курам_колдонуучу_АРАЛЫК import түзүү_колдонуучу_АРАЛЫК
from курам_Желе import түзүү_Желе
from 예제빌드 import 예제만들기
from курам_алыскы import түзүү_алыскы

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
курам_жол = 기준 / 'build'


def аткаруу_буйрук(аргумент_МАССИВ):
    subprocess.check_call([str(첫째값) for 첫째값 in аргумент_МАССИВ], cwd=str(기준))


def Жүргүзүү():
    курам_жол.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    объект_файл_маанилеш_өзгөрткүч = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Архив_курал = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Куралдар in ('javac', 시언어번역기, 시플플번역기, 연결편집기, объект_файл_маанилеш_өзгөрткүч, Архив_курал):
        if not shutil.which(Куралдар):
            raise SystemExit('필요한 курам_тутум Куралдар 없음: ' + Куралдар)
    арип_маалымат = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    арип_берилмелер = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(арип_берилмелер) != 65616 * 32 or hashlib.sha256(арип_берилмелер).hexdigest() != арип_маалымат['sha256']:
        raise SystemExit('Терминал арип_маани Өлчөмү/SHA256 불일치')
    экспорттоо_жадыбал = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.Чыгыш', 'jshell_input': '셸입출력.입력', 'java_task': 'өзөк.작업', 'jfs_path_start': 'эс_Файлдар.жол_Баштоо',
               'jfs_path_byte': 'эс_Файлдар.жол_байт', 'jfs_open': 'эс_Файлдар.Ачуу',
               'jfs_read': 'эс_Файлдар.Окуу', 'jfs_write': 'эс_Файлдар.Жазуу',
               'jfs_seek': 'эс_Файлдар.옮기기', 'jfs_close': 'эс_Файлдар.Жабуу',
               'jfs_size': 'эс_Файлдар.Өлчөмү', 'jfs_unlink': 'эс_Файлдар.지우기',
               'jfs_truncate': 'эс_Файлдар.топ_узундук'}
    экспорттоо_жадыбал.update({'jfs_entry_count': 'эс_Файлдар.파일한도', 'jfs_entry_length': 'эс_Файлдар.공개이름길이', 'jfs_entry_byte': 'эс_Файлдар.공개이름바이트', 'jfs_entry_size': 'эс_Файлдар.공개파일크기'})
    экспорттоо_жадыбал.update({'jdraw_prepare': '화면합성.Даярдоо', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.клип',
        'jdraw_clip_value': '화면합성.клип_маани', 'jdraw_begin': '화면합성.Жүргүзүү',
        'jdraw_end': '화면합성.Бүттү', 'jdraw_pixel': '화면합성.пиксел',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.көрсөткүч'})
    экспорттоо_жадыбал.update({'jfs_mkdir': 'эс_Файлдар.түзүү_каталог', 'jfs_rmdir': 'эс_Файлдар.алып_салуу_каталог', 'jfs_kind': 'эс_Файлдар.항목종류'})
    экспорттоо_жадыбал.update({'jnet_socket': '되돌림망.түзүү_киргизме_жазуу', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.жөнөтүү',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Жабуу'})
    экспорттоо_жадыбал.update({'jstream_create': 'агым_Желе.түзүү_киргизме_жазуу', 'jstream_bind': 'агым_Желе.묶기', 'jstream_listen': 'агым_Желе.듣기', 'jstream_connect': 'агым_Желе.Туташуу', 'jstream_accept': 'агым_Желе.кабыл_алуу_туташуу', 'jstream_read': 'агым_Желе.Окуу', 'jstream_write': 'агым_Желе.Жазуу', 'jstream_port': 'агым_Желе.창구읽기', 'jstream_peer': 'агым_Желе.상대창구읽기', 'jstream_close': 'агым_Желе.Жабуу'})
    for символ_маани in list(экспорттоо_жадыбал):
        if символ_маани.startswith('jstream_') or символ_маани.startswith('jnet_') and символ_маани not in ('jnet_put', 'jnet_get'):
            экспорттоо_жадыбал[символ_маани.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = экспорттоо_жадыбал.pop(символ_маани)
    예제들 = ['public final class пакет { public static void Даярдоо() {']
    for ЖОЛ in sorted((기준 / '예제').iterdir()):
        if ЖОЛ.is_file():
            예제들.append('명령해석기.статикалык_файл(%s, %s);' %
                (json.dumps(ЖОЛ.name), json.dumps(ЖОЛ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (курам_жол / 'пакет.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, аткаруу_буйрук)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(курам_жол)) as 작업경로:
        класс_жол = Path(작업경로)
        аткаруу_буйрук(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', класс_жол, '-sourcepath', класс_жол, '-d', класс_жол] + sorted((기준 / 'Булак').glob('*.java')) + [курам_жол / 'пакет.java', курам_жол / '예제꾸러미.java'])
        # Файл·сырты·терезе 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        аргумент_МАССИВ = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'өзөк.Жүргүзүү', '--heap-words', '1048576', '-o', курам_жол / 'kernel-java.c']
        for символ_маани, ыкма_киргизме_жазуу in sorted(экспорттоо_жадыбал.items()):
            аргумент_МАССИВ += ['--export', символ_маани + '=' + ыкма_киргизме_жазуу]
        аткаруу_буйрук(аргумент_МАССИВ + sorted(класс_жол.glob('*.class')))
    (курам_жол / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    түзүү_колдонуучу_АРАЛЫК(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Архив_курал, 설정비트, аткаруу_буйрук)
    Желе = түзүү_Желе(기준, 시언어번역기, Архив_курал, 설정비트, аткаруу_буйрук)
    원격사용 = түзүү_алыскы(기준, 시언어번역기, Архив_курал, 설정비트, аткаруу_буйрук)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', курам_жол]
    빌드작업 = [(시언어번역기, [], курам_жол / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'машина/Терминал.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'машина/уижет.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], курам_жол / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'машина/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'машина/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'машина/колдонуучу.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/киргизме_жазуу_упай_маани.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Туташуу.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [файл_киргизме_жазуу for файл_киргизме_жазуу in 설정비트 if файл_киргизме_жазуу != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        аткаруу_буйрук([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', курам_жол / 출력결과])
    аткаруу_буйрук([Архив_курал, 'rcs', курам_жол / 'libposix-kor-arm64.a', курам_жол / 'posix.o'])
    аткаруу_буйрук([연결편집기, '--gc-sections', '-T', 기준 / '부팅/Шилтеме_түзүлүш.ld', '-Map', курам_жол / 'kernel.map', '-o', курам_жол / 'kernel.elf'] +
        [курам_жол / Аты for Аты in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', курам_жол / 'libposix-kor-arm64.a', Желе, 원격사용, курам_жол / 'remote/libassh.a', курам_жол / 'remote/libbearssl.a', '--end-group'])
    аткаруу_буйрук([объект_файл_маанилеш_өзгөрткүч, '-O', 'binary', курам_жол / 'kernel.elf', курам_жол / 'kernel8.img'])
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
    for Аты in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Аты] = hashlib.sha256((курам_жол / Аты).read_bytes()).hexdigest()
    (курам_жол / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', курам_жол / 'kernel8.img')


if __name__ == '__main__':
    Жүргүзүү()
