#!/usr/bin/env python3
"""ഹോസ്റ്റ് javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from ബിൽഡ്_ഉപയോക്താവ്_സ്ഥലം import സൃഷ്_ടിക്കുക_ഉപയോക്താവ്_സ്ഥലം
from ബിൽഡ്_നെറ്റ്_വർക്ക് import സൃഷ്_ടിക്കുക_നെറ്റ്_വർക്ക്
from 예제빌드 import 예제만들기
from ബിൽഡ്_വിദൂര import സൃഷ്_ടിക്കുക_വിദൂര

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]
കലവറ_വർഗ്ഗമൂലം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1]
ബിൽഡ്_പാത = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build'


def നടപ്പാക്കുക_കമാന്_ഡ്(ആര്_ഗ്യുമെന്_റ്_അരേ):
    subprocess.check_call([str(첫째값) for 첫째값 in ആര്_ഗ്യുമെന്_റ്_അരേ], cwd=str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം))


def നടപ്പിലാക്കുക():
    ബിൽഡ്_പാത.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ഓബ്ജക്റ്റ്_ഫയല്_കണ്_വെര്_ട്ടര് = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ശേഖരം_ഉപകരണം = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ഉപകരണങ്ങൾ in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ഓബ്ജക്റ്റ്_ഫയല്_കണ്_വെര്_ട്ടര്, ശേഖരം_ഉപകരണം):
        if not shutil.which(ഉപകരണങ്ങൾ):
            raise SystemExit('필요한 ബിൽഡ്_సిస్టమ్ ഉപകരണങ്ങൾ 없음: ' + ഉപകരണങ്ങൾ)
    ഫോണ്ട്_വിവരം = json.loads((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor/terminal-font.json').read_text())
    ഫോണ്ട്_ഡാറ്റാ = (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor/terminal-font.bin').read_bytes()
    if len(ഫോണ്ട്_ഡാറ്റാ) != 65616 * 32 or hashlib.sha256(ഫോണ്ട്_ഡാറ്റാ).hexdigest() != ഫോണ്ട്_വിവരം['sha256']:
        raise SystemExit('ടെ_ര്മിനല് ഫോണ്ട്_മൂല്യം വലിപ്പം/SHA256 불일치')
    എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక = {'jshell_interactive': '셸입출력.വിവര_സാങ്കേതികവിദ്യ_ഇടപെടാനുതകുന്ന', 'jshell_output': '셸입출력.ഫലം', 'jshell_input': '셸입출력.입력', 'java_task': 'കെര്_ണല്.작업', 'jfs_path_start': 'മെമ്മറി_ഫയലുകൾ.പാത_ആരംഭം',
               'jfs_path_byte': 'മെമ്മറി_ഫയലുകൾ.പാത_బైట్', 'jfs_open': 'മെമ്മറി_ഫയലുകൾ.തുറക്കുക',
               'jfs_read': 'മെമ്മറി_ഫയലുകൾ.വായന', 'jfs_write': 'മെമ്മറി_ഫയലുകൾ.എഴുത്തു്',
               'jfs_seek': 'മെമ്മറി_ഫയലുകൾ.തിരയുക_പദവി', 'jfs_close': 'മെമ്മറി_ഫയലുകൾ.അടയ്ക്കു',
               'jfs_size': 'മെമ്മറി_ഫയലുകൾ.വലിപ്പം', 'jfs_unlink': 'മെമ്മറി_ഫയലുകൾ.മായ്ക്കുക_എന്_ട്രി',
               'jfs_truncate': 'മെമ്മറി_ഫയലുകൾ.ഗണം_ദൈര്_ഘ്യം'}
    എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక.update({'jfs_entry_count': 'മെമ്മറി_ഫയലുകൾ.파일한도', 'jfs_entry_length': 'മെമ്മറി_ഫയലുകൾ.공개이름길이', 'jfs_entry_byte': 'മെമ്മറി_ഫയലുകൾ.공개이름바이트', 'jfs_entry_size': 'മെമ്മറി_ഫയലുകൾ.공개파일크기'})
    എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక.update({'jdraw_prepare': '화면합성.തയ്യാറാക്കുക', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ക്ലിപ്പ്',
        'jdraw_clip_value': '화면합성.ക്ലിപ്പ്_മൂല്യം', 'jdraw_begin': '화면합성.നടപ്പിലാക്കുക',
        'jdraw_end': '화면합성.പൂർത്തിയാക്കുക', 'jdraw_pixel': '화면합성.പെല്',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.പോയിന്_റര്'})
    എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక.update({'jfs_mkdir': 'മെമ്മറി_ഫയലുകൾ.സൃഷ്_ടിക്കുക_ഡയറക്ടറി', 'jfs_rmdir': 'മെമ്മറി_ഫയലുകൾ.നീക്കംചെയ്യുക_ഡയറക്ടറി', 'jfs_kind': 'മെമ്മറി_ഫയലുകൾ.항목종류'})
    എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక.update({'jnet_socket': '되돌림망.സൃഷ്_ടിക്കുക_എന്_ട്രി', 'jnet_bind': '되돌림망.బైండ్_చేయి_അവസാനബിന്ദു',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.അയയ്ക്കുക',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.പ്രേഷകന്_അവസാനബിന്ദു', 'jnet_close': '되돌림망.അടയ്ക്കു'})
    എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక.update({'jstream_create': 'സ്ട്രീം_നെറ്റ്_വർക്ക്.സൃഷ്_ടിക്കുക_എന്_ട്രി', 'jstream_bind': 'സ്ട്രീം_നെറ്റ്_വർക്ക്.బైండ్_చేయి_അവസാനബിന്ദു', 'jstream_listen': 'സ്ട്രീം_നെറ്റ്_വർക്ക്.ശ്രദ്ധിക്കുക_അവസാനബിന്ദു', 'jstream_connect': 'സ്ട്രീം_നെറ്റ്_വർക്ക്.കണക്ടു്_ചെയ്യുക', 'jstream_accept': 'സ്ട്രീം_നെറ്റ്_വർക്ക്.സ്വീകരിക്കുക_കണക്ഷൻ', 'jstream_read': 'സ്ട്രീം_നെറ്റ്_വർക്ക്.വായന', 'jstream_write': 'സ്ട്രീം_നെറ്റ്_വർക്ക്.എഴുത്തു്', 'jstream_port': 'സ്ട്രീം_നെറ്റ്_വർക്ക്.창구읽기', 'jstream_peer': 'സ്ട്രീം_നെറ്റ്_വർക്ക്.상대창구읽기', 'jstream_close': 'സ്ട്രീം_നെറ്റ്_വർക്ക്.അടയ്ക്കു'})
    for nbsp_ചിഹ്നം_മൂല്യം in list(എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక):
        if nbsp_ചിഹ്നം_മൂല്യം.startswith('jstream_') or nbsp_ചിഹ്നം_മൂല്യം.startswith('jnet_') and nbsp_ചിഹ്നം_മൂല്യം not in ('jnet_put', 'jnet_get'):
            എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక[nbsp_ചിഹ്നം_മൂല്യം.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక.pop(nbsp_ചിഹ്നം_മൂല്യം)
    예제들 = ['public final class ബണ്ടിൽ { public static void തയ്യാറാക്കുക() {']
    for വഴി in sorted((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '예제').iterdir()):
        if വഴി.is_file():
            예제들.append('명령해석기.സ്ഥിരമായ_ഫയല്(%s, %s);' %
                (json.dumps(വഴി.name), json.dumps(വഴി.read_text(encoding='utf-8'), ensure_ascii=True)))
    (ബിൽഡ്_പാത / 'ബണ്ടിൽ.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, കലവറ_വർഗ്ഗമൂലം, നടപ്പാക്കുക_കമാന്_ഡ്)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(ബിൽഡ്_പാത)) as 작업경로:
        ക്ലാസ്_പാത = Path(작업경로)
        നടപ്പാക്കുക_കമാന്_ഡ്(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ക്ലാസ്_പാത, '-sourcepath', ക്ലാസ്_പാത, '-d', ക്ലാസ്_പാത] + sorted((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉറവിടം').glob('*.java')) + [ബിൽഡ്_പാത / 'ബണ്ടിൽ.java', ബിൽഡ്_പാത / '예제꾸러미.java'])
        # ഫയല്·ഷെല്·ജാലകം 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ആര്_ഗ്യുമെന്_റ്_അരേ = ['sh', കലവറ_വർഗ്ഗമൂലം / 'compiler/미리번역.sh', '--entry', 'കെര്_ണല്.നടപ്പിലാക്കുക', '--heap-words', '1048576', '-o', ബിൽഡ്_പാത / 'kernel-java.c']
        for nbsp_ചിഹ്നം_മൂല്യം, విధానం_എന്_ട്രി in sorted(എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక.items()):
            ആര്_ഗ്യുമെന്_റ്_അരേ += ['--export', nbsp_ചിഹ്നം_മൂല്യം + '=' + విధానం_എന്_ട്രി]
        നടപ്പാക്കുക_കമാന്_ഡ്(ആര്_ഗ്യുമെന്_റ്_അരേ + sorted(ക്ലാസ്_പാത.glob('*.class')))
    (ബിൽഡ്_പാത / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ് = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = കലവറ_വർഗ്ഗമൂലം / 'posix-kor/arm64-native'
    സൃഷ്_ടിക്കുക_ഉപയോക്താവ്_സ്ഥലം(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, കലവറ_വർഗ്ഗമൂലം, 시언어번역기, 시플플번역기, 연결편집기, ശേഖരം_ഉപകരണം, കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്, നടപ്പാക്കുക_കമാന്_ഡ്)
    നെറ്റ്_വർക്ക് = സൃഷ്_ടിക്കുക_നെറ്റ്_വർക്ക്(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, 시언어번역기, ശേഖരം_ഉപകരണം, കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്, നടപ്പാക്കുക_കമാന്_ഡ്)
    원격사용 = സൃഷ്_ടിക്കുക_വിദൂര(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, 시언어번역기, ശേഖരം_ഉപകരണം, കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്, നടപ്പാക്കുക_കമാന്_ഡ്)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', ബിൽഡ്_പാത]
    빌드작업 = [(시언어번역기, [], ബിൽഡ്_പാത / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'മെഷീൻ/ടെ_ര്മിനല്.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'മെഷീൻ/വിജറ്റ്.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], ബിൽഡ്_പാത / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'മെഷീൻ/ബോർഡ്.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'മെഷീൻ/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'മെഷീൻ/ഉപയോക്താവ്.c', 'user.o'),
            (시언어번역기, [], പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '부팅/എന്_ട്രി_പോയിന്_റ്_മൂല്യം.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'കണക്ടു്_ചെയ്യുക.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '시험/ഫയല്_കോളുകൾ.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ഫയല്_എന്_ട്രി for ഫയല്_എന്_ട്രി in കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ് if ഫയല്_എന്_ട്രി != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്
        നടപ്പാക്കുക_കമാന്_ഡ്([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', ബിൽഡ്_പാത / 출력결과])
    നടപ്പാക്കുക_കമാന്_ഡ്([ശേഖരം_ഉപകരണം, 'rcs', ബിൽഡ്_പാത / 'libposix-kor-arm64.a', ബിൽഡ്_പാത / 'posix.o'])
    നടപ്പാക്കുക_കമാന്_ഡ്([연결편집기, '--gc-sections', '-T', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '부팅/ലിങ്ക്_ലേഔട്ട്.ld', '-Map', ബിൽഡ്_പാത / 'kernel.map', '-o', ബിൽഡ്_പാത / 'kernel.elf'] +
        [ബിൽഡ്_പാത / പേരു് for പേരു് in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', ബിൽഡ്_പാത / 'libposix-kor-arm64.a', നെറ്റ്_വർക്ക്, 원격사용, ബിൽഡ്_പാത / 'remote/libassh.a', ബിൽഡ്_പാത / 'remote/libbearssl.a', '--end-group'])
    നടപ്പാക്കുക_കമാന്_ഡ്([ഓബ്ജക്റ്റ്_ഫയല്_കണ്_വെര്_ട്ടര്, '-O', 'binary', ബിൽഡ്_പാത / 'kernel.elf', ബിൽഡ്_പാത / 'kernel8.img'])
    ബണ്ടിൽ_ആവിഷ്കാരം = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
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
    for പേരു് in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        ബണ്ടിൽ_ആവിഷ്കാരം['sha256'][പേരു്] = hashlib.sha256((ബിൽഡ്_പാത / പേരു്).read_bytes()).hexdigest()
    (ബിൽഡ്_പാത / 'build.json').write_text(json.dumps(ബണ്ടിൽ_ആവിഷ്കാരം, indent=2) + '\n')
    print('완료:', ബിൽഡ്_പാത / 'kernel8.img')


if __name__ == '__main__':
    നടപ്പിലാക്കുക()
