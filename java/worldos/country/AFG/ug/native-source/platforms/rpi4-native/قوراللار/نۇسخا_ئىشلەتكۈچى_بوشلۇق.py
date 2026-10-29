"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def قۇرۇش_ئىشلەتكۈچى_بوشلۇق(يىلتىز_يول, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, ئارخىپ_قورال, 설정비트, ئىجرا_قىلىش_بۇيرۇق):
    설정비트 = [تەڭشەك_قىممىتى for تەڭشەك_قىممىتى in 설정비트 if تەڭشەك_قىممىتى != '-mgeneral-regs-only']
    نۇسخا_يول = يىلتىز_يول / 'build'
    출력결과 = نۇسخا_يول / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = يىلتىز_يول / 'ئىشلەتكۈچى'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, يول, ئاتى in [
            (시언어번역기, [], 원본자료 / 'ئىجرا_قىل_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ئىجرا_قىلىش_بۇيرۇق.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'ئىشلەتكۈچى_كۆۋرۈك.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'تەھرىرلىگۈچ.c', 'vi.o')]:
        ئىجرا_قىلىش_بۇيرۇق([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', يول, '-o', 출력결과 / ئاتى])
    ئىجرا_قىلىش_بۇيرۇق([ئارخىپ_قورال, 'rcs', نۇسخا_يول / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for ئاتى in ('demo', 'fault', 'network', 'vi'):
        ئىجرا_قىلىش_بۇيرۇق([연결편집기, '-T', 원본자료 / 'ئۇلانما_لايىھە.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (ئاتى + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (ئاتى + '.o'), نۇسخا_يول / 'libposix-kor-user.a'])
    자바라이브러리만들기(يىلتىز_يول, ئىجرا_قىلىش_بۇيرۇق)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(نۇسخا_يول)) as 작업경로:
        تۈركۈم_يول = Path(작업경로)
        ئىجرا_قىلىش_بۇيرۇق(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', تۈركۈم_يول, '-sourcepath', تۈركۈم_يول, '-d', تۈركۈم_يول] +
            [مەلۇمات_ئورۇنلاشتۇرۇش for مەلۇمات_ئورۇنلاشتۇرۇش in sorted((저장소경로 / 'os/ئىشلەتكۈچى/자바').glob('*.java')) if مەلۇمات_ئورۇنلاشتۇرۇش.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ئىجرا_قىلىش_بۇيرۇق(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'قورال_كىرگۈزۈش.ئىجرا_قىل_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(تۈركۈم_يول.glob('*.class')))
    압축해제경로 = يىلتىز_يول / 'vendor/uzlib'
    for يول, ئاتى in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'توپلام.c', 'jar.o')] + [(압축해제경로 / (ئاتى + '.c'), ئاتى + '.o') for ئاتى in ('tinflate', 'crc32', 'adler32')]:
        ئىجرا_قىلىش_بۇيرۇق([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', يول, '-o', 출력결과 / ئاتى])
    ئىجرا_قىلىش_بۇيرۇق([연결편집기, '-T', 원본자료 / 'ئۇلانما_لايىھە.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / ئاتى for ئاتى in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(يىلتىز_يول, 시언어번역기, 연결편집기)
    시언어번역기만들기(يىلتىز_يول, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ئىجرا_قىلىش_بۇيرۇق)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    ئەپ_بېشى_ئاغما = struct.unpack_from('<Q', 유효함, 32)[0]
    بېشى_تىزىم = [ئەپ_بېشى_ئاغما + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [مەلۇمات_ئورۇنلاشتۇرۇش for مەلۇمات_ئورۇنلاشتۇرۇش in بېشى_تىزىم if struct.unpack_from('<I', 유효함, مەلۇمات_ئورۇنلاشتۇرۇش)[0] == 1]
    تېكىست, مەلۇمات = 적재구획[:2]
    بۇيرۇق_ئادرېس = struct.unpack_from('<Q', 유효함, تېكىست + 16)[0]
    مەلۇمات_ئادرېس = struct.unpack_from('<Q', 유효함, مەلۇمات + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', بۇيرۇق_ئادرېس + 1), ('data-entry', 24, 'Q', مەلۇمات_ئادرېس),
               ('outside-file', تېكىست + 32, 'Q', len(유효함) + 1), ('short-memory', تېكىست + 40, 'Q', 1),
               ('kernel-address', تېكىست + 16, 'Q', 0x80000), ('memory-overflow', تېكىست + 40, 'Q', 2**64 - 1),
               ('writable-code', تېكىست + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', تېكىست, 'I', 2),
               ('unaligned-load', تېكىست + 16, 'Q', بۇيرۇق_ئادرېس + 8),
               ('overlap', مەلۇمات + 16, 'Q', بۇيرۇق_ئادرېس)]
    for ئاتى, ئاغما_قىممىتى, فورمات_932e03c8, قىممىتى in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + فورمات_932e03c8, 바뀐자료, ئاغما_قىممىتى, قىممىتى)
        시험사례.append((ئاتى, bytes(바뀐자료)))
    탑재덩이들 = [(ئاتى.replace('-', '_'), 출력결과 / (ئاتى + '.elf')) for ئاتى in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for ئىزدەش_ئىندېكس, (ئاتى, يۈك_مەلۇمات) in enumerate(시험사례):
        يول = 출력결과 / ('invalid-{}.elf'.format(ئاتى)); يول.write_bytes(يۈك_مەلۇمات)
        탑재덩이들.append(('invalid_{}'.format(ئىزدەش_ئىندېكس), يول))
    어셈블리자료, بېشى_قىممىتى = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for ئاتى, يول in 탑재덩이들:
        بەلگە_قىممىتى = 'user_blob_' + ئاتى
        크기목록[ئاتى] = يول.stat().st_size
        # 생성한 باراۋەرلىك_قىممىتى 경로만 넣어 프로젝트 경로의 공백/نەقىل 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + بەلگە_قىممىتى, بەلگە_قىممىتى + ':', '.incbin "{}"'.format(يول.relative_to(يىلتىز_يول))]
        بېشى_قىممىتى.append('extern const unsigned char {}[];'.format(بەلگە_قىممىتى))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    بېشى_قىممىتى += ['static const ئەپ 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    بېشى_قىممىتى += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    بېشى_قىممىتى += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    بېشى_قىممىتى += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], ئۇسۇل_ھالەت) for ئۇسۇل_ھالەت in (0, 1)]
    بېشى_قىممىتى += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    بېشى_قىممىتى += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    بېشى_قىممىتى += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    بېشى_قىممىتى += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    بېشى_قىممىتى += ['};', 'static const ئەپ 잘못된실행항목들[] = {']
    بېشى_قىممىتى += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(يۈك_مەلۇمات)) for 순번, (_, يۈك_مەلۇمات) in enumerate(시험사례)]
    بېشى_قىممىتى += ['};']
    (نۇسخا_يول / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (نۇسخا_يول / 'programs.h').write_text('\n'.join(بېشى_قىممىتى) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(ئاتى for ئاتى, _ in 시험사례) + '\n')
    ئىجرا_قىلىش_بۇيرۇق([시언어번역기] + 설정비트 + ['-c', نۇسخا_يول / 'programs.S', '-o', نۇسخا_يول / 'programs.o'])
