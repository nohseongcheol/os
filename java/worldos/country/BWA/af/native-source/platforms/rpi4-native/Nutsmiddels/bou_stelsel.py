#!/usr/bin/env python3
"""hou javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from bou_gebruiker_ruimte import Skep_gebruiker_ruimte
from bou_Netwerk import Skep_Netwerk
from 예제빌드 import 예제만들기
from bou_afstands import Skep_afstands

Project_wortel = Path(__file__).resolve().parents[1]
bewaarplek_wortel = Project_wortel.parents[1]
bou_pad = Project_wortel / 'build'


def uitvoer_bevel(argument_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_ARRAY], cwd=str(Project_wortel))


def Loop():
    bou_pad.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objek_lêer_omsetter = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Argief_nutsmiddel = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Nutsmiddels in ('javac', 시언어번역기, 시플플번역기, 연결편집기, objek_lêer_omsetter, Argief_nutsmiddel):
        if not shutil.which(Nutsmiddels):
            raise SystemExit('필요한 bou_stelsel Nutsmiddels 없음: ' + Nutsmiddels)
    font_inligting = json.loads((Project_wortel / 'vendor/terminal-font.json').read_text())
    font_data = (Project_wortel / 'vendor/terminal-font.bin').read_bytes()
    if len(font_data) != 65616 * 32 or hashlib.sha256(font_data).hexdigest() != font_inligting['sha256']:
        raise SystemExit('Terminaal font_VALUE Grootte/SHA256 불일치')
    uitvoer_tabel = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.Afvoer', 'jshell_input': '셸입출력.입력', 'java_task': 'kern.작업', 'jfs_path_start': 'Geheue_Lêers.pad_BEGIN',
               'jfs_path_byte': 'Geheue_Lêers.pad_greep', 'jfs_open': 'Geheue_Lêers.skep',
               'jfs_read': 'Geheue_Lêers.Lees', 'jfs_write': 'Geheue_Lêers.Skryf',
               'jfs_seek': 'Geheue_Lêers.soek_plaas', 'jfs_close': 'Geheue_Lêers.Sluit',
               'jfs_size': 'Geheue_Lêers.Grootte', 'jfs_unlink': 'Geheue_Lêers.vee_uit_inskrywing',
               'jfs_truncate': 'Geheue_Lêers.stel_lengte'}
    uitvoer_tabel.update({'jfs_entry_count': 'Geheue_Lêers.파일한도', 'jfs_entry_length': 'Geheue_Lêers.공개이름길이', 'jfs_entry_byte': 'Geheue_Lêers.공개이름바이트', 'jfs_entry_size': 'Geheue_Lêers.공개파일크기'})
    uitvoer_tabel.update({'jdraw_prepare': '화면합성.Maak_gereed', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.snit',
        'jdraw_clip_value': '화면합성.snit_VALUE', 'jdraw_begin': '화면합성.Loop',
        'jdraw_end': '화면합성.Klaar', 'jdraw_pixel': '화면합성.pieksel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.wyser'})
    uitvoer_tabel.update({'jfs_mkdir': 'Geheue_Lêers.Skep_gids', 'jfs_rmdir': 'Geheue_Lêers.verwyder_gids', 'jfs_kind': 'Geheue_Lêers.항목종류'})
    uitvoer_tabel.update({'jnet_socket': '되돌림망.Skep_inskrywing', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.e_pos',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Sluit'})
    uitvoer_tabel.update({'jstream_create': 'Stream_Netwerk.Skep_inskrywing', 'jstream_bind': 'Stream_Netwerk.묶기', 'jstream_listen': 'Stream_Netwerk.듣기', 'jstream_connect': 'Stream_Netwerk.Koppel', 'jstream_accept': 'Stream_Netwerk.aanvaar_verbinding', 'jstream_read': 'Stream_Netwerk.Lees', 'jstream_write': 'Stream_Netwerk.Skryf', 'jstream_port': 'Stream_Netwerk.창구읽기', 'jstream_peer': 'Stream_Netwerk.상대창구읽기', 'jstream_close': 'Stream_Netwerk.Sluit'})
    for simbool_VALUE in list(uitvoer_tabel):
        if simbool_VALUE.startswith('jstream_') or simbool_VALUE.startswith('jnet_') and simbool_VALUE not in ('jnet_put', 'jnet_get'):
            uitvoer_tabel[simbool_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = uitvoer_tabel.pop(simbool_VALUE)
    예제들 = ['public final class bondel { public static void Maak_gereed() {']
    for Pad in sorted((Project_wortel / '예제').iterdir()):
        if Pad.is_file():
            예제들.append('명령해석기.staties_lêer(%s, %s);' %
                (json.dumps(Pad.name), json.dumps(Pad.read_text(encoding='utf-8'), ensure_ascii=True)))
    (bou_pad / 'bondel.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_wortel, bewaarplek_wortel, uitvoer_bevel)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(bou_pad)) as 작업경로:
        Klas_pad = Path(작업경로)
        uitvoer_bevel(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Klas_pad, '-sourcepath', Klas_pad, '-d', Klas_pad] + sorted((Project_wortel / 'Bron').glob('*.java')) + [bou_pad / 'bondel.java', bou_pad / '예제꾸러미.java'])
        # Lêer·dop·venster 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_ARRAY = ['sh', bewaarplek_wortel / 'compiler/미리번역.sh', '--entry', 'kern.Loop', '--heap-words', '1048576', '-o', bou_pad / 'kernel-java.c']
        for simbool_VALUE, metode_inskrywing in sorted(uitvoer_tabel.items()):
            argument_ARRAY += ['--export', simbool_VALUE + '=' + metode_inskrywing]
        uitvoer_bevel(argument_ARRAY + sorted(Klas_pad.glob('*.class')))
    (bou_pad / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfigurasie_Agtergrond_intelligente_oordragdiens = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = bewaarplek_wortel / 'posix-kor/arm64-native'
    Skep_gebruiker_ruimte(Project_wortel, bewaarplek_wortel, 시언어번역기, 시플플번역기, 연결편집기, Argief_nutsmiddel, konfigurasie_Agtergrond_intelligente_oordragdiens, uitvoer_bevel)
    Netwerk = Skep_Netwerk(Project_wortel, 시언어번역기, Argief_nutsmiddel, konfigurasie_Agtergrond_intelligente_oordragdiens, uitvoer_bevel)
    원격사용 = Skep_afstands(Project_wortel, 시언어번역기, Argief_nutsmiddel, konfigurasie_Agtergrond_intelligente_oordragdiens, uitvoer_bevel)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', bou_pad]
    빌드작업 = [(시언어번역기, [], bou_pad / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_wortel / 'masjien/Terminaal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_wortel / 'masjien/legstuk.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], bou_pad / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_wortel / 'masjien/bord.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_wortel / 'masjien/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_wortel / 'masjien/gebruiker.c', 'user.o'),
            (시언어번역기, [], Project_wortel / '부팅/inskrywing_p_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Koppel.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_wortel / '시험/lêer_Oproepe.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [lêer_inskrywing for lêer_inskrywing in konfigurasie_Agtergrond_intelligente_oordragdiens if lêer_inskrywing != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfigurasie_Agtergrond_intelligente_oordragdiens
        uitvoer_bevel([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', bou_pad / 출력결과])
    uitvoer_bevel([Argief_nutsmiddel, 'rcs', bou_pad / 'libposix-kor-arm64.a', bou_pad / 'posix.o'])
    uitvoer_bevel([연결편집기, '--gc-sections', '-T', Project_wortel / '부팅/Skakel_Uitleg.ld', '-Map', bou_pad / 'kernel.map', '-o', bou_pad / 'kernel.elf'] +
        [bou_pad / Naam for Naam in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', bou_pad / 'libposix-kor-arm64.a', Netwerk, 원격사용, bou_pad / 'remote/libassh.a', bou_pad / 'remote/libbearssl.a', '--end-group'])
    uitvoer_bevel([objek_lêer_omsetter, '-O', 'binary', bou_pad / 'kernel.elf', bou_pad / 'kernel8.img'])
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
    for Naam in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Naam] = hashlib.sha256((bou_pad / Naam).read_bytes()).hexdigest()
    (bou_pad / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', bou_pad / 'kernel8.img')


if __name__ == '__main__':
    Loop()
