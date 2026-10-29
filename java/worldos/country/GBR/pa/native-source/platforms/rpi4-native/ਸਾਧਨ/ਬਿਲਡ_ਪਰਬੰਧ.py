#!/usr/bin/env python3
"""ਹੋਸਟ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from ਬਿਲਡ_ਉਪਭੋਗਤਾ_ਥਾਂ import ਬਣਾਓ_ਉਪਭੋਗਤਾ_ਥਾਂ
from ਬਿਲਡ_ਨੈਟਵਰਕ import ਬਣਾਓ_ਨੈਟਵਰਕ
from 예제빌드 import 예제만들기
from ਬਿਲਡ_ਰਿਮੋਟ import ਬਣਾਓ_ਰਿਮੋਟ

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]
저장소 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1]
ਬਿਲਡ_ਰਸਤਾ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build'


def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ):
    subprocess.check_call([str(첫째값) for 첫째값 in ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ], cwd=str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ))


def ਚਲਾਓ_2():
    ਬਿਲਡ_ਰਸਤਾ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ਔਬਜੈਕਟ_ਲਿਖਤ_ਪੱਤਰ_ਬਦਲਣਾ = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ਸੰਗ੍ਰਹਿ_ਸਾਧਨ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ਸਾਧਨ in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ਔਬਜੈਕਟ_ਲਿਖਤ_ਪੱਤਰ_ਬਦਲਣਾ, ਸੰਗ੍ਰਹਿ_ਸਾਧਨ):
        if not shutil.which(ਸਾਧਨ):
            raise SystemExit('필요한 ਬਿਲਡ_ਪਰਬੰਧ ਸਾਧਨ 없음: ' + ਸਾਧਨ)
    ਫੌਂਟ_ਜਾਣਕਾਰੀ = json.loads((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor/terminal-font.json').read_text())
    ਫੌਂਟ_ਸਮੱਗਰੀ = (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor/terminal-font.bin').read_bytes()
    if len(ਫੌਂਟ_ਸਮੱਗਰੀ) != 65616 * 32 or hashlib.sha256(ਫੌਂਟ_ਸਮੱਗਰੀ).hexdigest() != ਫੌਂਟ_ਜਾਣਕਾਰੀ['sha256']:
        raise SystemExit('ਟਰਮੀਨਲ ਫੌਂਟ_ਕੀਮਤ ਆਕਾਰ/SHA256 불일치')
    ਨਿਰਯਾਤ_ਤਾਲਿਕਾ = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.ਆਉਟਪੁੱਟ', 'jshell_input': '셸입출력.입력', 'java_task': 'ਪੱਕੇ_ਹੋਣਾ.작업', 'jfs_path_start': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.ਰਸਤਾ_ਸੁਰੂ',
               'jfs_path_byte': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.ਰਸਤਾ_ਬਾਈਟ', 'jfs_open': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.ਖੋਲ੍ਹੋ',
               'jfs_read': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.ਪੜ੍ਹਨ', 'jfs_write': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.ਲਿਖਣ',
               'jfs_seek': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.ਸੀਕ_ਸਥਿਤੀ_ਬਦਲੋ', 'jfs_close': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.ਬੰਦ_ਕਰੋ',
               'jfs_size': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.ਆਕਾਰ', 'jfs_unlink': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.지우기',
               'jfs_truncate': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.ਸੈਟ_ਲੰਬਾਈ'}
    ਨਿਰਯਾਤ_ਤਾਲਿਕਾ.update({'jfs_entry_count': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.파일한도', 'jfs_entry_length': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.공개이름길이', 'jfs_entry_byte': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.공개이름바이트', 'jfs_entry_size': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.공개파일크기'})
    ਨਿਰਯਾਤ_ਤਾਲਿਕਾ.update({'jdraw_prepare': '화면합성.ਤਿਆਰ_ਕਰੋ', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ਕਲਿਪ',
        'jdraw_clip_value': '화면합성.ਕਲਿਪ_ਕੀਮਤ', 'jdraw_begin': '화면합성.ਚਲਾਓ_2',
        'jdraw_end': '화면합성.ਖਤਮ_ਕਰਨਾ', 'jdraw_pixel': '화면합성.ਬਿੰਦੂ',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.ਪੌਇੰਟਰ'})
    ਨਿਰਯਾਤ_ਤਾਲਿਕਾ.update({'jfs_mkdir': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.ਬਣਾਓ_ਨਿਰਦੇਸ਼ਕ', 'jfs_rmdir': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.ਹਟਾਉਣਾ_ਨਿਰਦੇਸ਼ਕ', 'jfs_kind': 'ਮੈਮਰੀ_ਫ਼ਾਈਲਾਂ.항목종류'})
    ਨਿਰਯਾਤ_ਤਾਲਿਕਾ.update({'jnet_socket': '되돌림망.ਬਣਾਓ_ਦਾਖਲਾ', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ਈਮੇਲ',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.ਬੰਦ_ਕਰੋ'})
    ਨਿਰਯਾਤ_ਤਾਲਿਕਾ.update({'jstream_create': 'ਸਟ੍ਰੀਮ_ਨੈਟਵਰਕ.ਬਣਾਓ_ਦਾਖਲਾ', 'jstream_bind': 'ਸਟ੍ਰੀਮ_ਨੈਟਵਰਕ.묶기', 'jstream_listen': 'ਸਟ੍ਰੀਮ_ਨੈਟਵਰਕ.듣기', 'jstream_connect': 'ਸਟ੍ਰੀਮ_ਨੈਟਵਰਕ.ਕੁਨੈਕਸ਼ਨ_ਕਰੋ', 'jstream_accept': 'ਸਟ੍ਰੀਮ_ਨੈਟਵਰਕ.ਸਵੀਕਾਰ_ਕਰੋ_ਸਬੰਧ', 'jstream_read': 'ਸਟ੍ਰੀਮ_ਨੈਟਵਰਕ.ਪੜ੍ਹਨ', 'jstream_write': 'ਸਟ੍ਰੀਮ_ਨੈਟਵਰਕ.ਲਿਖਣ', 'jstream_port': 'ਸਟ੍ਰੀਮ_ਨੈਟਵਰਕ.창구읽기', 'jstream_peer': 'ਸਟ੍ਰੀਮ_ਨੈਟਵਰਕ.상대창구읽기', 'jstream_close': 'ਸਟ੍ਰੀਮ_ਨੈਟਵਰਕ.ਬੰਦ_ਕਰੋ'})
    for ਪ੍ਰਤੀਕ_ਕੀਮਤ in list(ਨਿਰਯਾਤ_ਤਾਲਿਕਾ):
        if ਪ੍ਰਤੀਕ_ਕੀਮਤ.startswith('jstream_') or ਪ੍ਰਤੀਕ_ਕੀਮਤ.startswith('jnet_') and ਪ੍ਰਤੀਕ_ਕੀਮਤ not in ('jnet_put', 'jnet_get'):
            ਨਿਰਯਾਤ_ਤਾਲਿਕਾ[ਪ੍ਰਤੀਕ_ਕੀਮਤ.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ਨਿਰਯਾਤ_ਤਾਲਿਕਾ.pop(ਪ੍ਰਤੀਕ_ਕੀਮਤ)
    예제들 = ['public final class ਬੰਡਲ { public static void ਤਿਆਰ_ਕਰੋ() {']
    for ਮਾਰਗ in sorted((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '예제').iterdir()):
        if ਮਾਰਗ.is_file():
            예제들.append('명령해석기.ਸਥਾਈ_ਲਿਖਤ_ਪੱਤਰ(%s, %s);' %
                (json.dumps(ਮਾਰਗ.name), json.dumps(ਮਾਰਗ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (ਬਿਲਡ_ਰਸਤਾ / 'ਬੰਡਲ.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, 저장소, ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(ਬਿਲਡ_ਰਸਤਾ)) as 작업경로:
        ਸ੍ਰੇਣੀ_ਰਸਤਾ = Path(작업경로)
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ਸ੍ਰੇਣੀ_ਰਸਤਾ, '-sourcepath', ਸ੍ਰੇਣੀ_ਰਸਤਾ, '-d', ਸ੍ਰੇਣੀ_ਰਸਤਾ] + sorted((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਸਰੋਤ').glob('*.java')) + [ਬਿਲਡ_ਰਸਤਾ / 'ਬੰਡਲ.java', ਬਿਲਡ_ਰਸਤਾ / '예제꾸러미.java'])
        # ਫਾਇਲ·ਸ਼ੈਲ·ਵਿੰਡੋ 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'ਪੱਕੇ_ਹੋਣਾ.ਚਲਾਓ_2', '--heap-words', '1048576', '-o', ਬਿਲਡ_ਰਸਤਾ / 'kernel-java.c']
        for ਪ੍ਰਤੀਕ_ਕੀਮਤ, ਮੈਥਡ_ਦਾਖਲਾ in sorted(ਨਿਰਯਾਤ_ਤਾਲਿਕਾ.items()):
            ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ += ['--export', ਪ੍ਰਤੀਕ_ਕੀਮਤ + '=' + ਮੈਥਡ_ਦਾਖਲਾ]
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ + sorted(ਸ੍ਰੇਣੀ_ਰਸਤਾ.glob('*.class')))
    (ਬਿਲਡ_ਰਸਤਾ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    ਬਣਾਓ_ਉਪਭੋਗਤਾ_ਥਾਂ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, 저장소, 시언어번역기, 시플플번역기, 연결편집기, ਸੰਗ੍ਰਹਿ_ਸਾਧਨ, 설정비트, ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼)
    ਨੈਟਵਰਕ = ਬਣਾਓ_ਨੈਟਵਰਕ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, 시언어번역기, ਸੰਗ੍ਰਹਿ_ਸਾਧਨ, 설정비트, ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼)
    원격사용 = ਬਣਾਓ_ਰਿਮੋਟ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, 시언어번역기, ਸੰਗ੍ਰਹਿ_ਸਾਧਨ, 설정비트, ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', ਬਿਲਡ_ਰਸਤਾ]
    빌드작업 = [(시언어번역기, [], ਬਿਲਡ_ਰਸਤਾ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਮਸ਼ੀਨ/ਟਰਮੀਨਲ.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਮਸ਼ੀਨ/ਵਿਜੇਟ.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], ਬਿਲਡ_ਰਸਤਾ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਮਸ਼ੀਨ/ਬੋਰਡ.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਮਸ਼ੀਨ/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਮਸ਼ੀਨ/ਉਪਭੋਗਤਾ.c', 'user.o'),
            (시언어번역기, [], ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '부팅/ਦਾਖਲਾ_ਪੌਇੰਟ_ਕੀਮਤ.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '시험/ਲਿਖਤ_ਪੱਤਰ_ਕਾਲਾਂ.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ for ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ in 설정비트 if ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', ਬਿਲਡ_ਰਸਤਾ / 출력결과])
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([ਸੰਗ੍ਰਹਿ_ਸਾਧਨ, 'rcs', ਬਿਲਡ_ਰਸਤਾ / 'libposix-kor-arm64.a', ਬਿਲਡ_ਰਸਤਾ / 'posix.o'])
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([연결편집기, '--gc-sections', '-T', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '부팅/ਲਿੰਕ_ਖਾਕਾ.ld', '-Map', ਬਿਲਡ_ਰਸਤਾ / 'kernel.map', '-o', ਬਿਲਡ_ਰਸਤਾ / 'kernel.elf'] +
        [ਬਿਲਡ_ਰਸਤਾ / ਨਾਂ for ਨਾਂ in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', ਬਿਲਡ_ਰਸਤਾ / 'libposix-kor-arm64.a', ਨੈਟਵਰਕ, 원격사용, ਬਿਲਡ_ਰਸਤਾ / 'remote/libassh.a', ਬਿਲਡ_ਰਸਤਾ / 'remote/libbearssl.a', '--end-group'])
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([ਔਬਜੈਕਟ_ਲਿਖਤ_ਪੱਤਰ_ਬਦਲਣਾ, '-O', 'binary', ਬਿਲਡ_ਰਸਤਾ / 'kernel.elf', ਬਿਲਡ_ਰਸਤਾ / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'ਪੰਜਾਬੀ.자체', 'korean_exceptions': 20,
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
    for ਨਾਂ in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][ਨਾਂ] = hashlib.sha256((ਬਿਲਡ_ਰਸਤਾ / ਨਾਂ).read_bytes()).hexdigest()
    (ਬਿਲਡ_ਰਸਤਾ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', ਬਿਲਡ_ਰਸਤਾ / 'kernel8.img')


if __name__ == '__main__':
    ਚਲਾਓ_2()
