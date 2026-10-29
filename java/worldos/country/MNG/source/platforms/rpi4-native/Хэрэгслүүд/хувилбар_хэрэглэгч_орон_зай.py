"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def үүсгэх_хэрэглэгч_орон_зай(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Архив_хэрэгсэл, 설정비트, Гүйцэтгэх_команд):
    설정비트 = [Тохиргоо_утга for Тохиргоо_утга in 설정비트 if Тохиргоо_утга != '-mgeneral-regs-only']
    хувилбар_зам = 기준경로 / 'build'
    출력결과 = хувилбар_зам / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'хэрэглэгч'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, ЗАМ, Нэр in [
            (시언어번역기, [], 원본자료 / 'Ажиллуулах.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Гүйцэтгэх_команд.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Засварлагч.c', 'vi.o')]:
        Гүйцэтгэх_команд([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', ЗАМ, '-o', 출력결과 / Нэр])
    Гүйцэтгэх_команд([Архив_хэрэгсэл, 'rcs', хувилбар_зам / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Нэр in ('demo', 'fault', 'network', 'vi'):
        Гүйцэтгэх_команд([연결편집기, '-T', 원본자료 / 'Холбох_Бүдүүвч.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Нэр + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Нэр + '.o'), хувилбар_зам / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, Гүйцэтгэх_команд)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(хувилбар_зам)) as 작업경로:
        класс_зам = Path(작업경로)
        Гүйцэтгэх_команд(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', класс_зам, '-sourcepath', класс_зам, '-d', класс_зам] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/хэрэглэгч/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Гүйцэтгэх_команд(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'хэрэгсэл_оролт.Ажиллуулах',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(класс_зам.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for ЗАМ, Нэр in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'багц.c', 'jar.o')] + [(압축해제경로 / (Нэр + '.c'), Нэр + '.o') for Нэр in ('tinflate', 'crc32', 'adler32')]:
        Гүйцэтгэх_команд([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', ЗАМ, '-o', 출력결과 / Нэр])
    Гүйцэтгэх_команд([연결편집기, '-T', 원본자료 / 'Холбох_Бүдүүвч.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Нэр for Нэр in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, Гүйцэтгэх_команд)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    програм_Толгой_Оффсет = struct.unpack_from('<Q', 유효함, 32)[0]
    Толгой_Жагсаалт = [програм_Толгой_Оффсет + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in Толгой_Жагсаалт if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    Бичвэр, өгөгдөл = 적재구획[:2]
    команд_хаяг = struct.unpack_from('<Q', 유효함, Бичвэр + 16)[0]
    өгөгдөл_хаяг = struct.unpack_from('<Q', 유효함, өгөгдөл + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', команд_хаяг + 1), ('data-entry', 24, 'Q', өгөгдөл_хаяг),
               ('outside-file', Бичвэр + 32, 'Q', len(유효함) + 1), ('short-memory', Бичвэр + 40, 'Q', 1),
               ('kernel-address', Бичвэр + 16, 'Q', 0x80000), ('memory-overflow', Бичвэр + 40, 'Q', 2**64 - 1),
               ('writable-code', Бичвэр + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Бичвэр, 'I', 2),
               ('unaligned-load', Бичвэр + 16, 'Q', команд_хаяг + 8),
               ('overlap', өгөгдөл + 16, 'Q', команд_хаяг)]
    for Нэр, Оффсет_утга, формат_932e03c8, утга in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + формат_932e03c8, 바뀐자료, Оффсет_утга, утга)
        시험사례.append((Нэр, bytes(바뀐자료)))
    탑재덩이들 = [(Нэр.replace('-', '_'), 출력결과 / (Нэр + '.elf')) for Нэр in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (Нэр, ашигтай_ачаалал_өгөгдөл) in enumerate(시험사례):
        ЗАМ = 출력결과 / ('invalid-{}.elf'.format(Нэр)); ЗАМ.write_bytes(ашигтай_ачаалал_өгөгдөл)
        탑재덩이들.append(('invalid_{}'.format(색인), ЗАМ))
    어셈블리자료, Толгой_утга = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Нэр, ЗАМ in 탑재덩이들:
        тэмдэг_утга = 'user_blob_' + Нэр
        크기목록[Нэр] = ЗАМ.stat().st_size
        # 생성한 ижил_түвшин_утга 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + тэмдэг_утга, тэмдэг_утга + ':', '.incbin "{}"'.format(ЗАМ.relative_to(기준경로))]
        Толгой_утга.append('extern const unsigned char {}[];'.format(тэмдэг_утга))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Толгой_утга += ['static const програм 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Толгой_утга += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Толгой_утга += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Толгой_утга += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], арга_горим) for арга_горим in (0, 1)]
    Толгой_утга += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Толгой_утга += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Толгой_утга += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Толгой_утга += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Толгой_утга += ['};', 'static const програм 잘못된실행항목들[] = {']
    Толгой_утга += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ашигтай_ачаалал_өгөгдөл)) for 순번, (_, ашигтай_ачаалал_өгөгдөл) in enumerate(시험사례)]
    Толгой_утга += ['};']
    (хувилбар_зам / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (хувилбар_зам / 'programs.h').write_text('\n'.join(Толгой_утга) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Нэр for Нэр, _ in 시험사례) + '\n')
    Гүйцэтгэх_команд([시언어번역기] + 설정비트 + ['-c', хувилбар_зам / 'programs.S', '-o', хувилбар_зам / 'programs.o'])
