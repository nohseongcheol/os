#!/usr/bin/env python3
"""lletya javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from llunio_defnyddiwr_lle import Creu_defnyddiwr_lle
from llunio_Rhwydwaith import Creu_Rhwydwaith
from 예제빌드 import 예제만들기
from llunio_pell import Creu_pell

prosiect_gwraidd = Path(__file__).resolve().parents[1]
저장소 = prosiect_gwraidd.parents[1]
llunio_llwybr = prosiect_gwraidd / 'build'


def Gweithredu_gorchymyn(arg_ARAE):
    subprocess.check_call([str(첫째값) for 첫째값 in arg_ARAE], cwd=str(prosiect_gwraidd))


def Gweithredu_2():
    llunio_llwybr.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    gwrthrych_ffeil_trawsnewidydd = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Archif_offeryn = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Offer in ('javac', 시언어번역기, 시플플번역기, 연결편집기, gwrthrych_ffeil_trawsnewidydd, Archif_offeryn):
        if not shutil.which(Offer):
            raise SystemExit('필요한 llunio_system Offer 없음: ' + Offer)
    ffont_gwybodaeth = json.loads((prosiect_gwraidd / 'vendor/terminal-font.json').read_text())
    ffont_data = (prosiect_gwraidd / 'vendor/terminal-font.bin').read_bytes()
    if len(ffont_data) != 65616 * 32 or hashlib.sha256(ffont_data).hexdigest() != ffont_gwybodaeth['sha256']:
        raise SystemExit('Terfynell ffont_VALUE Maint/SHA256 불일치')
    allgludo_tabl = {'jshell_interactive': '셸입출력.technoleg_gwybodaeth_rhyngweithiol', 'jshell_output': '셸입출력.Allbwn', 'jshell_input': '셸입출력.입력', 'java_task': 'cnewyllyn.작업', 'jfs_path_start': 'Cof_Ffeil.llwybr_START',
               'jfs_path_byte': 'Cof_Ffeil.llwybr_beit', 'jfs_open': 'Cof_Ffeil.Agor',
               'jfs_read': 'Cof_Ffeil.Darllen', 'jfs_write': 'Cof_Ffeil.Ysgrifennu',
               'jfs_seek': 'Cof_Ffeil.chwilio_safle', 'jfs_close': 'Cof_Ffeil.Cau',
               'jfs_size': 'Cof_Ffeil.Maint', 'jfs_unlink': 'Cof_Ffeil.지우기',
               'jfs_truncate': 'Cof_Ffeil.set_hyd'}
    allgludo_tabl.update({'jfs_entry_count': 'Cof_Ffeil.파일한도', 'jfs_entry_length': 'Cof_Ffeil.공개이름길이', 'jfs_entry_byte': 'Cof_Ffeil.공개이름바이트', 'jfs_entry_size': 'Cof_Ffeil.공개파일크기'})
    allgludo_tabl.update({'jdraw_prepare': '화면합성.Paratoi', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.clip',
        'jdraw_clip_value': '화면합성.clip_VALUE', 'jdraw_begin': '화면합성.Gweithredu_2',
        'jdraw_end': '화면합성.Gorffen', 'jdraw_pixel': '화면합성.pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.pwyntydd'})
    allgludo_tabl.update({'jfs_mkdir': 'Cof_Ffeil.Creu_cyfeiriadur', 'jfs_rmdir': 'Cof_Ffeil.tynnu_cyfeiriadur', 'jfs_kind': 'Cof_Ffeil.항목종류'})
    allgludo_tabl.update({'jnet_socket': '되돌림망.Creu_cofnod', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.anfon',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Cau'})
    allgludo_tabl.update({'jstream_create': 'ffrwd_Rhwydwaith.Creu_cofnod', 'jstream_bind': 'ffrwd_Rhwydwaith.묶기', 'jstream_listen': 'ffrwd_Rhwydwaith.듣기', 'jstream_connect': 'ffrwd_Rhwydwaith.Cysylltu', 'jstream_accept': 'ffrwd_Rhwydwaith.derbyn_cyswllt', 'jstream_read': 'ffrwd_Rhwydwaith.Darllen', 'jstream_write': 'ffrwd_Rhwydwaith.Ysgrifennu', 'jstream_port': 'ffrwd_Rhwydwaith.창구읽기', 'jstream_peer': 'ffrwd_Rhwydwaith.상대창구읽기', 'jstream_close': 'ffrwd_Rhwydwaith.Cau'})
    for symbol_VALUE in list(allgludo_tabl):
        if symbol_VALUE.startswith('jstream_') or symbol_VALUE.startswith('jnet_') and symbol_VALUE not in ('jnet_put', 'jnet_get'):
            allgludo_tabl[symbol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = allgludo_tabl.pop(symbol_VALUE)
    예제들 = ['public final class bwndel { public static void Paratoi() {']
    for LLWYBR in sorted((prosiect_gwraidd / '예제').iterdir()):
        if LLWYBR.is_file():
            예제들.append('명령해석기.statig_ffeil(%s, %s);' %
                (json.dumps(LLWYBR.name), json.dumps(LLWYBR.read_text(encoding='utf-8'), ensure_ascii=True)))
    (llunio_llwybr / 'bwndel.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(prosiect_gwraidd, 저장소, Gweithredu_gorchymyn)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(llunio_llwybr)) as 작업경로:
        Dosbarth_llwybr = Path(작업경로)
        Gweithredu_gorchymyn(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Dosbarth_llwybr, '-sourcepath', Dosbarth_llwybr, '-d', Dosbarth_llwybr] + sorted((prosiect_gwraidd / 'FFYNHONNELL').glob('*.java')) + [llunio_llwybr / 'bwndel.java', llunio_llwybr / '예제꾸러미.java'])
        # Ffeil·cragen·ffenestr 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        arg_ARAE = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'cnewyllyn.Gweithredu_2', '--heap-words', '1048576', '-o', llunio_llwybr / 'kernel-java.c']
        for symbol_VALUE, dull_cofnod in sorted(allgludo_tabl.items()):
            arg_ARAE += ['--export', symbol_VALUE + '=' + dull_cofnod]
        Gweithredu_gorchymyn(arg_ARAE + sorted(Dosbarth_llwybr.glob('*.class')))
    (llunio_llwybr / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    Creu_defnyddiwr_lle(prosiect_gwraidd, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Archif_offeryn, 설정비트, Gweithredu_gorchymyn)
    Rhwydwaith = Creu_Rhwydwaith(prosiect_gwraidd, 시언어번역기, Archif_offeryn, 설정비트, Gweithredu_gorchymyn)
    원격사용 = Creu_pell(prosiect_gwraidd, 시언어번역기, Archif_offeryn, 설정비트, Gweithredu_gorchymyn)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', llunio_llwybr]
    빌드작업 = [(시언어번역기, [], llunio_llwybr / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], prosiect_gwraidd / 'peiriant/Terfynell.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], prosiect_gwraidd / 'peiriant/teclyn.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], llunio_llwybr / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], prosiect_gwraidd / 'peiriant/bwrdd.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], prosiect_gwraidd / 'peiriant/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], prosiect_gwraidd / 'peiriant/defnyddiwr.c', 'user.o'),
            (시언어번역기, [], prosiect_gwraidd / '부팅/cofnod_p_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Cysylltu.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], prosiect_gwraidd / '시험/ffeil_Galwadau.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ffeil_cofnod for ffeil_cofnod in 설정비트 if ffeil_cofnod != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        Gweithredu_gorchymyn([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', llunio_llwybr / 출력결과])
    Gweithredu_gorchymyn([Archif_offeryn, 'rcs', llunio_llwybr / 'libposix-kor-arm64.a', llunio_llwybr / 'posix.o'])
    Gweithredu_gorchymyn([연결편집기, '--gc-sections', '-T', prosiect_gwraidd / '부팅/Dolen_Llywio.ld', '-Map', llunio_llwybr / 'kernel.map', '-o', llunio_llwybr / 'kernel.elf'] +
        [llunio_llwybr / Enw for Enw in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', llunio_llwybr / 'libposix-kor-arm64.a', Rhwydwaith, 원격사용, llunio_llwybr / 'remote/libassh.a', llunio_llwybr / 'remote/libbearssl.a', '--end-group'])
    Gweithredu_gorchymyn([gwrthrych_ffeil_trawsnewidydd, '-O', 'binary', llunio_llwybr / 'kernel.elf', llunio_llwybr / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Cymraeg.자체', 'korean_exceptions': 20,
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
    for Enw in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Enw] = hashlib.sha256((llunio_llwybr / Enw).read_bytes()).hexdigest()
    (llunio_llwybr / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', llunio_llwybr / 'kernel8.img')


if __name__ == '__main__':
    Gweithredu_2()
