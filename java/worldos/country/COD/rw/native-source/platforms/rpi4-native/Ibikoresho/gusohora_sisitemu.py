#!/usr/bin/env python3
"""gucumbikira javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from gusohora_ukoresha_akanya import kurema_ukoresha_akanya
from gusohora_Urusobemiyoboro import kurema_Urusobemiyoboro_48d29d6d
from 예제빌드 import 예제만들기
from gusohora_kure import kurema_kure

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
gusohora_inzira = 기준 / 'build'


def gukora_ibwiriza(ingingo_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in ingingo_ARRAY], cwd=str(기준))


def ihuriro():
    gusohora_inzira.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ikintu_dosiye_muhinduzi = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    gushyingura_igikoresho = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Ibikoresho in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ikintu_dosiye_muhinduzi, gushyingura_igikoresho):
        if not shutil.which(Ibikoresho):
            raise SystemExit('필요한 gusohora_sisitemu Ibikoresho 없음: ' + Ibikoresho)
    imyandikire_amakuru = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    imyandikire_amakurushingiro = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(imyandikire_amakurushingiro) != 65616 * 32 or hashlib.sha256(imyandikire_amakurushingiro).hexdigest() != imyandikire_amakuru['sha256']:
        raise SystemExit('터미널 imyandikire_agaciro Ingano/SHA256 불일치')
    kwimura_imbonerahamwe = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'intima.작업', 'jfs_path_start': 'ububiko_Dosiye.inzira_Itangira',
               'jfs_path_byte': 'ububiko_Dosiye.inzira_bayiti', 'jfs_open': 'ububiko_Dosiye.Gufungura',
               'jfs_read': 'ububiko_Dosiye.읽기', 'jfs_write': 'ububiko_Dosiye.kwandika',
               'jfs_seek': 'ububiko_Dosiye.옮기기', 'jfs_close': 'ububiko_Dosiye.Gufunga',
               'jfs_size': 'ububiko_Dosiye.Ingano', 'jfs_unlink': 'ububiko_Dosiye.지우기',
               'jfs_truncate': 'ububiko_Dosiye.itsinda_uburebure'}
    kwimura_imbonerahamwe.update({'jfs_entry_count': 'ububiko_Dosiye.파일한도', 'jfs_entry_length': 'ububiko_Dosiye.공개이름길이', 'jfs_entry_byte': 'ububiko_Dosiye.공개이름바이트', 'jfs_entry_size': 'ububiko_Dosiye.공개파일크기'})
    kwimura_imbonerahamwe.update({'jdraw_prepare': '화면합성.Gutegura', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.kiripu',
        'jdraw_clip_value': '화면합성.kiripu_agaciro', 'jdraw_begin': '화면합성.ihuriro',
        'jdraw_end': '화면합성.Kurangiza', 'jdraw_pixel': '화면합성.pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.mwerekana'})
    kwimura_imbonerahamwe.update({'jfs_mkdir': 'ububiko_Dosiye.kurema_ububiko', 'jfs_rmdir': 'ububiko_Dosiye.gukuramo_ububiko', 'jfs_kind': 'ububiko_Dosiye.항목종류'})
    kwimura_imbonerahamwe.update({'jnet_socket': '되돌림망.kurema_icyinjizwa', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.kohereza',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Gufunga'})
    kwimura_imbonerahamwe.update({'jstream_create': 'Stream_Urusobemiyoboro.kurema_icyinjizwa', 'jstream_bind': 'Stream_Urusobemiyoboro.묶기', 'jstream_listen': 'Stream_Urusobemiyoboro.듣기', 'jstream_connect': 'Stream_Urusobemiyoboro.Guhuza', 'jstream_accept': 'Stream_Urusobemiyoboro.kwemera_kwihuza', 'jstream_read': 'Stream_Urusobemiyoboro.읽기', 'jstream_write': 'Stream_Urusobemiyoboro.kwandika', 'jstream_port': 'Stream_Urusobemiyoboro.창구읽기', 'jstream_peer': 'Stream_Urusobemiyoboro.상대창구읽기', 'jstream_close': 'Stream_Urusobemiyoboro.Gufunga'})
    for ikimenyetso_agaciro in list(kwimura_imbonerahamwe):
        if ikimenyetso_agaciro.startswith('jstream_') or ikimenyetso_agaciro.startswith('jnet_') and ikimenyetso_agaciro not in ('jnet_put', 'jnet_get'):
            kwimura_imbonerahamwe[ikimenyetso_agaciro.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = kwimura_imbonerahamwe.pop(ikimenyetso_agaciro)
    예제들 = ['public final class ipaki { public static void Gutegura() {']
    for Inzira in sorted((기준 / '예제').iterdir()):
        if Inzira.is_file():
            예제들.append('명령해석기.kitayega_dosiye(%s, %s);' %
                (json.dumps(Inzira.name), json.dumps(Inzira.read_text(encoding='utf-8'), ensure_ascii=True)))
    (gusohora_inzira / 'ipaki.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, gukora_ibwiriza)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(gusohora_inzira)) as 작업경로:
        icyiciro_inzira = Path(작업경로)
        gukora_ibwiriza(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', icyiciro_inzira, '-sourcepath', icyiciro_inzira, '-d', icyiciro_inzira] + sorted((기준 / 'Inkomoko').glob('*.java')) + [gusohora_inzira / 'ipaki.java', gusohora_inzira / '예제꾸러미.java'])
        # Idosiye·insomamabwiriza·idirishya 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ingingo_ARRAY = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'intima.ihuriro', '--heap-words', '1048576', '-o', gusohora_inzira / 'kernel-java.c']
        for ikimenyetso_agaciro, uburyo_icyinjizwa in sorted(kwimura_imbonerahamwe.items()):
            ingingo_ARRAY += ['--export', ikimenyetso_agaciro + '=' + uburyo_icyinjizwa]
        gukora_ibwiriza(ingingo_ARRAY + sorted(icyiciro_inzira.glob('*.class')))
    (gusohora_inzira / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    kurema_ukoresha_akanya(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, gushyingura_igikoresho, 설정비트, gukora_ibwiriza)
    Urusobemiyoboro = kurema_Urusobemiyoboro_48d29d6d(기준, 시언어번역기, gushyingura_igikoresho, 설정비트, gukora_ibwiriza)
    원격사용 = kurema_kure(기준, 시언어번역기, gushyingura_igikoresho, 설정비트, gukora_ibwiriza)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', gusohora_inzira]
    빌드작업 = [(시언어번역기, [], gusohora_inzira / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'imashini/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'imashini/wijeti.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], gusohora_inzira / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'imashini/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'imashini/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'imashini/ukoresha.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/icyinjizwa_inota_agaciro.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Guhuza.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [dosiye_icyinjizwa for dosiye_icyinjizwa in 설정비트 if dosiye_icyinjizwa != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        gukora_ibwiriza([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', gusohora_inzira / 출력결과])
    gukora_ibwiriza([gushyingura_igikoresho, 'rcs', gusohora_inzira / 'libposix-kor-arm64.a', gusohora_inzira / 'posix.o'])
    gukora_ibwiriza([연결편집기, '--gc-sections', '-T', 기준 / '부팅/Ihuza_Imimerere.ld', '-Map', gusohora_inzira / 'kernel.map', '-o', gusohora_inzira / 'kernel.elf'] +
        [gusohora_inzira / Izina for Izina in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', gusohora_inzira / 'libposix-kor-arm64.a', Urusobemiyoboro, 원격사용, gusohora_inzira / 'remote/libassh.a', gusohora_inzira / 'remote/libbearssl.a', '--end-group'])
    gukora_ibwiriza([ikintu_dosiye_muhinduzi, '-O', 'binary', gusohora_inzira / 'kernel.elf', gusohora_inzira / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Ikinyarwanda.자체', 'korean_exceptions': 20,
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
    for Izina in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Izina] = hashlib.sha256((gusohora_inzira / Izina).read_bytes()).hexdigest()
    (gusohora_inzira / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', gusohora_inzira / 'kernel8.img')


if __name__ == '__main__':
    ihuriro()
