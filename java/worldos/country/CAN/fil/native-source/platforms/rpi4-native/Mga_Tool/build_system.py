#!/usr/bin/env python3
"""host javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from build_gumagamit_SPACE import Create_gumagamit_SPACE
from build_Network import Create_Network
from 예제빌드 import 예제만들기
from build_malayuan import Create_malayuan

Project_root = Path(__file__).resolve().parents[1]
repository_root = Project_root.parents[1]
build_path = Project_root / 'build'


def Mag_execute_utos(argumento_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argumento_ARRAY], cwd=str(Project_root))


def run():
    build_path.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    bagay_file_converter = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Archive_tool = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Mga_Tool in ('javac', 시언어번역기, 시플플번역기, 연결편집기, bagay_file_converter, Archive_tool):
        if not shutil.which(Mga_Tool):
            raise SystemExit('필요한 build_system Mga_Tool 없음: ' + Mga_Tool)
    font_impormasyon = json.loads((Project_root / 'vendor/terminal-font.json').read_text())
    font_data = (Project_root / 'vendor/terminal-font.bin').read_bytes()
    if len(font_data) != 65616 * 32 or hashlib.sha256(font_data).hexdigest() != font_impormasyon['sha256']:
        raise SystemExit('Terminal font_VALUE sukat_82232621/SHA256 불일치')
    export_talahanayan = {'jshell_interactive': '셸입출력.information_technology_tumutugon_interactive', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'kernel.작업', 'jfs_path_start': 'Memory_Mga_File.path_Start',
               'jfs_path_byte': 'Memory_Mga_File.path_byte', 'jfs_open': 'Memory_Mga_File.buksan',
               'jfs_read': 'Memory_Mga_File.읽기', 'jfs_write': 'Memory_Mga_File.sumulat',
               'jfs_seek': 'Memory_Mga_File.i_seek_posisyon', 'jfs_close': 'Memory_Mga_File.isara',
               'jfs_size': 'Memory_Mga_File.sukat_82232621', 'jfs_unlink': 'Memory_Mga_File.burahin_pagpasok',
               'jfs_truncate': 'Memory_Mga_File.set_haba'}
    export_talahanayan.update({'jfs_entry_count': 'Memory_Mga_File.파일한도', 'jfs_entry_length': 'Memory_Mga_File.공개이름길이', 'jfs_entry_byte': 'Memory_Mga_File.공개이름바이트', 'jfs_entry_size': 'Memory_Mga_File.공개파일크기'})
    export_talahanayan.update({'jdraw_prepare': '화면합성.Ihanda', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.clip',
        'jdraw_clip_value': '화면합성.clip_VALUE', 'jdraw_begin': '화면합성.run',
        'jdraw_end': '화면합성.Tapos_Na', 'jdraw_pixel': '화면합성.pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.pointer'})
    export_talahanayan.update({'jfs_mkdir': 'Memory_Mga_File.Create_Directory', 'jfs_rmdir': 'Memory_Mga_File.tanggalin_Directory', 'jfs_kind': 'Memory_Mga_File.항목종류'})
    export_talahanayan.update({'jnet_socket': '되돌림망.Create_pagpasok', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.i_email',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.isara'})
    export_talahanayan.update({'jstream_create': 'Stream_Network.Create_pagpasok', 'jstream_bind': 'Stream_Network.묶기', 'jstream_listen': 'Stream_Network.듣기', 'jstream_connect': 'Stream_Network.CONNECT', 'jstream_accept': 'Stream_Network.tanggapin_koneksyon', 'jstream_read': 'Stream_Network.읽기', 'jstream_write': 'Stream_Network.sumulat', 'jstream_port': 'Stream_Network.창구읽기', 'jstream_peer': 'Stream_Network.상대창구읽기', 'jstream_close': 'Stream_Network.isara'})
    for simbolo_VALUE in list(export_talahanayan):
        if simbolo_VALUE.startswith('jstream_') or simbolo_VALUE.startswith('jnet_') and simbolo_VALUE not in ('jnet_put', 'jnet_get'):
            export_talahanayan[simbolo_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = export_talahanayan.pop(simbolo_VALUE)
    예제들 = ['public final class bundle { public static void Ihanda() {']
    for path in sorted((Project_root / '예제').iterdir()):
        if path.is_file():
            예제들.append('명령해석기.hindi_nababago_file(%s, %s);' %
                (json.dumps(path.name), json.dumps(path.read_text(encoding='utf-8'), ensure_ascii=True)))
    (build_path / 'bundle.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_root, repository_root, Mag_execute_utos)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(build_path)) as 작업경로:
        kategorya_path = Path(작업경로)
        Mag_execute_utos(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', kategorya_path, '-sourcepath', kategorya_path, '-d', kategorya_path] + sorted((Project_root / 'pinagmulan').glob('*.java')) + [build_path / 'bundle.java', build_path / '예제꾸러미.java'])
        # file·shell·window 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argumento_ARRAY = ['sh', repository_root / 'compiler/미리번역.sh', '--entry', 'kernel.run', '--heap-words', '1048576', '-o', build_path / 'kernel-java.c']
        for simbolo_VALUE, pamamaraan_pagpasok in sorted(export_talahanayan.items()):
            argumento_ARRAY += ['--export', simbolo_VALUE + '=' + pamamaraan_pagpasok]
        Mag_execute_utos(argumento_ARRAY + sorted(kategorya_path.glob('*.class')))
    (build_path / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    kompigurasyon_Background_Intelligent_Transfer_Service = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = repository_root / 'posix-kor/arm64-native'
    Create_gumagamit_SPACE(Project_root, repository_root, 시언어번역기, 시플플번역기, 연결편집기, Archive_tool, kompigurasyon_Background_Intelligent_Transfer_Service, Mag_execute_utos)
    Network = Create_Network(Project_root, 시언어번역기, Archive_tool, kompigurasyon_Background_Intelligent_Transfer_Service, Mag_execute_utos)
    원격사용 = Create_malayuan(Project_root, 시언어번역기, Archive_tool, kompigurasyon_Background_Intelligent_Transfer_Service, Mag_execute_utos)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', build_path]
    빌드작업 = [(시언어번역기, [], build_path / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_root / 'machine/Terminal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_root / 'machine/widget.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], build_path / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_root / 'machine/board.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_root / 'machine/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_root / 'machine/gumagamit.c', 'user.o'),
            (시언어번역기, [], Project_root / '부팅/pagpasok_point_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'CONNECT.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_root / '시험/file_Mga_Tawag.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [file_pagpasok for file_pagpasok in kompigurasyon_Background_Intelligent_Transfer_Service if file_pagpasok != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else kompigurasyon_Background_Intelligent_Transfer_Service
        Mag_execute_utos([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', build_path / 출력결과])
    Mag_execute_utos([Archive_tool, 'rcs', build_path / 'libposix-kor-arm64.a', build_path / 'posix.o'])
    Mag_execute_utos([연결편집기, '--gc-sections', '-T', Project_root / '부팅/Link_Layout.ld', '-Map', build_path / 'kernel.map', '-o', build_path / 'kernel.elf'] +
        [build_path / pangalan for pangalan in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', build_path / 'libposix-kor-arm64.a', Network, 원격사용, build_path / 'remote/libassh.a', build_path / 'remote/libbearssl.a', '--end-group'])
    Mag_execute_utos([bagay_file_converter, '-O', 'binary', build_path / 'kernel.elf', build_path / 'kernel8.img'])
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
    for pangalan in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][pangalan] = hashlib.sha256((build_path / pangalan).read_bytes()).hexdigest()
    (build_path / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', build_path / 'kernel8.img')


if __name__ == '__main__':
    run()
