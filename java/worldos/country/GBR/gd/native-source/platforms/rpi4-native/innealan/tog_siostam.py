#!/usr/bin/env python3
"""òstair javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from tog_cleachdaiche_spàs import Create_cleachdaiche_spàs
from tog_lìonra import Create_lìonra
from 예제빌드 import 예제만들기
from tog_cian import Create_cian

tilg_freumh = Path(__file__).resolve().parents[1]
저장소 = tilg_freumh.parents[1]
tog_slighe = tilg_freumh / 'build'


def gnìomhaich_àithne(argamaid_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argamaid_ARRAY], cwd=str(tilg_freumh))


def ruith():
    tog_slighe.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    nì_faidhle_iompaichear = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    taisg_inneal = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for innealan in ('javac', 시언어번역기, 시플플번역기, 연결편집기, nì_faidhle_iompaichear, taisg_inneal):
        if not shutil.which(innealan):
            raise SystemExit('필요한 tog_siostam innealan 없음: ' + innealan)
    cruth_clò_fios = json.loads((tilg_freumh / 'vendor/terminal-font.json').read_text())
    cruth_clò_dàta = (tilg_freumh / 'vendor/terminal-font.bin').read_bytes()
    if len(cruth_clò_dàta) != 65616 * 32 or hashlib.sha256(cruth_clò_dàta).hexdigest() != cruth_clò_fios['sha256']:
        raise SystemExit('tèirmineal cruth_clò_VALUE atharraich_am_meud/SHA256 불일치')
    às_phortaich_clàr = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'eitean.작업', 'jfs_path_start': 'cuimhne_faidhlichean.slighe_Start',
               'jfs_path_byte': 'cuimhne_faidhlichean.slighe_baidht', 'jfs_open': 'cuimhne_faidhlichean.fosgail',
               'jfs_read': 'cuimhne_faidhlichean.읽기', 'jfs_write': 'cuimhne_faidhlichean.sgrìobh',
               'jfs_seek': 'cuimhne_faidhlichean.sir_suidhich', 'jfs_close': 'cuimhne_faidhlichean.dùin',
               'jfs_size': 'cuimhne_faidhlichean.atharraich_am_meud', 'jfs_unlink': 'cuimhne_faidhlichean.지우기',
               'jfs_truncate': 'cuimhne_faidhlichean.seata_faid'}
    às_phortaich_clàr.update({'jfs_entry_count': 'cuimhne_faidhlichean.파일한도', 'jfs_entry_length': 'cuimhne_faidhlichean.공개이름길이', 'jfs_entry_byte': 'cuimhne_faidhlichean.공개이름바이트', 'jfs_entry_size': 'cuimhne_faidhlichean.공개파일크기'})
    às_phortaich_clàr.update({'jdraw_prepare': '화면합성.Ullaich', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.cliop',
        'jdraw_clip_value': '화면합성.cliop_VALUE', 'jdraw_begin': '화면합성.ruith',
        'jdraw_end': '화면합성.Coilean', 'jdraw_pixel': '화면합성.pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.tomhaire'})
    às_phortaich_clàr.update({'jfs_mkdir': 'cuimhne_faidhlichean.Create_eòlaire', 'jfs_rmdir': 'cuimhne_faidhlichean.thoir_air_falbh_eòlaire', 'jfs_kind': 'cuimhne_faidhlichean.항목종류'})
    às_phortaich_clàr.update({'jnet_socket': '되돌림망.Create_cur_a_steach', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.cuir',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.dùin'})
    às_phortaich_clàr.update({'jstream_create': 'sruth_lìonra.Create_cur_a_steach', 'jstream_bind': 'sruth_lìonra.묶기', 'jstream_listen': 'sruth_lìonra.듣기', 'jstream_connect': 'sruth_lìonra.CONNECT', 'jstream_accept': 'sruth_lìonra.gabh_ris_ceangal', 'jstream_read': 'sruth_lìonra.읽기', 'jstream_write': 'sruth_lìonra.sgrìobh', 'jstream_port': 'sruth_lìonra.창구읽기', 'jstream_peer': 'sruth_lìonra.상대창구읽기', 'jstream_close': 'sruth_lìonra.dùin'})
    for samhla_VALUE in list(às_phortaich_clàr):
        if samhla_VALUE.startswith('jstream_') or samhla_VALUE.startswith('jnet_') and samhla_VALUE not in ('jnet_put', 'jnet_get'):
            às_phortaich_clàr[samhla_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = às_phortaich_clàr.pop(samhla_VALUE)
    예제들 = ['public final class trusgan { public static void Ullaich() {']
    for Slighe in sorted((tilg_freumh / '예제').iterdir()):
        if Slighe.is_file():
            예제들.append('명령해석기.stadaigeach_faidhle(%s, %s);' %
                (json.dumps(Slighe.name), json.dumps(Slighe.read_text(encoding='utf-8'), ensure_ascii=True)))
    (tog_slighe / 'trusgan.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(tilg_freumh, 저장소, gnìomhaich_àithne)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(tog_slighe)) as 작업경로:
        clas_slighe = Path(작업경로)
        gnìomhaich_àithne(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', clas_slighe, '-sourcepath', clas_slighe, '-d', clas_slighe] + sorted((tilg_freumh / 'tùs').glob('*.java')) + [tog_slighe / 'trusgan.java', tog_slighe / '예제꾸러미.java'])
        # faidhle·slige·uinneag 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argamaid_ARRAY = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'eitean.ruith', '--heap-words', '1048576', '-o', tog_slighe / 'kernel-java.c']
        for samhla_VALUE, dòigh_cur_a_steach in sorted(às_phortaich_clàr.items()):
            argamaid_ARRAY += ['--export', samhla_VALUE + '=' + dòigh_cur_a_steach]
        gnìomhaich_àithne(argamaid_ARRAY + sorted(clas_slighe.glob('*.class')))
    (tog_slighe / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    Create_cleachdaiche_spàs(tilg_freumh, 저장소, 시언어번역기, 시플플번역기, 연결편집기, taisg_inneal, 설정비트, gnìomhaich_àithne)
    lìonra = Create_lìonra(tilg_freumh, 시언어번역기, taisg_inneal, 설정비트, gnìomhaich_àithne)
    원격사용 = Create_cian(tilg_freumh, 시언어번역기, taisg_inneal, 설정비트, gnìomhaich_àithne)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', tog_slighe]
    빌드작업 = [(시언어번역기, [], tog_slighe / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], tilg_freumh / 'inneal/tèirmineal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], tilg_freumh / 'inneal/widget.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], tog_slighe / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], tilg_freumh / 'inneal/bòrd.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], tilg_freumh / 'inneal/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], tilg_freumh / 'inneal/cleachdaiche.c', 'user.o'),
            (시언어번역기, [], tilg_freumh / '부팅/cur_a_steach_puing_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'CONNECT.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], tilg_freumh / '시험/faidhle_gairmean.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [faidhle_cur_a_steach for faidhle_cur_a_steach in 설정비트 if faidhle_cur_a_steach != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        gnìomhaich_àithne([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', tog_slighe / 출력결과])
    gnìomhaich_àithne([taisg_inneal, 'rcs', tog_slighe / 'libposix-kor-arm64.a', tog_slighe / 'posix.o'])
    gnìomhaich_àithne([연결편집기, '--gc-sections', '-T', tilg_freumh / '부팅/ceangal_co_dhealbhachd.ld', '-Map', tog_slighe / 'kernel.map', '-o', tog_slighe / 'kernel.elf'] +
        [tog_slighe / Ainm for Ainm in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', tog_slighe / 'libposix-kor-arm64.a', lìonra, 원격사용, tog_slighe / 'remote/libassh.a', tog_slighe / 'remote/libbearssl.a', '--end-group'])
    gnìomhaich_àithne([nì_faidhle_iompaichear, '-O', 'binary', tog_slighe / 'kernel.elf', tog_slighe / 'kernel8.img'])
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
    for Ainm in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Ainm] = hashlib.sha256((tog_slighe / Ainm).read_bytes()).hexdigest()
    (tog_slighe / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', tog_slighe / 'kernel8.img')


if __name__ == '__main__':
    ruith()
