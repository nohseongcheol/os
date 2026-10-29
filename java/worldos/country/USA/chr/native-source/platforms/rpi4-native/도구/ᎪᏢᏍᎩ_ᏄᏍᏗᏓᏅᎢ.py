#!/usr/bin/env python3
"""ᎠᏁᏢᏍᎩ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from ᎪᏢᏍᎩ_ᎬᏗᏍᎩ_SPACE import 사용자영역만들기
from ᎪᏢᏍᎩ_ᏧᎾᏚᏓᎵ import 통신망만들기
from 예제빌드 import 예제만들기
from 원격빌드 import 원격만들기

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ = 기준 / 'build'


def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᏗᏓᎦᏘᎸᏍᏗ_array):
    subprocess.check_call([str(첫째값) for 첫째값 in ᏗᏓᎦᏘᎸᏍᏗ_array], cwd=str(기준))


def ᎠᎢᏎᏍᏗ():
    ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ᎪᎱᏍᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏁᏟᏴᏍᎩ = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for 도구 in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ᎪᎱᏍᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏁᏟᏴᏍᎩ, ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ):
        if not shutil.which(도구):
            raise SystemExit('필요한 ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ 도구 없음: ' + 도구)
    ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᎧᏃᎮᏢᎥᏍᎩ = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᎦᏟᏌᏅᎯ = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᎦᏟᏌᏅᎯ) != 65616 * 32 or hashlib.sha256(ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᎦᏟᏌᏅᎯ).hexdigest() != ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᎧᏃᎮᏢᎥᏍᎩ['sha256']:
        raise SystemExit('터미널 ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ ᎢᎩᏓ/SHA256 불일치')
    ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'kernel.작업', 'jfs_path_start': '기억파일.ᎠᏍᏓᏩᏛᏍᏗ_ᎭᏂᎩᏍᏓ',
               'jfs_path_byte': '기억파일.ᎠᏍᏓᏩᏛᏍᏗ_byte', 'jfs_open': '기억파일.ᎯᏍᏚᎢ',
               'jfs_read': '기억파일.읽기', 'jfs_write': '기억파일.ᎪᏪᎶᏗ',
               'jfs_seek': '기억파일.옮기기', 'jfs_close': '기억파일.ᎯᏍᏚᎲᎦ',
               'jfs_size': '기억파일.ᎢᎩᏓ', 'jfs_unlink': '기억파일.지우기',
               'jfs_truncate': '기억파일.ᎦᎪᏗ_ᏱᎦᏅᎯᏓ'}
    ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ.update({'jfs_entry_count': '기억파일.파일한도', 'jfs_entry_length': '기억파일.공개이름길이', 'jfs_entry_byte': '기억파일.공개이름바이트', 'jfs_entry_size': '기억파일.공개파일크기'})
    ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ.update({'jdraw_prepare': '화면합성.ᎭᏛᏅᎢᏍᏓ', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ᎠᎬᎭᎸᏓ_ᏗᏓᏴᎳᏛᏙᏗ',
        'jdraw_clip_value': '화면합성.ᎠᎬᎭᎸᏓ_ᏗᏓᏴᎳᏛᏙᏗ_ᏧᎬᏩᎶᏗᏯ', 'jdraw_begin': '화면합성.ᎠᎢᏎᏍᏗ',
        'jdraw_end': '화면합성.ᎯᏍᏆᏓ', 'jdraw_pixel': '화면합성.pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.ᎠᏎᎯᎯ'})
    ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ.update({'jfs_mkdir': '기억파일.폴더만들기', 'jfs_rmdir': '기억파일.ᎯᎲᎾ_ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ', 'jfs_kind': '기억파일.항목종류'})
    ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ.update({'jnet_socket': '되돌림망.만들기', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ᏫᎦᏅᏗ',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.ᎯᏍᏚᎲᎦ'})
    ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ.update({'jstream_create': 'ᎤᏪᎬ_ᏧᎾᏚᏓᎵ.만들기', 'jstream_bind': 'ᎤᏪᎬ_ᏧᎾᏚᏓᎵ.묶기', 'jstream_listen': 'ᎤᏪᎬ_ᏧᎾᏚᏓᎵ.듣기', 'jstream_connect': 'ᎤᏪᎬ_ᏧᎾᏚᏓᎵ.ᎫᏓᎳ', 'jstream_accept': 'ᎤᏪᎬ_ᏧᎾᏚᏓᎵ.받음', 'jstream_read': 'ᎤᏪᎬ_ᏧᎾᏚᏓᎵ.읽기', 'jstream_write': 'ᎤᏪᎬ_ᏧᎾᏚᏓᎵ.ᎪᏪᎶᏗ', 'jstream_port': 'ᎤᏪᎬ_ᏧᎾᏚᏓᎵ.창구읽기', 'jstream_peer': 'ᎤᏪᎬ_ᏧᎾᏚᏓᎵ.상대창구읽기', 'jstream_close': 'ᎤᏪᎬ_ᏧᎾᏚᏓᎵ.ᎯᏍᏚᎲᎦ'})
    for 심볼 in list(ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ):
        if 심볼.startswith('jstream_') or 심볼.startswith('jnet_') and 심볼 not in ('jnet_put', 'jnet_get'):
            ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ[심볼.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ.pop(심볼)
    예제들 = ['public final class ᎦᏇᏅᎯ { public static void ᎭᏛᏅᎢᏍᏓ() {']
    for ᎠᏍᏓᏩᏛᏍᏗ in sorted((기준 / '예제').iterdir()):
        if ᎠᏍᏓᏩᏛᏍᏗ.is_file():
            예제들.append('명령해석기.ᎾᏓᏅᏍᎬᎾ_ᎠᏍᏆᏂᎪᏙᏗ(%s, %s);' %
                (json.dumps(ᎠᏍᏓᏩᏛᏍᏗ.name), json.dumps(ᎠᏍᏓᏩᏛᏍᏗ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'ᎦᏇᏅᎯ.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ)) as 작업경로:
        ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ = Path(작업경로)
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ, '-sourcepath', ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ, '-d', ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ] + sorted((기준 / 'ᎦᏟᏌᏅᎯ_0201f362').glob('*.java')) + [ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'ᎦᏇᏅᎯ.java', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / '예제꾸러미.java'])
        # ᎠᏍᏆᏂᎪᏙᏗ·ᎤᏯᏍᎦ·ᏦᎳᏂ 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ᏗᏓᎦᏘᎸᏍᏗ_array = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'kernel.ᎠᎢᏎᏍᏗ', '--heap-words', '1048576', '-o', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'kernel-java.c']
        for 심볼, method_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ in sorted(ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ.items()):
            ᏗᏓᎦᏘᎸᏍᏗ_array += ['--export', 심볼 + '=' + method_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ]
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᏗᏓᎦᏘᎸᏍᏗ_array + sorted(ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ.glob('*.class')))
    (ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    사용자영역만들기(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, 설정비트, ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ)
    ᏧᎾᏚᏓᎵ = 통신망만들기(기준, 시언어번역기, ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, 설정비트, ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ)
    원격사용 = 원격만들기(기준, 시언어번역기, ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, 설정비트, ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ]
    빌드작업 = [(시언어번역기, [], ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / '기계/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / '기계/화면요소.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / '기계/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / '기계/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / '기계/ᎬᏗᏍᎩ.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ_ᏧᎬᏩᎶᏗᏯ.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'ᎫᏓᎳ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ for ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ in 설정비트 if ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 출력결과])
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, 'rcs', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'libposix-kor-arm64.a', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'posix.o'])
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([연결편집기, '--gc-sections', '-T', 기준 / '부팅/ᎫᏓᎸᎢ_ᏱᎬᏂ.ld', '-Map', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'kernel.map', '-o', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'kernel.elf'] +
        [ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / ᏚᏙᎥᎢ for ᏚᏙᎥᎢ in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'libposix-kor-arm64.a', ᏧᎾᏚᏓᎵ, 원격사용, ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'remote/libassh.a', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'remote/libbearssl.a', '--end-group'])
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([ᎪᎱᏍᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏁᏟᏴᏍᎩ, '-O', 'binary', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'kernel.elf', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'kernel8.img'])
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
    for ᏚᏙᎥᎢ in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][ᏚᏙᎥᎢ] = hashlib.sha256((ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / ᏚᏙᎥᎢ).read_bytes()).hexdigest()
    (ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', ᎪᏢᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ / 'kernel8.img')


if __name__ == '__main__':
    ᎠᎢᏎᏍᏗ()
