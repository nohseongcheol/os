"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def دروستکردن_بەکارهێنەر_مەودا(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, ئەرشیف_ئامراز, 설정비트, جێبەجێکردن_فەرمان):
    설정비트 = [ڕێكبەندەكان_نرخ for ڕێكبەندەكان_نرخ in 설정비트 if ڕێكبەندەكان_نرخ != '-mgeneral-regs-only']
    دروستکراو_گوزەر = 기준경로 / 'build'
    출력결과 = دروستکراو_گوزەر / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'بەکارهێنەر'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, گوزەر, ناو in [
            (시언어번역기, [], 원본자료 / 'ڕادان.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'جێبەجێکردن_فەرمان.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'بژارکەر.c', 'vi.o')]:
        جێبەجێکردن_فەرمان([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', گوزەر, '-o', 출력결과 / ناو])
    جێبەجێکردن_فەرمان([ئەرشیف_ئامراز, 'rcs', دروستکراو_گوزەر / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for ناو in ('demo', 'fault', 'network', 'vi'):
        جێبەجێکردن_فەرمان([연결편집기, '-T', 원본자료 / 'لینك_ڕیزبەست.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (ناو + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (ناو + '.o'), دروستکراو_گوزەر / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, جێبەجێکردن_فەرمان)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(دروستکراو_گوزەر)) as 작업경로:
        کلاس_گوزەر = Path(작업경로)
        جێبەجێکردن_فەرمان(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', کلاس_گوزەر, '-sourcepath', کلاس_گوزەر, '-d', کلاس_گوزەر] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/بەکارهێنەر/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        جێبەجێکردن_فەرمان(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'ئامراز_تێنووسین.ڕادان',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(کلاس_گوزەر.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for گوزەر, ناو in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'گورزە.c', 'jar.o')] + [(압축해제경로 / (ناو + '.c'), ناو + '.o') for ناو in ('tinflate', 'crc32', 'adler32')]:
        جێبەجێکردن_فەرمان([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', گوزەر, '-o', 출력결과 / ناو])
    جێبەجێکردن_فەرمان([연결편집기, '-T', 원본자료 / 'لینك_ڕیزبەست.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / ناو for ناو in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, جێبەجێکردن_فەرمان)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    بەرنامە_سەرپەڕ_ئۆفسێت = struct.unpack_from('<Q', 유효함, 32)[0]
    سەرپەڕ_لیست = [بەرنامە_سەرپەڕ_ئۆفسێت + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in سەرپەڕ_لیست if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    دەق, دەیتا = 적재구획[:2]
    فەرمان_ناونیشان = struct.unpack_from('<Q', 유효함, دەق + 16)[0]
    دەیتا_ناونیشان = struct.unpack_from('<Q', 유효함, دەیتا + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', فەرمان_ناونیشان + 1), ('data-entry', 24, 'Q', دەیتا_ناونیشان),
               ('outside-file', دەق + 32, 'Q', len(유효함) + 1), ('short-memory', دەق + 40, 'Q', 1),
               ('kernel-address', دەق + 16, 'Q', 0x80000), ('memory-overflow', دەق + 40, 'Q', 2**64 - 1),
               ('writable-code', دەق + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', دەق, 'I', 2),
               ('unaligned-load', دەق + 16, 'Q', فەرمان_ناونیشان + 8),
               ('overlap', دەیتا + 16, 'Q', فەرمان_ناونیشان)]
    for ناو, ئۆفسێت_نرخ, بیچم_932e03c8, نرخ in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + بیچم_932e03c8, 바뀐자료, ئۆفسێت_نرخ, نرخ)
        시험사례.append((ناو, bytes(바뀐자료)))
    탑재덩이들 = [(ناو.replace('-', '_'), 출력결과 / (ناو + '.elf')) for ناو in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (ناو, بارگەى_كرێ_دەیتا) in enumerate(시험사례):
        گوزەر = 출력결과 / ('invalid-{}.elf'.format(ناو)); گوزەر.write_bytes(بارگەى_كرێ_دەیتا)
        탑재덩이들.append(('invalid_{}'.format(색인), گوزەر))
    어셈블리자료, سەرپەڕ_نرخ = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for ناو, گوزەر in 탑재덩이들:
        سیمبۆل_نرخ = 'user_blob_' + ناو
        크기목록[ناو] = گوزەر.stat().st_size
        # 생성한 هاوتا_نرخ 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + سیمبۆل_نرخ, سیمبۆل_نرخ + ':', '.incbin "{}"'.format(گوزەر.relative_to(기준경로))]
        سەرپەڕ_نرخ.append('extern const unsigned char {}[];'.format(سیمبۆل_نرخ))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    سەرپەڕ_نرخ += ['static const بەرنامە 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    سەرپەڕ_نرخ += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    سەرپەڕ_نرخ += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    سەرپەڕ_نرخ += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], ڕێگا_دۆخ) for ڕێگا_دۆخ in (0, 1)]
    سەرپەڕ_نرخ += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    سەرپەڕ_نرخ += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    سەرپەڕ_نرخ += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    سەرپەڕ_نرخ += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    سەرپەڕ_نرخ += ['};', 'static const بەرنامە 잘못된실행항목들[] = {']
    سەرپەڕ_نرخ += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(بارگەى_كرێ_دەیتا)) for 순번, (_, بارگەى_كرێ_دەیتا) in enumerate(시험사례)]
    سەرپەڕ_نرخ += ['};']
    (دروستکراو_گوزەر / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (دروستکراو_گوزەر / 'programs.h').write_text('\n'.join(سەرپەڕ_نرخ) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(ناو for ناو, _ in 시험사례) + '\n')
    جێبەجێکردن_فەرمان([시언어번역기] + 설정비트 + ['-c', دروستکراو_گوزەر / 'programs.S', '-o', دروستکراو_گوزەر / 'programs.o'])
