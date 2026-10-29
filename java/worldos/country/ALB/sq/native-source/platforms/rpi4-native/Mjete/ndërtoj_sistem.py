#!/usr/bin/env python3
"""pritës javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from ndërtoj_përdorues_HAPËSIRË import Krijo_përdorues_HAPËSIRË
from ndërtoj_rrjet import Krijo_rrjet
from 예제빌드 import 예제만들기
from ndërtoj_në_largësi import Krijo_në_largësi

Project_rrënjë = Path(__file__).resolve().parents[1]
depo_rrënjë = Project_rrënjë.parents[1]
ndërtoj_shteg = Project_rrënjë / 'build'


def zbatoj_komandë(argument_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_ARRAY], cwd=str(Project_rrënjë))


def Ekzekuto():
    ndërtoj_shteg.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objekt_skedar_konvertues = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    arkiv_vegël = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Mjete in ('javac', 시언어번역기, 시플플번역기, 연결편집기, objekt_skedar_konvertues, arkiv_vegël):
        if not shutil.which(Mjete):
            raise SystemExit('필요한 ndërtoj_sistem Mjete 없음: ' + Mjete)
    font_informacion = json.loads((Project_rrënjë / 'vendor/terminal-font.json').read_text())
    font_të_dhëna = (Project_rrënjë / 'vendor/terminal-font.bin').read_bytes()
    if len(font_të_dhëna) != 65616 * 32 or hashlib.sha256(font_të_dhëna).hexdigest() != font_informacion['sha256']:
        raise SystemExit('Terminali font_VALUE Madhësi/SHA256 불일치')
    eksportoj_tabelë = {'jshell_interactive': '셸입출력.teknologjia_e_informacionit_ndërvepruese', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'bërthamë.작업', 'jfs_path_start': 'Memorie_Skedarët.shteg_nis',
               'jfs_path_byte': 'Memorie_Skedarët.shteg_bajt', 'jfs_open': 'Memorie_Skedarët.Hap',
               'jfs_read': 'Memorie_Skedarët.Leximi', 'jfs_write': 'Memorie_Skedarët.Shkrimi',
               'jfs_seek': 'Memorie_Skedarët.kërko_pozicioni', 'jfs_close': 'Memorie_Skedarët.Mbyll',
               'jfs_size': 'Memorie_Skedarët.Madhësi', 'jfs_unlink': 'Memorie_Skedarët.spastroj_futje',
               'jfs_truncate': 'Memorie_Skedarët.bashkësi_gjatësi'}
    eksportoj_tabelë.update({'jfs_entry_count': 'Memorie_Skedarët.파일한도', 'jfs_entry_length': 'Memorie_Skedarët.공개이름길이', 'jfs_entry_byte': 'Memorie_Skedarët.공개이름바이트', 'jfs_entry_size': 'Memorie_Skedarët.공개파일크기'})
    eksportoj_tabelë.update({'jdraw_prepare': '화면합성.Përgatit', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.fragment',
        'jdraw_clip_value': '화면합성.fragment_VALUE', 'jdraw_begin': '화면합성.Ekzekuto',
        'jdraw_end': '화면합성.Përfundo', 'jdraw_pixel': '화면합성.pikëz',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.tregues'})
    eksportoj_tabelë.update({'jfs_mkdir': 'Memorie_Skedarët.Krijo_direktori', 'jfs_rmdir': 'Memorie_Skedarët.heq_direktori', 'jfs_kind': 'Memorie_Skedarët.항목종류'})
    eksportoj_tabelë.update({'jnet_socket': '되돌림망.Krijo_futje', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.dërgoj',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Mbyll'})
    eksportoj_tabelë.update({'jstream_create': 'Stream_rrjet.Krijo_futje', 'jstream_bind': 'Stream_rrjet.묶기', 'jstream_listen': 'Stream_rrjet.듣기', 'jstream_connect': 'Stream_rrjet.Lidhu', 'jstream_accept': 'Stream_rrjet.prano_lidhje', 'jstream_read': 'Stream_rrjet.Leximi', 'jstream_write': 'Stream_rrjet.Shkrimi', 'jstream_port': 'Stream_rrjet.창구읽기', 'jstream_peer': 'Stream_rrjet.상대창구읽기', 'jstream_close': 'Stream_rrjet.Mbyll'})
    for simbol_VALUE in list(eksportoj_tabelë):
        if simbol_VALUE.startswith('jstream_') or simbol_VALUE.startswith('jnet_') and simbol_VALUE not in ('jnet_put', 'jnet_get'):
            eksportoj_tabelë[simbol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = eksportoj_tabelë.pop(simbol_VALUE)
    예제들 = ['public final class grupoj { public static void Përgatit() {']
    for POZICIONI in sorted((Project_rrënjë / '예제').iterdir()):
        if POZICIONI.is_file():
            예제들.append('명령해석기.statik_skedar(%s, %s);' %
                (json.dumps(POZICIONI.name), json.dumps(POZICIONI.read_text(encoding='utf-8'), ensure_ascii=True)))
    (ndërtoj_shteg / 'grupoj.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_rrënjë, depo_rrënjë, zbatoj_komandë)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(ndërtoj_shteg)) as 작업경로:
        klasë_shteg = Path(작업경로)
        zbatoj_komandë(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klasë_shteg, '-sourcepath', klasë_shteg, '-d', klasë_shteg] + sorted((Project_rrënjë / 'BURIMI').glob('*.java')) + [ndërtoj_shteg / 'grupoj.java', ndërtoj_shteg / '예제꾸러미.java'])
        # Kartelë·pasues·Dritare 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_ARRAY = ['sh', depo_rrënjë / 'compiler/미리번역.sh', '--entry', 'bërthamë.Ekzekuto', '--heap-words', '1048576', '-o', ndërtoj_shteg / 'kernel-java.c']
        for simbol_VALUE, metoda_futje in sorted(eksportoj_tabelë.items()):
            argument_ARRAY += ['--export', simbol_VALUE + '=' + metoda_futje]
        zbatoj_komandë(argument_ARRAY + sorted(klasë_shteg.glob('*.class')))
    (ndërtoj_shteg / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = depo_rrënjë / 'posix-kor/arm64-native'
    Krijo_përdorues_HAPËSIRË(Project_rrënjë, depo_rrënjë, 시언어번역기, 시플플번역기, 연결편집기, arkiv_vegël, konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond, zbatoj_komandë)
    rrjet = Krijo_rrjet(Project_rrënjë, 시언어번역기, arkiv_vegël, konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond, zbatoj_komandë)
    원격사용 = Krijo_në_largësi(Project_rrënjë, 시언어번역기, arkiv_vegël, konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond, zbatoj_komandë)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', ndërtoj_shteg]
    빌드작업 = [(시언어번역기, [], ndërtoj_shteg / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rrënjë / 'makinë/Terminali.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rrënjë / 'makinë/widget.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], ndërtoj_shteg / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rrënjë / 'makinë/panel.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rrënjë / 'makinë/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rrënjë / 'makinë/përdorues.c', 'user.o'),
            (시언어번역기, [], Project_rrënjë / '부팅/futje_p_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Lidhu.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_rrënjë / '시험/skedar_Thirrjet.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [skedar_futje for skedar_futje in konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond if skedar_futje != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond
        zbatoj_komandë([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', ndërtoj_shteg / 출력결과])
    zbatoj_komandë([arkiv_vegël, 'rcs', ndërtoj_shteg / 'libposix-kor-arm64.a', ndërtoj_shteg / 'posix.o'])
    zbatoj_komandë([연결편집기, '--gc-sections', '-T', Project_rrënjë / '부팅/lidh_Navigimi.ld', '-Map', ndërtoj_shteg / 'kernel.map', '-o', ndërtoj_shteg / 'kernel.elf'] +
        [ndërtoj_shteg / Emër for Emër in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', ndërtoj_shteg / 'libposix-kor-arm64.a', rrjet, 원격사용, ndërtoj_shteg / 'remote/libassh.a', ndërtoj_shteg / 'remote/libbearssl.a', '--end-group'])
    zbatoj_komandë([objekt_skedar_konvertues, '-O', 'binary', ndërtoj_shteg / 'kernel.elf', ndërtoj_shteg / 'kernel8.img'])
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
    for Emër in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Emër] = hashlib.sha256((ndërtoj_shteg / Emër).read_bytes()).hexdigest()
    (ndërtoj_shteg / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', ndërtoj_shteg / 'kernel8.img')


if __name__ == '__main__':
    Ekzekuto()
