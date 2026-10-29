"""독립된 اپنا ABI ELF64와 로더 رد_کریں_قدر 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def بنائیں_صارف_اسپیس(روٹ_راہ, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, محفوظ_ٹول, 설정비트, نفاذ_کریں_حکم):
    설정비트 = [سیٹنگز_قدر for سیٹنگز_قدر in 설정비트 if سیٹنگز_قدر != '-mgeneral-regs-only']
    بلڈ_راہ = روٹ_راہ / 'build'
    출력결과 = بلڈ_راہ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = روٹ_راہ / 'صارف'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, راستہ_2, نام in [
            (시언어번역기, [], 원본자료 / 'چلائیں.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'نفاذ_کریں_حکم.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'صارف_برج.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'فائلمثال.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'تدوین_کار.c', 'vi.o')]:
        نفاذ_کریں_حکم([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', راستہ_2, '-o', 출력결과 / نام])
    نفاذ_کریں_حکم([محفوظ_ٹول, 'rcs', بلڈ_راہ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for نام in ('demo', 'fault', 'network', 'vi'):
        نفاذ_کریں_حکم([연결편집기, '-T', 원본자료 / 'ربط_ترتیب.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (نام + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (نام + '.o'), بلڈ_راہ / 'libposix-kor-user.a'])
    자바라이브러리만들기(روٹ_راہ, نفاذ_کریں_حکم)
    # 기존 اپنا Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(بلڈ_راہ)) as 작업경로:
        صنف_راہ = Path(작업경로)
        نفاذ_کریں_حکم(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', صنف_راہ, '-sourcepath', صنف_راہ, '-d', صنف_راہ] +
            [کوائف_پوزیشن_ٹھیک_کریں for کوائف_پوزیشن_ٹھیک_کریں in sorted((저장소경로 / 'os/صارف/자바').glob('*.java')) if کوائف_پوزیشن_ٹھیک_کریں.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        نفاذ_کریں_حکم(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'ٹول_اندراج.چلائیں',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(صنف_راہ.glob('*.class')))
    압축해제경로 = روٹ_راہ / 'vendor/uzlib'
    for راستہ_2, نام in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'بنڈل.c', 'jar.o')] + [(압축해제경로 / (نام + '.c'), نام + '.o') for نام in ('tinflate', 'crc32', 'adler32')]:
        نفاذ_کریں_حکم([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', راستہ_2, '-o', 출력결과 / نام])
    نفاذ_کریں_حکم([연결편집기, '-T', 원본자료 / 'ربط_ترتیب.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / نام for نام in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(روٹ_راہ, 시언어번역기, 연결편집기)
    시언어번역기만들기(روٹ_راہ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, نفاذ_کریں_حکم)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    ایپ_سرصفحہ_آفسٹ = struct.unpack_from('<Q', 유효함, 32)[0]
    سرصفحہ_فہرست = [ایپ_سرصفحہ_آفسٹ + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [کوائف_پوزیشن_ٹھیک_کریں for کوائف_پوزیشن_ٹھیک_کریں in سرصفحہ_فہرست if struct.unpack_from('<I', 유효함, کوائف_پوزیشن_ٹھیک_کریں)[0] == 1]
    متن, کوائف = 적재구획[:2]
    حکم_پتہ = struct.unpack_from('<Q', 유효함, متن + 16)[0]
    کوائف_پتہ = struct.unpack_from('<Q', 유효함, کوائف + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', حکم_پتہ + 1), ('data-entry', 24, 'Q', کوائف_پتہ),
               ('outside-file', متن + 32, 'Q', len(유효함) + 1), ('short-memory', متن + 40, 'Q', 1),
               ('kernel-address', متن + 16, 'Q', 0x80000), ('memory-overflow', متن + 40, 'Q', 2**64 - 1),
               ('writable-code', متن + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', متن, 'I', 2),
               ('unaligned-load', متن + 16, 'Q', حکم_پتہ + 8),
               ('overlap', کوائف + 16, 'Q', حکم_پتہ)]
    for نام, آفسٹ_قدر, وضع_932e03c8, قدر in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + وضع_932e03c8, 바뀐자료, آفسٹ_قدر, قدر)
        시험사례.append((نام, bytes(바뀐자료)))
    탑재덩이들 = [(نام.replace('-', '_'), 출력결과 / (نام + '.elf')) for نام in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for لُک_اپ_اشاریہ, (نام, پے_لوڈ_کوائف) in enumerate(시험사례):
        راستہ_2 = 출력결과 / ('invalid-{}.elf'.format(نام)); راستہ_2.write_bytes(پے_لوڈ_کوائف)
        탑재덩이들.append(('invalid_{}'.format(لُک_اپ_اشاریہ), راستہ_2))
    어셈블리자료, سرصفحہ_قدر = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for نام, راستہ_2 in 탑재덩이들:
        علامت_قدر = 'user_blob_' + نام
        크기목록[نام] = راستہ_2.stat().st_size
        # 생성한 ساتھی_قدر 경로만 넣어 프로젝트 경로의 공백/اقتباس 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + علامت_قدر, علامت_قدر + ':', '.incbin "{}"'.format(راستہ_2.relative_to(روٹ_راہ))]
        سرصفحہ_قدر.append('extern const unsigned char {}[];'.format(علامت_قدر))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    سرصفحہ_قدر += ['static const ایپ 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    سرصفحہ_قدر += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    سرصفحہ_قدر += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    سرصفحہ_قدر += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], طریقہ_موڈ) for طریقہ_موڈ in (0, 1)]
    سرصفحہ_قدر += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    سرصفحہ_قدر += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    سرصفحہ_قدر += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    سرصفحہ_قدر += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    سرصفحہ_قدر += ['};', 'static const ایپ 잘못된실행항목들[] = {']
    سرصفحہ_قدر += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(پے_لوڈ_کوائف)) for 순번, (_, پے_لوڈ_کوائف) in enumerate(시험사례)]
    سرصفحہ_قدر += ['};']
    (بلڈ_راہ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (بلڈ_راہ / 'programs.h').write_text('\n'.join(سرصفحہ_قدر) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(نام for نام, _ in 시험사례) + '\n')
    نفاذ_کریں_حکم([시언어번역기] + 설정비트 + ['-c', بلڈ_راہ / 'programs.S', '-o', بلڈ_راہ / 'programs.o'])
