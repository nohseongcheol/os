#!/usr/bin/env python3
"""go_nea_ditirelo javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from aga_mošomiši_sekgoba import 사용자영역만들기
from aga_Netweke import 통신망만들기
from 예제빌드 import 예제만들기
from aga_ya_kgole import 원격만들기

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
aga_tsela = 기준 / 'build'


def phethagatša_taelo(akumente_arei):
    subprocess.check_call([str(첫째값) for 첫째값 in akumente_arei], cwd=str(기준))


def Diriša():
    aga_tsela.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    selo_faele_sefetošetši = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Akhaebe_tholosi = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Ditholosi in ('javac', 시언어번역기, 시플플번역기, 연결편집기, selo_faele_sefetošetši, Akhaebe_tholosi):
        if not shutil.which(Ditholosi):
            raise SystemExit('필요한 aga_lenaneo Ditholosi 없음: ' + Ditholosi)
    fonte_tshedimošo = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    fonte_data = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(fonte_data) != 65616 * 32 or hashlib.sha256(fonte_data).hexdigest() != fonte_tshedimošo['sha256']:
        raise SystemExit('터미널 fonte_boleng Bogolo/SHA256 불일치')
    Iša_tafola = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'khenele.작업', 'jfs_path_start': 'memori_Difaele.tsela_Thomišo',
               'jfs_path_byte': 'memori_Difaele.tsela_paete', 'jfs_open': 'memori_Difaele.Bula',
               'jfs_read': 'memori_Difaele.Bala', 'jfs_write': 'memori_Difaele.Ngwala',
               'jfs_seek': 'memori_Difaele.옮기기', 'jfs_close': 'memori_Difaele.Tswalela',
               'jfs_size': 'memori_Difaele.Bogolo', 'jfs_unlink': 'memori_Difaele.지우기',
               'jfs_truncate': 'memori_Difaele.sehlopha_botelele'}
    Iša_tafola.update({'jfs_entry_count': 'memori_Difaele.파일한도', 'jfs_entry_length': 'memori_Difaele.공개이름길이', 'jfs_entry_byte': 'memori_Difaele.공개이름바이트', 'jfs_entry_size': 'memori_Difaele.공개파일크기'})
    Iša_tafola.update({'jdraw_prepare': '화면합성.Lokišetša', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.setsopolwa',
        'jdraw_clip_value': '화면합성.setsopolwa_boleng', 'jdraw_begin': '화면합성.Diriša',
        'jdraw_end': '화면합성.Fetša', 'jdraw_pixel': '화면합성.phele',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.sešupi'})
    Iša_tafola.update({'jfs_mkdir': 'memori_Difaele.폴더만들기', 'jfs_rmdir': 'memori_Difaele.tloša_lelokelelo', 'jfs_kind': 'memori_Difaele.항목종류'})
    Iša_tafola.update({'jnet_socket': '되돌림망.만들기', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.Romela',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Tswalela'})
    Iša_tafola.update({'jstream_create': 'Stream_Netweke.만들기', 'jstream_bind': 'Stream_Netweke.묶기', 'jstream_listen': 'Stream_Netweke.듣기', 'jstream_connect': 'Stream_Netweke.Ikgokaganye', 'jstream_accept': 'Stream_Netweke.amogela_kgokaganya', 'jstream_read': 'Stream_Netweke.Bala', 'jstream_write': 'Stream_Netweke.Ngwala', 'jstream_port': 'Stream_Netweke.창구읽기', 'jstream_peer': 'Stream_Netweke.상대창구읽기', 'jstream_close': 'Stream_Netweke.Tswalela'})
    for leswao_boleng in list(Iša_tafola):
        if leswao_boleng.startswith('jstream_') or leswao_boleng.startswith('jnet_') and leswao_boleng not in ('jnet_put', 'jnet_get'):
            Iša_tafola[leswao_boleng.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = Iša_tafola.pop(leswao_boleng)
    예제들 = ['public final class sehlopha { public static void Lokišetša() {']
    for Tsejana in sorted((기준 / '예제').iterdir()):
        if Tsejana.is_file():
            예제들.append('명령해석기.ya_go_se_fetoge_faele(%s, %s);' %
                (json.dumps(Tsejana.name), json.dumps(Tsejana.read_text(encoding='utf-8'), ensure_ascii=True)))
    (aga_tsela / 'sehlopha.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, phethagatša_taelo)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(aga_tsela)) as 작업경로:
        legoro_tsela = Path(작업경로)
        phethagatša_taelo(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', legoro_tsela, '-sourcepath', legoro_tsela, '-d', legoro_tsela] + sorted((기준 / 'mohlodi').glob('*.java')) + [aga_tsela / 'sehlopha.java', aga_tsela / '예제꾸러미.java'])
        # Faele·šele·lefastere 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        akumente_arei = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'khenele.Diriša', '--heap-words', '1048576', '-o', aga_tsela / 'kernel-java.c']
        for leswao_boleng, mokgwa_go_tsenya_tshedimošo in sorted(Iša_tafola.items()):
            akumente_arei += ['--export', leswao_boleng + '=' + mokgwa_go_tsenya_tshedimošo]
        phethagatša_taelo(akumente_arei + sorted(legoro_tsela.glob('*.class')))
    (aga_tsela / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    사용자영역만들기(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Akhaebe_tholosi, 설정비트, phethagatša_taelo)
    Netweke = 통신망만들기(기준, 시언어번역기, Akhaebe_tholosi, 설정비트, phethagatša_taelo)
    원격사용 = 원격만들기(기준, 시언어번역기, Akhaebe_tholosi, 설정비트, phethagatša_taelo)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', aga_tsela]
    빌드작업 = [(시언어번역기, [], aga_tsela / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'motšhene/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'motšhene/witšete.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], aga_tsela / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'motšhene/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'motšhene/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'motšhene/mošomiši.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/go_tsenya_tshedimošo_ntlha_boleng.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Ikgokaganye.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [faele_go_tsenya_tshedimošo for faele_go_tsenya_tshedimošo in 설정비트 if faele_go_tsenya_tshedimošo != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        phethagatša_taelo([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', aga_tsela / 출력결과])
    phethagatša_taelo([Akhaebe_tholosi, 'rcs', aga_tsela / 'libposix-kor-arm64.a', aga_tsela / 'posix.o'])
    phethagatša_taelo([연결편집기, '--gc-sections', '-T', 기준 / '부팅/linke_Sebopego.ld', '-Map', aga_tsela / 'kernel.map', '-o', aga_tsela / 'kernel.elf'] +
        [aga_tsela / Leina for Leina in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', aga_tsela / 'libposix-kor-arm64.a', Netweke, 원격사용, aga_tsela / 'remote/libassh.a', aga_tsela / 'remote/libbearssl.a', '--end-group'])
    phethagatša_taelo([selo_faele_sefetošetši, '-O', 'binary', aga_tsela / 'kernel.elf', aga_tsela / 'kernel8.img'])
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
    for Leina in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Leina] = hashlib.sha256((aga_tsela / Leina).read_bytes()).hexdigest()
    (aga_tsela / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', aga_tsela / 'kernel8.img')


if __name__ == '__main__':
    Diriša()
