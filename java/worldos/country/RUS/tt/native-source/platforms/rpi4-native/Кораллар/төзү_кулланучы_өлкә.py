"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from төзү_PYTHON import Төзү_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Төзү_кулланучы_өлкә(тамыр_юл, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Архив_чара, 설정비트, үтәргә_команда):
    설정비트 = [Параметрлар_VALUE for Параметрлар_VALUE in 설정비트 if Параметрлар_VALUE != '-mgeneral-regs-only']
    төзү_юл = тамыр_юл / 'build'
    출력결과 = төзү_юл / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = тамыр_юл / 'кулланучы'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Yul, исем in [
            (시언어번역기, [], 원본자료 / 'эшләтү.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'үтәргә_команда.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'кулланучы_күпер.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Редактор.c', 'vi.o')]:
        үтәргә_команда([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Yul, '-o', 출력결과 / исем])
    үтәргә_команда([Архив_чара, 'rcs', төзү_юл / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for исем in ('demo', 'fault', 'network', 'vi'):
        үтәргә_команда([연결편집기, '-T', 원본자료 / 'бәйләү_план.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (исем + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (исем + '.o'), төзү_юл / 'libposix-kor-user.a'])
    자바라이브러리만들기(тамыр_юл, үтәргә_команда)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(төзү_юл)) as 작업경로:
        класс_юл = Path(작업경로)
        үтәргә_команда(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', класс_юл, '-sourcepath', класс_юл, '-d', класс_юл] +
            [мәгълүмат_урнаштыру for мәгълүмат_урнаштыру in sorted((저장소경로 / 'os/кулланучы/자바').glob('*.java')) if мәгълүмат_урнаштыру.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        үтәргә_команда(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'чара_кертү.эшләтү',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(класс_юл.glob('*.class')))
    압축해제경로 = тамыр_юл / 'vendor/uzlib'
    for Yul, исем in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'пакет.c', 'jar.o')] + [(압축해제경로 / (исем + '.c'), исем + '.o') for исем in ('tinflate', 'crc32', 'adler32')]:
        үтәргә_команда([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Yul, '-o', 출력결과 / исем])
    үтәргә_команда([연결편집기, '-T', 원본자료 / 'бәйләү_план.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / исем for исем in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Төзү_PYTHON(тамыр_юл, 시언어번역기, 연결편집기)
    시언어번역기만들기(тамыр_юл, 저장소경로, 시언어번역기, 연결편집기, 설정비트, үтәргә_команда)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    кушымта_Башлама_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Башлама_Исемлек = [кушымта_Башлама_OFFSET + элемент_COUNT * 56 for элемент_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [мәгълүмат_урнаштыру for мәгълүмат_урнаштыру in Башлама_Исемлек if struct.unpack_from('<I', 유효함, мәгълүмат_урнаштыру)[0] == 1]
    Mäten, мәгълүмат = 적재구획[:2]
    команда_адрес = struct.unpack_from('<Q', 유효함, Mäten + 16)[0]
    мәгълүмат_адрес = struct.unpack_from('<Q', 유효함, мәгълүмат + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', команда_адрес + 1), ('data-entry', 24, 'Q', мәгълүмат_адрес),
               ('outside-file', Mäten + 32, 'Q', len(유효함) + 1), ('short-memory', Mäten + 40, 'Q', 1),
               ('kernel-address', Mäten + 16, 'Q', 0x80000), ('memory-overflow', Mäten + 40, 'Q', 2**64 - 1),
               ('writable-code', Mäten + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Mäten, 'I', 2),
               ('unaligned-load', Mäten + 16, 'Q', команда_адрес + 8),
               ('overlap', мәгълүмат + 16, 'Q', команда_адрес)]
    for исем, OFFSET_VALUE, формат_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + формат_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((исем, bytes(바뀐자료)))
    탑재덩이들 = [(исем.replace('-', '_'), 출력결과 / (исем + '.elf')) for исем in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for Эзләү_INDEX, (исем, төп_өлеш_мәгълүмат) in enumerate(시험사례):
        Yul = 출력결과 / ('invalid-{}.elf'.format(исем)); Yul.write_bytes(төп_өлеш_мәгълүмат)
        탑재덩이들.append(('invalid_{}'.format(Эзләү_INDEX), Yul))
    어셈블리자료, Башлама_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for исем, Yul in 탑재덩이들:
        символ_VALUE = 'user_blob_' + исем
        크기목록[исем] = Yul.stat().st_size
        # 생성한 тиңдәш_VALUE 경로만 넣어 프로젝트 경로의 공백/Куштырнаклар 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + символ_VALUE, символ_VALUE + ':', '.incbin "{}"'.format(Yul.relative_to(тамыр_юл))]
        Башлама_VALUE.append('extern const unsigned char {}[];'.format(символ_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Башлама_VALUE += ['static const кушымта 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Башлама_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Башлама_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Башлама_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], ысул_MODE) for ысул_MODE in (0, 1)]
    Башлама_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Башлама_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Башлама_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Башлама_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Башлама_VALUE += ['};', 'static const кушымта 잘못된실행항목들[] = {']
    Башлама_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(төп_өлеш_мәгълүмат)) for 순번, (_, төп_өлеш_мәгълүмат) in enumerate(시험사례)]
    Башлама_VALUE += ['};']
    (төзү_юл / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (төзү_юл / 'programs.h').write_text('\n'.join(Башлама_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(исем for исем, _ in 시험사례) + '\n')
    үтәргә_команда([시언어번역기] + 설정비트 + ['-c', төзү_юл / 'programs.S', '-o', төзү_юл / 'programs.o'])
