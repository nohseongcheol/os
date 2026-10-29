"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def 사용자영역만들기(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, 묶음도구, 설정비트, 실행):
    설정비트 = [설정값 for 설정값 in 설정비트 if 설정값 != '-mgeneral-regs-only']
    빌드경로 = 기준경로 / 'build'
    출력결과 = 빌드경로 / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / '사용자'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Percurso, Nomine in [
            (시언어번역기, [], 원본자료 / 'Exeque.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '실행.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '편집기.c', 'vi.o')]:
        실행([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Percurso, '-o', 출력결과 / Nomine])
    실행([묶음도구, 'rcs', 빌드경로 / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Nomine in ('demo', 'fault', 'network', 'vi'):
        실행([연결편집기, '-T', 원본자료 / '배치.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Nomine + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Nomine + '.o'), 빌드경로 / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, 실행)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(빌드경로)) as 작업경로:
        클래스경로 = Path(작업경로)
        실행(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', 클래스경로, '-sourcepath', 클래스경로, '-d', 클래스경로] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/사용자/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        실행(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', '도구시작.Exeque',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(클래스경로.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for Percurso, Nomine in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / '꾸러미.c', 'jar.o')] + [(압축해제경로 / (Nomine + '.c'), Nomine + '.o') for Nomine in ('tinflate', 'crc32', 'adler32')]:
        실행([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Percurso, '-o', 출력결과 / Nomine])
    실행([연결편집기, '-T', 원본자료 / '배치.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Nomine for Nomine in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, 실행)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    프로그램머리변위 = struct.unpack_from('<Q', 유효함, 32)[0]
    머리목록 = [프로그램머리변위 + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in 머리목록 if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    texto, 자료 = 적재구획[:2]
    명령주소 = struct.unpack_from('<Q', 유효함, texto + 16)[0]
    자료주소 = struct.unpack_from('<Q', 유효함, 자료 + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', 명령주소 + 1), ('data-entry', 24, 'Q', 자료주소),
               ('outside-file', texto + 32, 'Q', len(유효함) + 1), ('short-memory', texto + 40, 'Q', 1),
               ('kernel-address', texto + 16, 'Q', 0x80000), ('memory-overflow', texto + 40, 'Q', 2**64 - 1),
               ('writable-code', texto + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', texto, 'I', 2),
               ('unaligned-load', texto + 16, 'Q', 명령주소 + 8),
               ('overlap', 자료 + 16, 'Q', 명령주소)]
    for Nomine, 변위, 자료서식, 값 in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + 자료서식, 바뀐자료, 변위, 값)
        시험사례.append((Nomine, bytes(바뀐자료)))
    탑재덩이들 = [(Nomine.replace('-', '_'), 출력결과 / (Nomine + '.elf')) for Nomine in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (Nomine, 내용자료) in enumerate(시험사례):
        Percurso = 출력결과 / ('invalid-{}.elf'.format(Nomine)); Percurso.write_bytes(내용자료)
        탑재덩이들.append(('invalid_{}'.format(색인), Percurso))
    어셈블리자료, 머리부 = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nomine, Percurso in 탑재덩이들:
        심볼 = 'user_blob_' + Nomine
        크기목록[Nomine] = Percurso.stat().st_size
        # 생성한 상대 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + 심볼, 심볼 + ':', '.incbin "{}"'.format(Percurso.relative_to(기준경로))]
        머리부.append('extern const unsigned char {}[];'.format(심볼))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    머리부 += ['static const 실행항목 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    머리부 += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    머리부 += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    머리부 += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], 방식) for 방식 in (0, 1)]
    머리부 += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    머리부 += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    머리부 += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    머리부 += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    머리부 += ['};', 'static const 실행항목 잘못된실행항목들[] = {']
    머리부 += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(내용자료)) for 순번, (_, 내용자료) in enumerate(시험사례)]
    머리부 += ['};']
    (빌드경로 / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (빌드경로 / 'programs.h').write_text('\n'.join(머리부) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Nomine for Nomine, _ in 시험사례) + '\n')
    실행([시언어번역기] + 설정비트 + ['-c', 빌드경로 / 'programs.S', '-o', 빌드경로 / 'programs.o'])
