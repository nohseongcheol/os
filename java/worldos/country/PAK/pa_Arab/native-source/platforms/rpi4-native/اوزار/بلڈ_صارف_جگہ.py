"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def بنڑاؤ_صارف_جگہ(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, محفوظہ_ٹول, 설정비트, نفاذ_کرو_حکم):
    설정비트 = [سیٹنگاں_قدر for سیٹنگاں_قدر in 설정비트 if سیٹنگاں_قدر != '-mgeneral-regs-only']
    بلڈ_راہ = 기준경로 / 'build'
    출력결과 = بلڈ_راہ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'صارف'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, راہ, ناں in [
            (시언어번역기, [], 원본자료 / 'چلاؤ.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'نفاذ_کرو_حکم.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'صارف_برج.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'تدوین_کار.c', 'vi.o')]:
        نفاذ_کرو_حکم([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', راہ, '-o', 출력결과 / ناں])
    نفاذ_کرو_حکم([محفوظہ_ٹول, 'rcs', بلڈ_راہ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for ناں in ('demo', 'fault', 'network', 'vi'):
        نفاذ_کرو_حکم([연결편집기, '-T', 원본자료 / 'ربط_لے_آؤٹ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (ناں + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (ناں + '.o'), بلڈ_راہ / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, نفاذ_کرو_حکم)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(بلڈ_راہ)) as 작업경로:
        درجہ_راہ = Path(작업경로)
        نفاذ_کرو_حکم(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', درجہ_راہ, '-sourcepath', درجہ_راہ, '-d', درجہ_راہ] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/صارف/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        نفاذ_کرو_حکم(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'ٹول_داخلہ.چلاؤ',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(درجہ_راہ.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for راہ, ناں in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'گٹھ.c', 'jar.o')] + [(압축해제경로 / (ناں + '.c'), ناں + '.o') for ناں in ('tinflate', 'crc32', 'adler32')]:
        نفاذ_کرو_حکم([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', راہ, '-o', 출력결과 / ناں])
    نفاذ_کرو_حکم([연결편집기, '-T', 원본자료 / 'ربط_لے_آؤٹ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / ناں for ناں in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, نفاذ_کرو_حکم)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    ایپ_سرتحریر_آف_سیٹ = struct.unpack_from('<Q', 유효함, 32)[0]
    سرتحریر_فرست = [ایپ_سرتحریر_آف_سیٹ + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in سرتحریر_فرست if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    متن, کوائف = 적재구획[:2]
    حکم_پتا = struct.unpack_from('<Q', 유효함, متن + 16)[0]
    کوائف_پتا = struct.unpack_from('<Q', 유효함, کوائف + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', حکم_پتا + 1), ('data-entry', 24, 'Q', کوائف_پتا),
               ('outside-file', متن + 32, 'Q', len(유효함) + 1), ('short-memory', متن + 40, 'Q', 1),
               ('kernel-address', متن + 16, 'Q', 0x80000), ('memory-overflow', متن + 40, 'Q', 2**64 - 1),
               ('writable-code', متن + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', متن, 'I', 2),
               ('unaligned-load', متن + 16, 'Q', حکم_پتا + 8),
               ('overlap', کوائف + 16, 'Q', حکم_پتا)]
    for ناں, آف_سیٹ_قدر, وضع_932e03c8, قدر in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + وضع_932e03c8, 바뀐자료, آف_سیٹ_قدر, قدر)
        시험사례.append((ناں, bytes(바뀐자료)))
    탑재덩이들 = [(ناں.replace('-', '_'), 출력결과 / (ناں + '.elf')) for ناں in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (ناں, پے_لوڈ_کوائف) in enumerate(시험사례):
        راہ = 출력결과 / ('invalid-{}.elf'.format(ناں)); راہ.write_bytes(پے_لوڈ_کوائف)
        탑재덩이들.append(('invalid_{}'.format(색인), راہ))
    어셈블리자료, سرتحریر_قدر = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for ناں, راہ in 탑재덩이들:
        علامت_قدر = 'user_blob_' + ناں
        크기목록[ناں] = راہ.stat().st_size
        # 생성한 ہم_سر_قدر 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + علامت_قدر, علامت_قدر + ':', '.incbin "{}"'.format(راہ.relative_to(기준경로))]
        سرتحریر_قدر.append('extern const unsigned char {}[];'.format(علامت_قدر))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    سرتحریر_قدر += ['static const ایپ 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    سرتحریر_قدر += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    سرتحریر_قدر += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    سرتحریر_قدر += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], طریقہ_موڈ) for طریقہ_موڈ in (0, 1)]
    سرتحریر_قدر += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    سرتحریر_قدر += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    سرتحریر_قدر += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    سرتحریر_قدر += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    سرتحریر_قدر += ['};', 'static const ایپ 잘못된실행항목들[] = {']
    سرتحریر_قدر += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(پے_لوڈ_کوائف)) for 순번, (_, پے_لوڈ_کوائف) in enumerate(시험사례)]
    سرتحریر_قدر += ['};']
    (بلڈ_راہ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (بلڈ_راہ / 'programs.h').write_text('\n'.join(سرتحریر_قدر) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(ناں for ناں, _ in 시험사례) + '\n')
    نفاذ_کرو_حکم([시언어번역기] + 설정비트 + ['-c', بلڈ_راہ / 'programs.S', '-o', بلڈ_راہ / 'programs.o'])
