"""독립된 свой ABI ELF64와 로더 отклонить_ЗНАЧЕН испытания 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from BLD_PYTHON import Create_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from BLD_C_компилятор import Create_C_компилятор


def Create_пользователь_место(корень_путь, репозиторий_путь, C_компилятор, 시플플번역기, компоновщик_средство, Архив_средство, настройки_BITS, 실행):
    настройки_BITS = [Настройки_ЗНАЧЕН for Настройки_ЗНАЧЕН in настройки_BITS if Настройки_ЗНАЧЕН != '-mgeneral-regs-only']
    BLD_путь = корень_путь / 'build'
    выход = BLD_путь / 'user'
    выход.mkdir(exist_ok=True)
    원본자료 = корень_путь / 'пространство_пользователя'
    포직스경로 = репозиторий_путь / 'posix-kor/arm64-native'
    включать_путь = ['-I', 원본자료, '-I', 포직스경로 / 'объявления', '-I', выход]
    for компилятор_средство, 추가영역, путь, Название in [
            (C_компилятор, [], 원본자료 / 'запустить.S', 'start.o'),
            (C_компилятор, ['-std=c11'], 원본자료 / '실행.c', 'runtime.o'),
            (C_компилятор, ['-std=c11'], 포직스경로 / 'пользователь_мост.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'ПримерФайла.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_компилятор, ['-std=c11'], 원본자료 / 'Защита_тест.c', 'fault.o'),
            (C_компилятор, ['-std=c11'], 원본자료 / 'Редактор.c', 'vi.o')]:
        실행([компилятор_средство] + настройки_BITS + 추가영역 + включать_путь + ['-Wall', '-Wextra', '-Werror', '-c', путь, '-o', выход / Название])
    실행([Архив_средство, 'rcs', BLD_путь / 'libposix-kor-user.a', выход / 'posix.o'])
    for Название in ('demo', 'fault', 'network', 'vi'):
        실행([компоновщик_средство, '-T', 원본자료 / 'схема_компоновки.ld', '-z', 'max-page-size=4096', '-o', выход / (Название + '.elf'),
             выход / 'start.o', выход / 'runtime.o', выход / (Название + '.o'), BLD_путь / 'libposix-kor-user.a'])
    자바라이브러리만들기(корень_путь, 실행)
    # 기존 свой Java компилятор/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(BLD_путь)) as 작업경로:
        Класс_путь = Path(작업경로)
        실행(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Класс_путь, '-sourcepath', Класс_путь, '-d', Класс_путь] +
            [данные_позиция for данные_позиция in sorted((репозиторий_путь / 'os/пространство_пользователя/자바').glob('*.java')) if данные_позиция.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        실행(['sh', репозиторий_путь / 'compiler/미리번역.sh', '--entry', 'средство_ввод.запустить',
             '--profile', 'user', '--heap-words', '1048576', '-o', выход / 'java-tools.c'] + sorted(Класс_путь.glob('*.class')))
    압축해제경로 = корень_путь / 'vendor/uzlib'
    for путь, Название in [(выход / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'пакет.c', 'jar.o')] + [(압축해제경로 / (Название + '.c'), Название + '.o') for Название in ('tinflate', 'crc32', 'adler32')]:
        실행([C_компилятор] + настройки_BITS + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + включать_путь + ['-c', путь, '-o', выход / Название])
    실행([компоновщик_средство, '-T', 원본자료 / 'схема_компоновки.ld', '-z', 'max-page-size=4096', '-o', выход / 'java-tools.elf'] +
        [выход / Название for Название in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Create_PYTHON(корень_путь, C_компилятор, компоновщик_средство)
    Create_C_компилятор(корень_путь, репозиторий_путь, C_компилятор, компоновщик_средство, настройки_BITS, 실행)
    допустимый = (выход / 'demo.elf').read_bytes()
    программа_Заголовок_СМЕЩ = struct.unpack_from('<Q', допустимый, 32)[0]
    Заголовок_Список = [программа_Заголовок_СМЕЩ + товар_СЧЁТ * 56 for товар_СЧЁТ in range(struct.unpack_from('<H', допустимый, 56)[0])]
    적재구획 = [данные_позиция for данные_позиция in Заголовок_Список if struct.unpack_from('<I', допустимый, данные_позиция)[0] == 1]
    текст, данные = 적재구획[:2]
    명령주소 = struct.unpack_from('<Q', допустимый, текст + 16)[0]
    данные_АДРЕС = struct.unpack_from('<Q', допустимый, данные + 16)[0]
    вызов_ABI = допустимый.index(b'JKOROS\0')
    тестовый_случай = [('empty', b''), ('short', допустимый[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', 명령주소 + 1), ('data-entry', 24, 'Q', данные_АДРЕС),
               ('outside-file', текст + 32, 'Q', len(допустимый) + 1), ('short-memory', текст + 40, 'Q', 1),
               ('kernel-address', текст + 16, 'Q', 0x80000), ('memory-overflow', текст + 40, 'Q', 2**64 - 1),
               ('writable-code', текст + 4, 'I', 7), ('missing-abi', вызов_ABI, 'B', ord('X')),
               ('wrong-abi', вызов_ABI + 8, 'I', 2), ('dynamic', текст, 'I', 2),
               ('unaligned-load', текст + 16, 'Q', 명령주소 + 8),
               ('overlap', данные + 16, 'Q', 명령주소)]
    for Название, СМЕЩ_ЗНАЧЕН, формат_932e03c8, ЗНАЧЕН in 수정사항:
        바뀐자료 = bytearray(допустимый); struct.pack_into('<' + формат_932e03c8, 바뀐자료, СМЕЩ_ЗНАЧЕН, ЗНАЧЕН)
        тестовый_случай.append((Название, bytes(바뀐자료)))
    탑재덩이들 = [(Название.replace('-', '_'), выход / (Название + '.elf')) for Название in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for Поиск_ИНДЕКС, (Название, полезные_данные_данные) in enumerate(тестовый_случай):
        путь = выход / ('invalid-{}.elf'.format(Название)); путь.write_bytes(полезные_данные_данные)
        탑재덩이들.append(('invalid_{}'.format(Поиск_ИНДЕКС), путь))
    сборка_ec50080d, Заголовок_ЗНАЧЕН = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Название, путь in 탑재덩이들:
        символ_ЗНАЧЕН = 'user_blob_' + Название
        크기목록[Название] = путь.stat().st_size
        # 생성한 одноранговый_ЗНАЧЕН 경로만 넣어 프로젝트 경로의 공백/Цитата 영향을 피한다.
        сборка_ec50080d += ['.balign 16', '.global ' + символ_ЗНАЧЕН, символ_ЗНАЧЕН + ':', '.incbin "{}"'.format(путь.relative_to(корень_путь))]
        Заголовок_ЗНАЧЕН.append('extern const unsigned char {}[];'.format(символ_ЗНАЧЕН))
    сборка_ec50080d.append('.section .note.GNU-stack,"",%progbits')
    Заголовок_ЗНАЧЕН += ['static const программа 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Заголовок_ЗНАЧЕН += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Заголовок_ЗНАЧЕН += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Заголовок_ЗНАЧЕН += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], метод_МОДА) for метод_МОДА in (0, 1)]
    Заголовок_ЗНАЧЕН += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Заголовок_ЗНАЧЕН += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Заголовок_ЗНАЧЕН += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Заголовок_ЗНАЧЕН += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Заголовок_ЗНАЧЕН += ['};', 'static const программа 잘못된실행항목들[] = {']
    Заголовок_ЗНАЧЕН += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(полезные_данные_данные)) for 순번, (_, полезные_данные_данные) in enumerate(тестовый_случай)]
    Заголовок_ЗНАЧЕН += ['};']
    (BLD_путь / 'programs.S').write_text('\n'.join(сборка_ec50080d) + '\n')
    (BLD_путь / 'programs.h').write_text('\n'.join(Заголовок_ЗНАЧЕН) + '\n')
    (выход / 'invalid-cases.txt').write_text('\n'.join(Название for Название, _ in тестовый_случай) + '\n')
    실행([C_компилятор] + настройки_BITS + ['-c', BLD_путь / 'programs.S', '-o', BLD_путь / 'programs.o'])
