"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from bou_PYTHON import Skep_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Skep_gebruiker_ruimte(wortel_pad, bewaarplek_pad, 시언어번역기, 시플플번역기, 연결편집기, Argief_nutsmiddel, konfigurasie_Agtergrond_intelligente_oordragdiens, uitvoer_bevel):
    konfigurasie_Agtergrond_intelligente_oordragdiens = [Instellings_VALUE for Instellings_VALUE in konfigurasie_Agtergrond_intelligente_oordragdiens if Instellings_VALUE != '-mgeneral-regs-only']
    bou_pad = wortel_pad / 'build'
    출력결과 = bou_pad / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = wortel_pad / 'gebruiker'
    포직스경로 = bewaarplek_pad / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Pad, Naam in [
            (시언어번역기, [], 원본자료 / 'Loop.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'uitvoer_bevel.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'gebruiker_brug.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Redigeerder.c', 'vi.o')]:
        uitvoer_bevel([번역기] + konfigurasie_Agtergrond_intelligente_oordragdiens + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Pad, '-o', 출력결과 / Naam])
    uitvoer_bevel([Argief_nutsmiddel, 'rcs', bou_pad / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Naam in ('demo', 'fault', 'network', 'vi'):
        uitvoer_bevel([연결편집기, '-T', 원본자료 / 'Skakel_Uitleg.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Naam + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Naam + '.o'), bou_pad / 'libposix-kor-user.a'])
    자바라이브러리만들기(wortel_pad, uitvoer_bevel)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(bou_pad)) as 작업경로:
        Klas_pad = Path(작업경로)
        uitvoer_bevel(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Klas_pad, '-sourcepath', Klas_pad, '-d', Klas_pad] +
            [data_plaas for data_plaas in sorted((bewaarplek_pad / 'os/gebruiker/자바').glob('*.java')) if data_plaas.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        uitvoer_bevel(['sh', bewaarplek_pad / 'compiler/미리번역.sh', '--entry', 'nutsmiddel_inskrywing.Loop',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Klas_pad.glob('*.class')))
    압축해제경로 = wortel_pad / 'vendor/uzlib'
    for Pad, Naam in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'bondel.c', 'jar.o')] + [(압축해제경로 / (Naam + '.c'), Naam + '.o') for Naam in ('tinflate', 'crc32', 'adler32')]:
        uitvoer_bevel([시언어번역기] + konfigurasie_Agtergrond_intelligente_oordragdiens + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Pad, '-o', 출력결과 / Naam])
    uitvoer_bevel([연결편집기, '-T', 원본자료 / 'Skakel_Uitleg.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Naam for Naam in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Skep_PYTHON(wortel_pad, 시언어번역기, 연결편집기)
    시언어번역기만들기(wortel_pad, bewaarplek_pad, 시언어번역기, 연결편집기, konfigurasie_Agtergrond_intelligente_oordragdiens, uitvoer_bevel)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    program_Loopkop_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Loopkop_Lys = [program_Loopkop_OFFSET + item_COUNT * 56 for item_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [data_plaas for data_plaas in Loopkop_Lys if struct.unpack_from('<I', 유효함, data_plaas)[0] == 1]
    Teks, data = 적재구획[:2]
    bevel_adres = struct.unpack_from('<Q', 유효함, Teks + 16)[0]
    data_adres = struct.unpack_from('<Q', 유효함, data + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', bevel_adres + 1), ('data-entry', 24, 'Q', data_adres),
               ('outside-file', Teks + 32, 'Q', len(유효함) + 1), ('short-memory', Teks + 40, 'Q', 1),
               ('kernel-address', Teks + 16, 'Q', 0x80000), ('memory-overflow', Teks + 40, 'Q', 2**64 - 1),
               ('writable-code', Teks + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Teks, 'I', 2),
               ('unaligned-load', Teks + 16, 'Q', bevel_adres + 8),
               ('overlap', data + 16, 'Q', bevel_adres)]
    for Naam, OFFSET_VALUE, formaat_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + formaat_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Naam, bytes(바뀐자료)))
    탑재덩이들 = [(Naam.replace('-', '_'), 출력결과 / (Naam + '.elf')) for Naam in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Naam, lading_data) in enumerate(시험사례):
        Pad = 출력결과 / ('invalid-{}.elf'.format(Naam)); Pad.write_bytes(lading_data)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), Pad))
    어셈블리자료, Loopkop_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Naam, Pad in 탑재덩이들:
        simbool_VALUE = 'user_blob_' + Naam
        크기목록[Naam] = Pad.stat().st_size
        # 생성한 portuur_VALUE 경로만 넣어 프로젝트 경로의 공백/Aanhaling 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + simbool_VALUE, simbool_VALUE + ':', '.incbin "{}"'.format(Pad.relative_to(wortel_pad))]
        Loopkop_VALUE.append('extern const unsigned char {}[];'.format(simbool_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Loopkop_VALUE += ['static const program 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Loopkop_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Loopkop_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Loopkop_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metode_MODE) for metode_MODE in (0, 1)]
    Loopkop_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Loopkop_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Loopkop_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Loopkop_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Loopkop_VALUE += ['};', 'static const program 잘못된실행항목들[] = {']
    Loopkop_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(lading_data)) for 순번, (_, lading_data) in enumerate(시험사례)]
    Loopkop_VALUE += ['};']
    (bou_pad / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (bou_pad / 'programs.h').write_text('\n'.join(Loopkop_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Naam for Naam, _ in 시험사례) + '\n')
    uitvoer_bevel([시언어번역기] + konfigurasie_Agtergrond_intelligente_oordragdiens + ['-c', bou_pad / 'programs.S', '-o', bou_pad / 'programs.o'])
