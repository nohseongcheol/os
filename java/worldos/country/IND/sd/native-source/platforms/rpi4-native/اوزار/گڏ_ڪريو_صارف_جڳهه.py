"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def ٺاھيو_صارف_جڳهه(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, محفوظ_ٽول, 설정비트, تعميل_ڪرڻ_حڪم):
    설정비트 = [سيٽنگون_قدر for سيٽنگون_قدر in 설정비트 if سيٽنگون_قدر != '-mgeneral-regs-only']
    گڏ_ڪريو_راههه = 기준경로 / 'build'
    출력결과 = گڏ_ڪريو_راههه / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'صارف'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, راههه, نالو in [
            (시언어번역기, [], 원본자료 / 'هلائڻ.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'تعميل_ڪرڻ_حڪم.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'تدوين_ڪار.c', 'vi.o')]:
        تعميل_ڪرڻ_حڪم([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', راههه, '-o', 출력결과 / نالو])
    تعميل_ڪرڻ_حڪم([محفوظ_ٽول, 'rcs', گڏ_ڪريو_راههه / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for نالو in ('demo', 'fault', 'network', 'vi'):
        تعميل_ڪرڻ_حڪم([연결편집기, '-T', 원본자료 / 'ڪڙي_لي_آئوٽ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (نالو + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (نالو + '.o'), گڏ_ڪريو_راههه / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, تعميل_ڪرڻ_حڪم)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(گڏ_ڪريو_راههه)) as 작업경로:
        درجو_راههه = Path(작업경로)
        تعميل_ڪرڻ_حڪم(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', درجو_راههه, '-sourcepath', درجو_راههه, '-d', درجو_راههه] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/صارف/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        تعميل_ڪرڻ_حڪم(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'ٽول_داخلا.هلائڻ',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(درجو_راههه.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for راههه, نالو in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'بنڊل.c', 'jar.o')] + [(압축해제경로 / (نالو + '.c'), نالو + '.o') for نالو in ('tinflate', 'crc32', 'adler32')]:
        تعميل_ڪرڻ_حڪم([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', راههه, '-o', 출력결과 / نالو])
    تعميل_ڪرڻ_حڪم([연결편집기, '-T', 원본자료 / 'ڪڙي_لي_آئوٽ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / نالو for نالو in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, تعميل_ڪرڻ_حڪم)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    ائپ_هيڊر_آف_سيٽ = struct.unpack_from('<Q', 유효함, 32)[0]
    هيڊر_فهرست = [ائپ_هيڊر_آف_سيٽ + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in هيڊر_فهرست if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    متن, ڪوائف = 적재구획[:2]
    حڪم_پتو = struct.unpack_from('<Q', 유효함, متن + 16)[0]
    ڪوائف_پتو = struct.unpack_from('<Q', 유효함, ڪوائف + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', حڪم_پتو + 1), ('data-entry', 24, 'Q', ڪوائف_پتو),
               ('outside-file', متن + 32, 'Q', len(유효함) + 1), ('short-memory', متن + 40, 'Q', 1),
               ('kernel-address', متن + 16, 'Q', 0x80000), ('memory-overflow', متن + 40, 'Q', 2**64 - 1),
               ('writable-code', متن + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', متن, 'I', 2),
               ('unaligned-load', متن + 16, 'Q', حڪم_پتو + 8),
               ('overlap', ڪوائف + 16, 'Q', حڪم_پتو)]
    for نالو, آف_سيٽ_قدر, وضع_932e03c8, قدر in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + وضع_932e03c8, 바뀐자료, آف_سيٽ_قدر, قدر)
        시험사례.append((نالو, bytes(바뀐자료)))
    탑재덩이들 = [(نالو.replace('-', '_'), 출력결과 / (نالو + '.elf')) for نالو in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (نالو, بنيادي_بار_ڪوائف) in enumerate(시험사례):
        راههه = 출력결과 / ('invalid-{}.elf'.format(نالو)); راههه.write_bytes(بنيادي_بار_ڪوائف)
        탑재덩이들.append(('invalid_{}'.format(색인), راههه))
    어셈블리자료, هيڊر_قدر = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for نالو, راههه in 탑재덩이들:
        نشاني_قدر = 'user_blob_' + نالو
        크기목록[نالو] = راههه.stat().st_size
        # 생성한 همعصر_قدر 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + نشاني_قدر, نشاني_قدر + ':', '.incbin "{}"'.format(راههه.relative_to(기준경로))]
        هيڊر_قدر.append('extern const unsigned char {}[];'.format(نشاني_قدر))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    هيڊر_قدر += ['static const ائپ 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    هيڊر_قدر += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    هيڊر_قدر += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    هيڊر_قدر += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], طريقو_موڊ) for طريقو_موڊ in (0, 1)]
    هيڊر_قدر += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    هيڊر_قدر += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    هيڊر_قدر += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    هيڊر_قدر += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    هيڊر_قدر += ['};', 'static const ائپ 잘못된실행항목들[] = {']
    هيڊر_قدر += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(بنيادي_بار_ڪوائف)) for 순번, (_, بنيادي_بار_ڪوائف) in enumerate(시험사례)]
    هيڊر_قدر += ['};']
    (گڏ_ڪريو_راههه / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (گڏ_ڪريو_راههه / 'programs.h').write_text('\n'.join(هيڊر_قدر) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(نالو for نالو, _ in 시험사례) + '\n')
    تعميل_ڪرڻ_حڪم([시언어번역기] + 설정비트 + ['-c', گڏ_ڪريو_راههه / 'programs.S', '-o', گڏ_ڪريو_راههه / 'programs.o'])
