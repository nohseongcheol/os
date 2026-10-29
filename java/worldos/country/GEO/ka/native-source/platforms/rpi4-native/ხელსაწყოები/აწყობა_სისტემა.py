#!/usr/bin/env python3
"""მასპინძელი javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from აწყობა_მომხმარებელი_სივრცე import შექმნა_მომხმარებელი_სივრცე
from აწყობა_ქსელი import შექმნა_ქსელი
from 예제빌드 import 예제만들기
from აწყობა_დისტანციური import შექმნა_დისტანციური

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]
저장소 = პროეცირება_ფესვი.parents[1]
აწყობა_მდებარეობა = პროეცირება_ფესვი / 'build'


def შესრულება_ბრძანება(არგუმენტი_მასივი):
    subprocess.check_call([str(첫째값) for 첫째값 in არგუმენტი_მასივი], cwd=str(პროეცირება_ფესვი))


def გაშვება():
    აწყობა_მდებარეობა.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ობიექტი_ფაილი_გარდამქმნელი = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    არქივი_ხელსაწყო = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ხელსაწყოები in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ობიექტი_ფაილი_გარდამქმნელი, არქივი_ხელსაწყო):
        if not shutil.which(ხელსაწყოები):
            raise SystemExit('필요한 აწყობა_სისტემა ხელსაწყოები 없음: ' + ხელსაწყოები)
    შრიფტი_ინფო = json.loads((პროეცირება_ფესვი / 'vendor/terminal-font.json').read_text())
    შრიფტი_მონაცემები = (პროეცირება_ფესვი / 'vendor/terminal-font.bin').read_bytes()
    if len(შრიფტი_მონაცემები) != 65616 * 32 or hashlib.sha256(შრიფტი_მონაცემები).hexdigest() != შრიფტი_ინფო['sha256']:
        raise SystemExit('ტერმინალი შრიფტი_მნიშვნელობა ზომა/SHA256 불일치')
    ექსპორტი_ცხრილი = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'ბირთვი.작업', 'jfs_path_start': 'მეხსიერება_ფაილები.მდებარეობა_დაწყება',
               'jfs_path_byte': 'მეხსიერება_ფაილები.მდებარეობა_ბაიტი', 'jfs_open': 'მეხსიერება_ფაილები.გახსნა',
               'jfs_read': 'მეხსიერება_ფაილები.კითხვა', 'jfs_write': 'მეხსიერება_ფაილები.ჩაწერა',
               'jfs_seek': 'მეხსიერება_ფაილები.ძებნა_პოზიცია', 'jfs_close': 'მეხსიერება_ფაილები.დახურვა',
               'jfs_size': 'მეხსიერება_ფაილები.ზომა', 'jfs_unlink': 'მეხსიერება_ფაილები.지우기',
               'jfs_truncate': 'მეხსიერება_ფაილები.ნაკრები_სიგრძე'}
    ექსპორტი_ცხრილი.update({'jfs_entry_count': 'მეხსიერება_ფაილები.파일한도', 'jfs_entry_length': 'მეხსიერება_ფაილები.공개이름길이', 'jfs_entry_byte': 'მეხსიერება_ფაილები.공개이름바이트', 'jfs_entry_size': 'მეხსიერება_ფაილები.공개파일크기'})
    ექსპორტი_ცხრილი.update({'jdraw_prepare': '화면합성.მომზადება', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.კლიპი',
        'jdraw_clip_value': '화면합성.კლიპი_მნიშვნელობა', 'jdraw_begin': '화면합성.გაშვება',
        'jdraw_end': '화면합성.დასრულება', 'jdraw_pixel': '화면합성.პიქსელი',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.კურსორი'})
    ექსპორტი_ცხრილი.update({'jfs_mkdir': 'მეხსიერება_ფაილები.შექმნა_საქაღალდე', 'jfs_rmdir': 'მეხსიერება_ფაილები.ამოშლა_საქაღალდე', 'jfs_kind': 'მეხსიერება_ფაილები.항목종류'})
    ექსპორტი_ცხრილი.update({'jnet_socket': '되돌림망.შექმნა_შენატანი', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.გაგზავნა',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.დახურვა'})
    ექსპორტი_ცხრილი.update({'jstream_create': 'ნაკადი_ქსელი.შექმნა_შენატანი', 'jstream_bind': 'ნაკადი_ქსელი.묶기', 'jstream_listen': 'ნაკადი_ქსელი.듣기', 'jstream_connect': 'ნაკადი_ქსელი.დაკავშირება', 'jstream_accept': 'ნაკადი_ქსელი.მიღება_კავშირი', 'jstream_read': 'ნაკადი_ქსელი.კითხვა', 'jstream_write': 'ნაკადი_ქსელი.ჩაწერა', 'jstream_port': 'ნაკადი_ქსელი.창구읽기', 'jstream_peer': 'ნაკადი_ქსელი.상대창구읽기', 'jstream_close': 'ნაკადი_ქსელი.დახურვა'})
    for სიმბოლო_მნიშვნელობა in list(ექსპორტი_ცხრილი):
        if სიმბოლო_მნიშვნელობა.startswith('jstream_') or სიმბოლო_მნიშვნელობა.startswith('jnet_') and სიმბოლო_მნიშვნელობა not in ('jnet_put', 'jnet_get'):
            ექსპორტი_ცხრილი[სიმბოლო_მნიშვნელობა.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ექსპორტი_ცხრილი.pop(სიმბოლო_მნიშვნელობა)
    예제들 = ['public final class შეკვრა { public static void მომზადება() {']
    for გეზი in sorted((პროეცირება_ფესვი / '예제').iterdir()):
        if გეზი.is_file():
            예제들.append('명령해석기.სტატიკური_ფაილი(%s, %s);' %
                (json.dumps(გეზი.name), json.dumps(გეზი.read_text(encoding='utf-8'), ensure_ascii=True)))
    (აწყობა_მდებარეობა / 'შეკვრა.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(პროეცირება_ფესვი, 저장소, შესრულება_ბრძანება)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(აწყობა_მდებარეობა)) as 작업경로:
        კლასი_მდებარეობა = Path(작업경로)
        შესრულება_ბრძანება(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', კლასი_მდებარეობა, '-sourcepath', კლასი_მდებარეობა, '-d', კლასი_მდებარეობა] + sorted((პროეცირება_ფესვი / 'წყარო').glob('*.java')) + [აწყობა_მდებარეობა / 'შეკვრა.java', აწყობა_მდებარეობა / '예제꾸러미.java'])
        # ფაილი·გარემო·ფანჯარა 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        არგუმენტი_მასივი = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'ბირთვი.გაშვება', '--heap-words', '1048576', '-o', აწყობა_მდებარეობა / 'kernel-java.c']
        for სიმბოლო_მნიშვნელობა, მეთოდი_შენატანი in sorted(ექსპორტი_ცხრილი.items()):
            არგუმენტი_მასივი += ['--export', სიმბოლო_მნიშვნელობა + '=' + მეთოდი_შენატანი]
        შესრულება_ბრძანება(არგუმენტი_მასივი + sorted(კლასი_მდებარეობა.glob('*.class')))
    (აწყობა_მდებარეობა / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    შექმნა_მომხმარებელი_სივრცე(პროეცირება_ფესვი, 저장소, 시언어번역기, 시플플번역기, 연결편집기, არქივი_ხელსაწყო, 설정비트, შესრულება_ბრძანება)
    ქსელი = შექმნა_ქსელი(პროეცირება_ფესვი, 시언어번역기, არქივი_ხელსაწყო, 설정비트, შესრულება_ბრძანება)
    원격사용 = შექმნა_დისტანციური(პროეცირება_ფესვი, 시언어번역기, არქივი_ხელსაწყო, 설정비트, შესრულება_ბრძანება)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', აწყობა_მდებარეობა]
    빌드작업 = [(시언어번역기, [], აწყობა_მდებარეობა / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], პროეცირება_ფესვი / 'კომპიუტერი/ტერმინალი.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], პროეცირება_ფესვი / 'კომპიუტერი/ვიჯეტი.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], აწყობა_მდებარეობა / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], პროეცირება_ფესვი / 'კომპიუტერი/დაფა.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], პროეცირება_ფესვი / 'კომპიუტერი/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], პროეცირება_ფესვი / 'კომპიუტერი/მომხმარებელი.c', 'user.o'),
            (시언어번역기, [], პროეცირება_ფესვი / '부팅/შენატანი_პტ_მნიშვნელობა.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'დაკავშირება.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], პროეცირება_ფესვი / '시험/ფაილი_ზარები.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ფაილი_შენატანი for ფაილი_შენატანი in 설정비트 if ფაილი_შენატანი != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        შესრულება_ბრძანება([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', აწყობა_მდებარეობა / 출력결과])
    შესრულება_ბრძანება([არქივი_ხელსაწყო, 'rcs', აწყობა_მდებარეობა / 'libposix-kor-arm64.a', აწყობა_მდებარეობა / 'posix.o'])
    შესრულება_ბრძანება([연결편집기, '--gc-sections', '-T', პროეცირება_ფესვი / '부팅/ბმული_განლაგება.ld', '-Map', აწყობა_მდებარეობა / 'kernel.map', '-o', აწყობა_მდებარეობა / 'kernel.elf'] +
        [აწყობა_მდებარეობა / სახელი for სახელი in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', აწყობა_მდებარეობა / 'libposix-kor-arm64.a', ქსელი, 원격사용, აწყობა_მდებარეობა / 'remote/libassh.a', აწყობა_მდებარეობა / 'remote/libbearssl.a', '--end-group'])
    შესრულება_ბრძანება([ობიექტი_ფაილი_გარდამქმნელი, '-O', 'binary', აწყობა_მდებარეობა / 'kernel.elf', აწყობა_მდებარეობა / 'kernel8.img'])
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
    for სახელი in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][სახელი] = hashlib.sha256((აწყობა_მდებარეობა / სახელი).read_bytes()).hexdigest()
    (აწყობა_მდებარეობა / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', აწყობა_მდებარეობა / 'kernel8.img')


if __name__ == '__main__':
    გაშვება()
