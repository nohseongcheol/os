#!/usr/bin/env python3
"""usu javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from wue_òjìàrụ_ohere import mepụta_òjìàrụ_ohere
from wue_Netwọọkụ import mepụta_Netwọọkụ
from 예제빌드 import 예제만들기
from wue_ebe_dị̀anyā import mepụta_ebe_dị̀anyā

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
wue_ụzọ_ozi = 기준 / 'build'


def mee_nnyemiwu(agụment_MKPOKỌTA):
    subprocess.check_call([str(첫째값) for 첫째값 in agụment_MKPOKỌTA], cwd=str(기준))


def Bido():
    wue_ụzọ_ozi.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ihe_ọbọakwụkwọ_ogbanwe = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ọkpụ_ngwaọrụ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Ngwaọrụ in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ihe_ọbọakwụkwọ_ogbanwe, ọkpụ_ngwaọrụ):
        if not shutil.which(Ngwaọrụ):
            raise SystemExit('필요한 wue_sistèm Ngwaọrụ 없음: ' + Ngwaọrụ)
    ọnụndèe_ozi = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    ọnụndèe_datà = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(ọnụndèe_datà) != 65616 * 32 or hashlib.sha256(ọnụndèe_datà).hexdigest() != ọnụndèe_ozi['sha256']:
        raise SystemExit('터미널 ọnụndèe_valuu Ụhara/SHA256 불일치')
    zifè_tebùl = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'mkpụrụobī_kọmpùta.작업', 'jfs_path_start': 'memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_Mbido',
               'jfs_path_byte': 'memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị', 'jfs_open': 'memọrị_Ndi_ọbọakwụkwọ.Mepee',
               'jfs_read': 'memọrị_Ndi_ọbọakwụkwọ.Wepụta_ọzi', 'jfs_write': 'memọrị_Ndi_ọbọakwụkwọ.Chekwaa_ozi',
               'jfs_seek': 'memọrị_Ndi_ọbọakwụkwọ.옮기기', 'jfs_close': 'memọrị_Ndi_ọbọakwụkwọ.Mechie',
               'jfs_size': 'memọrị_Ndi_ọbọakwụkwọ.Ụhara', 'jfs_unlink': 'memọrị_Ndi_ọbọakwụkwọ.지우기',
               'jfs_truncate': 'memọrị_Ndi_ọbọakwụkwọ.Seti_ogologo'}
    zifè_tebùl.update({'jfs_entry_count': 'memọrị_Ndi_ọbọakwụkwọ.파일한도', 'jfs_entry_length': 'memọrị_Ndi_ọbọakwụkwọ.공개이름길이', 'jfs_entry_byte': 'memọrị_Ndi_ọbọakwụkwọ.공개이름바이트', 'jfs_entry_size': 'memọrị_Ndi_ọbọakwụkwọ.공개파일크기'})
    zifè_tebùl.update({'jdraw_prepare': '화면합성.Kwado', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ntipanye',
        'jdraw_clip_value': '화면합성.ntipanye_valuu', 'jdraw_begin': '화면합성.Bido',
        'jdraw_end': '화면합성.Gwụ', 'jdraw_pixel': '화면합성.pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.nrụaka'})
    zifè_tebùl.update({'jfs_mkdir': 'memọrị_Ndi_ọbọakwụkwọ.mepụta_dàịrektrị', 'jfs_rmdir': 'memọrị_Ndi_ọbọakwụkwọ.wepụ_dàịrektrị', 'jfs_kind': 'memọrị_Ndi_ọbọakwụkwọ.항목종류'})
    zifè_tebùl.update({'jnet_socket': '되돌림망.mepụta_ndebà', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.zìga',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Mechie'})
    zifè_tebùl.update({'jstream_create': 'agịrị_Netwọọkụ.mepụta_ndebà', 'jstream_bind': 'agịrị_Netwọọkụ.묶기', 'jstream_listen': 'agịrị_Netwọọkụ.듣기', 'jstream_connect': 'agịrị_Netwọọkụ.Banye', 'jstream_accept': 'agịrị_Netwọọkụ.nabata_njikọ', 'jstream_read': 'agịrị_Netwọọkụ.Wepụta_ọzi', 'jstream_write': 'agịrị_Netwọọkụ.Chekwaa_ozi', 'jstream_port': 'agịrị_Netwọọkụ.창구읽기', 'jstream_peer': 'agịrị_Netwọọkụ.상대창구읽기', 'jstream_close': 'agịrị_Netwọọkụ.Mechie'})
    for adimara_valuu in list(zifè_tebùl):
        if adimara_valuu.startswith('jstream_') or adimara_valuu.startswith('jnet_') and adimara_valuu not in ('jnet_put', 'jnet_get'):
            zifè_tebùl[adimara_valuu.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = zifè_tebùl.pop(adimara_valuu)
    예제들 = ['public final class ngwungwu { public static void Kwado() {']
    for ụzọ_ozi in sorted((기준 / '예제').iterdir()):
        if ụzọ_ozi.is_file():
            예제들.append('명령해석기.adịmgbanwò_ọbọakwụkwọ(%s, %s);' %
                (json.dumps(ụzọ_ozi.name), json.dumps(ụzọ_ozi.read_text(encoding='utf-8'), ensure_ascii=True)))
    (wue_ụzọ_ozi / 'ngwungwu.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, mee_nnyemiwu)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(wue_ụzọ_ozi)) as 작업경로:
        klaàsị_ụzọ_ozi = Path(작업경로)
        mee_nnyemiwu(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klaàsị_ụzọ_ozi, '-sourcepath', klaàsị_ụzọ_ozi, '-d', klaàsị_ụzọ_ozi] + sorted((기준 / 'ebensìbịa').glob('*.java')) + [wue_ụzọ_ozi / 'ngwungwu.java', wue_ụzọ_ozi / '예제꾸러미.java'])
        # Faịlụ·nkọwannyemiwu·windò 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        agụment_MKPOKỌTA = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'mkpụrụobī_kọmpùta.Bido', '--heap-words', '1048576', '-o', wue_ụzọ_ozi / 'kernel-java.c']
        for adimara_valuu, usoro_ndebà in sorted(zifè_tebùl.items()):
            agụment_MKPOKỌTA += ['--export', adimara_valuu + '=' + usoro_ndebà]
        mee_nnyemiwu(agụment_MKPOKỌTA + sorted(klaàsị_ụzọ_ozi.glob('*.class')))
    (wue_ụzọ_ozi / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    mepụta_òjìàrụ_ohere(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, ọkpụ_ngwaọrụ, 설정비트, mee_nnyemiwu)
    Netwọọkụ = mepụta_Netwọọkụ(기준, 시언어번역기, ọkpụ_ngwaọrụ, 설정비트, mee_nnyemiwu)
    원격사용 = mepụta_ebe_dị̀anyā(기준, 시언어번역기, ọkpụ_ngwaọrụ, 설정비트, mee_nnyemiwu)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', wue_ụzọ_ozi]
    빌드작업 = [(시언어번역기, [], wue_ụzọ_ozi / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'ngwa_komputa/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'ngwa_komputa/ngwa_nkepụta.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], wue_ụzọ_ozi / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'ngwa_komputa/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'ngwa_komputa/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'ngwa_komputa/òjìàrụ.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/ndebà_akara_valuu.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Banye.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ọbọakwụkwọ_ndebà for ọbọakwụkwọ_ndebà in 설정비트 if ọbọakwụkwọ_ndebà != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        mee_nnyemiwu([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', wue_ụzọ_ozi / 출력결과])
    mee_nnyemiwu([ọkpụ_ngwaọrụ, 'rcs', wue_ụzọ_ozi / 'libposix-kor-arm64.a', wue_ụzọ_ozi / 'posix.o'])
    mee_nnyemiwu([연결편집기, '--gc-sections', '-T', 기준 / '부팅/Njikọ_Nhàzi.ld', '-Map', wue_ụzọ_ozi / 'kernel.map', '-o', wue_ụzọ_ozi / 'kernel.elf'] +
        [wue_ụzọ_ozi / Aha for Aha in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', wue_ụzọ_ozi / 'libposix-kor-arm64.a', Netwọọkụ, 원격사용, wue_ụzọ_ozi / 'remote/libassh.a', wue_ụzọ_ozi / 'remote/libbearssl.a', '--end-group'])
    mee_nnyemiwu([ihe_ọbọakwụkwọ_ogbanwe, '-O', 'binary', wue_ụzọ_ozi / 'kernel.elf', wue_ụzọ_ozi / 'kernel8.img'])
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
    for Aha in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Aha] = hashlib.sha256((wue_ụzọ_ozi / Aha).read_bytes()).hexdigest()
    (wue_ụzọ_ozi / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', wue_ụzọ_ozi / 'kernel8.img')


if __name__ == '__main__':
    Bido()
