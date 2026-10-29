#!/usr/bin/env python3
"""હોસ્ટ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from બિલ્ડ_ઉપયોગકર્તા_જગ્યા import બનાવો_ઉપયોગકર્તા_જગ્યા
from બિલ્ડ_નેટવર્ક import બનાવો_નેટવર્ક_48d29d6d
from 예제빌드 import 예제만들기
from બિલ્ડ_રિમોટ import બનાવો_રિમોટ

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]
저장소 = પ્રોજેક્ટ_રૂટ.parents[1]
બિલ્ડ_પાથ = પ્રોજેક્ટ_રૂટ / 'build'


def અમલ_કરો_આદેશ(દલીલ_અરે):
    subprocess.check_call([str(첫째값) for 첫째값 in દલીલ_અરે], cwd=str(પ્રોજેક્ટ_રૂટ))


def ચલાવો_2():
    બિલ્ડ_પાથ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ઑબ્જેક્ટ_ફાઇલ_કન્વર્ટર = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    સંગ્રહ_ઉપકરણ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ઉપકરણો in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ઑબ્જેક્ટ_ફાઇલ_કન્વર્ટર, સંગ્રહ_ઉપકરણ):
        if not shutil.which(ઉપકરણો):
            raise SystemExit('필요한 બિલ્ડ_સિસ્ટમ ઉપકરણો 없음: ' + ઉપકરણો)
    ફૉન્ટ_માહિતી = json.loads((પ્રોજેક્ટ_રૂટ / 'vendor/terminal-font.json').read_text())
    ફૉન્ટ_ડેટા = (પ્રોજેક્ટ_રૂટ / 'vendor/terminal-font.bin').read_bytes()
    if len(ફૉન્ટ_ડેટા) != 65616 * 32 or hashlib.sha256(ફૉન્ટ_ડેટા).hexdigest() != ફૉન્ટ_માહિતી['sha256']:
        raise SystemExit('ટર્મિનલ ફૉન્ટ_મૂલ્ય માપ/SHA256 불일치')
    નિકાસ_કરો_કોષ્ટક = {'jshell_interactive': '셸입출력.ઇન્ટરમિટેંટ_સહભાગી', 'jshell_output': '셸입출력.આઉટપુટ', 'jshell_input': '셸입출력.입력', 'java_task': 'કર્નેલ.작업', 'jfs_path_start': 'મેમરી_ફાઇલો.પાથ_પ્રારંભ',
               'jfs_path_byte': 'મેમરી_ફાઇલો.પાથ_બાઇટ', 'jfs_open': 'મેમરી_ફાઇલો.ખોલો',
               'jfs_read': 'મેમરી_ફાઇલો.વાંચો', 'jfs_write': 'મેમરી_ફાઇલો.લખો',
               'jfs_seek': 'મેમરી_ફાઇલો.સીક_સ્થિતિ', 'jfs_close': 'મેમરી_ફાઇલો.બંધ_કરો',
               'jfs_size': 'મેમરી_ફાઇલો.માપ', 'jfs_unlink': 'મેમરી_ફાઇલો.지우기',
               'jfs_truncate': 'મેમરી_ફાઇલો.સેટ_લંબાઈ'}
    નિકાસ_કરો_કોષ્ટક.update({'jfs_entry_count': 'મેમરી_ફાઇલો.파일한도', 'jfs_entry_length': 'મેમરી_ફાઇલો.공개이름길이', 'jfs_entry_byte': 'મેમરી_ફાઇલો.공개이름바이트', 'jfs_entry_size': 'મેમરી_ફાઇલો.공개파일크기'})
    નિકાસ_કરો_કોષ્ટક.update({'jdraw_prepare': '화면합성.તૈયાર_કરો', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ક્લિપ',
        'jdraw_clip_value': '화면합성.ક્લિપ_મૂલ્ય', 'jdraw_begin': '화면합성.ચલાવો_2',
        'jdraw_end': '화면합성.સમાપ્ત_કરો', 'jdraw_pixel': '화면합성.પેલ',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.સૂચક'})
    નિકાસ_કરો_કોષ્ટક.update({'jfs_mkdir': 'મેમરી_ફાઇલો.બનાવો_નિર્દેશિકા', 'jfs_rmdir': 'મેમરી_ફાઇલો.કાઢી_નાંખો_નિર્દેશિકા', 'jfs_kind': 'મેમરી_ફાઇલો.항목종류'})
    નિકાસ_કરો_કોષ્ટક.update({'jnet_socket': '되돌림망.બનાવો_પ્રવેશ', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.મોકલો',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.બંધ_કરો'})
    નિકાસ_કરો_કોષ્ટક.update({'jstream_create': 'સ્ટ્રીમ_નેટવર્ક.બનાવો_પ્રવેશ', 'jstream_bind': 'સ્ટ્રીમ_નેટવર્ક.묶기', 'jstream_listen': 'સ્ટ્રીમ_નેટવર્ક.듣기', 'jstream_connect': 'સ્ટ્રીમ_નેટવર્ક.સંપર્ક_કરો', 'jstream_accept': 'સ્ટ્રીમ_નેટવર્ક.સ્વીકારો_કનેક્શન', 'jstream_read': 'સ્ટ્રીમ_નેટવર્ક.વાંચો', 'jstream_write': 'સ્ટ્રીમ_નેટવર્ક.લખો', 'jstream_port': 'સ્ટ્રીમ_નેટવર્ક.창구읽기', 'jstream_peer': 'સ્ટ્રીમ_નેટવર્ક.상대창구읽기', 'jstream_close': 'સ્ટ્રીમ_નેટવર્ક.બંધ_કરો'})
    for પ્રતીક_મૂલ્ય in list(નિકાસ_કરો_કોષ્ટક):
        if પ્રતીક_મૂલ્ય.startswith('jstream_') or પ્રતીક_મૂલ્ય.startswith('jnet_') and પ્રતીક_મૂલ્ય not in ('jnet_put', 'jnet_get'):
            નિકાસ_કરો_કોષ્ટક[પ્રતીક_મૂલ્ય.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = નિકાસ_કરો_કોષ્ટક.pop(પ્રતીક_મૂલ્ય)
    예제들 = ['public final class બન્ડલ { public static void તૈયાર_કરો() {']
    for પથ in sorted((પ્રોજેક્ટ_રૂટ / '예제').iterdir()):
        if પથ.is_file():
            예제들.append('명령해석기.સ્થિર_ફાઇલ(%s, %s);' %
                (json.dumps(પથ.name), json.dumps(પથ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (બિલ્ડ_પાથ / 'બન્ડલ.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(પ્રોજેક્ટ_રૂટ, 저장소, અમલ_કરો_આદેશ)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(બિલ્ડ_પાથ)) as 작업경로:
        વર્ગ_પાથ = Path(작업경로)
        અમલ_કરો_આદેશ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', વર્ગ_પાથ, '-sourcepath', વર્ગ_પાથ, '-d', વર્ગ_પાથ] + sorted((પ્રોજેક્ટ_રૂટ / 'સ્રોત').glob('*.java')) + [બિલ્ડ_પાથ / 'બન્ડલ.java', બિલ્ડ_પાથ / '예제꾸러미.java'])
        # ફાઈલ·શેલ·વિંડો 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        દલીલ_અરે = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'કર્નેલ.ચલાવો_2', '--heap-words', '1048576', '-o', બિલ્ડ_પાથ / 'kernel-java.c']
        for પ્રતીક_મૂલ્ય, પદ્ધતિ_પ્રવેશ in sorted(નિકાસ_કરો_કોષ્ટક.items()):
            દલીલ_અરે += ['--export', પ્રતીક_મૂલ્ય + '=' + પદ્ધતિ_પ્રવેશ]
        અમલ_કરો_આદેશ(દલીલ_અરે + sorted(વર્ગ_પાથ.glob('*.class')))
    (બિલ્ડ_પાથ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    બનાવો_ઉપયોગકર્તા_જગ્યા(પ્રોજેક્ટ_રૂટ, 저장소, 시언어번역기, 시플플번역기, 연결편집기, સંગ્રહ_ઉપકરણ, 설정비트, અમલ_કરો_આદેશ)
    નેટવર્ક = બનાવો_નેટવર્ક_48d29d6d(પ્રોજેક્ટ_રૂટ, 시언어번역기, સંગ્રહ_ઉપકરણ, 설정비트, અમલ_કરો_આદેશ)
    원격사용 = બનાવો_રિમોટ(પ્રોજેક્ટ_રૂટ, 시언어번역기, સંગ્રહ_ઉપકરણ, 설정비트, અમલ_કરો_આદેશ)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', બિલ્ડ_પાથ]
    빌드작업 = [(시언어번역기, [], બિલ્ડ_પાથ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], પ્રોજેક્ટ_રૂટ / 'મશીન/ટર્મિનલ.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], પ્રોજેક્ટ_રૂટ / 'મશીન/વિજેટ.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], બિલ્ડ_પાથ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], પ્રોજેક્ટ_રૂટ / 'મશીન/બોર્ડ.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], પ્રોજેક્ટ_રૂટ / 'મશીન/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], પ્રોજેક્ટ_રૂટ / 'મશીન/ઉપયોગકર્તા.c', 'user.o'),
            (시언어번역기, [], પ્રોજેક્ટ_રૂટ / '부팅/પ્રવેશ_બિંદુ_મૂલ્ય.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'સંપર્ક_કરો.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], પ્રોજેક્ટ_રૂટ / '시험/ફાઇલ_કૉલ્સ.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ફાઇલ_પ્રવેશ for ફાઇલ_પ્રવેશ in 설정비트 if ફાઇલ_પ્રવેશ != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        અમલ_કરો_આદેશ([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', બિલ્ડ_પાથ / 출력결과])
    અમલ_કરો_આદેશ([સંગ્રહ_ઉપકરણ, 'rcs', બિલ્ડ_પાથ / 'libposix-kor-arm64.a', બિલ્ડ_પાથ / 'posix.o'])
    અમલ_કરો_આદેશ([연결편집기, '--gc-sections', '-T', પ્રોજેક્ટ_રૂટ / '부팅/લિંક_લેઆઉટ.ld', '-Map', બિલ્ડ_પાથ / 'kernel.map', '-o', બિલ્ડ_પાથ / 'kernel.elf'] +
        [બિલ્ડ_પાથ / નામ for નામ in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', બિલ્ડ_પાથ / 'libposix-kor-arm64.a', નેટવર્ક, 원격사용, બિલ્ડ_પાથ / 'remote/libassh.a', બિલ્ડ_પાથ / 'remote/libbearssl.a', '--end-group'])
    અમલ_કરો_આદેશ([ઑબ્જેક્ટ_ફાઇલ_કન્વર્ટર, '-O', 'binary', બિલ્ડ_પાથ / 'kernel.elf', બિલ્ડ_પાથ / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'ગુજરાતી.자체', 'korean_exceptions': 20,
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
    for નામ in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][નામ] = hashlib.sha256((બિલ્ડ_પાથ / નામ).read_bytes()).hexdigest()
    (બિલ્ડ_પાથ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', બિલ્ડ_પાથ / 'kernel8.img')


if __name__ == '__main__':
    ચલાવો_2()
