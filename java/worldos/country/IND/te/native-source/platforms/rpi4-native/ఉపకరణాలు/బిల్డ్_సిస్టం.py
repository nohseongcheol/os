#!/usr/bin/env python3
"""హోస్ట్ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from బిల్డ్_వినియోగదారు_ఖాళీ import క్రియేట్_వినియోగదారు_ఖాళీ
from బిల్డ్_నెట్_వర్క్ import క్రియేట్_నెట్_వర్క్
from 예제빌드 import 예제만들기
from బిల్డ్_రిమోట్ import క్రియేట్_రిమోట్

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]
రిపోజిటరీ_మూలం = ప్రొజెక్ట్_మూలం.parents[1]
బిల్డ్_పథం = ప్రొజెక్ట్_మూలం / 'build'


def అమలు_చేయి_ఆదేశం(కారకం_శ్రేణి):
    subprocess.check_call([str(첫째값) for 첫째값 in కారకం_శ్రేణి], cwd=str(ప్రొజెక్ట్_మూలం))


def నడుపుము():
    బిల్డ్_పథం.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    అంశం_ఫైలు_పరివర్తకం = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ఆర్కైవ్_ఉపకరణం = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ఉపకరణాలు in ('javac', 시언어번역기, 시플플번역기, 연결편집기, అంశం_ఫైలు_పరివర్తకం, ఆర్కైవ్_ఉపకరణం):
        if not shutil.which(ఉపకరణాలు):
            raise SystemExit('필요한 బిల్డ్_సిస్టం ఉపకరణాలు 없음: ' + ఉపకరణాలు)
    అక్షరాకృతి_సమాచారం = json.loads((ప్రొజెక్ట్_మూలం / 'vendor/terminal-font.json').read_text())
    అక్షరాకృతి_డేటా = (ప్రొజెక్ట్_మూలం / 'vendor/terminal-font.bin').read_bytes()
    if len(అక్షరాకృతి_డేటా) != 65616 * 32 or hashlib.sha256(అక్షరాకృతి_డేటా).hexdigest() != అక్షరాకృతి_సమాచారం['sha256']:
        raise SystemExit('టెర్మినల్ అక్షరాకృతి_మూల్యం పరిమాణం/SHA256 불일치')
    ఎగుమతి_చేయు_పట్టిక = {'jshell_interactive': '셸입출력.సమాచార_టెక్నాలజీ_పరస్పర', 'jshell_output': '셸입출력.అవుట్పుట్', 'jshell_input': '셸입출력.입력', 'java_task': 'కెర్నల్.작업', 'jfs_path_start': 'మెమరీ_ఫైల్_లు.పథం_ప్రారంభం',
               'jfs_path_byte': 'మెమరీ_ఫైల్_లు.పథం_బైట్', 'jfs_open': 'మెమరీ_ఫైల్_లు.తెరువు',
               'jfs_read': 'మెమరీ_ఫైల్_లు.చదువు', 'jfs_write': 'మెమరీ_ఫైల్_లు.వ్రాయుము',
               'jfs_seek': 'మెమరీ_ఫైల్_లు.శోధించు_స్థాయి', 'jfs_close': 'మెమరీ_ఫైల్_లు.మూసివేయి',
               'jfs_size': 'మెమరీ_ఫైల్_లు.పరిమాణం', 'jfs_unlink': 'మెమరీ_ఫైల్_లు.తుడిచివేయి_ప్రవేశం',
               'jfs_truncate': 'మెమరీ_ఫైల్_లు.సెట్_పొడవు'}
    ఎగుమతి_చేయు_పట్టిక.update({'jfs_entry_count': 'మెమరీ_ఫైల్_లు.파일한도', 'jfs_entry_length': 'మెమరీ_ఫైల్_లు.공개이름길이', 'jfs_entry_byte': 'మెమరీ_ఫైల్_లు.공개이름바이트', 'jfs_entry_size': 'మెమరీ_ఫైల్_లు.공개파일크기'})
    ఎగుమతి_చేయు_పట్టిక.update({'jdraw_prepare': '화면합성.సిద్ధం_చేయు', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.క్లిప్',
        'jdraw_clip_value': '화면합성.క్లిప్_మూల్యం', 'jdraw_begin': '화면합성.నడుపుము',
        'jdraw_end': '화면합성.ముగింపు', 'jdraw_pixel': '화면합성.పెల్',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.పాయింటర్'})
    ఎగుమతి_చేయు_పట్టిక.update({'jfs_mkdir': 'మెమరీ_ఫైల్_లు.క్రియేట్_సంచయని', 'jfs_rmdir': 'మెమరీ_ఫైల్_లు.తీసివెయ్యి_సంచయని', 'jfs_kind': 'మెమరీ_ఫైల్_లు.항목종류'})
    ఎగుమతి_చేయు_పట్టిక.update({'jnet_socket': '되돌림망.క్రియేట్_ప్రవేశం', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.పంపు',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.మూసివేయి'})
    ఎగుమతి_చేయు_పట్టిక.update({'jstream_create': 'ధార_నెట్_వర్క్.క్రియేట్_ప్రవేశం', 'jstream_bind': 'ధార_నెట్_వర్క్.묶기', 'jstream_listen': 'ధార_నెట్_వర్క్.듣기', 'jstream_connect': 'ధార_నెట్_వర్క్.కనెక్టుచేయి', 'jstream_accept': 'ధార_నెట్_వర్క్.ఆమోదించు_కనెక్షన్', 'jstream_read': 'ధార_నెట్_వర్క్.చదువు', 'jstream_write': 'ధార_నెట్_వర్క్.వ్రాయుము', 'jstream_port': 'ధార_నెట్_వర్క్.창구읽기', 'jstream_peer': 'ధార_నెట్_వర్క్.상대창구읽기', 'jstream_close': 'ధార_నెట్_వర్క్.మూసివేయి'})
    for చిహ్నం_మూల్యం in list(ఎగుమతి_చేయు_పట్టిక):
        if చిహ్నం_మూల్యం.startswith('jstream_') or చిహ్నం_మూల్యం.startswith('jnet_') and చిహ్నం_మూల్యం not in ('jnet_put', 'jnet_get'):
            ఎగుమతి_చేయు_పట్టిక[చిహ్నం_మూల్యం.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ఎగుమతి_చేయు_పట్టిక.pop(చిహ్నం_మూల్యం)
    예제들 = ['public final class బండిల్ { public static void సిద్ధం_చేయు() {']
    for పాత్ in sorted((ప్రొజెక్ట్_మూలం / '예제').iterdir()):
        if పాత్.is_file():
            예제들.append('명령해석기.నిశ్చల_ఫైలు(%s, %s);' %
                (json.dumps(పాత్.name), json.dumps(పాత్.read_text(encoding='utf-8'), ensure_ascii=True)))
    (బిల్డ్_పథం / 'బండిల్.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(ప్రొజెక్ట్_మూలం, రిపోజిటరీ_మూలం, అమలు_చేయి_ఆదేశం)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(బిల్డ్_పథం)) as 작업경로:
        తరగతి_పథం = Path(작업경로)
        అమలు_చేయి_ఆదేశం(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', తరగతి_పథం, '-sourcepath', తరగతి_పథం, '-d', తరగతి_పథం] + sorted((ప్రొజెక్ట్_మూలం / 'వనరు').glob('*.java')) + [బిల్డ్_పథం / 'బండిల్.java', బిల్డ్_పథం / '예제꾸러미.java'])
        # దస్త్రం·షెల్·విండో 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        కారకం_శ్రేణి = ['sh', రిపోజిటరీ_మూలం / 'compiler/미리번역.sh', '--entry', 'కెర్నల్.నడుపుము', '--heap-words', '1048576', '-o', బిల్డ్_పథం / 'kernel-java.c']
        for చిహ్నం_మూల్యం, విధానం_ప్రవేశం in sorted(ఎగుమతి_చేయు_పట్టిక.items()):
            కారకం_శ్రేణి += ['--export', చిహ్నం_మూల్యం + '=' + విధానం_ప్రవేశం]
        అమలు_చేయి_ఆదేశం(కారకం_శ్రేణి + sorted(తరగతి_పథం.glob('*.class')))
    (బిల్డ్_పథం / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = రిపోజిటరీ_మూలం / 'posix-kor/arm64-native'
    క్రియేట్_వినియోగదారు_ఖాళీ(ప్రొజెక్ట్_మూలం, రిపోజిటరీ_మూలం, 시언어번역기, 시플플번역기, 연결편집기, ఆర్కైవ్_ఉపకరణం, నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ, అమలు_చేయి_ఆదేశం)
    నెట్_వర్క్ = క్రియేట్_నెట్_వర్క్(ప్రొజెక్ట్_మూలం, 시언어번역기, ఆర్కైవ్_ఉపకరణం, నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ, అమలు_చేయి_ఆదేశం)
    원격사용 = క్రియేట్_రిమోట్(ప్రొజెక్ట్_మూలం, 시언어번역기, ఆర్కైవ్_ఉపకరణం, నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ, అమలు_చేయి_ఆదేశం)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', బిల్డ్_పథం]
    빌드작업 = [(시언어번역기, [], బిల్డ్_పథం / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ప్రొజెక్ట్_మూలం / 'యంత్రం/టెర్మినల్.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ప్రొజెక్ట్_మూలం / 'యంత్రం/విడ్జెట్.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], బిల్డ్_పథం / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ప్రొజెక్ట్_మూలం / 'యంత్రం/బోర్డు.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ప్రొజెక్ట్_మూలం / 'యంత్రం/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ప్రొజెక్ట్_మూలం / 'యంత్రం/వినియోగదారు.c', 'user.o'),
            (시언어번역기, [], ప్రొజెక్ట్_మూలం / '부팅/ప్రవేశం_పాయింట్_మూల్యం.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'కనెక్టుచేయి.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], ప్రొజెక్ట్_మూలం / '시험/ఫైలు_కాల్_లు.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ఫైలు_ప్రవేశం for ఫైలు_ప్రవేశం in నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ if ఫైలు_ప్రవేశం != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ
        అమలు_చేయి_ఆదేశం([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', బిల్డ్_పథం / 출력결과])
    అమలు_చేయి_ఆదేశం([ఆర్కైవ్_ఉపకరణం, 'rcs', బిల్డ్_పథం / 'libposix-kor-arm64.a', బిల్డ్_పథం / 'posix.o'])
    అమలు_చేయి_ఆదేశం([연결편집기, '--gc-sections', '-T', ప్రొజెక్ట్_మూలం / '부팅/బంధం_లేవుట్.ld', '-Map', బిల్డ్_పథం / 'kernel.map', '-o', బిల్డ్_పథం / 'kernel.elf'] +
        [బిల్డ్_పథం / పేరు for పేరు in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', బిల్డ్_పథం / 'libposix-kor-arm64.a', నెట్_వర్క్, 원격사용, బిల్డ్_పథం / 'remote/libassh.a', బిల్డ్_పథం / 'remote/libbearssl.a', '--end-group'])
    అమలు_చేయి_ఆదేశం([అంశం_ఫైలు_పరివర్తకం, '-O', 'binary', బిల్డ్_పథం / 'kernel.elf', బిల్డ్_పథం / 'kernel8.img'])
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
    for పేరు in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][పేరు] = hashlib.sha256((బిల్డ్_పథం / పేరు).read_bytes()).hexdigest()
    (బిల్డ్_పథం / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', బిల్డ్_పథం / 'kernel8.img')


if __name__ == '__main__':
    నడుపుము()
