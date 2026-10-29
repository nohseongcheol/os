#!/usr/bin/env python3
"""gazda javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from épít_felhasználó_tér import készít_felhasználó_tér
from épít_hálózat import készít_hálózat_48d29d6d
from 예제빌드 import 예제만들기
from épít_távoli import készít_távoli

teendő_gyök = Path(__file__).resolve().parents[1]
adattár_gyök = teendő_gyök.parents[1]
épít_útvonal = teendő_gyök / 'build'


def végrehajt_parancs(argumentum_TÖMB):
    subprocess.check_call([str(첫째값) for 첫째값 in argumentum_TÖMB], cwd=str(teendő_gyök))


def Futtatás():
    épít_útvonal.mkdir(exist_ok=True)
    C_fordítóprogram = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    kapcsolószerkesztő_eszköz = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objektum_Fájl_átalakító = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    archív_eszköz = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Eszközök in ('javac', C_fordítóprogram, 시플플번역기, kapcsolószerkesztő_eszköz, objektum_Fájl_átalakító, archív_eszköz):
        if not shutil.which(Eszközök):
            raise SystemExit('필요한 épít_Rendszer Eszközök 없음: ' + Eszközök)
    betűkészlet_infó = json.loads((teendő_gyök / 'vendor/terminal-font.json').read_text())
    betűkészlet_adat = (teendő_gyök / 'vendor/terminal-font.bin').read_bytes()
    if len(betűkészlet_adat) != 65616 * 32 or hashlib.sha256(betűkészlet_adat).hexdigest() != betűkészlet_infó['sha256']:
        raise SystemExit('Terminál betűkészlet_ÉRTÉK Méret/SHA256 불일치')
    exportál_tábla = {'jshell_interactive': '셸입출력.informatikai_részleg_interaktív', 'jshell_output': '셸입출력.Kimenet', 'jshell_input': '셸입출력.bevitel_ÉRTÉK', 'java_task': 'kernel.작업', 'jfs_path_start': 'Memória_Files.útvonal_START',
               'jfs_path_byte': 'Memória_Files.útvonal_bájt', 'jfs_open': 'Memória_Files.Megnyitás',
               'jfs_read': 'Memória_Files.Olvasás', 'jfs_write': 'Memória_Files.Írás',
               'jfs_seek': 'Memória_Files.keres_pozíció', 'jfs_close': 'Memória_Files.Bezárás',
               'jfs_size': 'Memória_Files.Méret', 'jfs_unlink': 'Memória_Files.töröl_bejegyzés',
               'jfs_truncate': 'Memória_Files.halmaz_hossz'}
    exportál_tábla.update({'jfs_entry_count': 'Memória_Files.파일한도', 'jfs_entry_length': 'Memória_Files.공개이름길이', 'jfs_entry_byte': 'Memória_Files.공개이름바이트', 'jfs_entry_size': 'Memória_Files.공개파일크기'})
    exportál_tábla.update({'jdraw_prepare': '화면합성.Előkészítés', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klip',
        'jdraw_clip_value': '화면합성.klip_ÉRTÉK', 'jdraw_begin': '화면합성.Futtatás',
        'jdraw_end': '화면합성.Befejezés', 'jdraw_pixel': '화면합성.képpont',
        'jdraw_rectangle': '화면합성.téglalap_kitöltés', 'jdraw_pointer': '화면합성.mutató'})
    exportál_tábla.update({'jfs_mkdir': 'Memória_Files.készít_címtár', 'jfs_rmdir': 'Memória_Files.eltávolít_címtár', 'jfs_kind': 'Memória_Files.bejegyzés_Altípus'})
    exportál_tábla.update({'jnet_socket': 'visszacsatolt_hálózat.készít_bejegyzés', 'jnet_bind': 'visszacsatolt_hálózat.BIND_végpont',
        'jnet_put': 'visszacsatolt_hálózat.자료넣기', 'jnet_get': 'visszacsatolt_hálózat.자료읽기', 'jnet_send': 'visszacsatolt_hálózat.küld',
        'jnet_recv': 'visszacsatolt_hálózat.fogad', 'jnet_port': 'visszacsatolt_hálózat.창구읽기', 'jnet_address': 'visszacsatolt_hálózat.주소읽기',
        'jnet_peer': 'visszacsatolt_hálózat.feladó_végpont', 'jnet_close': 'visszacsatolt_hálózat.Bezárás'})
    exportál_tábla.update({'jstream_create': 'Stream_hálózat.készít_bejegyzés', 'jstream_bind': 'Stream_hálózat.BIND_végpont', 'jstream_listen': 'Stream_hálózat.figyelés_végpont', 'jstream_connect': 'Stream_hálózat.Kapcsolódás', 'jstream_accept': 'Stream_hálózat.elfogad_ismerős', 'jstream_read': 'Stream_hálózat.Olvasás', 'jstream_write': 'Stream_hálózat.Írás', 'jstream_port': 'Stream_hálózat.창구읽기', 'jstream_peer': 'Stream_hálózat.상대창구읽기', 'jstream_close': 'Stream_hálózat.Bezárás'})
    for szimbólum_ÉRTÉK in list(exportál_tábla):
        if szimbólum_ÉRTÉK.startswith('jstream_') or szimbólum_ÉRTÉK.startswith('jnet_') and szimbólum_ÉRTÉK not in ('jnet_put', 'jnet_get'):
            exportál_tábla[szimbólum_ÉRTÉK.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exportál_tábla.pop(szimbólum_ÉRTÉK)
    예제들 = ['public final class köteg { public static void Előkészítés() {']
    for ÚTVONAL in sorted((teendő_gyök / '예제').iterdir()):
        if ÚTVONAL.is_file():
            예제들.append('명령해석기.statikus_Fájl(%s, %s);' %
                (json.dumps(ÚTVONAL.name), json.dumps(ÚTVONAL.read_text(encoding='utf-8'), ensure_ascii=True)))
    (épít_útvonal / 'köteg.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(teendő_gyök, adattár_gyök, végrehajt_parancs)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(épít_útvonal)) as 작업경로:
        tanóra_útvonal = Path(작업경로)
        végrehajt_parancs(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', tanóra_útvonal, '-sourcepath', tanóra_útvonal, '-d', tanóra_útvonal] + sorted((teendő_gyök / 'FORRÁS').glob('*.java')) + [épít_útvonal / 'köteg.java', épít_útvonal / '예제꾸러미.java'])
        # Fájl·felület·Ablak 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argumentum_TÖMB = ['sh', adattár_gyök / 'compiler/미리번역.sh', '--entry', 'kernel.Futtatás', '--heap-words', '1048576', '-o', épít_útvonal / 'kernel-java.c']
        for szimbólum_ÉRTÉK, metódus_bejegyzés in sorted(exportál_tábla.items()):
            argumentum_TÖMB += ['--export', szimbólum_ÉRTÉK + '=' + metódus_bejegyzés]
        végrehajt_parancs(argumentum_TÖMB + sorted(tanóra_útvonal.glob('*.class')))
    (épít_útvonal / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfiguráció_BITS = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = adattár_gyök / 'posix-kor/arm64-native'
    készít_felhasználó_tér(teendő_gyök, adattár_gyök, C_fordítóprogram, 시플플번역기, kapcsolószerkesztő_eszköz, archív_eszköz, konfiguráció_BITS, végrehajt_parancs)
    hálózat = készít_hálózat_48d29d6d(teendő_gyök, C_fordítóprogram, archív_eszköz, konfiguráció_BITS, végrehajt_parancs)
    távoli_használ = készít_távoli(teendő_gyök, C_fordítóprogram, archív_eszköz, konfiguráció_BITS, végrehajt_parancs)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', épít_útvonal]
    빌드작업 = [(C_fordítóprogram, [], épít_útvonal / 'terminal-font.S', 'font.o'),
            (C_fordítóprogram, ['-std=c11', '-Wall', '-Wextra', '-Werror'], teendő_gyök / 'gép/Terminál.c', 'terminal.o'),
            (C_fordítóprogram, ['-std=c11', '-Wall', '-Wextra', '-Werror'], teendő_gyök / 'gép/widget.c', 'widgets.o'),
            (C_fordítóprogram, ['-std=c11'], épít_útvonal / 'kernel-java.c', 'java.o'),
            (C_fordítóprogram, ['-std=c11', '-Wall', '-Wextra', '-Werror'], teendő_gyök / 'gép/fal.c', 'board.o'),
            (C_fordítóprogram, ['-std=c11', '-Wall', '-Wextra', '-Werror'], teendő_gyök / 'gép/화면그림.c', 'drawing.o'),
            (C_fordítóprogram, ['-std=c11', '-Wall', '-Wextra', '-Werror'], teendő_gyök / 'gép/felhasználó.c', 'user.o'),
            (C_fordítóprogram, [], teendő_gyök / '부팅/belépési_pont_ÉRTÉK.S', 'entry.o'),
            (C_fordítóprogram, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Kapcsolódás.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], teendő_gyök / '시험/Fájl_Hívások.cpp', 'cpp.o')]
    for fordítóprogram_eszköz, 추가영역, 원본자료, kimenet in 빌드작업:
        원본설정 = [Fájl_bejegyzés for Fájl_bejegyzés in konfiguráció_BITS if Fájl_bejegyzés != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfiguráció_BITS
        végrehajt_parancs([fordítóprogram_eszköz] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', épít_útvonal / kimenet])
    végrehajt_parancs([archív_eszköz, 'rcs', épít_útvonal / 'libposix-kor-arm64.a', épít_útvonal / 'posix.o'])
    végrehajt_parancs([kapcsolószerkesztő_eszköz, '--gc-sections', '-T', teendő_gyök / '부팅/csatol_Navigáció.ld', '-Map', épít_útvonal / 'kernel.map', '-o', épít_útvonal / 'kernel.elf'] +
        [épít_útvonal / Név for Név in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', épít_útvonal / 'libposix-kor-arm64.a', hálózat, távoli_használ, épít_útvonal / 'remote/libassh.a', épít_útvonal / 'remote/libbearssl.a', '--end-group'])
    végrehajt_parancs([objektum_Fájl_átalakító, '-O', 'binary', épít_útvonal / 'kernel.elf', épít_útvonal / 'kernel8.img'])
    köteg_jegyzékfájl = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'magyar.saját', 'korean_exceptions': 20,
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
    for Név in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        köteg_jegyzékfájl['sha256'][Név] = hashlib.sha256((épít_útvonal / Név).read_bytes()).hexdigest()
    (épít_útvonal / 'build.json').write_text(json.dumps(köteg_jegyzékfájl, indent=2) + '\n')
    print('완료:', épít_útvonal / 'kernel8.img')


if __name__ == '__main__':
    Futtatás()
