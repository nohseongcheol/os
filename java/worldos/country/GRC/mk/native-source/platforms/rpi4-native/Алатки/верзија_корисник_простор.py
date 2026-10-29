"""독립된 자체 ABI ELF64와 로더 одбива_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from верзија_PYTHON import Create_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Create_корисник_простор(корен_патека, склад_патека, 시언어번역기, 시플플번역기, 연결편집기, Архива_алатка, конфигурација_Услуга_за_интелигентен_пренос_во_заднина, Изврши_наредба):
    конфигурација_Услуга_за_интелигентен_пренос_во_заднина = [Параметри_VALUE for Параметри_VALUE in конфигурација_Услуга_за_интелигентен_пренос_во_заднина if Параметри_VALUE != '-mgeneral-regs-only']
    верзија_патека = корен_патека / 'build'
    출력결과 = верзија_патека / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = корен_патека / 'корисник'
    포직스경로 = склад_патека / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, ПАТЕКА, Име in [
            (시언어번역기, [], 원본자료 / 'Изврши_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Изврши_наредба.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'корисник_мост.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Уредник.c', 'vi.o')]:
        Изврши_наредба([번역기] + конфигурација_Услуга_за_интелигентен_пренос_во_заднина + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', ПАТЕКА, '-o', 출력결과 / Име])
    Изврши_наредба([Архива_алатка, 'rcs', верзија_патека / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Име in ('demo', 'fault', 'network', 'vi'):
        Изврши_наредба([연결편집기, '-T', 원본자료 / 'Врска_Распоред.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Име + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Име + '.o'), верзија_патека / 'libposix-kor-user.a'])
    자바라이브러리만들기(корен_патека, Изврши_наредба)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(верзија_патека)) as 작업경로:
        класа_патека = Path(작업경로)
        Изврши_наредба(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', класа_патека, '-sourcepath', класа_патека, '-d', класа_патека] +
            [податоци_позиционирање for податоци_позиционирање in sorted((склад_патека / 'os/корисник/자바').glob('*.java')) if податоци_позиционирање.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Изврши_наредба(['sh', склад_патека / 'compiler/미리번역.sh', '--entry', 'алатка_внес.Изврши_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(класа_патека.glob('*.class')))
    압축해제경로 = корен_патека / 'vendor/uzlib'
    for ПАТЕКА, Име in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'пакет.c', 'jar.o')] + [(압축해제경로 / (Име + '.c'), Име + '.o') for Име in ('tinflate', 'crc32', 'adler32')]:
        Изврши_наредба([시언어번역기] + конфигурација_Услуга_за_интелигентен_пренос_во_заднина + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', ПАТЕКА, '-o', 출력결과 / Име])
    Изврши_наредба([연결편집기, '-T', 원본자료 / 'Врска_Распоред.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Име for Име in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Create_PYTHON(корен_патека, 시언어번역기, 연결편집기)
    시언어번역기만들기(корен_патека, склад_патека, 시언어번역기, 연결편집기, конфигурација_Услуга_за_интелигентен_пренос_во_заднина, Изврши_наредба)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    програма_Заглавие_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Заглавие_Список = [програма_Заглавие_OFFSET + ставка_COUNT * 56 for ставка_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [податоци_позиционирање for податоци_позиционирање in Заглавие_Список if struct.unpack_from('<I', 유효함, податоци_позиционирање)[0] == 1]
    Текст, податоци = 적재구획[:2]
    наредба_адреса = struct.unpack_from('<Q', 유효함, Текст + 16)[0]
    податоци_адреса = struct.unpack_from('<Q', 유효함, податоци + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', наредба_адреса + 1), ('data-entry', 24, 'Q', податоци_адреса),
               ('outside-file', Текст + 32, 'Q', len(유효함) + 1), ('short-memory', Текст + 40, 'Q', 1),
               ('kernel-address', Текст + 16, 'Q', 0x80000), ('memory-overflow', Текст + 40, 'Q', 2**64 - 1),
               ('writable-code', Текст + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Текст, 'I', 2),
               ('unaligned-load', Текст + 16, 'Q', наредба_адреса + 8),
               ('overlap', податоци + 16, 'Q', наредба_адреса)]
    for Име, OFFSET_VALUE, формат_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + формат_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Име, bytes(바뀐자료)))
    탑재덩이들 = [(Име.replace('-', '_'), 출력결과 / (Име + '.elf')) for Име in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Име, капацитет_податоци) in enumerate(시험사례):
        ПАТЕКА = 출력결과 / ('invalid-{}.elf'.format(Име)); ПАТЕКА.write_bytes(капацитет_податоци)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), ПАТЕКА))
    어셈블리자료, Заглавие_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Име, ПАТЕКА in 탑재덩이들:
        симбол_VALUE = 'user_blob_' + Име
        크기목록[Име] = ПАТЕКА.stat().st_size
        # 생성한 рамноправен_уред_VALUE 경로만 넣어 프로젝트 경로의 공백/Цитат 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + симбол_VALUE, симбол_VALUE + ':', '.incbin "{}"'.format(ПАТЕКА.relative_to(корен_патека))]
        Заглавие_VALUE.append('extern const unsigned char {}[];'.format(симбол_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Заглавие_VALUE += ['static const програма 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Заглавие_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Заглавие_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Заглавие_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], метод_MODE) for метод_MODE in (0, 1)]
    Заглавие_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Заглавие_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Заглавие_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Заглавие_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Заглавие_VALUE += ['};', 'static const програма 잘못된실행항목들[] = {']
    Заглавие_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(капацитет_податоци)) for 순번, (_, капацитет_податоци) in enumerate(시험사례)]
    Заглавие_VALUE += ['};']
    (верзија_патека / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (верзија_патека / 'programs.h').write_text('\n'.join(Заглавие_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Име for Име, _ in 시험사례) + '\n')
    Изврши_наредба([시언어번역기] + конфигурација_Услуга_за_интелигентен_пренос_во_заднина + ['-c', верзија_патека / 'programs.S', '-o', верзија_патека / 'programs.o'])
