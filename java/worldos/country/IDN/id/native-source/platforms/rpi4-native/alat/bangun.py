#!/usr/bin/env python3
"""host javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from build_pengguna_SPACE import Buat_pengguna_SPACE
from build_jaringan import Buat_jaringan
from 예제빌드 import 예제만들기
from build_jarak_jauh import Buat_jarak_jauh

Tugas_akar = Path(__file__).resolve().parents[1]
repositori_akar = Tugas_akar.parents[1]
build_jalur = Tugas_akar / 'build'


def Jalankan_perintah(argumen_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argumen_ARRAY], cwd=str(Tugas_akar))


def jalankan():
    build_jalur.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objek_file_pengonversi = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arsip_alat = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for alat in ('javac', 시언어번역기, 시플플번역기, 연결편집기, objek_file_pengonversi, Arsip_alat):
        if not shutil.which(alat):
            raise SystemExit('필요한 bangun alat 없음: ' + alat)
    font_info = json.loads((Tugas_akar / 'vendor/terminal-font.json').read_text())
    font_data = (Tugas_akar / 'vendor/terminal-font.bin').read_bytes()
    if len(font_data) != 65616 * 32 or hashlib.sha256(font_data).hexdigest() != font_info['sha256']:
        raise SystemExit('terminal font_VALUE Ukuran/SHA256 불일치')
    Ekspor_tabel = {'jshell_interactive': '셸입출력.teknologi_informasi_interaktif', 'jshell_output': '셸입출력.keluaranTeks', 'jshell_input': '셸입출력.입력', 'java_task': 'Inti.작업', 'jfs_path_start': 'BerkasMemori.jalur_Mulai',
               'jfs_path_byte': 'BerkasMemori.jalur_byte', 'jfs_open': 'BerkasMemori.Buka',
               'jfs_read': 'BerkasMemori.Baca', 'jfs_write': 'BerkasMemori.Tulis',
               'jfs_seek': 'BerkasMemori.cari_posisi', 'jfs_close': 'BerkasMemori.Tutup',
               'jfs_size': 'BerkasMemori.Ukuran', 'jfs_unlink': 'BerkasMemori.hapus_entri_c8dbc399',
               'jfs_truncate': 'BerkasMemori.set_panjang'}
    Ekspor_tabel.update({'jfs_entry_count': 'BerkasMemori.파일한도', 'jfs_entry_length': 'BerkasMemori.공개이름길이', 'jfs_entry_byte': 'BerkasMemori.공개이름바이트', 'jfs_entry_size': 'BerkasMemori.공개파일크기'})
    Ekspor_tabel.update({'jdraw_prepare': '화면합성.Siapkan', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klip',
        'jdraw_clip_value': '화면합성.klip_VALUE', 'jdraw_begin': '화면합성.jalankan',
        'jdraw_end': '화면합성.Selesai', 'jdraw_pixel': '화면합성.elgam',
        'jdraw_rectangle': '화면합성.persegi_isi', 'jdraw_pointer': '화면합성.pointer'})
    Ekspor_tabel.update({'jfs_mkdir': 'BerkasMemori.Buat_Direktori', 'jfs_rmdir': 'BerkasMemori.hapus_Direktori', 'jfs_kind': 'BerkasMemori.항목종류'})
    Ekspor_tabel.update({'jnet_socket': '되돌림망.Buat_entri', 'jnet_bind': '되돌림망.ikat_peserta',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.kirim',
        'jnet_recv': '되돌림망.terima', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.pengirim_peserta', 'jnet_close': '되돌림망.Tutup'})
    Ekspor_tabel.update({'jstream_create': 'Stream_jaringan.Buat_entri', 'jstream_bind': 'Stream_jaringan.ikat_peserta', 'jstream_listen': 'Stream_jaringan.mendengarkan_peserta', 'jstream_connect': 'Stream_jaringan.Sambung', 'jstream_accept': 'Stream_jaringan.terima_koneksi', 'jstream_read': 'Stream_jaringan.Baca', 'jstream_write': 'Stream_jaringan.Tulis', 'jstream_port': 'Stream_jaringan.창구읽기', 'jstream_peer': 'Stream_jaringan.상대창구읽기', 'jstream_close': 'Stream_jaringan.Tutup'})
    for simbol_VALUE in list(Ekspor_tabel):
        if simbol_VALUE.startswith('jstream_') or simbol_VALUE.startswith('jnet_') and simbol_VALUE not in ('jnet_put', 'jnet_get'):
            Ekspor_tabel[simbol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = Ekspor_tabel.pop(simbol_VALUE)
    예제들 = ['public final class paket { public static void Siapkan() {']
    for jalur in sorted((Tugas_akar / '예제').iterdir()):
        if jalur.is_file():
            예제들.append('PenafsirPerintah.statik_file(%s, %s);' %
                (json.dumps(jalur.name), json.dumps(jalur.read_text(encoding='utf-8'), ensure_ascii=True)))
    (build_jalur / 'paket.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Tugas_akar, repositori_akar, Jalankan_perintah)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(build_jalur)) as 작업경로:
        Kelas_jalur = Path(작업경로)
        Jalankan_perintah(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Kelas_jalur, '-sourcepath', Kelas_jalur, '-d', Kelas_jalur] + sorted((Tugas_akar / 'kodeSumber').glob('*.java')) + [build_jalur / 'paket.java', build_jalur / '예제꾸러미.java'])
        # berkas·shell·Jendela 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argumen_ARRAY = ['sh', repositori_akar / 'compiler/미리번역.sh', '--entry', 'Inti.jalankan', '--heap-words', '1048576', '-o', build_jalur / 'kernel-java.c']
        for simbol_VALUE, metode_entri in sorted(Ekspor_tabel.items()):
            argumen_ARRAY += ['--export', simbol_VALUE + '=' + metode_entri]
        Jalankan_perintah(argumen_ARRAY + sorted(Kelas_jalur.glob('*.class')))
    (build_jalur / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfigurasi_Background_Intelligent_Transfer_Service = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = repositori_akar / 'posix-kor/arm64-native'
    Buat_pengguna_SPACE(Tugas_akar, repositori_akar, 시언어번역기, 시플플번역기, 연결편집기, Arsip_alat, konfigurasi_Background_Intelligent_Transfer_Service, Jalankan_perintah)
    jaringan = Buat_jaringan(Tugas_akar, 시언어번역기, Arsip_alat, konfigurasi_Background_Intelligent_Transfer_Service, Jalankan_perintah)
    jarak_jauh_gunakan = Buat_jarak_jauh(Tugas_akar, 시언어번역기, Arsip_alat, konfigurasi_Background_Intelligent_Transfer_Service, Jalankan_perintah)
    포함인수 = ['-I', 포직스경로 / 'deklarasi', '-I', build_jalur]
    빌드작업 = [(시언어번역기, [], build_jalur / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Tugas_akar / 'mesin/terminal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Tugas_akar / 'mesin/unsur_layar.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], build_jalur / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Tugas_akar / 'mesin/Papan.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Tugas_akar / 'mesin/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Tugas_akar / 'mesin/ruang_pengguna.c', 'user.o'),
            (시언어번역기, [], Tugas_akar / 'awal_mesin/entri_p_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Sambung.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Tugas_akar / 'pengujian/file_Panggilan.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [file_entri for file_entri in konfigurasi_Background_Intelligent_Transfer_Service if file_entri != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfigurasi_Background_Intelligent_Transfer_Service
        Jalankan_perintah([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', build_jalur / 출력결과])
    Jalankan_perintah([Arsip_alat, 'rcs', build_jalur / 'libposix-kor-arm64.a', build_jalur / 'posix.o'])
    Jalankan_perintah([연결편집기, '--gc-sections', '-T', Tugas_akar / 'awal_mesin/tata_letak_penautan.ld', '-Map', build_jalur / 'kernel.map', '-o', build_jalur / 'kernel.elf'] +
        [build_jalur / Nama_2 for Nama_2 in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', build_jalur / 'libposix-kor-arm64.a', jaringan, jarak_jauh_gunakan, build_jalur / 'remote/libassh.a', build_jalur / 'remote/libbearssl.a', '--end-group'])
    Jalankan_perintah([objek_file_pengonversi, '-O', 'binary', build_jalur / 'kernel.elf', build_jalur / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Indonesia.Asli', 'korean_exceptions': 20,
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
    for Nama_2 in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Nama_2] = hashlib.sha256((build_jalur / Nama_2).read_bytes()).hexdigest()
    (build_jalur / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', build_jalur / 'kernel8.img')


if __name__ == '__main__':
    jalankan()
