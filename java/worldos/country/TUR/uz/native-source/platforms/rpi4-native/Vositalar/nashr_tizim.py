#!/usr/bin/env python3
"""tashkilotchi javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from nashr_foydalanuvchi_joy import Yaratish_foydalanuvchi_joy
from nashr_Tarmoq import Yaratish_Tarmoq
from 예제빌드 import 예제만들기
from nashr_masofaviy_972fb256 import Yaratish_masofaviy

Project_ildiz = Path(__file__).resolve().parents[1]
repozitoriy_ildiz = Project_ildiz.parents[1]
nashr_yo_l = Project_ildiz / 'build'


def bajarmoq_buyruq(dalil_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in dalil_ARRAY], cwd=str(Project_ildiz))


def Bajarish():
    nashr_yo_l.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    obyekt_fayl_konverter = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arxiv_vosita = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Vositalar in ('javac', 시언어번역기, 시플플번역기, 연결편집기, obyekt_fayl_konverter, Arxiv_vosita):
        if not shutil.which(Vositalar):
            raise SystemExit('필요한 nashr_tizim Vositalar 없음: ' + Vositalar)
    shrift_ma_lumot = json.loads((Project_ildiz / 'vendor/terminal-font.json').read_text())
    shrift_ma_lumotlar = (Project_ildiz / 'vendor/terminal-font.bin').read_bytes()
    if len(shrift_ma_lumotlar) != 65616 * 32 or hashlib.sha256(shrift_ma_lumotlar).hexdigest() != shrift_ma_lumot['sha256']:
        raise SystemExit('Terminal shrift_VALUE Hajmi/SHA256 불일치')
    eksport_qilmoq_jadval = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'o_zak.작업', 'jfs_path_start': 'Xotira_Fayllar.yo_l_Start',
               'jfs_path_byte': 'Xotira_Fayllar.yo_l_bayt', 'jfs_open': 'Xotira_Fayllar.Ochish',
               'jfs_read': 'Xotira_Fayllar.Oʻqish', 'jfs_write': 'Xotira_Fayllar.Yozish',
               'jfs_seek': 'Xotira_Fayllar.izlamoq_holat', 'jfs_close': 'Xotira_Fayllar.Yopish',
               'jfs_size': 'Xotira_Fayllar.Hajmi', 'jfs_unlink': 'Xotira_Fayllar.tozalash_kiritish',
               'jfs_truncate': 'Xotira_Fayllar.to_plam_uzunlik'}
    eksport_qilmoq_jadval.update({'jfs_entry_count': 'Xotira_Fayllar.파일한도', 'jfs_entry_length': 'Xotira_Fayllar.공개이름길이', 'jfs_entry_byte': 'Xotira_Fayllar.공개이름바이트', 'jfs_entry_size': 'Xotira_Fayllar.공개파일크기'})
    eksport_qilmoq_jadval.update({'jdraw_prepare': '화면합성.Tayyorlamoq', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klip',
        'jdraw_clip_value': '화면합성.klip_VALUE', 'jdraw_begin': '화면합성.Bajarish',
        'jdraw_end': '화면합성.Tugatmoq', 'jdraw_pixel': '화면합성.piksel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.kursor'})
    eksport_qilmoq_jadval.update({'jfs_mkdir': 'Xotira_Fayllar.Yaratish_katalog', 'jfs_rmdir': 'Xotira_Fayllar.olib_tashlamoq_katalog', 'jfs_kind': 'Xotira_Fayllar.항목종류'})
    eksport_qilmoq_jadval.update({'jnet_socket': '되돌림망.Yaratish_kiritish', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.yuborish',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Yopish'})
    eksport_qilmoq_jadval.update({'jstream_create': 'oqim_Tarmoq.Yaratish_kiritish', 'jstream_bind': 'oqim_Tarmoq.묶기', 'jstream_listen': 'oqim_Tarmoq.듣기', 'jstream_connect': 'oqim_Tarmoq.Ulanish', 'jstream_accept': 'oqim_Tarmoq.qabul_qilish_aloqa', 'jstream_read': 'oqim_Tarmoq.Oʻqish', 'jstream_write': 'oqim_Tarmoq.Yozish', 'jstream_port': 'oqim_Tarmoq.창구읽기', 'jstream_peer': 'oqim_Tarmoq.상대창구읽기', 'jstream_close': 'oqim_Tarmoq.Yopish'})
    for ramz_VALUE in list(eksport_qilmoq_jadval):
        if ramz_VALUE.startswith('jstream_') or ramz_VALUE.startswith('jnet_') and ramz_VALUE not in ('jnet_put', 'jnet_get'):
            eksport_qilmoq_jadval[ramz_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = eksport_qilmoq_jadval.pop(ramz_VALUE)
    예제들 = ['public final class to_plam { public static void Tayyorlamoq() {']
    for yo_l in sorted((Project_ildiz / '예제').iterdir()):
        if yo_l.is_file():
            예제들.append('명령해석기.statik_fayl(%s, %s);' %
                (json.dumps(yo_l.name), json.dumps(yo_l.read_text(encoding='utf-8'), ensure_ascii=True)))
    (nashr_yo_l / 'to_plam.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_ildiz, repozitoriy_ildiz, bajarmoq_buyruq)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(nashr_yo_l)) as 작업경로:
        Sinf_yo_l = Path(작업경로)
        bajarmoq_buyruq(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Sinf_yo_l, '-sourcepath', Sinf_yo_l, '-d', Sinf_yo_l] + sorted((Project_ildiz / 'manba').glob('*.java')) + [nashr_yo_l / 'to_plam.java', nashr_yo_l / '예제꾸러미.java'])
        # Fayl·qobiq·oyna 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        dalil_ARRAY = ['sh', repozitoriy_ildiz / 'compiler/미리번역.sh', '--entry', 'o_zak.Bajarish', '--heap-words', '1048576', '-o', nashr_yo_l / 'kernel-java.c']
        for ramz_VALUE, uslub_kiritish in sorted(eksport_qilmoq_jadval.items()):
            dalil_ARRAY += ['--export', ramz_VALUE + '=' + uslub_kiritish]
        bajarmoq_buyruq(dalil_ARRAY + sorted(Sinf_yo_l.glob('*.class')))
    (nashr_yo_l / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = repozitoriy_ildiz / 'posix-kor/arm64-native'
    Yaratish_foydalanuvchi_joy(Project_ildiz, repozitoriy_ildiz, 시언어번역기, 시플플번역기, 연결편집기, Arxiv_vosita, tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati, bajarmoq_buyruq)
    Tarmoq = Yaratish_Tarmoq(Project_ildiz, 시언어번역기, Arxiv_vosita, tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati, bajarmoq_buyruq)
    원격사용 = Yaratish_masofaviy(Project_ildiz, 시언어번역기, Arxiv_vosita, tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati, bajarmoq_buyruq)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', nashr_yo_l]
    빌드작업 = [(시언어번역기, [], nashr_yo_l / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_ildiz / '기계/Terminal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_ildiz / '기계/vidjet.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], nashr_yo_l / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_ildiz / '기계/yozuv_taxtasi.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_ildiz / '기계/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_ildiz / '기계/foydalanuvchi.c', 'user.o'),
            (시언어번역기, [], Project_ildiz / '부팅/kiritish_nuqta_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Ulanish.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_ildiz / '시험/fayl_Qo_ng_iroqlar.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [fayl_kiritish for fayl_kiritish in tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati if fayl_kiritish != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati
        bajarmoq_buyruq([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', nashr_yo_l / 출력결과])
    bajarmoq_buyruq([Arxiv_vosita, 'rcs', nashr_yo_l / 'libposix-kor-arm64.a', nashr_yo_l / 'posix.o'])
    bajarmoq_buyruq([연결편집기, '--gc-sections', '-T', Project_ildiz / '부팅/ulash_Maket.ld', '-Map', nashr_yo_l / 'kernel.map', '-o', nashr_yo_l / 'kernel.elf'] +
        [nashr_yo_l / Nomi for Nomi in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', nashr_yo_l / 'libposix-kor-arm64.a', Tarmoq, 원격사용, nashr_yo_l / 'remote/libassh.a', nashr_yo_l / 'remote/libbearssl.a', '--end-group'])
    bajarmoq_buyruq([obyekt_fayl_konverter, '-O', 'binary', nashr_yo_l / 'kernel.elf', nashr_yo_l / 'kernel8.img'])
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
    for Nomi in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Nomi] = hashlib.sha256((nashr_yo_l / Nomi).read_bytes()).hexdigest()
    (nashr_yo_l / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', nashr_yo_l / 'kernel8.img')


if __name__ == '__main__':
    Bajarish()
