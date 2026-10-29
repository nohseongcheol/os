#!/usr/bin/env python3
"""ໂຮສ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from ສ້າງ_ຜູ້ໃຊ້_ພື້ນທີ່ import ສ້າງ_ຜູ້ໃຊ້_ພື້ນທີ່_7f0e0e89
from ສ້າງ_ເຄືອຂ່າຍ_243da480 import ສ້າງ_ເຄືອຂ່າຍ_48d29d6d
from 예제빌드 import 예제만들기
from ສ້າງ_ທາງ_ໄກ import ສ້າງ_ທາງ_ໄກ_69c9c1ef

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]
ຣີໂພຊິທໍຣີ_ເລກຮາກ = ໂຄງ_ການ_ເລກຮາກ.parents[1]
ສ້າງ_ທາງໂຄຈອນ = ໂຄງ_ການ_ເລກຮາກ / 'build'


def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ):
    subprocess.check_call([str(첫째값) for 첫째값 in ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ], cwd=str(ໂຄງ_ການ_ເລກຮາກ))


def ແລ່ນ():
    ສ້າງ_ທາງໂຄຈອນ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ວັດ_ຖຸ_ຟາຍ_ເຄື່ອງປ່ຽນ = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ການສໍາເນົາ_ເຄື່ອງມື = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ເຄື່ອງມື in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ວັດ_ຖຸ_ຟາຍ_ເຄື່ອງປ່ຽນ, ການສໍາເນົາ_ເຄື່ອງມື):
        if not shutil.which(ເຄື່ອງມື):
            raise SystemExit('필요한 ສ້າງ_ລະບົບ ເຄື່ອງມື 없음: ' + ເຄື່ອງມື)
    ຮູບແບບຕົວຫນັງສື_ຂໍ້_ມູນ = json.loads((ໂຄງ_ການ_ເລກຮາກ / 'vendor/terminal-font.json').read_text())
    ຮູບແບບຕົວຫນັງສື_ຂໍ້ມູນ = (ໂຄງ_ການ_ເລກຮາກ / 'vendor/terminal-font.bin').read_bytes()
    if len(ຮູບແບບຕົວຫນັງສື_ຂໍ້ມູນ) != 65616 * 32 or hashlib.sha256(ຮູບແບບຕົວຫນັງສື_ຂໍ້ມູນ).hexdigest() != ຮູບແບບຕົວຫນັງສື_ຂໍ້_ມູນ['sha256']:
        raise SystemExit('ເທີມີນໍ ຮູບແບບຕົວຫນັງສື_ຄ່າ ຂະ_ຫນາດ/SHA256 불일치')
    ສົ່ງອອກ_ຕາຕະລາງ = {'jshell_interactive': '셸입출력.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ແບບໂຕ້ຕອບ', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'ແກນກາງ.작업', 'jfs_path_start': 'ຄວາມຈໍາ_ໄຟລ໌.ທາງໂຄຈອນ_ເລີ່ມ',
               'jfs_path_byte': 'ຄວາມຈໍາ_ໄຟລ໌.ທາງໂຄຈອນ_ໄບ', 'jfs_open': 'ຄວາມຈໍາ_ໄຟລ໌.ສ້າງ',
               'jfs_read': 'ຄວາມຈໍາ_ໄຟລ໌.읽기', 'jfs_write': 'ຄວາມຈໍາ_ໄຟລ໌.ຂຽນ',
               'jfs_seek': 'ຄວາມຈໍາ_ໄຟລ໌.ຊອກຫາ_ຈັດຕໍາແຫນ່ງ', 'jfs_close': 'ຄວາມຈໍາ_ໄຟລ໌.ປິດ',
               'jfs_size': 'ຄວາມຈໍາ_ໄຟລ໌.ຂະ_ຫນາດ', 'jfs_unlink': 'ຄວາມຈໍາ_ໄຟລ໌.ລຶບ_ເຂົ້າໃນ',
               'jfs_truncate': 'ຄວາມຈໍາ_ໄຟລ໌.ຊຸດ_ຄວາມຍາວ'}
    ສົ່ງອອກ_ຕາຕະລາງ.update({'jfs_entry_count': 'ຄວາມຈໍາ_ໄຟລ໌.파일한도', 'jfs_entry_length': 'ຄວາມຈໍາ_ໄຟລ໌.공개이름길이', 'jfs_entry_byte': 'ຄວາມຈໍາ_ໄຟລ໌.공개이름바이트', 'jfs_entry_size': 'ຄວາມຈໍາ_ໄຟລ໌.공개파일크기'})
    ສົ່ງອອກ_ຕາຕະລາງ.update({'jdraw_prepare': '화면합성.ກະ_ກຽມ', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ຄ_ລິບ',
        'jdraw_clip_value': '화면합성.ຄ_ລິບ_ຄ່າ', 'jdraw_begin': '화면합성.ແລ່ນ',
        'jdraw_end': '화면합성.ສໍາ_ເລັດ', 'jdraw_pixel': '화면합성.ເປ_ລ',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.ລູກສອນເມົ້າ'})
    ສົ່ງອອກ_ຕາຕະລາງ.update({'jfs_mkdir': 'ຄວາມຈໍາ_ໄຟລ໌.ສ້າງ_ກຸ່ມຂໍ້ມູນ', 'jfs_rmdir': 'ຄວາມຈໍາ_ໄຟລ໌.폴더지우기', 'jfs_kind': 'ຄວາມຈໍາ_ໄຟລ໌.항목종류'})
    ສົ່ງອອກ_ຕາຕະລາງ.update({'jnet_socket': '되돌림망.ສ້າງ_ເຂົ້າໃນ', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ສົ່ງ',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.ປິດ'})
    ສົ່ງອອກ_ຕາຕະລາງ.update({'jstream_create': 'ສະຕຣີມ_ເຄືອຂ່າຍ.ສ້າງ_ເຂົ້າໃນ', 'jstream_bind': 'ສະຕຣີມ_ເຄືອຂ່າຍ.묶기', 'jstream_listen': 'ສະຕຣີມ_ເຄືອຂ່າຍ.듣기', 'jstream_connect': 'ສະຕຣີມ_ເຄືອຂ່າຍ.ເຊື່ອມຕໍ່', 'jstream_accept': 'ສະຕຣີມ_ເຄືອຂ່າຍ.ຕອບຮັບ_ການເຊື່ອມຕໍ່', 'jstream_read': 'ສະຕຣີມ_ເຄືອຂ່າຍ.읽기', 'jstream_write': 'ສະຕຣີມ_ເຄືອຂ່າຍ.ຂຽນ', 'jstream_port': 'ສະຕຣີມ_ເຄືອຂ່າຍ.창구읽기', 'jstream_peer': 'ສະຕຣີມ_ເຄືອຂ່າຍ.상대창구읽기', 'jstream_close': 'ສະຕຣີມ_ເຄືອຂ່າຍ.ປິດ'})
    for ສັນຍາລັກ_ຄ່າ in list(ສົ່ງອອກ_ຕາຕະລາງ):
        if ສັນຍາລັກ_ຄ່າ.startswith('jstream_') or ສັນຍາລັກ_ຄ່າ.startswith('jnet_') and ສັນຍາລັກ_ຄ່າ not in ('jnet_put', 'jnet_get'):
            ສົ່ງອອກ_ຕາຕະລາງ[ສັນຍາລັກ_ຄ່າ.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ສົ່ງອອກ_ຕາຕະລາງ.pop(ສັນຍາລັກ_ຄ່າ)
    예제들 = ['public final class ຊຸດ { public static void ກະ_ກຽມ() {']
    for ທາງໂຄຈອນ in sorted((ໂຄງ_ການ_ເລກຮາກ / '예제').iterdir()):
        if ທາງໂຄຈອນ.is_file():
            예제들.append('명령해석기.ກໍານົດເອງ_ຟາຍ(%s, %s);' %
                (json.dumps(ທາງໂຄຈອນ.name), json.dumps(ທາງໂຄຈອນ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (ສ້າງ_ທາງໂຄຈອນ / 'ຊຸດ.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(ໂຄງ_ການ_ເລກຮາກ, ຣີໂພຊິທໍຣີ_ເລກຮາກ, ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(ສ້າງ_ທາງໂຄຈອນ)) as 작업경로:
        ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ = Path(작업경로)
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ, '-sourcepath', ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ, '-d', ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ] + sorted((ໂຄງ_ການ_ເລກຮາກ / 'ແຫຼ່ງທີ່ມາ').glob('*.java')) + [ສ້າງ_ທາງໂຄຈອນ / 'ຊຸດ.java', ສ້າງ_ທາງໂຄຈອນ / '예제꾸러미.java'])
        # ຟາຍ·ເຊລ·ວິນໂດ 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ = ['sh', ຣີໂພຊິທໍຣີ_ເລກຮາກ / 'compiler/미리번역.sh', '--entry', 'ແກນກາງ.ແລ່ນ', '--heap-words', '1048576', '-o', ສ້າງ_ທາງໂຄຈອນ / 'kernel-java.c']
        for ສັນຍາລັກ_ຄ່າ, ວິ_ທີ_ເຂົ້າໃນ in sorted(ສົ່ງອອກ_ຕາຕະລາງ.items()):
            ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ += ['--export', ສັນຍາລັກ_ຄ່າ + '=' + ວິ_ທີ_ເຂົ້າໃນ]
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ + sorted(ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ.glob('*.class')))
    (ສ້າງ_ທາງໂຄຈອນ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = ຣີໂພຊິທໍຣີ_ເລກຮາກ / 'posix-kor/arm64-native'
    ສ້າງ_ຜູ້ໃຊ້_ພື້ນທີ່_7f0e0e89(ໂຄງ_ການ_ເລກຮາກ, ຣີໂພຊິທໍຣີ_ເລກຮາກ, 시언어번역기, 시플플번역기, 연결편집기, ການສໍາເນົາ_ເຄື່ອງມື, ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ, ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ)
    ເຄືອຂ່າຍ = ສ້າງ_ເຄືອຂ່າຍ_48d29d6d(ໂຄງ_ການ_ເລກຮາກ, 시언어번역기, ການສໍາເນົາ_ເຄື່ອງມື, ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ, ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ)
    원격사용 = ສ້າງ_ທາງ_ໄກ_69c9c1ef(ໂຄງ_ການ_ເລກຮາກ, 시언어번역기, ການສໍາເນົາ_ເຄື່ອງມື, ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ, ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', ສ້າງ_ທາງໂຄຈອນ]
    빌드작업 = [(시언어번역기, [], ສ້າງ_ທາງໂຄຈອນ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ໂຄງ_ການ_ເລກຮາກ / 'ເຄື່ອງຈັກ/ເທີມີນໍ.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ໂຄງ_ການ_ເລກຮາກ / 'ເຄື່ອງຈັກ/ວິດເຈັດ.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], ສ້າງ_ທາງໂຄຈອນ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ໂຄງ_ການ_ເລກຮາກ / 'ເຄື່ອງຈັກ/ກະດານ.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ໂຄງ_ການ_ເລກຮາກ / 'ເຄື່ອງຈັກ/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ໂຄງ_ການ_ເລກຮາກ / 'ເຄື່ອງຈັກ/ຜູ້ໃຊ້.c', 'user.o'),
            (시언어번역기, [], ໂຄງ_ການ_ເລກຮາກ / '부팅/ເຂົ້າໃນ_ຈຸດ_ຄ່າ.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'ເຊື່ອມຕໍ່.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], ໂຄງ_ການ_ເລກຮາກ / '시험/ຟາຍ_ໂທ.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ຟາຍ_ເຂົ້າໃນ for ຟາຍ_ເຂົ້າໃນ in ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ if ຟາຍ_ເຂົ້າໃນ != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', ສ້າງ_ທາງໂຄຈອນ / 출력결과])
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([ການສໍາເນົາ_ເຄື່ອງມື, 'rcs', ສ້າງ_ທາງໂຄຈອນ / 'libposix-kor-arm64.a', ສ້າງ_ທາງໂຄຈອນ / 'posix.o'])
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([연결편집기, '--gc-sections', '-T', ໂຄງ_ການ_ເລກຮາກ / '부팅/ລິ້ງ_ຮູບແບບ.ld', '-Map', ສ້າງ_ທາງໂຄຈອນ / 'kernel.map', '-o', ສ້າງ_ທາງໂຄຈອນ / 'kernel.elf'] +
        [ສ້າງ_ທາງໂຄຈອນ / ຊື່ for ຊື່ in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', ສ້າງ_ທາງໂຄຈອນ / 'libposix-kor-arm64.a', ເຄືອຂ່າຍ, 원격사용, ສ້າງ_ທາງໂຄຈອນ / 'remote/libassh.a', ສ້າງ_ທາງໂຄຈອນ / 'remote/libbearssl.a', '--end-group'])
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([ວັດ_ຖຸ_ຟາຍ_ເຄື່ອງປ່ຽນ, '-O', 'binary', ສ້າງ_ທາງໂຄຈອນ / 'kernel.elf', ສ້າງ_ທາງໂຄຈອນ / 'kernel8.img'])
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
    for ຊື່ in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][ຊື່] = hashlib.sha256((ສ້າງ_ທາງໂຄຈອນ / ຊື່).read_bytes()).hexdigest()
    (ສ້າງ_ທາງໂຄຈອນ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', ສ້າງ_ທາງໂຄຈອນ / 'kernel8.img')


if __name__ == '__main__':
    ແລ່ນ()
