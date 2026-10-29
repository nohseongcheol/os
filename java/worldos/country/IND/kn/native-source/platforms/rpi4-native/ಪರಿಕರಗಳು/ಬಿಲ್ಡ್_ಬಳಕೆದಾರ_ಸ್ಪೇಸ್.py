"""독립된 자체 ABI ELF64와 로더 ನಿರಾಕರಿಸು_ಮೌಲ್ಯ 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def ರಚಿಸು_ಬಳಕೆದಾರ_ಸ್ಪೇಸ್(ಮೂಲ_ಹಾದಿ, ಸಂಗ್ರಹಣೆ_ಹಾದಿ, 시언어번역기, 시플플번역기, 연결편집기, ಅರ್ಖೀವ್_ಪರಿಕರ, ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ, ಪೂರೈಸು_ಆದೇಶ):
    ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ = [ಸೆಟ್ಟಿಂಗ್ಸ್_ಮೌಲ್ಯ for ಸೆಟ್ಟಿಂಗ್ಸ್_ಮೌಲ್ಯ in ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ if ಸೆಟ್ಟಿಂಗ್ಸ್_ಮೌಲ್ಯ != '-mgeneral-regs-only']
    ಬಿಲ್ಡ್_ಹಾದಿ = ಮೂಲ_ಹಾದಿ / 'build'
    출력결과 = ಬಿಲ್ಡ್_ಹಾದಿ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = ಮೂಲ_ಹಾದಿ / 'ಬಳಕೆದಾರ'
    포직스경로 = ಸಂಗ್ರಹಣೆ_ಹಾದಿ / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, ಮಾರ್ಗ, ಹೆಸರು in [
            (시언어번역기, [], 원본자료 / 'ಚಲಾಯಿಸು_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ಪೂರೈಸು_ಆದೇಶ.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'ಬಳಕೆದಾರ_ಸೇತುವೆ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ಸಂಪಾದಕ.c', 'vi.o')]:
        ಪೂರೈಸು_ಆದೇಶ([번역기] + ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', ಮಾರ್ಗ, '-o', 출력결과 / ಹೆಸರು])
    ಪೂರೈಸು_ಆದೇಶ([ಅರ್ಖೀವ್_ಪರಿಕರ, 'rcs', ಬಿಲ್ಡ್_ಹಾದಿ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for ಹೆಸರು in ('demo', 'fault', 'network', 'vi'):
        ಪೂರೈಸು_ಆದೇಶ([연결편집기, '-T', 원본자료 / 'ಜೋಡಣೆ_ಲೇಔಟ್.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (ಹೆಸರು + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (ಹೆಸರು + '.o'), ಬಿಲ್ಡ್_ಹಾದಿ / 'libposix-kor-user.a'])
    자바라이브러리만들기(ಮೂಲ_ಹಾದಿ, ಪೂರೈಸು_ಆದೇಶ)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(ಬಿಲ್ಡ್_ಹಾದಿ)) as 작업경로:
        ವರ್ಗ_ಹಾದಿ = Path(작업경로)
        ಪೂರೈಸು_ಆದೇಶ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', ವರ್ಗ_ಹಾದಿ, '-sourcepath', ವರ್ಗ_ಹಾದಿ, '-d', ವರ್ಗ_ಹಾದಿ] +
            [ಡೇಟಾ_ಹುದ್ದೆ for ಡೇಟಾ_ಹುದ್ದೆ in sorted((ಸಂಗ್ರಹಣೆ_ಹಾದಿ / 'os/ಬಳಕೆದಾರ/자바').glob('*.java')) if ಡೇಟಾ_ಹುದ್ದೆ.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ಪೂರೈಸು_ಆದೇಶ(['sh', ಸಂಗ್ರಹಣೆ_ಹಾದಿ / 'compiler/미리번역.sh', '--entry', 'ಪರಿಕರ_ನಮೂದು.ಚಲಾಯಿಸು_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(ವರ್ಗ_ಹಾದಿ.glob('*.class')))
    압축해제경로 = ಮೂಲ_ಹಾದಿ / 'vendor/uzlib'
    for ಮಾರ್ಗ, ಹೆಸರು in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'ಬಂಡಲ್.c', 'jar.o')] + [(압축해제경로 / (ಹೆಸರು + '.c'), ಹೆಸರು + '.o') for ಹೆಸರು in ('tinflate', 'crc32', 'adler32')]:
        ಪೂರೈಸು_ಆದೇಶ([시언어번역기] + ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', ಮಾರ್ಗ, '-o', 출력결과 / ಹೆಸರು])
    ಪೂರೈಸು_ಆದೇಶ([연결편집기, '-T', 원본자료 / 'ಜೋಡಣೆ_ಲೇಔಟ್.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / ಹೆಸರು for ಹೆಸರು in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(ಮೂಲ_ಹಾದಿ, 시언어번역기, 연결편집기)
    시언어번역기만들기(ಮೂಲ_ಹಾದಿ, ಸಂಗ್ರಹಣೆ_ಹಾದಿ, 시언어번역기, 연결편집기, ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ, ಪೂರೈಸು_ಆದೇಶ)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    ಅಪ್ಲಿ_ಶಿರೋಲೇಖ_ಆಫ್_ಸೆಟ್ = struct.unpack_from('<Q', 유효함, 32)[0]
    ಶಿರೋಲೇಖ_ಪಟ್ಟಿ = [ಅಪ್ಲಿ_ಶಿರೋಲೇಖ_ಆಫ್_ಸೆಟ್ + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [ಡೇಟಾ_ಹುದ್ದೆ for ಡೇಟಾ_ಹುದ್ದೆ in ಶಿರೋಲೇಖ_ಪಟ್ಟಿ if struct.unpack_from('<I', 유효함, ಡೇಟಾ_ಹುದ್ದೆ)[0] == 1]
    ಪಠ್ಯ, ಡೇಟಾ = 적재구획[:2]
    ಆದೇಶ_ಇಮೇಲ್ = struct.unpack_from('<Q', 유효함, ಪಠ್ಯ + 16)[0]
    ಡೇಟಾ_ಇಮೇಲ್ = struct.unpack_from('<Q', 유효함, ಡೇಟಾ + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ಆದೇಶ_ಇಮೇಲ್ + 1), ('data-entry', 24, 'Q', ಡೇಟಾ_ಇಮೇಲ್),
               ('outside-file', ಪಠ್ಯ + 32, 'Q', len(유효함) + 1), ('short-memory', ಪಠ್ಯ + 40, 'Q', 1),
               ('kernel-address', ಪಠ್ಯ + 16, 'Q', 0x80000), ('memory-overflow', ಪಠ್ಯ + 40, 'Q', 2**64 - 1),
               ('writable-code', ಪಠ್ಯ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', ಪಠ್ಯ, 'I', 2),
               ('unaligned-load', ಪಠ್ಯ + 16, 'Q', ಆದೇಶ_ಇಮೇಲ್ + 8),
               ('overlap', ಡೇಟಾ + 16, 'Q', ಆದೇಶ_ಇಮೇಲ್)]
    for ಹೆಸರು, ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ, ಸ್ವರೂಪ_932e03c8, ಮೌಲ್ಯ in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + ಸ್ವರೂಪ_932e03c8, 바뀐자료, ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ, ಮೌಲ್ಯ)
        시험사례.append((ಹೆಸರು, bytes(바뀐자료)))
    탑재덩이들 = [(ಹೆಸರು.replace('-', '_'), 출력결과 / (ಹೆಸರು + '.elf')) for ಹೆಸರು in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for ನೋಡುವ_ಪದಸೂಚಿ, (ಹೆಸರು, ಪೇಲೋಡ್_ಡೇಟಾ) in enumerate(시험사례):
        ಮಾರ್ಗ = 출력결과 / ('invalid-{}.elf'.format(ಹೆಸರು)); ಮಾರ್ಗ.write_bytes(ಪೇಲೋಡ್_ಡೇಟಾ)
        탑재덩이들.append(('invalid_{}'.format(ನೋಡುವ_ಪದಸೂಚಿ), ಮಾರ್ಗ))
    어셈블리자료, ಶಿರೋಲೇಖ_ಮೌಲ್ಯ = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for ಹೆಸರು, ಮಾರ್ಗ in 탑재덩이들:
        ಚಿಹ್ನೆ_ಮೌಲ್ಯ = 'user_blob_' + ಹೆಸರು
        크기목록[ಹೆಸರು] = ಮಾರ್ಗ.stat().st_size
        # 생성한 ಪೀರ್_ಮೌಲ್ಯ 경로만 넣어 프로젝트 경로의 공백/ಕೋಟ್ 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + ಚಿಹ್ನೆ_ಮೌಲ್ಯ, ಚಿಹ್ನೆ_ಮೌಲ್ಯ + ':', '.incbin "{}"'.format(ಮಾರ್ಗ.relative_to(ಮೂಲ_ಹಾದಿ))]
        ಶಿರೋಲೇಖ_ಮೌಲ್ಯ.append('extern const unsigned char {}[];'.format(ಚಿಹ್ನೆ_ಮೌಲ್ಯ))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ += ['static const ಅಪ್ಲಿ 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], ವಿಧಾನ_ಮೋಡ್) for ವಿಧಾನ_ಮೋಡ್ in (0, 1)]
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ += ['};', 'static const ಅಪ್ಲಿ 잘못된실행항목들[] = {']
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ಪೇಲೋಡ್_ಡೇಟಾ)) for 순번, (_, ಪೇಲೋಡ್_ಡೇಟಾ) in enumerate(시험사례)]
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ += ['};']
    (ಬಿಲ್ಡ್_ಹಾದಿ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (ಬಿಲ್ಡ್_ಹಾದಿ / 'programs.h').write_text('\n'.join(ಶಿರೋಲೇಖ_ಮೌಲ್ಯ) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(ಹೆಸರು for ಹೆಸರು, _ in 시험사례) + '\n')
    ಪೂರೈಸು_ಆದೇಶ([시언어번역기] + ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ + ['-c', ಬಿಲ್ಡ್_ಹಾದಿ / 'programs.S', '-o', ಬಿಲ್ಡ್_ಹಾದಿ / 'programs.o'])
