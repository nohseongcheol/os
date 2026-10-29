#!/usr/bin/env python3
"""esasy javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from düz_ulanyjy_ýer import döretmek_ulanyjy_ýer
from düz_Tor_243da480 import döretmek_Tor
from 예제빌드 import 예제만들기
from düz_uzakdan import döretmek_uzakdan

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
düz_ýol = 기준 / 'build'


def ýerine_ýetir_buýruk(argument_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_ARRAY], cwd=str(기준))


def Bitir():
    düz_ýol.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    obýekt_faýl_özgerdiji = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arhiw_gural = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Gurallar in ('javac', 시언어번역기, 시플플번역기, 연결편집기, obýekt_faýl_özgerdiji, Arhiw_gural):
        if not shutil.which(Gurallar):
            raise SystemExit('필요한 düz_ulgam Gurallar 없음: ' + Gurallar)
    şrift_maglumat_c16c0f1c = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    şrift_maglumat = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(şrift_maglumat) != 65616 * 32 or hashlib.sha256(şrift_maglumat).hexdigest() != şrift_maglumat_c16c0f1c['sha256']:
        raise SystemExit('터미널 şrift_baha Ululyk/SHA256 불일치')
    eksport_et_tablisa = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'ýadro.작업', 'jfs_path_start': 'ýat_Faýllar.ýol_başlat',
               'jfs_path_byte': 'ýat_Faýllar.ýol_baýt', 'jfs_open': 'ýat_Faýllar.Aç',
               'jfs_read': 'ýat_Faýllar.Oka', 'jfs_write': 'ýat_Faýllar.Ýaz',
               'jfs_seek': 'ýat_Faýllar.옮기기', 'jfs_close': 'ýat_Faýllar.Ýap',
               'jfs_size': 'ýat_Faýllar.Ululyk', 'jfs_unlink': 'ýat_Faýllar.지우기',
               'jfs_truncate': 'ýat_Faýllar.köplük_dowamlylyk'}
    eksport_et_tablisa.update({'jfs_entry_count': 'ýat_Faýllar.파일한도', 'jfs_entry_length': 'ýat_Faýllar.공개이름길이', 'jfs_entry_byte': 'ýat_Faýllar.공개이름바이트', 'jfs_entry_size': 'ýat_Faýllar.공개파일크기'})
    eksport_et_tablisa.update({'jdraw_prepare': '화면합성.Taýýarla', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klip',
        'jdraw_clip_value': '화면합성.klip_baha', 'jdraw_begin': '화면합성.Bitir',
        'jdraw_end': '화면합성.Tamamla', 'jdraw_pixel': '화면합성.pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.görkeziji'})
    eksport_et_tablisa.update({'jfs_mkdir': 'ýat_Faýllar.döretmek_katalog', 'jfs_rmdir': 'ýat_Faýllar.aýyr_katalog', 'jfs_kind': 'ýat_Faýllar.항목종류'})
    eksport_et_tablisa.update({'jnet_socket': '되돌림망.döretmek_girizmeklik', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.iber',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Ýap'})
    eksport_et_tablisa.update({'jstream_create': 'Stream_Tor.döretmek_girizmeklik', 'jstream_bind': 'Stream_Tor.묶기', 'jstream_listen': 'Stream_Tor.듣기', 'jstream_connect': 'Stream_Tor.Birikme', 'jstream_accept': 'Stream_Tor.kabul_et_birikme', 'jstream_read': 'Stream_Tor.Oka', 'jstream_write': 'Stream_Tor.Ýaz', 'jstream_port': 'Stream_Tor.창구읽기', 'jstream_peer': 'Stream_Tor.상대창구읽기', 'jstream_close': 'Stream_Tor.Ýap'})
    for nyşan_baha in list(eksport_et_tablisa):
        if nyşan_baha.startswith('jstream_') or nyşan_baha.startswith('jnet_') and nyşan_baha not in ('jnet_put', 'jnet_get'):
            eksport_et_tablisa[nyşan_baha.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = eksport_et_tablisa.pop(nyşan_baha)
    예제들 = ['public final class toplum { public static void Taýýarla() {']
    for Ýol in sorted((기준 / '예제').iterdir()):
        if Ýol.is_file():
            예제들.append('명령해석기.statiki_faýl(%s, %s);' %
                (json.dumps(Ýol.name), json.dumps(Ýol.read_text(encoding='utf-8'), ensure_ascii=True)))
    (düz_ýol / 'toplum.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, ýerine_ýetir_buýruk)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(düz_ýol)) as 작업경로:
        klas_ýol = Path(작업경로)
        ýerine_ýetir_buýruk(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klas_ýol, '-sourcepath', klas_ýol, '-d', klas_ýol] + sorted((기준 / 'Çeşme').glob('*.java')) + [düz_ýol / 'toplum.java', düz_ýol / '예제꾸러미.java'])
        # Faýl·gabyjak·penjire 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_ARRAY = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'ýadro.Bitir', '--heap-words', '1048576', '-o', düz_ýol / 'kernel-java.c']
        for nyşan_baha, usul_girizmeklik in sorted(eksport_et_tablisa.items()):
            argument_ARRAY += ['--export', nyşan_baha + '=' + usul_girizmeklik]
        ýerine_ýetir_buýruk(argument_ARRAY + sorted(klas_ýol.glob('*.class')))
    (düz_ýol / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    döretmek_ulanyjy_ýer(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Arhiw_gural, 설정비트, ýerine_ýetir_buýruk)
    Tor = döretmek_Tor(기준, 시언어번역기, Arhiw_gural, 설정비트, ýerine_ýetir_buýruk)
    원격사용 = döretmek_uzakdan(기준, 시언어번역기, Arhiw_gural, 설정비트, ýerine_ýetir_buýruk)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', düz_ýol]
    빌드작업 = [(시언어번역기, [], düz_ýol / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'kompýuter/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'kompýuter/wijet.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], düz_ýol / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'kompýuter/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'kompýuter/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'kompýuter/ulanyjy.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/girizmeklik_utuk_baha.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Birikme.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [faýl_girizmeklik for faýl_girizmeklik in 설정비트 if faýl_girizmeklik != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        ýerine_ýetir_buýruk([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', düz_ýol / 출력결과])
    ýerine_ýetir_buýruk([Arhiw_gural, 'rcs', düz_ýol / 'libposix-kor-arm64.a', düz_ýol / 'posix.o'])
    ýerine_ýetir_buýruk([연결편집기, '--gc-sections', '-T', 기준 / '부팅/Bag_Ýerleşiş.ld', '-Map', düz_ýol / 'kernel.map', '-o', düz_ýol / 'kernel.elf'] +
        [düz_ýol / Ad for Ad in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', düz_ýol / 'libposix-kor-arm64.a', Tor, 원격사용, düz_ýol / 'remote/libassh.a', düz_ýol / 'remote/libbearssl.a', '--end-group'])
    ýerine_ýetir_buýruk([obýekt_faýl_özgerdiji, '-O', 'binary', düz_ýol / 'kernel.elf', düz_ýol / 'kernel8.img'])
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
    for Ad in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Ad] = hashlib.sha256((düz_ýol / Ad).read_bytes()).hexdigest()
    (düz_ýol / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', düz_ýol / 'kernel8.img')


if __name__ == '__main__':
    Bitir()
