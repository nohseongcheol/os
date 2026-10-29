"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def 사용자영역만들기(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, ƴeewtirde_kuutorgal, 설정비트, 실행):
    설정비트 = [설정값 for 설정값 in 설정비트 if 설정값 != '-mgeneral-regs-only']
    tafde_laawol = 기준경로 / 'build'
    출력결과 = tafde_laawol / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'kuutoro'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, laawol, innde in [
            (시언어번역기, [], 원본자료 / 'huutoraade.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '실행.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'feewnditirde.c', 'vi.o')]:
        실행([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', laawol, '-o', 출력결과 / innde])
    실행([ƴeewtirde_kuutorgal, 'rcs', tafde_laawol / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for innde in ('demo', 'fault', 'network', 'vi'):
        실행([연결편집기, '-T', 원본자료 / 'jokkere_lelngo.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (innde + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (innde + '.o'), tafde_laawol / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, 실행)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(tafde_laawol)) as 작업경로:
        fedde_laawol = Path(작업경로)
        실행(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', fedde_laawol, '-sourcepath', fedde_laawol, '-d', fedde_laawol] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/kuutoro/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        실행(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'kuutorgal_naatnugol.huutoraade',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(fedde_laawol.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for laawol, innde in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / '꾸러미.c', 'jar.o')] + [(압축해제경로 / (innde + '.c'), innde + '.o') for innde in ('tinflate', 'crc32', 'adler32')]:
        실행([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', laawol, '-o', 출력결과 / innde])
    실행([연결편집기, '-T', 원본자료 / 'jokkere_lelngo.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / innde for innde in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, 실행)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    프로그램머리변위 = struct.unpack_from('<Q', 유효함, 32)[0]
    meetalol_hello_Doggol = [프로그램머리변위 + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in meetalol_hello_Doggol if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    binndi, keɓe = 적재구획[:2]
    ginol_ñiiɓirde = struct.unpack_from('<Q', 유효함, binndi + 16)[0]
    keɓe_ñiiɓirde = struct.unpack_from('<Q', 유효함, keɓe + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ginol_ñiiɓirde + 1), ('data-entry', 24, 'Q', keɓe_ñiiɓirde),
               ('outside-file', binndi + 32, 'Q', len(유효함) + 1), ('short-memory', binndi + 40, 'Q', 1),
               ('kernel-address', binndi + 16, 'Q', 0x80000), ('memory-overflow', binndi + 40, 'Q', 2**64 - 1),
               ('writable-code', binndi + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', binndi, 'I', 2),
               ('unaligned-load', binndi + 16, 'Q', ginol_ñiiɓirde + 8),
               ('overlap', keɓe + 16, 'Q', ginol_ñiiɓirde)]
    for innde, 변위, formaa_932e03c8, njaru in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + formaa_932e03c8, 바뀐자료, 변위, njaru)
        시험사례.append((innde, bytes(바뀐자료)))
    탑재덩이들 = [(innde.replace('-', '_'), 출력결과 / (innde + '.elf')) for innde in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (innde, 내용자료) in enumerate(시험사례):
        laawol = 출력결과 / ('invalid-{}.elf'.format(innde)); laawol.write_bytes(내용자료)
        탑재덩이들.append(('invalid_{}'.format(색인), laawol))
    어셈블리자료, meetalol_hello_njaru = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for innde, laawol in 탑재덩이들:
        심볼 = 'user_blob_' + innde
        크기목록[innde] = laawol.stat().st_size
        # 생성한 giƴiraaɗo_njaru 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + 심볼, 심볼 + ':', '.incbin "{}"'.format(laawol.relative_to(기준경로))]
        meetalol_hello_njaru.append('extern const unsigned char {}[];'.format(심볼))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    meetalol_hello_njaru += ['static const tafirde 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    meetalol_hello_njaru += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    meetalol_hello_njaru += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    meetalol_hello_njaru += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], 방식) for 방식 in (0, 1)]
    meetalol_hello_njaru += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    meetalol_hello_njaru += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    meetalol_hello_njaru += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    meetalol_hello_njaru += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    meetalol_hello_njaru += ['};', 'static const tafirde 잘못된실행항목들[] = {']
    meetalol_hello_njaru += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(내용자료)) for 순번, (_, 내용자료) in enumerate(시험사례)]
    meetalol_hello_njaru += ['};']
    (tafde_laawol / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (tafde_laawol / 'programs.h').write_text('\n'.join(meetalol_hello_njaru) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(innde for innde, _ in 시험사례) + '\n')
    실행([시언어번역기] + 설정비트 + ['-c', tafde_laawol / 'programs.S', '-o', tafde_laawol / 'programs.o'])
