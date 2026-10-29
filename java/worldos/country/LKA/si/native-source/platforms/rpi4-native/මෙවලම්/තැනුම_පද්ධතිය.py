#!/usr/bin/env python3
"""ධාරකය javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from තැනුම_පරිශීලක_ස්ථානය import සාදන්න_පරිශීලක_ස්ථානය
from තැනුම_ජාලය import සාදන්න_ජාලය_48d29d6d
from 예제빌드 import 예제만들기
from තැනුම_දුරස්ථ import සාදන්න_දුරස්ථ

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
තැනුම_පෙත = 기준 / 'build'


def ක්_රියාත්මක_කරන්න_විධානය(විස්තාරකය_ආරා_ව):
    subprocess.check_call([str(첫째값) for 첫째값 in විස්තාරකය_ආරා_ව], cwd=str(기준))


def ක්_රියාත්මක_කරන්න_2():
    තැනුම_පෙත.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    වස්තුව_ගොනුව_පරිවර්තකය = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    සංරක්ෂිතය_මෙවලම = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for මෙවලම් in ('javac', 시언어번역기, 시플플번역기, 연결편집기, වස්තුව_ගොනුව_පරිවර්තකය, සංරක්ෂිතය_මෙවලම):
        if not shutil.which(මෙවලම්):
            raise SystemExit('필요한 තැනුම_පද්ධතිය මෙවලම් 없음: ' + මෙවලම්)
    ෆොන්ටය_තතු = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    ෆොන්ටය_දත්ත = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(ෆොන්ටය_දත්ත) != 65616 * 32 or hashlib.sha256(ෆොන්ටය_දත්ත).hexdigest() != ෆොන්ටය_තතු['sha256']:
        raise SystemExit('අග්_රය ෆොන්ටය_අගය ප්_රමාණය/SHA256 불일치')
    නිර්යාත_කරන්න_වගුව = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'කර්නලය.작업', 'jfs_path_start': 'මතකය_ගොනු.පෙත_ඇරඹුම',
               'jfs_path_byte': 'මතකය_ගොනු.පෙත_බයිටය', 'jfs_open': 'මතකය_ගොනු.විවෘත_කරන්න',
               'jfs_read': 'මතකය_ගොනු.කියවීම', 'jfs_write': 'මතකය_ගොනු.ලිවීම',
               'jfs_seek': 'මතකය_ගොනු.옮기기', 'jfs_close': 'මතකය_ගොනු.වසන්න',
               'jfs_size': 'මතකය_ගොනු.ප්_රමාණය', 'jfs_unlink': 'මතකය_ගොනු.지우기',
               'jfs_truncate': 'මතකය_ගොනු.කට්ටලය_දිග'}
    නිර්යාත_කරන්න_වගුව.update({'jfs_entry_count': 'මතකය_ගොනු.파일한도', 'jfs_entry_length': 'මතකය_ගොනු.공개이름길이', 'jfs_entry_byte': 'මතකය_ගොනු.공개이름바이트', 'jfs_entry_size': 'මතකය_ගොනු.공개파일크기'})
    නිර්යාත_කරන්න_වගුව.update({'jdraw_prepare': '화면합성.පිළියෙල_කරන්න', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.පසුර',
        'jdraw_clip_value': '화면합성.පසුර_අගය', 'jdraw_begin': '화면합성.ක්_රියාත්මක_කරන්න_2',
        'jdraw_end': '화면합성.ෆිනිෂ්', 'jdraw_pixel': '화면합성.පික්සලය',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.පොයින්ටරය'})
    නිර්යාත_කරන්න_වගුව.update({'jfs_mkdir': 'මතකය_ගොනු.සාදන්න_නාමාවලිය', 'jfs_rmdir': 'මතකය_ගොනු.ඉවත්_කරන්න_නාමාවලිය', 'jfs_kind': 'මතකය_ගොනු.항목종류'})
    නිර්යාත_කරන්න_වගුව.update({'jnet_socket': '되돌림망.සාදන්න_පිවිසුම', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ඊමේල්',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.වසන්න'})
    නිර්යාත_කරන්න_වගුව.update({'jstream_create': 'දහර_ජාලය.සාදන්න_පිවිසුම', 'jstream_bind': 'දහර_ජාලය.묶기', 'jstream_listen': 'දහර_ජාලය.듣기', 'jstream_connect': 'දහර_ජාලය.සම්බන්ද_වන්න', 'jstream_accept': 'දහර_ජාලය.පිළිගන්න_සබැඳුම', 'jstream_read': 'දහර_ජාලය.කියවීම', 'jstream_write': 'දහර_ජාලය.ලිවීම', 'jstream_port': 'දහර_ජාලය.창구읽기', 'jstream_peer': 'දහර_ජාලය.상대창구읽기', 'jstream_close': 'දහර_ජාලය.වසන්න'})
    for සංකේතය_අගය in list(නිර්යාත_කරන්න_වගුව):
        if සංකේතය_අගය.startswith('jstream_') or සංකේතය_අගය.startswith('jnet_') and සංකේතය_අගය not in ('jnet_put', 'jnet_get'):
            නිර්යාත_කරන්න_වගුව[සංකේතය_අගය.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = නිර්යාත_කරන්න_වගුව.pop(සංකේතය_අගය)
    예제들 = ['public final class පොදිය { public static void පිළියෙල_කරන්න() {']
    for මාර්_ගය in sorted((기준 / '예제').iterdir()):
        if මාර්_ගය.is_file():
            예제들.append('명령해석기.ස්ථිතික_ගොනුව(%s, %s);' %
                (json.dumps(මාර්_ගය.name), json.dumps(මාර්_ගය.read_text(encoding='utf-8'), ensure_ascii=True)))
    (තැනුම_පෙත / 'පොදිය.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, ක්_රියාත්මක_කරන්න_විධානය)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(තැනුම_පෙත)) as 작업경로:
        පන්තිය_පෙත = Path(작업경로)
        ක්_රියාත්මක_කරන්න_විධානය(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', පන්තිය_පෙත, '-sourcepath', පන්තිය_පෙත, '-d', පන්තිය_පෙත] + sorted((기준 / 'මූලය').glob('*.java')) + [තැනුම_පෙත / 'පොදිය.java', තැනුම_පෙත / '예제꾸러미.java'])
        # ගොනු·කවචය·කවුළුව 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        විස්තාරකය_ආරා_ව = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'කර්නලය.ක්_රියාත්මක_කරන්න_2', '--heap-words', '1048576', '-o', තැනුම_පෙත / 'kernel-java.c']
        for සංකේතය_අගය, ක්_රමය_පිවිසුම in sorted(නිර්යාත_කරන්න_වගුව.items()):
            විස්තාරකය_ආරා_ව += ['--export', සංකේතය_අගය + '=' + ක්_රමය_පිවිසුම]
        ක්_රියාත්මක_කරන්න_විධානය(විස්තාරකය_ආරා_ව + sorted(පන්තිය_පෙත.glob('*.class')))
    (තැනුම_පෙත / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    සාදන්න_පරිශීලක_ස්ථානය(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, සංරක්ෂිතය_මෙවලම, 설정비트, ක්_රියාත්මක_කරන්න_විධානය)
    ජාලය = සාදන්න_ජාලය_48d29d6d(기준, 시언어번역기, සංරක්ෂිතය_මෙවලම, 설정비트, ක්_රියාත්මක_කරන්න_විධානය)
    원격사용 = සාදන්න_දුරස්ථ(기준, 시언어번역기, සංරක්ෂිතය_මෙවලම, 설정비트, ක්_රියාත්මක_කරන්න_විධානය)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', තැනුම_පෙත]
    빌드작업 = [(시언어번역기, [], තැනුම_පෙත / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'යන්ත්_රය/අග්_රය.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'යන්ත්_රය/විජෙට්ටුව.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], තැනුම_පෙත / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'යන්ත්_රය/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'යන්ත්_රය/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'යන්ත්_රය/පරිශීලක.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/පිවිසුම_ලකුණ_අගය.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'සම්බන්ද_වන්න.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ගොනුව_පිවිසුම for ගොනුව_පිවිසුම in 설정비트 if ගොනුව_පිවිසුම != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        ක්_රියාත්මක_කරන්න_විධානය([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', තැනුම_පෙත / 출력결과])
    ක්_රියාත්මක_කරන්න_විධානය([සංරක්ෂිතය_මෙවලම, 'rcs', තැනුම_පෙත / 'libposix-kor-arm64.a', තැනුම_පෙත / 'posix.o'])
    ක්_රියාත්මක_කරන්න_විධානය([연결편집기, '--gc-sections', '-T', 기준 / '부팅/සබැඳිය_සැකැස්ම.ld', '-Map', තැනුම_පෙත / 'kernel.map', '-o', තැනුම_පෙත / 'kernel.elf'] +
        [තැනුම_පෙත / නම for නම in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', තැනුම_පෙත / 'libposix-kor-arm64.a', ජාලය, 원격사용, තැනුම_පෙත / 'remote/libassh.a', තැනුම_පෙත / 'remote/libbearssl.a', '--end-group'])
    ක්_රියාත්මක_කරන්න_විධානය([වස්තුව_ගොනුව_පරිවර්තකය, '-O', 'binary', තැනුම_පෙත / 'kernel.elf', තැනුම_පෙත / 'kernel8.img'])
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
    for නම in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][නම] = hashlib.sha256((තැනුම_පෙත / නම).read_bytes()).hexdigest()
    (තැනුම_පෙත / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', තැනුම_පෙත / 'kernel8.img')


if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_2()
