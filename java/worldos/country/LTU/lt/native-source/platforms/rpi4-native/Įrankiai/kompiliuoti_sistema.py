#!/usr/bin/env python3
"""organizuoti javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from kompiliuoti_naudotojas_erdvė import kurti_naudotojas_erdvė
from kompiliuoti_tinklas import kurti_tinklas_48d29d6d
from 예제빌드 import 예제만들기
from kompiliuoti_nuotolinis import kurti_nuotolinis

Project_šaknis = Path(__file__).resolve().parents[1]
saugykla_šaknis = Project_šaknis.parents[1]
kompiliuoti_kelias = Project_šaknis / 'build'


def Vykdyti_komanda(argumentas_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argumentas_ARRAY], cwd=str(Project_šaknis))


def Paleisti():
    kompiliuoti_kelias.mkdir(exist_ok=True)
    C_kompiliatorius = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objektas_Failas_keitiklis = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Archyvas_įrankis = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Įrankiai in ('javac', C_kompiliatorius, 시플플번역기, 연결편집기, objektas_Failas_keitiklis, Archyvas_įrankis):
        if not shutil.which(Įrankiai):
            raise SystemExit('필요한 kompiliuoti_sistema Įrankiai 없음: ' + Įrankiai)
    šriftas_informacija = json.loads((Project_šaknis / 'vendor/terminal-font.json').read_text())
    šriftas_duomenys = (Project_šaknis / 'vendor/terminal-font.bin').read_bytes()
    if len(šriftas_duomenys) != 65616 * 32 or hashlib.sha256(šriftas_duomenys).hexdigest() != šriftas_informacija['sha256']:
        raise SystemExit('Terminalas šriftas_VALUE Dydis/SHA256 불일치')
    eksportuoti_lentelė = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.Išvestis', 'jshell_input': '셸입출력.입력', 'java_task': 'branduolys.작업', 'jfs_path_start': 'atmintis_Failai.kelias_Start',
               'jfs_path_byte': 'atmintis_Failai.kelias_baitas', 'jfs_open': 'atmintis_Failai.Atverti',
               'jfs_read': 'atmintis_Failai.Skaitymas', 'jfs_write': 'atmintis_Failai.Rašymas',
               'jfs_seek': 'atmintis_Failai.ieškoti_padėtis', 'jfs_close': 'atmintis_Failai.Užverti',
               'jfs_size': 'atmintis_Failai.Dydis', 'jfs_unlink': 'atmintis_Failai.ištrinti_įrašas',
               'jfs_truncate': 'atmintis_Failai.길이정하기'}
    eksportuoti_lentelė.update({'jfs_entry_count': 'atmintis_Failai.파일한도', 'jfs_entry_length': 'atmintis_Failai.공개이름길이', 'jfs_entry_byte': 'atmintis_Failai.공개이름바이트', 'jfs_entry_size': 'atmintis_Failai.공개파일크기'})
    eksportuoti_lentelė.update({'jdraw_prepare': '화면합성.Parengti', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klipas',
        'jdraw_clip_value': '화면합성.klipas_VALUE', 'jdraw_begin': '화면합성.Paleisti',
        'jdraw_end': '화면합성.Baigti', 'jdraw_pixel': '화면합성.pikselis',
        'jdraw_rectangle': '화면합성.stačiakampis_užpildas', 'jdraw_pointer': '화면합성.rodyklė'})
    eksportuoti_lentelė.update({'jfs_mkdir': 'atmintis_Failai.kurti_Katalogas', 'jfs_rmdir': 'atmintis_Failai.pašalinti_Katalogas', 'jfs_kind': 'atmintis_Failai.항목종류'})
    eksportuoti_lentelė.update({'jnet_socket': 'ciklinis_testas_tinklas.kurti_įrašas', 'jnet_bind': 'ciklinis_testas_tinklas.BIND_dalyvis',
        'jnet_put': 'ciklinis_testas_tinklas.자료넣기', 'jnet_get': 'ciklinis_testas_tinklas.자료읽기', 'jnet_send': 'ciklinis_testas_tinklas.siųsti',
        'jnet_recv': 'ciklinis_testas_tinklas.gauti', 'jnet_port': 'ciklinis_testas_tinklas.창구읽기', 'jnet_address': 'ciklinis_testas_tinklas.주소읽기',
        'jnet_peer': 'ciklinis_testas_tinklas.siuntėjas_dalyvis', 'jnet_close': 'ciklinis_testas_tinklas.Užverti'})
    eksportuoti_lentelė.update({'jstream_create': 'Stream_tinklas.kurti_įrašas', 'jstream_bind': 'Stream_tinklas.BIND_dalyvis', 'jstream_listen': 'Stream_tinklas.laukti_dalyvis', 'jstream_connect': 'Stream_tinklas.Prisijungti', 'jstream_accept': 'Stream_tinklas.priimti_ryšys', 'jstream_read': 'Stream_tinklas.Skaitymas', 'jstream_write': 'Stream_tinklas.Rašymas', 'jstream_port': 'Stream_tinklas.창구읽기', 'jstream_peer': 'Stream_tinklas.상대창구읽기', 'jstream_close': 'Stream_tinklas.Užverti'})
    for simbolis_VALUE in list(eksportuoti_lentelė):
        if simbolis_VALUE.startswith('jstream_') or simbolis_VALUE.startswith('jnet_') and simbolis_VALUE not in ('jnet_put', 'jnet_get'):
            eksportuoti_lentelė[simbolis_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = eksportuoti_lentelė.pop(simbolis_VALUE)
    예제들 = ['public final class paketas { public static void Parengti() {']
    for KELIAS in sorted((Project_šaknis / '예제').iterdir()):
        if KELIAS.is_file():
            예제들.append('명령해석기.정적파일(%s, %s);' %
                (json.dumps(KELIAS.name), json.dumps(KELIAS.read_text(encoding='utf-8'), ensure_ascii=True)))
    (kompiliuoti_kelias / 'paketas.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_šaknis, saugykla_šaknis, Vykdyti_komanda)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(kompiliuoti_kelias)) as 작업경로:
        klasė_kelias = Path(작업경로)
        Vykdyti_komanda(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klasė_kelias, '-sourcepath', klasė_kelias, '-d', klasė_kelias] + sorted((Project_šaknis / 'ŠALTINIS').glob('*.java')) + [kompiliuoti_kelias / 'paketas.java', kompiliuoti_kelias / '예제꾸러미.java'])
        # Failas·apvalkalas·Langas 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argumentas_ARRAY = ['sh', saugykla_šaknis / 'compiler/미리번역.sh', '--entry', 'branduolys.Paleisti', '--heap-words', '1048576', '-o', kompiliuoti_kelias / 'kernel-java.c']
        for simbolis_VALUE, metodas_įrašas in sorted(eksportuoti_lentelė.items()):
            argumentas_ARRAY += ['--export', simbolis_VALUE + '=' + metodas_įrašas]
        Vykdyti_komanda(argumentas_ARRAY + sorted(klasė_kelias.glob('*.class')))
    (kompiliuoti_kelias / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = saugykla_šaknis / 'posix-kor/arm64-native'
    kurti_naudotojas_erdvė(Project_šaknis, saugykla_šaknis, C_kompiliatorius, 시플플번역기, 연결편집기, Archyvas_įrankis, konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba, Vykdyti_komanda)
    tinklas = kurti_tinklas_48d29d6d(Project_šaknis, C_kompiliatorius, Archyvas_įrankis, konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba, Vykdyti_komanda)
    nuotolinis_naudoti = kurti_nuotolinis(Project_šaknis, C_kompiliatorius, Archyvas_įrankis, konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba, Vykdyti_komanda)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', kompiliuoti_kelias]
    빌드작업 = [(C_kompiliatorius, [], kompiliuoti_kelias / 'terminal-font.S', 'font.o'),
            (C_kompiliatorius, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_šaknis / 'mašina/Terminalas.c', 'terminal.o'),
            (C_kompiliatorius, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_šaknis / 'mašina/valdiklis.c', 'widgets.o'),
            (C_kompiliatorius, ['-std=c11'], kompiliuoti_kelias / 'kernel-java.c', 'java.o'),
            (C_kompiliatorius, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_šaknis / 'mašina/Lenta.c', 'board.o'),
            (C_kompiliatorius, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_šaknis / 'mašina/화면그림.c', 'drawing.o'),
            (C_kompiliatorius, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_šaknis / 'mašina/naudotojas.c', 'user.o'),
            (C_kompiliatorius, [], Project_šaknis / '부팅/įrašas_p_VALUE.S', 'entry.o'),
            (C_kompiliatorius, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Prisijungti.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_šaknis / '시험/Failas_Skambučiai.cpp', 'cpp.o')]
    for kompiliatorius_įrankis, 추가영역, 원본자료, išeiga in 빌드작업:
        원본설정 = [Failas_įrašas for Failas_įrašas in konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba if Failas_įrašas != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba
        Vykdyti_komanda([kompiliatorius_įrankis] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', kompiliuoti_kelias / išeiga])
    Vykdyti_komanda([Archyvas_įrankis, 'rcs', kompiliuoti_kelias / 'libposix-kor-arm64.a', kompiliuoti_kelias / 'posix.o'])
    Vykdyti_komanda([연결편집기, '--gc-sections', '-T', Project_šaknis / '부팅/sieti_schema.ld', '-Map', kompiliuoti_kelias / 'kernel.map', '-o', kompiliuoti_kelias / 'kernel.elf'] +
        [kompiliuoti_kelias / Pavadinimas_2 for Pavadinimas_2 in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', kompiliuoti_kelias / 'libposix-kor-arm64.a', tinklas, nuotolinis_naudoti, kompiliuoti_kelias / 'remote/libassh.a', kompiliuoti_kelias / 'remote/libbearssl.a', '--end-group'])
    Vykdyti_komanda([objektas_Failas_keitiklis, '-O', 'binary', kompiliuoti_kelias / 'kernel.elf', kompiliuoti_kelias / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Lietuvių.savas', 'korean_exceptions': 20,
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
    for Pavadinimas_2 in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Pavadinimas_2] = hashlib.sha256((kompiliuoti_kelias / Pavadinimas_2).read_bytes()).hexdigest()
    (kompiliuoti_kelias / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', kompiliuoti_kelias / 'kernel8.img')


if __name__ == '__main__':
    Paleisti()
