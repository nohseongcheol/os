"""독립된 자체 ABI ELF64와 로더 ପ୍ରତ୍ୟାକ୍ଷାନ_ମୂଲ୍ୟ 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def ସୃଷ୍ଟି_ଉପଭୋକ୍ତା_ସ୍ଥାନ(ରୁଟ୍_ପଥ, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, ଅଭିଲେଖାଗାର_ଉପକରଣ, 설정비트, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ):
    설정비트 = [ସେଟିଂସ୍_ମୂଲ୍ୟ for ସେଟିଂସ୍_ମୂଲ୍ୟ in 설정비트 if ସେଟିଂସ୍_ମୂଲ୍ୟ != '-mgeneral-regs-only']
    ବିଲ୍ଡ୍_ପଥ = ରୁଟ୍_ପଥ / 'build'
    출력결과 = ବିଲ୍ଡ୍_ପଥ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = ରୁଟ୍_ପଥ / 'ଉପଭୋକ୍ତା'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, ପଥ, ନାମ in [
            (시언어번역기, [], 원본자료 / 'ଚଳାନ୍ତୁ.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'ଉପଭୋକ୍ତା_ବ୍ରିଜ୍.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ସଂପାଦକ.c', 'vi.o')]:
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', ପଥ, '-o', 출력결과 / ନାମ])
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([ଅଭିଲେଖାଗାର_ଉପକରଣ, 'rcs', ବିଲ୍ଡ୍_ପଥ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for ନାମ in ('demo', 'fault', 'network', 'vi'):
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([연결편집기, '-T', 원본자료 / 'ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (ନାମ + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (ନାମ + '.o'), ବିଲ୍ଡ୍_ପଥ / 'libposix-kor-user.a'])
    자바라이브러리만들기(ରୁଟ୍_ପଥ, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(ବିଲ୍ଡ୍_ପଥ)) as 작업경로:
        ଶ୍ରେଣୀ_ପଥ = Path(작업경로)
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ଶ୍ରେଣୀ_ପଥ, '-sourcepath', ଶ୍ରେଣୀ_ପଥ, '-d', ଶ୍ରେଣୀ_ପଥ] +
            [ଡାଟା_ସ୍ଥିତି for ଡାଟା_ସ୍ଥିତି in sorted((저장소경로 / 'os/ଉପଭୋକ୍ତା/자바').glob('*.java')) if ଡାଟା_ସ୍ଥିତି.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'ଉପକରଣ_ଏଣ୍ଟ୍ରି.ଚଳାନ୍ତୁ',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(ଶ୍ରେଣୀ_ପଥ.glob('*.class')))
    압축해제경로 = ରୁଟ୍_ପଥ / 'vendor/uzlib'
    for ପଥ, ନାମ in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'ବଣ୍ଡଲ୍.c', 'jar.o')] + [(압축해제경로 / (ନାମ + '.c'), ନାମ + '.o') for ନାମ in ('tinflate', 'crc32', 'adler32')]:
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', ପଥ, '-o', 출력결과 / ନାମ])
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([연결편집기, '-T', 원본자료 / 'ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / ନାମ for ନାମ in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(ରୁଟ୍_ପଥ, 시언어번역기, 연결편집기)
    시언어번역기만들기(ରୁଟ୍_ପଥ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    ଅନୁପ୍ରୟୋଗ_ଶୀର୍ଷକ_ଅଫ୍_ସେଟ୍ = struct.unpack_from('<Q', 유효함, 32)[0]
    ଶୀର୍ଷକ_ତାଲିକା = [ଅନୁପ୍ରୟୋଗ_ଶୀର୍ଷକ_ଅଫ୍_ସେଟ୍ + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [ଡାଟା_ସ୍ଥିତି for ଡାଟା_ସ୍ଥିତି in ଶୀର୍ଷକ_ତାଲିକା if struct.unpack_from('<I', 유효함, ଡାଟା_ସ୍ଥିତି)[0] == 1]
    ପାଠ୍ଯ, ଡାଟା = 적재구획[:2]
    ନିର୍ଦ୍ଦେଶ_ଠିକଣା = struct.unpack_from('<Q', 유효함, ପାଠ୍ଯ + 16)[0]
    ଡାଟା_ଠିକଣା = struct.unpack_from('<Q', 유효함, ଡାଟା + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ନିର୍ଦ୍ଦେଶ_ଠିକଣା + 1), ('data-entry', 24, 'Q', ଡାଟା_ଠିକଣା),
               ('outside-file', ପାଠ୍ଯ + 32, 'Q', len(유효함) + 1), ('short-memory', ପାଠ୍ଯ + 40, 'Q', 1),
               ('kernel-address', ପାଠ୍ଯ + 16, 'Q', 0x80000), ('memory-overflow', ପାଠ୍ଯ + 40, 'Q', 2**64 - 1),
               ('writable-code', ପାଠ୍ଯ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', ପାଠ୍ଯ, 'I', 2),
               ('unaligned-load', ପାଠ୍ଯ + 16, 'Q', ନିର୍ଦ୍ଦେଶ_ଠିକଣା + 8),
               ('overlap', ଡାଟା + 16, 'Q', ନିର୍ଦ୍ଦେଶ_ଠିକଣା)]
    for ନାମ, ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ, ଫର୍ମାଟ୍_932e03c8, ମୂଲ୍ୟ in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + ଫର୍ମାଟ୍_932e03c8, 바뀐자료, ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ, ମୂଲ୍ୟ)
        시험사례.append((ନାମ, bytes(바뀐자료)))
    탑재덩이들 = [(ନାମ.replace('-', '_'), 출력결과 / (ନାମ + '.elf')) for ନାମ in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା, (ନାମ, ପେଲୋଡ୍_ଡାଟା) in enumerate(시험사례):
        ପଥ = 출력결과 / ('invalid-{}.elf'.format(ନାମ)); ପଥ.write_bytes(ପେଲୋଡ୍_ଡାଟା)
        탑재덩이들.append(('invalid_{}'.format(ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା), ପଥ))
    어셈블리자료, ଶୀର୍ଷକ_ମୂଲ୍ୟ = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for ନାମ, ପଥ in 탑재덩이들:
        ସଙ୍କେତ_ମୂଲ୍ୟ = 'user_blob_' + ନାମ
        크기목록[ନାମ] = ପଥ.stat().st_size
        # 생성한 ସମକକ୍ଷ_ମୂଲ୍ୟ 경로만 넣어 프로젝트 경로의 공백/କ୍ୟୁଏଟ୍ 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + ସଙ୍କେତ_ମୂଲ୍ୟ, ସଙ୍କେତ_ମୂଲ୍ୟ + ':', '.incbin "{}"'.format(ପଥ.relative_to(ରୁଟ୍_ପଥ))]
        ଶୀର୍ଷକ_ମୂଲ୍ୟ.append('extern const unsigned char {}[];'.format(ସଙ୍କେତ_ମୂଲ୍ୟ))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    ଶୀର୍ଷକ_ମୂଲ୍ୟ += ['static const ଅନୁପ୍ରୟୋଗ 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    ଶୀର୍ଷକ_ମୂଲ୍ୟ += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    ଶୀର୍ଷକ_ମୂଲ୍ୟ += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    ଶୀର୍ଷକ_ମୂଲ୍ୟ += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], ପଦ୍ଧତି_ମୋଡ୍) for ପଦ୍ଧତି_ମୋଡ୍ in (0, 1)]
    ଶୀର୍ଷକ_ମୂଲ୍ୟ += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    ଶୀର୍ଷକ_ମୂଲ୍ୟ += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    ଶୀର୍ଷକ_ମୂଲ୍ୟ += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    ଶୀର୍ଷକ_ମୂଲ୍ୟ += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    ଶୀର୍ଷକ_ମୂଲ୍ୟ += ['};', 'static const ଅନୁପ୍ରୟୋଗ 잘못된실행항목들[] = {']
    ଶୀର୍ଷକ_ମୂଲ୍ୟ += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ପେଲୋଡ୍_ଡାଟା)) for 순번, (_, ପେଲୋଡ୍_ଡାଟା) in enumerate(시험사례)]
    ଶୀର୍ଷକ_ମୂଲ୍ୟ += ['};']
    (ବିଲ୍ଡ୍_ପଥ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (ବିଲ୍ଡ୍_ପଥ / 'programs.h').write_text('\n'.join(ଶୀର୍ଷକ_ମୂଲ୍ୟ) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(ନାମ for ନାମ, _ in 시험사례) + '\n')
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([시언어번역기] + 설정비트 + ['-c', ବିଲ୍ଡ୍_ପଥ / 'programs.S', '-o', ବିଲ୍ଡ୍_ପଥ / 'programs.o'])
