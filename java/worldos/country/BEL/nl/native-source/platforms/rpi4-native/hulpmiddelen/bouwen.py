#!/usr/bin/env python3
"""host javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from build_gebruiker_Space import maken_gebruiker_Space
from build_net import maken_net
from 예제빌드 import 예제만들기
from build_extern import maken_extern

Taken_wortel = Path(__file__).resolve().parents[1]
opslagplaats_wortel = Taken_wortel.parents[1]
build_pad = Taken_wortel / 'build'


def Uitvoeren_opdracht(argument_MATRIX):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_MATRIX], cwd=str(Taken_wortel))


def starten():
    build_pad.mkdir(exist_ok=True)
    C_compiler = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    linker_hulpmiddel = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    object_Bestand_conversieprogramma = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Archief_hulpmiddel = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for hulpmiddelen in ('javac', C_compiler, 시플플번역기, linker_hulpmiddel, object_Bestand_conversieprogramma, Archief_hulpmiddel):
        if not shutil.which(hulpmiddelen):
            raise SystemExit('필요한 bouwen hulpmiddelen 없음: ' + hulpmiddelen)
    lettertype_info = json.loads((Taken_wortel / 'vendor/terminal-font.json').read_text())
    lettertype_gegevens = (Taken_wortel / 'vendor/terminal-font.bin').read_bytes()
    if len(lettertype_gegevens) != 65616 * 32 or hashlib.sha256(lettertype_gegevens).hexdigest() != lettertype_info['sha256']:
        raise SystemExit('terminal lettertype_WAARDE Grootte/SHA256 불일치')
    exporteren_tabel = {'jshell_interactive': '셸입출력.informatie_interactief', 'jshell_output': '셸입출력.tekstuitvoer', 'jshell_input': '셸입출력.invoer_WAARDE', 'java_task': 'Kern.작업', 'jfs_path_start': 'GeheugenBestanden.pad_START',
               'jfs_path_byte': 'GeheugenBestanden.pad_byte', 'jfs_open': 'GeheugenBestanden.Openen',
               'jfs_read': 'GeheugenBestanden.Lezen', 'jfs_write': 'GeheugenBestanden.Schrijven',
               'jfs_seek': 'GeheugenBestanden.zoeken_functie', 'jfs_close': 'GeheugenBestanden.Sluiten',
               'jfs_size': 'GeheugenBestanden.Grootte', 'jfs_unlink': 'GeheugenBestanden.wissen_invoer',
               'jfs_truncate': 'GeheugenBestanden.set_tijdsduur'}
    exporteren_tabel.update({'jfs_entry_count': 'GeheugenBestanden.파일한도', 'jfs_entry_length': 'GeheugenBestanden.공개이름길이', 'jfs_entry_byte': 'GeheugenBestanden.공개이름바이트', 'jfs_entry_size': 'GeheugenBestanden.공개파일크기'})
    exporteren_tabel.update({'jdraw_prepare': '화면합성.Bereid_voor', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.ophalen_hoogte', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.clip',
        'jdraw_clip_value': '화면합성.clip_WAARDE', 'jdraw_begin': '화면합성.starten',
        'jdraw_end': '화면합성.Voltooien', 'jdraw_pixel': '화면합성.pixel',
        'jdraw_rectangle': '화면합성.rechthoek_vullen', 'jdraw_pointer': '화면합성.wijzer'})
    exporteren_tabel.update({'jfs_mkdir': 'GeheugenBestanden.maken_map', 'jfs_rmdir': 'GeheugenBestanden.verwijderen_map', 'jfs_kind': 'GeheugenBestanden.invoer_soort'})
    exporteren_tabel.update({'jnet_socket': 'loopback_net.maken_invoer', 'jnet_bind': 'loopback_net.BIND_eindpunt',
        'jnet_put': 'loopback_net.자료넣기', 'jnet_get': 'loopback_net.자료읽기', 'jnet_send': 'loopback_net.e_mailen',
        'jnet_recv': 'loopback_net.ontvangen', 'jnet_port': 'loopback_net.창구읽기', 'jnet_address': 'loopback_net.주소읽기',
        'jnet_peer': 'loopback_net.afzender_eindpunt', 'jnet_close': 'loopback_net.Sluiten'})
    exporteren_tabel.update({'jstream_create': 'Stream_net.maken_invoer', 'jstream_bind': 'Stream_net.BIND_eindpunt', 'jstream_listen': 'Stream_net.듣기', 'jstream_connect': 'Stream_net.Verbinden', 'jstream_accept': 'Stream_net.accepteren_verbinding', 'jstream_read': 'Stream_net.Lezen', 'jstream_write': 'Stream_net.Schrijven', 'jstream_port': 'Stream_net.창구읽기', 'jstream_peer': 'Stream_net.상대창구읽기', 'jstream_close': 'Stream_net.Sluiten'})
    for symbool_WAARDE in list(exporteren_tabel):
        if symbool_WAARDE.startswith('jstream_') or symbool_WAARDE.startswith('jnet_') and symbool_WAARDE not in ('jnet_put', 'jnet_get'):
            exporteren_tabel[symbool_WAARDE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exporteren_tabel.pop(symbool_WAARDE)
    예제들 = ['public final class bundel { public static void Bereid_voor() {']
    for pad in sorted((Taken_wortel / '예제').iterdir()):
        if pad.is_file():
            예제들.append('Opdrachtvertolker.statisch_Bestand(%s, %s);' %
                (json.dumps(pad.name), json.dumps(pad.read_text(encoding='utf-8'), ensure_ascii=True)))
    (build_pad / 'bundel.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Taken_wortel, opslagplaats_wortel, Uitvoeren_opdracht)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(build_pad)) as 작업경로:
        les_pad = Path(작업경로)
        Uitvoeren_opdracht(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', les_pad, '-sourcepath', les_pad, '-d', les_pad] + sorted((Taken_wortel / 'broncode').glob('*.java')) + [build_pad / 'bundel.java', build_pad / '예제꾸러미.java'])
        # bestand·Shell·Venster 세션·통신과 Java scherm 합성 배열을 모두 수용한다.
        argument_MATRIX = ['sh', opslagplaats_wortel / 'compiler/미리번역.sh', '--entry', 'Kern.starten', '--heap-words', '1048576', '-o', build_pad / 'kernel-java.c']
        for symbool_WAARDE, methode_invoer in sorted(exporteren_tabel.items()):
            argument_MATRIX += ['--export', symbool_WAARDE + '=' + methode_invoer]
        Uitvoeren_opdracht(argument_MATRIX + sorted(les_pad.glob('*.class')))
    (build_pad / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    configuratie_BITS = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = opslagplaats_wortel / 'posix-kor/arm64-native'
    maken_gebruiker_Space(Taken_wortel, opslagplaats_wortel, C_compiler, 시플플번역기, linker_hulpmiddel, Archief_hulpmiddel, configuratie_BITS, Uitvoeren_opdracht)
    net = maken_net(Taken_wortel, C_compiler, Archief_hulpmiddel, configuratie_BITS, Uitvoeren_opdracht)
    extern_gebruik = maken_extern(Taken_wortel, C_compiler, Archief_hulpmiddel, configuratie_BITS, Uitvoeren_opdracht)
    포함인수 = ['-I', 포직스경로 / 'declaraties', '-I', build_pad]
    빌드작업 = [(C_compiler, [], build_pad / 'terminal-font.S', 'font.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Taken_wortel / 'machine/terminal.c', 'terminal.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Taken_wortel / 'machine/schermelement.c', 'widgets.o'),
            (C_compiler, ['-std=c11'], build_pad / 'kernel-java.c', 'java.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Taken_wortel / 'machine/Bord.c', 'board.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Taken_wortel / 'machine/scherm_tekening.c', 'drawing.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Taken_wortel / 'machine/gebruikersruimte.c', 'user.o'),
            (C_compiler, [], Taken_wortel / 'machineopstart/beginpunt_WAARDE.S', 'entry.o'),
            (C_compiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Verbinden.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Taken_wortel / 'tests/Bestand_Oproepen.cpp', 'cpp.o')]
    for compiler_hulpmiddel, 추가영역, 원본자료, uitvoer in 빌드작업:
        원본설정 = [Bestand_invoer for Bestand_invoer in configuratie_BITS if Bestand_invoer != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else configuratie_BITS
        Uitvoeren_opdracht([compiler_hulpmiddel] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', build_pad / uitvoer])
    Uitvoeren_opdracht([Archief_hulpmiddel, 'rcs', build_pad / 'libposix-kor-arm64.a', build_pad / 'posix.o'])
    Uitvoeren_opdracht([linker_hulpmiddel, '--gc-sections', '-T', Taken_wortel / 'machineopstart/koppelindeling.ld', '-Map', build_pad / 'kernel.map', '-o', build_pad / 'kernel.elf'] +
        [build_pad / Naam for Naam in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', build_pad / 'libposix-kor-arm64.a', net, extern_gebruik, build_pad / 'remote/libassh.a', build_pad / 'remote/libbearssl.a', '--end-group'])
    Uitvoeren_opdracht([object_Bestand_conversieprogramma, '-O', 'binary', build_pad / 'kernel.elf', build_pad / 'kernel8.img'])
    bundel_manifest = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Nederlands.Eigen', 'korean_exceptions': 20,
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
    for Naam in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        bundel_manifest['sha256'][Naam] = hashlib.sha256((build_pad / Naam).read_bytes()).hexdigest()
    (build_pad / 'build.json').write_text(json.dumps(bundel_manifest, indent=2) + '\n')
    print('완료:', build_pad / 'kernel8.img')


if __name__ == '__main__':
    starten()
