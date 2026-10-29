#!/usr/bin/env python3
"""sauka javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from Gina_Mai_anfani_da_kwamfuta_wuri import ƙirƙíra_Mai_anfani_da_kwamfuta_wuri
from Gina_Hanyar_sadarwa import ƙirƙíra_Hanyar_sadarwa
from 예제빌드 import 예제만들기
from Gina_na_nesa import ƙirƙíra_na_nesa

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
Gina_Hanyar_shiga = 기준 / 'build'


def gudanar_Umarni(Tubalin_aiki_TSARI):
    subprocess.check_call([str(첫째값) for 첫째값 in Tubalin_aiki_TSARI], cwd=str(기준))


def Tafiyar_da():
    Gina_Hanyar_shiga.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    abu_Fayil_Mai_canzawa = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Rumbun_ajiya_kayan_aiki = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Kaya in ('javac', 시언어번역기, 시플플번역기, 연결편집기, abu_Fayil_Mai_canzawa, Rumbun_ajiya_kayan_aiki):
        if not shutil.which(Kaya):
            raise SystemExit('필요한 Gina_na_ura Kaya 없음: ' + Kaya)
    salon_rubutu_bayani = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    salon_rubutu_Tarin_bayani = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(salon_rubutu_Tarin_bayani) != 65616 * 32 or hashlib.sha256(salon_rubutu_Tarin_bayani).hexdigest() != salon_rubutu_bayani['sha256']:
        raise SystemExit('터미널 salon_rubutu_Daraja Girma/SHA256 불일치')
    Fitar_da_tebur = {'jshell_interactive': '셸입출력.kimiyar_bayanai_Shigar_da_umarni_na_kwamfuta', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'Kwara.작업', 'jfs_path_start': 'Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_Fara',
               'jfs_path_byte': 'Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit', 'jfs_open': 'Mahardatar_kwamfuta_Fayiloli.Buɗe',
               'jfs_read': 'Mahardatar_kwamfuta_Fayiloli.Yi_Karatu', 'jfs_write': 'Mahardatar_kwamfuta_Fayiloli.Yi_Rubutu',
               'jfs_seek': 'Mahardatar_kwamfuta_Fayiloli.옮기기', 'jfs_close': 'Mahardatar_kwamfuta_Fayiloli.Rufe',
               'jfs_size': 'Mahardatar_kwamfuta_Fayiloli.Girma', 'jfs_unlink': 'Mahardatar_kwamfuta_Fayiloli.share_Mashigar_bayanai',
               'jfs_truncate': 'Mahardatar_kwamfuta_Fayiloli.zubi_Tsawo'}
    Fitar_da_tebur.update({'jfs_entry_count': 'Mahardatar_kwamfuta_Fayiloli.파일한도', 'jfs_entry_length': 'Mahardatar_kwamfuta_Fayiloli.공개이름길이', 'jfs_entry_byte': 'Mahardatar_kwamfuta_Fayiloli.공개이름바이트', 'jfs_entry_size': 'Mahardatar_kwamfuta_Fayiloli.공개파일크기'})
    Fitar_da_tebur.update({'jdraw_prepare': '화면합성.Shirya', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.darfi',
        'jdraw_clip_value': '화면합성.darfi_Daraja', 'jdraw_begin': '화면합성.Tafiyar_da',
        'jdraw_end': '화면합성.Gama', 'jdraw_pixel': '화면합성.pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.manuni'})
    Fitar_da_tebur.update({'jfs_mkdir': 'Mahardatar_kwamfuta_Fayiloli.ƙirƙíra_ma_ajiya', 'jfs_rmdir': 'Mahardatar_kwamfuta_Fayiloli.Cire_ma_ajiya', 'jfs_kind': 'Mahardatar_kwamfuta_Fayiloli.항목종류'})
    Fitar_da_tebur.update({'jnet_socket': '되돌림망.ƙirƙíra_Mashigar_bayanai', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.Aika',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Rufe'})
    Fitar_da_tebur.update({'jstream_create': 'watsuwa_Hanyar_sadarwa.ƙirƙíra_Mashigar_bayanai', 'jstream_bind': 'watsuwa_Hanyar_sadarwa.묶기', 'jstream_listen': 'watsuwa_Hanyar_sadarwa.듣기', 'jstream_connect': 'watsuwa_Hanyar_sadarwa.Haɗi', 'jstream_accept': 'watsuwa_Hanyar_sadarwa.받음', 'jstream_read': 'watsuwa_Hanyar_sadarwa.Yi_Karatu', 'jstream_write': 'watsuwa_Hanyar_sadarwa.Yi_Rubutu', 'jstream_port': 'watsuwa_Hanyar_sadarwa.창구읽기', 'jstream_peer': 'watsuwa_Hanyar_sadarwa.상대창구읽기', 'jstream_close': 'watsuwa_Hanyar_sadarwa.Rufe'})
    for alama_Daraja in list(Fitar_da_tebur):
        if alama_Daraja.startswith('jstream_') or alama_Daraja.startswith('jnet_') and alama_Daraja not in ('jnet_put', 'jnet_get'):
            Fitar_da_tebur[alama_Daraja.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = Fitar_da_tebur.pop(alama_Daraja)
    예제들 = ['public final class dami { public static void Shirya() {']
    for Hanyar_shiga in sorted((기준 / '예제').iterdir()):
        if Hanyar_shiga.is_file():
            예제들.append('명령해석기.Tsaye_cik_Fayil(%s, %s);' %
                (json.dumps(Hanyar_shiga.name), json.dumps(Hanyar_shiga.read_text(encoding='utf-8'), ensure_ascii=True)))
    (Gina_Hanyar_shiga / 'dami.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, gudanar_Umarni)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(Gina_Hanyar_shiga)) as 작업경로:
        Aji_Hanyar_shiga = Path(작업경로)
        gudanar_Umarni(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Aji_Hanyar_shiga, '-sourcepath', Aji_Hanyar_shiga, '-d', Aji_Hanyar_shiga] + sorted((기준 / 'tushe').glob('*.java')) + [Gina_Hanyar_shiga / 'dami.java', Gina_Hanyar_shiga / '예제꾸러미.java'])
        # Fayil·Mai_fayyace_umani·taga 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        Tubalin_aiki_TSARI = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'Kwara.Tafiyar_da', '--heap-words', '1048576', '-o', Gina_Hanyar_shiga / 'kernel-java.c']
        for alama_Daraja, tsari_Mashigar_bayanai in sorted(Fitar_da_tebur.items()):
            Tubalin_aiki_TSARI += ['--export', alama_Daraja + '=' + tsari_Mashigar_bayanai]
        gudanar_Umarni(Tubalin_aiki_TSARI + sorted(Aji_Hanyar_shiga.glob('*.class')))
    (Gina_Hanyar_shiga / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    ƙirƙíra_Mai_anfani_da_kwamfuta_wuri(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Rumbun_ajiya_kayan_aiki, saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango, gudanar_Umarni)
    Hanyar_sadarwa = ƙirƙíra_Hanyar_sadarwa(기준, 시언어번역기, Rumbun_ajiya_kayan_aiki, saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango, gudanar_Umarni)
    원격사용 = ƙirƙíra_na_nesa(기준, 시언어번역기, Rumbun_ajiya_kayan_aiki, saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango, gudanar_Umarni)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', Gina_Hanyar_shiga]
    빌드작업 = [(시언어번역기, [], Gina_Hanyar_shiga / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'na_ura_mai_kwakwalwa/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'na_ura_mai_kwakwalwa/wijet.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], Gina_Hanyar_shiga / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'na_ura_mai_kwakwalwa/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'na_ura_mai_kwakwalwa/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'na_ura_mai_kwakwalwa/Mai_anfani_da_kwamfuta.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/Mashigar_bayanai_maki_Daraja.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Haɗi.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [Fayil_Mashigar_bayanai for Fayil_Mashigar_bayanai in saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango if Fayil_Mashigar_bayanai != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango
        gudanar_Umarni([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', Gina_Hanyar_shiga / 출력결과])
    gudanar_Umarni([Rumbun_ajiya_kayan_aiki, 'rcs', Gina_Hanyar_shiga / 'libposix-kor-arm64.a', Gina_Hanyar_shiga / 'posix.o'])
    gudanar_Umarni([연결편집기, '--gc-sections', '-T', 기준 / '부팅/Kafa_Zagaye.ld', '-Map', Gina_Hanyar_shiga / 'kernel.map', '-o', Gina_Hanyar_shiga / 'kernel.elf'] +
        [Gina_Hanyar_shiga / Suna for Suna in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', Gina_Hanyar_shiga / 'libposix-kor-arm64.a', Hanyar_sadarwa, 원격사용, Gina_Hanyar_shiga / 'remote/libassh.a', Gina_Hanyar_shiga / 'remote/libbearssl.a', '--end-group'])
    gudanar_Umarni([abu_Fayil_Mai_canzawa, '-O', 'binary', Gina_Hanyar_shiga / 'kernel.elf', Gina_Hanyar_shiga / 'kernel8.img'])
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
    for Suna in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Suna] = hashlib.sha256((Gina_Hanyar_shiga / Suna).read_bytes()).hexdigest()
    (Gina_Hanyar_shiga / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', Gina_Hanyar_shiga / 'kernel8.img')


if __name__ == '__main__':
    Tafiyar_da()
