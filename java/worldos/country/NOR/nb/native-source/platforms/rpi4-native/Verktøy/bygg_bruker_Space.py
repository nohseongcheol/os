"""독립된 eget ABI ELF64와 로더 avvise_VERDI 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from bygg_PYTHON import åpne_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from bygg_C_kompilator import åpne_C_kompilator


def åpne_bruker_Space(rot_bane, repositorium_bane, C_kompilator, 시플플번역기, koblingsprogram_verktøy, Arkiv_verktøy, konfigurasjon_BITS, Utfør_kommando):
    konfigurasjon_BITS = [Innstillinger_VERDI for Innstillinger_VERDI in konfigurasjon_BITS if Innstillinger_VERDI != '-mgeneral-regs-only']
    bygg_bane = rot_bane / 'build'
    produksjon = bygg_bane / 'user'
    produksjon.mkdir(exist_ok=True)
    원본자료 = rot_bane / 'bruker'
    포직스경로 = repositorium_bane / 'posix-kor/arm64-native'
    inkludere_bane = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', produksjon]
    for kompilator_verktøy, 추가영역, Sti, Navn in [
            (C_kompilator, [], 원본자료 / 'Kjør_2.S', 'start.o'),
            (C_kompilator, ['-std=c11'], 원본자료 / 'Utfør_kommando.c', 'runtime.o'),
            (C_kompilator, ['-std=c11'], 포직스경로 / 'bruker_bro.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'Fileksempel.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_kompilator, ['-std=c11'], 원본자료 / 'Beskyttelse_test.c', 'fault.o'),
            (C_kompilator, ['-std=c11'], 원본자료 / 'Redaktør.c', 'vi.o')]:
        Utfør_kommando([kompilator_verktøy] + konfigurasjon_BITS + 추가영역 + inkludere_bane + ['-Wall', '-Wextra', '-Werror', '-c', Sti, '-o', produksjon / Navn])
    Utfør_kommando([Arkiv_verktøy, 'rcs', bygg_bane / 'libposix-kor-user.a', produksjon / 'posix.o'])
    for Navn in ('demo', 'fault', 'network', 'vi'):
        Utfør_kommando([koblingsprogram_verktøy, '-T', 원본자료 / 'koble_Oppsett.ld', '-z', 'max-page-size=4096', '-o', produksjon / (Navn + '.elf'),
             produksjon / 'start.o', produksjon / 'runtime.o', produksjon / (Navn + '.o'), bygg_bane / 'libposix-kor-user.a'])
    자바라이브러리만들기(rot_bane, Utfør_kommando)
    # 기존 eget Java kompilator/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(bygg_bane)) as 작업경로:
        time_bane = Path(작업경로)
        Utfør_kommando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', time_bane, '-sourcepath', time_bane, '-d', time_bane] +
            [data_plassere for data_plassere in sorted((repositorium_bane / 'os/bruker/자바').glob('*.java')) if data_plassere.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Utfør_kommando(['sh', repositorium_bane / 'compiler/미리번역.sh', '--entry', 'verktøy_oppføring.Kjør_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', produksjon / 'java-tools.c'] + sorted(time_bane.glob('*.class')))
    압축해제경로 = rot_bane / 'vendor/uzlib'
    for Sti, Navn in [(produksjon / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'bunt.c', 'jar.o')] + [(압축해제경로 / (Navn + '.c'), Navn + '.o') for Navn in ('tinflate', 'crc32', 'adler32')]:
        Utfør_kommando([C_kompilator] + konfigurasjon_BITS + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + inkludere_bane + ['-c', Sti, '-o', produksjon / Navn])
    Utfør_kommando([koblingsprogram_verktøy, '-T', 원본자료 / 'koble_Oppsett.ld', '-z', 'max-page-size=4096', '-o', produksjon / 'java-tools.elf'] +
        [produksjon / Navn for Navn in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    åpne_PYTHON(rot_bane, C_kompilator, koblingsprogram_verktøy)
    åpne_C_kompilator(rot_bane, repositorium_bane, C_kompilator, koblingsprogram_verktøy, konfigurasjon_BITS, Utfør_kommando)
    gyldig = (produksjon / 'demo.elf').read_bytes()
    app_Topptekst_FORSKYVNING = struct.unpack_from('<Q', gyldig, 32)[0]
    Topptekst_Liste = [app_Topptekst_FORSKYVNING + vare_ANTALL * 56 for vare_ANTALL in range(struct.unpack_from('<H', gyldig, 56)[0])]
    적재구획 = [data_plassere for data_plassere in Topptekst_Liste if struct.unpack_from('<I', gyldig, data_plassere)[0] == 1]
    Tekst, data = 적재구획[:2]
    kommando_e_post = struct.unpack_from('<Q', gyldig, Tekst + 16)[0]
    data_e_post = struct.unpack_from('<Q', gyldig, data + 16)[0]
    호출규약 = gyldig.index(b'JKOROS\0')
    test_sak = [('empty', b''), ('short', gyldig[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', kommando_e_post + 1), ('data-entry', 24, 'Q', data_e_post),
               ('outside-file', Tekst + 32, 'Q', len(gyldig) + 1), ('short-memory', Tekst + 40, 'Q', 1),
               ('kernel-address', Tekst + 16, 'Q', 0x80000), ('memory-overflow', Tekst + 40, 'Q', 2**64 - 1),
               ('writable-code', Tekst + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Tekst, 'I', 2),
               ('unaligned-load', Tekst + 16, 'Q', kommando_e_post + 8),
               ('overlap', data + 16, 'Q', kommando_e_post)]
    for Navn, FORSKYVNING_VERDI, format_932e03c8, VERDI in 수정사항:
        바뀐자료 = bytearray(gyldig); struct.pack_into('<' + format_932e03c8, 바뀐자료, FORSKYVNING_VERDI, VERDI)
        test_sak.append((Navn, bytes(바뀐자료)))
    탑재덩이들 = [(Navn.replace('-', '_'), produksjon / (Navn + '.elf')) for Navn in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for Oppslag_INDEKS, (Navn, nyttelast_data) in enumerate(test_sak):
        Sti = produksjon / ('invalid-{}.elf'.format(Navn)); Sti.write_bytes(nyttelast_data)
        탑재덩이들.append(('invalid_{}'.format(Oppslag_INDEKS), Sti))
    samling, Topptekst_VERDI = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Navn, Sti in 탑재덩이들:
        symbol_VERDI = 'user_blob_' + Navn
        크기목록[Navn] = Sti.stat().st_size
        # 생성한 node_VERDI_6a3b6fa7 경로만 넣어 프로젝트 경로의 공백/Sitat 영향을 피한다.
        samling += ['.balign 16', '.global ' + symbol_VERDI, symbol_VERDI + ':', '.incbin "{}"'.format(Sti.relative_to(rot_bane))]
        Topptekst_VERDI.append('extern const unsigned char {}[];'.format(symbol_VERDI))
    samling.append('.section .note.GNU-stack,"",%progbits')
    Topptekst_VERDI += ['static const app 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Topptekst_VERDI += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Topptekst_VERDI += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Topptekst_VERDI += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metode_MODUS) for metode_MODUS in (0, 1)]
    Topptekst_VERDI += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Topptekst_VERDI += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Topptekst_VERDI += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Topptekst_VERDI += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Topptekst_VERDI += ['};', 'static const app 잘못된실행항목들[] = {']
    Topptekst_VERDI += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(nyttelast_data)) for 순번, (_, nyttelast_data) in enumerate(test_sak)]
    Topptekst_VERDI += ['};']
    (bygg_bane / 'programs.S').write_text('\n'.join(samling) + '\n')
    (bygg_bane / 'programs.h').write_text('\n'.join(Topptekst_VERDI) + '\n')
    (produksjon / 'invalid-cases.txt').write_text('\n'.join(Navn for Navn, _ in test_sak) + '\n')
    Utfør_kommando([C_kompilator] + konfigurasjon_BITS + ['-c', bygg_bane / 'programs.S', '-o', bygg_bane / 'programs.o'])
