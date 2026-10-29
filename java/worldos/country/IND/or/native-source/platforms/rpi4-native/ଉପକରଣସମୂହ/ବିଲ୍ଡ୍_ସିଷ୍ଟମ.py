#!/usr/bin/env python3
"""ଆୟୋଜକ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from ବିଲ୍ଡ୍_ଉପଭୋକ୍ତା_ସ୍ଥାନ import ସୃଷ୍ଟି_ଉପଭୋକ୍ତା_ସ୍ଥାନ
from ବିଲ୍ଡ୍_ନେଟ୍_ୱାର୍କ୍ import ସୃଷ୍ଟି_ନେଟ୍_ୱାର୍କ୍
from 예제빌드 import 예제만들기
from ବିଲ୍ଡ୍_ଦୂରବର୍ତ୍ତୀ import ସୃଷ୍ଟି_ଦୂରବର୍ତ୍ତୀ

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]
저장소 = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1]
ବିଲ୍ଡ୍_ପଥ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build'


def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ଯୁକ୍ତି_ଆରେ):
    subprocess.check_call([str(첫째값) for 첫째값 in ଯୁକ୍ତି_ଆରେ], cwd=str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍))


def ଚଳାନ୍ତୁ():
    ବିଲ୍ଡ୍_ପଥ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ଅବଜେକ୍ଟ_ଫାଇଲ୍_କନର୍ଭଟର୍ = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ଅଭିଲେଖାଗାର_ଉପକରଣ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ଉପକରଣସମୂହ in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ଅବଜେକ୍ଟ_ଫାଇଲ୍_କନର୍ଭଟର୍, ଅଭିଲେଖାଗାର_ଉପକରଣ):
        if not shutil.which(ଉପକରଣସମୂହ):
            raise SystemExit('필요한 ବିଲ୍ଡ୍_ସିଷ୍ଟମ ଉପକରଣସମୂହ 없음: ' + ଉପକରଣସମୂହ)
    ଫଣ୍ଟ_ସୂଚନା = json.loads((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/terminal-font.json').read_text())
    ଫଣ୍ଟ_ଡାଟା = (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/terminal-font.bin').read_bytes()
    if len(ଫଣ୍ଟ_ଡାଟା) != 65616 * 32 or hashlib.sha256(ଫଣ୍ଟ_ଡାଟା).hexdigest() != ଫଣ୍ଟ_ସୂଚନା['sha256']:
        raise SystemExit('ଟର୍ମିନାଲ ଫଣ୍ଟ_ମୂଲ୍ୟ ଆକାର/SHA256 불일치')
    ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ = {'jshell_interactive': '셸입출력.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ', 'jshell_output': '셸입출력.ନିର୍ଗମ', 'jshell_input': '셸입출력.입력', 'java_task': 'କେନ୍ଦ୍ରିକ.작업', 'jfs_path_start': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.ପଥ_ଆରମ୍ଭ',
               'jfs_path_byte': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.ପଥ_ବାଇଟ୍', 'jfs_open': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.ଖୋଲନ୍ତୁ',
               'jfs_read': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.ପଢନ୍ତୁ', 'jfs_write': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.ଲେଖନ୍ତୁ',
               'jfs_seek': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.ସୀକ୍_ସ୍ଥିତି', 'jfs_close': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.ବନ୍ଦ_କରନ୍ତୁ',
               'jfs_size': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.ଆକାର', 'jfs_unlink': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.지우기',
               'jfs_truncate': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.ସେଟ୍_ଦୈର୍ଘ୍ୟ'}
    ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ.update({'jfs_entry_count': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.파일한도', 'jfs_entry_length': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.공개이름길이', 'jfs_entry_byte': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.공개이름바이트', 'jfs_entry_size': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.공개파일크기'})
    ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ.update({'jdraw_prepare': '화면합성.ପ୍ରସ୍ତୁତ', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.କ୍ଲିପ୍',
        'jdraw_clip_value': '화면합성.କ୍ଲିପ୍_ମୂଲ୍ୟ', 'jdraw_begin': '화면합성.ଚଳାନ୍ତୁ',
        'jdraw_end': '화면합성.ସମାପ୍ତ', 'jdraw_pixel': '화면합성.ପିକ୍ସେଲ୍',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.ପଏଣ୍ଟର୍'})
    ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ.update({'jfs_mkdir': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.ସୃଷ୍ଟି_ଡିରେକ୍ଟୋରୀ', 'jfs_rmdir': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.ଅପସାରଣ_କରିବା_ଡିରେକ୍ଟୋରୀ', 'jfs_kind': 'ମୋମରୀ_ଫାଇଲ୍_ଗୁଡିକ.항목종류'})
    ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ.update({'jnet_socket': '되돌림망.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ପଠାନ୍ତୁ',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.ବନ୍ଦ_କରନ୍ତୁ'})
    ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ.update({'jstream_create': 'ଷ୍ଟ୍ରିମ୍_ନେଟ୍_ୱାର୍କ୍.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି', 'jstream_bind': 'ଷ୍ଟ୍ରିମ୍_ନେଟ୍_ୱାର୍କ୍.묶기', 'jstream_listen': 'ଷ୍ଟ୍ରିମ୍_ନେଟ୍_ୱାର୍କ୍.듣기', 'jstream_connect': 'ଷ୍ଟ୍ରିମ୍_ନେଟ୍_ୱାର୍କ୍.ସଂଯୋଗ_କରନ୍ତୁ', 'jstream_accept': 'ଷ୍ଟ୍ରିମ୍_ନେଟ୍_ୱାର୍କ୍.ସ୍ୱୀକାର_କରିବା_ସଂଯୋଗ', 'jstream_read': 'ଷ୍ଟ୍ରିମ୍_ନେଟ୍_ୱାର୍କ୍.ପଢନ୍ତୁ', 'jstream_write': 'ଷ୍ଟ୍ରିମ୍_ନେଟ୍_ୱାର୍କ୍.ଲେଖନ୍ତୁ', 'jstream_port': 'ଷ୍ଟ୍ରିମ୍_ନେଟ୍_ୱାର୍କ୍.창구읽기', 'jstream_peer': 'ଷ୍ଟ୍ରିମ୍_ନେଟ୍_ୱାର୍କ୍.상대창구읽기', 'jstream_close': 'ଷ୍ଟ୍ରିମ୍_ନେଟ୍_ୱାର୍କ୍.ବନ୍ଦ_କରନ୍ତୁ'})
    for ସଙ୍କେତ_ମୂଲ୍ୟ in list(ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ):
        if ସଙ୍କେତ_ମୂଲ୍ୟ.startswith('jstream_') or ସଙ୍କେତ_ମୂଲ୍ୟ.startswith('jnet_') and ସଙ୍କେତ_ମୂଲ୍ୟ not in ('jnet_put', 'jnet_get'):
            ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ[ସଙ୍କେତ_ମୂଲ୍ୟ.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ.pop(ସଙ୍କେତ_ମୂଲ୍ୟ)
    예제들 = ['public final class ବଣ୍ଡଲ୍ { public static void ପ୍ରସ୍ତୁତ() {']
    for ପଥ in sorted((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '예제').iterdir()):
        if ପଥ.is_file():
            예제들.append('명령해석기.ସ୍ଥିର_ଫାଇଲ୍(%s, %s);' %
                (json.dumps(ପଥ.name), json.dumps(ପଥ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (ବିଲ୍ଡ୍_ପଥ / 'ବଣ୍ଡଲ୍.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, 저장소, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(ବିଲ୍ଡ୍_ପଥ)) as 작업경로:
        ଶ୍ରେଣୀ_ପଥ = Path(작업경로)
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ଶ୍ରେଣୀ_ପଥ, '-sourcepath', ଶ୍ରେଣୀ_ପଥ, '-d', ଶ୍ରେଣୀ_ପଥ] + sorted((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉତ୍ସ').glob('*.java')) + [ବିଲ୍ଡ୍_ପଥ / 'ବଣ୍ଡଲ୍.java', ବିଲ୍ଡ୍_ପଥ / '예제꾸러미.java'])
        # ଫାଇଲ·ଖୋଳ·ଓ୍ୱିଣ୍ଡୋ 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ଯୁକ୍ତି_ଆରେ = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'କେନ୍ଦ୍ରିକ.ଚଳାନ୍ତୁ', '--heap-words', '1048576', '-o', ବିଲ୍ଡ୍_ପଥ / 'kernel-java.c']
        for ସଙ୍କେତ_ମୂଲ୍ୟ, ପଦ୍ଧତି_ଏଣ୍ଟ୍ରି in sorted(ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ.items()):
            ଯୁକ୍ତି_ଆରେ += ['--export', ସଙ୍କେତ_ମୂଲ୍ୟ + '=' + ପଦ୍ଧତି_ଏଣ୍ଟ୍ରି]
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ଯୁକ୍ତି_ଆରେ + sorted(ଶ୍ରେଣୀ_ପଥ.glob('*.class')))
    (ବିଲ୍ଡ୍_ପଥ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    ସୃଷ୍ଟି_ଉପଭୋକ୍ତା_ସ୍ଥାନ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, 저장소, 시언어번역기, 시플플번역기, 연결편집기, ଅଭିଲେଖାଗାର_ଉପକରଣ, 설정비트, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ)
    ନେଟ୍_ୱାର୍କ୍ = ସୃଷ୍ଟି_ନେଟ୍_ୱାର୍କ୍(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, 시언어번역기, ଅଭିଲେଖାଗାର_ଉପକରଣ, 설정비트, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ)
    원격사용 = ସୃଷ୍ଟି_ଦୂରବର୍ତ୍ତୀ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, 시언어번역기, ଅଭିଲେଖାଗାର_ଉପକରଣ, 설정비트, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', ବିଲ୍ଡ୍_ପଥ]
    빌드작업 = [(시언어번역기, [], ବିଲ୍ଡ୍_ପଥ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ମେସିନ୍/ଟର୍ମିନାଲ.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ମେସିନ୍/ୱିଜାର୍ଡ୍.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], ବିଲ୍ଡ୍_ପଥ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ମେସିନ୍/ବୋର୍ଡ୍.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ମେସିନ୍/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ମେସିନ୍/ଉପଭୋକ୍ତା.c', 'user.o'),
            (시언어번역기, [], ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '부팅/ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍_ମୂଲ୍ୟ.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'ସଂଯୋଗ_କରନ୍ତୁ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '시험/ଫାଇଲ୍_କଲ୍ସ.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ଫାଇଲ୍_ଏଣ୍ଟ୍ରି for ଫାଇଲ୍_ଏଣ୍ଟ୍ରି in 설정비트 if ଫାଇଲ୍_ଏଣ୍ଟ୍ରି != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', ବିଲ୍ଡ୍_ପଥ / 출력결과])
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([ଅଭିଲେଖାଗାର_ଉପକରଣ, 'rcs', ବିଲ୍ଡ୍_ପଥ / 'libposix-kor-arm64.a', ବିଲ୍ଡ୍_ପଥ / 'posix.o'])
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([연결편집기, '--gc-sections', '-T', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '부팅/ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld', '-Map', ବିଲ୍ଡ୍_ପଥ / 'kernel.map', '-o', ବିଲ୍ଡ୍_ପଥ / 'kernel.elf'] +
        [ବିଲ୍ଡ୍_ପଥ / ନାମ for ନାମ in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', ବିଲ୍ଡ୍_ପଥ / 'libposix-kor-arm64.a', ନେଟ୍_ୱାର୍କ୍, 원격사용, ବିଲ୍ଡ୍_ପଥ / 'remote/libassh.a', ବିଲ୍ଡ୍_ପଥ / 'remote/libbearssl.a', '--end-group'])
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([ଅବଜେକ୍ଟ_ଫାଇଲ୍_କନର୍ଭଟର୍, '-O', 'binary', ବିଲ୍ଡ୍_ପଥ / 'kernel.elf', ବିଲ୍ଡ୍_ପଥ / 'kernel8.img'])
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
    for ନାମ in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][ନାମ] = hashlib.sha256((ବିଲ୍ଡ୍_ପଥ / ନାମ).read_bytes()).hexdigest()
    (ବିଲ୍ଡ୍_ପଥ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', ବିଲ୍ଡ୍_ପଥ / 'kernel8.img')


if __name__ == '__main__':
    ଚଳାନ୍ତୁ()
