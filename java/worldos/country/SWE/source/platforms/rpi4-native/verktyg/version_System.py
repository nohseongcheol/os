#!/usr/bin/env python3
"""värd javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from version_användare_Space import Skapa_användare_Space
from version_nätverk import Skapa_nätverk
from 예제빌드 import 예제만들기
from version_fjärr import Skapa_fjärr

åtgärd_rot = Path(__file__).resolve().parents[1]
centrallager_rot = åtgärd_rot.parents[1]
version_väg = åtgärd_rot / 'build'


def köra_kommando(argument_MATRIS):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_MATRIS], cwd=str(åtgärd_rot))


def Kör():
    version_väg.mkdir(exist_ok=True)
    C_kompilerare = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    länkare_verktyg = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objekt_fil_konverterare = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arkiv_verktyg = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for verktyg in ('javac', C_kompilerare, 시플플번역기, länkare_verktyg, objekt_fil_konverterare, Arkiv_verktyg):
        if not shutil.which(verktyg):
            raise SystemExit('필요한 version_System verktyg 없음: ' + verktyg)
    teckensnitt_info = json.loads((åtgärd_rot / 'vendor/terminal-font.json').read_text())
    teckensnitt_data = (åtgärd_rot / 'vendor/terminal-font.bin').read_bytes()
    if len(teckensnitt_data) != 65616 * 32 or hashlib.sha256(teckensnitt_data).hexdigest() != teckensnitt_info['sha256']:
        raise SystemExit('kommandotolk teckensnitt_värde Storlek/SHA256 불일치')
    exportera_tabell = {'jshell_interactive': '셸입출력.informationsteknik_interaktiv', 'jshell_output': '셸입출력.utmatningsposition', 'jshell_input': '셸입출력.indata_värde', 'java_task': 'kärna.작업', 'jfs_path_start': 'Minne_Filer.väg_START',
               'jfs_path_byte': 'Minne_Filer.väg_byte', 'jfs_open': 'Minne_Filer.Öppna',
               'jfs_read': 'Minne_Filer.Läs', 'jfs_write': 'Minne_Filer.Skriv',
               'jfs_seek': 'Minne_Filer.söka_placera', 'jfs_close': 'Minne_Filer.Stäng',
               'jfs_size': 'Minne_Filer.Storlek', 'jfs_unlink': 'Minne_Filer.radera_post',
               'jfs_truncate': 'Minne_Filer.uppsättning_längd'}
    exportera_tabell.update({'jfs_entry_count': 'Minne_Filer.파일한도', 'jfs_entry_length': 'Minne_Filer.공개이름길이', 'jfs_entry_byte': 'Minne_Filer.공개이름바이트', 'jfs_entry_size': 'Minne_Filer.공개파일크기'})
    exportera_tabell.update({'jdraw_prepare': '화면합성.Förbereda', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klipp',
        'jdraw_clip_value': '화면합성.klipp_värde', 'jdraw_begin': '화면합성.Kör',
        'jdraw_end': '화면합성.slut', 'jdraw_pixel': '화면합성.bildpunkt',
        'jdraw_rectangle': '화면합성.rektangel_Fyll', 'jdraw_pointer': '화면합성.markör'})
    exportera_tabell.update({'jfs_mkdir': 'Minne_Filer.Skapa_Katalog', 'jfs_rmdir': 'Minne_Filer.ta_bort_Katalog', 'jfs_kind': 'Minne_Filer.post_variant'})
    exportera_tabell.update({'jnet_socket': 'loopback_nätverk.Skapa_post', 'jnet_bind': 'loopback_nätverk.BIND_deltagare',
        'jnet_put': 'loopback_nätverk.자료넣기', 'jnet_get': 'loopback_nätverk.läsa_data', 'jnet_send': 'loopback_nätverk.skicka',
        'jnet_recv': 'loopback_nätverk.få', 'jnet_port': 'loopback_nätverk.läsa_deltagare_port', 'jnet_address': 'loopback_nätverk.läsa_ADRESS',
        'jnet_peer': 'loopback_nätverk.avsändare_deltagare', 'jnet_close': 'loopback_nätverk.Stäng'})
    exportera_tabell.update({'jstream_create': 'flöde_nätverk.Skapa_post', 'jstream_bind': 'flöde_nätverk.BIND_deltagare', 'jstream_listen': 'flöde_nätverk.lyssna_deltagare', 'jstream_connect': 'flöde_nätverk.Anslut', 'jstream_accept': 'flöde_nätverk.acceptera_kontakt', 'jstream_read': 'flöde_nätverk.Läs', 'jstream_write': 'flöde_nätverk.Skriv', 'jstream_port': 'flöde_nätverk.läsa_deltagare_port', 'jstream_peer': 'flöde_nätverk.läsa_peer_port', 'jstream_close': 'flöde_nätverk.Stäng'})
    for symbol_värde in list(exportera_tabell):
        if symbol_värde.startswith('jstream_') or symbol_värde.startswith('jnet_') and symbol_värde not in ('jnet_put', 'jnet_get'):
            exportera_tabell[symbol_värde.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exportera_tabell.pop(symbol_värde)
    예제들 = ['public final class bunt { public static void Förbereda() {']
    for sökväg_2 in sorted((åtgärd_rot / '예제').iterdir()):
        if sökväg_2.is_file():
            예제들.append('명령해석기.statisk_fil(%s, %s);' %
                (json.dumps(sökväg_2.name), json.dumps(sökväg_2.read_text(encoding='utf-8'), ensure_ascii=True)))
    (version_väg / 'bunt.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(åtgärd_rot, centrallager_rot, köra_kommando)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(version_väg)) as 작업경로:
        Kurs_väg = Path(작업경로)
        köra_kommando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Kurs_väg, '-sourcepath', Kurs_väg, '-d', Kurs_väg] + sorted((åtgärd_rot / 'källfil').glob('*.java')) + [version_väg / 'bunt.java', version_väg / '예제꾸러미.java'])
        # filnamn·Shell·Fönster 세션·통신과 Java skärmbild 합성 배열을 모두 수용한다.
        argument_MATRIS = ['sh', centrallager_rot / 'compiler/미리번역.sh', '--entry', 'kärna.Kör', '--heap-words', '1048576', '-o', version_väg / 'kernel-java.c']
        for symbol_värde, metod_post in sorted(exportera_tabell.items()):
            argument_MATRIS += ['--export', symbol_värde + '=' + metod_post]
        köra_kommando(argument_MATRIS + sorted(Kurs_väg.glob('*.class')))
    (version_väg / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfiguration_BITS = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = centrallager_rot / 'posix-kor/arm64-native'
    Skapa_användare_Space(åtgärd_rot, centrallager_rot, C_kompilerare, 시플플번역기, länkare_verktyg, Arkiv_verktyg, konfiguration_BITS, köra_kommando)
    nätverk = Skapa_nätverk(åtgärd_rot, C_kompilerare, Arkiv_verktyg, konfiguration_BITS, köra_kommando)
    fjärr_använda = Skapa_fjärr(åtgärd_rot, C_kompilerare, Arkiv_verktyg, konfiguration_BITS, köra_kommando)
    포함인수 = ['-I', 포직스경로 / 'deklarationer', '-I', version_väg]
    빌드작업 = [(C_kompilerare, [], version_väg / 'terminal-font.S', 'font.o'),
            (C_kompilerare, ['-std=c11', '-Wall', '-Wextra', '-Werror'], åtgärd_rot / 'dator/kommandotolk.c', 'terminal.o'),
            (C_kompilerare, ['-std=c11', '-Wall', '-Wextra', '-Werror'], åtgärd_rot / 'dator/skärmelement.c', 'widgets.o'),
            (C_kompilerare, ['-std=c11'], version_väg / 'kernel-java.c', 'java.o'),
            (C_kompilerare, ['-std=c11', '-Wall', '-Wextra', '-Werror'], åtgärd_rot / 'dator/Tavla.c', 'board.o'),
            (C_kompilerare, ['-std=c11', '-Wall', '-Wextra', '-Werror'], åtgärd_rot / 'dator/skärmbild_ritning.c', 'drawing.o'),
            (C_kompilerare, ['-std=c11', '-Wall', '-Wextra', '-Werror'], åtgärd_rot / 'dator/användarutrymme.c', 'user.o'),
            (C_kompilerare, [], åtgärd_rot / 'maskinstart/startpunkt_värde.S', 'entry.o'),
            (C_kompilerare, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Anslut.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], åtgärd_rot / 'tester/fil_Samtal.cpp', 'cpp.o')]
    for kompilerare_verktyg, 추가영역, 원본자료, utleverans in 빌드작업:
        원본설정 = [fil_post for fil_post in konfiguration_BITS if fil_post != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfiguration_BITS
        köra_kommando([kompilerare_verktyg] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', version_väg / utleverans])
    köra_kommando([Arkiv_verktyg, 'rcs', version_väg / 'libposix-kor-arm64.a', version_väg / 'posix.o'])
    köra_kommando([länkare_verktyg, '--gc-sections', '-T', åtgärd_rot / 'maskinstart/länkningslayout.ld', '-Map', version_väg / 'kernel.map', '-o', version_väg / 'kernel.elf'] +
        [version_väg / Namn for Namn in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', version_väg / 'libposix-kor-arm64.a', nätverk, fjärr_använda, version_väg / 'remote/libassh.a', version_väg / 'remote/libbearssl.a', '--end-group'])
    köra_kommando([objekt_fil_konverterare, '-O', 'binary', version_väg / 'kernel.elf', version_väg / 'kernel8.img'])
    bunt_manifest = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Svenska.eget', 'korean_exceptions': 20,
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
    for Namn in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        bunt_manifest['sha256'][Namn] = hashlib.sha256((version_väg / Namn).read_bytes()).hexdigest()
    (version_väg / 'build.json').write_text(json.dumps(bunt_manifest, indent=2) + '\n')
    print('완료:', version_väg / 'kernel8.img')


if __name__ == '__main__':
    Kör()
