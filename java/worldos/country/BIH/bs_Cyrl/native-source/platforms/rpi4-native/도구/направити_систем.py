#!/usr/bin/env python3
"""хост_рачунар javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from направити_корисник_простор import 사용자영역만들기
from направити_Мрежа import 통신망만들기
from 예제빌드 import 예제만들기
from направити_удаљено import 원격만들기

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
направити_пут = 기준 / 'build'


def 실행(аргумент_низ):
    subprocess.check_call([str(첫째값) for 첫째값 in аргумент_низ], cwd=str(기준))


def 시작():
    направити_пут.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    објект_фајл_претварач = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    архива_алатка = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for 도구 in ('javac', 시언어번역기, 시플플번역기, 연결편집기, објект_фајл_претварач, архива_алатка):
        if not shutil.which(도구):
            raise SystemExit('필요한 направити_систем 도구 없음: ' + 도구)
    фонт_информација = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    фонт_подаци = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(фонт_подаци) != 65616 * 32 or hashlib.sha256(фонт_подаци).hexdigest() != фонт_информација['sha256']:
        raise SystemExit('터미널 фонт_вриједност подесити_величину/SHA256 불일치')
    извозити_табела = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'језгро.작업', 'jfs_path_start': '기억파일.пут_почети',
               'jfs_path_byte': '기억파일.пут_бајт', 'jfs_open': '기억파일.отворити',
               'jfs_read': '기억파일.읽기', 'jfs_write': '기억파일.писати',
               'jfs_seek': '기억파일.옮기기', 'jfs_close': '기억파일.затворити',
               'jfs_size': '기억파일.подесити_величину', 'jfs_unlink': '기억파일.지우기',
               'jfs_truncate': '기억파일.именовани_скуп_дужина'}
    извозити_табела.update({'jfs_entry_count': '기억파일.파일한도', 'jfs_entry_length': '기억파일.공개이름길이', 'jfs_entry_byte': '기억파일.공개이름바이트', 'jfs_entry_size': '기억파일.공개파일크기'})
    извозити_табела.update({'jdraw_prepare': '화면합성.Припремити', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.исјечак',
        'jdraw_clip_value': '화면합성.исјечак_вриједност', 'jdraw_begin': '화면합성.시작',
        'jdraw_end': '화면합성.마침', 'jdraw_pixel': '화면합성.Пел',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.포인터'})
    извозити_табела.update({'jfs_mkdir': '기억파일.폴더만들기', 'jfs_rmdir': '기억파일.уклонити_директориј', 'jfs_kind': '기억파일.항목종류'})
    извозити_табела.update({'jnet_socket': '되돌림망.만들기', 'jnet_bind': '되돌림망.повезати_крајња_тачка_bbe6b410',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.послати',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.пошиљалац_крајња_тачка', 'jnet_close': '되돌림망.затворити'})
    извозити_табела.update({'jstream_create': 'ток_Мрежа.만들기', 'jstream_bind': 'ток_Мрежа.повезати_крајња_тачка_bbe6b410', 'jstream_listen': 'ток_Мрежа.слушати_крајња_тачка', 'jstream_connect': 'ток_Мрежа.повезати', 'jstream_accept': 'ток_Мрежа.받음', 'jstream_read': 'ток_Мрежа.읽기', 'jstream_write': 'ток_Мрежа.писати', 'jstream_port': 'ток_Мрежа.창구읽기', 'jstream_peer': 'ток_Мрежа.상대창구읽기', 'jstream_close': 'ток_Мрежа.затворити'})
    for 심볼 in list(извозити_табела):
        if 심볼.startswith('jstream_') or 심볼.startswith('jnet_') and 심볼 not in ('jnet_put', 'jnet_get'):
            извозити_табела[심볼.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = извозити_табела.pop(심볼)
    예제들 = ['public final class пакет { public static void Припремити() {']
    for пут in sorted((기준 / '예제').iterdir()):
        if пут.is_file():
            예제들.append('명령해석기.статични_фајл(%s, %s);' %
                (json.dumps(пут.name), json.dumps(пут.read_text(encoding='utf-8'), ensure_ascii=True)))
    (направити_пут / 'пакет.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, 실행)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(направити_пут)) as 작업경로:
        класа_пут = Path(작업경로)
        실행(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', класа_пут, '-sourcepath', класа_пут, '-d', класа_пут] + sorted((기준 / 'извор').glob('*.java')) + [направити_пут / 'пакет.java', направити_пут / '예제꾸러미.java'])
        # фајл·љуска·прозор 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        аргумент_низ = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'језгро.시작', '--heap-words', '1048576', '-o', направити_пут / 'kernel-java.c']
        for 심볼, 메소드 in sorted(извозити_табела.items()):
            аргумент_низ += ['--export', 심볼 + '=' + 메소드]
        실행(аргумент_низ + sorted(класа_пут.glob('*.class')))
    (направити_пут / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    사용자영역만들기(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, архива_алатка, 설정비트, 실행)
    Мрежа = 통신망만들기(기준, 시언어번역기, архива_алатка, 설정비트, 실행)
    원격사용 = 원격만들기(기준, 시언어번역기, архива_алатка, 설정비트, 실행)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', направити_пут]
    빌드작업 = [(시언어번역기, [], направити_пут / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / '기계/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / '기계/виџет.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], направити_пут / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / '기계/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / '기계/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / '기계/корисник.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/унос_тачка_вриједност.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'повезати.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [фајл_унос for фајл_унос in 설정비트 if фајл_унос != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        실행([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', направити_пут / 출력결과])
    실행([архива_алатка, 'rcs', направити_пут / 'libposix-kor-arm64.a', направити_пут / 'posix.o'])
    실행([연결편집기, '--gc-sections', '-T', 기준 / '부팅/веза_изглед.ld', '-Map', направити_пут / 'kernel.map', '-o', направити_пут / 'kernel.elf'] +
        [направити_пут / назив for назив in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', направити_пут / 'libposix-kor-arm64.a', Мрежа, 원격사용, направити_пут / 'remote/libassh.a', направити_пут / 'remote/libbearssl.a', '--end-group'])
    실행([објект_фајл_претварач, '-O', 'binary', направити_пут / 'kernel.elf', направити_пут / 'kernel8.img'])
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
    for назив in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][назив] = hashlib.sha256((направити_пут / назив).read_bytes()).hexdigest()
    (направити_пут / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', направити_пут / 'kernel8.img')


if __name__ == '__main__':
    시작()
