#!/usr/bin/env python3
"""host javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from qurmaq_istifadəçi_məkan import yarat_istifadəçi_məkan
from qurmaq_Şəbəkə import yarat_Şəbəkə
from 예제빌드 import 예제만들기
from qurmaq_uzaq import yarat_uzaq

Project_kök = Path(__file__).resolve().parents[1]
anbar_kök = Project_kök.parents[1]
qurmaq_yol = Project_kök / 'build'


def icra_etmək_əmr(arqument_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in arqument_ARRAY], cwd=str(Project_kök))


def İcra_Et():
    qurmaq_yol.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    obyekt_fayl_çevirici = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arxiv_alət = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Alətlər in ('javac', 시언어번역기, 시플플번역기, 연결편집기, obyekt_fayl_çevirici, Arxiv_alət):
        if not shutil.which(Alətlər):
            raise SystemExit('필요한 qurmaq_sistem Alətlər 없음: ' + Alətlər)
    şrift_məlumat = json.loads((Project_kök / 'vendor/terminal-font.json').read_text())
    şrift_verilənlər = (Project_kök / 'vendor/terminal-font.bin').read_bytes()
    if len(şrift_verilənlər) != 65616 * 32 or hashlib.sha256(şrift_verilənlər).hexdigest() != şrift_məlumat['sha256']:
        raise SystemExit('Terminal şrift_VALUE Böyüklük/SHA256 불일치')
    ixrac_etmək_cədvəl = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'nüvə.작업', 'jfs_path_start': 'Yaddaş_Fayllar.yol_Başla',
               'jfs_path_byte': 'Yaddaş_Fayllar.yol_bayt', 'jfs_open': 'Yaddaş_Fayllar.Aç',
               'jfs_read': 'Yaddaş_Fayllar.Oxuma', 'jfs_write': 'Yaddaş_Fayllar.Yazma',
               'jfs_seek': 'Yaddaş_Fayllar.axtarmaq_yerinə_qoymaq', 'jfs_close': 'Yaddaş_Fayllar.Bağla',
               'jfs_size': 'Yaddaş_Fayllar.Böyüklük', 'jfs_unlink': 'Yaddaş_Fayllar.silmək_daxiletmə_c8dbc399',
               'jfs_truncate': 'Yaddaş_Fayllar.Dəst_uzunluq'}
    ixrac_etmək_cədvəl.update({'jfs_entry_count': 'Yaddaş_Fayllar.파일한도', 'jfs_entry_length': 'Yaddaş_Fayllar.공개이름길이', 'jfs_entry_byte': 'Yaddaş_Fayllar.공개이름바이트', 'jfs_entry_size': 'Yaddaş_Fayllar.공개파일크기'})
    ixrac_etmək_cədvəl.update({'jdraw_prepare': '화면합성.Hazırla', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klip',
        'jdraw_clip_value': '화면합성.klip_VALUE', 'jdraw_begin': '화면합성.İcra_Et',
        'jdraw_end': '화면합성.Bitir', 'jdraw_pixel': '화면합성.piksel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.göstərici'})
    ixrac_etmək_cədvəl.update({'jfs_mkdir': 'Yaddaş_Fayllar.yarat_kataloq', 'jfs_rmdir': 'Yaddaş_Fayllar.silmək_kataloq', 'jfs_kind': 'Yaddaş_Fayllar.항목종류'})
    ixrac_etmək_cədvəl.update({'jnet_socket': '되돌림망.yarat_daxiletmə', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.göndərmək',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Bağla'})
    ixrac_etmək_cədvəl.update({'jstream_create': 'axın_Şəbəkə.yarat_daxiletmə', 'jstream_bind': 'axın_Şəbəkə.묶기', 'jstream_listen': 'axın_Şəbəkə.듣기', 'jstream_connect': 'axın_Şəbəkə.Bağlan', 'jstream_accept': 'axın_Şəbəkə.qəbul_et_qoşulma', 'jstream_read': 'axın_Şəbəkə.Oxuma', 'jstream_write': 'axın_Şəbəkə.Yazma', 'jstream_port': 'axın_Şəbəkə.창구읽기', 'jstream_peer': 'axın_Şəbəkə.상대창구읽기', 'jstream_close': 'axın_Şəbəkə.Bağla'})
    for simvol_VALUE in list(ixrac_etmək_cədvəl):
        if simvol_VALUE.startswith('jstream_') or simvol_VALUE.startswith('jnet_') and simvol_VALUE not in ('jnet_put', 'jnet_get'):
            ixrac_etmək_cədvəl[simvol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ixrac_etmək_cədvəl.pop(simvol_VALUE)
    예제들 = ['public final class paket { public static void Hazırla() {']
    for Cığır in sorted((Project_kök / '예제').iterdir()):
        if Cığır.is_file():
            예제들.append('명령해석기.statik_fayl(%s, %s);' %
                (json.dumps(Cığır.name), json.dumps(Cığır.read_text(encoding='utf-8'), ensure_ascii=True)))
    (qurmaq_yol / 'paket.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_kök, anbar_kök, icra_etmək_əmr)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(qurmaq_yol)) as 작업경로:
        Sinif_yol = Path(작업경로)
        icra_etmək_əmr(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Sinif_yol, '-sourcepath', Sinif_yol, '-d', Sinif_yol] + sorted((Project_kök / 'QAYNAQ').glob('*.java')) + [qurmaq_yol / 'paket.java', qurmaq_yol / '예제꾸러미.java'])
        # FAYL·örtük·pəncərə 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        arqument_ARRAY = ['sh', anbar_kök / 'compiler/미리번역.sh', '--entry', 'nüvə.İcra_Et', '--heap-words', '1048576', '-o', qurmaq_yol / 'kernel-java.c']
        for simvol_VALUE, metod_daxiletmə in sorted(ixrac_etmək_cədvəl.items()):
            arqument_ARRAY += ['--export', simvol_VALUE + '=' + metod_daxiletmə]
        icra_etmək_əmr(arqument_ARRAY + sorted(Sinif_yol.glob('*.class')))
    (qurmaq_yol / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = anbar_kök / 'posix-kor/arm64-native'
    yarat_istifadəçi_məkan(Project_kök, anbar_kök, 시언어번역기, 시플플번역기, 연결편집기, Arxiv_alət, konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti, icra_etmək_əmr)
    Şəbəkə = yarat_Şəbəkə(Project_kök, 시언어번역기, Arxiv_alət, konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti, icra_etmək_əmr)
    원격사용 = yarat_uzaq(Project_kök, 시언어번역기, Arxiv_alət, konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti, icra_etmək_əmr)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', qurmaq_yol]
    빌드작업 = [(시언어번역기, [], qurmaq_yol / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_kök / 'maşın/Terminal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_kök / 'maşın/vidget.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], qurmaq_yol / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_kök / 'maşın/lövhə.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_kök / 'maşın/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_kök / 'maşın/istifadəçi.c', 'user.o'),
            (시언어번역기, [], Project_kök / '부팅/daxiletmə_p_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Bağlan.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_kök / '시험/fayl_Zənglər.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [fayl_daxiletmə for fayl_daxiletmə in konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti if fayl_daxiletmə != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti
        icra_etmək_əmr([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', qurmaq_yol / 출력결과])
    icra_etmək_əmr([Arxiv_alət, 'rcs', qurmaq_yol / 'libposix-kor-arm64.a', qurmaq_yol / 'posix.o'])
    icra_etmək_əmr([연결편집기, '--gc-sections', '-T', Project_kök / '부팅/keçid_Düzüm.ld', '-Map', qurmaq_yol / 'kernel.map', '-o', qurmaq_yol / 'kernel.elf'] +
        [qurmaq_yol / Ad for Ad in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', qurmaq_yol / 'libposix-kor-arm64.a', Şəbəkə, 원격사용, qurmaq_yol / 'remote/libassh.a', qurmaq_yol / 'remote/libbearssl.a', '--end-group'])
    icra_etmək_əmr([obyekt_fayl_çevirici, '-O', 'binary', qurmaq_yol / 'kernel.elf', qurmaq_yol / 'kernel8.img'])
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
    for Ad in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Ad] = hashlib.sha256((qurmaq_yol / Ad).read_bytes()).hexdigest()
    (qurmaq_yol / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', qurmaq_yol / 'kernel8.img')


if __name__ == '__main__':
    İcra_Et()
