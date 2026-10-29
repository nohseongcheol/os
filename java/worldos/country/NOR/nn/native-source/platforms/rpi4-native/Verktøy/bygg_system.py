#!/usr/bin/env python3
"""vert javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from bygg_brukar_område import Opprett_brukar_område
from bygg_Nettverk import Opprett_Nettverk
from 예제빌드 import 예제만들기
from bygg_fjern import Opprett_fjern

spegle_rot = Path(__file__).resolve().parents[1]
저장소 = spegle_rot.parents[1]
bygg_bane = spegle_rot / 'build'


def Utfør_kommando(argument_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_ARRAY], cwd=str(spegle_rot))


def Køyr_2():
    bygg_bane.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objekt_fil_konverteringsprogram = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arkiv_verktøy = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Verktøy in ('javac', 시언어번역기, 시플플번역기, 연결편집기, objekt_fil_konverteringsprogram, Arkiv_verktøy):
        if not shutil.which(Verktøy):
            raise SystemExit('필요한 bygg_system Verktøy 없음: ' + Verktøy)
    skrift_informasjon = json.loads((spegle_rot / 'vendor/terminal-font.json').read_text())
    skrift_data = (spegle_rot / 'vendor/terminal-font.bin').read_bytes()
    if len(skrift_data) != 65616 * 32 or hashlib.sha256(skrift_data).hexdigest() != skrift_informasjon['sha256']:
        raise SystemExit('Terminal skrift_VALUE Storleik/SHA256 불일치')
    eksportere_tabell = {'jshell_interactive': '셸입출력.informasjonsteknologi_interaktiv', 'jshell_output': '셸입출력.Utdata', 'jshell_input': '셸입출력.입력', 'java_task': 'kjerne.작업', 'jfs_path_start': 'Minne_Filer.bane_START',
               'jfs_path_byte': 'Minne_Filer.bane_byte', 'jfs_open': 'Minne_Filer.Opna',
               'jfs_read': 'Minne_Filer.Les', 'jfs_write': 'Minne_Filer.Skriv',
               'jfs_seek': 'Minne_Filer.søk_plassere', 'jfs_close': 'Minne_Filer.Lukk',
               'jfs_size': 'Minne_Filer.Storleik', 'jfs_unlink': 'Minne_Filer.지우기',
               'jfs_truncate': 'Minne_Filer.sett_lengd'}
    eksportere_tabell.update({'jfs_entry_count': 'Minne_Filer.파일한도', 'jfs_entry_length': 'Minne_Filer.공개이름길이', 'jfs_entry_byte': 'Minne_Filer.공개이름바이트', 'jfs_entry_size': 'Minne_Filer.공개파일크기'})
    eksportere_tabell.update({'jdraw_prepare': '화면합성.Klargjer', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klipp',
        'jdraw_clip_value': '화면합성.klipp_VALUE', 'jdraw_begin': '화면합성.Køyr_2',
        'jdraw_end': '화면합성.Ferdig', 'jdraw_pixel': '화면합성.piksel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.peikar'})
    eksportere_tabell.update({'jfs_mkdir': 'Minne_Filer.Opprett_katalog', 'jfs_rmdir': 'Minne_Filer.fjerne_katalog', 'jfs_kind': 'Minne_Filer.항목종류'})
    eksportere_tabell.update({'jnet_socket': '되돌림망.Opprett_oppføring', 'jnet_bind': '되돌림망.BIND_endepunkt',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.sende',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.avsendar_endepunkt', 'jnet_close': '되돌림망.Lukk'})
    eksportere_tabell.update({'jstream_create': 'Stream_Nettverk.Opprett_oppføring', 'jstream_bind': 'Stream_Nettverk.BIND_endepunkt', 'jstream_listen': 'Stream_Nettverk.lytte_endepunkt', 'jstream_connect': 'Stream_Nettverk.Kopla_til', 'jstream_accept': 'Stream_Nettverk.godta_kontakt', 'jstream_read': 'Stream_Nettverk.Les', 'jstream_write': 'Stream_Nettverk.Skriv', 'jstream_port': 'Stream_Nettverk.창구읽기', 'jstream_peer': 'Stream_Nettverk.상대창구읽기', 'jstream_close': 'Stream_Nettverk.Lukk'})
    for symbol_VALUE in list(eksportere_tabell):
        if symbol_VALUE.startswith('jstream_') or symbol_VALUE.startswith('jnet_') and symbol_VALUE not in ('jnet_put', 'jnet_get'):
            eksportere_tabell[symbol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = eksportere_tabell.pop(symbol_VALUE)
    예제들 = ['public final class bunt { public static void Klargjer() {']
    for STIGE in sorted((spegle_rot / '예제').iterdir()):
        if STIGE.is_file():
            예제들.append('명령해석기.statisk_fil(%s, %s);' %
                (json.dumps(STIGE.name), json.dumps(STIGE.read_text(encoding='utf-8'), ensure_ascii=True)))
    (bygg_bane / 'bunt.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(spegle_rot, 저장소, Utfør_kommando)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(bygg_bane)) as 작업경로:
        time_bane = Path(작업경로)
        Utfør_kommando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', time_bane, '-sourcepath', time_bane, '-d', time_bane] + sorted((spegle_rot / 'KJELDE').glob('*.java')) + [bygg_bane / 'bunt.java', bygg_bane / '예제꾸러미.java'])
        # Fil·grensesnitt·vindauge 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_ARRAY = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'kjerne.Køyr_2', '--heap-words', '1048576', '-o', bygg_bane / 'kernel-java.c']
        for symbol_VALUE, metode_oppføring in sorted(eksportere_tabell.items()):
            argument_ARRAY += ['--export', symbol_VALUE + '=' + metode_oppføring]
        Utfør_kommando(argument_ARRAY + sorted(time_bane.glob('*.class')))
    (bygg_bane / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    Opprett_brukar_område(spegle_rot, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Arkiv_verktøy, 설정비트, Utfør_kommando)
    Nettverk = Opprett_Nettverk(spegle_rot, 시언어번역기, Arkiv_verktøy, 설정비트, Utfør_kommando)
    원격사용 = Opprett_fjern(spegle_rot, 시언어번역기, Arkiv_verktøy, 설정비트, Utfør_kommando)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', bygg_bane]
    빌드작업 = [(시언어번역기, [], bygg_bane / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], spegle_rot / 'maskin/Terminal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], spegle_rot / 'maskin/miniprogram.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], bygg_bane / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], spegle_rot / 'maskin/Tavle.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], spegle_rot / 'maskin/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], spegle_rot / 'maskin/brukar.c', 'user.o'),
            (시언어번역기, [], spegle_rot / '부팅/oppføring_p_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Kopla_til.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], spegle_rot / '시험/fil_Samtalar.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [fil_oppføring for fil_oppføring in 설정비트 if fil_oppføring != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        Utfør_kommando([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', bygg_bane / 출력결과])
    Utfør_kommando([Arkiv_verktøy, 'rcs', bygg_bane / 'libposix-kor-arm64.a', bygg_bane / 'posix.o'])
    Utfør_kommando([연결편집기, '--gc-sections', '-T', spegle_rot / '부팅/kople_Oppsett.ld', '-Map', bygg_bane / 'kernel.map', '-o', bygg_bane / 'kernel.elf'] +
        [bygg_bane / Namn for Namn in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', bygg_bane / 'libposix-kor-arm64.a', Nettverk, 원격사용, bygg_bane / 'remote/libassh.a', bygg_bane / 'remote/libbearssl.a', '--end-group'])
    Utfør_kommando([objekt_fil_konverteringsprogram, '-O', 'binary', bygg_bane / 'kernel.elf', bygg_bane / 'kernel8.img'])
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
    for Namn in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Namn] = hashlib.sha256((bygg_bane / Namn).read_bytes()).hexdigest()
    (bygg_bane / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', bygg_bane / 'kernel8.img')


if __name__ == '__main__':
    Køyr_2()
