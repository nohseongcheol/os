"""독립된 propriu ABI ELF64와 로더 respinge_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from generare_PYTHON import crea_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from generare_C_compilator import crea_C_compilator


def crea_utilizator_SPAȚIU(rădăcină_cale, depozit_cale, C_compilator, 시플플번역기, 연결편집기, Arhivă_instrument, configurație_Serviciu_de_transfer_inteligent_în_fundal, executa_comandă):
    configurație_Serviciu_de_transfer_inteligent_în_fundal = [Setări_VALUE for Setări_VALUE in configurație_Serviciu_de_transfer_inteligent_în_fundal if Setări_VALUE != '-mgeneral-regs-only']
    generare_cale = rădăcină_cale / 'build'
    출력결과 = generare_cale / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = rădăcină_cale / 'utilizator'
    포직스경로 = depozit_cale / 'posix-kor/arm64-native'
    include_cale = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for compilator_instrument, 추가영역, Cale, Nume in [
            (C_compilator, [], 원본자료 / 'Pornește.S', 'start.o'),
            (C_compilator, ['-std=c11'], 원본자료 / 'executa_comandă.c', 'runtime.o'),
            (C_compilator, ['-std=c11'], 포직스경로 / 'utilizator_punte.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'ExempluFișier.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_compilator, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (C_compilator, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        executa_comandă([compilator_instrument] + configurație_Serviciu_de_transfer_inteligent_în_fundal + 추가영역 + include_cale + ['-Wall', '-Wextra', '-Werror', '-c', Cale, '-o', 출력결과 / Nume])
    executa_comandă([Arhivă_instrument, 'rcs', generare_cale / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Nume in ('demo', 'fault', 'network', 'vi'):
        executa_comandă([연결편집기, '-T', 원본자료 / 'Link_Aspect.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Nume + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Nume + '.o'), generare_cale / 'libposix-kor-user.a'])
    자바라이브러리만들기(rădăcină_cale, executa_comandă)
    # 기존 propriu Java compilator/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(generare_cale)) as 작업경로:
        Clasă_cale = Path(작업경로)
        executa_comandă(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Clasă_cale, '-sourcepath', Clasă_cale, '-d', Clasă_cale] +
            [date_poziție for date_poziție in sorted((depozit_cale / 'os/utilizator/자바').glob('*.java')) if date_poziție.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        executa_comandă(['sh', depozit_cale / 'compiler/미리번역.sh', '--entry', 'instrument_intrare.Pornește',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Clasă_cale.glob('*.class')))
    압축해제경로 = rădăcină_cale / 'vendor/uzlib'
    for Cale, Nume in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'set.c', 'jar.o')] + [(압축해제경로 / (Nume + '.c'), Nume + '.o') for Nume in ('tinflate', 'crc32', 'adler32')]:
        executa_comandă([C_compilator] + configurație_Serviciu_de_transfer_inteligent_în_fundal + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + include_cale + ['-c', Cale, '-o', 출력결과 / Nume])
    executa_comandă([연결편집기, '-T', 원본자료 / 'Link_Aspect.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Nume for Nume in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    crea_PYTHON(rădăcină_cale, C_compilator, 연결편집기)
    crea_C_compilator(rădăcină_cale, depozit_cale, C_compilator, 연결편집기, configurație_Serviciu_de_transfer_inteligent_în_fundal, executa_comandă)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    program_Antet_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Antet_Listă = [program_Antet_OFFSET + element_COUNT * 56 for element_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [date_poziție for date_poziție in Antet_Listă if struct.unpack_from('<I', 유효함, date_poziție)[0] == 1]
    SMS, date = 적재구획[:2]
    comandă_adresa = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    date_adresa = struct.unpack_from('<Q', 유효함, date + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', comandă_adresa + 1), ('data-entry', 24, 'Q', date_adresa),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', comandă_adresa + 8),
               ('overlap', date + 16, 'Q', comandă_adresa)]
    for Nume, OFFSET_VALUE, format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Nume, bytes(바뀐자료)))
    탑재덩이들 = [(Nume.replace('-', '_'), 출력결과 / (Nume + '.elf')) for Nume in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Nume, sarcină_date) in enumerate(시험사례):
        Cale = 출력결과 / ('invalid-{}.elf'.format(Nume)); Cale.write_bytes(sarcină_date)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), Cale))
    asamblare, Antet_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nume, Cale in 탑재덩이들:
        simbol_VALUE = 'user_blob_' + Nume
        크기목록[Nume] = Cale.stat().st_size
        # 생성한 pereche_VALUE 경로만 넣어 프로젝트 경로의 공백/Citat 영향을 피한다.
        asamblare += ['.balign 16', '.global ' + simbol_VALUE, simbol_VALUE + ':', '.incbin "{}"'.format(Cale.relative_to(rădăcină_cale))]
        Antet_VALUE.append('extern const unsigned char {}[];'.format(simbol_VALUE))
    asamblare.append('.section .note.GNU-stack,"",%progbits')
    Antet_VALUE += ['static const program 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Antet_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Antet_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Antet_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metodă_mod) for metodă_mod in (0, 1)]
    Antet_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Antet_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Antet_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Antet_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Antet_VALUE += ['};', 'static const program 잘못된실행항목들[] = {']
    Antet_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(sarcină_date)) for 순번, (_, sarcină_date) in enumerate(시험사례)]
    Antet_VALUE += ['};']
    (generare_cale / 'programs.S').write_text('\n'.join(asamblare) + '\n')
    (generare_cale / 'programs.h').write_text('\n'.join(Antet_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Nume for Nume, _ in 시험사례) + '\n')
    executa_comandă([C_compilator] + configurație_Serviciu_de_transfer_inteligent_în_fundal + ['-c', generare_cale / 'programs.S', '-o', generare_cale / 'programs.o'])
