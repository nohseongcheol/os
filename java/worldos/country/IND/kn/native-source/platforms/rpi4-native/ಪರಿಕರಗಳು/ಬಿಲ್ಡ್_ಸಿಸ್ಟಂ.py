#!/usr/bin/env python3
"""ಹೋಸ್ಟ್ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from ಬಿಲ್ಡ್_ಬಳಕೆದಾರ_ಸ್ಪೇಸ್ import ರಚಿಸು_ಬಳಕೆದಾರ_ಸ್ಪೇಸ್
from ಬಿಲ್ಡ್_ನೆಟ್_ವರ್ಕ್ import ರಚಿಸು_ನೆಟ್_ವರ್ಕ್_48d29d6d
from 예제빌드 import 예제만들기
from ಬಿಲ್ಡ್_ರಿಮೋಟ್ import ರಚಿಸು_ರಿಮೋಟ್

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]
ಸಂಗ್ರಹಣೆ_ಮೂಲ = ಬಿಂಬಿಸು_ಮೂಲ.parents[1]
ಬಿಲ್ಡ್_ಹಾದಿ = ಬಿಂಬಿಸು_ಮೂಲ / 'build'


def ಪೂರೈಸು_ಆದೇಶ(ವಾದ_ಅರೇ):
    subprocess.check_call([str(첫째값) for 첫째값 in ವಾದ_ಅರೇ], cwd=str(ಬಿಂಬಿಸು_ಮೂಲ))


def ಚಲಾಯಿಸು_2():
    ಬಿಲ್ಡ್_ಹಾದಿ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ಆಬ್ಜೆಕ್ಟ್_ಫೈಲ್_ಕನ್ವರ್ಟರ್ = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ಅರ್ಖೀವ್_ಪರಿಕರ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ಪರಿಕರಗಳು in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ಆಬ್ಜೆಕ್ಟ್_ಫೈಲ್_ಕನ್ವರ್ಟರ್, ಅರ್ಖೀವ್_ಪರಿಕರ):
        if not shutil.which(ಪರಿಕರಗಳು):
            raise SystemExit('필요한 ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ ಪರಿಕರಗಳು 없음: ' + ಪರಿಕರಗಳು)
    ಫಾಂಟ್_ಮಾಹಿತಿ = json.loads((ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/terminal-font.json').read_text())
    ಫಾಂಟ್_ಡೇಟಾ = (ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/terminal-font.bin').read_bytes()
    if len(ಫಾಂಟ್_ಡೇಟಾ) != 65616 * 32 or hashlib.sha256(ಫಾಂಟ್_ಡೇಟಾ).hexdigest() != ಫಾಂಟ್_ಮಾಹಿತಿ['sha256']:
        raise SystemExit('ಟರ್ಮಿನಲ್ ಫಾಂಟ್_ಮೌಲ್ಯ ಗಾತ್ರ/SHA256 불일치')
    ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ = {'jshell_interactive': '셸입출력.ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಸಂವಾದಕ', 'jshell_output': '셸입출력.ಔಟ್_ಪುಟ್', 'jshell_input': '셸입출력.입력', 'java_task': 'ಕರ್ನಲ್.작업', 'jfs_path_start': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ಹಾದಿ_ಆರಂಭಿಸು',
               'jfs_path_byte': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ಹಾದಿ_ಬೈಟ್', 'jfs_open': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ತೆರೆ',
               'jfs_read': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ಓದು', 'jfs_write': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ಬರೆ',
               'jfs_seek': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ಸೀಕ್_ಹುದ್ದೆ', 'jfs_close': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ಮುಚ್ಚು',
               'jfs_size': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ಗಾತ್ರ', 'jfs_unlink': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ಅಳಿಸು_ನಮೂದು',
               'jfs_truncate': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ಸೆಟ್_ಉದ್ದ'}
    ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ.update({'jfs_entry_count': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.파일한도', 'jfs_entry_length': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.공개이름길이', 'jfs_entry_byte': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.공개이름바이트', 'jfs_entry_size': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.공개파일크기'})
    ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ.update({'jdraw_prepare': '화면합성.ಸಿದ್ಧಪಡಿಸು', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ಕ್ಲಿಪ್',
        'jdraw_clip_value': '화면합성.ಕ್ಲಿಪ್_ಮೌಲ್ಯ', 'jdraw_begin': '화면합성.ಚಲಾಯಿಸು_2',
        'jdraw_end': '화면합성.ಮುಗಿಸು', 'jdraw_pixel': '화면합성.ಪೆಲ್',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.ಸೂಚಕ'})
    ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ.update({'jfs_mkdir': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ರಚಿಸು_ಡೈರೆಕ್ಟರಿ', 'jfs_rmdir': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.ತೆಗೆ_ಡೈರೆಕ್ಟರಿ', 'jfs_kind': 'ಮೆಮೊರಿ_ಫೈಲ್_ಗಳು.항목종류'})
    ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ.update({'jnet_socket': '되돌림망.ರಚಿಸು_ನಮೂದು', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ಕಳುಹಿಸಿ',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.ಮುಚ್ಚು'})
    ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ.update({'jstream_create': 'ಸ್ಟ್ರೀಮ್_ನೆಟ್_ವರ್ಕ್.ರಚಿಸು_ನಮೂದು', 'jstream_bind': 'ಸ್ಟ್ರೀಮ್_ನೆಟ್_ವರ್ಕ್.묶기', 'jstream_listen': 'ಸ್ಟ್ರೀಮ್_ನೆಟ್_ವರ್ಕ್.듣기', 'jstream_connect': 'ಸ್ಟ್ರೀಮ್_ನೆಟ್_ವರ್ಕ್.ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು', 'jstream_accept': 'ಸ್ಟ್ರೀಮ್_ನೆಟ್_ವರ್ಕ್.ಸಮ್ಮತಿಸು_ಸಂಪರ್ಕ', 'jstream_read': 'ಸ್ಟ್ರೀಮ್_ನೆಟ್_ವರ್ಕ್.ಓದು', 'jstream_write': 'ಸ್ಟ್ರೀಮ್_ನೆಟ್_ವರ್ಕ್.ಬರೆ', 'jstream_port': 'ಸ್ಟ್ರೀಮ್_ನೆಟ್_ವರ್ಕ್.창구읽기', 'jstream_peer': 'ಸ್ಟ್ರೀಮ್_ನೆಟ್_ವರ್ಕ್.상대창구읽기', 'jstream_close': 'ಸ್ಟ್ರೀಮ್_ನೆಟ್_ವರ್ಕ್.ಮುಚ್ಚು'})
    for ಚಿಹ್ನೆ_ಮೌಲ್ಯ in list(ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ):
        if ಚಿಹ್ನೆ_ಮೌಲ್ಯ.startswith('jstream_') or ಚಿಹ್ನೆ_ಮೌಲ್ಯ.startswith('jnet_') and ಚಿಹ್ನೆ_ಮೌಲ್ಯ not in ('jnet_put', 'jnet_get'):
            ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ[ಚಿಹ್ನೆ_ಮೌಲ್ಯ.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ.pop(ಚಿಹ್ನೆ_ಮೌಲ್ಯ)
    예제들 = ['public final class ಬಂಡಲ್ { public static void ಸಿದ್ಧಪಡಿಸು() {']
    for ಮಾರ್ಗ in sorted((ಬಿಂಬಿಸು_ಮೂಲ / '예제').iterdir()):
        if ಮಾರ್ಗ.is_file():
            예제들.append('명령해석기.ಸ್ಥಾಯಿ_ಫೈಲ್(%s, %s);' %
                (json.dumps(ಮಾರ್ಗ.name), json.dumps(ಮಾರ್ಗ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (ಬಿಲ್ಡ್_ಹಾದಿ / 'ಬಂಡಲ್.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(ಬಿಂಬಿಸು_ಮೂಲ, ಸಂಗ್ರಹಣೆ_ಮೂಲ, ಪೂರೈಸು_ಆದೇಶ)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(ಬಿಲ್ಡ್_ಹಾದಿ)) as 작업경로:
        ವರ್ಗ_ಹಾದಿ = Path(작업경로)
        ಪೂರೈಸು_ಆದೇಶ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ವರ್ಗ_ಹಾದಿ, '-sourcepath', ವರ್ಗ_ಹಾದಿ, '-d', ವರ್ಗ_ಹಾದಿ] + sorted((ಬಿಂಬಿಸು_ಮೂಲ / 'ಮೂಲ').glob('*.java')) + [ಬಿಲ್ಡ್_ಹಾದಿ / 'ಬಂಡಲ್.java', ಬಿಲ್ಡ್_ಹಾದಿ / '예제꾸러미.java'])
        # ಕಡತ·ಶೆಲ್·ವಿಂಡೋ 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ವಾದ_ಅರೇ = ['sh', ಸಂಗ್ರಹಣೆ_ಮೂಲ / 'compiler/미리번역.sh', '--entry', 'ಕರ್ನಲ್.ಚಲಾಯಿಸು_2', '--heap-words', '1048576', '-o', ಬಿಲ್ಡ್_ಹಾದಿ / 'kernel-java.c']
        for ಚಿಹ್ನೆ_ಮೌಲ್ಯ, ವಿಧಾನ_ನಮೂದು in sorted(ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ.items()):
            ವಾದ_ಅರೇ += ['--export', ಚಿಹ್ನೆ_ಮೌಲ್ಯ + '=' + ವಿಧಾನ_ನಮೂದು]
        ಪೂರೈಸು_ಆದೇಶ(ವಾದ_ಅರೇ + sorted(ವರ್ಗ_ಹಾದಿ.glob('*.class')))
    (ಬಿಲ್ಡ್_ಹಾದಿ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = ಸಂಗ್ರಹಣೆ_ಮೂಲ / 'posix-kor/arm64-native'
    ರಚಿಸು_ಬಳಕೆದಾರ_ಸ್ಪೇಸ್(ಬಿಂಬಿಸು_ಮೂಲ, ಸಂಗ್ರಹಣೆ_ಮೂಲ, 시언어번역기, 시플플번역기, 연결편집기, ಅರ್ಖೀವ್_ಪರಿಕರ, ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ, ಪೂರೈಸು_ಆದೇಶ)
    ನೆಟ್_ವರ್ಕ್ = ರಚಿಸು_ನೆಟ್_ವರ್ಕ್_48d29d6d(ಬಿಂಬಿಸು_ಮೂಲ, 시언어번역기, ಅರ್ಖೀವ್_ಪರಿಕರ, ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ, ಪೂರೈಸು_ಆದೇಶ)
    원격사용 = ರಚಿಸು_ರಿಮೋಟ್(ಬಿಂಬಿಸು_ಮೂಲ, 시언어번역기, ಅರ್ಖೀವ್_ಪರಿಕರ, ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ, ಪೂರೈಸು_ಆದೇಶ)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', ಬಿಲ್ಡ್_ಹಾದಿ]
    빌드작업 = [(시언어번역기, [], ಬಿಲ್ಡ್_ಹಾದಿ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ಬಿಂಬಿಸು_ಮೂಲ / 'ಯಂತ್ರ/ಟರ್ಮಿನಲ್.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ಬಿಂಬಿಸು_ಮೂಲ / 'ಯಂತ್ರ/ವಿಜೆಟ್.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], ಬಿಲ್ಡ್_ಹಾದಿ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ಬಿಂಬಿಸು_ಮೂಲ / 'ಯಂತ್ರ/ಬೋರ್ಡ್.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ಬಿಂಬಿಸು_ಮೂಲ / 'ಯಂತ್ರ/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ಬಿಂಬಿಸು_ಮೂಲ / 'ಯಂತ್ರ/ಬಳಕೆದಾರ.c', 'user.o'),
            (시언어번역기, [], ಬಿಂಬಿಸು_ಮೂಲ / '부팅/ನಮೂದು_ಬಿಂದು_ಮೌಲ್ಯ.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], ಬಿಂಬಿಸು_ಮೂಲ / '시험/ಫೈಲ್_ಕರೆಗಳು.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ಫೈಲ್_ನಮೂದು for ಫೈಲ್_ನಮೂದು in ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ if ಫೈಲ್_ನಮೂದು != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ
        ಪೂರೈಸು_ಆದೇಶ([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', ಬಿಲ್ಡ್_ಹಾದಿ / 출력결과])
    ಪೂರೈಸು_ಆದೇಶ([ಅರ್ಖೀವ್_ಪರಿಕರ, 'rcs', ಬಿಲ್ಡ್_ಹಾದಿ / 'libposix-kor-arm64.a', ಬಿಲ್ಡ್_ಹಾದಿ / 'posix.o'])
    ಪೂರೈಸು_ಆದೇಶ([연결편집기, '--gc-sections', '-T', ಬಿಂಬಿಸು_ಮೂಲ / '부팅/ಜೋಡಣೆ_ಲೇಔಟ್.ld', '-Map', ಬಿಲ್ಡ್_ಹಾದಿ / 'kernel.map', '-o', ಬಿಲ್ಡ್_ಹಾದಿ / 'kernel.elf'] +
        [ಬಿಲ್ಡ್_ಹಾದಿ / ಹೆಸರು for ಹೆಸರು in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', ಬಿಲ್ಡ್_ಹಾದಿ / 'libposix-kor-arm64.a', ನೆಟ್_ವರ್ಕ್, 원격사용, ಬಿಲ್ಡ್_ಹಾದಿ / 'remote/libassh.a', ಬಿಲ್ಡ್_ಹಾದಿ / 'remote/libbearssl.a', '--end-group'])
    ಪೂರೈಸು_ಆದೇಶ([ಆಬ್ಜೆಕ್ಟ್_ಫೈಲ್_ಕನ್ವರ್ಟರ್, '-O', 'binary', ಬಿಲ್ಡ್_ಹಾದಿ / 'kernel.elf', ಬಿಲ್ಡ್_ಹಾದಿ / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'ಕನ್ನಡ.자체', 'korean_exceptions': 20,
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
    for ಹೆಸರು in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][ಹೆಸರು] = hashlib.sha256((ಬಿಲ್ಡ್_ಹಾದಿ / ಹೆಸರು).read_bytes()).hexdigest()
    (ಬಿಲ್ಡ್_ಹಾದಿ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', ಬಿಲ್ಡ್_ಹಾದಿ / 'kernel8.img')


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
