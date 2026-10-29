"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def түзүү_колдонуучу_АРАЛЫК(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Архив_курал, 설정비트, аткаруу_буйрук):
    설정비트 = [Орнотуулар_маани for Орнотуулар_маани in 설정비트 if Орнотуулар_маани != '-mgeneral-regs-only']
    курам_жол = 기준경로 / 'build'
    출력결과 = курам_жол / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'колдонуучу'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, ЖОЛ, Аты in [
            (시언어번역기, [], 원본자료 / 'Жүргүзүү.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'аткаруу_буйрук.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Редактор.c', 'vi.o')]:
        аткаруу_буйрук([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', ЖОЛ, '-o', 출력결과 / Аты])
    аткаруу_буйрук([Архив_курал, 'rcs', курам_жол / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Аты in ('demo', 'fault', 'network', 'vi'):
        аткаруу_буйрук([연결편집기, '-T', 원본자료 / 'Шилтеме_түзүлүш.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Аты + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Аты + '.o'), курам_жол / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, аткаруу_буйрук)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(курам_жол)) as 작업경로:
        класс_жол = Path(작업경로)
        аткаруу_буйрук(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', класс_жол, '-sourcepath', класс_жол, '-d', класс_жол] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/колдонуучу/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        аткаруу_буйрук(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'курал_киргизме_жазуу.Жүргүзүү',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(класс_жол.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for ЖОЛ, Аты in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'пакет.c', 'jar.o')] + [(압축해제경로 / (Аты + '.c'), Аты + '.o') for Аты in ('tinflate', 'crc32', 'adler32')]:
        аткаруу_буйрук([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', ЖОЛ, '-o', 출력결과 / Аты])
    аткаруу_буйрук([연결편집기, '-T', 원본자료 / 'Шилтеме_түзүлүш.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Аты for Аты in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, аткаруу_буйрук)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    програм_баш_аты_Жылбышуу = struct.unpack_from('<Q', 유효함, 32)[0]
    баш_аты_Тизме = [програм_баш_аты_Жылбышуу + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in баш_аты_Тизме if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    Текст, берилмелер = 적재구획[:2]
    буйрук_дарек = struct.unpack_from('<Q', 유효함, Текст + 16)[0]
    берилмелер_дарек = struct.unpack_from('<Q', 유효함, берилмелер + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', буйрук_дарек + 1), ('data-entry', 24, 'Q', берилмелер_дарек),
               ('outside-file', Текст + 32, 'Q', len(유효함) + 1), ('short-memory', Текст + 40, 'Q', 1),
               ('kernel-address', Текст + 16, 'Q', 0x80000), ('memory-overflow', Текст + 40, 'Q', 2**64 - 1),
               ('writable-code', Текст + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Текст, 'I', 2),
               ('unaligned-load', Текст + 16, 'Q', буйрук_дарек + 8),
               ('overlap', берилмелер + 16, 'Q', буйрук_дарек)]
    for Аты, Жылбышуу_маани, формат_932e03c8, маани in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + формат_932e03c8, 바뀐자료, Жылбышуу_маани, маани)
        시험사례.append((Аты, bytes(바뀐자료)))
    탑재덩이들 = [(Аты.replace('-', '_'), 출력결과 / (Аты + '.elf')) for Аты in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (Аты, керектүү_жүктөө_ченеми_берилмелер) in enumerate(시험사례):
        ЖОЛ = 출력결과 / ('invalid-{}.elf'.format(Аты)); ЖОЛ.write_bytes(керектүү_жүктөө_ченеми_берилмелер)
        탑재덩이들.append(('invalid_{}'.format(색인), ЖОЛ))
    어셈블리자료, баш_аты_маани = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Аты, ЖОЛ in 탑재덩이들:
        символ_маани = 'user_blob_' + Аты
        크기목록[Аты] = ЖОЛ.stat().st_size
        # 생성한 бирдей_маани 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + символ_маани, символ_маани + ':', '.incbin "{}"'.format(ЖОЛ.relative_to(기준경로))]
        баш_аты_маани.append('extern const unsigned char {}[];'.format(символ_маани))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    баш_аты_маани += ['static const програм 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    баш_аты_маани += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    баш_аты_маани += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    баш_аты_маани += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], ыкма_режим) for ыкма_режим in (0, 1)]
    баш_аты_маани += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    баш_аты_маани += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    баш_аты_маани += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    баш_аты_маани += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    баш_аты_маани += ['};', 'static const програм 잘못된실행항목들[] = {']
    баш_аты_маани += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(керектүү_жүктөө_ченеми_берилмелер)) for 순번, (_, керектүү_жүктөө_ченеми_берилмелер) in enumerate(시험사례)]
    баш_аты_маани += ['};']
    (курам_жол / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (курам_жол / 'programs.h').write_text('\n'.join(баш_аты_маани) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Аты for Аты, _ in 시험사례) + '\n')
    аткаруу_буйрук([시언어번역기] + 설정비트 + ['-c', курам_жол / 'programs.S', '-o', курам_жол / 'programs.o'])
