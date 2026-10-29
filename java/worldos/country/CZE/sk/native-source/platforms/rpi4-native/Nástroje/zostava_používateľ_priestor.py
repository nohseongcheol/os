"""독립된 vlastné ABI ELF64와 로더 odmietnuť_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from zostava_PYTHON import Create_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from zostava_C_kompilátor import Create_C_kompilátor


def Create_používateľ_priestor(koreň_cesta, odkladací_priestor_cesta, C_kompilátor, 시플플번역기, 연결편집기, Archív_nástroj, konfigurácia_Background_Intelligent_Transfer_Service, Vykonať_príkaz):
    konfigurácia_Background_Intelligent_Transfer_Service = [Nastavenia_VALUE for Nastavenia_VALUE in konfigurácia_Background_Intelligent_Transfer_Service if Nastavenia_VALUE != '-mgeneral-regs-only']
    zostava_cesta = koreň_cesta / 'build'
    출력결과 = zostava_cesta / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = koreň_cesta / 'používateľ'
    포직스경로 = odkladací_priestor_cesta / 'posix-kor/arm64-native'
    zahrnúť_cesta = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for kompilátor_nástroj, 추가영역, Cesta, Názov in [
            (C_kompilátor, [], 원본자료 / 'Spustiť_2.S', 'start.o'),
            (C_kompilátor, ['-std=c11'], 원본자료 / 'Vykonať_príkaz.c', 'runtime.o'),
            (C_kompilátor, ['-std=c11'], 포직스경로 / 'používateľ_most.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'UkážkaSúboru.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_kompilátor, ['-std=c11'], 원본자료 / 'Ochrana_test.c', 'fault.o'),
            (C_kompilátor, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        Vykonať_príkaz([kompilátor_nástroj] + konfigurácia_Background_Intelligent_Transfer_Service + 추가영역 + zahrnúť_cesta + ['-Wall', '-Wextra', '-Werror', '-c', Cesta, '-o', 출력결과 / Názov])
    Vykonať_príkaz([Archív_nástroj, 'rcs', zostava_cesta / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Názov in ('demo', 'fault', 'network', 'vi'):
        Vykonať_príkaz([연결편집기, '-T', 원본자료 / 'odkaz_Navigácia.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Názov + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Názov + '.o'), zostava_cesta / 'libposix-kor-user.a'])
    자바라이브러리만들기(koreň_cesta, Vykonať_príkaz)
    # 기존 vlastné Java kompilátor/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(zostava_cesta)) as 작업경로:
        lekcia_cesta = Path(작업경로)
        Vykonať_príkaz(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', lekcia_cesta, '-sourcepath', lekcia_cesta, '-d', lekcia_cesta] +
            [údaje_pozícia for údaje_pozícia in sorted((odkladací_priestor_cesta / 'os/používateľ/자바').glob('*.java')) if údaje_pozícia.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Vykonať_príkaz(['sh', odkladací_priestor_cesta / 'compiler/미리번역.sh', '--entry', 'nástroj_položka.Spustiť_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(lekcia_cesta.glob('*.class')))
    압축해제경로 = koreň_cesta / 'vendor/uzlib'
    for Cesta, Názov in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'zväzok.c', 'jar.o')] + [(압축해제경로 / (Názov + '.c'), Názov + '.o') for Názov in ('tinflate', 'crc32', 'adler32')]:
        Vykonať_príkaz([C_kompilátor] + konfigurácia_Background_Intelligent_Transfer_Service + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + zahrnúť_cesta + ['-c', Cesta, '-o', 출력결과 / Názov])
    Vykonať_príkaz([연결편집기, '-T', 원본자료 / 'odkaz_Navigácia.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Názov for Názov in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Create_PYTHON(koreň_cesta, C_kompilátor, 연결편집기)
    Create_C_kompilátor(koreň_cesta, odkladací_priestor_cesta, C_kompilátor, 연결편집기, konfigurácia_Background_Intelligent_Transfer_Service, Vykonať_príkaz)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    program_Nadpis_Posun = struct.unpack_from('<Q', 유효함, 32)[0]
    Nadpis_Zoznam = [program_Nadpis_Posun + položka_COUNT * 56 for položka_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [údaje_pozícia for údaje_pozícia in Nadpis_Zoznam if struct.unpack_from('<I', 유효함, údaje_pozícia)[0] == 1]
    Spracovanie_textu, údaje = 적재구획[:2]
    príkaz_adresa = struct.unpack_from('<Q', 유효함, Spracovanie_textu + 16)[0]
    údaje_adresa = struct.unpack_from('<Q', 유효함, údaje + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    test_prípad = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', príkaz_adresa + 1), ('data-entry', 24, 'Q', údaje_adresa),
               ('outside-file', Spracovanie_textu + 32, 'Q', len(유효함) + 1), ('short-memory', Spracovanie_textu + 40, 'Q', 1),
               ('kernel-address', Spracovanie_textu + 16, 'Q', 0x80000), ('memory-overflow', Spracovanie_textu + 40, 'Q', 2**64 - 1),
               ('writable-code', Spracovanie_textu + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Spracovanie_textu, 'I', 2),
               ('unaligned-load', Spracovanie_textu + 16, 'Q', príkaz_adresa + 8),
               ('overlap', údaje + 16, 'Q', príkaz_adresa)]
    for Názov, Posun_VALUE, formát_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + formát_932e03c8, 바뀐자료, Posun_VALUE, VALUE)
        test_prípad.append((Názov, bytes(바뀐자료)))
    탑재덩이들 = [(Názov.replace('-', '_'), 출력결과 / (Názov + '.elf')) for Názov in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Názov, údajová_časť_údaje) in enumerate(test_prípad):
        Cesta = 출력결과 / ('invalid-{}.elf'.format(Názov)); Cesta.write_bytes(údajová_časť_údaje)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), Cesta))
    zostava, Nadpis_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Názov, Cesta in 탑재덩이들:
        symbol_VALUE = 'user_blob_' + Názov
        크기목록[Názov] = Cesta.stat().st_size
        # 생성한 partnerský_uzol_VALUE 경로만 넣어 프로젝트 경로의 공백/Citát 영향을 피한다.
        zostava += ['.balign 16', '.global ' + symbol_VALUE, symbol_VALUE + ':', '.incbin "{}"'.format(Cesta.relative_to(koreň_cesta))]
        Nadpis_VALUE.append('extern const unsigned char {}[];'.format(symbol_VALUE))
    zostava.append('.section .note.GNU-stack,"",%progbits')
    Nadpis_VALUE += ['static const program 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Nadpis_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Nadpis_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Nadpis_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metóda_MODE) for metóda_MODE in (0, 1)]
    Nadpis_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Nadpis_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Nadpis_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Nadpis_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Nadpis_VALUE += ['};', 'static const program 잘못된실행항목들[] = {']
    Nadpis_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(údajová_časť_údaje)) for 순번, (_, údajová_časť_údaje) in enumerate(test_prípad)]
    Nadpis_VALUE += ['};']
    (zostava_cesta / 'programs.S').write_text('\n'.join(zostava) + '\n')
    (zostava_cesta / 'programs.h').write_text('\n'.join(Nadpis_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Názov for Názov, _ in test_prípad) + '\n')
    Vykonať_príkaz([C_kompilátor] + konfigurácia_Background_Intelligent_Transfer_Service + ['-c', zostava_cesta / 'programs.S', '-o', zostava_cesta / 'programs.o'])
