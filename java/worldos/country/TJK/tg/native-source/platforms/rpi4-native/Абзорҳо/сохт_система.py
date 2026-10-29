#!/usr/bin/env python3
"""мизбон javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from сохт_корбар_фазо import эҷод_кардан_корбар_фазо
from сохт_Шабака import эҷод_кардан_Шабака
from 예제빌드 import 예제만들기
from сохт_дурдаст import эҷод_кардан_дурдаст

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
сохт_масир = 기준 / 'build'


def иҷро_кардан_фармон(аргумент_қатор):
    subprocess.check_call([str(첫째값) for 첫째값 in аргумент_қатор], cwd=str(기준))


def порча():
    сохт_масир.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    объект_файл_конвертер = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Бойгонӣ_абзор = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Абзорҳо in ('javac', 시언어번역기, 시플플번역기, 연결편집기, объект_файл_конвертер, Бойгонӣ_абзор):
        if not shutil.which(Абзорҳо):
            raise SystemExit('필요한 сохт_система Абзорҳо 없음: ' + Абзорҳо)
    шрифт_маълумот = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    шрифт_иттилоот = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(шрифт_иттилоот) != 65616 * 32 or hashlib.sha256(шрифт_иттилоот).hexdigest() != шрифт_маълумот['sha256']:
        raise SystemExit('터미널 шрифт_қимат андоза_кардан/SHA256 불일치')
    содир_кардан_ҷадвал = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'ҳаста.작업', 'jfs_path_start': 'ҳофиза_Файлҳо.масир_Оғоз',
               'jfs_path_byte': 'ҳофиза_Файлҳо.масир_байт', 'jfs_open': 'ҳофиза_Файлҳо.кушодан',
               'jfs_read': 'ҳофиза_Файлҳо.Хондан', 'jfs_write': 'ҳофиза_Файлҳо.Навиштан',
               'jfs_seek': 'ҳофиза_Файлҳо.옮기기', 'jfs_close': 'ҳофиза_Файлҳо.Пӯшидан',
               'jfs_size': 'ҳофиза_Файлҳо.андоза_кардан', 'jfs_unlink': 'ҳофиза_Файлҳо.지우기',
               'jfs_truncate': 'ҳофиза_Файлҳо.маҷмуъ_дарозӣ'}
    содир_кардан_ҷадвал.update({'jfs_entry_count': 'ҳофиза_Файлҳо.파일한도', 'jfs_entry_length': 'ҳофиза_Файлҳо.공개이름길이', 'jfs_entry_byte': 'ҳофиза_Файлҳо.공개이름바이트', 'jfs_entry_size': 'ҳофиза_Файлҳо.공개파일크기'})
    содир_кардан_ҷадвал.update({'jdraw_prepare': '화면합성.Омода_кардан', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.клип',
        'jdraw_clip_value': '화면합성.клип_қимат', 'jdraw_begin': '화면합성.порча',
        'jdraw_end': '화면합성.Тайёр', 'jdraw_pixel': '화면합성.пиксел',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.курсор'})
    содир_кардан_ҷадвал.update({'jfs_mkdir': 'ҳофиза_Файлҳо.эҷод_кардан_директория', 'jfs_rmdir': 'ҳофиза_Файлҳо.тоза_кардан_директория', 'jfs_kind': 'ҳофиза_Файлҳо.항목종류'})
    содир_кардан_ҷадвал.update({'jnet_socket': '되돌림망.эҷод_кардан_ворида', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.фиристодан',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Пӯшидан'})
    содир_кардан_ҷадвал.update({'jstream_create': 'ҷараён_Шабака.эҷод_кардан_ворида', 'jstream_bind': 'ҷараён_Шабака.묶기', 'jstream_listen': 'ҷараён_Шабака.듣기', 'jstream_connect': 'ҷараён_Шабака.ПАЙВАСТ', 'jstream_accept': 'ҷараён_Шабака.қабул_кардан_пайваст', 'jstream_read': 'ҷараён_Шабака.Хондан', 'jstream_write': 'ҷараён_Шабака.Навиштан', 'jstream_port': 'ҷараён_Шабака.창구읽기', 'jstream_peer': 'ҷараён_Шабака.상대창구읽기', 'jstream_close': 'ҷараён_Шабака.Пӯшидан'})
    for аломат_қимат in list(содир_кардан_ҷадвал):
        if аломат_қимат.startswith('jstream_') or аломат_қимат.startswith('jnet_') and аломат_қимат not in ('jnet_put', 'jnet_get'):
            содир_кардан_ҷадвал[аломат_қимат.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = содир_кардан_ҷадвал.pop(аломат_қимат)
    예제들 = ['public final class баста { public static void Омода_кардан() {']
    for масир in sorted((기준 / '예제').iterdir()):
        if масир.is_file():
            예제들.append('명령해석기.собит_файл(%s, %s);' %
                (json.dumps(масир.name), json.dumps(масир.read_text(encoding='utf-8'), ensure_ascii=True)))
    (сохт_масир / 'баста.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, иҷро_кардан_фармон)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(сохт_масир)) as 작업경로:
        синф_масир = Path(작업경로)
        иҷро_кардан_фармон(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', синф_масир, '-sourcepath', синф_масир, '-d', синф_масир] + sorted((기준 / 'манбаъ').glob('*.java')) + [сохт_масир / 'баста.java', сохт_масир / '예제꾸러미.java'])
        # Файл·восит·равзана 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        аргумент_қатор = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'ҳаста.порча', '--heap-words', '1048576', '-o', сохт_масир / 'kernel-java.c']
        for аломат_қимат, сабк_ворида in sorted(содир_кардан_ҷадвал.items()):
            аргумент_қатор += ['--export', аломат_қимат + '=' + сабк_ворида]
        иҷро_кардан_фармон(аргумент_қатор + sorted(синф_масир.glob('*.class')))
    (сохт_масир / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    эҷод_кардан_корбар_фазо(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Бойгонӣ_абзор, 설정비트, иҷро_кардан_фармон)
    Шабака = эҷод_кардан_Шабака(기준, 시언어번역기, Бойгонӣ_абзор, 설정비트, иҷро_кардан_фармон)
    원격사용 = эҷод_кардан_дурдаст(기준, 시언어번역기, Бойгонӣ_абзор, 설정비트, иҷро_кардан_фармон)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', сохт_масир]
    빌드작업 = [(시언어번역기, [], сохт_масир / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'компютер/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'компютер/виҷет.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], сохт_масир / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'компютер/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'компютер/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'компютер/корбар.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/ворида_нуқта_қимат.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'ПАЙВАСТ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [файл_ворида for файл_ворида in 설정비트 if файл_ворида != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        иҷро_кардан_фармон([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', сохт_масир / 출력결과])
    иҷро_кардан_фармон([Бойгонӣ_абзор, 'rcs', сохт_масир / 'libposix-kor-arm64.a', сохт_масир / 'posix.o'])
    иҷро_кардан_фармон([연결편집기, '--gc-sections', '-T', 기준 / '부팅/Пайванд_Тарҳбандӣ.ld', '-Map', сохт_масир / 'kernel.map', '-o', сохт_масир / 'kernel.elf'] +
        [сохт_масир / Ном for Ном in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', сохт_масир / 'libposix-kor-arm64.a', Шабака, 원격사용, сохт_масир / 'remote/libassh.a', сохт_масир / 'remote/libbearssl.a', '--end-group'])
    иҷро_кардан_фармон([объект_файл_конвертер, '-O', 'binary', сохт_масир / 'kernel.elf', сохт_масир / 'kernel8.img'])
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
    for Ном in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Ном] = hashlib.sha256((сохт_масир / Ном).read_bytes()).hexdigest()
    (сохт_масир / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', сохт_масир / 'kernel8.img')


if __name__ == '__main__':
    порча()
