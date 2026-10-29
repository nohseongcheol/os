#!/usr/bin/env python3
"""viesot javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from būvējums_lietotājs_telpa import atvērt_lietotājs_telpa
from būvējums_tīkls import atvērt_tīkls_48d29d6d
from 예제빌드 import 예제만들기
from būvējums_attāls import atvērt_attāls

Project_sakne = Path(__file__).resolve().parents[1]
repozitorijs_sakne = Project_sakne.parents[1]
būvējums_ceļš = Project_sakne / 'build'


def Izpildīt_komanda(arg_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in arg_ARRAY], cwd=str(Project_sakne))


def Palaist():
    būvējums_ceļš.mkdir(exist_ok=True)
    C_kompilators = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objekts_Fails_pārveidotājs = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arhīvs_rīks = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Rīki in ('javac', C_kompilators, 시플플번역기, 연결편집기, objekts_Fails_pārveidotājs, Arhīvs_rīks):
        if not shutil.which(Rīki):
            raise SystemExit('필요한 būvējums_sistēma Rīki 없음: ' + Rīki)
    fonts_informācija = json.loads((Project_sakne / 'vendor/terminal-font.json').read_text())
    fonts_dati = (Project_sakne / 'vendor/terminal-font.bin').read_bytes()
    if len(fonts_dati) != 65616 * 32 or hashlib.sha256(fonts_dati).hexdigest() != fonts_informācija['sha256']:
        raise SystemExit('Terminālis fonts_VALUE Izmērs/SHA256 불일치')
    eksportēt_tabula = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.Izvade', 'jshell_input': '셸입출력.입력', 'java_task': 'kodols.작업', 'jfs_path_start': 'atmiņa_Faili.ceļš_Sākt',
               'jfs_path_byte': 'atmiņa_Faili.ceļš_byte', 'jfs_open': 'atmiņa_Faili.Atvērt',
               'jfs_read': 'atmiņa_Faili.Lasīt', 'jfs_write': 'atmiņa_Faili.Rakstīt',
               'jfs_seek': 'atmiņa_Faili.meklēt_amats', 'jfs_close': 'atmiņa_Faili.Aizvērt',
               'jfs_size': 'atmiņa_Faili.Izmērs', 'jfs_unlink': 'atmiņa_Faili.dzēst_ievade',
               'jfs_truncate': 'atmiņa_Faili.길이정하기'}
    eksportēt_tabula.update({'jfs_entry_count': 'atmiņa_Faili.파일한도', 'jfs_entry_length': 'atmiņa_Faili.공개이름길이', 'jfs_entry_byte': 'atmiņa_Faili.공개이름바이트', 'jfs_entry_size': 'atmiņa_Faili.공개파일크기'})
    eksportēt_tabula.update({'jdraw_prepare': '화면합성.Sagatavot', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klips',
        'jdraw_clip_value': '화면합성.klips_VALUE', 'jdraw_begin': '화면합성.Palaist',
        'jdraw_end': '화면합성.beigas', 'jdraw_pixel': '화면합성.attēla_elements',
        'jdraw_rectangle': '화면합성.taisnstūris_aizpildīt', 'jdraw_pointer': '화면합성.rādītājs'})
    eksportēt_tabula.update({'jfs_mkdir': 'atmiņa_Faili.atvērt_Direktorijs', 'jfs_rmdir': 'atmiņa_Faili.noņemt_Direktorijs', 'jfs_kind': 'atmiņa_Faili.항목종류'})
    eksportēt_tabula.update({'jnet_socket': 'atgriezeniskā_cilpa_tīkls.atvērt_ievade', 'jnet_bind': 'atgriezeniskā_cilpa_tīkls.BIND_dalībnieks',
        'jnet_put': 'atgriezeniskā_cilpa_tīkls.자료넣기', 'jnet_get': 'atgriezeniskā_cilpa_tīkls.자료읽기', 'jnet_send': 'atgriezeniskā_cilpa_tīkls.sūtīt',
        'jnet_recv': 'atgriezeniskā_cilpa_tīkls.saņemt', 'jnet_port': 'atgriezeniskā_cilpa_tīkls.창구읽기', 'jnet_address': 'atgriezeniskā_cilpa_tīkls.주소읽기',
        'jnet_peer': 'atgriezeniskā_cilpa_tīkls.sūtītājs_dalībnieks', 'jnet_close': 'atgriezeniskā_cilpa_tīkls.Aizvērt'})
    eksportēt_tabula.update({'jstream_create': 'Stream_tīkls.atvērt_ievade', 'jstream_bind': 'Stream_tīkls.BIND_dalībnieks', 'jstream_listen': 'Stream_tīkls.klausīties_dalībnieks', 'jstream_connect': 'Stream_tīkls.Savienoties', 'jstream_accept': 'Stream_tīkls.akceptēt_paziņa', 'jstream_read': 'Stream_tīkls.Lasīt', 'jstream_write': 'Stream_tīkls.Rakstīt', 'jstream_port': 'Stream_tīkls.창구읽기', 'jstream_peer': 'Stream_tīkls.상대창구읽기', 'jstream_close': 'Stream_tīkls.Aizvērt'})
    for simbols_VALUE in list(eksportēt_tabula):
        if simbols_VALUE.startswith('jstream_') or simbols_VALUE.startswith('jnet_') and simbols_VALUE not in ('jnet_put', 'jnet_get'):
            eksportēt_tabula[simbols_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = eksportēt_tabula.pop(simbols_VALUE)
    예제들 = ['public final class saistīt { public static void Sagatavot() {']
    for CEĻŠ in sorted((Project_sakne / '예제').iterdir()):
        if CEĻŠ.is_file():
            예제들.append('명령해석기.정적파일(%s, %s);' %
                (json.dumps(CEĻŠ.name), json.dumps(CEĻŠ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (būvējums_ceļš / 'saistīt.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_sakne, repozitorijs_sakne, Izpildīt_komanda)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(būvējums_ceļš)) as 작업경로:
        klase_ceļš = Path(작업경로)
        Izpildīt_komanda(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klase_ceļš, '-sourcepath', klase_ceļš, '-d', klase_ceļš] + sorted((Project_sakne / 'AVOTS').glob('*.java')) + [būvējums_ceļš / 'saistīt.java', būvējums_ceļš / '예제꾸러미.java'])
        # Fails·čaula·Logs 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        arg_ARRAY = ['sh', repozitorijs_sakne / 'compiler/미리번역.sh', '--entry', 'kodols.Palaist', '--heap-words', '1048576', '-o', būvējums_ceļš / 'kernel-java.c']
        for simbols_VALUE, metode_ievade in sorted(eksportēt_tabula.items()):
            arg_ARRAY += ['--export', simbols_VALUE + '=' + metode_ievade]
        Izpildīt_komanda(arg_ARRAY + sorted(klase_ceļš.glob('*.class')))
    (būvējums_ceļš / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfigurācija_Background_Intelligent_Transfer_Service = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = repozitorijs_sakne / 'posix-kor/arm64-native'
    atvērt_lietotājs_telpa(Project_sakne, repozitorijs_sakne, C_kompilators, 시플플번역기, 연결편집기, Arhīvs_rīks, konfigurācija_Background_Intelligent_Transfer_Service, Izpildīt_komanda)
    tīkls = atvērt_tīkls_48d29d6d(Project_sakne, C_kompilators, Arhīvs_rīks, konfigurācija_Background_Intelligent_Transfer_Service, Izpildīt_komanda)
    attāls_lietot = atvērt_attāls(Project_sakne, C_kompilators, Arhīvs_rīks, konfigurācija_Background_Intelligent_Transfer_Service, Izpildīt_komanda)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', būvējums_ceļš]
    빌드작업 = [(C_kompilators, [], būvējums_ceļš / 'terminal-font.S', 'font.o'),
            (C_kompilators, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_sakne / 'mašīna/Terminālis.c', 'terminal.o'),
            (C_kompilators, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_sakne / 'mašīna/logrīks.c', 'widgets.o'),
            (C_kompilators, ['-std=c11'], būvējums_ceļš / 'kernel-java.c', 'java.o'),
            (C_kompilators, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_sakne / 'mašīna/Panelis.c', 'board.o'),
            (C_kompilators, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_sakne / 'mašīna/화면그림.c', 'drawing.o'),
            (C_kompilators, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_sakne / 'mašīna/lietotājs.c', 'user.o'),
            (C_kompilators, [], Project_sakne / '부팅/ieejas_punkts_VALUE.S', 'entry.o'),
            (C_kompilators, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Savienoties.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_sakne / '시험/Fails_Zvani.cpp', 'cpp.o')]
    for kompilators_rīks, 추가영역, 원본자료, ražojums in 빌드작업:
        원본설정 = [Fails_ievade for Fails_ievade in konfigurācija_Background_Intelligent_Transfer_Service if Fails_ievade != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfigurācija_Background_Intelligent_Transfer_Service
        Izpildīt_komanda([kompilators_rīks] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', būvējums_ceļš / ražojums])
    Izpildīt_komanda([Arhīvs_rīks, 'rcs', būvējums_ceļš / 'libposix-kor-arm64.a', būvējums_ceļš / 'posix.o'])
    Izpildīt_komanda([연결편집기, '--gc-sections', '-T', Project_sakne / '부팅/Saite_shēma.ld', '-Map', būvējums_ceļš / 'kernel.map', '-o', būvējums_ceļš / 'kernel.elf'] +
        [būvējums_ceļš / Nosaukums for Nosaukums in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', būvējums_ceļš / 'libposix-kor-arm64.a', tīkls, attāls_lietot, būvējums_ceļš / 'remote/libassh.a', būvējums_ceļš / 'remote/libbearssl.a', '--end-group'])
    Izpildīt_komanda([objekts_Fails_pārveidotājs, '-O', 'binary', būvējums_ceļš / 'kernel.elf', būvējums_ceļš / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Latviešu.savs', 'korean_exceptions': 20,
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
    for Nosaukums in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Nosaukums] = hashlib.sha256((būvējums_ceļš / Nosaukums).read_bytes()).hexdigest()
    (būvējums_ceļš / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', būvējums_ceļš / 'kernel8.img')


if __name__ == '__main__':
    Palaist()
