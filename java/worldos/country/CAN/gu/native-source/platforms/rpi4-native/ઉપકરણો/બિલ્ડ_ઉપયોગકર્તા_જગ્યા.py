"""독립된 자체 ABI ELF64와 로더 નકારો_મૂલ્ય 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def બનાવો_ઉપયોગકર્તા_જગ્યા(રૂટ_પાથ, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, સંગ્રહ_ઉપકરણ, 설정비트, અમલ_કરો_આદેશ):
    설정비트 = [સેટિંગ્સ_મૂલ્ય for સેટિંગ્સ_મૂલ્ય in 설정비트 if સેટિંગ્સ_મૂલ્ય != '-mgeneral-regs-only']
    બિલ્ડ_પાથ = રૂટ_પાથ / 'build'
    출력결과 = બિલ્ડ_પાથ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = રૂટ_પાથ / 'ઉપયોગકર્તા'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, પથ, નામ in [
            (시언어번역기, [], 원본자료 / 'ચલાવો_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'અમલ_કરો_આદેશ.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'ઉપયોગકર્તા_બ્રિજ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'સંપાદક.c', 'vi.o')]:
        અમલ_કરો_આદેશ([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', પથ, '-o', 출력결과 / નામ])
    અમલ_કરો_આદેશ([સંગ્રહ_ઉપકરણ, 'rcs', બિલ્ડ_પાથ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for નામ in ('demo', 'fault', 'network', 'vi'):
        અમલ_કરો_આદેશ([연결편집기, '-T', 원본자료 / 'લિંક_લેઆઉટ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (નામ + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (નામ + '.o'), બિલ્ડ_પાથ / 'libposix-kor-user.a'])
    자바라이브러리만들기(રૂટ_પાથ, અમલ_કરો_આદેશ)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(બિલ્ડ_પાથ)) as 작업경로:
        વર્ગ_પાથ = Path(작업경로)
        અમલ_કરો_આદેશ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', વર્ગ_પાથ, '-sourcepath', વર્ગ_પાથ, '-d', વર્ગ_પાથ] +
            [ડેટા_સ્થિતિ for ડેટા_સ્થિતિ in sorted((저장소경로 / 'os/ઉપયોગકર્તા/자바').glob('*.java')) if ડેટા_સ્થિતિ.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        અમલ_કરો_આદેશ(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'ઉપકરણ_પ્રવેશ.ચલાવો_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(વર્ગ_પાથ.glob('*.class')))
    압축해제경로 = રૂટ_પાથ / 'vendor/uzlib'
    for પથ, નામ in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'બન્ડલ.c', 'jar.o')] + [(압축해제경로 / (નામ + '.c'), નામ + '.o') for નામ in ('tinflate', 'crc32', 'adler32')]:
        અમલ_કરો_આદેશ([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', પથ, '-o', 출력결과 / નામ])
    અમલ_કરો_આદેશ([연결편집기, '-T', 원본자료 / 'લિંક_લેઆઉટ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / નામ for નામ in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(રૂટ_પાથ, 시언어번역기, 연결편집기)
    시언어번역기만들기(રૂટ_પાથ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, અમલ_કરો_આદેશ)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ = struct.unpack_from('<Q', 유효함, 32)[0]
    શીર્ષલેખ_સૂચી = [એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [ડેટા_સ્થિતિ for ડેટા_સ્થિતિ in શીર્ષલેખ_સૂચી if struct.unpack_from('<I', 유효함, ડેટા_સ્થિતિ)[0] == 1]
    લખાણ, ડેટા = 적재구획[:2]
    આદેશ_સરનામું = struct.unpack_from('<Q', 유효함, લખાણ + 16)[0]
    ડેટા_સરનામું = struct.unpack_from('<Q', 유효함, ડેટા + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', આદેશ_સરનામું + 1), ('data-entry', 24, 'Q', ડેટા_સરનામું),
               ('outside-file', લખાણ + 32, 'Q', len(유효함) + 1), ('short-memory', લખાણ + 40, 'Q', 1),
               ('kernel-address', લખાણ + 16, 'Q', 0x80000), ('memory-overflow', લખાણ + 40, 'Q', 2**64 - 1),
               ('writable-code', લખાણ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', લખાણ, 'I', 2),
               ('unaligned-load', લખાણ + 16, 'Q', આદેશ_સરનામું + 8),
               ('overlap', ડેટા + 16, 'Q', આદેશ_સરનામું)]
    for નામ, ઑફસેટ_મૂલ્ય, સ્વરૂપ_932e03c8, મૂલ્ય in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + સ્વરૂપ_932e03c8, 바뀐자료, ઑફસેટ_મૂલ્ય, મૂલ્ય)
        시험사례.append((નામ, bytes(바뀐자료)))
    탑재덩이들 = [(નામ.replace('-', '_'), 출력결과 / (નામ + '.elf')) for નામ in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for લુકઅપ_અનુક્રમણિકા, (નામ, પેલોડ_ડેટા) in enumerate(시험사례):
        પથ = 출력결과 / ('invalid-{}.elf'.format(નામ)); પથ.write_bytes(પેલોડ_ડેટા)
        탑재덩이들.append(('invalid_{}'.format(લુકઅપ_અનુક્રમણિકા), પથ))
    어셈블리자료, શીર્ષલેખ_મૂલ્ય = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for નામ, પથ in 탑재덩이들:
        પ્રતીક_મૂલ્ય = 'user_blob_' + નામ
        크기목록[નામ] = પથ.stat().st_size
        # 생성한 પીઅર_મૂલ્ય 경로만 넣어 프로젝트 경로의 공백/ક્વોટ 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + પ્રતીક_મૂલ્ય, પ્રતીક_મૂલ્ય + ':', '.incbin "{}"'.format(પથ.relative_to(રૂટ_પાથ))]
        શીર્ષલેખ_મૂલ્ય.append('extern const unsigned char {}[];'.format(પ્રતીક_મૂલ્ય))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    શીર્ષલેખ_મૂલ્ય += ['static const એપ્લિકેશન 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    શીર્ષલેખ_મૂલ્ય += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    શીર્ષલેખ_મૂલ્ય += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    શીર્ષલેખ_મૂલ્ય += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], પદ્ધતિ_મોડ) for પદ્ધતિ_મોડ in (0, 1)]
    શીર્ષલેખ_મૂલ્ય += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    શીર્ષલેખ_મૂલ્ય += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    શીર્ષલેખ_મૂલ્ય += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    શીર્ષલેખ_મૂલ્ય += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    શીર્ષલેખ_મૂલ્ય += ['};', 'static const એપ્લિકેશન 잘못된실행항목들[] = {']
    શીર્ષલેખ_મૂલ્ય += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(પેલોડ_ડેટા)) for 순번, (_, પેલોડ_ડેટા) in enumerate(시험사례)]
    શીર્ષલેખ_મૂલ્ય += ['};']
    (બિલ્ડ_પાથ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (બિલ્ડ_પાથ / 'programs.h').write_text('\n'.join(શીર્ષલેખ_મૂલ્ય) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(નામ for નામ, _ in 시험사례) + '\n')
    અમલ_કરો_આદેશ([시언어번역기] + 설정비트 + ['-c', બિલ્ડ_પાથ / 'programs.S', '-o', બિલ્ડ_પાથ / 'programs.o'])
