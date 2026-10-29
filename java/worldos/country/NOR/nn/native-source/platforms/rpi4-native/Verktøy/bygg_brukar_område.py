"""독립된 자체 ABI ELF64와 로더 avvise_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from bygg_PYTHON import Opprett_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Opprett_brukar_område(rot_bane, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Arkiv_verktøy, 설정비트, Utfør_kommando):
    설정비트 = [Innstillingar_VALUE for Innstillingar_VALUE in 설정비트 if Innstillingar_VALUE != '-mgeneral-regs-only']
    bygg_bane = rot_bane / 'build'
    출력결과 = bygg_bane / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = rot_bane / 'brukar'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, STIGE, Namn in [
            (시언어번역기, [], 원본자료 / 'Køyr_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Utfør_kommando.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'brukar_bru.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Redaktør.c', 'vi.o')]:
        Utfør_kommando([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', STIGE, '-o', 출력결과 / Namn])
    Utfør_kommando([Arkiv_verktøy, 'rcs', bygg_bane / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Namn in ('demo', 'fault', 'network', 'vi'):
        Utfør_kommando([연결편집기, '-T', 원본자료 / 'kople_Oppsett.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Namn + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Namn + '.o'), bygg_bane / 'libposix-kor-user.a'])
    자바라이브러리만들기(rot_bane, Utfør_kommando)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(bygg_bane)) as 작업경로:
        time_bane = Path(작업경로)
        Utfør_kommando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', time_bane, '-sourcepath', time_bane, '-d', time_bane] +
            [data_plassere for data_plassere in sorted((저장소경로 / 'os/brukar/자바').glob('*.java')) if data_plassere.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Utfør_kommando(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'verktøy_oppføring.Køyr_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(time_bane.glob('*.class')))
    압축해제경로 = rot_bane / 'vendor/uzlib'
    for STIGE, Namn in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'bunt.c', 'jar.o')] + [(압축해제경로 / (Namn + '.c'), Namn + '.o') for Namn in ('tinflate', 'crc32', 'adler32')]:
        Utfør_kommando([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', STIGE, '-o', 출력결과 / Namn])
    Utfør_kommando([연결편집기, '-T', 원본자료 / 'kople_Oppsett.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Namn for Namn in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Opprett_PYTHON(rot_bane, 시언어번역기, 연결편집기)
    시언어번역기만들기(rot_bane, 저장소경로, 시언어번역기, 연결편집기, 설정비트, Utfør_kommando)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    app_hode_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    hode_Liste = [app_hode_OFFSET + vare_COUNT * 56 for vare_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [data_plassere for data_plassere in hode_Liste if struct.unpack_from('<I', 유효함, data_plassere)[0] == 1]
    Tekst, data = 적재구획[:2]
    kommando_ADDRESS = struct.unpack_from('<Q', 유효함, Tekst + 16)[0]
    data_ADDRESS = struct.unpack_from('<Q', 유효함, data + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', kommando_ADDRESS + 1), ('data-entry', 24, 'Q', data_ADDRESS),
               ('outside-file', Tekst + 32, 'Q', len(유효함) + 1), ('short-memory', Tekst + 40, 'Q', 1),
               ('kernel-address', Tekst + 16, 'Q', 0x80000), ('memory-overflow', Tekst + 40, 'Q', 2**64 - 1),
               ('writable-code', Tekst + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Tekst, 'I', 2),
               ('unaligned-load', Tekst + 16, 'Q', kommando_ADDRESS + 8),
               ('overlap', data + 16, 'Q', kommando_ADDRESS)]
    for Namn, OFFSET_VALUE, format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Namn, bytes(바뀐자료)))
    탑재덩이들 = [(Namn.replace('-', '_'), 출력결과 / (Namn + '.elf')) for Namn in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Namn, nyttelast_data) in enumerate(시험사례):
        STIGE = 출력결과 / ('invalid-{}.elf'.format(Namn)); STIGE.write_bytes(nyttelast_data)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), STIGE))
    어셈블리자료, hode_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Namn, STIGE in 탑재덩이들:
        symbol_VALUE = 'user_blob_' + Namn
        크기목록[Namn] = STIGE.stat().st_size
        # 생성한 node_VALUE_6a3b6fa7 경로만 넣어 프로젝트 경로의 공백/Sitat 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + symbol_VALUE, symbol_VALUE + ':', '.incbin "{}"'.format(STIGE.relative_to(rot_bane))]
        hode_VALUE.append('extern const unsigned char {}[];'.format(symbol_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    hode_VALUE += ['static const app 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    hode_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    hode_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    hode_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metode_MODE) for metode_MODE in (0, 1)]
    hode_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    hode_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    hode_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    hode_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    hode_VALUE += ['};', 'static const app 잘못된실행항목들[] = {']
    hode_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(nyttelast_data)) for 순번, (_, nyttelast_data) in enumerate(시험사례)]
    hode_VALUE += ['};']
    (bygg_bane / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (bygg_bane / 'programs.h').write_text('\n'.join(hode_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Namn for Namn, _ in 시험사례) + '\n')
    Utfør_kommando([시언어번역기] + 설정비트 + ['-c', bygg_bane / 'programs.S', '-o', bygg_bane / 'programs.o'])
