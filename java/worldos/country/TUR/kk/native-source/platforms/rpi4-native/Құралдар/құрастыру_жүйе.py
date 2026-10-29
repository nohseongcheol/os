#!/usr/bin/env python3
"""орналастыру javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from құрастыру_пайдаланушы_орын import жасау_пайдаланушы_орын
from құрастыру_желі import жасау_желі
from 예제빌드 import 예제만들기
from 원격빌드 import 원격만들기

жоба_түбір = Path(__file__).resolve().parents[1]
репозиторий_түбір = жоба_түбір.parents[1]
құрастыру_жол = жоба_түбір / 'build'


def орындау_пәрмен(аргумент_массив):
    subprocess.check_call([str(첫째값) for 첫째값 in аргумент_массив], cwd=str(жоба_түбір))


def Орындау_2():
    құрастыру_жол.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    нысан_файл_түрлендіргіш = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Мұрағат_құрал = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Құралдар in ('javac', 시언어번역기, 시플플번역기, 연결편집기, нысан_файл_түрлендіргіш, Мұрағат_құрал):
        if not shutil.which(Құралдар):
            raise SystemExit('필요한 құрастыру_жүйе Құралдар 없음: ' + Құралдар)
    қаріп_ақпарат = json.loads((жоба_түбір / 'vendor/terminal-font.json').read_text())
    қаріп_деректер = (жоба_түбір / 'vendor/terminal-font.bin').read_bytes()
    if len(қаріп_деректер) != 65616 * 32 or hashlib.sha256(қаріп_деректер).hexdigest() != қаріп_ақпарат['sha256']:
        raise SystemExit('Терминал қаріп_мән Өлшемі/SHA256 불일치')
    экспорттау_кесте = {'jshell_interactive': '셸입출력.ақпараттық_жүйелер_көзбе_көз_белсенді', 'jshell_output': '셸입출력.Шығысы', 'jshell_input': '셸입출력.입력', 'java_task': 'ядро.작업', 'jfs_path_start': 'Жад_Файлдар.жол_басы',
               'jfs_path_byte': 'Жад_Файлдар.жол_байт', 'jfs_open': 'Жад_Файлдар.Ашу',
               'jfs_read': 'Жад_Файлдар.Оқу', 'jfs_write': 'Жад_Файлдар.Жазу',
               'jfs_seek': 'Жад_Файлдар.іздеу_лауазым', 'jfs_close': 'Жад_Файлдар.Жабу',
               'jfs_size': 'Жад_Файлдар.Өлшемі', 'jfs_unlink': 'Жад_Файлдар.өшіру_енгізу',
               'jfs_truncate': 'Жад_Файлдар.жинақ_ұзындық'}
    экспорттау_кесте.update({'jfs_entry_count': 'Жад_Файлдар.파일한도', 'jfs_entry_length': 'Жад_Файлдар.공개이름길이', 'jfs_entry_byte': 'Жад_Файлдар.공개이름바이트', 'jfs_entry_size': 'Жад_Файлдар.공개파일크기'})
    экспорттау_кесте.update({'jdraw_prepare': '화면합성.Дайындау', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.клип',
        'jdraw_clip_value': '화면합성.клип_мән', 'jdraw_begin': '화면합성.Орындау_2',
        'jdraw_end': '화면합성.соңы', 'jdraw_pixel': '화면합성.нүкте',
        'jdraw_rectangle': '화면합성.тік_төртбұрыш_бояу', 'jdraw_pointer': '화면합성.меңзер'})
    экспорттау_кесте.update({'jfs_mkdir': 'Жад_Файлдар.жасау_каталог', 'jfs_rmdir': 'Жад_Файлдар.жою_каталог', 'jfs_kind': 'Жад_Файлдар.항목종류'})
    экспорттау_кесте.update({'jnet_socket': '되돌림망.жасау_енгізу', 'jnet_bind': '되돌림망.байланыстыру_қатысушы',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.жіберу',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.жіберуші_қатысушы', 'jnet_close': '되돌림망.Жабу'})
    экспорттау_кесте.update({'jstream_create': 'ағым_желі.жасау_енгізу', 'jstream_bind': 'ағым_желі.байланыстыру_қатысушы', 'jstream_listen': 'ағым_желі.деректердің_берілуін_күту_қатысушы', 'jstream_connect': 'ағым_желі.Байланысу', 'jstream_accept': 'ағым_желі.қабылдау_қосылым', 'jstream_read': 'ағым_желі.Оқу', 'jstream_write': 'ағым_желі.Жазу', 'jstream_port': 'ағым_желі.창구읽기', 'jstream_peer': 'ағым_желі.상대창구읽기', 'jstream_close': 'ағым_желі.Жабу'})
    for символ_мән in list(экспорттау_кесте):
        if символ_мән.startswith('jstream_') or символ_мән.startswith('jnet_') and символ_мән not in ('jnet_put', 'jnet_get'):
            экспорттау_кесте[символ_мән.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = экспорттау_кесте.pop(символ_мән)
    예제들 = ['public final class жинау { public static void Дайындау() {']
    for Жол_2 in sorted((жоба_түбір / '예제').iterdir()):
        if Жол_2.is_file():
            예제들.append('명령해석기.тұрақты_файл(%s, %s);' %
                (json.dumps(Жол_2.name), json.dumps(Жол_2.read_text(encoding='utf-8'), ensure_ascii=True)))
    (құрастыру_жол / 'жинау.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(жоба_түбір, репозиторий_түбір, орындау_пәрмен)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(құрастыру_жол)) as 작업경로:
        оқу_жол = Path(작업경로)
        орындау_пәрмен(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', оқу_жол, '-sourcepath', оқу_жол, '-d', оқу_жол] + sorted((жоба_түбір / 'Неден').glob('*.java')) + [құрастыру_жол / 'жинау.java', құрастыру_жол / '예제꾸러미.java'])
        # Файл·қоршам·Терезе 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        аргумент_массив = ['sh', репозиторий_түбір / 'compiler/미리번역.sh', '--entry', 'ядро.Орындау_2', '--heap-words', '1048576', '-o', құрастыру_жол / 'kernel-java.c']
        for символ_мән, әдіс_енгізу in sorted(экспорттау_кесте.items()):
            аргумент_массив += ['--export', символ_мән + '=' + әдіс_енгізу]
        орындау_пәрмен(аргумент_массив + sorted(оқу_жол.glob('*.class')))
    (құрастыру_жол / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = репозиторий_түбір / 'posix-kor/arm64-native'
    жасау_пайдаланушы_орын(жоба_түбір, репозиторий_түбір, 시언어번역기, 시플플번역기, 연결편집기, Мұрағат_құрал, конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі, орындау_пәрмен)
    желі = жасау_желі(жоба_түбір, 시언어번역기, Мұрағат_құрал, конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі, орындау_пәрмен)
    원격사용 = 원격만들기(жоба_түбір, 시언어번역기, Мұрағат_құрал, конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі, орындау_пәрмен)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', құрастыру_жол]
    빌드작업 = [(시언어번역기, [], құрастыру_жол / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], жоба_түбір / 'компьютер/Терминал.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], жоба_түбір / 'компьютер/виджет.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], құрастыру_жол / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], жоба_түбір / 'компьютер/Тақта.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], жоба_түбір / 'компьютер/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], жоба_түбір / 'компьютер/пайдаланушы.c', 'user.o'),
            (시언어번역기, [], жоба_түбір / '부팅/енгізу_ұпай_мән.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Байланысу.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], жоба_түбір / '시험/файл_Қоңыраулар.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [файл_енгізу for файл_енгізу in конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі if файл_енгізу != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі
        орындау_пәрмен([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', құрастыру_жол / 출력결과])
    орындау_пәрмен([Мұрағат_құрал, 'rcs', құрастыру_жол / 'libposix-kor-arm64.a', құрастыру_жол / 'posix.o'])
    орындау_пәрмен([연결편집기, '--gc-sections', '-T', жоба_түбір / '부팅/Cілтеме_макет.ld', '-Map', құрастыру_жол / 'kernel.map', '-o', құрастыру_жол / 'kernel.elf'] +
        [құрастыру_жол / Аты for Аты in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', құрастыру_жол / 'libposix-kor-arm64.a', желі, 원격사용, құрастыру_жол / 'remote/libassh.a', құрастыру_жол / 'remote/libbearssl.a', '--end-group'])
    орындау_пәрмен([нысан_файл_түрлендіргіш, '-O', 'binary', құрастыру_жол / 'kernel.elf', құрастыру_жол / 'kernel8.img'])
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
    for Аты in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Аты] = hashlib.sha256((құрастыру_жол / Аты).read_bytes()).hexdigest()
    (құрастыру_жол / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', құрастыру_жол / 'kernel8.img')


if __name__ == '__main__':
    Орындау_2()
