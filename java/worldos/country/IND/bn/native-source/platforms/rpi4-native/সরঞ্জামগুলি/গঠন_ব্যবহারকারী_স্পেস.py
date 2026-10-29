"""독립된 নিজ ABI ELF64와 로더 প্রত্যাখ্যান_মান 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def ক্রিয়েট_ব্যবহারকারী_স্পেস(মূল_পথ, সংগ্রহস্থলের_পথ, 시언어번역기, 시플플번역기, 연결편집기, সংগ্রহ_করা_টুল, বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস, কার্যকর_করুন_আদেশ):
    বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস = [সেটিংস_মান for সেটিংস_মান in বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস if সেটিংস_মান != '-mgeneral-regs-only']
    গঠন_পথ = মূল_পথ / 'build'
    출력결과 = গঠন_পথ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = মূল_পথ / 'ব্যবহারকারী'
    포직스경로 = সংগ্রহস্থলের_পথ / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, পথ_2, নাম in [
            (시언어번역기, [], 원본자료 / 'চালনা.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'কার্যকর_করুন_আদেশ.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'ব্যবহারকারী_ব্রিজ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'ফাইলনমুনা.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'সম্পাদক.c', 'vi.o')]:
        কার্যকর_করুন_আদেশ([번역기] + বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', পথ_2, '-o', 출력결과 / নাম])
    কার্যকর_করুন_আদেশ([সংগ্রহ_করা_টুল, 'rcs', গঠন_পথ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for নাম in ('demo', 'fault', 'network', 'vi'):
        কার্যকর_করুন_আদেশ([연결편집기, '-T', 원본자료 / 'লিংক_লেআউট.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (নাম + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (নাম + '.o'), গঠন_পথ / 'libposix-kor-user.a'])
    자바라이브러리만들기(মূল_পথ, কার্যকর_করুন_আদেশ)
    # 기존 নিজ Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(গঠন_পথ)) as 작업경로:
        শ্রেণী_পথ = Path(작업경로)
        কার্যকর_করুন_আদেশ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', শ্রেণী_পথ, '-sourcepath', শ্রেণী_পথ, '-d', শ্রেণী_পথ] +
            [ডাটা_পদ for ডাটা_পদ in sorted((সংগ্রহস্থলের_পথ / 'os/ব্যবহারকারী/자바').glob('*.java')) if ডাটা_পদ.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        কার্যকর_করুন_আদেশ(['sh', সংগ্রহস্থলের_পথ / 'compiler/미리번역.sh', '--entry', 'টুল_ভুক্তি.চালনা',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(শ্রেণী_পথ.glob('*.class')))
    압축해제경로 = মূল_পথ / 'vendor/uzlib'
    for পথ_2, নাম in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'পাঁজা.c', 'jar.o')] + [(압축해제경로 / (নাম + '.c'), নাম + '.o') for নাম in ('tinflate', 'crc32', 'adler32')]:
        কার্যকর_করুন_আদেশ([시언어번역기] + বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', পথ_2, '-o', 출력결과 / নাম])
    কার্যকর_করুন_আদেশ([연결편집기, '-T', 원본자료 / 'লিংক_লেআউট.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / নাম for নাম in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(মূল_পথ, 시언어번역기, 연결편집기)
    시언어번역기만들기(মূল_পথ, সংগ্রহস্থলের_পথ, 시언어번역기, 연결편집기, বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস, কার্যকর_করুন_আদেশ)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    অ্যাপ_হেডার_অফসেট = struct.unpack_from('<Q', 유효함, 32)[0]
    হেডার_তালিকা = [অ্যাপ_হেডার_অফসেট + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [ডাটা_পদ for ডাটা_পদ in হেডার_তালিকা if struct.unpack_from('<I', 유효함, ডাটা_পদ)[0] == 1]
    পাঠ, ডাটা = 적재구획[:2]
    আদেশ_ইমেইল = struct.unpack_from('<Q', 유효함, পাঠ + 16)[0]
    ডাটা_ইমেইল = struct.unpack_from('<Q', 유효함, ডাটা + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', আদেশ_ইমেইল + 1), ('data-entry', 24, 'Q', ডাটা_ইমেইল),
               ('outside-file', পাঠ + 32, 'Q', len(유효함) + 1), ('short-memory', পাঠ + 40, 'Q', 1),
               ('kernel-address', পাঠ + 16, 'Q', 0x80000), ('memory-overflow', পাঠ + 40, 'Q', 2**64 - 1),
               ('writable-code', পাঠ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', পাঠ, 'I', 2),
               ('unaligned-load', পাঠ + 16, 'Q', আদেশ_ইমেইল + 8),
               ('overlap', ডাটা + 16, 'Q', আদেশ_ইমেইল)]
    for নাম, অফসেট_মান, বিন্যাস_932e03c8, মান in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + বিন্যাস_932e03c8, 바뀐자료, অফসেট_মান, মান)
        시험사례.append((নাম, bytes(바뀐자료)))
    탑재덩이들 = [(নাম.replace('-', '_'), 출력결과 / (নাম + '.elf')) for নাম in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for লুকআপ_সূচি, (নাম, পেলোড_ডাটা) in enumerate(시험사례):
        পথ_2 = 출력결과 / ('invalid-{}.elf'.format(নাম)); পথ_2.write_bytes(পেলোড_ডাটা)
        탑재덩이들.append(('invalid_{}'.format(লুকআপ_সূচি), পথ_2))
    어셈블리자료, হেডার_মান = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for নাম, পথ_2 in 탑재덩이들:
        প্রতীক_মান = 'user_blob_' + নাম
        크기목록[নাম] = পথ_2.stat().st_size
        # 생성한 পিয়ার_মান 경로만 넣어 프로젝트 경로의 공백/কোট 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + প্রতীক_মান, প্রতীক_মান + ':', '.incbin "{}"'.format(পথ_2.relative_to(মূল_পথ))]
        হেডার_মান.append('extern const unsigned char {}[];'.format(প্রতীক_মান))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    হেডার_মান += ['static const অ্যাপ 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    হেডার_মান += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    হেডার_মান += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    হেডার_মান += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], পদ্ধতি_মোড) for পদ্ধতি_মোড in (0, 1)]
    হেডার_মান += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    হেডার_মান += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    হেডার_মান += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    হেডার_মান += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    হেডার_মান += ['};', 'static const অ্যাপ 잘못된실행항목들[] = {']
    হেডার_মান += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(পেলোড_ডাটা)) for 순번, (_, পেলোড_ডাটা) in enumerate(시험사례)]
    হেডার_মান += ['};']
    (গঠন_পথ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (গঠন_পথ / 'programs.h').write_text('\n'.join(হেডার_মান) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(নাম for নাম, _ in 시험사례) + '\n')
    কার্যকর_করুন_আদেশ([시언어번역기] + বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস + ['-c', গঠন_পথ / 'programs.S', '-o', গঠন_পথ / 'programs.o'])
