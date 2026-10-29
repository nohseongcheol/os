"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def ক্ৰিয়েট_ব্যৱহাৰকৰ্তা_স্থান(ৰুট_পথ, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, অভিলেখাগাৰ_সঁজুলি, 설정비트, নিষ্পাদন_আদেশ):
    설정비트 = [ছেটিংছ_মান for ছেটিংছ_মান in 설정비트 if ছেটিংছ_মান != '-mgeneral-regs-only']
    বিল্ড_পথ = ৰুট_পথ / 'build'
    출력결과 = বিল্ড_পথ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = ৰুট_পথ / 'ব্যৱহাৰকৰ্তা'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, পথ, নাম in [
            (시언어번역기, [], 원본자료 / 'সঞ্চালন.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'নিষ্পাদন_আদেশ.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'ব্যৱহাৰকৰ্তা_ব্ৰীজ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'সম্পাদক.c', 'vi.o')]:
        নিষ্পাদন_আদেশ([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', পথ, '-o', 출력결과 / নাম])
    নিষ্পাদন_আদেশ([অভিলেখাগাৰ_সঁজুলি, 'rcs', বিল্ড_পথ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for নাম in ('demo', 'fault', 'network', 'vi'):
        নিষ্পাদন_আদেশ([연결편집기, '-T', 원본자료 / 'লিংক_লেআউট.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (নাম + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (নাম + '.o'), বিল্ড_পথ / 'libposix-kor-user.a'])
    자바라이브러리만들기(ৰুট_পথ, নিষ্পাদন_আদেশ)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(বিল্ড_পথ)) as 작업경로:
        শ্ৰেণী_পথ = Path(작업경로)
        নিষ্পাদন_আদেশ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', শ্ৰেণী_পথ, '-sourcepath', শ্ৰেণী_পথ, '-d', শ্ৰেণী_পথ] +
            [ডাটা_স্থান_সলনি_কৰক for ডাটা_স্থান_সলনি_কৰক in sorted((저장소경로 / 'os/ব্যৱহাৰকৰ্তা/자바').glob('*.java')) if ডাটা_স্থান_সলনি_কৰক.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        নিষ্পাদন_আদেশ(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'সঁজুলি_প্রবিষ্ট.সঞ্চালন',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(শ্ৰেণী_পথ.glob('*.class')))
    압축해제경로 = ৰুট_পথ / 'vendor/uzlib'
    for পথ, নাম in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'বাণ্ডল.c', 'jar.o')] + [(압축해제경로 / (নাম + '.c'), নাম + '.o') for নাম in ('tinflate', 'crc32', 'adler32')]:
        নিষ্পাদন_আদেশ([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', পথ, '-o', 출력결과 / নাম])
    নিষ্পাদন_আদেশ([연결편집기, '-T', 원본자료 / 'লিংক_লেআউট.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / নাম for নাম in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(ৰুট_পথ, 시언어번역기, 연결편집기)
    시언어번역기만들기(ৰুট_পথ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, নিষ্পাদন_আদেশ)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    এপ্প্_শিৰো_অফছেট = struct.unpack_from('<Q', 유효함, 32)[0]
    শিৰো_সূচী = [এপ্প্_শিৰো_অফছেট + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [ডাটা_স্থান_সলনি_কৰক for ডাটা_স্থান_সলনি_কৰক in শিৰো_সূচী if struct.unpack_from('<I', 유효함, ডাটা_স্থান_সলনি_কৰক)[0] == 1]
    টেক্সট, ডাটা = 적재구획[:2]
    আদেশ_ঠিকনা = struct.unpack_from('<Q', 유효함, টেক্সট + 16)[0]
    ডাটা_ঠিকনা = struct.unpack_from('<Q', 유효함, ডাটা + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', আদেশ_ঠিকনা + 1), ('data-entry', 24, 'Q', ডাটা_ঠিকনা),
               ('outside-file', টেক্সট + 32, 'Q', len(유효함) + 1), ('short-memory', টেক্সট + 40, 'Q', 1),
               ('kernel-address', টেক্সট + 16, 'Q', 0x80000), ('memory-overflow', টেক্সট + 40, 'Q', 2**64 - 1),
               ('writable-code', টেক্সট + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', টেক্সট, 'I', 2),
               ('unaligned-load', টেক্সট + 16, 'Q', আদেশ_ঠিকনা + 8),
               ('overlap', ডাটা + 16, 'Q', আদেশ_ঠিকনা)]
    for নাম, অফছেট_মান, সজ্জা_932e03c8, মান in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + সজ্জা_932e03c8, 바뀐자료, অফছেট_মান, মান)
        시험사례.append((নাম, bytes(바뀐자료)))
    탑재덩이들 = [(নাম.replace('-', '_'), 출력결과 / (নাম + '.elf')) for নাম in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for লুকআপ_ইনডেক্স, (নাম, প্লেল_ড_ডাটা) in enumerate(시험사례):
        পথ = 출력결과 / ('invalid-{}.elf'.format(নাম)); পথ.write_bytes(প্লেল_ড_ডাটা)
        탑재덩이들.append(('invalid_{}'.format(লুকআপ_ইনডেক্স), পথ))
    어셈블리자료, শিৰো_মান = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for নাম, পথ in 탑재덩이들:
        প্ৰতীক_মান = 'user_blob_' + নাম
        크기목록[নাম] = পথ.stat().st_size
        # 생성한 পীয়েৰ_মান 경로만 넣어 프로젝트 경로의 공백/কোট 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + প্ৰতীক_মান, প্ৰতীক_মান + ':', '.incbin "{}"'.format(পথ.relative_to(ৰুট_পথ))]
        শিৰো_মান.append('extern const unsigned char {}[];'.format(প্ৰতীক_মান))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    শিৰো_মান += ['static const এপ্প্ 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    শিৰো_মান += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    শিৰো_মান += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    শিৰো_মান += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], পদ্ধতি_মোড) for পদ্ধতি_মোড in (0, 1)]
    শিৰো_মান += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    শিৰো_মান += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    শিৰো_মান += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    শিৰো_মান += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    শিৰো_মান += ['};', 'static const এপ্প্ 잘못된실행항목들[] = {']
    শিৰো_মান += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(প্লেল_ড_ডাটা)) for 순번, (_, প্লেল_ড_ডাটা) in enumerate(시험사례)]
    শিৰো_মান += ['};']
    (বিল্ড_পথ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (বিল্ড_পথ / 'programs.h').write_text('\n'.join(শিৰো_মান) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(নাম for নাম, _ in 시험사례) + '\n')
    নিষ্পাদন_আদেশ([시언어번역기] + 설정비트 + ['-c', বিল্ড_পথ / 'programs.S', '-o', বিল্ড_পথ / 'programs.o'])
