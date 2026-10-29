"""독립된 eget ABI ELF64와 로더 avvisa_värde tester 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from version_PYTHON import Skapa_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from version_C_kompilerare import Skapa_C_kompilerare


def Skapa_användare_Space(rot_väg, centrallager_väg, C_kompilerare, 시플플번역기, länkare_verktyg, Arkiv_verktyg, konfiguration_BITS, köra_kommando):
    konfiguration_BITS = [Inställningar_värde for Inställningar_värde in konfiguration_BITS if Inställningar_värde != '-mgeneral-regs-only']
    version_väg = rot_väg / 'build'
    utleverans = version_väg / 'user'
    utleverans.mkdir(exist_ok=True)
    원본자료 = rot_väg / 'användarutrymme'
    포직스경로 = centrallager_väg / 'posix-kor/arm64-native'
    ta_med_väg = ['-I', 원본자료, '-I', 포직스경로 / 'deklarationer', '-I', utleverans]
    for kompilerare_verktyg, 추가영역, sökväg_2, Namn in [
            (C_kompilerare, [], 원본자료 / 'Kör.S', 'start.o'),
            (C_kompilerare, ['-std=c11'], 원본자료 / 'köra_kommando.c', 'runtime.o'),
            (C_kompilerare, ['-std=c11'], 포직스경로 / 'användare_brygga.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'Filexempel.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_kompilerare, ['-std=c11'], 원본자료 / 'Säkerhet_test.c', 'fault.o'),
            (C_kompilerare, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        köra_kommando([kompilerare_verktyg] + konfiguration_BITS + 추가영역 + ta_med_väg + ['-Wall', '-Wextra', '-Werror', '-c', sökväg_2, '-o', utleverans / Namn])
    köra_kommando([Arkiv_verktyg, 'rcs', version_väg / 'libposix-kor-user.a', utleverans / 'posix.o'])
    for Namn in ('demo', 'fault', 'network', 'vi'):
        köra_kommando([länkare_verktyg, '-T', 원본자료 / 'länkningslayout.ld', '-z', 'max-page-size=4096', '-o', utleverans / (Namn + '.elf'),
             utleverans / 'start.o', utleverans / 'runtime.o', utleverans / (Namn + '.o'), version_väg / 'libposix-kor-user.a'])
    자바라이브러리만들기(rot_väg, köra_kommando)
    # 기존 eget Java kompilerare/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(version_väg)) as 작업경로:
        Kurs_väg = Path(작업경로)
        köra_kommando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Kurs_väg, '-sourcepath', Kurs_väg, '-d', Kurs_väg] +
            [data_placera for data_placera in sorted((centrallager_väg / 'os/användarutrymme/자바').glob('*.java')) if data_placera.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        köra_kommando(['sh', centrallager_väg / 'compiler/미리번역.sh', '--entry', 'verktyg_post.Kör',
             '--profile', 'user', '--heap-words', '1048576', '-o', utleverans / 'java-tools.c'] + sorted(Kurs_väg.glob('*.class')))
    압축해제경로 = rot_väg / 'vendor/uzlib'
    for sökväg_2, Namn in [(utleverans / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'bunt.c', 'jar.o')] + [(압축해제경로 / (Namn + '.c'), Namn + '.o') for Namn in ('tinflate', 'crc32', 'adler32')]:
        köra_kommando([C_kompilerare] + konfiguration_BITS + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + ta_med_väg + ['-c', sökväg_2, '-o', utleverans / Namn])
    köra_kommando([länkare_verktyg, '-T', 원본자료 / 'länkningslayout.ld', '-z', 'max-page-size=4096', '-o', utleverans / 'java-tools.elf'] +
        [utleverans / Namn for Namn in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Skapa_PYTHON(rot_väg, C_kompilerare, länkare_verktyg)
    Skapa_C_kompilerare(rot_väg, centrallager_väg, C_kompilerare, länkare_verktyg, konfiguration_BITS, köra_kommando)
    giltig = (utleverans / 'demo.elf').read_bytes()
    app_huvud_FÖRSKJUTNING = struct.unpack_from('<Q', giltig, 32)[0]
    huvud_ange = [app_huvud_FÖRSKJUTNING + objekt_ANTAL * 56 for objekt_ANTAL in range(struct.unpack_from('<H', giltig, 56)[0])]
    적재구획 = [data_placera for data_placera in huvud_ange if struct.unpack_from('<I', giltig, data_placera)[0] == 1]
    text, data = 적재구획[:2]
    kommando_ADRESS = struct.unpack_from('<Q', giltig, text + 16)[0]
    data_ADRESS = struct.unpack_from('<Q', giltig, data + 16)[0]
    호출규약 = giltig.index(b'JKOROS\0')
    test_akt = [('empty', b''), ('short', giltig[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', kommando_ADRESS + 1), ('data-entry', 24, 'Q', data_ADRESS),
               ('outside-file', text + 32, 'Q', len(giltig) + 1), ('short-memory', text + 40, 'Q', 1),
               ('kernel-address', text + 16, 'Q', 0x80000), ('memory-overflow', text + 40, 'Q', 2**64 - 1),
               ('writable-code', text + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', text, 'I', 2),
               ('unaligned-load', text + 16, 'Q', kommando_ADRESS + 8),
               ('overlap', data + 16, 'Q', kommando_ADRESS)]
    for Namn, FÖRSKJUTNING_värde, format_932e03c8, värde in 수정사항:
        바뀐자료 = bytearray(giltig); struct.pack_into('<' + format_932e03c8, 바뀐자료, FÖRSKJUTNING_värde, värde)
        test_akt.append((Namn, bytes(바뀐자료)))
    탑재덩이들 = [(Namn.replace('-', '_'), utleverans / (Namn + '.elf')) for Namn in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LETAUPP_INDEX, (Namn, nyttolast_data) in enumerate(test_akt):
        sökväg_2 = utleverans / ('invalid-{}.elf'.format(Namn)); sökväg_2.write_bytes(nyttolast_data)
        탑재덩이들.append(('invalid_{}'.format(LETAUPP_INDEX), sökväg_2))
    montering, huvud_värde = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Namn, sökväg_2 in 탑재덩이들:
        symbol_värde = 'user_blob_' + Namn
        크기목록[Namn] = sökväg_2.stat().st_size
        # 생성한 peer_värde 경로만 넣어 프로젝트 경로의 공백/Citat 영향을 피한다.
        montering += ['.balign 16', '.global ' + symbol_värde, symbol_värde + ':', '.incbin "{}"'.format(sökväg_2.relative_to(rot_väg))]
        huvud_värde.append('extern const unsigned char {}[];'.format(symbol_värde))
    montering.append('.section .note.GNU-stack,"",%progbits')
    huvud_värde += ['static const app 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    huvud_värde += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    huvud_värde += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    huvud_värde += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metod_läge) for metod_läge in (0, 1)]
    huvud_värde += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    huvud_värde += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    huvud_värde += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    huvud_värde += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    huvud_värde += ['};', 'static const app 잘못된실행항목들[] = {']
    huvud_värde += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(nyttolast_data)) for 순번, (_, nyttolast_data) in enumerate(test_akt)]
    huvud_värde += ['};']
    (version_väg / 'programs.S').write_text('\n'.join(montering) + '\n')
    (version_väg / 'programs.h').write_text('\n'.join(huvud_värde) + '\n')
    (utleverans / 'invalid-cases.txt').write_text('\n'.join(Namn for Namn, _ in test_akt) + '\n')
    köra_kommando([C_kompilerare] + konfiguration_BITS + ['-c', version_väg / 'programs.S', '-o', version_väg / 'programs.o'])
