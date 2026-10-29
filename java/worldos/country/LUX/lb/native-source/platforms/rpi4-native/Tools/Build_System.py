#!/usr/bin/env python3
"""Host javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from Build_Benotzer_Plaz import Create_Benotzer_Plaz
from Build_Reseau import Create_Reseau
from 예제빌드 import 예제만들기
from Build_extern import Create_extern

projezéieren_Racinn = Path(__file__).resolve().parents[1]
저장소 = projezéieren_Racinn.parents[1]
Build_Wee = projezéieren_Racinn / 'build'


def ausféieren_Befeel(Argument_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in Argument_ARRAY], cwd=str(projezéieren_Racinn))


def Laf():
    Build_Wee.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Objet_Fichier_Konverter = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Archiv_Tool = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Tools in ('javac', 시언어번역기, 시플플번역기, 연결편집기, Objet_Fichier_Konverter, Archiv_Tool):
        if not shutil.which(Tools):
            raise SystemExit('필요한 Build_System Tools 없음: ' + Tools)
    Schrëftaart_Info = json.loads((projezéieren_Racinn / 'vendor/terminal-font.json').read_text())
    Schrëftaart_Daten = (projezéieren_Racinn / 'vendor/terminal-font.bin').read_bytes()
    if len(Schrëftaart_Daten) != 65616 * 32 or hashlib.sha256(Schrëftaart_Daten).hexdigest() != Schrëftaart_Info['sha256']:
        raise SystemExit('Terminal Schrëftaart_VALUE d_Gréisst_veränneren/SHA256 불일치')
    exportéieren_Tabell = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'Kernel.작업', 'jfs_path_start': 'Späicher_Fichieren.Wee_Start',
               'jfs_path_byte': 'Späicher_Fichieren.Wee_Byte', 'jfs_open': 'Späicher_Fichieren.ariichten',
               'jfs_read': 'Späicher_Fichieren.읽기', 'jfs_write': 'Späicher_Fichieren.schreiwen',
               'jfs_seek': 'Späicher_Fichieren.sichen_positionéieren', 'jfs_close': 'Späicher_Fichieren.Clôture',
               'jfs_size': 'Späicher_Fichieren.d_Gréisst_veränneren', 'jfs_unlink': 'Späicher_Fichieren.지우기',
               'jfs_truncate': 'Späicher_Fichieren.Saz_Längt'}
    exportéieren_Tabell.update({'jfs_entry_count': 'Späicher_Fichieren.파일한도', 'jfs_entry_length': 'Späicher_Fichieren.공개이름길이', 'jfs_entry_byte': 'Späicher_Fichieren.공개이름바이트', 'jfs_entry_size': 'Späicher_Fichieren.공개파일크기'})
    exportéieren_Tabell.update({'jdraw_prepare': '화면합성.Préparéieren', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.Clip',
        'jdraw_clip_value': '화면합성.Clip_VALUE', 'jdraw_begin': '화면합성.Laf',
        'jdraw_end': '화면합성.Ofschléissen', 'jdraw_pixel': '화면합성.Pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.Uweiser'})
    exportéieren_Tabell.update({'jfs_mkdir': 'Späicher_Fichieren.Create_Verzeechnes', 'jfs_rmdir': 'Späicher_Fichieren.ewechhuelen_Verzeechnes', 'jfs_kind': 'Späicher_Fichieren.항목종류'})
    exportéieren_Tabell.update({'jnet_socket': '되돌림망.Create_Agab', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.mailen',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Clôture'})
    exportéieren_Tabell.update({'jstream_create': 'Stream_Reseau.Create_Agab', 'jstream_bind': 'Stream_Reseau.묶기', 'jstream_listen': 'Stream_Reseau.듣기', 'jstream_connect': 'Stream_Reseau.Verbannen', 'jstream_accept': 'Stream_Reseau.acceptéieren_Verbindung', 'jstream_read': 'Stream_Reseau.읽기', 'jstream_write': 'Stream_Reseau.schreiwen', 'jstream_port': 'Stream_Reseau.창구읽기', 'jstream_peer': 'Stream_Reseau.상대창구읽기', 'jstream_close': 'Stream_Reseau.Clôture'})
    for Symbol_VALUE in list(exportéieren_Tabell):
        if Symbol_VALUE.startswith('jstream_') or Symbol_VALUE.startswith('jnet_') and Symbol_VALUE not in ('jnet_put', 'jnet_get'):
            exportéieren_Tabell[Symbol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exportéieren_Tabell.pop(Symbol_VALUE)
    예제들 = ['public final class Bëndel { public static void Préparéieren() {']
    for Wee in sorted((projezéieren_Racinn / '예제').iterdir()):
        if Wee.is_file():
            예제들.append('명령해석기.statesch_Fichier(%s, %s);' %
                (json.dumps(Wee.name), json.dumps(Wee.read_text(encoding='utf-8'), ensure_ascii=True)))
    (Build_Wee / 'Bëndel.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(projezéieren_Racinn, 저장소, ausféieren_Befeel)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(Build_Wee)) as 작업경로:
        Klass_Wee = Path(작업경로)
        ausféieren_Befeel(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Klass_Wee, '-sourcepath', Klass_Wee, '-d', Klass_Wee] + sorted((projezéieren_Racinn / 'Quell').glob('*.java')) + [Build_Wee / 'Bëndel.java', Build_Wee / '예제꾸러미.java'])
        # Fichier·Shell·Fënster 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        Argument_ARRAY = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'Kernel.Laf', '--heap-words', '1048576', '-o', Build_Wee / 'kernel-java.c']
        for Symbol_VALUE, Method_Agab in sorted(exportéieren_Tabell.items()):
            Argument_ARRAY += ['--export', Symbol_VALUE + '=' + Method_Agab]
        ausféieren_Befeel(Argument_ARRAY + sorted(Klass_Wee.glob('*.class')))
    (Build_Wee / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    Create_Benotzer_Plaz(projezéieren_Racinn, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Archiv_Tool, 설정비트, ausféieren_Befeel)
    Reseau = Create_Reseau(projezéieren_Racinn, 시언어번역기, Archiv_Tool, 설정비트, ausféieren_Befeel)
    원격사용 = Create_extern(projezéieren_Racinn, 시언어번역기, Archiv_Tool, 설정비트, ausféieren_Befeel)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', Build_Wee]
    빌드작업 = [(시언어번역기, [], Build_Wee / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projezéieren_Racinn / 'Computer/Terminal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projezéieren_Racinn / 'Computer/Widget.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], Build_Wee / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projezéieren_Racinn / 'Computer/Board.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projezéieren_Racinn / 'Computer/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projezéieren_Racinn / 'Computer/Benotzer.c', 'user.o'),
            (시언어번역기, [], projezéieren_Racinn / '부팅/Agab_Punkt_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Verbannen.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], projezéieren_Racinn / '시험/Fichier_Uriff.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [Fichier_Agab for Fichier_Agab in 설정비트 if Fichier_Agab != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        ausféieren_Befeel([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', Build_Wee / 출력결과])
    ausféieren_Befeel([Archiv_Tool, 'rcs', Build_Wee / 'libposix-kor-arm64.a', Build_Wee / 'posix.o'])
    ausféieren_Befeel([연결편집기, '--gc-sections', '-T', projezéieren_Racinn / '부팅/Link_Layout.ld', '-Map', Build_Wee / 'kernel.map', '-o', Build_Wee / 'kernel.elf'] +
        [Build_Wee / Numm for Numm in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', Build_Wee / 'libposix-kor-arm64.a', Reseau, 원격사용, Build_Wee / 'remote/libassh.a', Build_Wee / 'remote/libbearssl.a', '--end-group'])
    ausféieren_Befeel([Objet_Fichier_Konverter, '-O', 'binary', Build_Wee / 'kernel.elf', Build_Wee / 'kernel8.img'])
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
    for Numm in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Numm] = hashlib.sha256((Build_Wee / Numm).read_bytes()).hexdigest()
    (Build_Wee / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', Build_Wee / 'kernel8.img')


if __name__ == '__main__':
    Laf()
