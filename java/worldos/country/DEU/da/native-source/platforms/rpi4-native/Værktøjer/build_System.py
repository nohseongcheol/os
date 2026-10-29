#!/usr/bin/env python3
"""vært javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from build_bruger_Space import åbne_bruger_Space
from build_netværk import åbne_netværk
from 예제빌드 import 예제만들기
from build_fjern import åbne_fjern

To_do_rod = Path(__file__).resolve().parents[1]
lager_rod = To_do_rod.parents[1]
build_sti = To_do_rod / 'build'


def Udfør_kommando(argument_MATRIX):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_MATRIX], cwd=str(To_do_rod))


def Kør_2():
    build_sti.mkdir(exist_ok=True)
    C_compiler = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    linker_værktøj = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objekt_fil_konverteringsprogram = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arkiv_værktøj = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Værktøjer in ('javac', C_compiler, 시플플번역기, linker_værktøj, objekt_fil_konverteringsprogram, Arkiv_værktøj):
        if not shutil.which(Værktøjer):
            raise SystemExit('필요한 build_System Værktøjer 없음: ' + Værktøjer)
    skrifttype_info = json.loads((To_do_rod / 'vendor/terminal-font.json').read_text())
    skrifttype_data = (To_do_rod / 'vendor/terminal-font.bin').read_bytes()
    if len(skrifttype_data) != 65616 * 32 or hashlib.sha256(skrifttype_data).hexdigest() != skrifttype_info['sha256']:
        raise SystemExit('Terminal skrifttype_VÆRDI Størrelse/SHA256 불일치')
    eksportere_tabel = {'jshell_interactive': '셸입출력.it_interaktiv', 'jshell_output': '셸입출력.Udgang', 'jshell_input': '셸입출력.input_VÆRDI', 'java_task': 'kerne.작업', 'jfs_path_start': 'Hukommelse_Filer.sti_START',
               'jfs_path_byte': 'Hukommelse_Filer.sti_byte', 'jfs_open': 'Hukommelse_Filer.Åbn',
               'jfs_read': 'Hukommelse_Filer.Læse', 'jfs_write': 'Hukommelse_Filer.Skrive',
               'jfs_seek': 'Hukommelse_Filer.søge_placere', 'jfs_close': 'Hukommelse_Filer.Luk',
               'jfs_size': 'Hukommelse_Filer.Størrelse', 'jfs_unlink': 'Hukommelse_Filer.slette_post',
               'jfs_truncate': 'Hukommelse_Filer.sæt_varighed'}
    eksportere_tabel.update({'jfs_entry_count': 'Hukommelse_Filer.파일한도', 'jfs_entry_length': 'Hukommelse_Filer.공개이름길이', 'jfs_entry_byte': 'Hukommelse_Filer.공개이름바이트', 'jfs_entry_size': 'Hukommelse_Filer.공개파일크기'})
    eksportere_tabel.update({'jdraw_prepare': '화면합성.Tilrettelæg', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klippe',
        'jdraw_clip_value': '화면합성.klippe_VÆRDI', 'jdraw_begin': '화면합성.Kør_2',
        'jdraw_end': '화면합성.Udfør', 'jdraw_pixel': '화면합성.pixel',
        'jdraw_rectangle': '화면합성.rektangel_udfyld', 'jdraw_pointer': '화면합성.markør'})
    eksportere_tabel.update({'jfs_mkdir': 'Hukommelse_Filer.åbne_mappe', 'jfs_rmdir': 'Hukommelse_Filer.fjerne_mappe', 'jfs_kind': 'Hukommelse_Filer.항목종류'})
    eksportere_tabel.update({'jnet_socket': 'tilbagekobling_netværk.åbne_post_81b8d99b', 'jnet_bind': 'tilbagekobling_netværk.BIND_slutpunkt',
        'jnet_put': 'tilbagekobling_netværk.자료넣기', 'jnet_get': 'tilbagekobling_netværk.자료읽기', 'jnet_send': 'tilbagekobling_netværk.maile',
        'jnet_recv': 'tilbagekobling_netværk.modtage', 'jnet_port': 'tilbagekobling_netværk.창구읽기', 'jnet_address': 'tilbagekobling_netværk.주소읽기',
        'jnet_peer': 'tilbagekobling_netværk.afsender_slutpunkt', 'jnet_close': 'tilbagekobling_netværk.Luk'})
    eksportere_tabel.update({'jstream_create': 'strøm_netværk.åbne_post_81b8d99b', 'jstream_bind': 'strøm_netværk.BIND_slutpunkt', 'jstream_listen': 'strøm_netværk.lytte_slutpunkt', 'jstream_connect': 'strøm_netværk.Tilslut', 'jstream_accept': 'strøm_netværk.acceptere_forbindelse', 'jstream_read': 'strøm_netværk.Læse', 'jstream_write': 'strøm_netværk.Skrive', 'jstream_port': 'strøm_netværk.창구읽기', 'jstream_peer': 'strøm_netværk.상대창구읽기', 'jstream_close': 'strøm_netværk.Luk'})
    for symbol_VÆRDI in list(eksportere_tabel):
        if symbol_VÆRDI.startswith('jstream_') or symbol_VÆRDI.startswith('jnet_') and symbol_VÆRDI not in ('jnet_put', 'jnet_get'):
            eksportere_tabel[symbol_VÆRDI.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = eksportere_tabel.pop(symbol_VÆRDI)
    예제들 = ['public final class bundt { public static void Tilrettelæg() {']
    for Sti in sorted((To_do_rod / '예제').iterdir()):
        if Sti.is_file():
            예제들.append('명령해석기.statisk_fil(%s, %s);' %
                (json.dumps(Sti.name), json.dumps(Sti.read_text(encoding='utf-8'), ensure_ascii=True)))
    (build_sti / 'bundt.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(To_do_rod, lager_rod, Udfør_kommando)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(build_sti)) as 작업경로:
        Hold_sti = Path(작업경로)
        Udfør_kommando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Hold_sti, '-sourcepath', Hold_sti, '-d', Hold_sti] + sorted((To_do_rod / 'KILDE').glob('*.java')) + [build_sti / 'bundt.java', build_sti / '예제꾸러미.java'])
        # Fil·Shell·Vindue 세션·통신과 Java skærmbillede 합성 배열을 모두 수용한다.
        argument_MATRIX = ['sh', lager_rod / 'compiler/미리번역.sh', '--entry', 'kerne.Kør_2', '--heap-words', '1048576', '-o', build_sti / 'kernel-java.c']
        for symbol_VÆRDI, metode_post in sorted(eksportere_tabel.items()):
            argument_MATRIX += ['--export', symbol_VÆRDI + '=' + metode_post]
        Udfør_kommando(argument_MATRIX + sorted(Hold_sti.glob('*.class')))
    (build_sti / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfiguration_BITS = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = lager_rod / 'posix-kor/arm64-native'
    åbne_bruger_Space(To_do_rod, lager_rod, C_compiler, 시플플번역기, linker_værktøj, Arkiv_værktøj, konfiguration_BITS, Udfør_kommando)
    netværk = åbne_netværk(To_do_rod, C_compiler, Arkiv_værktøj, konfiguration_BITS, Udfør_kommando)
    fjern_brug = åbne_fjern(To_do_rod, C_compiler, Arkiv_værktøj, konfiguration_BITS, Udfør_kommando)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', build_sti]
    빌드작업 = [(C_compiler, [], build_sti / 'terminal-font.S', 'font.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], To_do_rod / 'maskine/Terminal.c', 'terminal.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], To_do_rod / 'maskine/widget.c', 'widgets.o'),
            (C_compiler, ['-std=c11'], build_sti / 'kernel-java.c', 'java.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], To_do_rod / 'maskine/Tavle.c', 'board.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], To_do_rod / 'maskine/skærmbillede_tegning.c', 'drawing.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], To_do_rod / 'maskine/bruger.c', 'user.o'),
            (C_compiler, [], To_do_rod / '부팅/indgangspunkt_VÆRDI.S', 'entry.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Tilslut.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], To_do_rod / '시험/fil_Opkald.cpp', 'cpp.o')]
    for compiler_værktøj, 추가영역, 원본자료, produktoutput in 빌드작업:
        원본설정 = [fil_post for fil_post in konfiguration_BITS if fil_post != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfiguration_BITS
        Udfør_kommando([compiler_værktøj] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', build_sti / produktoutput])
    Udfør_kommando([Arkiv_værktøj, 'rcs', build_sti / 'libposix-kor-arm64.a', build_sti / 'posix.o'])
    Udfør_kommando([linker_værktøj, '--gc-sections', '-T', To_do_rod / '부팅/Link_Layout.ld', '-Map', build_sti / 'kernel.map', '-o', build_sti / 'kernel.elf'] +
        [build_sti / Navn for Navn in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', build_sti / 'libposix-kor-arm64.a', netværk, fjern_brug, build_sti / 'remote/libassh.a', build_sti / 'remote/libbearssl.a', '--end-group'])
    Udfør_kommando([objekt_fil_konverteringsprogram, '-O', 'binary', build_sti / 'kernel.elf', build_sti / 'kernel8.img'])
    bundt_manifest = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Dansk.eget', 'korean_exceptions': 20,
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
    for Navn in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        bundt_manifest['sha256'][Navn] = hashlib.sha256((build_sti / Navn).read_bytes()).hexdigest()
    (build_sti / 'build.json').write_text(json.dumps(bundt_manifest, indent=2) + '\n')
    print('완료:', build_sti / 'kernel8.img')


if __name__ == '__main__':
    Kør_2()
