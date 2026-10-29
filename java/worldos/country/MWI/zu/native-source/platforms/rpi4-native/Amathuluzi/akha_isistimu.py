#!/usr/bin/env python3
"""singatha javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from akha_umsebenzisi_indawo import yakha_umsebenzisi_indawo
from akha_iNethiwekhi import yakha_iNethiwekhi
from 예제빌드 import 예제만들기
from akha_kude import yakha_kude

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
akha_umzila = 기준 / 'build'


def yenza_umyalo(i_agumenti_AMALUNGU_AFANAYO):
    subprocess.check_call([str(첫째값) for 첫째값 in i_agumenti_AMALUNGU_AFANAYO], cwd=str(기준))


def Sebenzisa():
    akha_umzila.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    into_ifayela_isiguquli = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    londoloza_ithuluzi = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Amathuluzi in ('javac', 시언어번역기, 시플플번역기, 연결편집기, into_ifayela_isiguquli, londoloza_ithuluzi):
        if not shutil.which(Amathuluzi):
            raise SystemExit('필요한 akha_isistimu Amathuluzi 없음: ' + Amathuluzi)
    ubuso_bohlamvu_ifonti_ulwazi = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    ubuso_bohlamvu_ifonti_imininingwane = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(ubuso_bohlamvu_ifonti_imininingwane) != 65616 * 32 or hashlib.sha256(ubuso_bohlamvu_ifonti_imininingwane).hexdigest() != ubuso_bohlamvu_ifonti_ulwazi['sha256']:
        raise SystemExit('터미널 ubuso_bohlamvu_ifonti_inani Ubungako/SHA256 불일치')
    thekelisa_ithebula = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'ikhenela.작업', 'jfs_path_start': 'inkumbulo_Amafayela.umzila_qala',
               'jfs_path_byte': 'inkumbulo_Amafayela.umzila_ibhayithi', 'jfs_open': 'inkumbulo_Amafayela.Vula',
               'jfs_read': 'inkumbulo_Amafayela.Funda', 'jfs_write': 'inkumbulo_Amafayela.Bhala',
               'jfs_seek': 'inkumbulo_Amafayela.옮기기', 'jfs_close': 'inkumbulo_Amafayela.Vala',
               'jfs_size': 'inkumbulo_Amafayela.Ubungako', 'jfs_unlink': 'inkumbulo_Amafayela.지우기',
               'jfs_truncate': 'inkumbulo_Amafayela.isethi_ubude'}
    thekelisa_ithebula.update({'jfs_entry_count': 'inkumbulo_Amafayela.파일한도', 'jfs_entry_length': 'inkumbulo_Amafayela.공개이름길이', 'jfs_entry_byte': 'inkumbulo_Amafayela.공개이름바이트', 'jfs_entry_size': 'inkumbulo_Amafayela.공개파일크기'})
    thekelisa_ithebula.update({'jdraw_prepare': '화면합성.Hlela', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.isiqeshana',
        'jdraw_clip_value': '화면합성.isiqeshana_inani', 'jdraw_begin': '화면합성.Sebenzisa',
        'jdraw_end': '화면합성.Qeda', 'jdraw_pixel': '화면합성.i_pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.isikhombi'})
    thekelisa_ithebula.update({'jfs_mkdir': 'inkumbulo_Amafayela.yakha_umkhombandlela', 'jfs_rmdir': 'inkumbulo_Amafayela.khipha_umkhombandlela', 'jfs_kind': 'inkumbulo_Amafayela.항목종류'})
    thekelisa_ithebula.update({'jnet_socket': '되돌림망.yakha_okufakwayo', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.Thumela',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Vala'})
    thekelisa_ithebula.update({'jstream_create': 'Stream_iNethiwekhi.yakha_okufakwayo', 'jstream_bind': 'Stream_iNethiwekhi.묶기', 'jstream_listen': 'Stream_iNethiwekhi.듣기', 'jstream_connect': 'Stream_iNethiwekhi.Xhumanisa', 'jstream_accept': 'Stream_iNethiwekhi.yamukela_uxhumano', 'jstream_read': 'Stream_iNethiwekhi.Funda', 'jstream_write': 'Stream_iNethiwekhi.Bhala', 'jstream_port': 'Stream_iNethiwekhi.창구읽기', 'jstream_peer': 'Stream_iNethiwekhi.상대창구읽기', 'jstream_close': 'Stream_iNethiwekhi.Vala'})
    for uphawu_inani in list(thekelisa_ithebula):
        if uphawu_inani.startswith('jstream_') or uphawu_inani.startswith('jnet_') and uphawu_inani not in ('jnet_put', 'jnet_get'):
            thekelisa_ithebula[uphawu_inani.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = thekelisa_ithebula.pop(uphawu_inani)
    예제들 = ['public final class isigaxa { public static void Hlela() {']
    for Indlela_2 in sorted((기준 / '예제').iterdir()):
        if Indlela_2.is_file():
            예제들.append('명령해석기.ngaguquki_ifayela(%s, %s);' %
                (json.dumps(Indlela_2.name), json.dumps(Indlela_2.read_text(encoding='utf-8'), ensure_ascii=True)))
    (akha_umzila / 'isigaxa.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, yenza_umyalo)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(akha_umzila)) as 작업경로:
        uhlobo_umzila = Path(작업경로)
        yenza_umyalo(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', uhlobo_umzila, '-sourcepath', uhlobo_umzila, '-d', uhlobo_umzila] + sorted((기준 / 'umthombo').glob('*.java')) + [akha_umzila / 'isigaxa.java', akha_umzila / '예제꾸러미.java'])
        # Ihele·isihumushi_miyalelo·ifasitela 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        i_agumenti_AMALUNGU_AFANAYO = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'ikhenela.Sebenzisa', '--heap-words', '1048576', '-o', akha_umzila / 'kernel-java.c']
        for uphawu_inani, indlela_okufakwayo in sorted(thekelisa_ithebula.items()):
            i_agumenti_AMALUNGU_AFANAYO += ['--export', uphawu_inani + '=' + indlela_okufakwayo]
        yenza_umyalo(i_agumenti_AMALUNGU_AFANAYO + sorted(uhlobo_umzila.glob('*.class')))
    (akha_umzila / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    yakha_umsebenzisi_indawo(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, londoloza_ithuluzi, 설정비트, yenza_umyalo)
    iNethiwekhi = yakha_iNethiwekhi(기준, 시언어번역기, londoloza_ithuluzi, 설정비트, yenza_umyalo)
    원격사용 = yakha_kude(기준, 시언어번역기, londoloza_ithuluzi, 설정비트, yenza_umyalo)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', akha_umzila]
    빌드작업 = [(시언어번역기, [], akha_umzila / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'umshini/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'umshini/iwijethi.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], akha_umzila / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'umshini/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'umshini/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'umshini/umsebenzisi.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/okufakwayo_iphoyinti_inani.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Xhumanisa.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ifayela_okufakwayo for ifayela_okufakwayo in 설정비트 if ifayela_okufakwayo != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        yenza_umyalo([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', akha_umzila / 출력결과])
    yenza_umyalo([londoloza_ithuluzi, 'rcs', akha_umzila / 'libposix-kor-arm64.a', akha_umzila / 'posix.o'])
    yenza_umyalo([연결편집기, '--gc-sections', '-T', 기준 / '부팅/xhuma_I_layout.ld', '-Map', akha_umzila / 'kernel.map', '-o', akha_umzila / 'kernel.elf'] +
        [akha_umzila / Igama for Igama in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', akha_umzila / 'libposix-kor-arm64.a', iNethiwekhi, 원격사용, akha_umzila / 'remote/libassh.a', akha_umzila / 'remote/libbearssl.a', '--end-group'])
    yenza_umyalo([into_ifayela_isiguquli, '-O', 'binary', akha_umzila / 'kernel.elf', akha_umzila / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Isi_Zulu.자체', 'korean_exceptions': 20,
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
    for Igama in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Igama] = hashlib.sha256((akha_umzila / Igama).read_bytes()).hexdigest()
    (akha_umzila / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', akha_umzila / 'kernel8.img')


if __name__ == '__main__':
    Sebenzisa()
