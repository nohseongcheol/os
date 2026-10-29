#!/usr/bin/env python3
"""አዘጋጅ_b78e430d javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from ግንብ_ተጠቃሚ_ቦታ import ፍጠር_ተጠቃሚ_ቦታ
from ግንብ_መረብ import ፍጠር_መረብ
from 예제빌드 import 예제만들기
from ግንብ_የሩቅ import ፍጠር_የሩቅ

አሳይ_ስር = Path(__file__).resolve().parents[1]
ማከማቻ_ስር = አሳይ_ስር.parents[1]
ግንብ_ዱካ = አሳይ_ስር / 'build'


def ፈጽም_ትእዛዝ(ነጋሪ_እሴት_ድርድር):
    subprocess.check_call([str(첫째값) for 첫째값 in ነጋሪ_እሴት_ድርድር], cwd=str(አሳይ_ስር))


def ማስኬጃ():
    ግንብ_ዱካ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ነገር_ፋይል_ለዋጭ = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ከዝን_መሳሪያ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for መሳሪያዎች in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ነገር_ፋይል_ለዋጭ, ከዝን_መሳሪያ):
        if not shutil.which(መሳሪያዎች):
            raise SystemExit('필요한 ግንብ_ስርዓት መሳሪያዎች 없음: ' + መሳሪያዎች)
    ቅርጸ_ቁምፊ_መረጃ = json.loads((አሳይ_ስር / 'vendor/terminal-font.json').read_text())
    ቅርጸ_ቁምፊ_ውሂብ = (አሳይ_ስር / 'vendor/terminal-font.bin').read_bytes()
    if len(ቅርጸ_ቁምፊ_ውሂብ) != 65616 * 32 or hashlib.sha256(ቅርጸ_ቁምፊ_ውሂብ).hexdigest() != ቅርጸ_ቁምፊ_መረጃ['sha256']:
        raise SystemExit('ተርሚናል ቅርጸ_ቁምፊ_እሴት መጠን/SHA256 불일치')
    አስወጣ_ሰንጠረዥ = {'jshell_interactive': '셸입출력.የመረጃ_ቴክኖሎጂ_በይነተገናኝ', 'jshell_output': '셸입출력.ውጤት', 'jshell_input': '셸입출력.입력', 'java_task': 'ዓንኳር.작업', 'jfs_path_start': 'ማስቀመጫ_ፋይሎች.ዱካ_ጀምር',
               'jfs_path_byte': 'ማስቀመጫ_ፋይሎች.ዱካ_ባይት', 'jfs_open': 'ማስቀመጫ_ፋይሎች.መክፈቻ',
               'jfs_read': 'ማስቀመጫ_ፋይሎች.ማንበቢያ', 'jfs_write': 'ማስቀመጫ_ፋይሎች.መጻፊያ',
               'jfs_seek': 'ማስቀመጫ_ፋይሎች.ፈልግ_በቦታ_አስቀመጠ', 'jfs_close': 'ማስቀመጫ_ፋይሎች.መዝጊያ',
               'jfs_size': 'ማስቀመጫ_ፋይሎች.መጠን', 'jfs_unlink': 'ማስቀመጫ_ፋይሎች.አስወግድ_ምዝግብ_c8dbc399',
               'jfs_truncate': 'ማስቀመጫ_ፋይሎች.ስብስብ_ርዝመት'}
    አስወጣ_ሰንጠረዥ.update({'jfs_entry_count': 'ማስቀመጫ_ፋይሎች.파일한도', 'jfs_entry_length': 'ማስቀመጫ_ፋይሎች.공개이름길이', 'jfs_entry_byte': 'ማስቀመጫ_ፋይሎች.공개이름바이트', 'jfs_entry_size': 'ማስቀመጫ_ፋይሎች.공개파일크기'})
    አስወጣ_ሰንጠረዥ.update({'jdraw_prepare': '화면합성.አዘጋጅ_9ce364fc', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ቅንጥብ',
        'jdraw_clip_value': '화면합성.ቅንጥብ_እሴት', 'jdraw_begin': '화면합성.ማስኬጃ',
        'jdraw_end': '화면합성.ጨርስ', 'jdraw_pixel': '화면합성.ፒክስል',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.ጠቋሚ'})
    አስወጣ_ሰንጠረዥ.update({'jfs_mkdir': 'ማስቀመጫ_ፋይሎች.ፍጠር_ማውጫ', 'jfs_rmdir': 'ማስቀመጫ_ፋይሎች.አስወግድ_ማውጫ', 'jfs_kind': 'ማስቀመጫ_ፋይሎች.항목종류'})
    አስወጣ_ሰንጠረዥ.update({'jnet_socket': '되돌림망.ፍጠር_ምዝግብ', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ላክ',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.መዝጊያ'})
    አስወጣ_ሰንጠረዥ.update({'jstream_create': 'ልቀቅ_መረብ.ፍጠር_ምዝግብ', 'jstream_bind': 'ልቀቅ_መረብ.묶기', 'jstream_listen': 'ልቀቅ_መረብ.듣기', 'jstream_connect': 'ልቀቅ_መረብ.መገናኛ', 'jstream_accept': 'ልቀቅ_መረብ.ተቀበል_ግንኙነት', 'jstream_read': 'ልቀቅ_መረብ.ማንበቢያ', 'jstream_write': 'ልቀቅ_መረብ.መጻፊያ', 'jstream_port': 'ልቀቅ_መረብ.창구읽기', 'jstream_peer': 'ልቀቅ_መረብ.상대창구읽기', 'jstream_close': 'ልቀቅ_መረብ.መዝጊያ'})
    for ምልክት_እሴት in list(አስወጣ_ሰንጠረዥ):
        if ምልክት_እሴት.startswith('jstream_') or ምልክት_እሴት.startswith('jnet_') and ምልክት_እሴት not in ('jnet_put', 'jnet_get'):
            አስወጣ_ሰንጠረዥ[ምልክት_እሴት.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = አስወጣ_ሰንጠረዥ.pop(ምልክት_እሴት)
    예제들 = ['public final class ቀርቅብ { public static void አዘጋጅ_9ce364fc() {']
    for መተላለፊያ in sorted((አሳይ_ስር / '예제').iterdir()):
        if መተላለፊያ.is_file():
            예제들.append('명령해석기.አይንቀሳቀሴ_ፋይል(%s, %s);' %
                (json.dumps(መተላለፊያ.name), json.dumps(መተላለፊያ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (ግንብ_ዱካ / 'ቀርቅብ.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(አሳይ_ስር, ማከማቻ_ስር, ፈጽም_ትእዛዝ)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(ግንብ_ዱካ)) as 작업경로:
        መደብ_ዱካ = Path(작업경로)
        ፈጽም_ትእዛዝ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', መደብ_ዱካ, '-sourcepath', መደብ_ዱካ, '-d', መደብ_ዱካ] + sorted((አሳይ_ስር / 'ምንጭ').glob('*.java')) + [ግንብ_ዱካ / 'ቀርቅብ.java', ግንብ_ዱካ / '예제꾸러미.java'])
        # ፋይል·ሼል·መስኮት 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ነጋሪ_እሴት_ድርድር = ['sh', ማከማቻ_ስር / 'compiler/미리번역.sh', '--entry', 'ዓንኳር.ማስኬጃ', '--heap-words', '1048576', '-o', ግንብ_ዱካ / 'kernel-java.c']
        for ምልክት_እሴት, ስልት_ምዝግብ in sorted(አስወጣ_ሰንጠረዥ.items()):
            ነጋሪ_እሴት_ድርድር += ['--export', ምልክት_እሴት + '=' + ስልት_ምዝግብ]
        ፈጽም_ትእዛዝ(ነጋሪ_እሴት_ድርድር + sorted(መደብ_ዱካ.glob('*.class')))
    (ግንብ_ዱካ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = ማከማቻ_ስር / 'posix-kor/arm64-native'
    ፍጠር_ተጠቃሚ_ቦታ(አሳይ_ስር, ማከማቻ_ስር, 시언어번역기, 시플플번역기, 연결편집기, ከዝን_መሳሪያ, ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት, ፈጽም_ትእዛዝ)
    መረብ = ፍጠር_መረብ(አሳይ_ስር, 시언어번역기, ከዝን_መሳሪያ, ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት, ፈጽም_ትእዛዝ)
    원격사용 = ፍጠር_የሩቅ(አሳይ_ስር, 시언어번역기, ከዝን_መሳሪያ, ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት, ፈጽም_ትእዛዝ)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', ግንብ_ዱካ]
    빌드작업 = [(시언어번역기, [], ግንብ_ዱካ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], አሳይ_ስር / 'ማሽን/ተርሚናል.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], አሳይ_ስር / 'ማሽን/ዊድጌት.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], ግንብ_ዱካ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], አሳይ_ስር / 'ማሽን/ቦርድ.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], አሳይ_ስር / 'ማሽን/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], አሳይ_ስር / 'ማሽን/ተጠቃሚ.c', 'user.o'),
            (시언어번역기, [], አሳይ_ስር / '부팅/ምዝግብ_ቦታ_እሴት.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'መገናኛ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], አሳይ_ስር / '시험/ፋይል_የስልክ_ጥሪዎች.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ፋይል_ምዝግብ for ፋይል_ምዝግብ in ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት if ፋይል_ምዝግብ != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት
        ፈጽም_ትእዛዝ([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', ግንብ_ዱካ / 출력결과])
    ፈጽም_ትእዛዝ([ከዝን_መሳሪያ, 'rcs', ግንብ_ዱካ / 'libposix-kor-arm64.a', ግንብ_ዱካ / 'posix.o'])
    ፈጽም_ትእዛዝ([연결편집기, '--gc-sections', '-T', አሳይ_ስር / '부팅/አገናኝ_አሰሳ.ld', '-Map', ግንብ_ዱካ / 'kernel.map', '-o', ግንብ_ዱካ / 'kernel.elf'] +
        [ግንብ_ዱካ / ስም for ስም in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', ግንብ_ዱካ / 'libposix-kor-arm64.a', መረብ, 원격사용, ግንብ_ዱካ / 'remote/libassh.a', ግንብ_ዱካ / 'remote/libbearssl.a', '--end-group'])
    ፈጽም_ትእዛዝ([ነገር_ፋይል_ለዋጭ, '-O', 'binary', ግንብ_ዱካ / 'kernel.elf', ግንብ_ዱካ / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'አማርኛ.자체', 'korean_exceptions': 20,
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
    for ስም in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][ስም] = hashlib.sha256((ግንብ_ዱካ / ስም).read_bytes()).hexdigest()
    (ግንብ_ዱካ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', ግንብ_ዱካ / 'kernel8.img')


if __name__ == '__main__':
    ማስኬጃ()
