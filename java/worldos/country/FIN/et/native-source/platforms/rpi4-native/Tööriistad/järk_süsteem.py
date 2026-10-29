#!/usr/bin/env python3
"""host javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from järk_kasutaja_ruum import avama_kasutaja_ruum
from järk_võrk import avama_võrk_48d29d6d
from 예제빌드 import 예제만들기
from järk_kauge import avama_kauge

Project_juur = Path(__file__).resolve().parents[1]
hoidla_juur = Project_juur.parents[1]
järk_tee = Project_juur / 'build'


def Täida_käsk(argument_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_ARRAY], cwd=str(Project_juur))


def Käivita_2():
    järk_tee.mkdir(exist_ok=True)
    _15_kompilaator = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objekt_Fail_muundur = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arhiiv_tööriist = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Tööriistad in ('javac', _15_kompilaator, 시플플번역기, 연결편집기, objekt_Fail_muundur, Arhiiv_tööriist):
        if not shutil.which(Tööriistad):
            raise SystemExit('필요한 järk_süsteem Tööriistad 없음: ' + Tööriistad)
    font_teave = json.loads((Project_juur / 'vendor/terminal-font.json').read_text())
    font_andmed = (Project_juur / 'vendor/terminal-font.bin').read_bytes()
    if len(font_andmed) != 65616 * 32 or hashlib.sha256(font_andmed).hexdigest() != font_teave['sha256']:
        raise SystemExit('terminal font_VALUE Suurus/SHA256 불일치')
    eksportima_tabel = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.Väljund', 'jshell_input': '셸입출력.입력', 'java_task': 'tuum.작업', 'jfs_path_start': 'Mälu_Failid.tee_START',
               'jfs_path_byte': 'Mälu_Failid.tee_bait', 'jfs_open': 'Mälu_Failid.Ava',
               'jfs_read': 'Mälu_Failid.Lugemine', 'jfs_write': 'Mälu_Failid.Kirjutamine',
               'jfs_seek': 'Mälu_Failid.otsima_ametikoht', 'jfs_close': 'Mälu_Failid.Suletud',
               'jfs_size': 'Mälu_Failid.Suurus', 'jfs_unlink': 'Mälu_Failid.kustutama_kirje',
               'jfs_truncate': 'Mälu_Failid.길이정하기'}
    eksportima_tabel.update({'jfs_entry_count': 'Mälu_Failid.파일한도', 'jfs_entry_length': 'Mälu_Failid.공개이름길이', 'jfs_entry_byte': 'Mälu_Failid.공개이름바이트', 'jfs_entry_size': 'Mälu_Failid.공개파일크기'})
    eksportima_tabel.update({'jdraw_prepare': '화면합성.Ettevalmistamine', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klipp',
        'jdraw_clip_value': '화면합성.klipp_VALUE', 'jdraw_begin': '화면합성.Käivita_2',
        'jdraw_end': '화면합성.lõpp', 'jdraw_pixel': '화면합성.piksel',
        'jdraw_rectangle': '화면합성.ristkülik_täide', 'jdraw_pointer': '화면합성.kursor'})
    eksportima_tabel.update({'jfs_mkdir': 'Mälu_Failid.avama_kaust', 'jfs_rmdir': 'Mälu_Failid.eemaldama_kaust', 'jfs_kind': 'Mälu_Failid.항목종류'})
    eksportima_tabel.update({'jnet_socket': 'tagastusliides_võrk.avama_kirje', 'jnet_bind': 'tagastusliides_võrk.BIND_osaleja',
        'jnet_put': 'tagastusliides_võrk.자료넣기', 'jnet_get': 'tagastusliides_võrk.자료읽기', 'jnet_send': 'tagastusliides_võrk.saatma',
        'jnet_recv': 'tagastusliides_võrk.saama', 'jnet_port': 'tagastusliides_võrk.창구읽기', 'jnet_address': 'tagastusliides_võrk.주소읽기',
        'jnet_peer': 'tagastusliides_võrk.saatja_osaleja', 'jnet_close': 'tagastusliides_võrk.Suletud'})
    eksportima_tabel.update({'jstream_create': 'voog_võrk.avama_kirje', 'jstream_bind': 'voog_võrk.BIND_osaleja', 'jstream_listen': 'voog_võrk.jälgima_osaleja', 'jstream_connect': 'voog_võrk.Ühendu', 'jstream_accept': 'voog_võrk.aktsepteerima_ühendus', 'jstream_read': 'voog_võrk.Lugemine', 'jstream_write': 'voog_võrk.Kirjutamine', 'jstream_port': 'voog_võrk.창구읽기', 'jstream_peer': 'voog_võrk.상대창구읽기', 'jstream_close': 'voog_võrk.Suletud'})
    for sümbol_VALUE in list(eksportima_tabel):
        if sümbol_VALUE.startswith('jstream_') or sümbol_VALUE.startswith('jnet_') and sümbol_VALUE not in ('jnet_put', 'jnet_get'):
            eksportima_tabel[sümbol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = eksportima_tabel.pop(sümbol_VALUE)
    예제들 = ['public final class kogum { public static void Ettevalmistamine() {']
    for RADA in sorted((Project_juur / '예제').iterdir()):
        if RADA.is_file():
            예제들.append('명령해석기.정적파일(%s, %s);' %
                (json.dumps(RADA.name), json.dumps(RADA.read_text(encoding='utf-8'), ensure_ascii=True)))
    (järk_tee / 'kogum.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_juur, hoidla_juur, Täida_käsk)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(järk_tee)) as 작업경로:
        tund_tee = Path(작업경로)
        Täida_käsk(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', tund_tee, '-sourcepath', tund_tee, '-d', tund_tee] + sorted((Project_juur / 'ALLIKAS').glob('*.java')) + [järk_tee / 'kogum.java', järk_tee / '예제꾸러미.java'])
        # Fail·kest·aken 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_ARRAY = ['sh', hoidla_juur / 'compiler/미리번역.sh', '--entry', 'tuum.Käivita_2', '--heap-words', '1048576', '-o', järk_tee / 'kernel-java.c']
        for sümbol_VALUE, meetod_kirje in sorted(eksportima_tabel.items()):
            argument_ARRAY += ['--export', sümbol_VALUE + '=' + meetod_kirje]
        Täida_käsk(argument_ARRAY + sorted(tund_tee.glob('*.class')))
    (järk_tee / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = hoidla_juur / 'posix-kor/arm64-native'
    avama_kasutaja_ruum(Project_juur, hoidla_juur, _15_kompilaator, 시플플번역기, 연결편집기, Arhiiv_tööriist, konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus, Täida_käsk)
    võrk = avama_võrk_48d29d6d(Project_juur, _15_kompilaator, Arhiiv_tööriist, konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus, Täida_käsk)
    kauge_kasutus = avama_kauge(Project_juur, _15_kompilaator, Arhiiv_tööriist, konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus, Täida_käsk)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', järk_tee]
    빌드작업 = [(_15_kompilaator, [], järk_tee / 'terminal-font.S', 'font.o'),
            (_15_kompilaator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_juur / 'arvuti/terminal.c', 'terminal.o'),
            (_15_kompilaator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_juur / 'arvuti/vidin.c', 'widgets.o'),
            (_15_kompilaator, ['-std=c11'], järk_tee / 'kernel-java.c', 'java.o'),
            (_15_kompilaator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_juur / 'arvuti/Tahvel.c', 'board.o'),
            (_15_kompilaator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_juur / 'arvuti/화면그림.c', 'drawing.o'),
            (_15_kompilaator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_juur / 'arvuti/kasutaja.c', 'user.o'),
            (_15_kompilaator, [], Project_juur / '부팅/kirje_p_VALUE.S', 'entry.o'),
            (_15_kompilaator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Ühendu.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_juur / '시험/Fail_Kõned.cpp', 'cpp.o')]
    for kompilaator_tööriist, 추가영역, 원본자료, toodang in 빌드작업:
        원본설정 = [Fail_kirje for Fail_kirje in konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus if Fail_kirje != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus
        Täida_käsk([kompilaator_tööriist] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', järk_tee / toodang])
    Täida_käsk([Arhiiv_tööriist, 'rcs', järk_tee / 'libposix-kor-arm64.a', järk_tee / 'posix.o'])
    Täida_käsk([연결편집기, '--gc-sections', '-T', Project_juur / '부팅/Link_küljend.ld', '-Map', järk_tee / 'kernel.map', '-o', järk_tee / 'kernel.elf'] +
        [järk_tee / Nimi_2 for Nimi_2 in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', järk_tee / 'libposix-kor-arm64.a', võrk, kauge_kasutus, järk_tee / 'remote/libassh.a', järk_tee / 'remote/libbearssl.a', '--end-group'])
    Täida_käsk([objekt_Fail_muundur, '-O', 'binary', järk_tee / 'kernel.elf', järk_tee / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Eesti.oma', 'korean_exceptions': 20,
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
    for Nimi_2 in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Nimi_2] = hashlib.sha256((järk_tee / Nimi_2).read_bytes()).hexdigest()
    (järk_tee / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', järk_tee / 'kernel8.img')


if __name__ == '__main__':
    Käivita_2()
