#!/usr/bin/env python3
"""አዐንግድ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from ህነጽ_ተጠቃሚ_ቦታ import ፍጠር_ተጠቃሚ_ቦታ
from ህነጽ_ማሕበራዊ_ኔትወርክ import ፍጠር_ማሕበራዊ_ኔትወርክ
from 예제빌드 import 예제만들기
from ህነጽ_ርሑቕ import ፍጠር_ርሑቕ

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
ህነጽ_መገዲ = 기준 / 'build'


def ተግብር_ትእዛዝ(ሓባሪ_ቁጽሪ_ተርታ):
    subprocess.check_call([str(첫째값) for 첫째값 in ሓባሪ_ቁጽሪ_ተርታ], cwd=str(기준))


def ኣኺድ():
    ህነጽ_መገዲ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ነገር_ፋይል_ለዋጢ = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ሰንድ_መሳርሒ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for መሳርሒታት in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ነገር_ፋይል_ለዋጢ, ሰንድ_መሳርሒ):
        if not shutil.which(መሳርሒታት):
            raise SystemExit('필요한 ህነጽ_ስርዓት መሳርሒታት 없음: ' + መሳርሒታት)
    ቅርጺ_ፊደል_ሓበሬታ_c16c0f1c = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    ቅርጺ_ፊደል_ሓበሬታ = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(ቅርጺ_ፊደል_ሓበሬታ) != 65616 * 32 or hashlib.sha256(ቅርጺ_ፊደል_ሓበሬታ).hexdigest() != ቅርጺ_ፊደል_ሓበሬታ_c16c0f1c['sha256']:
        raise SystemExit('터미널 ቅርጺ_ፊደል_ዋጋ መጠን/SHA256 불일치')
    ስደድ_ሰሌዳ = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'ፍረ.작업', 'jfs_path_start': 'ማህደር_ዝኽረት_ፋይላት.መገዲ_ጀምር',
               'jfs_path_byte': 'ማህደር_ዝኽረት_ፋይላት.መገዲ_ባይት', 'jfs_open': 'ማህደር_ዝኽረት_ፋይላት.ክፈት',
               'jfs_read': 'ማህደር_ዝኽረት_ፋይላት.읽기', 'jfs_write': 'ማህደር_ዝኽረት_ፋይላት.ጸሓፍ',
               'jfs_seek': 'ማህደር_ዝኽረት_ፋይላት.옮기기', 'jfs_close': 'ማህደር_ዝኽረት_ፋይላት.ዕጸው',
               'jfs_size': 'ማህደር_ዝኽረት_ፋይላት.መጠን', 'jfs_unlink': 'ማህደር_ዝኽረት_ፋይላት.지우기',
               'jfs_truncate': 'ማህደር_ዝኽረት_ፋይላት.እኩብ_ንውሓት'}
    ስደድ_ሰሌዳ.update({'jfs_entry_count': 'ማህደር_ዝኽረት_ፋይላት.파일한도', 'jfs_entry_length': 'ማህደር_ዝኽረት_ፋይላት.공개이름길이', 'jfs_entry_byte': 'ማህደር_ዝኽረት_ፋይላት.공개이름바이트', 'jfs_entry_size': 'ማህደር_ዝኽረት_ፋይላት.공개파일크기'})
    ስደድ_ሰሌዳ.update({'jdraw_prepare': '화면합성.ኣዳልው', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ቅንጣብ',
        'jdraw_clip_value': '화면합성.ቅንጣብ_ዋጋ', 'jdraw_begin': '화면합성.ኣኺድ',
        'jdraw_end': '화면합성.ጨርስ', 'jdraw_pixel': '화면합성.ንጣብ',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.ኣመልካቲ'})
    ስደድ_ሰሌዳ.update({'jfs_mkdir': 'ማህደር_ዝኽረት_ፋይላት.ፍጠር_ሓባሪ_ማህደር', 'jfs_rmdir': 'ማህደር_ዝኽረት_ፋይላት.ኣልግስ_ሓባሪ_ማህደር', 'jfs_kind': 'ማህደር_ዝኽረት_ፋይላት.항목종류'})
    ስደድ_ሰሌዳ.update({'jnet_socket': '되돌림망.ፍጠር_ምእታው', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ለኣኽ',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.ዕጸው'})
    ስደድ_ሰሌዳ.update({'jstream_create': 'ወሓዚ_ማሕበራዊ_ኔትወርክ.ፍጠር_ምእታው', 'jstream_bind': 'ወሓዚ_ማሕበራዊ_ኔትወርክ.묶기', 'jstream_listen': 'ወሓዚ_ማሕበራዊ_ኔትወርክ.듣기', 'jstream_connect': 'ወሓዚ_ማሕበራዊ_ኔትወርክ.ኣላግብ', 'jstream_accept': 'ወሓዚ_ማሕበራዊ_ኔትወርክ.ተቐበል_ርክብ', 'jstream_read': 'ወሓዚ_ማሕበራዊ_ኔትወርክ.읽기', 'jstream_write': 'ወሓዚ_ማሕበራዊ_ኔትወርክ.ጸሓፍ', 'jstream_port': 'ወሓዚ_ማሕበራዊ_ኔትወርክ.창구읽기', 'jstream_peer': 'ወሓዚ_ማሕበራዊ_ኔትወርክ.상대창구읽기', 'jstream_close': 'ወሓዚ_ማሕበራዊ_ኔትወርክ.ዕጸው'})
    for ምልክት_ዋጋ in list(ስደድ_ሰሌዳ):
        if ምልክት_ዋጋ.startswith('jstream_') or ምልክት_ዋጋ.startswith('jnet_') and ምልክት_ዋጋ not in ('jnet_put', 'jnet_get'):
            ስደድ_ሰሌዳ[ምልክት_ዋጋ.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ስደድ_ሰሌዳ.pop(ምልክት_ዋጋ)
    예제들 = ['public final class ጥማር { public static void ኣዳልው() {']
    for መገዲ in sorted((기준 / '예제').iterdir()):
        if መገዲ.is_file():
            예제들.append('명령해석기.ቀዋሚ_ፋይል(%s, %s);' %
                (json.dumps(መገዲ.name), json.dumps(መገዲ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (ህነጽ_መገዲ / 'ጥማር.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, ተግብር_ትእዛዝ)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(ህነጽ_መገዲ)) as 작업경로:
        ክፍሊ_መገዲ = Path(작업경로)
        ተግብር_ትእዛዝ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ክፍሊ_መገዲ, '-sourcepath', ክፍሊ_መገዲ, '-d', ክፍሊ_መገዲ] + sorted((기준 / 'ምንጪ').glob('*.java')) + [ህነጽ_መገዲ / 'ጥማር.java', ህነጽ_መገዲ / '예제꾸러미.java'])
        # ፋይል·ሽፋን·መስኮት 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ሓባሪ_ቁጽሪ_ተርታ = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'ፍረ.ኣኺድ', '--heap-words', '1048576', '-o', ህነጽ_መገዲ / 'kernel-java.c']
        for ምልክት_ዋጋ, ሜላ_ምእታው in sorted(ስደድ_ሰሌዳ.items()):
            ሓባሪ_ቁጽሪ_ተርታ += ['--export', ምልክት_ዋጋ + '=' + ሜላ_ምእታው]
        ተግብር_ትእዛዝ(ሓባሪ_ቁጽሪ_ተርታ + sorted(ክፍሊ_መገዲ.glob('*.class')))
    (ህነጽ_መገዲ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    ፍጠር_ተጠቃሚ_ቦታ(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, ሰንድ_መሳርሒ, 설정비트, ተግብር_ትእዛዝ)
    ማሕበራዊ_ኔትወርክ = ፍጠር_ማሕበራዊ_ኔትወርክ(기준, 시언어번역기, ሰንድ_መሳርሒ, 설정비트, ተግብር_ትእዛዝ)
    원격사용 = ፍጠር_ርሑቕ(기준, 시언어번역기, ሰንድ_መሳርሒ, 설정비트, ተግብር_ትእዛዝ)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', ህነጽ_መገዲ]
    빌드작업 = [(시언어번역기, [], ህነጽ_መገዲ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'ማሽን/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'ማሽን/መዘካከሪ_መትሓዚ.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], ህነጽ_መገዲ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'ማሽን/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'ማሽን/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'ማሽን/ተጠቃሚ.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/ምእታው_ነጥቢ_ዋጋ.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'ኣላግብ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ፋይል_ምእታው for ፋይል_ምእታው in 설정비트 if ፋይል_ምእታው != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        ተግብር_ትእዛዝ([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', ህነጽ_መገዲ / 출력결과])
    ተግብር_ትእዛዝ([ሰንድ_መሳርሒ, 'rcs', ህነጽ_መገዲ / 'libposix-kor-arm64.a', ህነጽ_መገዲ / 'posix.o'])
    ተግብር_ትእዛዝ([연결편집기, '--gc-sections', '-T', 기준 / '부팅/መጋጠሚ_ኣቀማምጣ.ld', '-Map', ህነጽ_መገዲ / 'kernel.map', '-o', ህነጽ_መገዲ / 'kernel.elf'] +
        [ህነጽ_መገዲ / ሽም for ሽም in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', ህነጽ_መገዲ / 'libposix-kor-arm64.a', ማሕበራዊ_ኔትወርክ, 원격사용, ህነጽ_መገዲ / 'remote/libassh.a', ህነጽ_መገዲ / 'remote/libbearssl.a', '--end-group'])
    ተግብር_ትእዛዝ([ነገር_ፋይል_ለዋጢ, '-O', 'binary', ህነጽ_መገዲ / 'kernel.elf', ህነጽ_መገዲ / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'ትግርኛ.자체', 'korean_exceptions': 20,
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
    for ሽም in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][ሽም] = hashlib.sha256((ህነጽ_መገዲ / ሽም).read_bytes()).hexdigest()
    (ህነጽ_መገዲ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', ህነጽ_መገዲ / 'kernel8.img')


if __name__ == '__main__':
    ኣኺድ()
