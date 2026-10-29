"""독립된 vlastní ABI ELF64와 로더 odmítnout_HODNOTA zkoušky 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from BLD_PYTHON import Create_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from BLD_C_kompilátor import Create_C_kompilátor


def Create_uživatel_Space(kořen_cesta, úložiště_cesta, C_kompilátor, 시플플번역기, linker_nástroj, Archiv_nástroj, konfigurace_BITS, Provést_příkaz):
    konfigurace_BITS = [Nastavení_HODNOTA for Nastavení_HODNOTA in konfigurace_BITS if Nastavení_HODNOTA != '-mgeneral-regs-only']
    BLD_cesta = kořen_cesta / 'build'
    výstup = BLD_cesta / 'user'
    výstup.mkdir(exist_ok=True)
    원본자료 = kořen_cesta / 'uživatelský_prostor'
    포직스경로 = úložiště_cesta / 'posix-kor/arm64-native'
    zahrnout_cesta = ['-I', 원본자료, '-I', 포직스경로 / 'deklarace', '-I', výstup]
    for kompilátor_nástroj, 추가영역, cesta_2, Název in [
            (C_kompilátor, [], 원본자료 / 'Spustit_2.S', 'start.o'),
            (C_kompilátor, ['-std=c11'], 원본자료 / 'Provést_příkaz.c', 'runtime.o'),
            (C_kompilátor, ['-std=c11'], 포직스경로 / 'uživatel_most.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'UkázkaSouboru.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_kompilátor, ['-std=c11'], 원본자료 / 'Ochrana_test.c', 'fault.o'),
            (C_kompilátor, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        Provést_příkaz([kompilátor_nástroj] + konfigurace_BITS + 추가영역 + zahrnout_cesta + ['-Wall', '-Wextra', '-Werror', '-c', cesta_2, '-o', výstup / Název])
    Provést_příkaz([Archiv_nástroj, 'rcs', BLD_cesta / 'libposix-kor-user.a', výstup / 'posix.o'])
    for Název in ('demo', 'fault', 'network', 'vi'):
        Provést_příkaz([linker_nástroj, '-T', 원본자료 / 'rozvržení_spojování.ld', '-z', 'max-page-size=4096', '-o', výstup / (Název + '.elf'),
             výstup / 'start.o', výstup / 'runtime.o', výstup / (Název + '.o'), BLD_cesta / 'libposix-kor-user.a'])
    자바라이브러리만들기(kořen_cesta, Provést_příkaz)
    # 기존 vlastní Java kompilátor/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(BLD_cesta)) as 작업경로:
        Třída_cesta = Path(작업경로)
        Provést_příkaz(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Třída_cesta, '-sourcepath', Třída_cesta, '-d', Třída_cesta] +
            [data_pozice for data_pozice in sorted((úložiště_cesta / 'os/uživatelský_prostor/자바').glob('*.java')) if data_pozice.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Provést_příkaz(['sh', úložiště_cesta / 'compiler/미리번역.sh', '--entry', 'nástroj_položka.Spustit_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', výstup / 'java-tools.c'] + sorted(Třída_cesta.glob('*.class')))
    압축해제경로 = kořen_cesta / 'vendor/uzlib'
    for cesta_2, Název in [(výstup / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'sada.c', 'jar.o')] + [(압축해제경로 / (Název + '.c'), Název + '.o') for Název in ('tinflate', 'crc32', 'adler32')]:
        Provést_příkaz([C_kompilátor] + konfigurace_BITS + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + zahrnout_cesta + ['-c', cesta_2, '-o', výstup / Název])
    Provést_příkaz([linker_nástroj, '-T', 원본자료 / 'rozvržení_spojování.ld', '-z', 'max-page-size=4096', '-o', výstup / 'java-tools.elf'] +
        [výstup / Název for Název in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Create_PYTHON(kořen_cesta, C_kompilátor, linker_nástroj)
    Create_C_kompilátor(kořen_cesta, úložiště_cesta, C_kompilátor, linker_nástroj, konfigurace_BITS, Provést_příkaz)
    platný = (výstup / 'demo.elf').read_bytes()
    program_Nadpis_POSUN = struct.unpack_from('<Q', platný, 32)[0]
    Nadpis_Seznam = [program_Nadpis_POSUN + zboží_POČET * 56 for zboží_POČET in range(struct.unpack_from('<H', platný, 56)[0])]
    적재구획 = [data_pozice for data_pozice in Nadpis_Seznam if struct.unpack_from('<I', platný, data_pozice)[0] == 1]
    text, data = 적재구획[:2]
    příkaz_ODKAZ = struct.unpack_from('<Q', platný, text + 16)[0]
    data_ODKAZ = struct.unpack_from('<Q', platný, data + 16)[0]
    VOLAT_ABI = platný.index(b'JKOROS\0')
    testovací_případ = [('empty', b''), ('short', platný[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', příkaz_ODKAZ + 1), ('data-entry', 24, 'Q', data_ODKAZ),
               ('outside-file', text + 32, 'Q', len(platný) + 1), ('short-memory', text + 40, 'Q', 1),
               ('kernel-address', text + 16, 'Q', 0x80000), ('memory-overflow', text + 40, 'Q', 2**64 - 1),
               ('writable-code', text + 4, 'I', 7), ('missing-abi', VOLAT_ABI, 'B', ord('X')),
               ('wrong-abi', VOLAT_ABI + 8, 'I', 2), ('dynamic', text, 'I', 2),
               ('unaligned-load', text + 16, 'Q', příkaz_ODKAZ + 8),
               ('overlap', data + 16, 'Q', příkaz_ODKAZ)]
    for Název, POSUN_HODNOTA, formát_932e03c8, HODNOTA in 수정사항:
        바뀐자료 = bytearray(platný); struct.pack_into('<' + formát_932e03c8, 바뀐자료, POSUN_HODNOTA, HODNOTA)
        testovací_případ.append((Název, bytes(바뀐자료)))
    탑재덩이들 = [(Název.replace('-', '_'), výstup / (Název + '.elf')) for Název in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for VYHLEDAT_INDEX, (Název, vytížení_data) in enumerate(testovací_případ):
        cesta_2 = výstup / ('invalid-{}.elf'.format(Název)); cesta_2.write_bytes(vytížení_data)
        탑재덩이들.append(('invalid_{}'.format(VYHLEDAT_INDEX), cesta_2))
    montáž, Nadpis_HODNOTA = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Název, cesta_2 in 탑재덩이들:
        symbol_HODNOTA = 'user_blob_' + Název
        크기목록[Název] = cesta_2.stat().st_size
        # 생성한 partner_HODNOTA 경로만 넣어 프로젝트 경로의 공백/Citát 영향을 피한다.
        montáž += ['.balign 16', '.global ' + symbol_HODNOTA, symbol_HODNOTA + ':', '.incbin "{}"'.format(cesta_2.relative_to(kořen_cesta))]
        Nadpis_HODNOTA.append('extern const unsigned char {}[];'.format(symbol_HODNOTA))
    montáž.append('.section .note.GNU-stack,"",%progbits')
    Nadpis_HODNOTA += ['static const program 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Nadpis_HODNOTA += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Nadpis_HODNOTA += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Nadpis_HODNOTA += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metoda_MODE) for metoda_MODE in (0, 1)]
    Nadpis_HODNOTA += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Nadpis_HODNOTA += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Nadpis_HODNOTA += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Nadpis_HODNOTA += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Nadpis_HODNOTA += ['};', 'static const program 잘못된실행항목들[] = {']
    Nadpis_HODNOTA += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(vytížení_data)) for 순번, (_, vytížení_data) in enumerate(testovací_případ)]
    Nadpis_HODNOTA += ['};']
    (BLD_cesta / 'programs.S').write_text('\n'.join(montáž) + '\n')
    (BLD_cesta / 'programs.h').write_text('\n'.join(Nadpis_HODNOTA) + '\n')
    (výstup / 'invalid-cases.txt').write_text('\n'.join(Název for Název, _ in testovací_případ) + '\n')
    Provést_příkaz([C_kompilátor] + konfigurace_BITS + ['-c', BLD_cesta / 'programs.S', '-o', BLD_cesta / 'programs.o'])
