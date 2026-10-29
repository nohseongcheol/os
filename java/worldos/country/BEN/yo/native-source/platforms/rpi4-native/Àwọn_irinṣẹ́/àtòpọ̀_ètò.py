#!/usr/bin/env python3
"""olùpèsè javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from àtòpọ̀_aṣàmúlò_àlàfo import Ṣẹ̀dá_aṣàmúlò_àlàfo
from àtòpọ̀_Alásopọ̀ import Ṣẹ̀dá_Alásopọ̀
from 예제빌드 import 예제만들기
from àtòpọ̀_Ìjìnnà import Ṣẹ̀dá_Ìjìnnà

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
àtòpọ̀_ọ̀nà = 기준 / 'build'


def ṣiṣẹ́_àṣẹ(ágúmẹ́ntì_ÀRÉÈ):
    subprocess.check_call([str(첫째값) for 첫째값 in ágúmẹ́ntì_ÀRÉÈ], cwd=str(기준))


def Rọ́ọ̀nù():
    àtòpọ̀_ọ̀nà.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    nǹkan_fáìlì_àyí_ohun_padà = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Àwọn_irinṣẹ́ in ('javac', 시언어번역기, 시플플번역기, 연결편집기, nǹkan_fáìlì_àyí_ohun_padà, Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́):
        if not shutil.which(Àwọn_irinṣẹ́):
            raise SystemExit('필요한 àtòpọ̀_ètò Àwọn_irinṣẹ́ 없음: ' + Àwọn_irinṣẹ́)
    ìrísí_lẹ́tà_Ìwífún = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    ìrísí_lẹ́tà_détà = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(ìrísí_lẹ́tà_détà) != 65616 * 32 or hashlib.sha256(ìrísí_lẹ́tà_détà).hexdigest() != ìrísí_lẹ́tà_Ìwífún['sha256']:
        raise SystemExit('터미널 ìrísí_lẹ́tà_iye Ìwọ̀n/SHA256 불일치')
    ṣàgbéjáde_atọ́ka = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'kánẹ́ẹ̀lì.작업', 'jfs_path_start': 'ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_bẹ̀rẹ̀',
               'jfs_path_byte': 'ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì', 'jfs_open': 'ibi_ìpamọ́_Àwọn_fáìlì.Ṣi',
               'jfs_read': 'ibi_ìpamọ́_Àwọn_fáìlì.Kàá', 'jfs_write': 'ibi_ìpamọ́_Àwọn_fáìlì.Kọ',
               'jfs_seek': 'ibi_ìpamọ́_Àwọn_fáìlì.옮기기', 'jfs_close': 'ibi_ìpamọ́_Àwọn_fáìlì.Ti',
               'jfs_size': 'ibi_ìpamọ́_Àwọn_fáìlì.Ìwọ̀n', 'jfs_unlink': 'ibi_ìpamọ́_Àwọn_fáìlì.지우기',
               'jfs_truncate': 'ibi_ìpamọ́_Àwọn_fáìlì.ọ̀wọ̀_gígùn'}
    ṣàgbéjáde_atọ́ka.update({'jfs_entry_count': 'ibi_ìpamọ́_Àwọn_fáìlì.파일한도', 'jfs_entry_length': 'ibi_ìpamọ́_Àwọn_fáìlì.공개이름길이', 'jfs_entry_byte': 'ibi_ìpamọ́_Àwọn_fáìlì.공개이름바이트', 'jfs_entry_size': 'ibi_ìpamọ́_Àwọn_fáìlì.공개파일크기'})
    ṣàgbéjáde_atọ́ka.update({'jdraw_prepare': '화면합성.gbaradì', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ní_ṣókí',
        'jdraw_clip_value': '화면합성.ní_ṣókí_iye', 'jdraw_begin': '화면합성.Rọ́ọ̀nù',
        'jdraw_end': '화면합성.Parí', 'jdraw_pixel': '화면합성.píkísẹ̀',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.ìtọ́ka'})
    ṣàgbéjáde_atọ́ka.update({'jfs_mkdir': 'ibi_ìpamọ́_Àwọn_fáìlì.Ṣẹ̀dá_àkójọpọ̀_fáìlì', 'jfs_rmdir': 'ibi_ìpamọ́_Àwọn_fáìlì.ṣèmúkúro_àkójọpọ̀_fáìlì', 'jfs_kind': 'ibi_ìpamọ́_Àwọn_fáìlì.항목종류'})
    ṣàgbéjáde_atọ́ka.update({'jnet_socket': '되돌림망.Ṣẹ̀dá_ìgbéwọlé', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.í_meèlì',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Ti'})
    ṣàgbéjáde_atọ́ka.update({'jstream_create': 'Stream_Alásopọ̀.Ṣẹ̀dá_ìgbéwọlé', 'jstream_bind': 'Stream_Alásopọ̀.묶기', 'jstream_listen': 'Stream_Alásopọ̀.듣기', 'jstream_connect': 'Stream_Alásopọ̀.Darapọ̀', 'jstream_accept': 'Stream_Alásopọ̀.gbà_Ìsomọ́', 'jstream_read': 'Stream_Alásopọ̀.Kàá', 'jstream_write': 'Stream_Alásopọ̀.Kọ', 'jstream_port': 'Stream_Alásopọ̀.창구읽기', 'jstream_peer': 'Stream_Alásopọ̀.상대창구읽기', 'jstream_close': 'Stream_Alásopọ̀.Ti'})
    for àmì_iye in list(ṣàgbéjáde_atọ́ka):
        if àmì_iye.startswith('jstream_') or àmì_iye.startswith('jnet_') and àmì_iye not in ('jnet_put', 'jnet_get'):
            ṣàgbéjáde_atọ́ka[àmì_iye.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ṣàgbéjáde_atọ́ka.pop(àmì_iye)
    예제들 = ['public final class àkópọ̀ { public static void gbaradì() {']
    for ọ̀nà in sorted((기준 / '예제').iterdir()):
        if ọ̀nà.is_file():
            예제들.append('명령해석기.ìdágún_fáìlì(%s, %s);' %
                (json.dumps(ọ̀nà.name), json.dumps(ọ̀nà.read_text(encoding='utf-8'), ensure_ascii=True)))
    (àtòpọ̀_ọ̀nà / 'àkópọ̀.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, ṣiṣẹ́_àṣẹ)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(àtòpọ̀_ọ̀nà)) as 작업경로:
        ọ̀wọ́_ọ̀nà = Path(작업경로)
        ṣiṣẹ́_àṣẹ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ọ̀wọ́_ọ̀nà, '-sourcepath', ọ̀wọ́_ọ̀nà, '-d', ọ̀wọ́_ọ̀nà] + sorted((기준 / 'orísun').glob('*.java')) + [àtòpọ̀_ọ̀nà / 'àkópọ̀.java', àtòpọ̀_ọ̀nà / '예제꾸러미.java'])
        # Fáìlì·ṣẹ́ẹ̀lì·wínńdò 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ágúmẹ́ntì_ÀRÉÈ = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'kánẹ́ẹ̀lì.Rọ́ọ̀nù', '--heap-words', '1048576', '-o', àtòpọ̀_ọ̀nà / 'kernel-java.c']
        for àmì_iye, ìlànà_ìgbéwọlé in sorted(ṣàgbéjáde_atọ́ka.items()):
            ágúmẹ́ntì_ÀRÉÈ += ['--export', àmì_iye + '=' + ìlànà_ìgbéwọlé]
        ṣiṣẹ́_àṣẹ(ágúmẹ́ntì_ÀRÉÈ + sorted(ọ̀wọ́_ọ̀nà.glob('*.class')))
    (àtòpọ̀_ọ̀nà / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    Ṣẹ̀dá_aṣàmúlò_àlàfo(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́, 설정비트, ṣiṣẹ́_àṣẹ)
    Alásopọ̀ = Ṣẹ̀dá_Alásopọ̀(기준, 시언어번역기, Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́, 설정비트, ṣiṣẹ́_àṣẹ)
    원격사용 = Ṣẹ̀dá_Ìjìnnà(기준, 시언어번역기, Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́, 설정비트, ṣiṣẹ́_àṣẹ)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', àtòpọ̀_ọ̀nà]
    빌드작업 = [(시언어번역기, [], àtòpọ̀_ọ̀nà / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'maṣíìnì/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'maṣíìnì/wíjẹ́ẹ̀tì.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], àtòpọ̀_ọ̀nà / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'maṣíìnì/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'maṣíìnì/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'maṣíìnì/aṣàmúlò.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/ìgbéwọlé_kókó_iye.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Darapọ̀.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [fáìlì_ìgbéwọlé for fáìlì_ìgbéwọlé in 설정비트 if fáìlì_ìgbéwọlé != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        ṣiṣẹ́_àṣẹ([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', àtòpọ̀_ọ̀nà / 출력결과])
    ṣiṣẹ́_àṣẹ([Ìpamọ_ọlọ́jọ́pípẹ́_irinṣẹ́, 'rcs', àtòpọ̀_ọ̀nà / 'libposix-kor-arm64.a', àtòpọ̀_ọ̀nà / 'posix.o'])
    ṣiṣẹ́_àṣẹ([연결편집기, '--gc-sections', '-T', 기준 / '부팅/ṣàsopọ̀_ètò_ìrísí.ld', '-Map', àtòpọ̀_ọ̀nà / 'kernel.map', '-o', àtòpọ̀_ọ̀nà / 'kernel.elf'] +
        [àtòpọ̀_ọ̀nà / Orúkọ for Orúkọ in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', àtòpọ̀_ọ̀nà / 'libposix-kor-arm64.a', Alásopọ̀, 원격사용, àtòpọ̀_ọ̀nà / 'remote/libassh.a', àtòpọ̀_ọ̀nà / 'remote/libbearssl.a', '--end-group'])
    ṣiṣẹ́_àṣẹ([nǹkan_fáìlì_àyí_ohun_padà, '-O', 'binary', àtòpọ̀_ọ̀nà / 'kernel.elf', àtòpọ̀_ọ̀nà / 'kernel8.img'])
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
    for Orúkọ in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Orúkọ] = hashlib.sha256((àtòpọ̀_ọ̀nà / Orúkọ).read_bytes()).hexdigest()
    (àtòpọ̀_ọ̀nà / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', àtòpọ̀_ọ̀nà / 'kernel8.img')


if __name__ == '__main__':
    Rọ́ọ̀nù()
