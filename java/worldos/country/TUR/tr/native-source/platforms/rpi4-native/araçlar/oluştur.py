#!/usr/bin/env python3
"""konak javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from BLD_kullanıcı_yer import açmak_kullanıcı_yer
from BLD_ağ import açmak_ağ
from 예제빌드 import 예제만들기
from BLD_uzak import açmak_uzak

işlem_kök = Path(__file__).resolve().parents[1]
depo_kök = işlem_kök.parents[1]
BLD_yol = işlem_kök / 'build'


def yürütmek_komut(bağımsız_değişken_DİZİ):
    subprocess.check_call([str(첫째값) for 첫째값 in bağımsız_değişken_DİZİ], cwd=str(işlem_kök))


def çalıştır():
    BLD_yol.mkdir(exist_ok=True)
    C_derleyici = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    bağlayıcı_araç = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    nesne_dosyası_dönüştürücü = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arşiv_araç = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for araçlar in ('javac', C_derleyici, 시플플번역기, bağlayıcı_araç, nesne_dosyası_dönüştürücü, Arşiv_araç):
        if not shutil.which(araçlar):
            raise SystemExit('필요한 oluştur araçlar 없음: ' + araçlar)
    yazı_tipi_bilgi = json.loads((işlem_kök / 'vendor/terminal-font.json').read_text())
    yazı_tipi_veri = (işlem_kök / 'vendor/terminal-font.bin').read_bytes()
    if len(yazı_tipi_veri) != 65616 * 32 or hashlib.sha256(yazı_tipi_veri).hexdigest() != yazı_tipi_bilgi['sha256']:
        raise SystemExit('uçbirim yazı_tipi_değer Boyut/SHA256 불일치')
    dışarı_aktarmak_tablo = {'jshell_interactive': '셸입출력.bilgi_teknolojisi_devralmak', 'jshell_output': '셸입출력.metinÇıktısı', 'jshell_input': '셸입출력.artış_değer', 'java_task': 'Çekirdek.작업', 'jfs_path_start': 'BellekDosyaları.yol_Start',
               'jfs_path_byte': 'BellekDosyaları.yol_bayt', 'jfs_open': 'BellekDosyaları.Aç',
               'jfs_read': 'BellekDosyaları.Okuma', 'jfs_write': 'BellekDosyaları.Yazma',
               'jfs_seek': 'BellekDosyaları.arama_konum', 'jfs_close': 'BellekDosyaları.Kapat',
               'jfs_size': 'BellekDosyaları.Boyut', 'jfs_unlink': 'BellekDosyaları.silmek_girdi',
               'jfs_truncate': 'BellekDosyaları.küme_süre'}
    dışarı_aktarmak_tablo.update({'jfs_entry_count': 'BellekDosyaları.파일한도', 'jfs_entry_length': 'BellekDosyaları.공개이름길이', 'jfs_entry_byte': 'BellekDosyaları.공개이름바이트', 'jfs_entry_size': 'BellekDosyaları.공개파일크기'})
    dışarı_aktarmak_tablo.update({'jdraw_prepare': '화면합성.Hazırlan', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klip',
        'jdraw_clip_value': '화면합성.klip_değer', 'jdraw_begin': '화면합성.çalıştır',
        'jdraw_end': '화면합성.Son', 'jdraw_pixel': '화면합성.piksel',
        'jdraw_rectangle': '화면합성.dikdörtgen_dolgu', 'jdraw_pointer': '화면합성.işaretçi'})
    dışarı_aktarmak_tablo.update({'jfs_mkdir': 'BellekDosyaları.açmak_dizin', 'jfs_rmdir': 'BellekDosyaları.kaldırmak_dizin', 'jfs_kind': 'BellekDosyaları.girdi_Tip'})
    dışarı_aktarmak_tablo.update({'jnet_socket': 'geri_döngü_ağ.açmak_girdi', 'jnet_bind': 'geri_döngü_ağ.BIND_uç_nokta',
        'jnet_put': 'geri_döngü_ağ.자료넣기', 'jnet_get': 'geri_döngü_ağ.자료읽기', 'jnet_send': 'geri_döngü_ağ.göndermek',
        'jnet_recv': 'geri_döngü_ağ.almak', 'jnet_port': 'geri_döngü_ağ.창구읽기', 'jnet_address': 'geri_döngü_ağ.주소읽기',
        'jnet_peer': 'geri_döngü_ağ.gönderen_uç_nokta', 'jnet_close': 'geri_döngü_ağ.Kapat'})
    dışarı_aktarmak_tablo.update({'jstream_create': 'akış_ağ.açmak_girdi', 'jstream_bind': 'akış_ağ.BIND_uç_nokta', 'jstream_listen': 'akış_ağ.dinlemek_uç_nokta', 'jstream_connect': 'akış_ağ.Bağlan', 'jstream_accept': 'akış_ağ.kabul_etmek_cxn', 'jstream_read': 'akış_ağ.Okuma', 'jstream_write': 'akış_ağ.Yazma', 'jstream_port': 'akış_ağ.창구읽기', 'jstream_peer': 'akış_ağ.상대창구읽기', 'jstream_close': 'akış_ağ.Kapat'})
    for simge_değer in list(dışarı_aktarmak_tablo):
        if simge_değer.startswith('jstream_') or simge_değer.startswith('jnet_') and simge_değer not in ('jnet_put', 'jnet_get'):
            dışarı_aktarmak_tablo[simge_değer.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = dışarı_aktarmak_tablo.pop(simge_değer)
    예제들 = ['public final class paket_iş { public static void Hazırlan() {']
    for yol in sorted((işlem_kök / '예제').iterdir()):
        if yol.is_file():
            예제들.append('KomutYorumlayıcı.statik_Dosya(%s, %s);' %
                (json.dumps(yol.name), json.dumps(yol.read_text(encoding='utf-8'), ensure_ascii=True)))
    (BLD_yol / 'paket_iş.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(işlem_kök, depo_kök, yürütmek_komut)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(BLD_yol)) as 작업경로:
        Sınıf_yol = Path(작업경로)
        yürütmek_komut(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Sınıf_yol, '-sourcepath', Sınıf_yol, '-d', Sınıf_yol] + sorted((işlem_kök / 'kaynakKod').glob('*.java')) + [BLD_yol / 'paket_iş.java', BLD_yol / '예제꾸러미.java'])
        # dosya·kabuk·Pencere 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        bağımsız_değişken_DİZİ = ['sh', depo_kök / 'compiler/미리번역.sh', '--entry', 'Çekirdek.çalıştır', '--heap-words', '1048576', '-o', BLD_yol / 'kernel-java.c']
        for simge_değer, metot_girdi in sorted(dışarı_aktarmak_tablo.items()):
            bağımsız_değişken_DİZİ += ['--export', simge_değer + '=' + metot_girdi]
        yürütmek_komut(bağımsız_değişken_DİZİ + sorted(Sınıf_yol.glob('*.class')))
    (BLD_yol / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    Yapılandırma_BITS = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = depo_kök / 'posix-kor/arm64-native'
    açmak_kullanıcı_yer(işlem_kök, depo_kök, C_derleyici, 시플플번역기, bağlayıcı_araç, Arşiv_araç, Yapılandırma_BITS, yürütmek_komut)
    ağ = açmak_ağ(işlem_kök, C_derleyici, Arşiv_araç, Yapılandırma_BITS, yürütmek_komut)
    uzak_kullanmak = açmak_uzak(işlem_kök, C_derleyici, Arşiv_araç, Yapılandırma_BITS, yürütmek_komut)
    포함인수 = ['-I', 포직스경로 / 'bildirimler', '-I', BLD_yol]
    빌드작업 = [(C_derleyici, [], BLD_yol / 'terminal-font.S', 'font.o'),
            (C_derleyici, ['-std=c11', '-Wall', '-Wextra', '-Werror'], işlem_kök / 'makine/uçbirim.c', 'terminal.o'),
            (C_derleyici, ['-std=c11', '-Wall', '-Wextra', '-Werror'], işlem_kök / 'makine/ekran_öğesi.c', 'widgets.o'),
            (C_derleyici, ['-std=c11'], BLD_yol / 'kernel-java.c', 'java.o'),
            (C_derleyici, ['-std=c11', '-Wall', '-Wextra', '-Werror'], işlem_kök / 'makine/Pano.c', 'board.o'),
            (C_derleyici, ['-std=c11', '-Wall', '-Wextra', '-Werror'], işlem_kök / 'makine/화면그림.c', 'drawing.o'),
            (C_derleyici, ['-std=c11', '-Wall', '-Wextra', '-Werror'], işlem_kök / 'makine/kullanıcı_alanı.c', 'user.o'),
            (C_derleyici, [], işlem_kök / 'makine_başlatma/giriş_noktası_değer.S', 'entry.o'),
            (C_derleyici, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Bağlan.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], işlem_kök / 'sınamalar/Dosya_Çağrılar.cpp', 'cpp.o')]
    for derleyici_araç, 추가영역, 원본자료, çıktı in 빌드작업:
        원본설정 = [Dosya_girdi for Dosya_girdi in Yapılandırma_BITS if Dosya_girdi != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else Yapılandırma_BITS
        yürütmek_komut([derleyici_araç] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', BLD_yol / çıktı])
    yürütmek_komut([Arşiv_araç, 'rcs', BLD_yol / 'libposix-kor-arm64.a', BLD_yol / 'posix.o'])
    yürütmek_komut([bağlayıcı_araç, '--gc-sections', '-T', işlem_kök / 'makine_başlatma/bağlama_düzeni.ld', '-Map', BLD_yol / 'kernel.map', '-o', BLD_yol / 'kernel.elf'] +
        [BLD_yol / İsim for İsim in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', BLD_yol / 'libposix-kor-arm64.a', ağ, uzak_kullanmak, BLD_yol / 'remote/libassh.a', BLD_yol / 'remote/libbearssl.a', '--end-group'])
    yürütmek_komut([nesne_dosyası_dönüştürücü, '-O', 'binary', BLD_yol / 'kernel.elf', BLD_yol / 'kernel8.img'])
    paket_iş_bildirim = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Türkçe.Öz', 'korean_exceptions': 20,
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
    for İsim in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        paket_iş_bildirim['sha256'][İsim] = hashlib.sha256((BLD_yol / İsim).read_bytes()).hexdigest()
    (BLD_yol / 'build.json').write_text(json.dumps(paket_iş_bildirim, indent=2) + '\n')
    print('완료:', BLD_yol / 'kernel8.img')


if __name__ == '__main__':
    çalıştır()
