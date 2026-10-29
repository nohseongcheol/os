#!/usr/bin/env python3
"""ហូស javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from ចងក្រង_អ្នកប្រើ_លំហ import បង្កើត_អ្នកប្រើ_លំហ
from ចងក្រង_ណិតវឺក import បង្កើត_ណិតវឺក
from 예제빌드 import 예제만들기
from ចងក្រង_ពីចម្ងាយ import បង្កើត_ពីចម្ងាយ

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]
ឃ្លាំង_ផ្ទុក_ឬស = បញ្ចាំង_ឬស.parents[1]
ចងក្រង_ផ្លូវ = បញ្ចាំង_ឬស / 'build'


def អនុវត្ត_ពាក្យបញ្ជា(អាគុយម៉ង់_អារេ):
    subprocess.check_call([str(첫째값) for 첫째값 in អាគុយម៉ង់_អារេ], cwd=str(បញ្ចាំង_ឬស))


def រត់():
    ចងក្រង_ផ្លូវ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    វត្ថុ_ឯកសារ_អង្គបំលែង = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ប័ណ្ណសារ_ឧបករណ៏ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ឧបករណ៍ in ('javac', 시언어번역기, 시플플번역기, 연결편집기, វត្ថុ_ឯកសារ_អង្គបំលែង, ប័ណ្ណសារ_ឧបករណ៏):
        if not shutil.which(ឧបករណ៍):
            raise SystemExit('필요한 ចងក្រង_ប្រព័ន្ធ ឧបករណ៍ 없음: ' + ឧបករណ៍)
    ពុម្ពអក្សរ_ព័ត៌មាន = json.loads((បញ្ចាំង_ឬស / 'vendor/terminal-font.json').read_text())
    ពុម្ពអក្សរ_ទិន្នន័យ = (បញ្ចាំង_ឬស / 'vendor/terminal-font.bin').read_bytes()
    if len(ពុម្ពអក្សរ_ទិន្នន័យ) != 65616 * 32 or hashlib.sha256(ពុម្ពអក្សរ_ទិន្នន័យ).hexdigest() != ពុម្ពអក្សរ_ព័ត៌មាន['sha256']:
        raise SystemExit('ស្ថានីយ ពុម្ពអក្សរ_តំលៃ ដាក់ទំហំ/SHA256 불일치')
    នាំចេញ_តារាង = {'jshell_interactive': '셸입출력.បច្ចេកវិទ្យាព័ត៌មាន_អន្តរកម្ម', 'jshell_output': '셸입출력.លទ្ធផល', 'jshell_input': '셸입출력.입력', 'java_task': 'ខឺណេល.작업', 'jfs_path_start': 'សតិ_ឯកសារ.ផ្លូវ_ផ្តើម',
               'jfs_path_byte': 'សតិ_ឯកសារ.ផ្លូវ_បៃ', 'jfs_open': 'សតិ_ឯកសារ.បើក',
               'jfs_read': 'សតិ_ឯកសារ.អាន', 'jfs_write': 'សតិ_ឯកសារ.សរសេរ',
               'jfs_seek': 'សតិ_ឯកសារ.ស្វែងរក_កំណត់ទីតាំង', 'jfs_close': 'សតិ_ឯកសារ.បិទ',
               'jfs_size': 'សតិ_ឯកសារ.ដាក់ទំហំ', 'jfs_unlink': 'សតិ_ឯកសារ.លុប_ការបញ្ចូល',
               'jfs_truncate': 'សតិ_ឯកសារ.កំណត់_ប្រវែង'}
    នាំចេញ_តារាង.update({'jfs_entry_count': 'សតិ_ឯកសារ.파일한도', 'jfs_entry_length': 'សតិ_ឯកសារ.공개이름길이', 'jfs_entry_byte': 'សតិ_ឯកសារ.공개이름바이트', 'jfs_entry_size': 'សតិ_ឯកសារ.공개파일크기'})
    នាំចេញ_តារាង.update({'jdraw_prepare': '화면합성.រៀបចំ', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.មេឌៀខ្លីៗ',
        'jdraw_clip_value': '화면합성.មេឌៀខ្លីៗ_តំលៃ', 'jdraw_begin': '화면합성.រត់',
        'jdraw_end': '화면합성.បញ្ចប់', 'jdraw_pixel': '화면합성.ចំនុចតូចៗ',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.អង្គ_ចង្អុល_កណ្ដុរ'})
    នាំចេញ_តារាង.update({'jfs_mkdir': 'សតិ_ឯកសារ.បង្កើត_បញ្ជី', 'jfs_rmdir': 'សតិ_ឯកសារ.យកចេញ_បញ្ជី', 'jfs_kind': 'សតិ_ឯកសារ.항목종류'})
    នាំចេញ_តារាង.update({'jnet_socket': '되돌림망.បង្កើត_ការបញ្ចូល', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ផ្ញើ',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.បិទ'})
    នាំចេញ_តារាង.update({'jstream_create': 'ស្ទ្រីម_ណិតវឺក.បង្កើត_ការបញ្ចូល', 'jstream_bind': 'ស្ទ្រីម_ណិតវឺក.묶기', 'jstream_listen': 'ស្ទ្រីម_ណិតវឺក.듣기', 'jstream_connect': 'ស្ទ្រីម_ណិតវឺក.ភ្ជាប់', 'jstream_accept': 'ស្ទ្រីម_ណិតវឺក.ទទួល_យក_ការភ្ជាប់', 'jstream_read': 'ស្ទ្រីម_ណិតវឺក.អាន', 'jstream_write': 'ស្ទ្រីម_ណិតវឺក.សរសេរ', 'jstream_port': 'ស្ទ្រីម_ណិតវឺក.창구읽기', 'jstream_peer': 'ស្ទ្រីម_ណិតវឺក.상대창구읽기', 'jstream_close': 'ស្ទ្រីម_ណិតវឺក.បិទ'})
    for និមិត្ត_សញ្ញា_តំលៃ in list(នាំចេញ_តារាង):
        if និមិត្ត_សញ្ញា_តំលៃ.startswith('jstream_') or និមិត្ត_សញ្ញា_តំលៃ.startswith('jnet_') and និមិត្ត_សញ្ញា_តំលៃ not in ('jnet_put', 'jnet_get'):
            នាំចេញ_តារាង[និមិត្ត_សញ្ញា_តំលៃ.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = នាំចេញ_តារាង.pop(និមិត្ត_សញ្ញា_តំលៃ)
    예제들 = ['public final class បាច់ { public static void រៀបចំ() {']
    for ផ្លូវ in sorted((បញ្ចាំង_ឬស / '예제').iterdir()):
        if ផ្លូវ.is_file():
            예제들.append('명령해석기.នឹង_ឯកសារ(%s, %s);' %
                (json.dumps(ផ្លូវ.name), json.dumps(ផ្លូវ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (ចងក្រង_ផ្លូវ / 'បាច់.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(បញ្ចាំង_ឬស, ឃ្លាំង_ផ្ទុក_ឬស, អនុវត្ត_ពាក្យបញ្ជា)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(ចងក្រង_ផ្លូវ)) as 작업경로:
        ថ្នាក់_ផ្លូវ = Path(작업경로)
        អនុវត្ត_ពាក្យបញ្ជា(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ថ្នាក់_ផ្លូវ, '-sourcepath', ថ្នាក់_ផ្លូវ, '-d', ថ្នាក់_ផ្លូវ] + sorted((បញ្ចាំង_ឬស / 'ប្រភព').glob('*.java')) + [ចងក្រង_ផ្លូវ / 'បាច់.java', ចងក្រង_ផ្លូវ / '예제꾸러미.java'])
        # ឯកសារ·셸·វីនដូ 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        អាគុយម៉ង់_អារេ = ['sh', ឃ្លាំង_ផ្ទុក_ឬស / 'compiler/미리번역.sh', '--entry', 'ខឺណេល.រត់', '--heap-words', '1048576', '-o', ចងក្រង_ផ្លូវ / 'kernel-java.c']
        for និមិត្ត_សញ្ញា_តំលៃ, វិធីសាស្រ្ត_ការបញ្ចូល in sorted(នាំចេញ_តារាង.items()):
            អាគុយម៉ង់_អារេ += ['--export', និមិត្ត_សញ្ញា_តំលៃ + '=' + វិធីសាស្រ្ត_ការបញ្ចូល]
        អនុវត្ត_ពាក្យបញ្ជា(អាគុយម៉ង់_អារេ + sorted(ថ្នាក់_ផ្លូវ.glob('*.class')))
    (ចងក្រង_ផ្លូវ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = ឃ្លាំង_ផ្ទុក_ឬស / 'posix-kor/arm64-native'
    បង្កើត_អ្នកប្រើ_លំហ(បញ្ចាំង_ឬស, ឃ្លាំង_ផ្ទុក_ឬស, 시언어번역기, 시플플번역기, 연결편집기, ប័ណ្ណសារ_ឧបករណ៏, ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ, អនុវត្ត_ពាក្យបញ្ជា)
    ណិតវឺក = បង្កើត_ណិតវឺក(បញ្ចាំង_ឬស, 시언어번역기, ប័ណ្ណសារ_ឧបករណ៏, ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ, អនុវត្ត_ពាក្យបញ្ជា)
    원격사용 = បង្កើត_ពីចម្ងាយ(បញ្ចាំង_ឬស, 시언어번역기, ប័ណ្ណសារ_ឧបករណ៏, ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ, អនុវត្ត_ពាក្យបញ្ជា)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', ចងក្រង_ផ្លូវ]
    빌드작업 = [(시언어번역기, [], ចងក្រង_ផ្លូវ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], បញ្ចាំង_ឬស / 'ម៉ាស៊ីន/ស្ថានីយ.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], បញ្ចាំង_ឬស / 'ម៉ាស៊ីន/វីដហ្គេត.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], ចងក្រង_ផ្លូវ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], បញ្ចាំង_ឬស / 'ម៉ាស៊ីន/ផ្ទាំង.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], បញ្ចាំង_ឬស / 'ម៉ាស៊ីន/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], បញ្ចាំង_ឬស / 'ម៉ាស៊ីន/អ្នកប្រើ.c', 'user.o'),
            (시언어번역기, [], បញ្ចាំង_ឬស / '부팅/ការបញ្ចូល_ចំនុច_តំលៃ.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'ភ្ជាប់.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], បញ្ចាំង_ឬស / '시험/ឯកសារ_ការហៅ.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ឯកសារ_ការបញ្ចូល for ឯកសារ_ការបញ្ចូល in ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ if ឯកសារ_ការបញ្ចូល != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ
        អនុវត្ត_ពាក្យបញ្ជា([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', ចងក្រង_ផ្លូវ / 출력결과])
    អនុវត្ត_ពាក្យបញ្ជា([ប័ណ្ណសារ_ឧបករណ៏, 'rcs', ចងក្រង_ផ្លូវ / 'libposix-kor-arm64.a', ចងក្រង_ផ្លូវ / 'posix.o'])
    អនុវត្ត_ពាក្យបញ្ជា([연결편집기, '--gc-sections', '-T', បញ្ចាំង_ឬស / '부팅/តំណ_ប្លង់.ld', '-Map', ចងក្រង_ផ្លូវ / 'kernel.map', '-o', ចងក្រង_ផ្លូវ / 'kernel.elf'] +
        [ចងក្រង_ផ្លូវ / ឈ្មោះ for ឈ្មោះ in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', ចងក្រង_ផ្លូវ / 'libposix-kor-arm64.a', ណិតវឺក, 원격사용, ចងក្រង_ផ្លូវ / 'remote/libassh.a', ចងក្រង_ផ្លូវ / 'remote/libbearssl.a', '--end-group'])
    អនុវត្ត_ពាក្យបញ្ជា([វត្ថុ_ឯកសារ_អង្គបំលែង, '-O', 'binary', ចងក្រង_ផ្លូវ / 'kernel.elf', ចងក្រង_ផ្លូវ / 'kernel8.img'])
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
    for ឈ្មោះ in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][ឈ្មោះ] = hashlib.sha256((ចងក្រង_ផ្លូវ / ឈ្មោះ).read_bytes()).hexdigest()
    (ចងក្រង_ផ្លូវ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', ចងក្រង_ផ្លូវ / 'kernel8.img')


if __name__ == '__main__':
    រត់()
